"""
Générateur de jeux de données pédagogiques — Formation Data Analyst (RNCP-38616 / BC06)
=======================================================================================
Univers fictif « NordRetail » : enseigne de distribution des Hauts-de-France.
Données 100 % reproductibles (seed=42). Aucune donnée personnelle réelle.

Usage :
    pip install pandas numpy openpyxl
    python generate_datasets.py

Produit, dans le même dossier, les fichiers utilisés par les cours et les TP.
Voir README.md pour la correspondance fichier ↔ module.
"""

from pathlib import Path
import numpy as np
import pandas as pd

OUT = Path(__file__).parent
rng = np.random.default_rng(42)

# --------------------------------------------------------------------------------------
# 1. DIMENSIONS
# --------------------------------------------------------------------------------------
magasins = pd.DataFrame([
    # id, ville, type, surface_m2, date_ouverture
    (1, "Lille",        "Magasin",   2400, "2015-03-12"),
    (2, "Roubaix",      "Magasin",   1800, "2017-09-01"),
    (3, "Tourcoing",    "Magasin",   1500, "2018-06-15"),
    (4, "Dunkerque",    "Magasin",   2100, "2016-11-20"),
    (5, "Valenciennes", "Magasin",   1300, "2019-02-04"),
    (6, "Amiens",       "Magasin",   1700, "2020-10-10"),
    (7, "En ligne",     "E-commerce",   0, "2014-01-01"),
], columns=["magasin_id", "ville", "type", "surface_m2", "date_ouverture"])

categories = {
    "Sport":          ["Vélo VTT", "Raquette tennis", "Ballon foot", "Tapis yoga", "Haltères 10kg", "Maillot bain", "Chaussures running"],
    "Mode":           ["Jean homme", "Robe été", "Veste hiver", "T-shirt coton", "Pull laine", "Baskets ville"],
    "Maison":         ["Canapé 3 places", "Lampe LED", "Set casseroles", "Couette 220x240", "Étagère bois", "Rideau occultant"],
    "Électroménager": ["Aspirateur", "Cafetière", "Micro-ondes", "Bouilloire", "Robot cuiseur", "Réfrigérateur"],
    "Bricolage":      ["Perceuse", "Tournevis set", "Peinture 5L", "Échelle alu", "Boîte à outils"],
}

prod_rows, pid = [], 1
for cat, items in categories.items():
    for nom in items:
        cout = round(float(rng.uniform(5, 400)), 2)
        marge = float(rng.uniform(1.25, 2.4))
        prix = round(cout * marge, 2)
        prod_rows.append((pid, nom, cat, prix, cout))
        pid += 1
produits = pd.DataFrame(prod_rows, columns=["produit_id", "produit", "categorie", "prix_unitaire", "cout_unitaire"])

# Clients
prenoms = ["Camille", "Lucas", "Léa", "Hugo", "Manon", "Nathan", "Chloé", "Enzo", "Jade", "Louis",
           "Inès", "Gabriel", "Sarah", "Raphaël", "Emma", "Maël", "Lina", "Adam", "Zoé", "Noah"]
noms = ["Dubois", "Lefebvre", "Vandamme", "Delattre", "Carlier", "Dhaussy", "Lemoine", "Becquart",
        "Vasseur", "Crombez", "Delplace", "Hennion", "Wattel", "Lecocq", "Druon", "Masson"]
villes_clients = ["Lille", "Roubaix", "Tourcoing", "Dunkerque", "Valenciennes", "Amiens", "Arras", "Douai", "Lens", "Calais"]
segments = ["Particulier", "Particulier", "Particulier", "Premium", "Professionnel"]

n_clients = 600
clients = pd.DataFrame({
    "client_id": np.arange(1, n_clients + 1),
    "prenom": rng.choice(prenoms, n_clients),
    "nom": rng.choice(noms, n_clients),
    "ville": rng.choice(villes_clients, n_clients, p=[.28, .14, .1, .1, .08, .08, .05, .06, .06, .05]),
    "segment": rng.choice(segments, n_clients),
    "date_inscription": pd.to_datetime("2020-01-01") + pd.to_timedelta(rng.integers(0, 365 * 5, n_clients), unit="D"),
})
clients["email"] = (clients["prenom"].str.lower() + "." + clients["nom"].str.lower()
                    + rng.integers(1, 99, n_clients).astype(str) + "@email.fr")

# --------------------------------------------------------------------------------------
# 2. TABLE DE FAITS — transactions de ventes 2023-2024 avec saisonnalité
# --------------------------------------------------------------------------------------
n = 12000
dates = pd.to_datetime("2023-01-01") + pd.to_timedelta(rng.integers(0, 730, n), unit="D")

def saison_factor(d):
    m = d.month
    f = 1.0
    if m in (1, 7):   f *= 1.5   # soldes
    if m == 12:       f *= 1.8   # Noël
    if m in (2, 11):  f *= 0.85
    return f

prod_idx = rng.integers(0, len(produits), n)
mag = rng.choice(magasins["magasin_id"], n, p=[.22, .16, .12, .15, .1, .12, .13])
cli = rng.integers(1, n_clients + 1, n)
base_q = rng.integers(1, 6, n)
season = np.array([saison_factor(d) for d in dates])
quantite = np.maximum(1, np.round(base_q * (0.7 + 0.6 * rng.random(n)) * (season / season.mean()))).astype(int)

prix = produits.loc[prod_idx, "prix_unitaire"].to_numpy()
cout = produits.loc[prod_idx, "cout_unitaire"].to_numpy()
remise = rng.choice([0, 0, 0, 0.05, 0.1, 0.2], n, p=[.55, .15, .1, .1, .07, .03])
montant = np.round(prix * quantite * (1 - remise), 2)
marge = np.round((prix * (1 - remise) - cout) * quantite, 2)

faits = pd.DataFrame({
    "vente_id": np.arange(1, n + 1),
    "date": dates,
    "magasin_id": mag,
    "produit_id": produits.loc[prod_idx, "produit_id"].to_numpy(),
    "client_id": cli,
    "quantite": quantite,
    "prix_unitaire": prix,
    "remise": remise,
    "montant": montant,
    "marge": marge,
}).sort_values("date").reset_index(drop=True)
faits["vente_id"] = np.arange(1, n + 1)

# --------------------------------------------------------------------------------------
# 3. VENTES "À PLAT" propre — ventes_magasins.csv (cours Maths ch.3 + module 1.2)
# --------------------------------------------------------------------------------------
ventes = (faits
          .merge(magasins[["magasin_id", "ville", "type"]], on="magasin_id")
          .merge(produits[["produit_id", "produit", "categorie"]], on="produit_id"))
ventes_plat = ventes[["date", "ville", "type", "categorie", "produit",
                      "quantite", "prix_unitaire", "remise", "montant", "marge", "client_id"]].copy()
ventes_plat = ventes_plat.sort_values("date").reset_index(drop=True)
ventes_plat.to_csv(OUT / "ventes_magasins.csv", index=False)
ventes_plat.to_csv(OUT / "ventes_retail_nord.csv", index=False)  # alias

# --------------------------------------------------------------------------------------
# 4. VERSION "SALE" — ventes_sales.csv / ventes_corrompu.csv (module 3.3 nettoyage)
# --------------------------------------------------------------------------------------
sale = ventes_plat.copy()
sale["date"] = sale["date"].dt.strftime("%Y-%m-%d")

# dates en formats mélangés (1 sur 5 en JJ/MM/AAAA)
mask_fmt = rng.random(len(sale)) < 0.2
sale.loc[mask_fmt, "date"] = pd.to_datetime(sale.loc[mask_fmt, "date"]).dt.strftime("%d/%m/%Y")
# casse de ville incohérente + espaces parasites
def messy_city(v, r):
    if r < 0.15: return v.upper()
    if r < 0.30: return v.lower()
    if r < 0.40: return f"  {v} "
    return v
rr = rng.random(len(sale))
sale["ville"] = [messy_city(v, r) for v, r in zip(sale["ville"], rr)]
# valeurs manquantes
sale.loc[rng.random(len(sale)) < 0.05, "client_id"] = np.nan
sale.loc[rng.random(len(sale)) < 0.04, "quantite"] = np.nan
sale.loc[rng.random(len(sale)) < 0.03, "montant"] = np.nan
# montant avec virgule décimale (texte) sur une partie
mask_comma = rng.random(len(sale)) < 0.1
sale["montant"] = sale["montant"].astype("object")
sale.loc[mask_comma, "montant"] = sale.loc[mask_comma, "montant"].apply(
    lambda x: str(x).replace(".", ",") if pd.notna(x) else x)
# quantités négatives (retours mal saisis) + outliers absurdes
idx_neg = rng.choice(len(sale), 40, replace=False)
sale.loc[idx_neg, "quantite"] = -sale.loc[idx_neg, "quantite"].fillna(1).astype(float).abs()
idx_out = rng.choice(len(sale), 8, replace=False)
sale.loc[idx_out, "quantite"] = rng.choice([999, 5000, 9999], 8)
# doublons exacts
dups = sale.sample(35, random_state=0)
sale = pd.concat([sale, dups], ignore_index=True)
sale = sale.sample(frac=1, random_state=1).reset_index(drop=True)
sale.to_csv(OUT / "ventes_sales.csv", index=False)
sale.to_csv(OUT / "ventes_corrompu.csv", index=False)  # alias

# --------------------------------------------------------------------------------------
# 5. SCHÉMA EN ÉTOILE — Dim_*, Dim_Date, Faits_Ventes (module 2.2 modélisation)
# --------------------------------------------------------------------------------------
magasins.to_csv(OUT / "Dim_Magasin.csv", index=False)
produits.to_csv(OUT / "Dim_Produit.csv", index=False)
clients.assign(date_inscription=clients["date_inscription"].dt.strftime("%Y-%m-%d")) \
       .to_csv(OUT / "Dim_Client.csv", index=False)

dmin, dmax = faits["date"].min(), faits["date"].max()
drange = pd.date_range(dmin, dmax, freq="D")
mois_fr = ["janvier", "février", "mars", "avril", "mai", "juin",
           "juillet", "août", "septembre", "octobre", "novembre", "décembre"]
jours_fr = ["lundi", "mardi", "mercredi", "jeudi", "vendredi", "samedi", "dimanche"]
dim_date = pd.DataFrame({
    "date_id": drange.strftime("%Y%m%d").astype(int),
    "date": drange.strftime("%Y-%m-%d"),
    "annee": drange.year,
    "trimestre": "T" + drange.quarter.astype(str),
    "mois": drange.month,
    "nom_mois": [mois_fr[m - 1] for m in drange.month],
    "jour": drange.day,
    "jour_semaine": [jours_fr[d] for d in drange.dayofweek],
    "est_weekend": (drange.dayofweek >= 5).astype(int),
})
dim_date.to_csv(OUT / "Dim_Date.csv", index=False)

faits_star = faits.copy()
faits_star["date_id"] = faits_star["date"].dt.strftime("%Y%m%d").astype(int)
faits_star = faits_star[["vente_id", "date_id", "magasin_id", "produit_id",
                         "client_id", "quantite", "prix_unitaire", "remise", "montant", "marge"]]
faits_star.to_csv(OUT / "Faits_Ventes.csv", index=False)

# --------------------------------------------------------------------------------------
# 6. FICHIERS MULTI-MAGASINS — pour l'ETL de consolidation (module 3.2)
#    Formats volontairement hétérogènes pour rendre la consolidation formatrice.
# --------------------------------------------------------------------------------------
for mid, ville in [(1, "lille"), (2, "roubaix"), (3, "tourcoing"), (5, "valenciennes")]:
    sub = ventes_plat[ventes_plat["ville"] == ville.capitalize()][
        ["date", "categorie", "produit", "quantite", "montant"]].copy()
    if ville == "lille":            # séparateur point-virgule + en-têtes FR
        sub.to_csv(OUT / f"ventes_{ville}.csv", index=False, sep=";")
    elif ville == "roubaix":        # colonnes renommées
        sub.rename(columns={"montant": "CA", "quantite": "qte"}, inplace=True)
        sub.to_csv(OUT / f"ventes_{ville}.csv", index=False)
    else:
        sub.to_csv(OUT / f"ventes_{ville}.csv", index=False)
# résultat attendu de la consolidation
ventes_plat[["date", "ville", "categorie", "produit", "quantite", "montant"]] \
    .to_csv(OUT / "ventes_consolidees.csv", index=False)

# --------------------------------------------------------------------------------------
# 7. RÉFÉRENTIEL PRODUITS + OBJECTIFS (module 3.4 extraction multi-sources)
# --------------------------------------------------------------------------------------
marques = ["NordPro", "Hauts-Tech", "Belle Maison", "SportNord", "Générique"]
referentiel = produits.copy()
referentiel["marque"] = rng.choice(marques, len(produits))
referentiel["actif"] = rng.choice([1, 1, 1, 0], len(produits))
referentiel.to_csv(OUT / "referentiel_produits.csv", index=False)

# objectifs mensuels par magasin (xlsx + csv)
obj_rows = []
for mid in magasins["magasin_id"]:
    ca_ref = ventes.loc[ventes["magasin_id"] == mid, "montant"].sum() / 24  # moy mensuelle
    for m in range(1, 13):
        obj_rows.append((mid, 2024, m, round(ca_ref * float(rng.uniform(0.9, 1.2)), -2)))
objectifs = pd.DataFrame(obj_rows, columns=["magasin_id", "annee", "mois", "objectif_ca"])
objectifs.to_csv(OUT / "objectifs_2024.csv", index=False)
objectifs.to_excel(OUT / "objectifs_2024.xlsx", index=False)

# --------------------------------------------------------------------------------------
# 8. setup.sql — base relationnelle (module 1.1 SQL) — compatible SQLite & PostgreSQL
# --------------------------------------------------------------------------------------
def sql_str(v):
    if pd.isna(v):
        return "NULL"
    if isinstance(v, (int, np.integer)):
        return str(int(v))
    if isinstance(v, (float, np.floating)):
        return f"{v:.2f}"
    return "'" + str(v).replace("'", "''") + "'"

lines = ["-- Base NordRetail — schéma pédagogique (SQLite / PostgreSQL)",
         "-- Généré par generate_datasets.py (reproductible, seed=42)",
         "DROP TABLE IF EXISTS commandes;", "DROP TABLE IF EXISTS clients;",
         "DROP TABLE IF EXISTS produits;", "DROP TABLE IF EXISTS magasins;", "",
         """CREATE TABLE magasins (
  magasin_id INTEGER PRIMARY KEY, ville TEXT, type TEXT,
  surface_m2 INTEGER, date_ouverture TEXT);""",
         """CREATE TABLE produits (
  produit_id INTEGER PRIMARY KEY, produit TEXT, categorie TEXT,
  prix_unitaire REAL, cout_unitaire REAL);""",
         """CREATE TABLE clients (
  client_id INTEGER PRIMARY KEY, prenom TEXT, nom TEXT, ville TEXT,
  segment TEXT, date_inscription TEXT, email TEXT);""",
         """CREATE TABLE commandes (
  vente_id INTEGER PRIMARY KEY, date TEXT, magasin_id INTEGER, produit_id INTEGER,
  client_id INTEGER, quantite INTEGER, prix_unitaire REAL, remise REAL, montant REAL,
  FOREIGN KEY (magasin_id) REFERENCES magasins(magasin_id),
  FOREIGN KEY (produit_id) REFERENCES produits(produit_id),
  FOREIGN KEY (client_id) REFERENCES clients(client_id));""", ""]

def insert_block(table, df, cols):
    out = []
    for _, row in df.iterrows():
        vals = ", ".join(sql_str(row[c]) for c in cols)
        out.append(f"INSERT INTO {table} ({', '.join(cols)}) VALUES ({vals});")
    return out

lines += insert_block("magasins", magasins, list(magasins.columns))
lines += insert_block("produits", produits, list(produits.columns))
cl = clients.assign(date_inscription=clients["date_inscription"].dt.strftime("%Y-%m-%d"))
lines += insert_block("clients", cl, list(cl.columns))
# on limite les commandes à 3000 pour garder un fichier .sql raisonnable
cmd = faits.head(3000).assign(date=faits.head(3000)["date"].dt.strftime("%Y-%m-%d"))
lines += insert_block("commandes", cmd,
                      ["vente_id", "date", "magasin_id", "produit_id", "client_id",
                       "quantite", "prix_unitaire", "remise", "montant"])
(OUT / "setup.sql").write_text("\n".join(lines), encoding="utf-8")

# --------------------------------------------------------------------------------------
# Manifest
# --------------------------------------------------------------------------------------
print("Jeux de données générés dans", OUT)
for f in sorted(OUT.glob("*")):
    if f.suffix in (".csv", ".xlsx", ".sql"):
        print(f"  {f.name:32s} {f.stat().st_size/1024:8.1f} Ko")
