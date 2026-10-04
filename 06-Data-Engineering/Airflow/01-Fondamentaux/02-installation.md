# 02 — Installation et Configuration

## Options d'installation

Il existe plusieurs façons d'installer Airflow :

| Méthode | Usage | Complexité |
|---|---|---|
| `pip install apache-airflow` puis `airflow standalone` | Développement local rapide | Faible |
| Docker Compose officiel | Formation, dev, petits projets | Moyenne |
| Helm Chart (Kubernetes) | Production, scalabilité | Élevée |
| Astro CLI (Astronomer) | Développement local clé en main, production managée | Faible |

Dans cette formation, nous utilisons **Docker Compose** : le fichier officiel montre tous les composants d'Airflow, ce qui est idéal pour apprendre. La documentation officielle précise qu'il est destiné à l'apprentissage et au développement, pas à la production.

---

## Installation avec Docker Compose

### Prérequis

```bash
# Vérifier Docker
docker --version
# Docker version 24.0.x ou supérieur

# Vérifier Docker Compose
docker compose version
# Docker Compose version 2.14.0 ou supérieur

# Vérifier la mémoire disponible (minimum 4 Go recommandés)
docker info | grep -i memory
```

### Récupérer le fichier Docker Compose officiel

```bash
# Créer le répertoire de travail
mkdir ~/airflow-formation && cd ~/airflow-formation

# Télécharger le docker-compose.yaml officiel d'Airflow 3.3.2
curl -LfO 'https://airflow.apache.org/docs/apache-airflow/3.3.2/docker-compose.yaml'
```

### Structure du projet

```bash
mkdir -p ./dags ./logs ./plugins ./config

# Ce fichier est nécessaire pour que le container ait les bons droits (surtout sous Linux)
echo -e "AIRFLOW_UID=$(id -u)" > .env
```

L'arborescence doit ressembler à :

```
airflow-formation/
├── docker-compose.yaml
├── .env
├── dags/            ← Vos fichiers DAG Python
├── logs/            ← Logs des task instances
├── plugins/         ← Opérateurs/hooks personnalisés
└── config/          ← airflow.cfg (généré à l'initialisation), réglages personnalisés
```

---

> 🔴 **ACTION FORMATEUR — CAPTURE REQUISE**
> **Capturer :** Le terminal avec la commande `docker compose up airflow-init` en cours d'exécution, montrant les logs d'initialisation
> **Expliquer :** Que fait `airflow-init` : il vérifie les ressources disponibles, applique les migrations de la metadata DB (`airflow db migrate`), crée l'utilisateur admin par défaut, et prépare les dossiers. Montrer que c'est une opération one-shot (le conteneur se termine avec le code 0).

---

### Initialisation et démarrage

```bash
# Initialiser la base de données et créer le compte admin (à faire une seule fois)
docker compose up airflow-init
# Attendu en fin de sortie : airflow-init-1 exited with code 0

# Démarrer tous les services en arrière-plan
docker compose up -d

# Vérifier que tout tourne
docker compose ps
```

Résultat attendu de `docker compose ps` :

```
NAME                                        STATUS
airflow-formation-airflow-apiserver-1       Up (healthy)
airflow-formation-airflow-scheduler-1       Up (healthy)
airflow-formation-airflow-dag-processor-1   Up (healthy)
airflow-formation-airflow-triggerer-1       Up (healthy)
airflow-formation-airflow-worker-1          Up (healthy)
airflow-formation-postgres-1                Up (healthy)
airflow-formation-redis-1                   Up (healthy)
```

> Compose affiche un avertissement `The "FERNET_KEY" variable is not set` : le fichier officiel lit cette variable dans `.env`. Sans elle, les mots de passe des connexions ne sont pas chiffrés dans la metadata DB — acceptable en formation, pas en production.

### Accéder à l'interface web

```
URL : http://localhost:8080
Login : airflow
Password : airflow
```

Ce compte est créé par `airflow-init`. Le fichier officiel active le gestionnaire d'authentification **FAB** (provider `apache-airflow-providers-fab`), qui gère utilisateurs et rôles comme en Airflow 2. Sans ce réglage, Airflow 3 utilise par défaut le **SimpleAuthManager**, un gestionnaire minimal prévu pour le développement.

---

## Alternative : Astro CLI

L'**Astro CLI** (outil open source d'Astronomer) démarre un Airflow 3 local complet en deux commandes, sans fichier Docker Compose à maintenir :

```bash
astro dev init    # crée la structure du projet (dags/, Dockerfile, requirements.txt...)
astro dev start   # construit l'image et démarre Airflow en local
```

C'est une alternative plus simple au quotidien. Elle est détaillée dans le module 6 : [Airflow 3 avec Astro CLI, Snowflake et dbt](../06-Airflow3-Astro/01-airflow3-astro-snowflake-dbt.md).

---

## Anatomie du docker-compose.yaml

Voici les sections clés à comprendre :

```yaml
# docker-compose.yaml (extraits commentés)

x-airflow-common:
  # Image de base — peut être remplacée par une image custom
  &airflow-common
  image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:3.3.2}

  environment:
    &airflow-common-env
    # Type d'executor (LocalExecutor, CeleryExecutor, KubernetesExecutor)
    AIRFLOW__CORE__EXECUTOR: CeleryExecutor

    # Gestionnaire d'authentification : FAB (utilisateurs, rôles, login/mot de passe)
    AIRFLOW__CORE__AUTH_MANAGER: airflow.providers.fab.auth_manager.fab_auth_manager.FabAuthManager

    # Connexion à la metadata DB
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow

    # Connexion au broker Celery (Redis ici)
    AIRFLOW__CELERY__RESULT_BACKEND: db+postgresql+psycopg2://airflow:airflow@postgres/airflow
    AIRFLOW__CELERY__BROKER_URL: redis://:@redis:6379/0

    # Clé de chiffrement des connexions (Fernet), lue dans .env
    AIRFLOW__CORE__FERNET_KEY: ${FERNET_KEY}

    # DAGs d'exemple : mettez 'false' pour ne voir que vos DAGs
    AIRFLOW__CORE__LOAD_EXAMPLES: 'true'

    # Adresse de l'API d'exécution : c'est par elle que les workers
    # lisent et écrivent l'état des tâches (plus d'accès direct à la DB)
    AIRFLOW__CORE__EXECUTION_API_SERVER_URL: 'http://airflow-apiserver:8080/execution/'

    # Secret partagé pour signer les jetons JWT échangés entre composants
    AIRFLOW__API_AUTH__JWT_SECRET: ${AIRFLOW__API_AUTH__JWT_SECRET:-airflow_jwt_secret}

  volumes:
    # Monte vos DAGs dans le container
    - ${AIRFLOW_PROJ_DIR:-.}/dags:/opt/airflow/dags
    - ${AIRFLOW_PROJ_DIR:-.}/logs:/opt/airflow/logs
    - ${AIRFLOW_PROJ_DIR:-.}/config:/opt/airflow/config
    - ${AIRFLOW_PROJ_DIR:-.}/plugins:/opt/airflow/plugins

services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow

  redis:
    image: redis:7.2-bookworm
    # Sert de broker de messages pour Celery

  airflow-apiserver:
    <<: *airflow-common
    command: api-server          # remplace "webserver" d'Airflow 2
    ports:
      - "8080:8080"
    healthcheck:
      test: ["CMD", "curl", "--fail", "http://localhost:8080/api/v2/monitor/health"]

  airflow-scheduler:
    <<: *airflow-common
    command: scheduler

  airflow-dag-processor:
    <<: *airflow-common
    command: dag-processor       # analyse des fichiers DAG, séparée du scheduler

  airflow-worker:
    <<: *airflow-common
    command: celery worker

  airflow-triggerer:
    <<: *airflow-common
    command: triggerer

  airflow-init:
    <<: *airflow-common
    # Service one-shot : migrations de la DB + création du compte admin
    environment:
      <<: *airflow-common-env
      _AIRFLOW_DB_MIGRATE: 'true'
      _AIRFLOW_WWW_USER_CREATE: 'true'
      _AIRFLOW_WWW_USER_USERNAME: ${_AIRFLOW_WWW_USER_USERNAME:-airflow}
      _AIRFLOW_WWW_USER_PASSWORD: ${_AIRFLOW_WWW_USER_PASSWORD:-airflow}
```

> **Si vous venez d'Airflow 2 :** le service `airflow-webserver` (commande `webserver`) n'existe plus ; il est remplacé par `airflow-apiserver` (commande `api-server`), et un service `airflow-dag-processor` s'ajoute.

---

## Les Executors

L'Executor détermine **comment et où** les tâches sont exécutées.

### SequentialExecutor (supprimé en Airflow 3)

```
Airflow Scheduler
      │
      └──► Tâche 1 (bloque jusqu'à la fin)
      └──► Tâche 2 (ensuite seulement)
      └──► Tâche 3
```

- Exécutait **une seule tâche à la fois**, avec SQLite
- C'était l'exécuteur par défaut d'Airflow 2 : vous le croiserez dans d'anciens tutoriels
- **Il n'existe plus en Airflow 3** : l'exécuteur par défaut est désormais le `LocalExecutor`

### LocalExecutor

```
Airflow Scheduler
      ├──► Process 1 (Tâche A)
      ├──► Process 2 (Tâche B)  ← exécution parallèle
      └──► Process 3 (Tâche C)
```

- Utilise des **sous-processus locaux** sur la même machine que le Scheduler
- Supporte la **parallélisation** (plafonnée par `[core] parallelism`)
- **Exécuteur par défaut** d'Airflow 3 ; à utiliser avec PostgreSQL (SQLite reste réservé aux essais rapides)
- **Adapté pour le développement et les petits déploiements**

```ini
[core]
executor = LocalExecutor

[database]
sql_alchemy_conn = postgresql+psycopg2://airflow:airflow@localhost/airflow
```

Docker Compose simplifié pour LocalExecutor (ni Redis, ni worker Celery) :

```yaml
# docker-compose-local.yaml
x-airflow-common:
  &airflow-common
  image: apache/airflow:3.3.2
  environment:
    AIRFLOW__CORE__EXECUTOR: LocalExecutor
    AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: >-
      postgresql+psycopg2://airflow:airflow@postgres/airflow
    AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
    AIRFLOW__CORE__FERNET_KEY: ''
    # Les tâches joignent l'API d'exécution servie par l'API Server
    AIRFLOW__CORE__EXECUTION_API_SERVER_URL: 'http://airflow-apiserver:8080/execution/'
    # Même secret JWT pour tous les composants
    AIRFLOW__API_AUTH__JWT_SECRET: 'secret_de_formation'
    # SimpleAuthManager (défaut d'Airflow 3) : tout visiteur est admin, sans login.
    # À réserver à un poste de développement !
    AIRFLOW__CORE__SIMPLE_AUTH_MANAGER_ALL_ADMINS: 'true'
  volumes:
    - ./dags:/opt/airflow/dags
    - ./logs:/opt/airflow/logs
  user: "${AIRFLOW_UID:-50000}:0"
  depends_on:
    &airflow-common-depends-on
    postgres:
      condition: service_healthy

services:
  postgres:
    image: postgres:16
    environment:
      POSTGRES_USER: airflow
      POSTGRES_PASSWORD: airflow
      POSTGRES_DB: airflow
    healthcheck:
      test: ["CMD", "pg_isready", "-U", "airflow"]
      interval: 10s
      retries: 5

  airflow-init:
    <<: *airflow-common
    command: db migrate

  airflow-apiserver:
    <<: *airflow-common
    command: api-server
    ports:
      - "8080:8080"
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  airflow-scheduler:
    <<: *airflow-common
    command: scheduler
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully

  airflow-dag-processor:
    <<: *airflow-common
    command: dag-processor
    depends_on:
      <<: *airflow-common-depends-on
      airflow-init:
        condition: service_completed_successfully
```

> **Si vous venez d'Airflow 2 :** `airflow db init` est remplacé par `airflow db migrate`, et `airflow webserver` par `airflow api-server`. La commande `airflow users create` n'existe plus qu'avec le gestionnaire d'authentification FAB : avec le SimpleAuthManager, les comptes se déclarent dans la configuration (`[core] simple_auth_manager_users`).

### CeleryExecutor

```
Airflow Scheduler
      │
      └──► Redis/RabbitMQ (queue)
               ├──► Worker 1 (machine A)
               ├──► Worker 2 (machine A)
               ├──► Worker 3 (machine B)   ← scalabilité horizontale
               └──► Worker 4 (machine B)
```

- Distribue les tâches sur des **workers Celery** (potentiellement sur plusieurs machines)
- Supporte la **scalabilité horizontale**
- Nécessite un **broker de messages** (Redis ou RabbitMQ)
- **Standard en production** pour les workloads importants

### KubernetesExecutor

```
Airflow Scheduler
      │
      └──► Kubernetes API
               ├──► Pod Task A (créé à la demande, détruit après)
               ├──► Pod Task B
               └──► Pod Task C
```

- Chaque tâche = un Pod Kubernetes éphémère
- **Isolation maximale** entre les tâches
- Scalabilité quasi illimitée
- Coûte plus cher en latence (création du pod ~30s)
- Adapté aux workloads Kubernetes natifs

---

## Configuration via airflow.cfg

Le fichier `airflow.cfg` (ou variables d'environnement `AIRFLOW__SECTION__KEY`) permet de personnaliser le comportement d'Airflow.

### Paramètres importants

```ini
[core]
# Répertoire des DAGs
dags_folder = /opt/airflow/dags

# Exécuteur (LocalExecutor par défaut)
executor = LocalExecutor

# Nombre maximum de tâches actives simultanément dans un même DAG
max_active_tasks_per_dag = 16

# Parallélisme global (toutes tâches, tous DAGs)
parallelism = 32

# Combien de DAG Runs actifs par DAG au maximum
max_active_runs_per_dag = 16

# Charger ou non les exemples Airflow
load_examples = False

[dag_processor]
# Fréquence de recherche de nouveaux fichiers dans le dossier dags (secondes)
refresh_interval = 300

# Délai minimal entre deux analyses d'un même fichier DAG (secondes)
min_file_process_interval = 30

# Nombre de processus d'analyse en parallèle
parsing_processes = 2

[scheduler]
# Rattrapage des runs manqués quand un DAG ne précise pas catchup (False par défaut en Airflow 3)
catchup_by_default = False

[api]
# Port de l'API Server (interface web + API REST)
port = 8080

# Nombre de processus de l'API Server
workers = 1

[database]
# Connexion à la metadata DB
sql_alchemy_conn = postgresql+psycopg2://user:pass@host/dbname

# Nombre de connexions dans le pool
sql_alchemy_pool_size = 5
```

> **Si vous venez d'Airflow 2 :** la section `[webserver]` (`web_server_port`, `workers`, `auth_backends`) a laissé place à `[api]`, et les réglages d'analyse des DAGs (`dag_dir_list_interval`, `parsing_processes`) sont passés de `[scheduler]` à `[dag_processor]`.

### Surcharge par variables d'environnement

Toutes les valeurs de `airflow.cfg` peuvent être surchargées par des variables d'environnement suivant ce pattern :

```
AIRFLOW__{SECTION}__{KEY}
```

Exemples :
```bash
# Équivalent à [core] load_examples = False
AIRFLOW__CORE__LOAD_EXAMPLES=False

# Équivalent à [api] port = 8080
AIRFLOW__API__PORT=8080

# Connexion DB
AIRFLOW__DATABASE__SQL_ALCHEMY_CONN=postgresql+psycopg2://airflow:airflow@postgres/airflow
```

C'est la méthode recommandée avec Docker Compose :

```yaml
environment:
  AIRFLOW__CORE__EXECUTOR: LocalExecutor
  AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
  AIRFLOW__CORE__PARALLELISM: '32'
  AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: postgresql+psycopg2://airflow:airflow@postgres/airflow
```

---

## Installer des providers (packages supplémentaires)

Airflow utilise un système de **providers** — des packages pip séparés pour chaque intégration externe.

```bash
# Lister les providers installés
airflow providers list

# Providers courants
pip install apache-airflow-providers-postgres    # PostgreSQL
pip install apache-airflow-providers-amazon       # AWS (S3, Redshift...)
pip install apache-airflow-providers-google       # GCP (BigQuery, GCS...)
pip install apache-airflow-providers-http         # HTTP/REST
pip install apache-airflow-providers-slack        # Slack notifications
pip install apache-airflow-providers-dbt-cloud    # dbt Cloud
```

En Airflow 3, même les opérateurs de base (`BashOperator`, `PythonOperator`, `EmptyOperator`...) vivent dans un provider : `apache-airflow-providers-standard`. Il est installé d'office avec Airflow, ainsi que `common-sql` (`SQLExecuteQueryOperator`).

### Avec Docker — image custom

```dockerfile
# Dockerfile
FROM apache/airflow:3.3.2-python3.12

# Installer des providers supplémentaires
# (répéter la version d'Airflow empêche pip de la changer par accident)
RUN pip install --no-cache-dir \
    "apache-airflow==${AIRFLOW_VERSION}" \
    apache-airflow-providers-postgres==7.0.2 \
    apache-airflow-providers-amazon==9.36.0 \
    apache-airflow-providers-http==6.1.0 \
    pandas \
    scikit-learn
```

Les versions de providers ci-dessus sont celles du [fichier de contraintes](https://raw.githubusercontent.com/apache/airflow/constraints-3.3.2/constraints-3.12.txt) d'Airflow 3.3.2 : c'est la référence pour connaître les versions testées avec une version donnée d'Airflow.

```yaml
# docker-compose.yaml — utiliser l'image custom
x-airflow-common:
  &airflow-common
  build: .    # au lieu de image: ${AIRFLOW_IMAGE_NAME:-apache/airflow:3.3.2}
```

```bash
# Rebuild l'image
docker compose build
docker compose up -d
```

---

## Commandes CLI essentielles

```bash
# Entrer dans un container Airflow
docker compose exec airflow-scheduler bash

# ---- Commandes DAGs ----
# Lister tous les DAGs
airflow dags list

# Déclencher manuellement un DAG
airflow dags trigger mon_dag

# Déclencher avec une date logique spécifique
airflow dags trigger mon_dag --logical-date 2024-01-15T00:00:00

# Tester un DAG : exécute un DAG Run complet dans le processus courant, sans scheduler
airflow dags test mon_dag 2024-01-15

# Mettre en pause/relancer un DAG
airflow dags pause mon_dag
airflow dags unpause mon_dag

# Rejouer une période passée (remplace "airflow dags backfill" d'Airflow 2)
airflow backfill create --dag-id mon_dag --from-date 2024-01-01 --to-date 2024-01-07

# ---- Commandes Tasks ----
# Tester une tâche spécifique
airflow tasks test mon_dag ma_tache 2024-01-15

# Lister les tâches d'un DAG
airflow tasks list mon_dag

# ---- Commandes DB ----
# Créer ou mettre à jour le schéma de la base de données
# (remplace "airflow db init" et "airflow db upgrade" d'Airflow 2)
airflow db migrate

# Réinitialiser la base de données (DANGER : efface tout)
airflow db reset

# ---- Commandes Variables ----
airflow variables set ma_variable "ma_valeur"
airflow variables get ma_variable

# ---- Commandes Connections ----
airflow connections list
airflow connections get ma_connexion
```

---

> 🔴 **ACTION FORMATEUR — CAPTURE REQUISE**
> **Capturer :** Terminal avec `docker compose ps` montrant tous les services en état "healthy", puis ouverture du navigateur sur http://localhost:8080
> **Expliquer :** Identifier chaque service dans la liste (apiserver, scheduler, dag-processor, triggerer, worker, postgres, redis). Expliquer que "healthy" signifie que le healthcheck Docker passe. Ouvrir l'interface et se connecter avec les identifiants par défaut.

---

## Vérification de l'installation

```bash
# Vérifier la version d'Airflow
docker compose exec airflow-scheduler airflow version

# Vérifier la santé des composants
curl http://localhost:8080/api/v2/monitor/health

# Réponse attendue :
# {
#   "metadatabase": {"status": "healthy"},
#   "scheduler": {"status": "healthy", "latest_scheduler_heartbeat": "..."},
#   "triggerer": {"status": "healthy", "latest_triggerer_heartbeat": "..."},
#   "dag_processor": {"status": "healthy", "latest_dag_processor_heartbeat": "..."}
# }
```

L'API REST d'Airflow 3 est servie sous `/api/v2` ; l'ancienne API `/api/v1` d'Airflow 2 a été retirée.

---

## Résolution des problèmes courants

### L'API Server (interface web) ne démarre pas

```bash
# Voir les logs
docker compose logs airflow-apiserver

# Problème courant : mémoire insuffisante allouée à Docker (4 Go minimum, 8 Go conseillés)

# Problème courant : droits sur le dossier logs
chmod -R 777 ./logs

# Problème : UID mismatch
echo "AIRFLOW_UID=$(id -u)" > .env
docker compose down && docker compose up -d
```

### "DAG not found" après avoir créé un fichier

```bash
# Le DAG Processor recherche les nouveaux fichiers toutes les 5 minutes par défaut
# ([dag_processor] refresh_interval) ; un fichier déjà connu est ré-analysé toutes les 30 s.
# Attendre ou forcer le rechargement :
docker compose exec airflow-scheduler airflow dags reserialize

# Si le DAG n'apparaît toujours pas, regarder les logs du DAG Processor :
docker compose logs airflow-dag-processor

# Vérifier les erreurs de parsing :
docker compose exec airflow-scheduler airflow dags list-import-errors
```

### Erreur de connexion à la DB

```bash
# Vérifier que postgres est bien démarré
docker compose ps postgres

# Tester la connexion
docker compose exec airflow-scheduler airflow db check
```

---

## Points clés à retenir

1. **Docker Compose** (fichier officiel) permet de voir tous les composants d'Airflow 3 : API Server, Scheduler, DAG Processor, Triggerer, workers
2. **LocalExecutor** pour le développement, **CeleryExecutor** pour la production simple, **KubernetesExecutor** pour Kubernetes
3. La configuration se fait via `airflow.cfg` ou variables d'environnement `AIRFLOW__SECTION__KEY`
4. Les **providers** sont des packages pip séparés pour chaque intégration
5. Le dossier `dags/` est **monté en volume** — tout fichier `.py` ajouté est automatiquement détecté par le DAG Processor
6. `airflow db migrate`, `airflow api-server` et `airflow dag-processor` remplacent `db init`, `webserver` et l'analyse intégrée au scheduler d'Airflow 2
