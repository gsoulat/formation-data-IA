# 01 — Idempotence et Sécurité des Ré-exécutions

## Qu'est-ce que l'idempotence ?

Une tâche est **idempotente** si son exécution plusieurs fois avec les mêmes paramètres produit le même résultat que si elle avait été exécutée une seule fois.

En pratique : **re-exécuter une tâche ne doit pas dupliquer les données ni produire d'effets indésirables**.

> L'idempotence est probablement le principe le plus important dans les pipelines de données. Sans elle, un retry automatique ou un rejoue manuel peut corrompre vos données.

---

## Pourquoi c'est crucial avec Airflow

Airflow re-exécute des tâches dans plusieurs situations :
- **Retry automatique** après un échec (si `retries > 0`)
- **Rejoue manuel** via "Clear" dans l'interface
- **Backfill** pour rattraper des dates passées
- **Catchup** au démarrage d'un nouveau DAG (si `catchup=True`)

Si vos tâches ne sont pas idempotentes → **données dupliquées**.

---

## Exemples : idempotent vs non-idempotent

Dans les exemples ci-dessous, `context['ds']` est la **date logique** du run au format `YYYY-MM-DD`. Le hook s'importe avec `from airflow.providers.postgres.hooks.postgres import PostgresHook`.

### INSERT simple — non-idempotent

```python
# ❌ NON IDEMPOTENT
def charger_donnees(**context):
    hook = PostgresHook('postgres_prod')
    hook.run("""
        INSERT INTO ventes (date, montant)
        SELECT date, montant FROM staging.ventes_temp
        WHERE date = %(d)s
    """, parameters={'d': context['ds']})
# Si exécuté 2 fois le même jour → doublons !
```

### DELETE + INSERT — idempotent

```python
# ✓ IDEMPOTENT
def charger_donnees(**context):
    hook = PostgresHook('postgres_prod')
    hook.run([
        "DELETE FROM ventes WHERE date = %(d)s",
        """
        INSERT INTO ventes (date, montant)
        SELECT date, montant FROM staging.ventes_temp
        WHERE date = %(d)s
        """
    ], parameters={'d': context['ds']})
# Peut être exécuté N fois → résultat identique
```

### INSERT ON CONFLICT — idempotent

```python
# ✓ IDEMPOTENT via UPSERT
def charger_donnees(**context):
    hook = PostgresHook('postgres_prod')
    hook.run("""
        INSERT INTO ventes_journalieres (date, produit_id, total)
        SELECT
            date,
            produit_id,
            SUM(montant) as total
        FROM staging.ventes
        WHERE date = %(d)s
        GROUP BY date, produit_id
        ON CONFLICT (date, produit_id)
        DO UPDATE SET
            total = EXCLUDED.total,
            updated_at = NOW()
    """, parameters={'d': context['ds']})
```

### Fichiers — idempotent

```python
# ❌ NON IDEMPOTENT — append à un fichier existant
def exporter():
    with open('/tmp/output.csv', 'a') as f:  # mode 'a' = append
        f.write(nouvelles_donnees)

# ✓ IDEMPOTENT — écrire avec date dans le nom
def exporter(**context):
    chemin = f'/tmp/output_{context["ds_nodash"]}.csv'
    with open(chemin, 'w') as f:  # mode 'w' = overwrite
        f.write(nouvelles_donnees)

# ✓ IDEMPOTENT — écrire dans un répertoire partitionné
def exporter(**context):
    date = context['ds']
    chemin = f'/data/ventes/date={date}/data.parquet'
    df.to_parquet(chemin)  # Écrase si existe
```

---

## Quelle période traiter ? Date logique et intervalle de données

Une tâche idempotente traite toujours **la même tranche de données** pour un run donné. Cette tranche doit donc être déduite du run (sa date logique, son intervalle de données), jamais de l'horloge (`datetime.now()`).

> **Changement important en Airflow 3.** Avec une expression cron ou un préréglage (`@daily`, `@monthly`...), Airflow 3 utilise par défaut `CronTriggerTimetable` : la date logique est **l'instant du déclenchement**, et `data_interval_start == data_interval_end == logical_date`. En Airflow 2, le même `@daily` donnait un intervalle d'un jour, et le run déclenché le 10 janvier à minuit portait la date logique du 9 janvier. Un code qui traite « la période `[data_interval_start, data_interval_end)` » doit donc être adapté, sinon il traite une période vide.

| Run planifié déclenché le 2024-01-10 à 00:00 UTC | `logical_date` / `ds` | `data_interval_start` | `data_interval_end` |
|---|---|---|---|
| `schedule='@daily'` (Airflow 3, `CronTriggerTimetable`) | 2024-01-10 | 2024-01-10 00:00 | 2024-01-10 00:00 |
| `schedule=CronDataIntervalTimetable("0 0 * * *", timezone="UTC")` | 2024-01-09 | 2024-01-09 00:00 | 2024-01-10 00:00 |

Deux façons correctes de traiter « les données de la veille » :

```python
from datetime import datetime
from airflow.sdk import dag, task
from airflow.timetables.interval import CronDataIntervalTimetable


# Option A — intervalle de données explicite (sémantique d'Airflow 2)
@dag(
    dag_id='ventes_intervalle',
    start_date=datetime(2024, 1, 1),
    schedule=CronDataIntervalTimetable("0 0 * * *", timezone="UTC"),
    catchup=False,
)
def ventes_intervalle():

    @task
    def charger(data_interval_start=None, data_interval_end=None):
        # Run déclenché le 2024-01-10 à 00:00 → [2024-01-09 00:00, 2024-01-10 00:00)
        print(f"Période traitée : [{data_interval_start}, {data_interval_end})")

    charger()


# Option B — @daily (CronTriggerTimetable) : la période se calcule depuis logical_date
@dag(
    dag_id='ventes_declenchement',
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    catchup=False,
)
def ventes_declenchement():

    @task
    def charger(logical_date=None):
        fin = logical_date                       # 2024-01-10 00:00
        debut = logical_date.subtract(days=1)    # 2024-01-09 00:00
        print(f"Période traitée : [{debut}, {fin})")

    charger()


ventes_intervalle()
ventes_declenchement()
```

Dans les deux cas, rejouer le run redonne exactement la même période : c'est ce qui rend le `DELETE + INSERT` ou l'UPSERT sûrs.

> Les variables `execution_date`, `prev_execution_date`, `next_execution_date`, `yesterday_ds` et `tomorrow_ds`, fréquentes dans les tutoriels Airflow 2, n'existent plus : utiliser `logical_date`, `ds`, `data_interval_start` et `data_interval_end`. L'option de configuration `[scheduler] create_cron_data_intervals = True` rétablit l'ancien comportement pour toutes les expressions cron, mais le choix explicite de la timetable dans le DAG est plus lisible.

---

## Idempotence dans les pipelines complets

Le pipeline ci-dessous utilise `CronDataIntervalTimetable` : pour un run planifié ou un backfill, `ds` désigne le **jour couvert par l'intervalle de données** (le run déclenché le 10 janvier à minuit traite la journée du 9).

```python
# dags/pipeline_idempotent.py

from datetime import datetime, timedelta
from airflow.sdk import dag, task
from airflow.timetables.interval import CronDataIntervalTimetable

@dag(
    dag_id='pipeline_etl_idempotent',
    start_date=datetime(2024, 1, 1),
    schedule=CronDataIntervalTimetable("0 0 * * *", timezone="UTC"),
    catchup=True,      # Peut rattraper les dates passées en toute sécurité
    default_args={'retries': 3, 'retry_delay': timedelta(minutes=5)},
    tags=['idempotent', 'bonnes-pratiques'],
)
def pipeline_etl_idempotent():

    @task
    def extraire(**context) -> str:
        """
        IDEMPOTENT : utilise la date logique dans le nom du fichier.
        Re-exécuter écrase le fichier précédent.
        """
        import json, os
        date = context['ds']

        # Simulation d'une extraction API
        donnees = [
            {'date': date, 'id': i, 'valeur': i * 42.0}
            for i in range(100)
        ]

        # Chemin unique par date — écrase si existe déjà
        chemin = f'/tmp/extract_{context["ds_nodash"]}.json'
        with open(chemin, 'w') as f:  # 'w' = overwrite, pas append
            json.dump(donnees, f)

        print(f"Extrait et sauvegardé : {chemin}")
        return chemin

    @task
    def transformer(chemin_source: str, **context) -> str:
        """
        IDEMPOTENT : écrase le fichier de sortie si existe.
        """
        import json, os

        with open(chemin_source) as f:
            donnees = json.load(f)

        transformees = [
            {**d, 'valeur_normalisee': d['valeur'] / 100.0}
            for d in donnees
        ]

        chemin_dest = f'/tmp/transform_{context["ds_nodash"]}.json'
        with open(chemin_dest, 'w') as f:
            json.dump(transformees, f)

        return chemin_dest

    @task
    def charger_en_db(chemin: str, **context) -> int:
        """
        IDEMPOTENT via UPSERT : ON CONFLICT DO UPDATE
        ou DELETE + INSERT selon la base de données.
        """
        import json
        from airflow.providers.postgres.hooks.postgres import PostgresHook

        with open(chemin) as f:
            donnees = json.load(f)

        hook = PostgresHook('postgres_prod')
        date = context['ds']

        # Pattern DELETE + INSERT (idempotent)
        hook.run(
            "DELETE FROM resultats_journaliers WHERE date_traitement = %(d)s",
            parameters={'d': date},
        )

        rows = [(d['date'], d['id'], d['valeur'], d['valeur_normalisee']) for d in donnees]
        hook.insert_rows(
            table='resultats_journaliers',
            rows=rows,
            target_fields=['date_traitement', 'id', 'valeur', 'valeur_normalisee'],
        )

        print(f"Chargé {len(rows)} lignes pour le {date}")
        return len(rows)

    @task
    def exporter_s3(chemin: str, **context) -> str:
        """
        IDEMPOTENT : upload S3 avec replace=True
        """
        from airflow.providers.amazon.aws.hooks.s3 import S3Hook

        hook = S3Hook('aws_prod')
        date = context['ds']
        cle_s3 = f'resultats/date={date}/data.json'

        # replace=True → écrase si existe
        hook.load_file(
            filename=chemin,
            key=cle_s3,
            bucket_name='mon-data-lake',
            replace=True,   # ← Idempotent
        )

        print(f"Exporté vers s3://mon-data-lake/{cle_s3}")
        return cle_s3

    @task
    def nettoyer_temp(**context) -> None:
        """Nettoyage des fichiers temporaires."""
        import os
        date_nodash = context['ds_nodash']
        for f in [f'/tmp/extract_{date_nodash}.json', f'/tmp/transform_{date_nodash}.json']:
            if os.path.exists(f):
                os.remove(f)
                print(f"Supprimé : {f}")

    # Orchestration
    chemin_extract = extraire()
    chemin_transform = transformer(chemin_extract)
    nb_charges = charger_en_db(chemin_transform)
    cle_s3 = exporter_s3(chemin_transform)
    nettoyer_temp()

dag = pipeline_etl_idempotent()
```

---

## Le paramètre catchup

> **Changement en Airflow 3 :** `catchup` vaut désormais `False` par défaut (c'était `True` en Airflow 2). Un nouveau DAG ne rattrape donc plus son historique, sauf si on le demande explicitement.

```python
from datetime import datetime
from airflow.sdk import DAG

# catchup=False (comportement par défaut en Airflow 3)
# Airflow ne crée que le run le plus récent, pas les échéances manquées.
with DAG(
    dag_id='sans_catchup',
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    catchup=False,   # Valeur par défaut, écrite ici pour être explicite
) as dag:
    pass

# catchup=True : Airflow crée un DAG Run pour CHAQUE échéance manquée
# entre start_date et maintenant.
#
# Exemple :
# start_date = 2024-01-01
# schedule = @daily
# Aujourd'hui = 2024-01-10 (dans la matinée)
# → Airflow crée 10 DAG Runs (dates logiques 2024-01-01 à 2024-01-10)
#   (9 runs, du 01 au 09, avec CronDataIntervalTimetable ou en Airflow 2)
with DAG(
    dag_id='avec_catchup',
    start_date=datetime(2024, 1, 1),
    schedule='@daily',
    catchup=True,   # Rattraper les dates manquées
    max_active_runs=3,  # Maximum 3 DAG Runs simultanés pendant le catchup
) as dag:
    pass
```

### Configuration globale du catchup

```ini
# airflow.cfg — valeur par défaut de catchup pour tous les DAGs
# (False en Airflow 3 ; passer à True pour retrouver le comportement d'Airflow 2)
[scheduler]
catchup_by_default = False
```

---

## Backfill manuel

Le backfill permet de re-exécuter un DAG sur des dates passées, même si `catchup=False`.

> La commande `airflow dags backfill` d'Airflow 2 n'existe plus. En Airflow 3, un backfill est un objet créé par `airflow backfill create` (ou depuis l'interface) puis **exécuté par le Scheduler** : la commande rend la main immédiatement, et le suivi se fait dans l'interface.

```bash
# Rejouer le DAG 'etl_ventes' pour janvier 2024 (bornes incluses)
airflow backfill create \
    --dag-id etl_ventes \
    --from-date 2024-01-01 \
    --to-date 2024-01-31

# Avec parallélisme (3 DAG Runs simultanés max)
airflow backfill create \
    --dag-id etl_ventes \
    --from-date 2024-01-01 \
    --to-date 2024-01-31 \
    --max-active-runs 3

# Simuler sans exécuter (dry run)
airflow backfill create \
    --dag-id etl_ventes \
    --from-date 2024-01-01 \
    --to-date 2024-01-31 \
    --dry-run

# Rejouer aussi les dates qui ont déjà un run
# (none par défaut : seules les dates sans run sont créées ; failed ; completed)
airflow backfill create \
    --dag-id etl_ventes \
    --from-date 2024-01-01 \
    --to-date 2024-01-31 \
    --reprocess-behavior completed
```

Depuis l'interface : sur la page du DAG, bouton **Trigger** puis option **Backfill** — on choisit la plage de dates, le comportement de retraitement (*Missing Runs*, *Missing and Errored Runs*, *All Runs*) et le nombre maximal de runs actifs. L'onglet **Backfills** du DAG liste les backfills, que l'on peut mettre en pause ou annuler.

> Un backfill n'est sûr que si vos tâches sont **idempotentes**. Sans ça, vous dupliquerez les données.

---

## Gestion des re-exécutions dans l'interface

### Clear d'une tâche

1. Cliquer sur la tâche dans la grille ou dans la vue Graph
2. Cliquer "Clear Task Instance" → la tâche est remise à zéro (plus d'état)
3. Le Scheduler la replanifie automatiquement

### Clear d'un DAG Run entier

1. Ouvrir le DAG Run et cliquer sur le bouton "Clear Dag Run"
2. Choisir "Clear existing tasks" (toutes les tâches du run sont rejouées) ou "Clear only failed tasks" (seulement celles en échec)

### Options de Clear d'une tâche

```
☐ Past        → Clear aussi cette tâche dans les runs précédents
☐ Future      → Clear aussi cette tâche dans les runs suivants
☐ Upstream    → Clear aussi les tâches en amont
☒ Downstream  → Clear aussi les tâches en aval (recommandé)
☐ Clear only failed tasks → Limiter aux tâches en échec
```

La boîte de dialogue affiche la liste des tâches concernées (*Affected Tasks*) avant confirmation. L'option "Include itself" d'Airflow 2 a disparu : la tâche sélectionnée est toujours incluse.

---

> 🔴 **ACTION FORMATEUR — CAPTURE REQUISE**
> **Capturer :** L'interface Airflow 3 — dialogue de confirmation "Clear Task Instance" d'une tâche, avec les options (Past, Future, Upstream, Downstream, Clear only failed tasks) et la liste des tâches concernées
> **Expliquer :** Expliquer chaque option. Cas typique : une tâche a échoué et toutes les tâches en aval ont `upstream_failed`. Cocher "Downstream" pour les rejouer toutes en chaîne. Montrer comment le DAG Run repasse de "failed" à "running" après un Clear.

---

## Checklist d'idempotence

Pour vérifier qu'une tâche est idempotente, poser ces questions :

```
□ Si j'exécute cette tâche 2 fois → même résultat qu'une fois ?
□ Mes INSERT utilisent ON CONFLICT DO UPDATE ou DELETE+INSERT ?
□ Mes fichiers de sortie sont en mode write (écrase), pas append ?
□ Je filtre sur la date logique (ds) ou l'intervalle de données dans mes requêtes SQL ?
□ La période traitée est déduite du run, jamais de datetime.now() ?
□ Mes uploads cloud utilisent replace=True ?
□ Je partitionne mes fichiers par date ? (/date=YYYY-MM-DD/)
□ Je supprime les données du jour AVANT de les recréer ?
```

---

## max_active_runs — limiter les runs simultanés

```python
from datetime import datetime
from airflow.sdk import DAG

with DAG(
    dag_id='pipeline_lent',
    start_date=datetime(2024, 1, 1),
    schedule='@hourly',
    catchup=True,
    max_active_runs=1,  # Un seul run à la fois (évite les conflits DB)
) as dag:
    pass
```

```python
# Configurer au niveau global dans airflow.cfg
# [core]
# max_active_runs_per_dag = 16
```

---

## Points clés à retenir

1. **Idempotence** = re-exécuter N fois → même résultat qu'une seule fois
2. Utiliser `DELETE WHERE date = ...` + `INSERT` ou `INSERT ON CONFLICT DO UPDATE`
3. Utiliser la date logique (`ds`, `ds_nodash`) dans les noms de fichiers et les filtres SQL
4. En Airflow 3, `@daily` déclenche **à** la date logique (intervalle de données vide) : utiliser `CronDataIntervalTimetable` ou calculer la période depuis `logical_date`
5. `catchup=False` est le défaut en Airflow 3 ; ne passer à `True` que si le rattrapage a du sens métier
6. Le **backfill** (`airflow backfill create` ou interface) est sûr uniquement avec des tâches idempotentes
7. `max_active_runs=1` pour les pipelines qui ne peuvent pas tourner en parallèle
