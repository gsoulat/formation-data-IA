# 04 — Jeudi : capteurs différés, assets et branchement

> 🎬 **Le fil rouge.** Mardi, votre DAG a échoué sur le dernier mois : le fichier n'était pas
> encore publié. L'analyste hausse les épaules : « La TLC publie quand elle veut. Des fois le 20,
> des fois deux mois après. » Aujourd'hui, le pipeline cesse d'espérer que la donnée est là à une
> heure fixe : il **attend** qu'elle arrive, sans rien bloquer, et la suite démarre **parce que**
> la donnée a changé.

| | |
|---|---|
| **Matin** | Capteurs : `poke`, `reschedule`, différé · le triggerer · lire un capteur différé écrit à la main |
| **Après-midi** | Branchement « déjà chargé ? » · assets : la transformation déclenchée par la donnée |
| **Point de départ** | [`atelier/exercices/jeudi_ingestion.py`](atelier/exercices/jeudi_ingestion.py) |

---

## Objectifs

1. Choisir entre les trois façons d'attendre, et justifier le mode différé.
2. Comprendre comment un opérateur différé et un déclencheur se partagent le travail.
3. Terminer proprement quand il n'y a rien à faire (branchement).
4. Enchaîner deux DAG par la donnée plutôt que par l'horloge (assets).

---

## 1. Attendre : trois façons, un seul bon choix ici

Un **capteur** (*sensor*) est une tâche qui attend qu'une condition soit vraie : un fichier
publié, une table remplie, une heure atteinte.

| Mode | Pendant l'attente | Coût pour 24 mois qui attendent 3 semaines |
|---|---|---|
| `poke` (défaut) | la tâche **occupe une place d'exécution**, et dort entre deux vérifications | 24 places bloquées trois semaines : plus rien d'autre ne tourne |
| `reschedule` | la tâche se termine entre deux vérifications et reprend une place à chaque vérification | acceptable, mais chaque vérification relance un processus Python complet |
| **différé** (*deferrable*) | la tâche **rend sa place** et confie l'attente au **triggerer**, une boucle `asyncio` qui fait patienter des milliers d'attentes à la fois | quasi nul : 24 coroutines légères dans un seul service |

La TLC publie **un à trois mois** après la fin du mois. Une attente longue, sans date connue,
répétée chaque mois : c'est exactement le cas du mode différé.

---

## 2. Comment fonctionne une tâche différée

```
 exécuteur (scheduler)                          triggerer
 ─────────────────────                          ─────────
 FichierPublieSensor.execute()
   │ HEAD sur l'URL → 403 (pas publié)
   │ self.defer(trigger=…)  ───────────────▶   FichierPublieTrigger.run()   (async)
   ▼                                              boucle : HEAD toutes les 6 h
 la tâche passe en "deferred"                     403 → attendre…
 et libère sa place                               200 → yield TriggerEvent({...})
                                                          │
 FichierPublieSensor.execute_complete(event)  ◀──────────┘
   la tâche reprend et renvoie l'événement (XCom)
```

Deux classes, deux rôles :

| Classe | Tourne où | Rôle |
|---|---|---|
| **Opérateur** (`FichierPublieSensor`) | sur l'exécuteur | vérifie une fois ; si ce n'est pas prêt, appelle `self.defer()` et s'arrête |
| **Déclencheur** (`FichierPublieTrigger`) | dans `airflow-triggerer` | une coroutine qui attend la condition et émet un `TriggerEvent` |

> ⚠️ **Le triggerer doit tourner.** S'il est arrêté, les tâches restent en `deferred` pour
> toujours, sans erreur. Refaites le test du lundi : `docker compose stop airflow-triggerer`.

### Pourquoi ne pas utiliser `HttpSensor(deferrable=True)` ?

Le provider HTTP fournit un capteur différé. En préparant ce cours, nous l'avons lu, et il ne
convient pas à notre source :

- son déclencheur ne se remet en attente que si le serveur répond **404** ;
- la TLC (derrière le CDN CloudFront) répond **403** pour un fichier pas encore publié ;
- sur un 403, le déclencheur **reboucle immédiatement, sans pause** : il bombarde le serveur ;
- son paramètre `response_error_codes_allowlist` n'est pas transmis au déclencheur.

La leçon dépasse ce cas : **un opérateur fourni n'est pas une garantie**. Testez-le contre votre
vraie source avant de lui confier la production.

### Le capteur de l'atelier

Il est fourni, dans [`atelier/plugins/tlc/capteurs.py`](atelier/plugins/tlc/capteurs.py). Lisez-le
en entier (une centaine de lignes) avant de l'utiliser. Les passages clés :

```python
class FichierPublieTrigger(BaseTrigger):
    def serialize(self):
        # Le triggerer recrée l'objet dans un autre processus, à partir de ce chemin
        # d'import et de ces arguments : ils doivent être sérialisables en JSON.
        return ("tlc.capteurs.FichierPublieTrigger", {"url": self.url, "intervalle": self.intervalle})

    async def run(self):
        async with aiohttp.ClientSession() as session:
            while True:
                async with session.head(self.url) as rep:
                    if rep.status == 200:
                        yield TriggerEvent({"statut": "publie", "etag": ..., "taille": ...})
                        return
                    if rep.status not in (403, 404):
                        yield TriggerEvent({"statut": "erreur", "code": rep.status})
                        return
                await asyncio.sleep(self.intervalle)     # jamais time.sleep() : bloquerait tout le triggerer


class FichierPublieSensor(BaseSensorOperator):
    template_fields = ("url",)                          # l'URL peut contenir du Jinja

    def execute(self, context):
        rep = requests.head(self.url, timeout=30)
        if rep.status_code == 200:
            return {...}                                # déjà publié : inutile de différer
        self.defer(trigger=FichierPublieTrigger(url=self.url, intervalle=self.intervalle),
                   method_name="execute_complete",
                   timeout=timedelta(seconds=self.timeout))

    def execute_complete(self, context, event):
        if event["statut"] != "publie":
            raise RuntimeError(...)
        return event                                    # part dans un XCom
```

| Point | Pourquoi |
|---|---|
| `asyncio.sleep`, jamais `time.sleep` | le triggerer fait tourner **toutes** les attentes dans une seule boucle. Un `time.sleep` les gèle toutes. |
| premier essai dans `execute` | si le fichier est déjà là (rattrapage), on évite un aller-retour par le triggerer |
| `timeout` | au-delà, la tâche échoue. Pour la TLC : 90 jours. |
| `retries=0` sur le capteur | un capteur qui a attendu 90 jours en vain ne doit pas repartir pour 90 jours |
| l'événement contient l'`ETag` | l'empreinte du fichier côté serveur : elle change si la TLC republie le mois |

Utilisation dans le DAG :

```python
MOIS = "{{ params.mois or data_interval_start.strftime('%Y-%m') }}"

publication = FichierPublieSensor(
    task_id="attendre_publication",
    url=url_fichier(MOIS),               # rendu par Jinja au moment de l'exécution
    intervalle=6 * 3600,                 # une vérification toutes les 6 h
    timeout=90 * 24 * 3600,
    retries=0,
)
```

---

## 3. Terminer proprement : le branchement

Un mois peut être déjà chargé, et inchangé : la TLC ne l'a pas republié. Recharger 3,5 millions
de lignes pour rien coûte des crédits. On **choisit** alors la branche à suivre :

```python
@task.branch
def verifier_nouveaute(publication: dict) -> str:
    if etag_deja_charge(SnowflakeHook(), mois_courant()) == publication["etag"]:
        return "deja_a_jour"          # id de la tâche à exécuter ; les autres branches sont sautées
    return "telecharger"

choix = verifier_nouveaute(publication.output)
choix >> [telecharger_tache, EmptyOperator(task_id="deja_a_jour")]
```

La fonction renvoie l'**identifiant** de la tâche à suivre. Les tâches des autres branches passent
en `skipped`, puis leurs descendantes aussi. L'exécution se termine **en succès** : il n'y avait
rien à faire, ce n'est pas une erreur.

L'`ETag` de chaque mois chargé est noté dans `RAW.LOAD_LOG` par la tâche `charger`.

### Les règles de déclenchement (*trigger rules*)

Par défaut, une tâche ne démarre que si **toutes** ses tâches amont ont réussi (`all_success`). On
peut changer cette règle :

| Règle | La tâche démarre si… | Exemple |
|---|---|---|
| `all_success` (défaut) | toutes les amont ont réussi | `charger` après `telecharger` |
| `all_done` | toutes les amont sont terminées, quel que soit leur état | `nettoyer` : supprimer le fichier local même si le chargement a échoué |
| `none_failed_min_one_success` | aucune n'a échoué et au moins une a réussi | rejoindre deux branches après un branchement |
| `one_failed` | au moins une a échoué | une tâche d'alerte |

---

## 4. Enchaîner par la donnée : les assets

Mardi, on aurait pu planifier la transformation « le 25 de chaque mois, en espérant que
l'ingestion soit finie ». Avec les **assets**, la transformation démarre **quand la table brute a
été mise à jour**, et seulement dans ce cas.

```python
from airflow.sdk import Asset

TRAJETS_BRUTS = Asset("nyc_taxi.raw.yellow_trips")

# DAG d'ingestion : la tâche qui écrit déclare ce qu'elle produit
@task(pool="snowflake", outlets=[TRAJETS_BRUTS])
def charger(fichier, publication): ...

# DAG de transformation : pas d'horaire, il écoute l'asset
@dag(schedule=[TRAJETS_BRUTS], ...)
def taxi_jaune_indicateurs(): ...
```

| Ce qui se passe | Pourquoi c'est mieux qu'un horaire |
|---|---|
| `charger` réussit → Airflow enregistre un **événement** sur l'asset | la transformation ne tourne jamais sur une table incomplète |
| le DAG `taxi_jaune_indicateurs` démarre | si l'ingestion prend trois semaines de retard, la transformation aussi, automatiquement |
| si `charger` est sautée (branche `deja_a_jour`), pas d'événement | pas de recalcul inutile |

Dans l'interface : menu **Assets**, et le graphe qui relie les deux DAG.

> 💡 **Le nom d'un asset.** C'est un identifiant, pas une connexion : Airflow ne va pas lire
> Snowflake. Un préfixe comme `snowflake://` déclenche une validation par le provider, qui exige
> alors une URI complète (`snowflake://compte/base/schéma/table`). Un nom simple et stable
> (`nyc_taxi.raw.yellow_trips`) suffit, **à condition d'utiliser exactement le même** dans les deux
> DAG.

### Le DAG de transformation

Il calcule deux tables dans `MARTS` avec `SQLExecuteQueryOperator` : les calculs sont faits **par
Snowflake**, Airflow ne voit passer aucune ligne.

```python
from airflow.providers.common.sql.operators.sql import SQLExecuteQueryOperator

indicateurs = SQLExecuteQueryOperator(
    task_id="indicateurs_mensuels",
    conn_id="snowflake_default",
    sql="""
        CREATE OR REPLACE TABLE MARTS.INDICATEURS_MENSUELS AS
        SELECT DATE_TRUNC('month', TPEP_PICKUP_DATETIME)::DATE AS MOIS,
               COUNT(*)                          AS NB_COURSES,
               ROUND(MEDIAN(TRIP_DISTANCE), 2)   AS DISTANCE_MEDIANE_MILES,
               ROUND(MEDIAN(TOTAL_AMOUNT), 2)    AS MONTANT_MEDIAN_USD
        FROM RAW.YELLOW_TRIPS
        WHERE TOTAL_AMOUNT > 0 AND TRIP_DISTANCE > 0
        GROUP BY 1
    """,
)
```

> 🧭 **Le piège des dates hors du mois.** Mardi, votre contrôle a trouvé quelques dizaines de
> courses par fichier dont la date sort du mois (le fichier de juillet 2026 contient même des
> courses datées de 2008). Grouper par `DATE_TRUNC('month', TPEP_PICKUP_DATETIME)` crée alors de
> faux « mois » de quelques lignes. Groupez plutôt par le **mois du fichier source**, et filtrez les
> courses hors de ce mois — en les comptant dans une table de qualité.

---

## 5. Atelier (après-midi)

Partez de [`atelier/exercices/jeudi_ingestion.py`](atelier/exercices/jeudi_ingestion.py) : le DAG
`taxi_jaune_ingestion`, à compléter.

1. Ajoutez le capteur `attendre_publication` devant le téléchargement.
2. Ajoutez un paramètre `mois` (`Param`, motif `AAAA-MM`, vide par défaut) pour rejouer un mois à
   la main ; utilisez-le dans le gabarit de l'URL et dans `mois_courant()`.
3. Écrivez `verifier_nouveaute` (branchement) et la tâche vide `deja_a_jour`.
4. Faites écrire l'`ETag` dans `RAW.LOAD_LOG` après chaque chargement (`MERGE`).
5. Déclarez l'asset en sortie de `charger`, et écrivez le DAG `taxi_jaune_indicateurs` qui
   l'écoute : une table `MARTS.QUALITE_MENSUELLE`, puis `MARTS.INDICATEURS_MENSUELS`.
6. Ajoutez `nettoyer`, qui supprime le fichier local **même si le chargement a échoué**.

**Vérifications :**

| Test | Résultat attendu |
|---|---|
| Déclencher avec `{"mois": "<un mois pas encore publié>"}` | `attendre_publication` passe en `deferred` ; le log du triggerer affiche `pas encore publié (HTTP 403)` |
| Arrêter le triggerer pendant l'attente | la tâche reste en `deferred`, sans erreur. Le redémarrer : l'attente reprend |
| Déclencher avec `{"mois": "2025-01"}` (déjà chargé mercredi) | `deja_a_jour` s'exécute, `telecharger` et `charger` sont `skipped`, l'exécution est **en succès**, `taxi_jaune_indicateurs` **ne démarre pas** |
| Supprimer la ligne de janvier dans `RAW.LOAD_LOG`, redéclencher | janvier est rechargé (toujours 3 475 226 lignes), puis `taxi_jaune_indicateurs` démarre tout seul |

---

## 6. Auto-évaluation

- [ ] Je sais choisir entre `poke`, `reschedule` et différé, et justifier mon choix.
- [ ] Je sais ce que font l'opérateur et le déclencheur d'une tâche différée, et où chacun tourne.
- [ ] Je sais pourquoi on n'écrit jamais `time.sleep` dans un déclencheur.
- [ ] Je teste un opérateur fourni contre ma vraie source avant de m'y fier.
- [ ] Je sais écrire un branchement et terminer une exécution en succès quand il n'y a rien à faire.
- [ ] Je connais les règles de déclenchement `all_success`, `all_done` et `none_failed_min_one_success`.
- [ ] Je sais enchaîner deux DAG par un asset, et dire pourquoi c'est préférable à un horaire.

## 7. Pour aller plus loin

- Opérateurs différés : https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html
- Assets et planification par la donnée : https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/asset-scheduling.html
- Branchement : https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#branching
- Règles de déclenchement : https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#trigger-rules

➡️ **Demain : [05 — Fiabilité, tests et mini-brief](05-vendredi-fiabilite-tests.md)**
