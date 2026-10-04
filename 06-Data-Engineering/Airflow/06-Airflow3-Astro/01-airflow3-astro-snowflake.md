# Airflow 3 avec Astro CLI : Snowflake, SQL, dbt et notifications

Les modules 1 à 5 de cette formation présentent Airflow 3 avec Docker Compose. Ce chapitre montre la même chose avec Astro CLI, récapitule ce qui change par rapport à Airflow 2 (la plupart des tutoriels en ligne), et ajoute ce qui manque pour orchestrer un entrepôt Snowflake et un projet dbt : connexion par paire de clés, date logique et reprise d'historique, Cosmos, notifications.

Versions avec lesquelles le chapitre a été vérifié (octobre 2026) : Astro CLI 1.46, Astro Runtime 3.3 (Airflow 3.3.2), provider Snowflake 6.x, Astronomer Cosmos 1.15, dbt 1.12. La section 9 (notifications) n'a pas été exécutée : elle est signalée comme telle.

Exemple suivi : un fichier de ventes publié chaque mois (`ventes_2025-01.csv`, `ventes_2025-02.csv`...) à charger dans `SALES_DB.RAW_DATA.VENTES`, puis un projet dbt à exécuter. L'entrepôt, le rôle `SALES_ENGINEER` et l'utilisateur de service `SALES_ETL_SVC` sont ceux du chapitre [Sécurité Snowflake](../../../04-Cloud-Platforms/snowflake/10-securite.md). L'adresse de téléchargement est fictive : l'exemple se lit et se transpose, il ne se lance pas tel quel.

---

## 1. Ce qui change entre Airflow 2 et Airflow 3

La plupart des tutoriels et des vidéos disponibles sont en Airflow 2. Le raisonnement reste valable, mais le code ne se copie pas tel quel.

| Sujet | Airflow 2 (tutoriels anciens) | Airflow 3 |
|---|---|---|
| Import des décorateurs | `from airflow.decorators import dag, task` | `from airflow.sdk import dag, task` |
| Classe DAG | `from airflow import DAG` | `from airflow.sdk import DAG` |
| Contexte d'exécution | `from airflow.operators.python import get_current_context` | `from airflow.sdk import get_current_context` |
| Opérateurs Python et Bash | `airflow.operators.python`, `airflow.operators.bash` | `airflow.providers.standard.operators.python`, `airflow.providers.standard.operators.bash` |
| Planification | `schedule_interval="@monthly"` | `schedule="@monthly"` (l'ancien nom n'existe plus) |
| Date du run | `execution_date` | `logical_date` (`execution_date` n'existe plus) |
| Reprise d'historique | `catchup=True` par défaut | `catchup=False` par défaut : l'écrire explicitement |
| Variables | `from airflow.models import Variable` | `from airflow.sdk import Variable` |
| Interface web | conteneur `webserver` | conteneur `api-server` |
| Accès à la base interne d'Airflow depuis une tâche | possible | interdit : une tâche passe par l'API d'exécution |

Réflexe : devant un exemple trouvé en ligne, regarder d'abord les imports. `airflow.decorators` ou `schedule_interval` signalent de l'Airflow 2.

---

## 2. Un projet Airflow avec Astro CLI

Astro CLI remplace le fichier Docker Compose du module 1 : il génère le projet et lance les conteneurs.

```bash
mkdir ventes-airflow && cd ventes-airflow
astro dev init        # génère Dockerfile, dags/, include/, requirements.txt, .env
astro dev start       # construit l'image et démarre Airflow sur http://localhost:8080
```

| Fichier ou dossier | Rôle |
|---|---|
| `Dockerfile` | image de base (`FROM astrocrpublic.azurecr.io/runtime:3.x-y`) et ajouts système |
| `requirements.txt` | paquets Python installés dans l'image (providers, Cosmos) |
| `dags/` | les DAG, rechargés à chaud |
| `include/` | fichiers utilisés par les DAG (SQL, scripts) |
| `.env` | variables d'environnement des conteneurs en local ; jamais dans Git |

Commandes du quotidien :

| Commande | Effet |
|---|---|
| `astro dev start` / `astro dev stop` | démarrer / arrêter en conservant l'historique |
| `astro dev restart` | reconstruire l'image après une modification de `Dockerfile` ou `requirements.txt` |
| `astro dev kill` | tout supprimer, historique compris |
| `astro dev run dags list` | lister les DAG vus par Airflow |
| `astro dev run dags list-import-errors` | afficher les erreurs d'import |
| `astro dev run dags unpause <dag_id>` | activer un DAG (il est en pause à sa création) |
| `astro dev run dags list-runs <dag_id>` | état des exécutions d'un DAG |
| `astro dev run connections get <conn_id>` | vérifier qu'une connexion est bien définie |

`astro dev start` lance cinq conteneurs : `postgres` (base interne), `scheduler`, `dag-processor` (lit les fichiers de DAG), `api-server` (interface web et API) et `triggerer`.

À savoir : un nouveau DAG est en pause à sa création. Il faut l'activer, avec l'interrupteur de la liste des DAG ou avec `astro dev run dags unpause <dag_id>`. S'il a une date de début passée et `catchup=True`, les exécutions de rattrapage démarrent dès l'activation.

Ne pas confondre activer et déclencher : le bouton **Trigger** lance une exécution manuelle datée du moment présent. Pour un DAG qui déduit son fichier de la date du run, elle cherchera le fichier du mois en cours, qui n'existe pas encore.

---

## 3. Donner à Airflow l'accès à Snowflake sans secret dans le code

### 3.1 Le provider

Dans `requirements.txt` :

```
apache-airflow-providers-snowflake>=6.0
```

### 3.2 La connexion par variable d'environnement

Airflow crée une connexion pour toute variable d'environnement nommée `AIRFLOW_CONN_<IDENTIFIANT EN MAJUSCULES>`. La valeur est un JSON. Pour un utilisateur de service authentifié par paire de clés, la clé privée va dans l'extra `private_key_content`, sur une seule ligne.

Fabriquer la ligne (les retours à la ligne deviennent les deux caractères `\n`) :

```bash
PEM_ONE_LINE=$(awk 'NF {printf "%s\\n", $0}' ~/.ssh/snowflake/rsa_key.p8)
```

Fichier `.env` :

```
AIRFLOW_CONN_SNOWFLAKE_SALES='{"conn_type":"snowflake","login":"SALES_ETL_SVC","schema":"RAW_DATA","extra":{"account":"ORGANISATION-COMPTE","warehouse":"SALES_WH","database":"SALES_DB","role":"SALES_ENGINEER","private_key_content":"-----BEGIN PRIVATE KEY-----\nMIIEv...\n-----END PRIVATE KEY-----\n"}}'
```

L'identifiant de connexion à utiliser dans le code est `snowflake_sales`.

Trois règles :
- `.env` est listé dans `.gitignore` et dans `.dockerignore` : la clé n'entre ni dans Git ni dans l'image.
- Aucun fichier de clé n'est copié dans le projet.
- Une connexion définie par variable d'environnement n'apparaît pas toujours dans la page Connections de l'interface. La vérifier avec `astro dev run connections get snowflake_sales`.

### 3.3 Exécuter du SQL depuis une tâche

```python
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook

hook = SnowflakeHook(snowflake_conn_id="snowflake_sales")
lignes = hook.run("SELECT COUNT(*) FROM SALES_DB.RAW_DATA.VENTES", handler=lambda cur: cur.fetchall())
```

`hook.run` accepte aussi `PUT` (envoi d'un fichier du conteneur vers un stage) et `COPY INTO`.

### 3.4 Prouver que la connexion fonctionne avant d'aller plus loin

La mise en forme de la clé dans `.env` est l'étape la plus fragile. On la valide avec le plus petit DAG possible, avant d'écrire le vrai :

```python
import pendulum
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.sdk import dag, task


@dag(schedule=None, start_date=pendulum.datetime(2025, 1, 1, tz="UTC"), catchup=False)
def test_connexion():
    @task
    def qui_suis_je():
        ligne = SnowflakeHook(snowflake_conn_id="snowflake_sales").get_first(
            "SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE()"
        )
        print(ligne)

    qui_suis_je()


test_connexion()
```

Ce DAG n'a pas de planification (`schedule=None`) : c'est le seul cas où on le lance avec le bouton Trigger. Le log de la tâche doit afficher l'utilisateur de service, son rôle et son warehouse. Après toute modification de `.env`, relancer `astro dev restart` : le fichier n'est lu qu'au démarrage.

---

## 4. La date logique : traiter un mois, pas « aujourd'hui »

Chaque exécution d'un DAG planifié porte une **date logique** : la date de la période qu'elle traite. Elle ne change pas si on relance l'exécution six mois plus tard.

```python
from airflow.sdk import get_current_context

ctx = get_current_context()
mois = ctx["data_interval_start"].strftime("%Y-%m")     # "2025-01" pour le run du 1er janvier 2025
fichier = f"ventes_{mois}.csv"
```

Avec la planification par défaut d'Airflow 3, `data_interval_start` et `logical_date` sont la même date : celle du déclenchement prévu.

À ne jamais faire : `datetime.now()` ou `pendulum.today()` pour choisir le fichier. Le run de janvier relancé en octobre chercherait le fichier d'octobre, et l'historique ne pourrait pas être rejoué.

### Rejouer l'historique

```python
@dag(
    schedule="@monthly",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    end_date=pendulum.datetime(2025, 3, 1, tz="UTC"),
    catchup=True,          # crée un run par mois entre start_date et end_date
    max_active_runs=1,     # un mois à la fois, dans l'ordre
)
```

Airflow crée trois exécutions (1er janvier, 1er février, 1er mars 2025) et les enchaîne. Le chapitre [Idempotence](../04-Bonnes-Pratiques/01-idempotence.md) explique pourquoi chaque tâche doit pouvoir être rejouée sans effet de bord.

---

## 5. Un DAG de chargement complet

```python
"""Chargement mensuel des ventes : téléchargement → stage Snowflake → table RAW."""
from pathlib import Path

import pendulum
import requests
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
from airflow.sdk import dag, task, get_current_context

BASE_URL = "https://exemple.org/ventes"          # adresse fictive
STAGE = "SALES_DB.RAW_DATA.VENTES_STAGE"
CONN_ID = "snowflake_sales"


@dag(
    dag_id="ventes_mensuelles",
    schedule="@monthly",
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    end_date=pendulum.datetime(2025, 3, 1, tz="UTC"),
    catchup=True,
    max_active_runs=1,
    default_args={"retries": 2, "retry_delay": pendulum.duration(minutes=5)},
)
def ventes_mensuelles():

    @task
    def nom_du_fichier() -> str:
        ctx = get_current_context()
        return f"ventes_{ctx['data_interval_start'].strftime('%Y-%m')}.csv"

    @task
    def verifier_disponibilite(fichier: str) -> str:
        url = f"{BASE_URL}/{fichier}"
        requests.head(url, timeout=30).raise_for_status()   # échoue si le mois n'est pas publié
        return url

    @task
    def telecharger_et_deposer(url: str) -> str:
        destination = Path("/tmp") / url.rsplit("/", 1)[-1]
        try:
            with requests.get(url, stream=True, timeout=120) as reponse:
                reponse.raise_for_status()
                with destination.open("wb") as f:
                    for bloc in reponse.iter_content(chunk_size=8 * 1024 * 1024):
                        f.write(bloc)
            SnowflakeHook(snowflake_conn_id=CONN_ID).run(
                f"PUT file://{destination} @{STAGE} AUTO_COMPRESS=FALSE OVERWRITE=FALSE"
            )
        finally:
            destination.unlink(missing_ok=True)
        return destination.name

    @task
    def copier_dans_la_table(fichier: str) -> None:
        SnowflakeHook(snowflake_conn_id=CONN_ID).run(
            f"""
            COPY INTO SALES_DB.RAW_DATA.VENTES
            FROM @{STAGE}
            FILES = ('{fichier}')
            ON_ERROR = ABORT_STATEMENT
            """
        )

    copier_dans_la_table(telecharger_et_deposer(verifier_disponibilite(nom_du_fichier())))


ventes_mensuelles()
```

Choix à comprendre :

- **Téléchargement et `PUT` dans la même tâche.** Sur un Airflow à plusieurs machines, deux tâches peuvent s'exécuter sur deux machines différentes, qui ne partagent pas `/tmp`.
- **Suppression du fichier dans un `finally`.** Le disque du conteneur est limité.
- **Entre tâches, on ne passe que de petites valeurs** (un nom de fichier, une adresse), jamais le fichier lui-même. Voir le chapitre [XCom](../03-Concepts-Avances/01-xcom.md).
- **`retries`.** Un fichier pas encore publié ou une coupure réseau se règle souvent en réessayant.
- **`COPY INTO` sans `FORCE`.** Snowflake ne recharge pas un fichier déjà chargé : relancer le run n'ajoute aucune ligne.
- **Le `COPY INTO` de cet exemple est réduit au minimum.** Dans un vrai projet, il porte les options vues dans le chapitre [Charger des fichiers](../../../04-Cloud-Platforms/snowflake/11-chargement-stage-copy.md) : format de fichier, correspondance des colonnes par nom, colonnes techniques.

---

## 6. Exécuter des fichiers SQL et contrôler les données

Quand les transformations sont écrites en SQL, Airflow sert à les lancer dans le bon ordre, pour le bon mois, et à arrêter la chaîne si les données sont mauvaises.

### 6.1 Ranger le SQL dans des fichiers

Le SQL vit dans `include/sql/`, pas dans le code Python du DAG : le DAG décide de l'ordre, les fichiers décident du contenu.

```
include/sql/
├── staging/stg_ventes.sql
├── marts/ventes_par_jour.sql
└── controles/ventes_non_vides.sql
```

Dans `requirements.txt` : `apache-airflow-providers-common-sql` (installé aussi par le provider Snowflake).

```python
from airflow.providers.common.sql.operators.sql import SQLCheckOperator, SQLExecuteQueryOperator
from airflow.sdk import TaskGroup, dag

@dag(
    ...,
    template_searchpath="/usr/local/airflow/include/sql",   # dossier où chercher les fichiers .sql
    params={"seuil_montant_max": 10000},                     # valeurs réutilisables dans le SQL
)
def ventes_mensuelles():
    staging = SQLExecuteQueryOperator(
        task_id="stg_ventes",
        conn_id="snowflake_sales",
        sql="staging/stg_ventes.sql",        # chemin relatif à template_searchpath
        split_statements=True,               # le fichier peut contenir plusieurs instructions
    )
```

Une tâche = un fichier. Si la tâche échoue, on sait quel fichier relire, et on la relance seule.

### 6.2 Paramétrer le SQL par le mois traité

Avant d'exécuter un fichier `.sql`, Airflow remplace ce qui est entre doubles accolades :

| Dans le fichier SQL | Remplacé par | Exemple pour le run du 1er janvier 2025 |
|---|---|---|
| `{{ ds }}` | la date logique du run, au format `AAAA-MM-JJ` | `2025-01-01` |
| `{{ logical_date.strftime("%Y-%m") }}` | la date logique dans le format voulu | `2025-01` |
| `{{ params.seuil_montant_max }}` | un paramètre du DAG | `10000` |

Fichier `marts/ventes_par_jour.sql`, rejouable mois par mois :

```sql
-- On efface le mois traité, puis on le réinsère : relancer le run ne crée aucun doublon
-- et ne touche pas aux autres mois.
DELETE FROM SALES_DB.ANALYTICS.VENTES_PAR_JOUR
WHERE mois = '{{ ds }}'::date;

INSERT INTO SALES_DB.ANALYTICS.VENTES_PAR_JOUR
SELECT DATE_TRUNC('month', date_vente) AS mois, date_vente, SUM(montant) AS total
FROM SALES_DB.RAW_DATA.VENTES
WHERE DATE_TRUNC('month', date_vente) = '{{ ds }}'::date
  AND montant <= {{ params.seuil_montant_max }}
GROUP BY 1, 2;
```

Trois façons d'écrire une table, à choisir selon le cas :

| Écriture | Quand | Rejouable ? |
|---|---|---|
| `CREATE OR REPLACE VIEW ... AS SELECT` | simple renommage ou typage, rien n'est stocké | oui |
| `CREATE OR REPLACE TABLE ... AS SELECT` | petite table recalculée en entier à chaque run (dimension, agrégat) | oui |
| `DELETE` du mois puis `INSERT` | grosse table alimentée mois par mois | oui, si le `DELETE` et l'`INSERT` filtrent sur le même mois |

Un `INSERT` seul, sans `DELETE`, ajoute les lignes une seconde fois à chaque relance.

Pour vérifier ce qu'Airflow a réellement envoyé à Snowflake : onglet **Rendered Templates** de la tâche dans l'interface.

### 6.3 Contrôler les données avec une tâche

`SQLCheckOperator` exécute une requête qui renvoie **une ligne**. Si une des valeurs de cette ligne est fausse (ou vaut 0 ou vide), la tâche échoue et les tâches suivantes ne s'exécutent pas.

Fichier `controles/ventes_non_vides.sql` :

```sql
SELECT
    COUNT(*) > 0,                         -- le mois contient des lignes
    COUNT(*) = COUNT(DISTINCT id_vente)   -- aucun identifiant en double
FROM SALES_DB.RAW_DATA.VENTES
WHERE DATE_TRUNC('month', date_vente) = '{{ ds }}'::date;
```

```python
    controle = SQLCheckOperator(
        task_id="controle_ventes_non_vides",
        conn_id="snowflake_sales",
        sql="controles/ventes_non_vides.sql",
    )
```

Un contrôle peut aussi comparer une mesure à un seuil défini dans les paramètres du DAG :

```sql
-- Moins de 5 % de ventes sans client
SELECT COUNT_IF(id_client IS NULL) / COUNT(*) * 100 < {{ params.max_pct_sans_client }}
FROM SALES_DB.RAW_DATA.VENTES
WHERE DATE_TRUNC('month', date_vente) = '{{ ds }}'::date;
```

Un contrôle se place juste après la tâche qu'il vérifie et avant celles qui utilisent son résultat : une donnée fausse ne se propage pas.

Deux conseils pratiques :
- Mettre `retries=0` sur les contrôles. Relancer un contrôle ne change pas les données : avec des relances automatiques, la tâche resterait plusieurs minutes en attente (`up_for_retry`) avant d'échouer pour de bon.
- Pour voir un contrôle échouer, durcir temporairement son seuil (par exemple passer le paramètre à 0), relancer la tâche, constater que les suivantes passent à l'état `upstream_failed`, puis remettre le seuil.

### 6.4 Ordonner et regrouper

```python
    with TaskGroup("marts") as marts:
        dimensions = [
            SQLExecuteQueryOperator(task_id=nom, conn_id="snowflake_sales", sql=f"marts/{nom}.sql", split_statements=True)
            for nom in ("dim_client", "dim_produit")
        ]
        faits = SQLExecuteQueryOperator(task_id="fct_ventes", conn_id="snowflake_sales", sql="marts/fct_ventes.sql", split_statements=True)
        dimensions >> faits          # les deux dimensions en parallèle, puis les faits

    staging >> controle >> marts     # un groupe se chaîne comme une tâche
```

- `a >> b` : `b` attend que `a` ait réussi.
- `[a, b] >> c` : `c` attend `a` et `b`, qui s'exécutent en parallèle.
- `[a, b] >> [c, d]` n'existe pas : Python ne sait pas relier deux listes. On écrit une boucle, `for t in [a, b]: t >> [c, d]`, ce qui fait attendre `c` et `d` après `a` et `b`.
- Un `TaskGroup` rassemble des tâches sous un même cadre dans la vue Graph ; il se déplie d'un clic.

Pour trouver l'ordre : lire le `FROM` et les `JOIN` de chaque fichier. Une tâche doit passer après toutes celles qui créent les tables qu'elle lit.

---

## 7. Lancer un projet dbt depuis Airflow

### 7.1 Installer dbt dans l'image, à part

dbt et Airflow ont des dépendances Python incompatibles. On installe dbt dans un environnement virtuel dédié, à la suite de la ligne `FROM` du `Dockerfile` :

```dockerfile
RUN python -m venv dbt_venv && \
    . dbt_venv/bin/activate && \
    pip install --no-cache-dir "dbt-snowflake>=1.9,<2.0" && \
    deactivate

COPY dbt/ventes /usr/local/airflow/dbt/ventes
```

Le projet dbt est copié dans l'image sans `profiles.yml`, sans `target/` ni `dbt_packages/`.

### 7.2 Solution simple : une seule tâche

```python
from airflow.providers.standard.operators.bash import BashOperator

dbt_build = BashOperator(
    task_id="dbt_build",
    bash_command="/usr/local/airflow/dbt_venv/bin/dbt build --project-dir /usr/local/airflow/dbt/ventes",
)
```

Simple, mais le projet dbt est une boîte noire : un seul carré dans Airflow, et il faut alors fournir un `profiles.yml` et la clé au conteneur.

### 7.3 Solution détaillée : Astronomer Cosmos

Cosmos lit le projet dbt et crée une tâche Airflow par modèle, avec ses tests. Dans `requirements.txt` : `astronomer-cosmos>=1.11` (première version compatible Airflow 3).

```python
from pathlib import Path

from cosmos import DbtTaskGroup, ExecutionConfig, ProfileConfig, ProjectConfig, RenderConfig
from cosmos.constants import TestBehavior
from cosmos.profiles import SnowflakePrivateKeyPemProfileMapping

profil = ProfileConfig(
    profile_name="ventes",
    target_name="prod",
    profile_mapping=SnowflakePrivateKeyPemProfileMapping(
        conn_id="snowflake_sales",                       # la connexion Airflow de la section 3
        profile_args={"database": "SALES_DB", "schema": "ANALYTICS", "threads": 8},
    ),
)

# à l'intérieur de la fonction décorée par @dag
dbt = DbtTaskGroup(
    group_id="dbt",
    project_config=ProjectConfig(dbt_project_path=Path("/usr/local/airflow/dbt/ventes")),
    profile_config=profil,
    execution_config=ExecutionConfig(dbt_executable_path="/usr/local/airflow/dbt_venv/bin/dbt"),
    render_config=RenderConfig(test_behavior=TestBehavior.AFTER_EACH),
    operator_args={"install_deps": True},
)

copier_dans_la_table(...) >> dbt
```

Ce que cela apporte :

- Cosmos fabrique le profil dbt à partir de la connexion Airflow : il n'y a qu'un seul secret, et pas de `profiles.yml` dans l'image.
- Chaque modèle est une tâche : si un modèle échoue, on le relance seul.
- `TestBehavior.AFTER_EACH` lance les tests d'un modèle juste après lui, avant de construire les suivants.
- Le champ `schema` de la connexion est obligatoire pour ce profil.

---

## 8. Lire et diagnostiquer

Dans l'interface (http://localhost:8080) :

| Vue | Sert à |
|---|---|
| Liste des DAG | voir les erreurs d'import (bandeau rouge), activer ou mettre en pause |
| Grid | une colonne par exécution, une ligne par tâche : repérer d'un coup d'œil ce qui a échoué |
| Graph | l'enchaînement des tâches et des groupes |
| Logs d'une tâche | le message d'erreur exact ; toujours lire la fin du log |
| Clear sur une tâche | la relancer, ainsi que celles qui en dépendent |
| Clear sur une exécution entière | la rejouer du début. Indispensable après avoir ajouté des tâches à un DAG dont les exécutions sont déjà terminées : elles ne tournent pas d'elles-mêmes |

| Symptôme | Cause probable | Correction |
|---|---|---|
| Le DAG n'apparaît pas | erreur d'import | `astro dev run dags list-import-errors` |
| Avertissement de dépréciation ou erreur d'import sur `airflow.decorators`, erreur `unexpected keyword argument 'schedule_interval'` | code Airflow 2 | adapter avec le tableau de la section 1 |
| `ModuleNotFoundError: cosmos` | `requirements.txt` modifié sans reconstruire | `astro dev restart` |
| `dbt executable not found` | environnement virtuel dbt absent de l'image | vérifier le bloc `RUN python -m venv` du `Dockerfile`, puis `astro dev restart` |
| `JWT token is invalid` | clé privée mal mise sur une ligne, ou identifiant de compte erroné | régénérer avec la commande `awk` de la section 3.2 |
| `schema is required` (Cosmos) | champ `schema` absent du JSON de connexion | l'ajouter au niveau racine du JSON |
| Aucun run créé | `catchup` absent (faux par défaut en Airflow 3) ou DAG en pause | écrire `catchup=True`, activer le DAG |
| Erreur 403 ou 404 au téléchargement, sur un fichier daté du mois en cours | exécution lancée avec Trigger | supprimer cette exécution ; activer le DAG au lieu de le déclencher |
| Les tâches ajoutées au DAG ne s'exécutent pas | les exécutions existantes sont déjà terminées | Clear sur chaque exécution |
| Une tâche reste longtemps en `up_for_retry` | relances automatiques (`retries`) avec délai | attendre, ou `retries=0` sur cette tâche |
| `TypeError: unsupported operand type(s) for >>: 'list' and 'list'` | deux listes reliées par `>>` | boucle `for` (section 6.4) |
| La modification de `.env` n'est pas prise en compte | le fichier n'est lu qu'au démarrage | `astro dev restart` |
| `TemplateNotFound` | fichier SQL introuvable | le chemin donné à la tâche est relatif à `template_searchpath` |
| Un contrôle `SQLCheckOperator` échoue | une valeur de la ligne renvoyée est fausse | lire la requête dans Rendered Templates et l'exécuter dans Snowsight |
| `No such file` au moment du `PUT` | téléchargement et `PUT` dans deux tâches différentes | les regrouper |
| Port 8080 déjà utilisé | autre service local (par exemple `dbt docs serve`) | l'arrêter, ou changer le port dans la configuration d'Astro CLI (`astro config --help`) |

---

## 9. Être prévenu : notification en cas de succès ou d'échec

Cette section n'a pas été exécutée lors de la vérification du chapitre : la tester avant de s'appuyer dessus.

Un DAG accepte des fonctions de rappel, appelées par Airflow à la fin d'une exécution. Elles reçoivent le contexte de l'exécution.

```python
import os

import requests


def notifier(context):
    execution = context["dag_run"]
    message = f"{execution.dag_id} | {execution.run_id} | {execution.state}"
    requests.post(os.environ["DISCORD_WEBHOOK_URL"], json={"content": message}, timeout=10)


@dag(
    ...,
    on_success_callback=notifier,
    on_failure_callback=notifier,
)
```

- Un webhook Discord se crée dans les paramètres d'un salon (Intégrations → Webhooks). C'est une adresse qui accepte un message en JSON.
- L'adresse du webhook donne le droit d'écrire dans le salon : c'est un secret. Elle va dans `.env` (`DISCORD_WEBHOOK_URL=...`), pas dans le code.
- Les mêmes fonctions existent au niveau d'une tâche (`on_failure_callback` dans `default_args`) pour être prévenu dès la première tâche en échec.
- Pour tester l'échec : faire lever une exception à une tâche, ou demander un fichier qui n'existe pas.

Le chapitre [Opérateurs HTTP](../02-Operateurs/04-operateurs-http.md) détaille les appels de webhooks, et le chapitre [Production](../05-Deploiement/01-production.md) les fonctions de rappel.

---

## 10. Exercice d'application

Une association publie chaque mois un fichier `adhesions_AAAA-MM.csv`.

1. Créer un projet Astro et y déclarer une connexion Snowflake par variable d'environnement, avec un utilisateur de service et sa clé.
2. Écrire un DAG mensuel qui dérive le nom du fichier de la date du run, vérifie qu'il existe, le dépose sur un stage et le copie dans une table.
3. Ajouter un fichier SQL qui calcule le nombre d'adhésions par jour pour le mois traité, et un contrôle qui échoue si le mois est vide.
4. Régler le DAG pour qu'il rejoue les trois premiers mois de 2025, un par un.
5. Relancer le run de février : combien de lignes sont ajoutées, et pourquoi ?
6. Provoquer un échec et retrouver le message d'erreur dans les logs.

Questions : que se passerait-il si le nom du fichier était calculé avec la date du jour ? Pourquoi `max_active_runs=1` ? Où se trouve la clé privée quand le DAG tourne, et où ne se trouve-t-elle pas ?

## Points de vérification
- [ ] Imports en `airflow.sdk`, aucun `schedule_interval` ni `execution_date`
- [ ] Connexion Snowflake définie par variable d'environnement, vérifiée avec `astro dev run connections get`
- [ ] Nom du fichier dérivé de la date du run
- [ ] `catchup=True` écrit explicitement, trois exécutions réussies
- [ ] Relance d'un mois sans doublon
- [ ] Aucun secret dans Git ni dans l'image

## Documentation officielle
- [Astro CLI](https://www.astronomer.io/docs/astro/cli/install-cli)
- [TaskFlow (Airflow 3)](https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html)
- [Planification et catchup](https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/cron.html)
- [Connexion Snowflake du provider](https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/connections/snowflake.html)
- [Astronomer Cosmos](https://astronomer.github.io/astronomer-cosmos/)
- [Orchestrer dbt Core avec Cosmos](https://www.astronomer.io/docs/learn/airflow-dbt)
