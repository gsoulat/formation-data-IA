# La source du brief — point d'entrée

Ce fichier ne contient **que le point d'entrée de l'API et les premières commandes**.
L'inventaire du catalogue, le choix du périmètre, l'extraction, la conception des zones
et toute la gouvernance sont votre travail.

La source est **publique, réelle et sans authentification**. Elle est aussi **nominative** :
tout ce que vous en tirez est un traitement de données à caractère personnel.

---

## Démarrer toute la stack

```bash
cp .env.example .env      # puis adaptez les mots de passe
docker compose up -d
docker compose ps         # 6 services, tous "healthy" (5 à 10 min au 1er lancement)
```

| Service | Interface | Rôle |
|---|---|---|
| OpenMetadata | http://localhost:8585 | le catalogue (`admin@open-metadata.org` / `admin`) |
| MinIO | http://localhost:9001 | zone brute, stockage objet S3 |
| PostgreSQL | `localhost:5433` | zone travaillée (vos données) |
| Airflow (ingestion) | http://localhost:8080 | exécution des ingestions OpenMetadata |

> **Le port 5432 n'est pas le vôtre.** OpenMetadata embarque sa propre base PostgreSQL,
> qui contient ses métadonnées, pas vos données. La vôtre est sur **5433**.

Vérifiez votre mémoire avant le premier lancement : `docker info | grep "Total Memory"`.
La stack consomme environ 4,7 Go. Les soupapes en cas de machine juste sont documentées
en en-tête du `docker-compose.yml`.

---

## API Transparence-Santé (Opendatasoft Explore v2.1)

- Portail : https://www.transparence.sante.gouv.fr
- Documentation de l'API : https://help.opendatasoft.com/apis/ods-explore-v2/

### Lister tous les jeux du catalogue

```bash
curl -s --compressed \
  "https://www.transparence.sante.gouv.fr/api/explore/v2.1/catalog/datasets?limit=100" \
  | python3 -m json.tool
```

C'est le point de départ de la Phase 1. Combien de jeux ? Lesquels se ressemblent ?
Regardez les identifiants **et** les volumétries annoncées.

### Lire les enregistrements d'un jeu

```bash
curl -s --compressed \
  "https://www.transparence.sante.gouv.fr/api/explore/v2.1/catalog/datasets/<dataset_id>/records?limit=1" \
  | python3 -m json.tool
```

Remplacez `<dataset_id>` par un identifiant relevé à l'étape précédente.
Comme toutes les API Opendatasoft, celle-ci plafonne `limit` et `offset` : vérifiez-le
vous-même avant de concevoir votre extraction.

---

## Deux adresses pour deux points de vue

C'est la source de blocage numéro 1 de ce brief. Le même service n'a pas la même adresse
selon d'où on l'appelle :

| Depuis… | PostgreSQL | MinIO |
|---|---|---|
| **votre machine** (scripts Python, psql) | `localhost:5433` | `http://localhost:9000` |
| **OpenMetadata** (réseau Docker) | `postgres_eclairage:5432` | `http://minio:9000` |

Si le catalogue refuse de se connecter à une source, vérifiez l'adresse avant les identifiants.

---

## MinIO en ligne de commande

L'alias `mc` par défaut dans le conteneur n'a pas d'identifiants et renverra
« Access Denied ». Configurez-le d'abord :

```bash
docker exec eclairage_minio mc alias set loc http://localhost:9000 <user> <password>
docker exec eclairage_minio mc ls -r loc/<votre-bucket>
```

**Aucun bucket n'est créé** : concevoir les zones de stockage fait partie du travail.

---

## Règles non négociables

1. **Aucune donnée nominative dans Git.** Le `.gitignore` fourni est un garde-fou, pas une
   garantie. Vérifiez avant chaque commit — un fichier supprimé plus tard reste dans
   l'historique.
2. **Périmètre maîtrisé.** Vous n'avez aucune raison de charger dix millions de lignes.
   Choisissez, justifiez, documentez.
3. **Identifiez-vous** auprès de l'API avec un `User-Agent` explicite et temporisez vos appels.
