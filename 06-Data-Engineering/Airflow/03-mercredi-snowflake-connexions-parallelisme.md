# 03 — Mercredi : Snowflake, connexions et parallélisme

> 🎬 **Le fil rouge.** Vos fichiers Parquet s'empilent dans `data/`. L'équipe d'analyse, elle,
> travaille dans Snowflake. Aujourd'hui, le pipeline charge chaque mois dans l'entrepôt — sans
> mot de passe dans le code, sans doublon si on le relance, et sans faire exploser la facture.

| | |
|---|---|
| **Matin** | Snowflake en une heure · compte d'essai · clé RSA · connexions et variables Airflow |
| **Après-midi** | `PUT` + `COPY INTO` idempotent · évolution de schéma · rattrapage parallèle avec `.expand()` et un pool |
| **Point de départ** | [`atelier/exercices/mercredi_chargement.py`](atelier/exercices/mercredi_chargement.py) |

---

## Objectifs

1. Créer un compte d'essai Snowflake et le protéger contre la surconsommation.
2. Authentifier Airflow par clé RSA, avec un utilisateur de service au moindre privilège.
3. Déclarer une connexion sans jamais écrire de secret dans le code.
4. Charger un fichier Parquet dans Snowflake de façon idempotente.
5. Paralléliser un rattrapage sans saturer l'entrepôt.

---

## 1. Snowflake en une heure

Snowflake est un entrepôt de données **dans le cloud** qui sépare le stockage et le calcul :

| Notion | Ce que c'est | Ce qui est facturé |
|---|---|---|
| **Base** / **schéma** / **table** | l'organisation des données, comme dans Postgres | le stockage (quelques dollars par To et par mois) |
| **Entrepôt** (*warehouse*) | la puissance de calcul qui exécute les requêtes. Rien à voir avec un « entrepôt de données » : c'est un groupe de machines. | des **crédits**, à la seconde, **uniquement quand il tourne** (60 s minimum à chaque démarrage) |
| **Stage** | une zone de dépôt de fichiers avant chargement. Interne (géré par Snowflake) ou externe (un bucket S3, GCS, Azure). | le stockage des fichiers |
| **Rôle** | un ensemble de droits. On donne des droits aux rôles, et des rôles aux utilisateurs. | — |

Un entrepôt `X-SMALL` consomme **1 crédit par heure** de fonctionnement ; chaque taille au-dessus
double la consommation. Tout le cours tient largement dans un `X-SMALL`.

> ⚠️ **Le réglage qui protège votre essai gratuit : `AUTO_SUSPEND = 60`.** L'entrepôt s'éteint
> 60 secondes après la dernière requête et se rallume tout seul à la suivante
> (`AUTO_RESUME = TRUE`). Un entrepôt oublié allumé une nuit entière consomme 8 à 10 crédits pour
> rien.

### Créer le compte d'essai

1. Inscrivez-vous sur https://signup.snowflake.com. Choisissez l'édition **Enterprise**, le cloud
   **AWS** et une **région européenne** (Francfort, Irlande, Paris…).
2. L'essai dure **30 jours**, avec un crédit gratuit affiché dans Snowsight
   (*Admin › Cost Management*). Aucune carte bancaire n'est demandée.
3. Notez l'**identifiant du compte** : Snowsight › menu du compte (en bas à gauche) ›
   *Account details* › **Account identifier**, au format `ORGANISATION-COMPTE`.

### Générer la paire de clés de l'utilisateur de service

Airflow est un **programme**, pas une personne : il ne peut pas taper un code d'authentification
à deux facteurs. Snowflake refuse de plus en plus les connexions par simple mot de passe ; la
méthode normale pour un programme est un **utilisateur de service authentifié par clé RSA**.

```bash
cd atelier/secrets
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
chmod 600 rsa_key.p8

# La clé publique sur une seule ligne, à coller dans le script SQL :
grep -v -- "-----" rsa_key.pub | tr -d '\n'
```

| Fichier | Où il va | Secret ? |
|---|---|---|
| `rsa_key.p8` (clé **privée**) | reste dans `secrets/`, lu par Airflow | **oui** — jamais commitée, jamais envoyée |
| `rsa_key.pub` (clé **publique**) | copiée dans Snowflake (`RSA_PUBLIC_KEY`) | non |

> 💡 `-nocrypt` crée une clé sans phrase de passe : acceptable en local pour un cours. En
> production, on chiffre la clé et on met la phrase de passe dans le champ *Password* de la
> connexion Airflow.

### Installer les objets Snowflake

Ouvrez [`atelier/snowflake/01_installation.sql`](atelier/snowflake/01_installation.sql), remplacez
`<CLE_PUBLIQUE>` par votre clé sur une ligne, puis exécutez **tout le script** dans une feuille de
calcul Snowsight. Lisez-le avant : chaque bloc est commenté.

| Bloc | Ce qu'il crée | Pourquoi |
|---|---|---|
| 1 | moniteur de ressources `RM_FORMATION` (10 crédits/mois) | coupe l'entrepôt au-delà : un garde-fou financier |
| 2 | entrepôt `WH_AIRFLOW` (`X-SMALL`, `AUTO_SUSPEND = 60`) | le calcul d'Airflow, séparé de celui des analystes |
| 3 | base `NYC_TAXI`, schémas `RAW` et `MARTS` | `RAW` = la donnée telle que publiée ; `MARTS` = les tables calculées |
| 4 | rôle `ROLE_AIRFLOW` | le **strict nécessaire** : utiliser l'entrepôt, créer des tables dans deux schémas |
| 5 | utilisateur `AIRFLOW_SVC` de `TYPE = SERVICE` | pas de mot de passe, pas d'interface, uniquement la clé |
| 6 | stage `TLC_STAGE`, tables `YELLOW_TRIPS` et `LOAD_LOG` | créés **par** le rôle d'Airflow, qui en est donc propriétaire |

À la fin de la formation : [`99_destruction.sql`](atelier/snowflake/99_destruction.sql).

---

## 2. Connexions et variables Airflow

Une **connexion** regroupe tout ce qu'il faut pour joindre un système : type, hôte, identifiant,
secret, options. Les tâches ne la lisent pas en clair : elles demandent `snowflake_default` et
Airflow fournit le reste.

| Où la déclarer | Comment | Quand |
|---|---|---|
| **Variable d'environnement** `AIRFLOW_CONN_<ID>` | dans `.env`, au format JSON | **ce cours** : versionnable sans secret (la clé est dans un fichier à part), identique sur tous les postes |
| Interface › *Admin › Connections* | formulaire | essais rapides. Stockée dans la base, chiffrée par la `FERNET_KEY` |
| Gestionnaire de secrets (*secrets backend*) | Vault, AWS Secrets Manager… | production |

Dans `atelier/.env` :

```bash
AIRFLOW_CONN_SNOWFLAKE_DEFAULT='{"conn_type": "snowflake", "login": "AIRFLOW_SVC", "schema": "RAW",
  "extra": {"account": "ORGANISATION-COMPTE", "warehouse": "WH_AIRFLOW", "database": "NYC_TAXI",
            "role": "ROLE_AIRFLOW", "private_key_file": "/opt/airflow/secrets/rsa_key.p8"}}'
```

(sur **une seule ligne** dans le fichier). Puis `docker compose up -d` pour recharger
l'environnement, et vérifiez :

```bash
docker compose exec airflow-scheduler airflow connections get snowflake_default
docker compose exec airflow-scheduler python -c "
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook
print(SnowflakeHook().get_first('SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE()'))"
```

> ⚠️ Une connexion déclarée par variable d'environnement **n'apparaît pas** dans la liste de
> l'interface. Ce n'est pas un bug : elle n'est pas stockée dans la base.

Une **variable** Airflow est une valeur de configuration (un chemin, un seuil, une URL de webhook) :

```python
from airflow.sdk import Variable

@task
def alerter():
    url = Variable.get("ALERTE_WEBHOOK", default=None)   # DANS une tâche, jamais au niveau du module
```

---

## 3. Charger un mois dans Snowflake, de façon idempotente

### Le chemin d'un fichier

```
data/yellow/yellow_tripdata_2025-01.parquet
        │  PUT  (le connecteur envoie le fichier)
        ▼
@RAW.TLC_STAGE/2025-01/yellow_tripdata_2025-01.parquet
        │  COPY INTO  (Snowflake lit le Parquet et insère les lignes)
        ▼
RAW.YELLOW_TRIPS
```

### Le code

```python
from airflow.providers.snowflake.hooks.snowflake import SnowflakeHook

def charger_mois(hook, fichier: dict) -> dict:
    mois = fichier["mois"]
    source = f"{mois}/yellow_tripdata_{mois}.parquet"

    # 1. Déposer le fichier dans le stage (PUT n'est pas transactionnel)
    hook.run(f"PUT 'file://{fichier['chemin']}' @RAW.TLC_STAGE/{mois}/ "
             "OVERWRITE = TRUE AUTO_COMPRESS = FALSE")

    # 2. Supprimer puis recharger le mois, dans UNE transaction
    hook.run([
        f"DELETE FROM RAW.YELLOW_TRIPS WHERE SOURCE_FILE = '{source}'",
        f"""COPY INTO RAW.YELLOW_TRIPS
            FROM @RAW.TLC_STAGE/{mois}/
            FILE_FORMAT = (TYPE = PARQUET USE_LOGICAL_TYPE = TRUE)
            MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
            INCLUDE_METADATA = (SOURCE_FILE = METADATA$FILENAME, LOADED_AT = METADATA$START_SCAN_TIME)
            FORCE = TRUE
            ON_ERROR = ABORT_STATEMENT""",
    ], autocommit=False)

    # 3. Contrôler : autant de lignes dans Snowflake que dans le fichier
    charge = hook.get_first(f"SELECT COUNT(*) FROM RAW.YELLOW_TRIPS WHERE SOURCE_FILE = '{source}'")[0]
    if charge != fichier["nb_lignes"]:
        raise ValueError(f"{mois} : {charge} lignes chargées pour {fichier['nb_lignes']}")
    return {"mois": mois, "nb_lignes": charge}
```

| Option | Pourquoi |
|---|---|
| `DELETE` puis `COPY` avec `autocommit=False` | les deux dans une transaction : si le `COPY` échoue, le `DELETE` est annulé. Relancer un mois donne toujours **une** copie du mois, jamais zéro ni deux. |
| `FORCE = TRUE` | Snowflake mémorise les fichiers déjà chargés (64 jours) et les ignore par défaut. Comme on vient de supprimer le mois, on **veut** le recharger. |
| `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE` | associe les colonnes par **nom**, pas par position. Le fichier dit `Airport_fee`, la table `AIRPORT_FEE` : ça marche. |
| `USE_LOGICAL_TYPE = TRUE` | lit les dates Parquet comme des dates, et non comme de grands entiers |
| `INCLUDE_METADATA` | ajoute le fichier d'origine et l'heure de chargement à chaque ligne : c'est ce qui permet le `DELETE` ciblé |
| `ON_ERROR = ABORT_STATEMENT` | une seule ligne illisible fait échouer le chargement. On préfère un échec visible à des lignes silencieusement perdues. |

### Le schéma change : `ENABLE_SCHEMA_EVOLUTION`

La TLC ajoute des colonnes au fil du temps :

| Fichiers | Colonnes |
|---|---|
| jusqu'à décembre 2024 | 19 colonnes |
| à partir de janvier 2025 | + `cbd_congestion_fee` (péage urbain de Manhattan) |
| 2026 | + `request_source` |

La table est créée avec `ENABLE_SCHEMA_EVOLUTION = TRUE` : quand `COPY INTO` rencontre une colonne
nouvelle, **il l'ajoute à la table**. Chargez décembre 2024 puis janvier 2025, et regardez la
table grandir :

```sql
SELECT COLUMN_NAME, DATA_TYPE FROM NYC_TAXI.INFORMATION_SCHEMA.COLUMNS
WHERE TABLE_NAME = 'YELLOW_TRIPS' ORDER BY ORDINAL_POSITION;
```

> 🧭 **Question à se poser** : une colonne ajoutée automatiquement est pratique… et dangereuse. Si
> la source renomme une colonne, vous obtenez une colonne vide de plus, sans erreur. Comment le
> détecteriez-vous ? (Piste : vendredi, les tests.)

---

## 4. Rattraper plusieurs mois en parallèle

### Le mapping dynamique : `.expand()`

On ne sait pas à l'avance combien de mois il faudra rattraper. `.expand()` crée **une tâche par
élément d'une liste**, au moment de l'exécution :

```python
@task
def lister_mois(params=None) -> list[str]:
    debut = pendulum.from_format(params["debut"], "YYYY-MM")
    fin = pendulum.from_format(params["fin"], "YYYY-MM")
    return [m.format("YYYY-MM") for m in pendulum.interval(debut, fin).range("months")]

@task(pool="snowflake")
def rattraper(mois: str) -> dict:
    fichier = telecharger_mois(mois)
    try:
        return charger_mois(SnowflakeHook(), fichier)
    finally:
        Path(fichier["chemin"]).unlink(missing_ok=True)

rattraper.expand(mois=lister_mois())
```

Dans la vue Grid, `rattraper` affiche `[6]` : six instances, une par mois, chacune avec ses logs
et ses reprises. Si mars échoue, seul mars est rejoué.

### Limiter la charge : les pools

Six mois, c'est six téléchargements de 60 Mo et six `COPY INTO` en même temps. Un **pool** est un
nombre de places partagé : une tâche du pool ne démarre que s'il reste une place.

```bash
docker compose exec airflow-scheduler airflow pools set snowflake 2 "Chargements Snowflake"
```

Avec `pool="snowflake"`, **jamais plus de deux chargements simultanés**, tous DAG confondus : le
DAG mensuel et le DAG de rattrapage se partagent les deux places.

| Réglage | Limite… |
|---|---|
| `pool="…"` | le nombre de tâches simultanées **toutes exécutions et tous DAG confondus** |
| `max_active_tis_per_dag` | le nombre d'instances simultanées **d'une même tâche** |
| `max_active_runs` (DAG) | le nombre d'**exécutions** simultanées d'un DAG |

### Paramètres d'un déclenchement manuel

```python
from airflow.sdk import Param

@dag(schedule=None, params={
    "debut": Param("2025-01", type="string", pattern=r"^\d{4}-\d{2}$"),
    "fin": Param("2025-03", type="string", pattern=r"^\d{4}-\d{2}$"),
})
```

Au déclenchement (▶ › *Trigger DAG w/ config*), Airflow affiche un formulaire et **refuse** une
valeur qui ne respecte pas le motif.

---

## 5. Étendre l'image : `Dockerfile` plutôt que `_PIP_ADDITIONAL_REQUIREMENTS`

Le provider Snowflake est **déjà** dans l'image officielle. Pour tout autre paquet :

| Méthode | Ce qui se passe | Verdict |
|---|---|---|
| `_PIP_ADDITIONAL_REQUIREMENTS=paquet` dans `.env` | installé à **chaque démarrage** de **chaque** conteneur | essai rapide uniquement |
| `Dockerfile` : `FROM apache/airflow:3.3.2` + `RUN pip install …` | installé **une fois**, à la construction de l'image | la bonne pratique |

```bash
docker compose build && docker compose up -d
```

---

## 6. Atelier (après-midi)

1. Créez le compte d'essai, la paire de clés, exécutez le script d'installation.
2. Déclarez la connexion `snowflake_default` dans `.env` et vérifiez-la (section 2).
3. Écrivez `charger_mois(hook, fichier)` dans `plugins/tlc/chargement.py`.
4. Partez de [`atelier/exercices/mercredi_chargement.py`](atelier/exercices/mercredi_chargement.py) :
   ajoutez à votre DAG du mardi une tâche `charger` limitée par le pool `snowflake`.
5. Rattrapez **décembre 2024 et janvier 2025**. Vérifiez dans Snowsight :
   - le nombre de lignes par `SOURCE_FILE` ;
   - l'apparition de la colonne `CBD_CONGESTION_FEE`, vide pour décembre, remplie pour janvier.
6. **Relancez janvier.** Le nombre de lignes de janvier doit rester **3 475 226**. S'il a doublé,
   votre chargement n'est pas idempotent.
7. Écrivez le DAG `taxi_jaune_rattrapage` (manuel, paramètres `debut` et `fin`, `.expand()`) et
   rattrapez février à juin 2025. Dans la vue Grid, vérifiez qu'il n'y a jamais plus de deux
   instances en cours.

> 💰 **En fin de journée**, dans Snowsight : *Admin › Cost Management*. Combien de crédits avez-vous
> consommés ? L'entrepôt est-il bien suspendu (`SHOW WAREHOUSES`) ?

---

## 7. Auto-évaluation

- [ ] Je sais ce qu'est un entrepôt Snowflake, et ce qui est facturé.
- [ ] Mon entrepôt s'éteint seul (`AUTO_SUSPEND`), et un moniteur de ressources le plafonne.
- [ ] Airflow se connecte avec un utilisateur de service et une clé, pas un mot de passe.
- [ ] Aucun secret n'est dans mon code ni dans mon dépôt Git.
- [ ] Je sais expliquer pourquoi `DELETE` et `COPY INTO` sont dans la même transaction.
- [ ] Je sais pourquoi on utilise `FORCE = TRUE` ici, et ce qui se passerait sans.
- [ ] Je sais ce que fait `ENABLE_SCHEMA_EVOLUTION`, et quel risque il introduit.
- [ ] Je sais distinguer pool, `max_active_tis_per_dag` et `max_active_runs`.
- [ ] Je sais quand utiliser un `Dockerfile` plutôt que `_PIP_ADDITIONAL_REQUIREMENTS`.

## 8. Pour aller plus loin

- Provider Snowflake, connexion : https://airflow.apache.org/docs/apache-airflow-providers-snowflake/stable/connections/snowflake.html
- Snowflake, authentification par clé : https://docs.snowflake.com/en/user-guide/key-pair-auth
- Snowflake, `COPY INTO` : https://docs.snowflake.com/en/sql-reference/sql/copy-into-table
- Snowflake, évolution de schéma : https://docs.snowflake.com/en/user-guide/data-load-schema-evolution
- Mapping dynamique : https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/dynamic-task-mapping.html
- Pools : https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/pools.html

➡️ **Demain : [04 — Capteurs différés, assets et branchement](04-jeudi-capteurs-assets-branchement.md)**
