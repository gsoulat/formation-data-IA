# 05 — Vendredi : fiabilité, tests et mini-brief

> 🎬 **Le fil rouge.** L'analyste part lundi. Sa dernière question : « Et si ça casse à 3 h du
> matin pendant que je suis sur la plage, qui le sait ? Et quand tu modifieras le DAG dans six mois,
> comment tu sauras que tu n'as rien cassé ? » Ce matin : les alertes et les tests. Cet
> après-midi : vous transposez tout ce que vous avez appris à une nouvelle source, seul.

| | |
|---|---|
| **Matin** | Reprises · rappels d'échec · tests de DAG · méthode de débogage |
| **Après-midi** | Mini-brief (niveau 3 · transposer) : les taxis verts |
| **Point de départ** | [`atelier/exercices/vendredi_fiabilite.py`](atelier/exercices/vendredi_fiabilite.py) |

---

## Objectifs

1. Régler les reprises selon la nature de l'erreur.
2. Écrire un rappel d'échec qui produit une alerte exploitable.
3. Écrire des tests qui détectent un DAG cassé avant qu'il n'arrive en production.
4. Déboguer méthodiquement une tâche en échec.
5. Transposer le pipeline de la semaine à une nouvelle source, en autonomie.

---

## 1. Les reprises : toutes les erreurs ne se valent pas

| Erreur | Exemple | Réponse |
|---|---|---|
| **passagère** | coupure réseau, entrepôt Snowflake qui démarre, CDN qui répond 503 | reprendre : `retries=2`, `retry_delay=timedelta(minutes=5)` |
| **attendue** | fichier pas encore publié | ce n'est pas une erreur : **attendre** (capteur différé, jeudi) |
| **définitive** | colonne disparue, compte de lignes faux, clé Snowflake révoquée | échouer **une fois**, **vite**, et **alerter** : reprendre n'y changera rien |

```python
default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=5),
    "retry_exponential_backoff": True,       # 5 min, puis 10 min… : laisse le temps au service de revenir
    "max_retry_delay": timedelta(hours=1),
    "on_failure_callback": signaler_echec,
}
```

> 💡 Pour une erreur définitive détectée dans votre code, levez `AirflowFailException` (au lieu de
> `ValueError`) : la tâche échoue **sans** consommer ses reprises.

---

## 2. Une alerte qu'on peut exploiter à 3 h du matin

`on_failure_callback` est une fonction appelée quand une tâche échoue **définitivement** (après
ses reprises). Elle reçoit le contexte de l'exécution.

« La tâche `charger` a échoué » ne suffit pas. Il faut savoir, sans ouvrir Airflow :

| Information | Pourquoi |
|---|---|
| DAG et tâche | où chercher |
| **période de données** | quel mois rejouer |
| numéro de tentative | était-ce la dernière ? |
| message d'erreur | panne passagère ou définitive ? |
| **lien direct vers les logs** | un clic, pas une recherche |

Le rappel de l'atelier ([`plugins/tlc/alertes.py`](atelier/plugins/tlc/alertes.py)) écrit tout
cela dans les logs, et l'envoie à un webhook (Discord, Slack, Teams…) si la variable Airflow
`ALERTE_WEBHOOK` existe :

```python
def signaler_echec(context) -> None:
    ti = context["ti"]
    debut = context.get("data_interval_start")
    message = {
        "dag": ti.dag_id, "tache": ti.task_id,
        "periode": debut.strftime("%Y-%m") if debut else "déclenchement manuel",
        "tentative": ti.try_number,
        "erreur": repr(context.get("exception"))[:500],
        "logs": getattr(ti, "log_url", None),
    }
    log.error("ÉCHEC %s", message)

    url = Variable.get("ALERTE_WEBHOOK", default=None)
    if url:
        try:
            requests.post(url, json={"content": texte, "text": texte}, timeout=10)
        except requests.RequestException as exc:
            log.warning("Webhook d'alerte injoignable : %s", exc)   # ne jamais masquer l'erreur d'origine
```

> ⚠️ **Une alerte qui plante ne doit jamais masquer la vraie panne.** D'où le `try` / `except`
> autour de l'envoi : si le webhook est injoignable, on le note et on laisse l'erreur d'origine
> remonter.

**Tester son alerte** : créez un webhook sur un salon Discord de test, déclarez la variable
(*Admin › Variables* › `ALERTE_WEBHOOK`), puis faites échouer une tâche exprès.

> 💡 Airflow 3 propose aussi des **alertes d'échéance** (`DeadlineAlert`) : prévenir si une
> exécution n'est pas terminée à une heure donnée. Elles remplacent les SLA d'Airflow 2. Utile
> quand le problème n'est pas une erreur mais un **retard**.

---

## 3. Tester ses DAG

Un DAG cassé ne produit **aucune erreur visible** au moment où vous l'écrivez : il disparaît
simplement de l'interface au prochain passage du dag-processor. Les tests le détectent en une
seconde, avant le commit.

```bash
docker compose exec airflow-scheduler pytest /opt/airflow/tests -q
```

### Niveau 1 — le DAG s'importe

```python
from airflow.dag_processing.dagbag import DagBag      # Airflow 3 : plus dans airflow.models

@pytest.fixture(scope="session")
def dagbag():
    return DagBag(dag_folder="/opt/airflow/dags")

def test_aucune_erreur_import(dagbag):
    assert dagbag.import_errors == {}, dagbag.import_errors
```

### Niveau 2 — la structure est celle que vous croyez

```python
def test_structure_ingestion(dagbag):
    dag = dagbag.get_dag("taxi_jaune_ingestion")
    assert set(dag.get_task("verifier_nouveaute").downstream_task_ids) == {"telecharger", "deja_a_jour"}
    assert dag.get_task("charger").pool == "snowflake"
    assert dag.get_task("attendre_publication").retries == 0
```

### Niveau 3 — la logique, sans Snowflake

C'est pour ça que `charger_mois(hook, fichier)` **reçoit** le hook au lieu de le créer : un test
peut lui passer un faux hook qui enregistre les requêtes.

```python
class FauxHook:
    def __init__(self, lignes_en_base):
        self.requetes, self.lignes_en_base = [], lignes_en_base
    def run(self, sql, autocommit=True, parameters=None):
        self.requetes.append((sql, autocommit))
    def get_first(self, sql, parameters=None):
        return (self.lignes_en_base,)

def test_chargement_idempotent_dans_une_transaction():
    hook = FauxHook(lignes_en_base=100)
    charger_mois(hook, {"mois": "2025-01", "chemin": "/tmp/f.parquet", "nb_lignes": 100})
    put, (transaction, autocommit) = hook.requetes
    assert autocommit is False                      # DELETE et COPY dans la même transaction
    assert transaction[0].startswith("DELETE")
    assert "FORCE = TRUE" in transaction[1]

def test_chargement_echoue_si_le_compte_ne_tombe_pas_juste():
    with pytest.raises(ValueError):
        charger_mois(FauxHook(lignes_en_base=99), {"mois": "2025-01", "chemin": "/tmp/f", "nb_lignes": 100})
```

### Niveau 4 — le DAG entier, en vrai

```bash
docker compose exec airflow-scheduler airflow dags test taxi_jaune_ingestion \
    -c '{"mois": "2025-01"}'
```

`airflow dags test` exécute tout le DAG dans le terminal, contre le vrai Snowflake, sans passer par
le scheduler. En Python : `dag.test()`.

> ⚠️ Si une tâche échoue et doit être reprise, `airflow dags test` **attend** le `retry_delay`
> (5 minutes ici) et semble figé. Ce n'est pas un blocage : lisez les logs au-dessus.

| Niveau | Vitesse | Besoin de Snowflake ? | Quand |
|---|---|---|---|
| 1 et 2 | 1 seconde | non | avant **chaque** commit |
| 3 | 1 seconde | non | à chaque modification du code partagé |
| 4 | quelques minutes | oui | avant une mise en production |

---

## 4. Déboguer une tâche en échec : la méthode

1. **Lire le log de la tâche**, depuis la fin. L'erreur utile est souvent la dernière ligne
   `Traceback`, pas la première.
2. **Qualifier l'erreur** : passagère, attendue ou définitive (section 1) ?
3. **Reproduire seul** : `airflow tasks test <dag> <tâche> <date>`, ou la fonction Python appelée
   directement dans le conteneur :

```bash
docker compose exec -e PYTHONPATH=/opt/airflow/plugins airflow-scheduler python -c "
from tlc.chargement import telecharger_mois; print(telecharger_mois('2025-01'))"
```

4. **Corriger, puis rejouer seulement ce qui a échoué** : dans la vue Grid, sélectionnez la tâche
   › **Clear**. Airflow la relance, ainsi que ses descendantes, pour cette exécution uniquement.

Et la [page de dépannage](depannage.md) pour les cas où rien ne démarre.

---

## 5. Mini-brief — les taxis verts *(après-midi · individuel · niveau 3 transposer)*

### Contexte

Le cabinet élargit l'étude aux **taxis verts** (*green taxis*), autorisés à prendre des clients
dans les quartiers extérieurs et le nord de Manhattan. La TLC les publie au même endroit, au même
rythme : `green_tripdata_AAAA-MM.parquet`.

Ce n'est pas un copier-coller : le fichier est différent.

| | Taxis jaunes | Taxis verts |
|---|---|---|
| Courses par mois | ~3,5 millions | ~50 000 |
| Dates de prise en charge / dépose | `tpep_pickup_datetime`, `tpep_dropoff_datetime` | `lpep_pickup_datetime`, `lpep_dropoff_datetime` |
| Colonnes propres | `Airport_fee` | `ehail_fee`, `trip_type` |

### Ce qui est attendu

Un pipeline complet pour les taxis verts, dans Snowflake, depuis janvier 2025 :

1. une table `RAW.GREEN_TRIPS` adaptée au schéma des taxis verts, à schéma évolutif ;
2. un DAG d'ingestion mensuel qui **attend** la publication, **ne recharge pas** un mois inchangé,
   charge de façon **idempotente** et **contrôle** le nombre de lignes ;
3. un **rattrapage** de janvier 2025 à aujourd'hui, limité par le pool `snowflake` ;
4. un DAG de transformation **déclenché par la donnée** qui produit une table comparant, mois par
   mois, taxis jaunes et taxis verts (nombre de courses, montant médian, distance médiane) ;
5. un **rappel d'échec** branché sur toutes les tâches ;
6. des **tests** : import, structure, et au moins un test de logique avec un faux hook.

Vous choisissez comment factoriser le code : un module partagé paramétré par le type de taxi, ou
un module par type. **Justifiez ce choix** dans le README.

### Ce qui n'est pas fourni

Aucun squelette. Vous décidez des noms, de la structure du code, des tâches et de leur ordre.

### Livrables (17 h 30)

- votre atelier poussé sur votre dépôt GitHub : DAG, `plugins/`, `tests/`, script SQL de la table ;
- un README : ce que fait le pipeline, comment le lancer, vos choix et leurs raisons, ce que vous
  n'avez pas eu le temps de faire ;
- **aucun secret** dans le dépôt (vérifiez `git status` avant de pousser).

### Critères de réussite

| Critère | Comment on le vérifie |
|---|---|
| Le pipeline tourne de bout en bout | les exécutions de janvier à aujourd'hui sont en succès ; `RAW.GREEN_TRIPS` contient les bons volumes |
| Il attend sans bloquer | un mois pas encore publié met le capteur en `deferred` |
| Il est idempotent | relancer un mois ne change pas son nombre de lignes |
| Il ne travaille pas pour rien | un mois inchangé passe par la branche « déjà à jour » |
| La transformation dépend de la donnée | elle démarre après un chargement, et pas après un « déjà à jour » |
| Les échecs sont visibles | une panne provoquée produit une alerte avec la période et le lien vers les logs |
| Les tests passent | `pytest` vert, dont au moins un test de logique sans Snowflake |
| Aucun secret n'est versionné | `.env` et `secrets/` absents du dépôt |

---

## 6. Auto-évaluation de la semaine

- [ ] Je sais régler les reprises selon qu'une erreur est passagère, attendue ou définitive.
- [ ] Mes alertes donnent la période, l'erreur et le lien vers les logs.
- [ ] Mes tests détectent une erreur d'import et une structure inattendue en une seconde.
- [ ] Je sais tester une fonction qui parle à Snowflake sans Snowflake.
- [ ] Je sais rejouer uniquement la tâche qui a échoué (*Clear*).
- [ ] Je sais transposer le pipeline à une nouvelle source sans recopier aveuglément.

## 7. Et après : le brief NYC-Taxi

Le brief [NYC-Taxi-Orchestration — variante A](../../99-Brief/Data-Engineer/NYC-Taxi-Orchestration/VARIANTE_A_SNOWFLAKE_DBT_AIRFLOW.md)
reprend ce pipeline et y ajoute **dbt** pour les transformations, une question métier à laquelle
répondre, et le traitement documenté du changement de schéma. Tout ce que vous avez construit
cette semaine en est le socle.

## 8. Pour aller plus loin

- Tester ses DAG : https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#testing-a-dag
- Rappels : https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/callbacks.html
- Alertes d'échéance : https://airflow.apache.org/docs/apache-airflow/stable/howto/deadline-alerts.html
