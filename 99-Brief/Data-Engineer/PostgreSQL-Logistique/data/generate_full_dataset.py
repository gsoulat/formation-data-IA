"""
Script de generation du dataset complet TransFlow.

Ce script genere ~2.1 millions de livraisons (3 ans d'historique)
directement dans PostgreSQL. Il suppose que la base et les tables
sont deja creees via les scripts DDL de l'apprenant.

Usage:
    pip install psycopg2-binary faker
    python generate_full_dataset.py

Le script se connecte a PostgreSQL via les variables d'environnement :
    PGHOST (defaut: localhost)
    PGPORT (defaut: 5432)
    PGDATABASE (defaut: transflow)
    PGUSER (defaut: transflow)
    PGPASSWORD (defaut: transflow)
"""

import os
import random
import datetime
from collections import defaultdict

try:
    import psycopg2
    from psycopg2.extras import execute_values
except ImportError:
    print("Erreur: pip install psycopg2-binary")
    exit(1)

try:
    from faker import Faker
except ImportError:
    print("Erreur: pip install faker")
    exit(1)

fake = Faker("fr_FR")
random.seed(42)
Faker.seed(42)

# --- Configuration ---
NB_CLIENTS = 350
NB_VEHICULES = 120
NB_CHAUFFEURS = 180
NB_ENTREPOTS = 3
LIVRAISONS_PAR_JOUR_MOY = 1920  # ~700k/an
DATE_DEBUT = datetime.date(2021, 1, 1)
DATE_FIN = datetime.date(2023, 12, 31)
BATCH_SIZE = 5000

# --- Donnees de reference ---
ENTREPOTS = [
    (1, "TransFlow Lyon", "Lyon", "45 rue de la Part-Dieu", "69003", 45.7640, 4.8357, 12000, 8),
    (2, "TransFlow Bordeaux", "Bordeaux", "12 avenue des Chartrons", "33000", 44.8378, -0.5792, 8500, 5),
    (3, "TransFlow Lille", "Lille", "78 boulevard de la Liberte", "59000", 50.6292, 3.0573, 9200, 6),
]

TYPES_VEHICULES = [
    ("fourgonnette", 650, 4),
    ("fourgon", 1400, 13),
    ("camion", 8000, 40),
    ("camion", 12000, 55),
]

MARQUES = {
    "fourgonnette": [("Renault", "Kangoo"), ("Peugeot", "Partner"), ("Citroen", "Berlingo")],
    "fourgon": [("Renault", "Master"), ("Mercedes", "Sprinter"), ("Fiat", "Ducato"),
                ("Citroen", "Jumper"), ("Peugeot", "Boxer")],
    "camion": [("Renault", "D-Wide"), ("Volvo", "FL"), ("MAN", "TGL"),
               ("DAF", "LF"), ("Volvo", "FE"), ("MAN", "TGM")],
}

TYPES_CONTRAT = ["standard", "premium"]
PRIORITES = ["basse", "normale", "normale", "normale", "haute", "haute", "urgente"]
STATUTS_LIVRAISON = ["livree"] * 85 + ["livree_retard"] * 8 + ["en_cours"] * 3 + ["annulee"] * 2 + ["incident"] * 2
TYPES_INCIDENT = ["retard", "avarie", "retour", "perte_partielle"]
GRAVITES = ["mineur", "mineur", "mineur", "modere", "modere", "majeur"]

VILLES_LIVRAISON = [
    ("Paris", "75001", 465, 225, None),
    ("Lyon", "69001", 5, 5, 1),
    ("Villeurbanne", "69100", 8, 8, 1),
    ("Venissieux", "69200", 12, 12, 1),
    ("Ecully", "69130", 10, 10, 1),
    ("Bordeaux", "33000", 5, 556, 2),
    ("Merignac", "33700", 10, 560, 2),
    ("Pessac", "33600", 12, 558, 2),
    ("Talence", "33400", 8, 555, 2),
    ("Libourne", "33500", 35, 590, 2),
    ("Lille", "59000", 5, 690, 3),
    ("Villeneuve-d'Ascq", "59650", 12, 695, 3),
    ("Lomme", "59160", 8, 692, 3),
    ("Loos", "59120", 6, 688, 3),
    ("Douai", "59500", 40, 730, 3),
    ("Lesquin", "59810", 10, 695, 3),
    ("Roubaix", "59100", 15, 700, 3),
    ("Tourcoing", "59200", 18, 705, 3),
    ("Marseille", "13001", 315, 680, None),
    ("Toulouse", "31000", 540, 250, None),
    ("Nantes", "44000", 340, 350, None),
    ("Strasbourg", "67000", 490, 830, None),
    ("Montpellier", "34000", 305, 580, None),
    ("Rennes", "35000", 380, 610, None),
    ("Grenoble", "38000", 105, 660, None),
    ("Saint-Etienne", "42000", 60, 520, None),
    ("Dijon", "21000", 195, 540, None),
    ("Clermont-Ferrand", "63000", 170, 420, None),
]

DESCRIPTIONS_ARTICLES = [
    "Medicaments generiques",
    "Canapes et mobilier",
    "Farine et ingredients boulangerie",
    "Composants electroniques",
    "Vin AOC cartons",
    "Pieces detachees automobile",
    "Fruits et legumes bio",
    "Reactifs de laboratoire",
    "Textiles mode collection",
    "Produits bio epicerie",
    "Vins et spiritueux",
    "Filtres industriels",
    "Marchandises transit",
    "Produits frais marche",
    "Livres et papeterie",
    "Patisseries fines",
    "Materiel electrique",
    "Equipement informatique",
    "Cosmetiques",
    "Produits pharmaceutiques",
    "Mobilier de bureau",
    "Plantes et jardinage",
    "Equipement de laboratoire",
    "Produits chimiques",
    "Viande fraiche",
    "Fleurs coupees",
    "Metallurgie et toles",
    "Articles de sport",
    "Fournitures industrielles",
    "Materiel medical",
]


def get_connection():
    return psycopg2.connect(
        host=os.getenv("PGHOST", "localhost"),
        port=os.getenv("PGPORT", "5432"),
        dbname=os.getenv("PGDATABASE", "transflow"),
        user=os.getenv("PGUSER", "transflow"),
        password=os.getenv("PGPASSWORD", "transflow"),
    )


def generate_clients(cur):
    """Genere 350 clients avec quelques problemes de qualite volontaires."""
    print(f"Generation de {NB_CLIENTS} clients...")
    rows = []
    for i in range(1, NB_CLIENTS + 1):
        ville = fake.city()
        email = fake.company_email()
        telephone = fake.phone_number()

        # Problemes de qualite volontaires (~5%)
        siret = fake.siret() if random.random() > 0.05 else ""
        tel = telephone if random.random() > 0.03 else ""
        type_contrat = random.choice(TYPES_CONTRAT)
        volume = random.randint(500, 35000)
        date_debut = fake.date_between(start_date="-5y", end_date="-6M")
        actif = "oui" if random.random() > 0.08 else "non"

        # Quelques villes en majuscules pour tester le nettoyage
        if random.random() < 0.04:
            ville = ville.upper()

        rows.append((
            i, fake.company(), siret, fake.street_address(),
            fake.postcode(), ville, tel, email,
            type_contrat, volume, date_debut, actif,
        ))

    execute_values(cur, """
        INSERT INTO clients (id_client, raison_sociale, siret, adresse, code_postal,
            ville, telephone, email, type_contrat, volume_mensuel_kg,
            date_debut_contrat, actif)
        VALUES %s ON CONFLICT DO NOTHING
    """, rows)
    print(f"  -> {len(rows)} clients inseres.")
    return [r[0] for r in rows]


def generate_vehicules(cur):
    """Genere 120 vehicules repartis sur les 3 entrepots."""
    print(f"Generation de {NB_VEHICULES} vehicules...")
    rows = []
    repartition = [50, 35, 35]  # Lyon, Bordeaux, Lille

    idx = 1
    for entrepot_idx, nb in enumerate(repartition):
        for _ in range(nb):
            type_v, capacite_kg, capacite_m3 = random.choice(TYPES_VEHICULES)
            marque, modele = random.choice(MARQUES[type_v])
            immat = fake.license_plate()
            date_service = fake.date_between(start_date="-6y", end_date="-1y")
            date_maint = fake.date_between(start_date="-6M", end_date="today")
            km = random.randint(5000, 300000)
            statut = random.choices(
                ["disponible", "en_maintenance", "hors_service"],
                weights=[85, 10, 5],
            )[0]

            rows.append((
                idx, immat, type_v, marque, modele, capacite_kg, capacite_m3,
                entrepot_idx + 1, statut, date_service, date_maint, km,
            ))
            idx += 1

    execute_values(cur, """
        INSERT INTO vehicules (id_vehicule, immatriculation, type, marque, modele,
            capacite_kg, capacite_m3, id_entrepot, statut,
            date_mise_en_service, date_derniere_maintenance, km_compteur)
        VALUES %s ON CONFLICT DO NOTHING
    """, rows)
    print(f"  -> {len(rows)} vehicules inseres.")
    return rows


def generate_chauffeurs(cur):
    """Genere 180 chauffeurs."""
    print(f"Generation de {NB_CHAUFFEURS} chauffeurs...")
    rows = []
    repartition = [75, 52, 53]
    permis_options = ["B", "B+C", "B+C+CE"]

    idx = 1
    for entrepot_idx, nb in enumerate(repartition):
        for _ in range(nb):
            date_naissance = fake.date_of_birth(minimum_age=22, maximum_age=58)
            permis = random.choice(permis_options)
            # Quelques permis manquants
            if random.random() < 0.02:
                permis = ""
            date_embauche = fake.date_between(start_date="-6y", end_date="-3M")
            actif = "oui" if random.random() > 0.06 else "non"

            rows.append((
                idx, fake.last_name(), fake.first_name(), date_naissance,
                permis, fake.phone_number(),
                f"{fake.first_name().lower()}.{fake.last_name().lower()}@transflow.fr",
                entrepot_idx + 1, date_embauche, actif,
            ))
            idx += 1

    execute_values(cur, """
        INSERT INTO chauffeurs (id_chauffeur, nom, prenom, date_naissance, permis,
            telephone, email, id_entrepot, date_embauche, actif)
        VALUES %s ON CONFLICT DO NOTHING
    """, rows)
    print(f"  -> {len(rows)} chauffeurs inseres.")
    return rows


def generate_commandes_et_livraisons(cur, client_ids, vehicules, chauffeurs):
    """Genere ~2.1M livraisons sur 3 ans avec commandes associees."""

    # Index vehicules et chauffeurs par entrepot
    vehicules_par_entrepot = defaultdict(list)
    for v in vehicules:
        if v[7] in (1, 2, 3):  # id_entrepot
            vehicules_par_entrepot[v[7]].append(v[0])  # id_vehicule

    chauffeurs_par_entrepot = defaultdict(list)
    for c in chauffeurs:
        if c[9] == "oui":  # actif
            chauffeurs_par_entrepot[c[7]].append(c[0])  # id_chauffeur

    current_date = DATE_DEBUT
    id_commande = 1
    id_livraison = 1
    id_incident = 1
    total_jours = (DATE_FIN - DATE_DEBUT).days + 1

    commandes_batch = []
    livraisons_batch = []
    incidents_batch = []

    jour_count = 0

    while current_date <= DATE_FIN:
        jour_count += 1

        # Variation saisonniere : +20% en Q4, -15% en aout
        mois = current_date.month
        if mois in (10, 11, 12):
            facteur = 1.20
        elif mois == 8:
            facteur = 0.85
        elif mois in (6, 7):
            facteur = 0.95
        else:
            facteur = 1.0

        # Pas de livraison le dimanche, reduit le samedi
        jour_semaine = current_date.weekday()
        if jour_semaine == 6:
            current_date += datetime.timedelta(days=1)
            continue
        if jour_semaine == 5:
            facteur *= 0.3

        # Croissance annuelle +15%
        annee_offset = (current_date.year - DATE_DEBUT.year)
        facteur *= (1 + 0.15 * annee_offset)

        nb_livraisons_jour = int(LIVRAISONS_PAR_JOUR_MOY * facteur * random.uniform(0.85, 1.15))

        for _ in range(nb_livraisons_jour):
            id_client = random.choice(client_ids)

            # Repartition des departs : 42% Lyon, 29% Bordeaux, 29% Lille
            id_entrepot = random.choices([1, 2, 3], weights=[42, 29, 29])[0]

            # Destination : favoriser les villes proches de l'entrepot
            villes_proches = [v for v in VILLES_LIVRAISON if v[4] == id_entrepot]
            villes_loin = [v for v in VILLES_LIVRAISON if v[4] != id_entrepot]
            if random.random() < 0.7:
                dest = random.choice(villes_proches) if villes_proches else random.choice(VILLES_LIVRAISON)
            else:
                dest = random.choice(villes_loin) if villes_loin else random.choice(VILLES_LIVRAISON)

            ville_dest, cp_dest = dest[0], dest[1]
            distance = dest[2] if dest[4] == id_entrepot else dest[3]
            distance = int(distance * random.uniform(0.9, 1.1))

            nb_colis = random.randint(1, 50)
            poids = random.randint(10, 15000)
            volume = round(random.uniform(0.2, 40.0), 1)
            priorite = random.choice(PRIORITES)
            date_cmd = current_date - datetime.timedelta(days=random.randint(0, 3))
            date_souhaitee = current_date + datetime.timedelta(days=random.randint(0, 2))
            description = random.choice(DESCRIPTIONS_ARTICLES) + f" lot {fake.bothify('??-####')}"

            statut_liv = random.choice(STATUTS_LIVRAISON)
            statut_cmd = "livree" if statut_liv.startswith("livree") else statut_liv

            # Poids negatif (~0.1% - erreur de saisie volontaire)
            if random.random() < 0.001:
                poids = -poids

            commandes_batch.append((
                id_commande, id_client, description, nb_colis, poids, volume,
                date_cmd, date_souhaitee, priorite, statut_cmd,
            ))

            id_vehicule = random.choice(vehicules_par_entrepot[id_entrepot])
            id_chauffeur = random.choice(chauffeurs_par_entrepot[id_entrepot])

            heure_depart = datetime.time(
                random.randint(2, 8), random.choice([0, 15, 30, 45])
            )

            if statut_liv in ("livree", "livree_retard"):
                duree_h = max(0.5, distance / random.uniform(50, 80))
                if statut_liv == "livree_retard":
                    duree_h *= random.uniform(1.3, 2.0)
                delta = datetime.timedelta(hours=duree_h)
                dt_depart = datetime.datetime.combine(current_date, heure_depart)
                dt_arrivee = dt_depart + delta
                date_arrivee = dt_arrivee.date()
                heure_arrivee = dt_arrivee.time().replace(microsecond=0)
            else:
                date_arrivee = None
                heure_arrivee = None

            commentaire = ""
            if statut_liv == "livree_retard":
                commentaire = random.choice([
                    "retard cause bouchons",
                    "attente au quai",
                    "detour travaux",
                    "panne temporaire",
                    "controle routier",
                ])

            livraisons_batch.append((
                id_livraison, id_commande, id_vehicule, id_chauffeur,
                id_entrepot, ville_dest, cp_dest, distance,
                current_date, heure_depart,
                date_arrivee, heure_arrivee,
                "livree" if statut_liv == "livree_retard" else statut_liv,
                commentaire,
            ))

            # Incidents (~3% des livraisons)
            if statut_liv in ("livree_retard", "incident") or random.random() < 0.01:
                type_inc = random.choice(TYPES_INCIDENT)
                gravite = random.choice(GRAVITES)
                resolu = "oui" if random.random() > 0.15 else "non"
                date_resolution = (
                    current_date + datetime.timedelta(days=random.randint(0, 3))
                    if resolu == "oui" else None
                )
                incidents_batch.append((
                    id_incident, id_livraison, type_inc,
                    f"Incident {type_inc} sur livraison {id_livraison}",
                    current_date,
                    datetime.time(random.randint(5, 18), random.randint(0, 59)),
                    gravite, resolu, date_resolution,
                ))
                id_incident += 1

            id_commande += 1
            id_livraison += 1

        # Flush par batch
        if len(commandes_batch) >= BATCH_SIZE:
            _flush_commandes(cur, commandes_batch)
            _flush_livraisons(cur, livraisons_batch)
            _flush_incidents(cur, incidents_batch)
            commandes_batch.clear()
            livraisons_batch.clear()
            incidents_batch.clear()

        if jour_count % 30 == 0:
            progression = jour_count / total_jours * 100
            print(f"  -> {progression:.0f}% ({id_livraison - 1:,} livraisons generees)")

        current_date += datetime.timedelta(days=1)

    # Flush final
    if commandes_batch:
        _flush_commandes(cur, commandes_batch)
        _flush_livraisons(cur, livraisons_batch)
        _flush_incidents(cur, incidents_batch)

    print(f"\nGeneration terminee :")
    print(f"  - {id_commande - 1:,} commandes")
    print(f"  - {id_livraison - 1:,} livraisons")
    print(f"  - {id_incident - 1:,} incidents")


def _flush_commandes(cur, batch):
    execute_values(cur, """
        INSERT INTO commandes (id_commande, id_client, description_articles, nb_colis,
            poids_total_kg, volume_total_m3, date_commande, date_livraison_souhaitee,
            priorite, statut)
        VALUES %s ON CONFLICT DO NOTHING
    """, batch)


def _flush_livraisons(cur, batch):
    execute_values(cur, """
        INSERT INTO livraisons (id_livraison, id_commande, id_vehicule, id_chauffeur,
            id_entrepot_depart, ville_destination, code_postal_destination, distance_km,
            date_depart, heure_depart, date_arrivee, heure_arrivee, statut, commentaire)
        VALUES %s ON CONFLICT DO NOTHING
    """, batch)


def _flush_incidents(cur, batch):
    if not batch:
        return
    execute_values(cur, """
        INSERT INTO incidents (id_incident, id_livraison, type_incident, description,
            date_incident, heure_incident, gravite, resolu, date_resolution)
        VALUES %s ON CONFLICT DO NOTHING
    """, batch)


def main():
    print("=" * 60)
    print("TransFlow - Generation du dataset complet")
    print("=" * 60)

    conn = get_connection()
    conn.autocommit = False
    cur = conn.cursor()

    try:
        print("\n[1/4] Generation des clients...")
        client_ids = generate_clients(cur)
        conn.commit()

        print("\n[2/4] Generation des vehicules...")
        vehicules = generate_vehicules(cur)
        conn.commit()

        print("\n[3/4] Generation des chauffeurs...")
        chauffeurs = generate_chauffeurs(cur)
        conn.commit()

        print("\n[4/4] Generation des commandes, livraisons et incidents...")
        generate_commandes_et_livraisons(cur, client_ids, vehicules, chauffeurs)
        conn.commit()

        print("\nToutes les donnees ont ete inserees avec succes.")

    except Exception as e:
        conn.rollback()
        print(f"\nErreur: {e}")
        raise
    finally:
        cur.close()
        conn.close()


if __name__ == "__main__":
    main()
