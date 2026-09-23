# 01 — Lundi : architecture et premier DAG

> 🎬 **Le fil rouge.** Vous rejoignez l'équipe data d'un cabinet d'études urbaines qui suit
> l'activité des taxis new-yorkais. Jusqu'ici, un analyste télécharge chaque mois le fichier de la
> TLC, le charge à la main dans l'entrepôt et relance ses requêtes. Il part en congé trois semaines.
> Votre mission de la semaine : **qu'il n'ait plus jamais à le faire**.

| | |
|---|---|
| **Matin** | Pourquoi un orchestrateur · monter la stack · les cinq services |
| **Après-midi** | Premier DAG TaskFlow · vues Grid et Graph · logs · DAG cassé |
| **À la fin de la journée** | la stack tourne, vous savez dire à quoi sert chaque conteneur, votre premier DAG a réussi |

---

## Objectifs

1. Installer Airflow 3 en local avec Docker Compose et vérifier qu'il est en bonne santé.
2. Expliquer le rôle de chaque service, et ce qui casse quand l'un d'eux s'arrête.
3. Écrire un DAG avec l'API TaskFlow (`from airflow.sdk import dag, task`).
4. Lire une exécution : vue Grid, vue Graph, logs, XCom.
5. Diagnostiquer un DAG qui n'apparaît pas.

---

## 1. Le vocabulaire minimum

| Mot | Ce que c'est |
|---|---|
| **DAG** | *Directed Acyclic Graph*. Un pipeline : des tâches reliées par des dépendances, sans boucle. C'est un fichier Python dans `dags/`. |
| **Tâche** (*task*) | une étape du pipeline : télécharger, charger, calculer. |
| **Opérateur** | le modèle d'une tâche : `PythonOperator`, `SQLExecuteQueryOperator`… Avec TaskFlow, une fonction décorée par `@task` devient une tâche. |
| **Exécution** (*DAG run*) | une instance du DAG, lancée par le planning ou à la main. |
| **Instance de tâche** (*task instance*) | une tâche dans une exécution donnée, avec son état : `queued`, `running`, `success`, `failed`, `up_for_retry`, `deferred`, `skipped`… |
| **XCom** | petit message qu'une tâche transmet à une autre (quelques Ko, jamais un fichier de données). |

> 📌 **Airflow orchestre, il ne transforme pas.** Airflow décide *quand* et *dans quel ordre*
> lancer les étapes, et garde la trace de ce qui s'est passé. Le travail lourd (charger 3,5 millions
> de lignes, calculer des agrégats) est fait par Snowflake. Une tâche Airflow qui manipule des
> gigaoctets en mémoire est presque toujours une erreur de conception.

---

## 2. Monter la stack

### Avant de commencer

| Vérification | Commande | Attendu |
|---|---|---|
| Docker Compose v2 | `docker compose version` | v2.x (la commande `docker-compose` avec un tiret est l'ancienne, à ne plus utiliser) |
| Mémoire allouée à Docker | Docker Desktop › Settings › Resources | **4 Go minimum**, 8 Go conseillés |
| Port 8080 libre | `lsof -i :8080` (Mac/Linux) | aucune sortie |

> ⚠️ **Windows** : travaillez dans WSL2, et placez l'atelier **dans le système de fichiers Linux**
> (`~/formation/...`), pas dans `/mnt/c/...`. Sinon tout est lent et les fichiers de DAG ne sont
> pas toujours détectés.

### Démarrer

```bash
cd 06-Data-Engineering/Airflow/atelier
cp .env.example .env                 # Linux : remplacer AIRFLOW_UID=50000 par le résultat de `id -u`

docker compose build                 # construit l'image (1re fois : 1 à 2 min)
docker compose up airflow-init       # crée la base de métadonnées et le compte admin, puis s'arrête
docker compose up -d                 # démarre la stack en arrière-plan
docker compose ps                    # tous les services doivent finir en "healthy"
```

Ouvrez http://localhost:8080 et connectez-vous avec `airflow` / `airflow`.

> 💡 **Le port 8080 est déjà pris ?** Mettez `AIRFLOW_PORT=8088` dans `.env`, relancez
> `docker compose up -d`, et ouvrez http://localhost:8088. C'est ce que le fichier `.env` sert à
> faire : adapter la stack à votre machine sans toucher au `docker-compose.yaml`.

### Ce que fait `airflow-init`

Il s'exécute **une seule fois**, puis s'arrête avec le code 0 : c'est normal, ce n'est pas un
plantage. Il crée les tables de la base de métadonnées (`_AIRFLOW_DB_MIGRATE`) et le compte
administrateur (`_AIRFLOW_WWW_USER_CREATE`). Les autres services attendent qu'il ait terminé avant
de démarrer (`condition: service_completed_successfully`).

---

## 3. Les cinq services, et ce qui se passe quand l'un d'eux s'arrête

```
                ┌──────────────────────┐
  navigateur ──▶│  airflow-apiserver   │  interface web + API REST + API d'exécution
                └──────────┬───────────┘
                           │
  dags/*.py ──▶ ┌──────────┴───────────┐     ┌────────────────────┐
                │ airflow-dag-processor│────▶│      postgres       │  base de MÉTADONNÉES
                └──────────────────────┘     │ (DAG, exécutions,   │  (pas vos données !)
                ┌──────────────────────┐     │  états, XCom…)      │
                │  airflow-scheduler   │────▶│                     │
                │  + LocalExecutor     │     └────────────────────┘
                └──────────────────────┘              ▲
                ┌──────────────────────┐              │
                │  airflow-triggerer   │──────────────┘
                └──────────────────────┘
```

| Service | Son rôle | S'il s'arrête… |
|---|---|---|
| `postgres` | stocke l'état d'Airflow : quels DAG existent, quelles exécutions ont eu lieu, avec quel résultat | plus rien ne fonctionne |
| `airflow-apiserver` | sert l'interface web et l'API | plus d'interface… mais **les DAG continuent de tourner** |
| `airflow-scheduler` | décide quoi lancer et quand ; avec le `LocalExecutor`, il lance aussi les tâches | plus rien ne démarre : les exécutions restent en `queued` |
| `airflow-dag-processor` | lit les fichiers de `dags/` et enregistre les DAG | un nouveau DAG ou une modification **n'apparaît jamais** |
| `airflow-triggerer` | fait patienter les tâches **différées** (jeudi) | ces tâches restent bloquées en `deferred` |

### Exercice 1 — casser pour comprendre (30 min, en binôme)

1. Arrêtez le scheduler : `docker compose stop airflow-scheduler`.
   Déclenchez `bonjour_airflow` depuis l'interface. Que se passe-t-il ? Dans quel état reste
   l'exécution ?
2. Redémarrez-le : `docker compose start airflow-scheduler`. Que devient l'exécution ?
3. Arrêtez le dag-processor. Créez un fichier `dags/test_arret.py` en copiant `bonjour_airflow.py`
   et en changeant le `dag_id`. Attendez deux minutes. Le DAG apparaît-il ?
4. Redémarrez le dag-processor et chronométrez l'apparition du DAG.
5. Arrêtez l'apiserver. Les DAG en cours s'arrêtent-ils ?

Notez vos observations : elles vous serviront toute la semaine pour diagnostiquer une panne.

> 💡 **Pourquoi `LocalExecutor` et pas `CeleryExecutor` ?** Le fichier officiel utilise Celery,
> avec un broker Redis et un ou plusieurs `airflow-worker`. C'est l'architecture qui permet de
> répartir les tâches sur plusieurs machines. Sur un portable, elle ajoute deux conteneurs sans
> rien apporter : le `LocalExecutor` lance les tâches comme des processus du scheduler. Le
> changement tient en une ligne (`AIRFLOW__CORE__EXECUTOR`) et vous saurez la justifier.

### Lire le `docker-compose.yaml`

Ouvrez `atelier/docker-compose.yaml`. Trois choses à comprendre :

| Élément | Ce qu'il fait |
|---|---|
| `x-airflow-common: &airflow-common` | un bloc de configuration commun, défini une fois. Chaque service Airflow le réutilise avec `<<: *airflow-common`. Modifier une variable dans ce bloc la modifie pour tous les services. |
| `environment` | la configuration d'Airflow. Toute option de `airflow.cfg` peut se régler par une variable `AIRFLOW__SECTION__CLE` : `AIRFLOW__CORE__EXECUTOR` = option `executor` de la section `[core]`. |
| `volumes` | les dossiers partagés entre votre machine et les conteneurs. Vous éditez `dags/` avec votre éditeur, Airflow voit le changement. |

---

## 4. Votre premier DAG

Ouvrez `atelier/dags/bonjour_airflow.py` :

```python
import pendulum
from airflow.sdk import dag, task


@dag(
    dag_id="bonjour_airflow",
    schedule=None,                                    # uniquement à la main
    start_date=pendulum.datetime(2026, 1, 1, tz="UTC"),
    catchup=False,
    tags=["cours", "lundi"],
)
def bonjour_airflow():
    @task
    def extraire() -> list[int]:
        return [12, 7, 31, 18]

    @task
    def transformer(montants: list[int]) -> dict:
        return {"nb": len(montants), "total": sum(montants)}

    @task
    def charger(resume: dict) -> None:
        print(f"{resume['nb']} courses, {resume['total']} dollars au total")

    charger(transformer(extraire()))


bonjour_airflow()
```

| Ligne | Ce qu'elle fait |
|---|---|
| `from airflow.sdk import dag, task` | l'API d'Airflow 3 pour écrire des DAG (le *Task SDK*) |
| `@dag(...)` | transforme la fonction en DAG. `dag_id` est son nom unique. |
| `schedule=None` | aucun planning : le DAG ne tourne que si on le déclenche |
| `start_date` | toujours une date **fixe**, jamais `datetime.now()` (vous verrez pourquoi mardi) |
| `@task` | chaque fonction devient une tâche |
| `charger(transformer(extraire()))` | appeler une tâche avec la sortie d'une autre crée **la dépendance et l'échange de données** (XCom) |
| `bonjour_airflow()` | la dernière ligne enregistre le DAG. Oubliez-la et le DAG n'existe pas. |

### Exercice 2 — faire tourner et lire (45 min)

1. Dans l'interface, activez le DAG (interrupteur à gauche de son nom), puis déclenchez-le (▶).
2. Ouvrez la vue **Grid** : une colonne par exécution, une case par tâche. Cliquez sur une case.
3. Ouvrez les **logs** de `charger` : retrouvez la ligne `4 courses, 68 dollars au total`.
4. Ouvrez l'onglet **XCom** de `transformer` : que contient-il ?
5. Ouvrez la vue **Graph** : retrouvez les dépendances.
6. Depuis le terminal :

```bash
docker compose exec airflow-scheduler airflow dags list
docker compose exec airflow-scheduler airflow dags test bonjour_airflow
```

`airflow dags test` exécute tout le DAG dans le terminal, sans passer par le scheduler : c'est
l'outil de mise au point le plus rapide.

> ⚠️ **Un DAG nouvellement créé est en pause.** Le fichier de configuration dit
> `DAGS_ARE_PAUSED_AT_CREATION = true`. Un DAG en pause accepte vos déclenchements… mais ne les
> exécute pas : ils restent en `queued` indéfiniment. C'est la première cause de « mon DAG ne
> fait rien ».

### Exercice 3 — le DAG cassé (30 min)

1. Dans `bonjour_airflow.py`, ajoutez une faute : `import pandass`.
2. Attendez 30 secondes. Que montre l'interface ? Cherchez le bandeau rouge **DAG Import Errors**.
3. Retrouvez l'erreur en ligne de commande :

```bash
docker compose exec airflow-scheduler airflow dags list-import-errors
```

4. Corrigez. Combien de temps avant que le DAG redevienne normal ?

Retenez ce réflexe : **un DAG qui n'apparaît pas a presque toujours une erreur d'import**.

### Exercice 4 — à vous (1 h)

Écrivez `dags/mon_premier_dag.py` avec quatre tâches :

1. `lister_mois` renvoie la liste `["2025-01", "2025-02", "2025-03"]` ;
2. `construire_urls` renvoie, pour chaque mois, l'URL du fichier TLC :
   `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_AAAA-MM.parquet` ;
3. `verifier_urls` fait une requête `HEAD` sur chaque URL (`requests.head(url, timeout=30)`) et
   renvoie un dictionnaire `{mois: code_http}` ;
4. `resumer` affiche combien de fichiers sont disponibles.

Puis essayez avec un mois qui n'existe pas encore. Quel code HTTP obtenez-vous ?

> 💡 **Réponse attendue** : `403`, et non `404`. La source est servie par un CDN (CloudFront) qui
> répond « interdit » pour un fichier absent. Gardez-le en tête : jeudi, ce détail cassera un
> capteur du provider HTTP.

---

## 5. Ce qu'il ne faut jamais faire dans un fichier de DAG

Le dag-processor **relit vos fichiers toutes les 30 secondes** (réglé dans le
`docker-compose.yaml` ; 5 minutes par défaut en production). Tout ce qui est écrit **en dehors
des tâches** s'exécute à chaque lecture.

```python
# ❌ Au niveau du module : exécuté toutes les 30 s, même si le DAG ne tourne pas
donnees = requests.get("https://...").json()
connexion = snowflake.connector.connect(...)

# ✅ Dans une tâche : exécuté uniquement quand la tâche tourne
@task
def extraire():
    return requests.get("https://...").json()
```

---

## 6. Auto-évaluation

- [ ] Je sais démarrer, arrêter et remettre à zéro la stack (`up -d`, `down`, `down -v`).
- [ ] Je sais dire à quoi sert chacun des cinq services, et ce qui casse si l'un d'eux s'arrête.
- [ ] Je sais pourquoi on utilise ici le `LocalExecutor`.
- [ ] Je sais écrire un DAG TaskFlow et passer la sortie d'une tâche à la suivante.
- [ ] Je sais lire une exécution : vue Grid, logs, XCom.
- [ ] Je pense à activer un DAG avant de conclure qu'il ne fonctionne pas.
- [ ] Je sais trouver une erreur d'import dans l'interface et en ligne de commande.
- [ ] Je ne mets aucun appel réseau ni calcul lourd au niveau du module.

## 7. Pour aller plus loin

- Docker Compose officiel : https://airflow.apache.org/docs/apache-airflow/stable/howto/docker-compose/index.html
- Architecture d'Airflow 3 : https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/overview.html
- TaskFlow : https://airflow.apache.org/docs/apache-airflow/stable/tutorial/taskflow.html

➡️ **Demain : [02 — Le temps : planification et ingestion](02-mardi-planification-ingestion.md)**
