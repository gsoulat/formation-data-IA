#!/usr/bin/env python3
"""
KIT DE DEMARRAGE — L'ETL nocturne HERITE du prédécesseur.

NE PAS AMELIORER CE FICHIER : il représente l'existant que vous devez auditer
puis remplacer. Ses défauts sont volontaires et documentés dans le brief :

  1. mise à jour de dim_station PAR ECRASEMENT (ON CONFLICT DO UPDATE)
     -> c'est lui, le coupable de « l'analyse autoroute de janvier a changé » ;
  2. AUCUNE journalisation, AUCUNE alerte : s'il plante à 3 h du matin,
     personne ne le sait — l'application sert des prix périmés ;
  3. non idempotent : le relancer le même jour duplique tous les relevés ;
  4. aucune gestion d'erreurs : le moindre incident réseau stoppe tout ;
  5. pagination naïve : l'API plafonne à limit + offset <= 10 000 et le réseau
     compte aujourd'hui ~9 800 stations. Le jour où il en comptera 10 001,
     ce script en chargera silencieusement une partie seulement ;
  6. il écrit les coordonnées du flux JSON dans les mêmes colonnes que
     l'archive XML, sans se demander si les deux sources emploient la même
     unité ni le même type.

Usage : python3 etl_nocturne.py
Dépendances : psycopg2-binary
Connexion : variables d'environnement PGHOST / PGPORT / PGDATABASE / PGUSER / PGPASSWORD
"""

import datetime as dt
import gzip
import json
import urllib.request

import psycopg2
from psycopg2.extras import execute_values

API = ("https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/"
       "prix-des-carburants-en-france-flux-instantane-v2/records")

# Identifiants alignés sur ceux de l'archive annuelle officielle.
CARBURANTS = {
    "gazole": 1, "sp95": 2, "e85": 3, "gplc": 4, "e10": 5, "sp98": 6,
}


def nombre(valeur):
    """Convertit en flottant, ou None."""
    try:
        return float(valeur)
    except (TypeError, ValueError):
        return None


def appeler(url):
    """Appelle l'API et rend le JSON décodé.

    Le service répond en gzip même quand on ne le demande pas : il faut
    décompresser explicitement.
    """
    requete = urllib.request.Request(url, headers={"User-Agent": "rouleo-etl/1.0"})
    with urllib.request.urlopen(requete) as reponse:
        brut = reponse.read()
        if reponse.headers.get("Content-Encoding") == "gzip":
            brut = gzip.decompress(brut)
    return json.loads(brut.decode("utf-8"))


def lire_flux():
    """Récupère toutes les stations du flux instantané, 100 par 100."""
    stations, offset = [], 0
    while True:
        page = appeler(f"{API}?limit=100&offset={offset}")
        resultats = page.get("results", [])
        if not resultats:
            break
        stations.extend(resultats)
        offset += 100
    print(f"{len(stations)} stations lues")
    return stations


def main():
    conn = psycopg2.connect("")
    cur = conn.cursor()

    stations = lire_flux()

    # 1. Mise à jour des stations — PAR ECRASEMENT (aucune trace de l'état précédent)
    lignes_stations = [(
        str(s["id"]),
        (s.get("adresse") or "")[:200] or None,
        (s.get("ville") or "")[:120] or None,
        s.get("cp"),
        s.get("code_departement"),
        s.get("pop"),
        nombre(s.get("latitude")),
        nombre(s.get("longitude")),
        "|".join(s.get("services_service") or []) or None,
        s.get("horaires_automate_24_24") == "Oui",
    ) for s in stations]

    execute_values(cur, """
        INSERT INTO entrepot.dim_station
            (station_id, adresse, ville, code_postal, code_departement, type_voirie,
             latitude_brute, longitude_brute, services, automate_24_24)
        VALUES %s
        ON CONFLICT (station_id) DO UPDATE SET
            adresse          = EXCLUDED.adresse,
            ville            = EXCLUDED.ville,
            code_postal      = EXCLUDED.code_postal,
            code_departement = EXCLUDED.code_departement,
            type_voirie      = EXCLUDED.type_voirie,
            latitude_brute   = EXCLUDED.latitude_brute,
            longitude_brute  = EXCLUDED.longitude_brute,
            services         = EXCLUDED.services,
            automate_24_24   = EXCLUDED.automate_24_24,
            date_chargement  = now()
    """, lignes_stations, page_size=1000)

    # 2. Chargement des relevés — INSERT sec, aucun garde-fou contre le rejeu
    releves = []
    for s in stations:
        for prefixe, carburant_id in CARBURANTS.items():
            prix = s.get(f"{prefixe}_prix")
            maj = s.get(f"{prefixe}_maj")
            if prix is None or not maj:
                continue
            horodatage = dt.datetime.fromisoformat(maj).replace(tzinfo=None)
            releves.append((
                str(s["id"]), carburant_id,
                int(horodatage.strftime("%Y%m%d")), horodatage, prix, "flux_instantane",
            ))

    execute_values(cur, """
        INSERT INTO entrepot.fait_prix
            (station_id, carburant_id, temps_id, horodatage, prix, source)
        VALUES %s
    """, releves, page_size=5000)

    conn.commit()
    cur.close()
    conn.close()
    print(f"{len(releves)} relevés chargés")


if __name__ == "__main__":
    main()
