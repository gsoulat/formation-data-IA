# 02 — Variables et Connexions

## Variables Airflow

Les **Variables** Airflow sont des paires clé-valeur stockées dans la metadata database. Elles permettent de **paramétrer** les DAGs sans modifier le code.

> **Airflow 3** : une tâche n'a plus d'accès direct à la metadata database. Quand elle lit une Variable ou une Connexion, la demande passe par l'**API d'exécution** (portée par le serveur d'API). Pour vous, cela change surtout les imports : `from airflow.sdk import Variable, Connection, BaseHook` (en Airflow 2 : `from airflow.models import Variable`).

### Cas d'usage typiques

- URL d'une API, chemin d'un fichier de configuration
- Paramètres de pipeline (batch size, date de référence)
- Feature flags (activer/désactiver une fonctionnalité)
- Chemins S3, noms de tables, paramètres d'environnement

---

## Créer et gérer des Variables

### Via l'interface web

**Admin → Variables → Add Variable**

| Champ | Exemple |
|---|---|
| Key | `api_meteo_url` |
| Value | `https://api.open-meteo.com/v1/forecast` |
| Description | URL de l'API météo Open-Meteo |

Pour une valeur JSON, coller le texte JSON dans le champ Value : il sera désérialisé à la lecture avec `deserialize_json=True` (ou `{{ var.json.... }}` dans un template). La même page permet d'importer un fichier JSON de variables.

---

> 🔴 **ACTION FORMATEUR — CAPTURE REQUISE**
> **Capturer :** L'interface Airflow → Admin → Variables — formulaire de création d'une variable JSON (ex: configuration d'un pipeline avec plusieurs champs)
> **Expliquer :** Montrer que les variables dont la clé contient un mot sensible (`password`, `secret`, `token`, `api_key`, `private_key`...) sont automatiquement masquées dans l'UI et dans les logs (Airflow les cache pour des raisons de sécurité). Créer une variable `pipeline_config` avec un JSON complexe et montrer comment la récupérer en Python.

---

### Via CLI

```bash
# Créer une variable simple
airflow variables set api_url "https://api.example.com"

# Créer une variable JSON
airflow variables set pipeline_config '{"batch_size": 1000, "timeout": 300}'

# Lire une variable
airflow variables get api_url

# Lister toutes les variables
airflow variables list

# Supprimer une variable
airflow variables delete ancienne_variable

# Exporter toutes les variables (backup)
airflow variables export variables_backup.json

# Importer des variables depuis un fichier
airflow variables import variables_backup.json
```

> Ces commandes lisent et écrivent directement dans la metadata database : elles se lancent sur une machine (ou un conteneur) Airflow qui y a accès.

### Fichier d'import JSON

```json
{
  "api_meteo_url": "https://api.open-meteo.com/v1/forecast",
  "s3_bucket_raw": "mon-data-lake-raw",
  "s3_bucket_processed": "mon-data-lake-processed",
  "pipeline_config": {
    "batch_size": 5000,
    "timeout_minutes": 30,
    "retry_count": 3,
    "notification_email": "data-team@company.com"
  },
  "env": "production",
  "feature_flags": {
    "use_new_model": true,
    "enable_cache": false
  }
}
```

---

## Utiliser les Variables dans le code Python

```python
from airflow.sdk import Variable, task
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

@task
def lire_des_variables():
    # ---- Lecture simple ----
    api_url = Variable.get("api_meteo_url")
    # → "https://api.open-meteo.com/v1/forecast"

    # Avec valeur par défaut si la variable n'existe pas
    # (Airflow 2 : l'argument s'appelait default_var)
    bucket = Variable.get("s3_bucket", default="mon-bucket-defaut")

    # ---- Lecture JSON (désérialisation automatique) ----
    config = Variable.get("pipeline_config", deserialize_json=True)
    # → {"batch_size": 5000, "timeout_minutes": 30, ...}

    batch_size = config['batch_size']
    timeout = config['timeout_minutes']

# ---- Lecture dans une fonction Python (bonne pratique) ----
def ma_tache_avec_config(**context):
    """
    Toujours lire les variables DANS les fonctions, jamais au top-level.
    Au top-level, la lecture est refaite à chaque analyse du fichier
    par le processeur de DAG (toutes les 30 secondes environ par défaut).
    """
    config = Variable.get("pipeline_config", deserialize_json=True)
    env = Variable.get("env", default="dev")
    api_url = Variable.get("api_meteo_url")

    print(f"Environnement : {env}")
    print(f"Batch size : {config['batch_size']}")
    print(f"API URL : {api_url}")

# ---- Utilisation dans les templates Jinja ----
# Dans BashOperator ou les templates SQL :
tache_bash = BashOperator(
    task_id='utiliser_variable',
    bash_command='echo "Bucket: {{ var.value.s3_bucket_raw }}"',
)

# Variable JSON dans Jinja
# (PostgresOperator n'existe plus : on utilise SQLExecuteQueryOperator,
#  qui fonctionne avec toutes les bases SQL via conn_id)
tache_sql = SQLExecuteQueryOperator(
    task_id='sql_avec_variable',
    conn_id='postgres_production',
    sql="""
        SELECT * FROM ventes
        LIMIT {{ var.json.pipeline_config.batch_size }}
    """,
)
```

### Syntaxe Jinja pour les Variables

```
{{ var.value.nom_variable }}          → valeur brute (string)
{{ var.json.nom_variable }}           → valeur désérialisée JSON
{{ var.json.pipeline_config.batch_size }}  → champ d'un objet JSON
```

### Variables par variable d'environnement

Une Variable peut aussi être fournie sans passer par la base, avec une variable d'environnement nommée `AIRFLOW_VAR_<NOM EN MAJUSCULES>` :

```bash
export AIRFLOW_VAR_API_METEO_URL="https://api.open-meteo.com/v1/forecast"
export AIRFLOW_VAR_PIPELINE_CONFIG='{"batch_size": 5000, "timeout_minutes": 30}'
```

`Variable.get("api_meteo_url")` la retrouve comme n'importe quelle autre. Elle n'apparaît pas dans Admin → Variables, et elle doit être définie là où les tâches s'exécutent (workers).

---

## Connexions Airflow

Les **Connexions** (Connections) stockent les paramètres de connexion à des services externes : bases de données, APIs, cloud storage, services SSH, etc.

Elles centralisent les credentials et évitent de les coder en dur dans les DAGs.

### Paramètres d'une connexion

| Champ | Description |
|---|---|
| `conn_id` | Identifiant unique (ex: `postgres_prod`) |
| `conn_type` | Type de connexion (Postgres, HTTP, S3, SSH...) |
| `host` | Nom d'hôte ou IP |
| `schema` | Base de données ou schéma |
| `login` | Nom d'utilisateur |
| `password` | Mot de passe (stocké chiffré avec Fernet) |
| `port` | Port TCP |
| `extra` | JSON avec des paramètres supplémentaires |

---

## Types de connexions courants

### PostgreSQL / MySQL

```python
# ID: postgres_production
{
    "conn_type": "postgres",
    "host": "db.production.company.fr",
    "schema": "datawarehouse",
    "login": "airflow_user",
    "password": "xxxx",
    "port": 5432
}
```

### HTTP / REST API

```python
# ID: api_interne
{
    "conn_type": "http",
    "host": "api.company.fr",
    "schema": "https",
    "port": 443,
    "extra": {
        "Authorization": "Bearer eyJhbGciOiJSUzI1NiJ9...",
        "Content-Type": "application/json"
    }
}
```

> Le cas de Snowflake (authentification par paire de clés) est détaillé dans [Airflow 3 avec Astro, Snowflake et dbt](../06-Airflow3-Astro/01-airflow3-astro-snowflake-dbt.md).

### AWS S3

```python
# ID: aws_production
{
    "conn_type": "aws",
    "extra": {
        "aws_access_key_id": "AKIAIOSFODNN7EXAMPLE",
        "aws_secret_access_key": "wJalrXUtnFEMI/K7MDENG",
        "region_name": "eu-west-1"
    }
}
# Ou via rôle IAM (recommandé sur EC2/ECS) : extra = {"region_name": "eu-west-1"}
```

### Google Cloud Platform

```python
# ID: google_cloud_production
{
    "conn_type": "google_cloud_platform",
    "extra": {
        "project": "mon-projet-gcp",
        "key_path": "/secrets/service-account.json"
        # Ou "keyfile_dict": "{...json du service account...}"
    }
}
```

### SSH / SFTP

```python
# ID: serveur_sftp
{
    "conn_type": "ssh",
    "host": "sftp.partenaire.fr",
    "login": "utilisateur",
    "port": 22,
    "extra": {
        "key_file": "/opt/airflow/keys/sftp_key.pem"
        # Ou "password": "xxxx" pour authentification par mot de passe
    }
}
```

---

## Gérer les connexions

Dans l'interface : **Admin → Connections → Add Connection**. Les types proposés dépendent des providers installés.

### Via CLI

```bash
# Créer une connexion PostgreSQL
airflow connections add 'postgres_production' \
    --conn-type 'postgres' \
    --conn-host 'db.company.fr' \
    --conn-schema 'datawarehouse' \
    --conn-login 'airflow' \
    --conn-password 'secret' \
    --conn-port '5432'

# Créer une connexion HTTP avec extra
airflow connections add 'api_interne' \
    --conn-type 'http' \
    --conn-host 'api.company.fr' \
    --conn-schema 'https' \
    --conn-extra '{"Authorization": "Bearer mon_token"}'

# Lister les connexions
airflow connections list

# Supprimer
airflow connections delete 'ancienne_connexion'

# Exporter/importer
airflow connections export connections_backup.json
airflow connections import connections_backup.json
```

### Via une variable d'environnement

Comme pour les Variables, une connexion peut être définie par une variable d'environnement `AIRFLOW_CONN_<CONN_ID EN MAJUSCULES>`, au format URI ou JSON :

```bash
export AIRFLOW_CONN_POSTGRES_PRODUCTION='postgresql://airflow:secret@db.company.fr:5432/datawarehouse'

export AIRFLOW_CONN_API_INTERNE='{"conn_type": "http", "host": "api.company.fr", "schema": "https", "extra": {"Authorization": "Bearer mon_token"}}'
```

---

## Utiliser les connexions via les Hooks

```python
from airflow.providers.postgres.hooks.postgres import PostgresHook
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.http.hooks.http import HttpHook
from airflow.providers.standard.operators.python import PythonOperator

def utiliser_connexions(**context):
    # ---- PostgreSQL ----
    pg_hook = PostgresHook(postgres_conn_id='postgres_production')

    # Exécuter une requête
    records = pg_hook.get_records("SELECT COUNT(*) FROM ventes WHERE date = %(d)s",
                                   parameters={'d': context['ds']})
    print(f"Ventes du jour : {records[0][0]}")

    # DataFrame pandas (get_pandas_df est déprécié au profit de get_df)
    df = pg_hook.get_df("SELECT * FROM ventes LIMIT 10")

    # Connexion SQLAlchemy (pour pandas.to_sql etc.)
    engine = pg_hook.get_sqlalchemy_engine()
    df.to_sql('ventes_temp', engine, if_exists='replace', index=False)

    # ---- S3 ----
    s3_hook = S3Hook(aws_conn_id='aws_production')

    # Uploader un fichier
    s3_hook.load_file(
        filename='/tmp/rapport.csv',
        key=f'rapports/{context["ds"]}/rapport.csv',
        bucket_name='mon-bucket',
        replace=True,
    )

    # Vérifier si un fichier existe
    existe = s3_hook.check_for_key('data/source/fichier.csv', 'mon-bucket')
    print(f"Fichier S3 existe : {existe}")

    # ---- HTTP ----
    http_hook = HttpHook(method='GET', http_conn_id='api_interne')
    response = http_hook.run('/api/v1/status')
    print(f"Statut API : {response.json()}")

tache = PythonOperator(
    task_id='utiliser_connexions',
    python_callable=utiliser_connexions,
)
```

Pour lire les champs d'une connexion sans passer par un Hook spécialisé :

```python
from airflow.sdk import BaseHook, task

@task
def lire_connexion():
    conn = BaseHook.get_connection('api_interne')
    print(conn.host, conn.port, conn.login)
    print(conn.extra_dejson)   # le champ extra, déjà converti en dict
```

---

## Sécurité : chiffrement avec Fernet

Airflow chiffre les mots de passe et le champ `extra` des Connexions, ainsi que les valeurs des Variables, avec une clé **Fernet** avant de les écrire dans la metadata database.

### Générer une clé Fernet

```python
# Générer une clé Fernet
from cryptography.fernet import Fernet
print(Fernet.generate_key().decode())
# → lNc7VV...xX= (clé base64 de 32 bytes)
```

### Configurer la clé dans Airflow

```ini
# airflow.cfg
[core]
fernet_key = lNc7VV...xX=
```

```yaml
# docker-compose.yaml
environment:
  AIRFLOW__CORE__FERNET_KEY: "lNc7VV...xX="
```

> Sans clé Fernet, les mots de passe sont stockés en clair. Toujours configurer une clé Fernet en production.

---

## Bonnes pratiques Variables & Connexions

```python
# ✓ Lire les variables DANS les tâches, jamais au top-level
with DAG(...) as dag:

    # ❌ Top-level : lecture refaite à chaque analyse du fichier par le
    #    processeur de DAG (parsing ralenti, appels inutiles), même si
    #    aucune tâche ne tourne
    URL = Variable.get("api_url")

    def ma_tache():
        # ✓ Dans la fonction : lu au moment de l'exécution
        URL = Variable.get("api_url")

# ✓ Utiliser des valeurs par défaut
# (la valeur par défaut est renvoyée telle quelle : donner un dict, pas du texte JSON)
config = Variable.get("pipeline_config",
                      default={"batch_size": 1000},
                      deserialize_json=True)

# ✓ Grouper les variables liées dans un JSON
# Une seule variable "pipeline_etl_config" plutôt que 10 variables séparées

# ✓ Utiliser des préfixes pour organiser
# prod_api_url, dev_api_url, staging_api_url
# ou via l'env : Variable.get(f"{env}_api_url")

# ✓ Pour les secrets, préférer les backends secrets (HashiCorp Vault, AWS Secrets Manager)
```

### Backends de secrets (production)

Un backend de secrets est interrogé **avant** les variables d'environnement et la metadata database. Il faut installer le provider correspondant (`apache-airflow-providers-amazon`, `apache-airflow-providers-hashicorp`...).

```ini
# airflow.cfg — utiliser AWS Secrets Manager
[secrets]
backend = airflow.providers.amazon.aws.secrets.secrets_manager.SecretsManagerBackend
backend_kwargs = {"connections_prefix": "airflow/connections", "variables_prefix": "airflow/variables"}
```

```ini
# airflow.cfg — utiliser HashiCorp Vault
[secrets]
backend = airflow.providers.hashicorp.secrets.vault.VaultBackend
backend_kwargs = {"connections_path": "connections", "variables_path": "variables", "mount_point": "airflow"}
```

---

## Exemple complet : DAG paramétré

```python
# dags/pipeline_parametre.py

from datetime import datetime
from airflow.sdk import dag, task, Variable

@dag(
    dag_id='pipeline_parametre',
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['variables', 'connexions'],
)
def pipeline_parametre():

    @task
    def charger_configuration() -> dict:
        """Charge toute la configuration depuis les Variables Airflow."""
        config = Variable.get("pipeline_config", deserialize_json=True, default={})
        env = Variable.get("env", default="dev")

        # Enrichir avec les valeurs calculées
        config['environment'] = env
        config['is_production'] = (env == "production")

        print(f"Configuration chargée pour l'environnement : {env}")
        print(f"Config : {config}")
        return config

    @task
    def extraire(config: dict) -> str:
        from airflow.providers.http.hooks.http import HttpHook

        # Utiliser une connexion différente selon l'env
        conn_id = 'api_production' if config['is_production'] else 'api_dev'
        hook = HttpHook(method='GET', http_conn_id=conn_id)

        response = hook.run(
            endpoint='/api/data',
            data={'limit': config.get('batch_size', 1000)},
        )

        import json
        chemin = '/tmp/data_brute.json'
        with open(chemin, 'w') as f:
            json.dump(response.json(), f)

        return chemin

    @task
    def charger(chemin: str, config: dict) -> int:
        from airflow.providers.postgres.hooks.postgres import PostgresHook
        import pandas as pd

        # Connexion selon l'environnement
        conn_id = 'postgres_production' if config['is_production'] else 'postgres_dev'
        hook = PostgresHook(postgres_conn_id=conn_id)

        df = pd.read_json(chemin)
        engine = hook.get_sqlalchemy_engine()
        table = config.get('table_destination', 'donnees_import')

        df.to_sql(table, engine, if_exists='append', index=False)
        print(f"{len(df)} lignes chargées dans {table}")
        return len(df)

    config = charger_configuration()
    chemin = extraire(config)
    nb = charger(chemin, config)

dag = pipeline_parametre()
```

---

## Points clés à retenir

1. **Variables** = configuration centralisée, modifiable sans re-déployer les DAGs
2. **Connexions** = credentials centralisés, chiffrés avec Fernet
3. Lire les Variables **dans les fonctions**, jamais au top-level du fichier DAG — avec `from airflow.sdk import Variable` en Airflow 3
4. Utiliser des Variables JSON pour regrouper la configuration liée
5. Les **Hooks** sont la couche basse d'accès aux connexions (`PostgresHook`, `S3Hook`, `HttpHook`...)
6. En production : utiliser un **backend de secrets** (Vault, AWS Secrets Manager) ou des variables d'environnement `AIRFLOW_VAR_...` / `AIRFLOW_CONN_...`
