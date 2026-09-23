# 02 — Mardi : le temps, la planification et l'ingestion

> 🎬 **Le fil rouge.** L'analyste vous montre son rituel : « Le 5 du mois, je télécharge le
> fichier du mois d'avant. Sauf quand il n'est pas encore sorti. Et quand je pars en vacances, je
> rattrape à mon retour… en espérant ne rien oublier. » Aujourd'hui, vous écrivez un DAG qui sait
> **quel mois il doit traiter** sans qu'on le lui dise, et qui sait **rattraper** un historique.

| | |
|---|---|
| **Matin** | Date logique, intervalle de données, `schedule`, `catchup`, backfill · le piège d'Airflow 3 |
| **Après-midi** | DAG mensuel de téléchargement · idempotence · rattrapage de janvier à mars 2025 |
| **Point de départ** | [`atelier/exercices/mardi_telechargement.py`](atelier/exercices/mardi_telechargement.py) |

---

## Objectifs

1. Distinguer date d'exécution, date logique et intervalle de données.
2. Choisir le bon type de planning, et savoir pourquoi `@monthly` ne suffit plus en Airflow 3.
3. Écrire une tâche qui tire toutes ses dates du contexte, jamais de `datetime.now()`.
4. Rendre un téléchargement idempotent.
5. Rattraper un historique avec un backfill.

---

## 1. Trois dates qu'il ne faut pas confondre

Le fichier de janvier 2025 contient les courses **du 1er au 31 janvier**. On ne peut le traiter
qu'**après** le 31 janvier. Airflow distingue donc :

| Notion | Pour l'exécution qui traite janvier 2025 | Variable du contexte |
|---|---|---|
| **Intervalle de données** | du 1er janvier 2025 00:00 au 1er février 2025 00:00 | `data_interval_start`, `data_interval_end` |
| **Date logique** | 1er janvier 2025 (le début de l'intervalle) | `logical_date`, et `ds` = `"2025-01-01"` |
| **Date d'exécution réelle** | le 1er février 2025 ou après | `run_after` / `start_date` de l'exécution |

> 📌 **La règle d'or de l'orchestration** : une tâche ne demande jamais « quelle heure est-il ? ».
> Elle demande « **quel intervalle dois-je traiter ?** ». C'est ce qui permet de rejouer le mois de
> mars en septembre et d'obtenir exactement le même résultat qu'en avril.

```python
# ❌ Faux : relancé en septembre, ce code traite août, pas le mois demandé
mois = (datetime.now() - relativedelta(months=1)).strftime("%Y-%m")

# ✅ Juste : le mois vient de l'exécution
@task
def telecharger(data_interval_start=None):
    mois = data_interval_start.strftime("%Y-%m")
```

Avec TaskFlow, **un paramètre qui porte le nom d'une variable du contexte est rempli
automatiquement** : `data_interval_start=None` suffit. Dans un opérateur classique, on utilise un
gabarit Jinja : `"{{ data_interval_start.strftime('%Y-%m') }}"`.

---

## 2. Le piège d'Airflow 3 : `@monthly` n'a plus d'intervalle

En Airflow 2, `schedule="@monthly"` créait un intervalle de données d'un mois. **En Airflow 3, ce
n'est plus le cas** : un raccourci cron déclenche une exécution à l'heure dite, et
`data_interval_start` vaut… l'heure de l'exécution.

Nous l'avons constaté en préparant ce cours : avec `schedule="@monthly"`, l'exécution du
1er septembre 2026 cherchait le fichier de **septembre**, pas celui d'août.

| Planning | Exécution du 1er septembre 2026 | Usage |
|---|---|---|
| `schedule="@monthly"` (= `CronTriggerTimetable`) | `data_interval_start` = 2026-09-01 | « lance ce traitement à cette heure » : un rapport, un nettoyage |
| `schedule=CronDataIntervalTimetable("@monthly", timezone="UTC")` | intervalle **août** : 2026-08-01 → 2026-09-01 | « traite la période qui vient de se terminer » : **une ingestion** |

```python
from airflow.sdk import CronDataIntervalTimetable, dag

@dag(
    schedule=CronDataIntervalTimetable("@monthly", timezone="UTC"),
    start_date=pendulum.datetime(2025, 1, 1, tz="UTC"),
    catchup=False,
)
```

> 💡 Le comportement d'Airflow 2 peut être rétabli pour toute l'instance avec l'option
> `[scheduler] create_cron_data_intervals = True`. Préférez l'écrire **dans le DAG** : celui qui le
> lit comprend tout de suite ce qu'il traite.

### `start_date` et `catchup`

| Paramètre | À retenir |
|---|---|
| `start_date` | toujours une date **fixe** et avec fuseau (`pendulum.datetime(2025, 1, 1, tz="UTC")`). Jamais `datetime.now()` : la date changerait à chaque lecture du fichier. |
| `catchup` | `False` par défaut en Airflow 3. À `True`, activer le DAG lance **toutes** les exécutions manquées depuis `start_date`. Pratique… et dangereux : 20 mois d'un coup, c'est 20 téléchargements simultanés. On préfère rattraper **explicitement**, avec un backfill. |
| `max_active_runs` | combien d'exécutions du DAG peuvent tourner en même temps. Votre garde-fou pendant un rattrapage. |
| fuseau horaire | Airflow travaille en **UTC**. Les heures de l'interface sont en UTC par défaut. Les données TLC, elles, sont en heure de New York : on le note, on ne mélange pas. |

### Un déclenchement manuel n'a pas de date logique

En Airflow 3, cliquer sur ▶ crée une exécution **sans date logique**. Si votre tâche lit
`data_interval_start`, elle ne traite pas le mois que vous imaginez. Deux solutions :

- **rejouer un mois passé** → un backfill (section 4) ;
- **choisir le mois à la main** → un paramètre du DAG (jeudi, avec `Param`).

---

## 3. Un téléchargement idempotent

**Idempotent** : l'exécuter une fois ou dix fois donne le même résultat. C'est la propriété qui
rend un pipeline rejouable sans crainte.

| Risque | Ce qui arrive | Parade |
|---|---|---|
| Coupure réseau au milieu | un fichier tronqué qui **a l'air** complet | écrire dans `fichier.part`, puis renommer une fois fini |
| Deux exécutions du même mois | deux copies, ou une copie écrasée pendant sa lecture | un chemin **déterminé par le mois**, jamais par l'heure |
| Fichier republié par la source | on garde l'ancien | on retélécharge à chaque exécution (jeudi : on comparera l'`ETag`) |

```python
def telecharger_mois(mois: str) -> dict:
    DOSSIER.mkdir(parents=True, exist_ok=True)
    cible = DOSSIER / f"yellow_tripdata_{mois}.parquet"
    partiel = cible.with_suffix(".part")

    with requests.get(url_fichier(mois), stream=True, timeout=(10, 300)) as rep:
        rep.raise_for_status()                       # 403 = pas publié : la tâche échoue
        with partiel.open("wb") as f:
            for bloc in rep.iter_content(chunk_size=1 << 20):   # par blocs de 1 Mo
                f.write(bloc)
    partiel.replace(cible)                           # atomique : tout ou rien

    nb_lignes = pq.ParquetFile(cible).metadata.num_rows   # lu dans l'en-tête, sans tout charger
    return {"mois": mois, "chemin": str(cible), "nb_lignes": nb_lignes}
```

> ⚠️ **Ce que la tâche renvoie part dans un XCom**, stocké dans la base de métadonnées. On y met
> un chemin et quelques chiffres, **jamais le contenu du fichier**. 60 Mo de Parquet dans un XCom,
> c'est une base Postgres qui gonfle à chaque exécution.

Où écrire le code partagé ? Dans `plugins/tlc/`, qu'Airflow ajoute au chemin d'import de tous ses
services. Les DAG font alors `from tlc.chargement import telecharger_mois`, et la même fonction
servira au DAG d'ingestion comme au DAG de rattrapage.

---

## 4. Rattraper l'historique : le backfill

Un **backfill** crée une exécution par intervalle sur une plage de dates, et le scheduler les
exécute comme des exécutions normales : elles apparaissent dans la vue Grid, avec leurs logs.

Depuis l'interface : page du DAG › bouton **Backfill**. Ou en ligne de commande :

```bash
# Voir ce qui serait créé, sans rien lancer
docker compose exec airflow-scheduler airflow backfill create \
    --dag-id taxi_jaune_telechargement \
    --from-date 2025-01-01 --to-date 2025-03-01 --dry-run

# Lancer
docker compose exec airflow-scheduler airflow backfill create \
    --dag-id taxi_jaune_telechargement \
    --from-date 2025-01-01 --to-date 2025-03-01 --max-active-runs 2
```

| Option | Sens |
|---|---|
| `--from-date` / `--to-date` | bornes des **dates logiques** (débuts d'intervalle), incluses. `2025-01-01` → `2025-03-01` = janvier, février, mars. |
| `--max-active-runs` | combien de mois en parallèle |
| `--reprocess-behavior` | que faire des mois déjà traités : `none` (ne pas refaire), `failed` (refaire les échecs), `completed` (tout refaire) |
| `--run-backwards` | commencer par le mois le plus récent |

> ⚠️ Le DAG doit être **activé** pour que les exécutions du backfill démarrent.

---

## 5. Atelier (après-midi)

Partez de [`atelier/exercices/mardi_telechargement.py`](atelier/exercices/mardi_telechargement.py),
copiez-le dans `atelier/dags/`, et complétez les `TODO`.

1. **`plugins/tlc/chargement.py`** : écrivez `telecharger_mois(mois)` (section 3).
2. **Le DAG** `taxi_jaune_telechargement` : planning mensuel **avec intervalle**, `start_date` au
   1er janvier 2025, `catchup=False`, deux reprises espacées de 2 minutes.
3. **`telecharger`** : tire le mois de `data_interval_start`.
4. **`controler`** : compte les courses dont la prise en charge tombe **hors** de l'intervalle
   (indice : `pyarrow.compute`, colonne `tpep_pickup_datetime`), affiche le résultat, et fait
   échouer la tâche si plus de 1 % des lignes sont hors du mois.
5. **Rattrapez** janvier à mars 2025 avec un backfill.

✅ **Valeurs attendues** (données TLC au 23/09/2026) :

| Mois | Lignes | Hors du mois |
|---|---|---|
| 2025-01 | 3 475 226 | 22 |
| 2025-02 | 3 577 543 | 31 |
| 2025-03 | 4 145 257 | 33 |

6. **Observez** ce qui arrive à l'exécution planifiée qui cherche le **dernier** mois : le fichier
   n'est pas encore publié. Combien de fois la tâche est-elle tentée ? Que dit l'erreur ? Est-ce
   une vraie panne ?

> 💡 **Réponse à la question 6** : ce n'est pas une panne, c'est un fichier **pas encore publié**.
> Réessayer toutes les 2 minutes n'a aucun sens pour un fichier qui arrivera dans trois semaines.
> Il faut **attendre**, et attendre sans bloquer de ressource : c'est le sujet de jeudi.

---

## 6. Auto-évaluation

- [ ] Je sais dire quelle période traite l'exécution du 1er mars d'un DAG mensuel à intervalle.
- [ ] Je sais pourquoi `schedule="@monthly"` ne convient pas à une ingestion en Airflow 3.
- [ ] Mes tâches tirent leurs dates du contexte, jamais de `datetime.now()`.
- [ ] Ma `start_date` est fixe, avec un fuseau horaire.
- [ ] Mon téléchargement ne laisse jamais de fichier tronqué.
- [ ] Je ne mets jamais de données volumineuses dans un XCom.
- [ ] Je sais lancer un backfill, en ligne de commande et depuis l'interface.
- [ ] Je sais distinguer « la source n'a pas encore publié » d'« il y a une panne ».

## 7. Pour aller plus loin

- Dates et intervalles : https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/timetable.html
- Backfill : https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/backfill.html
- Gabarits et variables du contexte : https://airflow.apache.org/docs/apache-airflow/stable/templates-ref.html

➡️ **Demain : [03 — Snowflake : connexion, chargement, parallélisme](03-mercredi-snowflake-connexions-parallelisme.md)**
