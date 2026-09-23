# Kit de démarrage — Airflow + DuckDB + dbt en local

Ce kit fournit **l'outillage**, pas la solution. Airflow, DuckDB et dbt sont installés et
fonctionnent ; les DAG, les modèles et les tests sont votre travail.

Il sert la **variante C** (100 % locale) et sert aussi à la **variante B** pour mettre au point
vos DAG en local avant de les déployer sur Cloud Composer — c'est la seule façon raisonnable de
travailler sur un orchestrateur facturé à l'heure.

## Mise en route

```bash
cp .env.example .env
docker compose up -d --build          # la 1re construction prend ~2 min
docker compose ps                     # doit être "healthy"

# mot de passe admin généré au premier démarrage :
docker compose logs airflow | grep -i "Password for user"
```

Interface Airflow : http://localhost:8080 (utilisateur `admin`).

## Ce qui est installé

| Composant | Version épinglée |
|---|---|
| Apache Airflow | 3.3.0 (Python 3.12) |
| DuckDB | 1.5.5 |
| dbt-duckdb | 1.10.1 |
| dbt-core | résolu par pip (1.12.x) |

Seuls `duckdb` et `dbt-duckdb` sont épinglés : pip résout `dbt-core` lui-même, ce qui évite les
conflits entre l'adaptateur et le cœur de dbt.

## Arborescence

```
starter-kit-local/
├── Dockerfile              # image Airflow + DuckDB + dbt (fourni)
├── docker-compose.yml      # la stack (fourni, commenté)
├── .env.example            # variables d'environnement
├── dags/                   # A VOUS — vos DAG
├── dbt/                    # A VOUS — votre projet dbt (voir dbt/README.md)
├── tests/                  # A VOUS — vos tests de DAG (voir tests/README.md)
├── plugins/                # A VOUS — opérateurs/hooks personnalisés si besoin
└── data/                   # la base DuckDB et les Parquet téléchargés (jamais commités)
```

Ces dossiers sont **partagés** entre votre machine et le conteneur : éditez avec votre éditeur
habituel, Airflow voit les changements.

## Variables d'environnement disponibles dans vos DAG

| Variable | Valeur |
|---|---|
| `DUCKDB_PATH` | `/opt/airflow/data/nyc_taxi.duckdb` |
| `DBT_PROJECT_DIR` | `/opt/airflow/dbt` |
| `DBT_PROFILES_DIR` | `/opt/airflow/dbt` |

## Vérifier que la chaîne fonctionne

DuckDB lit un Parquet distant sans rien télécharger — testez-le avant d'écrire quoi que ce soit :

```bash
docker exec nyctaxi_airflow python -c "
import duckdb
con = duckdb.connect()
con.execute('INSTALL httpfs; LOAD httpfs;')
n = con.execute(\"SELECT count(*) FROM read_parquet('https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet')\").fetchone()[0]
print(f'{n:,} lignes')
"
```

Vous devriez obtenir environ 2,96 millions de lignes en une seconde. C'est une capacité à
exploiter : vous pouvez explorer les données sans les charger.

## Pièges connus

**Disque.** Le jeu complet représente ~8 Go de Parquet, plus la base DuckDB. Prévoyez 15 Go
libres et vérifiez avant le backfill : `df -h .`

**Un seul écrivain sur DuckDB.** DuckDB n'accepte qu'un processus en écriture à la fois. Si une
tâche d'ingestion écrit pendant que `dbt run` tourne sur la même base, vous obtiendrez une erreur
de verrou. Ce n'est pas un bug, c'est une contrainte de conception de votre DAG.

**Mode standalone.** L'API, le scheduler et le triggerer tournent dans un seul conteneur avec une
base SQLite. Parfait pour apprendre et déboguer ; limité en parallélisme. Passer à un vrai
déploiement (Postgres + exécuteur distribué) est un bonus prévu — vous devrez alors justifier le
changement.

**Le triggerer doit tourner** pour que les capteurs différés fonctionnent. Le mode standalone le
démarre ; si vous modifiez la commande, vérifiez-le.

## Nettoyage

```bash
docker compose down -v      # supprime aussi la base de métadonnées d'Airflow
rm -rf data/*.duckdb data/*.parquet
```
