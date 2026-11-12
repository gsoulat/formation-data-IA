# IRVE — Bornes de recharge : deux versions d'un même brief

Les deux versions partent de **la même source réelle**, l'API nationale des bornes de recharge (IRVE), avec les
mêmes pièges dans les données. Elles ne mettent pas l'accent au même endroit.

- **[Version collecte](BRIEF_IRVE_COLLECTE.md)** — 5 jours, débutant-intermédiaire. Quatre types de sources (API
  ODRE, scraping Wikipédia, CSV Crit'Air E, PostgreSQL) croisées pour comparer bornes et parc de véhicules
  électriques, modèle Merise, requêtes SQL, RGPD.
- **[Version CI/CD](BRIEF_IRVE_CICD.md)** — 5 jours, intermédiaire. **Une seule source (l'API IRVE)**, trois
  scripts (extraction, nettoyage, consolidation) qui alimentent trois schémas PostgreSQL (`raw`, `staging`,
  `mart`), modèle Merise. En plus : uv obligatoire, commits conventionnels vérifiés par GitHub Actions, versions
  publiées par semantic-release et image Docker du pipeline publiée sur GHCR à chaque release. **La chaîne de
  livraison se construit en premier (J1)**, avant le pipeline. La CI ne fait que ça : pas de tests, pas de lint,
  pas de déploiement.

## Laquelle choisir ?

- **Version collecte** pour travailler la diversité des sources (scraping, fichiers, jointures entre sources).
- **Version CI/CD** pour un profil déjà solide (par exemple un Data Analyst à l'aise en Python et SQL), ou
  si le parcours a déjà vu Git et Docker et que vous voulez faire travailler l'industrialisation. Attention :
  avec une seule source, elle ne couvre pas tout le périmètre de C8 (page web, fichier) ni le croisement de
  sources de C10.

Le kit de démarrage ([`starter-kit/`](starter-kit/)) est commun aux deux versions.
