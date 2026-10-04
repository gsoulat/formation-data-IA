# 11. Charger des fichiers en SQL : format de fichier, stage, PUT et COPY INTO

[← Retour au sommaire](README.md) | [← Précédent](10-securite.md)

## Vue d'ensemble

Le chapitre 7 charge des fichiers CSV en cliquant dans l'interface. Ce chapitre fait la même chose en SQL et en Python, de façon rejouable : c'est ce qu'exécute un script d'ingestion ou un orchestrateur comme Airflow.

Exemple suivi : le fichier `Data/ecommerce/orders.csv` de ce dossier, chargé dans `SALES_DB.RAW_DATA.ORDERS_RAW` avec le rôle `SALES_ENGINEER` créé au [chapitre 10](10-securite.md). Les mêmes gestes s'appliquent à un fichier Parquet ; les différences sont signalées à chaque étape.

Le chargement se fait toujours en quatre objets et deux commandes :

```
fichier sur votre poste
      │  PUT            (envoi du fichier)
      ▼
   stage                (zone de dépôt des fichiers dans Snowflake)
      │  COPY INTO      (lecture du fichier selon un format de fichier)
      ▼
   table
```

---

## 1. Avec quel rôle créer les objets

Tous les objets de ce chapitre se créent avec le rôle des outils, pas avec `ACCOUNTADMIN` : le rôle qui crée un objet en devient propriétaire, et un objet créé par `ACCOUNTADMIN` est invisible pour les outils.

```sql
USE ROLE SALES_ENGINEER;
USE WAREHOUSE SALES_WH;
USE SCHEMA SALES_DB.RAW_DATA;
```

Le rôle doit avoir `CREATE TABLE`, `CREATE STAGE` et `CREATE FILE FORMAT` sur le schéma (chapitre 10, section 3.3).

## 2. Le format de fichier : comment lire le fichier

Un format de fichier décrit la structure des fichiers à lire. On le crée une fois et on le réutilise.

### CSV

```sql
CREATE OR REPLACE FILE FORMAT CSV_FF
  TYPE = CSV
  PARSE_HEADER = TRUE
  FIELD_OPTIONALLY_ENCLOSED_BY = '"'
  ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE;
```

| Option | Rôle |
|---|---|
| `PARSE_HEADER = TRUE` | la première ligne contient les noms de colonnes ; indispensable pour charger par nom de colonne |
| `FIELD_OPTIONALLY_ENCLOSED_BY = '"'` | les valeurs peuvent être entre guillemets (`"Dupont, Jean"`) |
| `ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE` | accepte que la table ait plus de colonnes que le fichier (les colonnes techniques de la section 4) |

Sans la troisième option, le chargement échoue avec `Number of columns in file (14) does not match that of the corresponding table (16)`.

### Parquet

```sql
CREATE OR REPLACE FILE FORMAT PARQUET_FF
  TYPE = PARQUET;
```

Un fichier Parquet contient déjà les noms et les types de ses colonnes : aucune option de lecture n'est nécessaire. L'option facultative `USE_VECTORIZED_SCANNER = TRUE` accélère la lecture des gros fichiers.

## 3. Le stage : où déposer les fichiers

Un stage interne est un espace de stockage géré par Snowflake. Il ne nécessite aucun compte chez un fournisseur cloud.

```sql
CREATE STAGE IF NOT EXISTS VENTES_STAGE
  COMMENT = 'Dépôt des fichiers de ventes avant chargement';

LIST @VENTES_STAGE;      -- fichiers présents sur le stage (vide pour l'instant)
```

## 4. La table de destination

```sql
CREATE TABLE IF NOT EXISTS ORDERS_RAW (
  order_id         NUMBER,
  customer_id      NUMBER,
  order_date       DATE,
  required_date    DATE,
  shipped_date     DATE,
  ship_via         VARCHAR,
  freight          FLOAT,
  ship_country     VARCHAR,
  ship_city        VARCHAR,
  order_status     VARCHAR,
  payment_method   VARCHAR,
  discount_amount  FLOAT,
  tax_amount       FLOAT,
  total_amount     FLOAT,
  -- colonnes techniques : d'où vient la ligne, quand a-t-elle été chargée
  _source_file     VARCHAR,
  _loaded_at       TIMESTAMP_NTZ
);
```

Choisir les types d'une table de données brutes :

| Nature de la colonne | Type conseillé | Piège |
|---|---|---|
| identifiant, compteur | `NUMBER` | `NUMBER` sans précision n'a aucune décimale : `12.75` devient `13` |
| montant, distance, mesure | `FLOAT` | ne pas utiliser `NUMBER` seul |
| date et heure sans fuseau | `TIMESTAMP_NTZ` | |
| texte | `VARCHAR` | inutile de fixer une longueur |

Dans une couche de données brutes, on déclare des types larges et on ne laisse pas Snowflake déduire les colonnes à partir d'un seul fichier : d'un fichier à l'autre, une même colonne peut passer d'entier à décimal, ou une colonne peut apparaître. Une table déduite du premier fichier casserait au suivant.

Les deux colonnes techniques n'existent pas dans le fichier : c'est `COPY INTO` qui les remplit (section 6). Elles permettent de répondre à « de quel fichier vient cette ligne ? » et « quand a-t-elle été chargée ? ».

## 5. PUT : envoyer le fichier sur le stage

`PUT` lit un fichier sur la machine qui exécute la commande. Une feuille SQL dans le navigateur n'a pas accès à votre disque : **`PUT` ne fonctionne pas dans Snowsight**. Il faut un programme installé sur le poste, par exemple le connecteur Python.

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install snowflake-connector-python cryptography
```

```python
import os
from pathlib import Path

import snowflake.connector
from cryptography.hazmat.primitives import serialization

cle = serialization.load_pem_private_key(
    Path("~/.ssh/snowflake/rsa_key.p8").expanduser().read_bytes(), password=None
)
conn = snowflake.connector.connect(
    account=os.environ["SNOWFLAKE_ACCOUNT"],      # ORGANISATION-COMPTE
    user="SALES_ETL_SVC",
    private_key=cle,
    role="SALES_ENGINEER",
    warehouse="SALES_WH",
    database="SALES_DB",
    schema="RAW_DATA",
)
fichier = Path("Data/ecommerce/orders.csv").resolve()

with conn.cursor() as cur:
    cur.execute(f"PUT file://{fichier} @VENTES_STAGE AUTO_COMPRESS=FALSE OVERWRITE=FALSE")
    print(cur.fetchone())     # la 7e valeur est le statut : UPLOADED ou SKIPPED
```

| Option | Rôle |
|---|---|
| `AUTO_COMPRESS=FALSE` | garde le fichier tel quel. Par défaut, `PUT` le compresse en gzip et change son nom (`orders.csv.gz`), ce qui est inutile pour un Parquet déjà compressé |
| `OVERWRITE=FALSE` | n'envoie pas de nouveau un fichier déjà présent : le statut vaut alors `SKIPPED` |

Vérifier dans Snowsight : `LIST @SALES_DB.RAW_DATA.VENTES_STAGE;`

## 6. COPY INTO : copier le fichier dans la table

`COPY INTO` s'exécute dans Snowflake : on peut le lancer depuis Snowsight comme depuis Python.

```sql
COPY INTO ORDERS_RAW
  FROM @VENTES_STAGE
  FILES = ('orders.csv')
  FILE_FORMAT = (FORMAT_NAME = CSV_FF)
  MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
  INCLUDE_METADATA = (_source_file = METADATA$FILENAME, _loaded_at = METADATA$START_SCAN_TIME)
  ON_ERROR = ABORT_STATEMENT;
```

| Option | Rôle |
|---|---|
| `FILES = ('...')` | ne charge que ce fichier, pas tout le contenu du stage |
| `FILE_FORMAT = (FORMAT_NAME = ...)` | le format créé à la section 2 |
| `MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE` | associe les colonnes du fichier à celles de la table par leur nom, sans tenir compte des majuscules. Une colonne absente du fichier reste vide dans la table |
| `INCLUDE_METADATA = (...)` | remplit les colonnes techniques avec le nom du fichier et l'heure du chargement. Exige `MATCH_BY_COLUMN_NAME` |
| `ON_ERROR = ABORT_STATEMENT` | à la première ligne illisible, rien n'est chargé. C'est la valeur par défaut, et la plus sûre |

Pour un fichier Parquet, seule la ligne `FILE_FORMAT` change (`FORMAT_NAME = PARQUET_FF`).

### Lire le résultat

`COPY INTO` renvoie une ligne par fichier :

| Colonne | Exemple | Sens |
|---|---|---|
| `file` | `ventes_stage/orders.csv` | fichier traité |
| `status` | `LOADED` | chargé. `LOAD_FAILED` : erreur, voir `first_error` |
| `rows_parsed` / `rows_loaded` | `29` / `29` | lignes lues et lignes chargées |

### Relancer le même chargement

```sql
COPY INTO ORDERS_RAW FROM @VENTES_STAGE FILES = ('orders.csv')
  FILE_FORMAT = (FORMAT_NAME = CSV_FF) MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
  INCLUDE_METADATA = (_source_file = METADATA$FILENAME, _loaded_at = METADATA$START_SCAN_TIME);
```

Le résultat est `Copy executed with 0 files processed` (statut `LOAD_SKIPPED` dans les outils) : Snowflake garde en mémoire, pendant 64 jours, les fichiers déjà chargés dans chaque table et ne les recharge pas. On peut donc relancer un chargement sans créer de doublon. L'option `FORCE = TRUE` désactive cette protection : ne pas l'utiliser.

## 7. Vérifier

```sql
SELECT COUNT(*) FROM ORDERS_RAW;                                   -- nombre de lignes du fichier, hors en-tête
SELECT _source_file, COUNT(*), MIN(_loaded_at) FROM ORDERS_RAW GROUP BY 1;
SELECT * FROM ORDERS_RAW LIMIT 5;                                  -- toutes les colonnes sont-elles remplies ?

-- Historique des chargements de la table : la preuve qu'un fichier n'a été chargé qu'une fois
SELECT file_name, status, row_count, last_load_time
FROM TABLE(INFORMATION_SCHEMA.COPY_HISTORY(
  TABLE_NAME => 'ORDERS_RAW', START_TIME => DATEADD(DAY, -7, CURRENT_TIMESTAMP())));
```

Si une colonne est entièrement vide alors qu'elle est remplie dans le fichier, son nom dans la table ne correspond pas à l'en-tête du fichier.

## 8. Le tout dans un script Python rejouable

```python
def charger(conn, fichier: Path, table: str, format_fichier: str) -> int:
    """Dépose un fichier sur le stage puis le copie dans la table. Rejouable sans doublon."""
    with conn.cursor() as cur:
        cur.execute(f"PUT file://{fichier.resolve()} @VENTES_STAGE AUTO_COMPRESS=FALSE OVERWRITE=FALSE")
        cur.execute(f"""
            COPY INTO {table}
            FROM @VENTES_STAGE
            FILES = ('{fichier.name}')
            FILE_FORMAT = (FORMAT_NAME = {format_fichier})
            MATCH_BY_COLUMN_NAME = CASE_INSENSITIVE
            INCLUDE_METADATA = (_source_file = METADATA$FILENAME, _loaded_at = METADATA$START_SCAN_TIME)
            ON_ERROR = ABORT_STATEMENT
        """)
        lignes = cur.fetchall()
    return sum(int(l[3]) for l in lignes if len(l) > 3 and str(l[1]) == "LOADED")


print(charger(conn, Path("Data/ecommerce/orders.csv"), "ORDERS_RAW", "CSV_FF"), "lignes chargées")
```

Pour charger un fichier publié sur Internet, on le télécharge d'abord sur le disque, par morceaux pour ne pas le garder en mémoire, puis on appelle la même fonction :

```python
import sys

import requests


def telecharger(url: str, dossier: Path = Path("/tmp/telechargements")) -> Path:
    dossier.mkdir(parents=True, exist_ok=True)
    destination = dossier / url.rsplit("/", 1)[-1]
    with requests.get(url, stream=True, timeout=120) as reponse:
        reponse.raise_for_status()                 # arrête tout si le fichier n'existe pas
        with destination.open("wb") as f:
            for morceau in reponse.iter_content(chunk_size=8 * 1024 * 1024):
                f.write(morceau)
    return destination


mois = sys.argv[1]                                 # python charger.py 2025-01
fichier = telecharger(f"https://exemple.org/ventes/ventes_{mois}.csv")
```

`sys.argv[1]` est le premier mot écrit après le nom du script dans le terminal : c'est ce qui rend le script utilisable pour n'importe quel mois.

## 9. Diagnostiquer

| Message | Cause probable | Correction |
|---|---|---|
| `PUT` : erreur de syntaxe ou commande non reconnue dans Snowsight | `PUT` n'existe pas dans l'interface web | l'exécuter depuis le connecteur Python |
| `Remote file '@.../x' was not found` | le fichier n'a pas été déposé, ou son nom diffère (compressé en `.gz` par `PUT`) | `LIST @stage` ; `AUTO_COMPRESS=FALSE` |
| `Number of columns in file (N) does not match that of the corresponding table (M)` | CSV et table avec colonnes techniques | `ERROR_ON_COLUMN_COUNT_MISMATCH = FALSE` dans le format |
| Colonnes vides après chargement | noms de colonnes différents de l'en-tête, ou `PARSE_HEADER` absent | aligner les noms ; recréer le format |
| `Numeric value '...' is not recognized` | type de colonne trop étroit | types larges (section 4) |
| Montants arrondis à l'entier | colonne en `NUMBER` sans décimales | `FLOAT` |
| `File format 'X' does not exist or not authorized` | format créé avec un autre rôle ou dans un autre schéma | le recréer avec le rôle des outils ; nom complet `BASE.SCHEMA.FORMAT` |
| `Copy executed with 0 files processed` | fichier déjà chargé | comportement normal : c'est la protection contre les doublons |
| Après un `DELETE FROM table`, le rechargement répond `0 files processed` et la table reste vide | `DELETE` ne remet pas à zéro la mémoire des fichiers chargés | vider la table avec `TRUNCATE TABLE`, qui efface aussi cette mémoire |
| Le format a été corrigé dans le script mais l'erreur persiste | l'objet n'a pas été recréé dans Snowflake | relancer le `CREATE OR REPLACE FILE FORMAT` |

## 10. Exercice d'application

1. Charger `Data/ecommerce/customers.csv` dans une table `CUSTOMERS_RAW` avec ses deux colonnes techniques.
2. Relancer le chargement et montrer, avec `COPY_HISTORY`, que le fichier n'a été chargé qu'une fois.
3. Ajouter une colonne `segment_b2b BOOLEAN` à la table, puis recharger un fichier qui ne la contient pas : que vaut-elle ?
4. Supprimer la table, le stage et les formats créés pendant l'exercice.

Questions : pourquoi `PUT` a-t-il besoin d'un programme sur votre poste alors que `COPY INTO` fonctionne dans Snowsight ? Que se passerait-il si deux tables différentes chargeaient le même fichier du stage ?

## ✅ Points de vérification
- [ ] Objets créés avec le rôle des outils (colonne `owner` de `SHOW TABLES`, `SHOW STAGES`, `SHOW FILE FORMATS`)
- [ ] Fichier visible avec `LIST @stage`
- [ ] Nombre de lignes de la table égal à celui du fichier
- [ ] Colonnes techniques remplies
- [ ] Second chargement sans aucune ligne ajoutée

## Documentation officielle
- [PUT](https://docs.snowflake.com/en/sql-reference/sql/put)
- [COPY INTO table](https://docs.snowflake.com/en/sql-reference/sql/copy-into-table)
- [CREATE FILE FORMAT](https://docs.snowflake.com/en/sql-reference/sql/create-file-format)
- [CREATE STAGE](https://docs.snowflake.com/en/sql-reference/sql/create-stage)
- [COPY_HISTORY](https://docs.snowflake.com/en/sql-reference/functions/copy_history)
- [Types de données](https://docs.snowflake.com/en/sql-reference/intro-summary-data-types)

---

[← Retour au sommaire](README.md)
