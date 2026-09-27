# Sources du brief — URL de départ

Ce fichier ne contient **que les points d'entrée**. Le reste (exploration, choix des champs,
stratégie d'extraction, documentation) est votre travail : voir la Phase 1 du brief.

Toutes les sources ci-dessous sont **publiques, réelles et sans authentification**.

---

## 1. API REST — Base nationale des IRVE (points de recharge)

Jeu de données ODRE (Open Data Réseaux Énergies), API Opendatasoft Explore v2.1.

- Fiche du jeu de données : https://odre.opendatasoft.com/explore/dataset/bornes-irve/
- Point d'entrée `records` : https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/bornes-irve/records
- Documentation de l'API : https://help.opendatasoft.com/apis/ods-explore-v2/

Premier appel à faire, dans un navigateur ou avec `curl` :

```
https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/bornes-irve/records?limit=1
```

Regardez `total_count`. Puis essayez `?limit=100&offset=15000` et lisez le message d'erreur.

## 2. Scraping — modèles de véhicules électriques

- Page principale : https://en.wikipedia.org/wiki/List_of_production_battery_electric_vehicles
- Page complémentaire (prises, paliers de puissance) : https://fr.wikipedia.org/wiki/Borne_de_recharge

Wikipédia autorise les robots respectueux. Envoyez un `User-Agent` explicite (voir `.env.example`)
et temporisez vos requêtes.

## 3. Fichier de données — parc de voitures électriques

- Fiche du jeu de données : https://www.data.gouv.fr/datasets/part-de-voitures-particulieres-electriques-critair-e-dans-le-parc

Plusieurs ressources CSV y sont publiées, à des granularités différentes.
Choisissez celle qui sert la question centrale, et dites pourquoi dans `docs/sources.md`.

## 4. Base de données — PostgreSQL

Fournie par le `docker-compose.yml` de ce kit.

```bash
cp .env.example .env      # puis adaptez les valeurs
docker compose up -d
docker compose ps         # le service doit être "healthy"
```

---

## Rappel

Aucun script d'extraction, de nettoyage ou d'import n'est fourni. C'est le sujet du brief.
