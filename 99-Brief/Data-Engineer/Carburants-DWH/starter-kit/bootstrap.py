#!/usr/bin/env python3
"""
KIT DE DEMARRAGE — Chargement initial de l'entrepôt Rouleo.

Ce script constitue l'HISTORIQUE DE DEPART dont vous héritez. Il télécharge
l'archive annuelle officielle des prix des carburants (données réelles), la
parcourt en flux (iterparse : le fichier décompressé pèse ~386 Mo) et alimente
le schéma en étoile.

Il n'est PAS le sujet du brief : ne le réécrivez pas. Mais lisez-le, car
plusieurs de ses choix sont contestables et feront partie de votre audit —
à commencer par le stockage des coordonnées géographiques telles que publiées.

Usage :
    python3 bootstrap.py --annee 2025 --departements 59,62
    python3 bootstrap.py --annee 2025                    # France entière (long)

Dépendances : psycopg2-binary
Connexion : variables d'environnement PGHOST / PGPORT / PGDATABASE / PGUSER / PGPASSWORD
"""

import argparse
import calendar
import datetime as dt
import os
import sys
import urllib.request
import xml.etree.ElementTree as ET
import zipfile
from pathlib import Path

import psycopg2
from psycopg2.extras import execute_values

URL_ARCHIVE = "https://donnees.roulez-eco.fr/opendata/annee/{annee}"
CACHE = Path(__file__).parent / "data"
LOT = 5000

JOURS = ["Lundi", "Mardi", "Mercredi", "Jeudi", "Vendredi", "Samedi", "Dimanche"]
MOIS = ["", "janvier", "février", "mars", "avril", "mai", "juin",
        "juillet", "août", "septembre", "octobre", "novembre", "décembre"]


def telecharger(annee):
    """Télécharge l'archive annuelle si elle n'est pas déjà en cache."""
    CACHE.mkdir(exist_ok=True)
    cible = CACHE / f"PrixCarburants_annuel_{annee}.zip"
    if cible.exists():
        print(f"[cache] {cible} ({cible.stat().st_size / 1e6:.0f} Mo)")
        return cible
    url = URL_ARCHIVE.format(annee=annee)
    print(f"[telechargement] {url}")
    urllib.request.urlretrieve(url, cible)
    print(f"[ok] {cible} ({cible.stat().st_size / 1e6:.0f} Mo)")
    return cible


def nombre(valeur):
    """Convertit en flottant, ou None. La source mélange entiers et décimaux."""
    try:
        return float(valeur)
    except (TypeError, ValueError):
        return None


def departement(code_postal):
    """Département déduit du code postal (les DOM tiennent sur 3 chiffres)."""
    if not code_postal:
        return None
    code_postal = code_postal.strip()
    if code_postal.startswith(("97", "98")):
        return code_postal[:3]
    return code_postal[:2]


def charger_dim_temps(cur, annee):
    """Génère l'année complète dans la dimension temps."""
    lignes = []
    debut = dt.date(annee, 1, 1)
    for n in range(366 if calendar.isleap(annee) else 365):
        j = debut + dt.timedelta(days=n)
        lignes.append((
            int(j.strftime("%Y%m%d")), j, j.year, (j.month - 1) // 3 + 1,
            j.month, MOIS[j.month], j.day, JOURS[j.weekday()], j.weekday() >= 5,
        ))
    execute_values(cur, """
        INSERT INTO entrepot.dim_temps
            (temps_id, date_jour, annee, trimestre, mois, nom_mois, jour, jour_semaine, est_weekend)
        VALUES %s ON CONFLICT (temps_id) DO NOTHING
    """, lignes)
    print(f"[dim_temps] {len(lignes)} jours")


def parcourir(chemin_zip, prefixes):
    """Parcourt l'archive en flux et rend (station, releves) point de vente par point de vente."""
    with zipfile.ZipFile(chemin_zip) as z:
        nom_xml = next(n for n in z.namelist() if n.lower().endswith(".xml"))
        print(f"[archive] membre {nom_xml}")
        with z.open(nom_xml) as flux:
            contexte = ET.iterparse(flux, events=("end",))
            for _, elem in contexte:
                if elem.tag != "pdv":
                    continue
                cp = (elem.get("cp") or "").strip()
                dept = departement(cp)
                if prefixes and dept not in prefixes:
                    elem.clear()
                    continue

                horaires = elem.find("horaires")
                services = [s.text for s in elem.findall("./services/service") if s.text]
                station = (
                    elem.get("id"),
                    (elem.findtext("adresse") or "").strip()[:200] or None,
                    (elem.findtext("ville") or "").strip()[:120] or None,
                    cp or None,
                    dept,
                    elem.get("pop"),
                    # NOTE (héritage) : valeurs stockées TELLES QUELLES.
                    # Ce ne sont pas des degrés. Personne ne l'a jamais vérifié.
                    nombre(elem.get("latitude")),
                    nombre(elem.get("longitude")),
                    "|".join(services) or None,
                    horaires is not None and horaires.get("automate-24-24") == "1",
                )

                releves = []
                for p in elem.findall("prix"):
                    valeur, maj = p.get("valeur"), p.get("maj")
                    if not valeur or not maj:
                        continue
                    try:
                        horodatage = dt.datetime.fromisoformat(maj)
                        releves.append((
                            station[0], int(p.get("id")),
                            int(horodatage.strftime("%Y%m%d")), horodatage, float(valeur),
                        ))
                    except (ValueError, TypeError):
                        continue

                carburants = {(int(p.get("id")), p.get("nom"))
                              for p in elem.findall("prix") if p.get("id") and p.get("nom")}
                yield station, releves, carburants
                elem.clear()


def main():
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--annee", type=int, default=2025)
    ap.add_argument("--departements", default="",
                    help="liste séparée par des virgules, ex : 59,62,75 (vide = France entière)")
    args = ap.parse_args()

    prefixes = {d.strip() for d in args.departements.split(",") if d.strip()}
    chemin_zip = telecharger(args.annee)

    conn = psycopg2.connect("")
    conn.autocommit = False
    cur = conn.cursor()
    # La dimension temps couvre largement : l'archive, l'année courante, et les
    # années intermédiaires. Le flux temps réel contient en effet des relevés
    # dont la dernière mise à jour remonte à plus d'un an — des stations dont
    # personne n'a corrigé le prix depuis longtemps.
    courante = dt.date.today().year
    for annee in range(min(args.annee, courante) - 2, max(args.annee, courante) + 1):
        charger_dim_temps(cur, annee)

    stations, releves, carburants = [], [], set()
    n_stations = n_releves = n_sans_prix = 0

    for station, prix, carbs in parcourir(chemin_zip, prefixes):
        stations.append(station)
        releves.extend(prix)
        carburants |= carbs
        n_stations += 1
        n_releves += len(prix)
        if not prix:
            n_sans_prix += 1

        # Les dimensions sont toujours écrites AVANT les faits qui les référencent :
        # une station n'est pas encore en base tant que son lot n'a pas été vidé.
        if len(stations) >= LOT or len(releves) >= LOT * 10:
            ecrire_stations(cur, stations)
            ecrire_carburants(cur, carburants)
            ecrire_releves(cur, releves)
            stations, releves = [], []

    ecrire_stations(cur, stations)
    ecrire_carburants(cur, carburants)
    ecrire_releves(cur, releves)
    conn.commit()
    cur.close()
    conn.close()

    print(f"[termine] {n_stations} stations, {n_releves} relevés, "
          f"{n_sans_prix} stations sans aucun relevé")


def ecrire_stations(cur, lignes):
    if not lignes:
        return
    # NOTE (héritage) : mise à jour PAR ECRASEMENT. Aucune trace de l'état précédent.
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
    """, lignes, page_size=1000)


def ecrire_carburants(cur, carburants):
    if not carburants:
        return
    execute_values(cur, """
        INSERT INTO entrepot.dim_carburant (carburant_id, nom)
        VALUES %s ON CONFLICT (carburant_id) DO NOTHING
    """, sorted(carburants))


def ecrire_releves(cur, lignes):
    if not lignes:
        return
    # NOTE (héritage) : INSERT sec. Rejouer ce script duplique tous les relevés.
    execute_values(cur, """
        INSERT INTO entrepot.fait_prix
            (station_id, carburant_id, temps_id, horodatage, prix)
        VALUES %s
    """, lignes, page_size=5000)


if __name__ == "__main__":
    sys.exit(main())
