# 01 — Déploiement en Production

## Vue d'ensemble des options de déploiement

| Option | Usage | Complexité | Scalabilité |
|---|---|---|---|
| Docker Compose | Dev, petites équipes | Faible | Limitée |
| Docker Swarm | Production simple | Moyenne | Modérée |
| Kubernetes (KubernetesExecutor) | Production, grandes équipes | Élevée | Illimitée |
| Astronomer (Cloud/On-prem) | Managé | Faible (opérationnel) | Élevée |
| AWS MWAA | AWS managé | Faible | Élevée |
| Google Cloud Composer | GCP managé | Faible | Élevée |

> Le déploiement sur un Airflow hébergé (Astro) est décrit dans [`../06-Airflow3-Astro/01-airflow3-astro-snowflake.md`](../06-Airflow3-Astro/01-airflow3-astro-snowflake.md). Ce chapitre traite du déploiement auto-géré sur Kubernetes.

### Les composants à déployer en Airflow 3

| Composant | Commande | Rôle |
|---|---|---|
| Serveur d'API | `airflow api-server` | Interface web, API REST (`/api/v2`) et API d'exécution utilisée par les tâches. Remplace le `webserver` d'Airflow 2 |
| Scheduler | `airflow scheduler` | Planifie les DAG Runs et confie les tâches à l'executor |
| Processeur de DAGs | `airflow dag-processor` | Analyse les fichiers de DAGs. Composant séparé et **obligatoire** (il était intégré au Scheduler par défaut en Airflow 2) |
| Triggerer | `airflow triggerer` | Exécute les opérateurs différables (optionnel si aucun n'est utilisé) |
| Base de métadonnées | PostgreSQL | Initialisée et migrée avec `airflow db migrate` (`airflow db init` n'existe plus) |

En Airflow 3, une tâche n'accède plus directement à la base de métadonnées : elle dialogue avec le serveur d'API (API d'exécution). Les Pods de tâches doivent donc pouvoir joindre le serveur d'API, et tous les composants doivent partager le même secret JWT.

---

## Déploiement Kubernetes avec KubernetesExecutor

### Architecture

```
┌──────────────────────────────────────────────────────────────┐
│                      Kubernetes Cluster                      │
│                                                              │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────────┐    │
│  │  Deployment  │  │  Deployment  │  │    Deployment    │    │
│  │  API Server  │  │  Scheduler   │  │  DAG Processor   │    │
│  │ (UI + API)   │  │              │  │                  │    │
│  └──────┬───────┘  └──────┬───────┘  └────────┬─────────┘    │
│         │                 │                   │              │
│         └─────────────────┼───────────────────┘              │
│                           │                                  │
│               ┌───────────▼────────────┐                     │
│               │       PostgreSQL       │                     │
│               │     (Metadata DB)      │                     │
│               └────────────────────────┘                     │
│                                                              │
│  ┌────────────────────────────────────────────────────────┐  │
│  │  Pods Tâches (créés dynamiquement par le Scheduler)    │  │
│  │  ┌───────┐  ┌───────┐  ┌───────┐  ┌───────┐            │  │
│  │  │Task A │  │Task B │  │Task C │  │Task D │            │  │
│  │  │(Pod)  │  │(Pod)  │  │(Pod)  │  │(Pod)  │            │  │
│  │  └───┬───┘  └───┬───┘  └───┬───┘  └───┬───┘            │  │
│  └──────┼──────────┼──────────┼──────────┼────────────────┘  │
│         └──────────┴────┬─────┴──────────┘                   │
│                         ▼                                    │
│        API Server (API d'exécution) — pas d'accès            │
│        direct des tâches à la base de métadonnées            │
└──────────────────────────────────────────────────────────────┘
```

### Helm Chart officiel

```bash
# Ajouter le repo Helm Airflow
helm repo add apache-airflow https://airflow.apache.org
helm repo update

# Installer Airflow avec le KubernetesExecutor
helm install airflow apache-airflow/airflow \
    --namespace airflow \
    --create-namespace \
    --set executor=KubernetesExecutor \
    --set apiServer.service.type=LoadBalancer \
    -f values-production.yaml

# Voir les versions du chart disponibles et toutes les valeurs configurables
helm search repo apache-airflow/airflow --versions
helm show values apache-airflow/airflow
```

> Les valeurs `webserver.*` des tutoriels Airflow 2 sont remplacées par `apiServer.*`. Chaque version du chart embarque une version d'Airflow par défaut (le chart 1.22.0 déploie Airflow 3.2.2) : pour déployer une autre version, renseigner `airflowVersion` et le tag de l'image, comme ci-dessous. Référence : [documentation du chart Helm officiel](https://airflow.apache.org/docs/helm-chart/stable/index.html).

### values-production.yaml

```yaml
# values-production.yaml

# Executor
executor: KubernetesExecutor

# Version d'Airflow déployée (le chart adapte ses manifests à cette version)
airflowVersion: "3.3.2"

# Image personnalisée (avec nos providers installés)
images:
  airflow:
    repository: mon-registry.company.fr/airflow
    tag: "3.3.2-custom"
    pullPolicy: IfNotPresent

# Secrets Kubernetes créés au préalable (jamais de valeur en clair dans ce fichier)
fernetKeySecretName: airflow-fernet-key       # clé 'fernet-key'
jwtSecretName: airflow-jwt-secret             # clé 'jwt-secret' (jetons de l'API d'exécution)
apiSecretKeySecretName: airflow-api-secret    # clé 'api-secret-key'

# Base de métadonnées externe (PostgreSQL RDS, Cloud SQL...)
# Le secret contient la chaîne de connexion SQLAlchemy sous la clé 'connection'
data:
  metadataSecretName: airflow-metadata

# PostgreSQL intégré au chart (désactivé car DB externe)
postgresql:
  enabled: false

# Serveur d'API (interface web + API) — remplace la section `webserver` d'Airflow 2
apiServer:
  replicas: 2
  resources:
    requests:
      memory: "512Mi"
      cpu: "500m"
    limits:
      memory: "2Gi"
      cpu: "2"
  service:
    type: ClusterIP

# Scheduler
scheduler:
  replicas: 1
  resources:
    requests:
      memory: "1Gi"
      cpu: "500m"
    limits:
      memory: "4Gi"
      cpu: "2"

# Processeur de DAGs (composant séparé, obligatoire en Airflow 3)
dagProcessor:
  enabled: true
  replicas: 1

# Synchronisation des DAGs depuis Git
dags:
  gitSync:
    enabled: true
    repo: https://github.com/company/airflow-dags.git
    branch: main
    ref: main       # branche, tag ou commit (git-sync v4)
    depth: 1
    period: 30s     # Pull toutes les 30 secondes
    subPath: "dags"

# Logs dans S3
logs:
  persistence:
    enabled: false  # Utiliser S3 à la place

# Variables d'environnement supplémentaires
env:
  - name: AIRFLOW__CORE__LOAD_EXAMPLES
    value: "false"
  - name: AIRFLOW__DAG_PROCESSOR__REFRESH_INTERVAL
    value: "30"
  - name: AIRFLOW__CORE__PARALLELISM
    value: "64"
  - name: AIRFLOW__CORE__MAX_ACTIVE_TASKS_PER_DAG
    value: "16"
```

Quelques points d'attention :

- **Secrets stables** : sans `jwtSecretName`, le secret JWT généré par le chart change à chaque `helm upgrade`, ce qui peut faire échouer des tâches pendant le redéploiement (avertissement du `values.yaml` du chart). Même logique pour la clé Fernet : la fournir par un secret que l'on sauvegarde.
- **Authentification** : le chart configure par défaut le gestionnaire d'authentification FAB (`config.core.auth_manager`) et crée un utilisateur admin (`createUserJob`). L'image doit donc contenir le provider `apache-airflow-providers-fab` (c'est le cas de l'image officielle). Sans configuration, Airflow 3 utilise le `SimpleAuthManager`, réservé au développement.
- **`AIRFLOW__SCHEDULER__DAG_DIR_LIST_INTERVAL`** (Airflow 2) est remplacé par `AIRFLOW__DAG_PROCESSOR__REFRESH_INTERVAL`.
- **Bundles de DAGs** : Airflow 3 sait aussi lire les DAGs directement depuis Git via un *DAG bundle* (`GitDagBundle` du provider `git`, valeur `dagProcessor.dagBundleConfigList` du chart), avec versionnement des DAGs. git-sync reste pris en charge ; voir la documentation du chart avant de choisir.

---

## CI/CD pour les DAGs

### Stratégie de déploiement

```
Developer
    │
    ├──[git push] → GitHub/GitLab
    │                    │
    │              GitHub Actions
    │                    │
    │         ┌──────────┴──────────┐
    │         │                     │
    │     Lint/Tests          Build & Push
    │    (pytest, ruff)        Image Docker
    │         │                     │
    │         └──────────┬──────────┘
    │                    │ (si main branch)
    │              Helm upgrade
    │           (mise à jour Airflow)
    │
    └──[git-sync] → Airflow lit les DAGs depuis Git
                    (synchronisation automatique toutes les 30s)
```

### Pipeline CI/CD complet

```yaml
# .github/workflows/deploy-airflow.yml
name: Deploy Airflow DAGs

on:
  push:
    branches: [main]
  pull_request:
    branches: [main]

env:
  REGISTRY: ghcr.io
  IMAGE_NAME: ${{ github.repository }}/airflow

jobs:
  # ---- Job 1 : Lint et tests ----
  lint-and-test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4

      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.12'

      - name: Install dependencies
        env:
          CONSTRAINTS: https://raw.githubusercontent.com/apache/airflow/constraints-3.3.2/constraints-3.12.txt
        run: |
          pip install ruff "apache-airflow==3.3.2" pytest pytest-mock --constraint "$CONSTRAINTS"
          pip install -r requirements.txt --constraint "$CONSTRAINTS"

      - name: Lint avec Ruff
        run: ruff check dags/ tests/

      - name: Tester les DAGs
        env:
          AIRFLOW__DATABASE__SQL_ALCHEMY_CONN: sqlite:////tmp/airflow.db
          AIRFLOW__CORE__LOAD_EXAMPLES: 'false'
        run: |
          airflow db migrate
          pytest tests/ -v

  # ---- Job 2 : Build et push de l'image Docker ----
  build-and-push:
    needs: lint-and-test
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    permissions:
      contents: read
      packages: write
    steps:
      - uses: actions/checkout@v4

      - name: Login to Container Registry
        uses: docker/login-action@v3
        with:
          registry: ${{ env.REGISTRY }}
          username: ${{ github.actor }}
          password: ${{ secrets.GITHUB_TOKEN }}

      - name: Build and push Docker image
        uses: docker/build-push-action@v5
        with:
          context: .
          push: true
          tags: |
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:latest
            ${{ env.REGISTRY }}/${{ env.IMAGE_NAME }}:${{ github.sha }}
          cache-from: type=gha
          cache-to: type=gha,mode=max

  # ---- Job 3 : Déploiement Kubernetes ----
  deploy:
    needs: build-and-push
    if: github.ref == 'refs/heads/main'
    runs-on: ubuntu-latest
    environment: production
    steps:
      - uses: actions/checkout@v4

      - name: Configure kubectl
        uses: azure/k8s-set-context@v3
        with:
          kubeconfig: ${{ secrets.KUBECONFIG }}

      - name: Deploy with Helm
        run: |
          helm repo add apache-airflow https://airflow.apache.org
          helm repo update
          helm upgrade airflow apache-airflow/airflow \
            --namespace airflow \
            --set images.airflow.tag=${{ github.sha }} \
            --wait \
            --timeout 10m \
            -f helm/values-production.yaml
```

---

## Dockerfile de production

```dockerfile
# Dockerfile
FROM apache/airflow:3.3.2-python3.12

USER root
RUN apt-get update && apt-get install -y \
    gcc \
    libpq-dev \
    && rm -rf /var/lib/apt/lists/*

USER airflow

# Installer les providers et dépendances
COPY requirements.txt /requirements.txt
RUN pip install --no-cache-dir \
    -c https://raw.githubusercontent.com/apache/airflow/constraints-3.3.2/constraints-3.12.txt \
    -r /requirements.txt

# Copier le code des utilitaires (pas les DAGs — ils viennent de git-sync)
COPY --chown=airflow:root dags/utils/ /opt/airflow/dags/utils/
```

```txt
# requirements.txt
# Pas de version épinglée pour les providers et les bibliothèques connues d'Airflow :
# c'est le fichier de contraintes (-c) qui fixe les versions testées avec Airflow 3.3.2.
apache-airflow-providers-postgres
apache-airflow-providers-amazon
apache-airflow-providers-http
apache-airflow-providers-slack
apache-airflow-providers-dbt-cloud
pandas
pyarrow
scikit-learn
# Absent du fichier de contraintes : à épingler vous-même après test
mlflow
```

> L'image officielle `apache/airflow` contient déjà les providers les plus courants (dont `standard`, `common-sql`, `postgres`, `amazon`, `http`, `fab`). Vérifier avec `docker run --rm apache/airflow:3.3.2 airflow providers list`.

---

## Supervision et Alertes

### Métriques Airflow avec Prometheus

```ini
# airflow.cfg
[metrics]
statsd_on = True
statsd_host = prometheus-statsd-exporter
statsd_port = 9125
statsd_prefix = airflow
```

Le chart Helm officiel déploie par défaut un exporteur StatsD pour Prometheus (`statsd.enabled: true`) et renseigne lui-même ces options : il reste à faire collecter son endpoint `/metrics` par Prometheus. Airflow sait aussi exporter ses métriques en OpenTelemetry (`[metrics] otel_on`).

### Alertes sur échec de DAG

```python
# dags/utils/alerting.py

def alerter_sur_echec(context):
    """
    Callback d'alerte Slack à appeler en cas d'échec.
    Usage : on_failure_callback=alerter_sur_echec dans le default_args
    """
    import json
    from airflow.providers.http.hooks.http import HttpHook

    ti = context.get('task_instance')
    dag = context['dag']
    exception = context.get('exception')

    message = {
        "text": f":red_circle: *Échec Pipeline Airflow*",
        "attachments": [{
            "color": "danger",
            "fields": [
                {"title": "DAG", "value": dag.dag_id, "short": True},
                {"title": "Tâche", "value": ti.task_id if ti else "—", "short": True},
                {"title": "Date", "value": context.get('ds', '—'), "short": True},
                {"title": "Run ID", "value": context['run_id'], "short": False},
                {"title": "Erreur", "value": str(exception)[:500] if exception else "Inconnue", "short": False},
                {"title": "Logs", "value": ti.log_url if ti else "—", "short": False},
            ]
        }]
    }

    hook = HttpHook(method='POST', http_conn_id='slack_webhook')
    hook.run(
        endpoint='/hooks/TXXXXX/BXXXXX/XXXXXXXX',
        data=json.dumps(message),
        headers={'Content-Type': 'application/json'},
    )
```

```python
# Utilisation dans les DAGs
from datetime import datetime, timedelta
from airflow.sdk import DAG
from utils.alerting import alerter_sur_echec

default_args = {
    'owner': 'data-team',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
    'on_failure_callback': alerter_sur_echec,  # ← Alerte sur chaque tâche en échec
}

with DAG(
    dag_id='pipeline_critique',
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    default_args=default_args,
    on_failure_callback=alerter_sur_echec,  # ← Alerte sur le DAG Run entier
) as dag:
    pass
```

Le callback d'une tâche s'exécute dans le processus de la tâche ; celui du DAG est exécuté par le processeur de DAGs, avec le contexte de la dernière tâche du run (d'où les `context.get(...)` : certaines clés peuvent manquer).

Plutôt qu'une fonction écrite à la main, on peut utiliser un **notifier** fourni par un provider : c'est la voie recommandée en Airflow 3 (la gestion des SLA et `sla_miss_callback` d'Airflow 2 ont été supprimés).

```python
from airflow.providers.smtp.notifications.smtp import SmtpNotifier

notifier_echec = SmtpNotifier(
    to='data-team@company.fr',
    subject='[Airflow] Échec de {{ dag.dag_id }}',
    html_content='Le run {{ run_id }} a échoué.',
    smtp_conn_id='smtp_default',
)

# Puis, dans le DAG ou dans default_args : on_failure_callback=notifier_echec
```

Le provider Slack propose l'équivalent pour Slack (voir sa documentation, module `airflow.providers.slack.notifications`).

---

> 🔴 **ACTION FORMATEUR — CAPTURE REQUISE**
> **Capturer :** Une notification Slack reçue suite à l'échec d'une tâche Airflow — montrant les détails (DAG, tâche, erreur, lien vers les logs)
> **Expliquer :** Montrer que la notification contient directement le lien vers les logs Airflow (`ti.log_url`). Expliquer la différence entre `on_failure_callback` sur une tâche (se déclenche quand la tâche échoue définitivement, une fois ses retries épuisés ; `on_retry_callback` couvre chaque tentative ratée) vs sur le DAG (se déclenche quand le DAG Run passe en échec). Montrer comment simuler un échec pour tester l'alerte.

---

## Gestion des logs en production

### Logs vers S3

```ini
# airflow.cfg
[logging]
remote_logging = True
remote_base_log_folder = s3://mon-bucket-logs/airflow
remote_log_conn_id = aws_production
encrypt_s3_logs = True
```

```yaml
# Kubernetes — variables d'environnement
env:
  - name: AIRFLOW__LOGGING__REMOTE_LOGGING
    value: "true"
  - name: AIRFLOW__LOGGING__REMOTE_BASE_LOG_FOLDER
    value: "s3://mon-bucket-logs/airflow"
  - name: AIRFLOW__LOGGING__REMOTE_LOG_CONN_ID
    value: "aws_production"
```

### Nettoyage des logs locaux et de la base de métadonnées

```ini
[logging]
# Supprimer les fichiers de logs locaux une fois envoyés vers le stockage distant
delete_local_logs = True
```

Airflow ne fait pas lui-même la rotation de ses logs locaux : sans stockage distant, prévoir un nettoyage externe (le chart Helm propose pour cela un conteneur *log groomer* sur les composants qui écrivent des logs). La base de métadonnées grossit elle aussi (DAG Runs, instances de tâches, XCom) ; la purge se fait avec `airflow db clean`, à planifier régulièrement :

```bash
# Simuler puis purger les enregistrements antérieurs au 1er janvier 2026
airflow db clean --clean-before-timestamp '2026-01-01 00:00:00+00:00' --dry-run
airflow db clean --clean-before-timestamp '2026-01-01 00:00:00+00:00' --yes
```

---

## Checklist de mise en production

```
Infrastructure
□ PostgreSQL externe (RDS, Cloud SQL, etc.) — jamais SQLite
□ Fernet key configurée et sauvegardée
□ Secret JWT et clé secrète de l'API fixés (identiques pour tous les composants)
□ Secrets dans Kubernetes Secrets ou Vault (jamais en clair dans les manifests)
□ Ingress HTTPS configuré pour le serveur d'API
□ Gestionnaire d'authentification de production configuré (pas le SimpleAuthManager)
□ Monitoring (Prometheus + Grafana) connecté

DAGs
□ Tests unitaires passent (pytest)
□ Tests d'intégrité DAG passent (DagBag)
□ catchup configuré intentionnellement
□ Toutes les tâches idempotentes
□ on_failure_callback configuré pour les DAGs critiques
□ Timeouts définis sur les tâches longues
□ Retries configurés avec backoff exponentiel

CI/CD
□ Pipeline CI/CD qui valide les DAGs avant merge
□ Build de l'image Docker automatisé
□ Déploiement Helm automatisé sur la branche main
□ Environnements dev/staging/prod séparés

Opérations
□ Alertes Slack/PagerDuty sur les échecs critiques
□ Nettoyage des logs et purge de la metadata DB (airflow db clean) planifiés
□ Backup de la metadata DB planifié
□ Plan de disaster recovery documenté
□ Runbooks pour les incidents courants
```

---

> 🔴 **ACTION FORMATEUR — CAPTURE REQUISE**
> **Capturer :** Le tableau de bord Grafana montrant les métriques Airflow (nombre de DAG Runs actifs, tâches en échec, latence du Scheduler)
> **Expliquer :** Pointer les métriques clés (préfixées par `airflow`) : `scheduler_heartbeat` (le scheduler est vivant), `ti_successes` et `ti_failures` (débit et taux d'erreur), `dagrun.duration.*` (durée des runs), `dag_processing.total_parse_time` (santé du processeur de DAGs). La liste complète figure dans la documentation officielle (page « Metrics »). Expliquer comment créer des alertes Grafana sur ces métriques.

---

## Points clés à retenir

1. **KubernetesExecutor** = scalabilité maximale, chaque tâche dans un Pod éphémère
2. **Helm Chart officiel** pour déployer Airflow sur Kubernetes ; en Airflow 3 : serveur d'API (`apiServer`) à la place du webserver, processeur de DAGs séparé
3. **git-sync** pour synchroniser les DAGs depuis Git automatiquement
4. Le CI/CD doit : linter → tester → build image → déployer
5. Configurer des **alertes Slack** via `on_failure_callback` pour les pipelines critiques
6. En production : PostgreSQL externe, Fernet key et secret JWT fixés, logs distants (S3), monitoring Prometheus
