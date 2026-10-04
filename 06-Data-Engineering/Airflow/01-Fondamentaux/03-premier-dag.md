# 03 — Premier DAG

## Structure d'un fichier DAG

Un fichier DAG Airflow est un fichier Python standard placé dans le répertoire `dags/`.

### Squelette minimal

```python
# dags/mon_premier_dag.py

from datetime import datetime, timedelta
from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator

# -------------------------------------------------------
# 1. Arguments par défaut — appliqués à toutes les tâches
# -------------------------------------------------------
default_args = {
    'owner': 'formation',               # Propriétaire du DAG
    'depends_on_past': False,           # Ne pas dépendre de l'exécution précédente
    'retries': 1,                       # Nombre de tentatives en cas d'échec
    'retry_delay': timedelta(minutes=5), # Délai entre les tentatives
}

# -------------------------------------------------------
# 2. Définition du DAG
# -------------------------------------------------------
with DAG(
    dag_id='mon_premier_dag',           # Identifiant unique du DAG
    description='Mon premier pipeline Airflow',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),    # Date de début de la planification
    schedule='@daily',                  # Planification (cron ou preset)
    catchup=False,                      # Ne pas rattraper les runs passés (défaut en Airflow 3)
    tags=['formation', 'débutant'],     # Tags pour filtrer dans l'UI
) as dag:

    # -------------------------------------------------------
    # 3. Définition des tâches
    # -------------------------------------------------------
    tache_bash = BashOperator(
        task_id='tache_bash',
        bash_command='echo "Bonjour depuis Bash ! Date : $(date)"',
    )

    def ma_fonction_python():
        print("Bonjour depuis Python !")
        print(f"Exécution en cours...")
        return "résultat"

    tache_python = PythonOperator(
        task_id='tache_python',
        python_callable=ma_fonction_python,
    )

    tache_finale = BashOperator(
        task_id='tache_finale',
        bash_command='echo "Pipeline terminé avec succès !"',
    )

    # -------------------------------------------------------
    # 4. Définition des dépendances
    # -------------------------------------------------------
    tache_bash >> tache_python >> tache_finale
```

> **Si vous venez d'Airflow 2 :** les imports ont changé. `from airflow import DAG` devient `from airflow.sdk import DAG`, et les opérateurs de base ont déménagé dans le provider *standard* : `airflow.operators.bash` → `airflow.providers.standard.operators.bash`, `airflow.operators.python` → `airflow.providers.standard.operators.python`. L'argument `schedule_interval` du DAG n'existe plus : seul `schedule` est accepté.

---

## Les éléments clés d'un DAG

### Le dag_id

```python
dag_id='mon_premier_dag'
```

- **Doit être unique** dans toute l'instance Airflow
- Sert d'identifiant du DAG dans la metadata DB
- Convention de nommage : `snake_case`, préfixe par domaine (`etl_`, `ml_`, `reporting_`)
- Exemples : `etl_ventes_quotidien`, `ml_recommandation_hebdo`

### Le start_date

```python
start_date=datetime(2024, 1, 1)
```

- Date à partir de laquelle Airflow commence à planifier ce DAG
- **Ne pas utiliser `datetime.now()`** — cela crée un start_date différent à chaque parsing du fichier

```python
# ❌ Mauvais — ne jamais faire ça
start_date=datetime.now()

# ✓ Correct — date fixe dans le passé
start_date=datetime(2024, 1, 1)
```

### Le schedule

```python
# Presets Airflow
schedule='@once'       # Une seule fois
schedule='@hourly'     # Toutes les heures
schedule='@daily'      # Tous les jours à minuit UTC
schedule='@weekly'     # Tous les dimanches à minuit UTC
schedule='@monthly'    # Le 1er de chaque mois
schedule=None          # Pas de planification automatique (déclenché manuellement)

# Expressions cron (5 champs : min heure jour_mois mois jour_semaine)
schedule='0 6 * * *'   # Tous les jours à 06h00 UTC
schedule='0 9 * * 1'   # Tous les lundis à 09h00 UTC
schedule='*/15 * * * *' # Toutes les 15 minutes

# timedelta
from datetime import timedelta
schedule=timedelta(hours=6)  # Toutes les 6 heures
```

**Date logique et intervalle de données.** Avec un preset ou une expression cron, Airflow 3 utilise par défaut la timetable `CronTriggerTimetable` : le run planifié à 06h00 le 15 janvier a pour `logical_date` le 15 janvier à 06h00, et `data_interval_start` = `data_interval_end` = `logical_date`. Si votre tâche doit traiter « la journée d'hier », elle calcule la période à partir de `logical_date`.

Pour retrouver le comportement d'Airflow 2 (le run couvre la période *précédant* son déclenchement, entre `data_interval_start` et `data_interval_end`), choisissez explicitement la timetable par intervalles :

```python
from airflow.timetables.interval import CronDataIntervalTimetable

# Le run déclenché le 16 janvier à 00h00 couvre [15 janvier 00h00, 16 janvier 00h00)
schedule=CronDataIntervalTimetable("0 0 * * *", timezone="UTC")
```

### Le catchup

```python
catchup=False  # Valeur par défaut en Airflow 3
```

- `catchup=True` : si le DAG a un `start_date` dans le passé, Airflow va créer **tous les DAG Runs manqués** depuis ce start_date
- `catchup=False` (défaut) : Airflow ne crée que le run le plus récent, puis suit la planification

> En Airflow 2, le défaut était `catchup=True` : beaucoup de tutoriels écrivent donc `catchup=False` explicitement. Le garder ne coûte rien et rend l'intention lisible.

```python
# Exemple avec catchup=True :
# start_date = 2024-01-01, schedule = @daily, DAG activé le 10 janvier à 09h00
# → Airflow crée 10 DAG Runs (du 1er au 10 janvier, un par minuit écoulé)

# Avec catchup=False :
# → Airflow crée uniquement le run du 10 janvier (le plus récent)
```

Pour rejouer volontairement une période passée, on utilise un **backfill** (`airflow backfill create --dag-id ... --from-date ... --to-date ...`, ou le bouton de déclenchement de l'interface).

---

## BashOperator

Exécute une commande shell dans un sous-processus.

```python
from airflow.providers.standard.operators.bash import BashOperator

# Commande simple
tache_simple = BashOperator(
    task_id='echo_date',
    bash_command='echo "Aujourd\'hui : $(date +%Y-%m-%d)"',
)

# Commande multi-lignes avec bash_command
tache_multilignes = BashOperator(
    task_id='script_multilignes',
    bash_command="""
        echo "Étape 1 : création du répertoire"
        mkdir -p /tmp/airflow_output

        echo "Étape 2 : génération des données"
        echo "data,$(date +%Y-%m-%d)" > /tmp/airflow_output/result.csv

        echo "Étape 3 : vérification"
        cat /tmp/airflow_output/result.csv
    """,
)

# Avec variables d'environnement
tache_env = BashOperator(
    task_id='avec_env',
    bash_command='echo "Env: $MON_ENV"',
    env={'MON_ENV': 'production'},
)

# Avec paramètres de template (Jinja2)
tache_template = BashOperator(
    task_id='avec_template',
    # {{ ds }} est remplacé par la date logique du run au format YYYY-MM-DD
    bash_command='echo "Date logique : {{ ds }}"',
)
```

### Variables de template Jinja2 disponibles

```python
{{ ds }}              # Date logique au format YYYY-MM-DD
{{ ds_nodash }}       # YYYYMMDD
{{ ts }}              # Timestamp ISO 8601
{{ ts_nodash }}       # YYYYMMDDTHHMMSS
{{ logical_date }}    # Date logique (objet datetime)
{{ data_interval_start }}  # Début de l'intervalle de données
{{ data_interval_end }}    # Fin de l'intervalle de données
{{ dag.dag_id }}      # ID du DAG
{{ task.task_id }}    # ID de la tâche courante
{{ run_id }}          # ID du DAG Run
{{ macros.ds_add(ds, 7) }}  # ds + 7 jours
{{ macros.ds_add(ds, -1) }} # ds - 1 jour (la veille)
```

> Les variables `execution_date`, `prev_ds`, `next_ds`, `yesterday_ds`, `tomorrow_ds`, `prev_execution_date` et `next_execution_date`, fréquentes dans les tutoriels Airflow 2, n'existent plus en Airflow 3. Utilisez `logical_date`, `data_interval_start`, `data_interval_end` et `macros.ds_add`.

---

## PythonOperator

Exécute une fonction Python.

```python
from airflow.providers.standard.operators.python import PythonOperator

# Fonction simple
def extraire_donnees():
    import requests
    response = requests.get("https://api.example.com/data")
    data = response.json()
    print(f"Récupéré {len(data)} enregistrements")
    return len(data)

tache_extraction = PythonOperator(
    task_id='extraire_donnees',
    python_callable=extraire_donnees,
)

# Avec des arguments
def transformer_donnees(source: str, limite: int):
    print(f"Transformation de {limite} enregistrements depuis {source}")
    # ... logique de transformation
    return f"Transformation terminée : {limite} lignes"

tache_transformation = PythonOperator(
    task_id='transformer_donnees',
    python_callable=transformer_donnees,
    op_kwargs={           # Arguments nommés passés à la fonction
        'source': 'api_ventes',
        'limite': 1000,
    },
    # op_args=['arg1', 'arg2']  # Arguments positionnels (liste)
)

# Accéder au contexte Airflow dans la fonction
def tache_avec_contexte(**context):
    """
    En passant **context, vous pouvez accéder à toutes les
    métadonnées du run Airflow. (L'argument provide_context=True
    des vieux tutoriels n'existe plus : le contexte est toujours fourni.)
    """
    date_logique = context['logical_date']
    dag_id = context['dag'].dag_id
    task_id = context['task'].task_id
    run_id = context['run_id']

    print(f"DAG: {dag_id}, Task: {task_id}")
    print(f"Date logique: {date_logique}")
    print(f"Run ID: {run_id}")

tache_contexte = PythonOperator(
    task_id='tache_avec_contexte',
    python_callable=tache_avec_contexte,
)
```

---

## Un DAG complet : pipeline ETL simple

```python
# dags/etl_simple.py

from datetime import datetime, timedelta
import pandas as pd
import json
import os

from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator

default_args = {
    'owner': 'data-team',
    'depends_on_past': False,
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
}

with DAG(
    dag_id='etl_meteo_simple',
    description='Pipeline ETL : extraction météo, transformation, sauvegarde',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule='0 8 * * *',  # Tous les jours à 8h
    catchup=False,
    tags=['etl', 'météo', 'formation'],
) as dag:

    # -------------------------------------------------------
    # Étape 1 : Vérification que l'API est disponible
    # -------------------------------------------------------
    verifier_api = BashOperator(
        task_id='verifier_api',
        bash_command='curl -sf https://api.open-meteo.com/v1/forecast?latitude=48.85&longitude=2.35&current_weather=true || exit 1',
    )

    # -------------------------------------------------------
    # Étape 2 : Extraction des données
    # -------------------------------------------------------
    def extraire_meteo(**context):
        import requests

        # Récupérer la date logique pour construire l'URL
        # (avec ce schedule cron : le jour du déclenchement, à 8h)
        exec_date = context['ds']  # Format: YYYY-MM-DD

        url = (
            "https://api.open-meteo.com/v1/forecast"
            "?latitude=48.8566&longitude=2.3522"
            "&daily=temperature_2m_max,temperature_2m_min,precipitation_sum"
            f"&start_date={exec_date}&end_date={exec_date}"
            "&timezone=Europe/Paris"
        )

        response = requests.get(url, timeout=10)
        response.raise_for_status()
        data = response.json()

        # Sauvegarder le JSON brut
        output_path = f'/tmp/meteo_raw_{exec_date}.json'
        with open(output_path, 'w') as f:
            json.dump(data, f, indent=2)

        print(f"Données sauvegardées dans {output_path}")
        return output_path

    extraire = PythonOperator(
        task_id='extraire_meteo',
        python_callable=extraire_meteo,
    )

    # -------------------------------------------------------
    # Étape 3 : Transformation
    # -------------------------------------------------------
    def transformer_meteo(**context):
        exec_date = context['ds']
        input_path = f'/tmp/meteo_raw_{exec_date}.json'

        with open(input_path) as f:
            raw = json.load(f)

        # Extraire les données pertinentes
        daily = raw.get('daily', {})
        df = pd.DataFrame({
            'date': daily.get('time', []),
            'temp_max': daily.get('temperature_2m_max', []),
            'temp_min': daily.get('temperature_2m_min', []),
            'precipitation': daily.get('precipitation_sum', []),
        })

        # Calculs supplémentaires
        df['temp_moyenne'] = (df['temp_max'] + df['temp_min']) / 2
        df['source'] = 'open-meteo'
        df['extracted_at'] = datetime.now().isoformat()

        output_path = f'/tmp/meteo_transformed_{exec_date}.csv'
        df.to_csv(output_path, index=False)

        print(f"DataFrame transformé :\n{df.to_string()}")
        print(f"Sauvegardé dans {output_path}")
        return output_path

    transformer = PythonOperator(
        task_id='transformer_meteo',
        python_callable=transformer_meteo,
    )

    # -------------------------------------------------------
    # Étape 4 : Chargement (simulation d'un INSERT SQL)
    # -------------------------------------------------------
    def charger_meteo(**context):
        exec_date = context['ds']
        input_path = f'/tmp/meteo_transformed_{exec_date}.csv'

        df = pd.read_csv(input_path)

        # Simulation d'un chargement (ici on loggue)
        for _, row in df.iterrows():
            print(f"INSERT INTO meteo_daily VALUES ({dict(row)})")

        print(f"{len(df)} lignes chargées avec succès")
        return len(df)

    charger = PythonOperator(
        task_id='charger_meteo',
        python_callable=charger_meteo,
    )

    # -------------------------------------------------------
    # Étape 5 : Nettoyage des fichiers temporaires
    # -------------------------------------------------------
    nettoyer = BashOperator(
        task_id='nettoyer',
        bash_command='rm -f /tmp/meteo_raw_{{ ds }}.json /tmp/meteo_transformed_{{ ds }}.csv',
    )

    # -------------------------------------------------------
    # Dépendances
    # -------------------------------------------------------
    verifier_api >> extraire >> transformer >> charger >> nettoyer
```

---

> 🔴 **ACTION FORMATEUR — CAPTURE REQUISE**
> **Capturer :** Le DAG `etl_meteo_simple` dans l'interface Airflow — vue Graph montrant les 5 tâches en vert après une exécution réussie
> **Expliquer :** Montrer comment naviguer dans la vue Graph. Cliquer sur chaque tâche pour voir : le statut, la durée d'exécution, les logs. Ouvrir les logs de `extraire_meteo` pour montrer le print du DataFrame.

---

## Définir des dépendances entre tâches

### Opérateurs `>>` et `<<`

```python
# Syntaxe avec >> (recommandée — plus lisible)
tache_a >> tache_b            # b dépend de a
tache_a >> tache_b >> tache_c  # chaîne séquentielle

# Syntaxe avec << (dépendance inversée)
tache_b << tache_a            # équivalent à a >> b

# Dépendances multiples — fanout
tache_a >> [tache_b, tache_c]  # b et c sont en parallèle après a

# Dépendances multiples — fanin
[tache_b, tache_c] >> tache_d  # d attend que b ET c soient terminées

# Combinaison
tache_a >> [tache_b, tache_c] >> tache_d
# Résultat :
#   tache_a
#   ├── tache_b ──► tache_d
#   └── tache_c ──► tache_d
```

### Méthodes `set_upstream` et `set_downstream`

```python
# Équivalent à tache_a >> tache_b
tache_b.set_upstream(tache_a)

# Équivalent aussi à tache_a >> tache_b
tache_a.set_downstream(tache_b)

# Utilisation de la fonction chain pour les chaînes longues
from airflow.sdk import chain

chain(tache_a, tache_b, tache_c, tache_d)
# Équivalent à : tache_a >> tache_b >> tache_c >> tache_d

# chain avec parallélisme
chain(tache_a, [tache_b, tache_c], tache_d)
# Équivalent à : tache_a >> [tache_b, tache_c] >> tache_d
```

### Exemple de topologie complexe

```python
with DAG('topologie_complexe', ...) as dag:

    debut = BashOperator(task_id='debut', bash_command='echo "start"')

    verif_a = BashOperator(task_id='verif_a', bash_command='echo "check a"')
    verif_b = BashOperator(task_id='verif_b', bash_command='echo "check b"')

    process_1 = BashOperator(task_id='process_1', bash_command='echo "p1"')
    process_2 = BashOperator(task_id='process_2', bash_command='echo "p2"')
    process_3 = BashOperator(task_id='process_3', bash_command='echo "p3"')

    agregation = BashOperator(task_id='agregation', bash_command='echo "merge"')
    notification = BashOperator(task_id='notification', bash_command='echo "notify"')

    # Topologie :
    #
    #                ┌── verif_a ─► process_1 ──┐
    # debut ──────────                            ├── agregation ──► notification
    #                └── verif_b ─► process_2 ──┘
    #                               └─────────► process_3 ──┘

    debut >> [verif_a, verif_b]
    verif_a >> process_1
    verif_b >> [process_2, process_3]
    [process_1, process_2, process_3] >> agregation
    agregation >> notification
```

---

## Gestion des erreurs et retries

```python
from datetime import timedelta
from airflow.providers.standard.operators.python import PythonOperator

def tache_fragile(**context):
    import random
    if random.random() < 0.3:
        raise ValueError("Erreur simulée !")
    print("Tâche réussie !")

def callback_echec(context):
    """Appelé automatiquement en cas d'échec de la tâche."""
    task_instance = context['task_instance']
    print(f"ALERTE: La tâche {task_instance.task_id} a échoué !")
    print(f"Exception: {context.get('exception')}")
    # Ici vous pouvez envoyer une alerte Slack, PagerDuty, etc.

def callback_succes(context):
    """Appelé en cas de succès."""
    print("Tâche réussie, notification envoyée.")

tache_avec_gestion_erreurs = PythonOperator(
    task_id='tache_fragile',
    python_callable=tache_fragile,
    retries=3,
    retry_delay=timedelta(seconds=30),
    retry_exponential_backoff=2.0,   # Délai multiplié par 2 à chaque retry (30 s, 1 min, 2 min...)
    max_retry_delay=timedelta(minutes=10),
    on_failure_callback=callback_echec,
    on_success_callback=callback_succes,
    # execution_timeout : temps maximum avant de considérer la tâche comme échouée
    execution_timeout=timedelta(minutes=30),
)
```

> Les arguments `email`, `email_on_failure` et `email_on_retry`, très présents dans les `default_args` des tutoriels Airflow 2, sont dépréciés en Airflow 3 (ils déclenchent un avertissement et disparaîtront en Airflow 4). Pour alerter par e-mail, on passe désormais un *notifier* au callback, par exemple `SmtpNotifier` du provider `smtp` ; les notifications sont abordées dans le [module 6](../06-Airflow3-Astro/01-airflow3-astro-snowflake-dbt.md).
>
> En Airflow 3, `retry_exponential_backoff` est un **multiplicateur** (0 = délai constant, 2.0 = le délai double à chaque tentative), et non plus un booléen comme en Airflow 2. Autre suppression à connaître : les SLA (`sla`, `sla_miss_callback`) n'existent plus.

---

> 🔴 **ACTION FORMATEUR — CAPTURE REQUISE**
> **Capturer :** Une Task Instance en état "failed" dans l'interface Airflow — afficher les logs d'erreur et le bouton "Clear" pour relancer
> **Expliquer :** Montrer comment lire les logs d'erreur (traceback Python visible directement dans l'UI). Montrer le compteur de retries. Expliquer le bouton "Clear" qui remet la tâche à l'état `none` pour qu'elle soit replanifiée. Montrer aussi "Mark as Success" pour forcer un succès.

---

## Bonnes pratiques pour le premier DAG

### Ce qu'il faut faire

```python
# ✓ Imports Airflow en haut du fichier
from airflow.sdk import DAG
from airflow.providers.standard.operators.python import PythonOperator
from datetime import datetime, timedelta

# ✓ default_args défini séparément
default_args = {
    'owner': 'equipe-data',
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

# ✓ catchup=False (explicite, même si c'est le défaut en Airflow 3)
# ✓ start_date fixe dans le passé
# ✓ tags pour faciliter la recherche dans l'UI
with DAG(
    dag_id='etl_ventes_v1',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    catchup=False,
    tags=['etl', 'ventes'],
) as dag:
    pass
```

### Ce qu'il ne faut pas faire

```python
# ❌ Ne pas faire de requêtes HTTP/DB au niveau du DAG (top-level)
# Ceci est exécuté à chaque analyse du fichier par le DAG Processor (toutes les 30s !)
response = requests.get("http://api.example.com")  # ← MAUVAIS

# ❌ Ne pas utiliser datetime.now() pour start_date
with DAG(start_date=datetime.now(), ...):  # ← MAUVAIS

# ❌ Ne pas faire d'imports lourds au top-level du fichier
import pandas as pd  # ← Éviter si non nécessaire au parsing
import torch         # ← Éviter absolument

# ✓ Faire les imports à l'intérieur des fonctions Python
def ma_tache():
    import pandas as pd  # ← Import local dans la fonction, OK
    df = pd.DataFrame(...)
```

---

## Points clés à retenir

1. Un DAG = un fichier Python dans le dossier `dags/`
2. `BashOperator` pour les commandes shell, `PythonOperator` pour le code Python
3. La syntaxe `>>` définit les dépendances dans l'ordre d'exécution
4. `start_date` doit être une date **fixe** — jamais `datetime.now()`
5. `catchup=False` (défaut en Airflow 3) évite les runs en retard non désirés
6. Les templates Jinja `{{ ds }}` permettent d'accéder aux métadonnées du run ; avec un schedule cron, la date logique est par défaut la date de déclenchement
7. Les callbacks (`on_failure_callback`) permettent d'alerter en cas d'échec
