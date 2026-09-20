# Jeux de données pédagogiques — NordRetail

Univers fictif **NordRetail**, enseigne de distribution des Hauts-de-France (magasins Lille, Roubaix, Tourcoing, Dunkerque, Valenciennes, Amiens + e-commerce). Données **100 % synthétiques et reproductibles** (`seed=42`), aucune donnée personnelle réelle.

> Régénérer : `pip install pandas numpy openpyxl && python generate_datasets.py`

## Contenu (2023-2024, ~12 000 ventes, CA ~14,4 M€)

| Fichier | Description | Utilisé par |
|---|---|---|
| `ventes_magasins.csv` | Ventes à plat **propres** (date, ville, catégorie, produit, quantité, prix, remise, montant, marge, client) | Maths ch.3 (stats), module 1.2 (pandas EDA), 1.3 (tendances) |
| `ventes_retail_nord.csv` | Alias de `ventes_magasins.csv` | idem |
| `ventes_sales.csv` | Version **sale** : manquants, doublons, casse incohérente, dates mixtes, négatifs, outliers, décimales à virgule | module 3.3 (nettoyage), 1.2 |
| `ventes_corrompu.csv` | Alias de `ventes_sales.csv` | module 3.3 |
| `Dim_Magasin.csv`, `Dim_Produit.csv`, `Dim_Client.csv`, `Dim_Date.csv` | Tables de **dimensions** (schéma en étoile) | module 2.2 (modélisation BI) |
| `Faits_Ventes.csv` | Table de **faits** (clés étrangères + mesures) | module 2.2, 2.3 (DAX) |
| `ventes_lille.csv` (`;`), `ventes_roubaix.csv` (colonnes renommées), `ventes_tourcoing.csv`, `ventes_valenciennes.csv` | Fichiers **multi-magasins hétérogènes** à consolider | module 3.2 (ETL) |
| `ventes_consolidees.csv` | Résultat **attendu** de la consolidation | module 3.2 |
| `referentiel_produits.csv` | Référentiel produits (marque, coût, actif) | module 3.4 (multi-sources) |
| `objectifs_2024.csv` / `.xlsx` | Objectifs de CA mensuels par magasin | module 3.4 (merge multi-sources) |
| `setup.sql` | Base relationnelle (magasins, produits, clients, commandes) — **SQLite & PostgreSQL** | module 1.1 (SQL) |

## Démarrage rapide

**Python / pandas**
```python
import pandas as pd
ventes = pd.read_csv("ventes_magasins.csv", parse_dates=["date"])
ventes.describe()
```

**SQL (SQLite)**
```bash
sqlite3 nordretail.db < setup.sql
sqlite3 nordretail.db "SELECT m.ville, ROUND(SUM(c.montant)) ca
  FROM commandes c JOIN magasins m USING(magasin_id)
  GROUP BY m.ville ORDER BY ca DESC;"
```

**Power BI / Looker Studio** : importer les fichiers `Dim_*.csv` + `Faits_Ventes.csv` et relier sur les clés (`magasin_id`, `produit_id`, `client_id`, `date_id`) → modèle en étoile.

## Cohérence pédagogique
- Le fichier **propre** et le fichier **sale** décrivent les mêmes ventes : on peut comparer avant/après nettoyage.
- Le **schéma en étoile** redécrit les mêmes faits, normalisés en dimensions.
- Saisonnalité intégrée : pics aux **soldes (janv./juil.)** et à **Noël (déc.)** — exploitable pour l'analyse de tendances (module 1.3).
