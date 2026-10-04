# 10. Sécurité : rôles, droits et utilisateurs de service en SQL

[← Retour au sommaire](README.md) | [← Précédent](09-monitoring.md) | [Suivant →](11-chargement-stage-copy.md)

## Vue d'ensemble

Les chapitres 3 et 8 créent un rôle et lui donnent des droits en cliquant dans l'interface. Ce chapitre reprend le sujet en SQL, de bout en bout : comprendre le modèle de droits de Snowflake, écrire un script d'infrastructure rejouable, créer un utilisateur de service authentifié par paire de clés pour un outil (dbt, Airflow, script Python), vérifier les droits et diagnostiquer les erreurs.

Exemple suivi : la base `SALES_DB` des chapitres précédents, avec deux rôles et un utilisateur de service.

| Objet | Nom | Rôle dans l'exemple |
|---|---|---|
| Warehouse | `SALES_WH` | calcul |
| Base | `SALES_DB` | schémas `RAW_DATA` (données brutes) et `ANALYTICS` (tables d'analyse) |
| Rôle outil | `SALES_ENGINEER` | charge `RAW_DATA`, construit `ANALYTICS` |
| Rôle lecteur | `SALES_ANALYST` | lit `ANALYTICS`, rien d'autre |
| Utilisateur de service | `SALES_ETL_SVC` | identité utilisée par les outils, sans mot de passe |

---

## 1. Le modèle de droits en cinq idées

### 1.1 Un droit se donne à un rôle, jamais à une personne

Snowflake applique un contrôle d'accès par rôles (RBAC) : un **privilège** porte sur un **objet** et se donne à un **rôle** ; le rôle se donne ensuite à un **utilisateur** ou à un autre rôle.

```
privilège (SELECT) ── sur ──> objet (table)
        │
        └── donné à ──> rôle (SALES_ANALYST) ── donné à ──> utilisateur (ALICE)
```

Conséquence pratique : pour savoir ce qu'un utilisateur peut faire, on regarde ses rôles, puis les droits de ces rôles.

### 1.2 Les objets sont emboîtés, et il faut un droit à chaque étage

```
Compte
├── Utilisateurs, Rôles
├── Warehouses
└── Bases de données
    └── Schémas
        └── Tables, vues, stages, formats de fichier...
```

Pour lire une table, un rôle a besoin de **quatre** droits : `USAGE` sur un warehouse, `USAGE` sur la base, `USAGE` sur le schéma, `SELECT` sur la table. S'il en manque un seul, Snowflake répond que l'objet « n'existe pas ou n'est pas autorisé », sans préciser lequel : il ne révèle pas l'existence d'un objet à un rôle qui n'a aucun droit dessus.

### 1.3 Chaque objet a un propriétaire : le rôle qui l'a créé

Le privilège `OWNERSHIP` appartient à un seul rôle, celui qui était actif au moment du `CREATE`. Le propriétaire a tous les droits sur l'objet, peut le supprimer et peut donner des droits dessus aux autres rôles.

C'est la source d'erreur la plus fréquente : une table créée dans une feuille SQL avec le rôle `ACCOUNTADMIN` appartient à `ACCOUNTADMIN`. Le rôle utilisé par l'outil ne la voit pas, ou la voit sans pouvoir la remplacer.

### 1.4 Les rôles forment une hiérarchie

Donner un rôle à un autre rôle (`GRANT ROLE enfant TO ROLE parent`) fait hériter le parent de tous les droits de l'enfant. Snowflake fournit des rôles système déjà organisés ainsi :

```
ACCOUNTADMIN
├── SECURITYADMIN
│   └── USERADMIN
└── SYSADMIN
    └── rôles personnalisés (SALES_ENGINEER, SALES_ANALYST...)

PUBLIC : donné automatiquement à tous les utilisateurs et à tous les rôles
```

| Rôle système | Sert à | À utiliser pour |
|---|---|---|
| `ACCOUNTADMIN` | tout, y compris la facturation | le moins possible : paramétrage du compte, suivi des coûts |
| `SECURITYADMIN` | gérer tous les droits du compte (privilège `MANAGE GRANTS`) | donner ou retirer des droits sur des objets dont on n'est pas propriétaire |
| `USERADMIN` | créer des utilisateurs et des rôles | `CREATE ROLE`, `CREATE USER` |
| `SYSADMIN` | créer des warehouses et des bases | `CREATE WAREHOUSE`, `CREATE DATABASE`, et les droits sur ces objets |
| `PUBLIC` | droits communs à tous | ne rien y mettre de sensible |

Bonne pratique : rattacher chaque rôle personnalisé à `SYSADMIN`. Sans cela, les objets créés par ce rôle échappent aux administrateurs, qui ne peuvent ni les voir ni les gérer.

### 1.5 À un instant donné, une session a un rôle actif

Les droits appliqués à une requête sont ceux du rôle actif (et des rôles dont il hérite). On le choisit avec `USE ROLE`, ou dans le sélecteur de rôle de la feuille SQL.

```sql
SELECT CURRENT_USER(), CURRENT_ROLE(), CURRENT_WAREHOUSE(), CURRENT_DATABASE(), CURRENT_SCHEMA();
```

Deux points à connaître :
- `USE ROLE X` n'est possible que si le rôle `X` a été donné à l'utilisateur, directement ou par héritage.
- Un utilisateur peut avoir des rôles secondaires actifs en plus du rôle principal. Ils comptent pour lire ou écrire, mais un `CREATE` n'est autorisé que par le rôle principal, qui devient propriétaire de l'objet.

---

## 2. Les privilèges utiles par type d'objet

| Objet | Privilège | Permet de |
|---|---|---|
| Warehouse | `USAGE` | exécuter des requêtes dessus |
| Warehouse | `OPERATE` | le démarrer, le suspendre, le reprendre |
| Warehouse | `MONITOR` | voir son activité et sa consommation |
| Base | `USAGE` | « entrer » dans la base (ne donne accès à aucun schéma) |
| Base | `CREATE SCHEMA` | y créer des schémas |
| Schéma | `USAGE` | « entrer » dans le schéma (ne donne accès à aucune table) |
| Schéma | `CREATE TABLE`, `CREATE VIEW`, `CREATE STAGE`, `CREATE FILE FORMAT` | y créer des objets de ce type |
| Table | `SELECT`, `INSERT`, `UPDATE`, `DELETE`, `TRUNCATE` | lire ou modifier les lignes |
| Vue | `SELECT` | lire la vue |
| Stage interne | `READ`, `WRITE` | lire les fichiers déposés, en déposer (`PUT`) |
| Format de fichier | `USAGE` | l'utiliser dans un `COPY INTO` |
| Tous | `ALL PRIVILEGES` | tous les privilèges du type d'objet, sauf `OWNERSHIP` |
| Tous | `OWNERSHIP` | tout, y compris supprimer l'objet et donner des droits dessus |

Il n'existe pas de `SELECT` sur un schéma ou sur une base : le droit de lecture se donne table par table, ou sur toutes les tables d'un schéma (section 4).

`ALL PRIVILEGES` est pratique mais large. Le principe du moindre privilège demande de lister les droits réellement nécessaires : c'est ce que fait le script de la section 3.

---

## 3. Écrire le script d'infrastructure

Un script d'infrastructure se versionne dans Git et doit pouvoir être rejoué sans erreur : chaque création utilise `IF NOT EXISTS`. L'ordre des instructions suit les dépendances : on ne peut pas donner un droit à un rôle qui n'existe pas encore, ni sur un objet pas encore créé.

```
rôles → warehouse → base → schémas → droits → utilisateur → rôle donné à l'utilisateur
```

### 3.1 Les rôles (USERADMIN)

```sql
USE ROLE USERADMIN;

CREATE ROLE IF NOT EXISTS SALES_ENGINEER COMMENT = 'Rôle des outils : chargement et transformations';
CREATE ROLE IF NOT EXISTS SALES_ANALYST  COMMENT = 'Lecture seule sur le schéma ANALYTICS';

-- Rattachement à la hiérarchie : SYSADMIN hérite des deux rôles
GRANT ROLE SALES_ENGINEER TO ROLE SYSADMIN;
GRANT ROLE SALES_ANALYST  TO ROLE SYSADMIN;
```

### 3.2 Les objets (SYSADMIN)

```sql
USE ROLE SYSADMIN;

CREATE WAREHOUSE IF NOT EXISTS SALES_WH
  WAREHOUSE_SIZE = 'XSMALL'
  AUTO_SUSPEND = 60            -- secondes d'inactivité avant suspension
  AUTO_RESUME = TRUE
  INITIALLY_SUSPENDED = TRUE;

CREATE DATABASE IF NOT EXISTS SALES_DB;
CREATE SCHEMA IF NOT EXISTS SALES_DB.RAW_DATA;
CREATE SCHEMA IF NOT EXISTS SALES_DB.ANALYTICS;
```

### 3.3 Les droits du rôle outil

`SYSADMIN` est propriétaire des objets qu'il vient de créer : il peut donc donner des droits dessus.

```sql
-- Calcul
GRANT USAGE, OPERATE ON WAREHOUSE SALES_WH TO ROLE SALES_ENGINEER;

-- Chaîne d'accès : base puis schémas
GRANT USAGE ON DATABASE SALES_DB TO ROLE SALES_ENGINEER;

-- RAW_DATA : y créer tables, stages et formats de fichier pour le chargement
GRANT USAGE, CREATE TABLE, CREATE STAGE, CREATE FILE FORMAT
  ON SCHEMA SALES_DB.RAW_DATA TO ROLE SALES_ENGINEER;

-- ANALYTICS : y créer tables et vues
GRANT USAGE, CREATE TABLE, CREATE VIEW
  ON SCHEMA SALES_DB.ANALYTICS TO ROLE SALES_ENGINEER;

-- Tables déjà présentes dans RAW_DATA et créées par un autre rôle (chapitres 6 et 7)
GRANT SELECT, INSERT ON ALL TABLES IN SCHEMA SALES_DB.RAW_DATA TO ROLE SALES_ENGINEER;
```

`SALES_ENGINEER` sera propriétaire de tout ce qu'il créera lui-même : aucun droit supplémentaire n'est nécessaire sur ses propres tables.

### 3.4 Les droits du rôle lecteur, et les droits futurs

```sql
GRANT USAGE ON WAREHOUSE SALES_WH          TO ROLE SALES_ANALYST;
GRANT USAGE ON DATABASE SALES_DB           TO ROLE SALES_ANALYST;
GRANT USAGE ON SCHEMA SALES_DB.ANALYTICS   TO ROLE SALES_ANALYST;

-- Objets qui existent aujourd'hui
GRANT SELECT ON ALL TABLES IN SCHEMA SALES_DB.ANALYTICS TO ROLE SALES_ANALYST;
GRANT SELECT ON ALL VIEWS  IN SCHEMA SALES_DB.ANALYTICS TO ROLE SALES_ANALYST;

-- Objets qui seront créés plus tard
GRANT SELECT ON FUTURE TABLES IN SCHEMA SALES_DB.ANALYTICS TO ROLE SALES_ANALYST;
GRANT SELECT ON FUTURE VIEWS  IN SCHEMA SALES_DB.ANALYTICS TO ROLE SALES_ANALYST;
```

`ON ALL TABLES` ne couvre que les tables existantes au moment du `GRANT`. `ON FUTURE TABLES` ne couvre que celles créées ensuite. Il faut les deux.

Les droits futurs sont indispensables dès qu'un outil reconstruit ses tables : un `CREATE OR REPLACE TABLE` (ce que fait dbt à chaque exécution) crée une nouvelle table, et les droits donnés directement sur l'ancienne sont perdus. Avec un droit futur, `SALES_ANALYST` retrouve automatiquement son `SELECT`.

### 3.5 L'utilisateur de service

Un outil ne se connecte pas avec le compte d'une personne. On lui crée un utilisateur de type `SERVICE` : il n'a pas de mot de passe, ne peut pas ouvrir l'interface web et s'authentifie par paire de clés (section 5).

```sql
USE ROLE USERADMIN;

CREATE USER IF NOT EXISTS SALES_ETL_SVC
  TYPE = SERVICE
  DEFAULT_ROLE = SALES_ENGINEER
  DEFAULT_WAREHOUSE = SALES_WH
  DEFAULT_NAMESPACE = SALES_DB.RAW_DATA
  RSA_PUBLIC_KEY = '<clé publique sur une seule ligne, voir section 5>'
  COMMENT = 'Compte de service des outils de chargement et de transformation';

GRANT ROLE SALES_ENGINEER TO USER SALES_ETL_SVC;
```

`DEFAULT_ROLE` indique seulement le rôle activé à la connexion : il ne donne pas le rôle. Sans le `GRANT ROLE ... TO USER`, la connexion échoue.

| Type d'utilisateur | Pour qui | Authentification |
|---|---|---|
| `PERSON` (défaut) | un humain | mot de passe avec authentification multifacteur, ou SSO |
| `SERVICE` | un outil, un script, un orchestrateur | paire de clés, OAuth ou jeton d'accès programmatique ; jamais de mot de passe |

### 3.6 Exécuter le script dans Snowsight

- Raccourci `Cmd/Ctrl + Entrée` : exécute **uniquement** l'instruction où se trouve le curseur (ou la sélection).
- Pour tout exécuter : flèche à droite du bouton d'exécution puis **Run All**, ou tout sélectionner (`Cmd/Ctrl + A`) avant de lancer.
- Le rôle affiché en haut de la feuille est le rôle de départ ; les `USE ROLE` du script le remplacent au fil de l'exécution.

Un script exécuté instruction par instruction dans le désordre produit l'erreur « Role ... does not exist or not authorized » : le `GRANT` est parti avant le `CREATE ROLE`.

Sur un compte d'essai, vous êtes seul administrateur : `ACCOUNTADMIN` peut remplacer `USERADMIN` et `SYSADMIN` dans tout le script. Les objets appartiendront alors à `ACCOUNTADMIN`, ce qui fonctionne mais n'est pas la pratique d'un compte d'entreprise. Si `SALES_WH` et `SALES_DB` ont été créés aux chapitres 4 et 5 avec un autre rôle que `SYSADMIN`, exécutez les sections 3.2 à 3.4 avec ce rôle.

---

## 4. Vérifier les droits

### 4.1 Lire ce qui a été donné

```sql
SHOW GRANTS TO ROLE SALES_ENGINEER;                  -- tous les droits du rôle
SHOW GRANTS OF ROLE SALES_ENGINEER;                  -- à qui le rôle est donné
SHOW GRANTS TO USER SALES_ETL_SVC;                   -- les rôles de l'utilisateur
SHOW GRANTS ON SCHEMA SALES_DB.ANALYTICS;            -- qui a quoi sur un objet
SHOW FUTURE GRANTS IN SCHEMA SALES_DB.ANALYTICS;     -- les droits futurs
SHOW ROLES LIKE 'SALES%';                            -- colonne owner : le propriétaire
```

### 4.2 Tester en prenant le rôle

La seule preuve est d'essayer, y compris ce qui doit être refusé.

```sql
USE ROLE SALES_ANALYST;
USE WAREHOUSE SALES_WH;

SELECT COUNT(*) FROM SALES_DB.ANALYTICS.DAILY_SALES;       -- doit réussir (si la table existe)
SELECT COUNT(*) FROM SALES_DB.RAW_DATA.CUSTOMERS;          -- doit échouer : pas de droit sur RAW_DATA
CREATE TABLE SALES_DB.ANALYTICS.TEST (id INT);             -- doit échouer : lecture seule
```

```sql
USE ROLE SALES_ENGINEER;
CREATE TABLE SALES_DB.ANALYTICS.TEST (id INT);             -- doit réussir
DROP TABLE SALES_DB.ANALYTICS.TEST;                        -- doit réussir : le rôle en est propriétaire
CREATE SCHEMA SALES_DB.AUTRE;                              -- doit échouer : pas de CREATE SCHEMA
```

### 4.3 Retirer un droit, changer un propriétaire

```sql
REVOKE INSERT ON ALL TABLES IN SCHEMA SALES_DB.RAW_DATA FROM ROLE SALES_ENGINEER;
REVOKE ROLE SALES_ANALYST FROM USER ALICE;

-- Table créée par erreur avec ACCOUNTADMIN : la rendre au rôle outil
GRANT OWNERSHIP ON TABLE SALES_DB.ANALYTICS.DAILY_SALES
  TO ROLE SALES_ENGINEER COPY CURRENT GRANTS;
```

`COPY CURRENT GRANTS` conserve les droits déjà donnés aux autres rôles lors du changement de propriétaire.

---

## 5. Authentification par paire de clés

### 5.1 Principe

L'outil garde une **clé privée** et signe avec elle un jeton à chaque connexion. Snowflake vérifie la signature avec la **clé publique** enregistrée sur l'utilisateur. Aucun secret ne circule sur le réseau, et la clé publique peut être écrite dans un script sans risque.

### 5.2 Générer la paire (terminal)

```bash
mkdir -p ~/.ssh/snowflake && cd ~/.ssh/snowflake
openssl genrsa 2048 | openssl pkcs8 -topk8 -inform PEM -out rsa_key.p8 -nocrypt
openssl rsa -in rsa_key.p8 -pubout -out rsa_key.pub
chmod 600 rsa_key.p8
```

| Fichier | Contenu | Où il va |
|---|---|---|
| `rsa_key.p8` | clé privée | reste sur le poste ou dans un coffre de secrets ; jamais dans Git, jamais dans une image Docker |
| `rsa_key.pub` | clé publique | dans Snowflake, sur l'utilisateur de service |

### 5.3 Enregistrer la clé publique

Snowflake attend la clé sur une seule ligne, sans les lignes `-----BEGIN PUBLIC KEY-----` et `-----END PUBLIC KEY-----` :

```bash
grep -v "BEGIN\|END" rsa_key.pub | tr -d '\n'; echo
```

Coller le résultat dans le `CREATE USER` (section 3.5), ou sur un utilisateur existant :

```sql
ALTER USER SALES_ETL_SVC SET RSA_PUBLIC_KEY = 'MIIBIjANBgkqh...';
```

### 5.4 Vérifier que la bonne clé est enregistrée

```sql
DESC USER SALES_ETL_SVC;     -- ligne RSA_PUBLIC_KEY_FP : SHA256:xxxxxxxx
```

L'empreinte affichée doit être identique à celle calculée sur le poste :

```bash
openssl rsa -pubin -in rsa_key.pub -outform DER | openssl dgst -sha256 -binary | openssl enc -base64
```

### 5.5 Trouver l'identifiant de compte

Les outils demandent l'identifiant de compte, au format `ORGANISATION-COMPTE`. Ce n'est ni le nom d'utilisateur ni l'URL complète.

```sql
SELECT CURRENT_ORGANIZATION_NAME() || '-' || CURRENT_ACCOUNT_NAME() AS account_identifier;
```

Dans l'interface : menu du profil (en bas à gauche) puis **Account** puis **View account details**, champ **Account identifier**.

### 5.6 Tester la connexion depuis le poste

```bash
python3 -m venv .venv && source .venv/bin/activate
pip install snowflake-connector-python cryptography
```

```python
import os
import snowflake.connector
from cryptography.hazmat.primitives import serialization

with open(os.path.expanduser("~/.ssh/snowflake/rsa_key.p8"), "rb") as f:
    private_key = serialization.load_pem_private_key(f.read(), password=None)

conn = snowflake.connector.connect(
    account="ORGANISATION-COMPTE",
    user="SALES_ETL_SVC",
    private_key=private_key,
    role="SALES_ENGINEER",
    warehouse="SALES_WH",
)
print(conn.cursor().execute("select current_user(), current_role(), current_warehouse()").fetchone())
```

Résultat attendu : `('SALES_ETL_SVC', 'SALES_ENGINEER', 'SALES_WH')`. Ce test valide d'un coup l'identifiant de compte, la clé, le rôle donné à l'utilisateur et le droit sur le warehouse.

### 5.7 Renouveler une clé sans interruption

Un utilisateur accepte deux clés publiques en même temps : on ajoute la nouvelle, on bascule les outils, puis on retire l'ancienne.

```sql
ALTER USER SALES_ETL_SVC SET RSA_PUBLIC_KEY_2 = '<nouvelle clé>';
-- basculer les outils sur la nouvelle clé privée, puis :
ALTER USER SALES_ETL_SVC UNSET RSA_PUBLIC_KEY;
```

---

## 6. Diagnostiquer une erreur de droits

Méthode : identifier le rôle actif, puis remonter la chaîne warehouse → base → schéma → objet.

```sql
SELECT CURRENT_ROLE();
SHOW GRANTS TO ROLE <rôle actif>;
SHOW GRANTS ON <type> <objet>;      -- colonne grantee_name : qui a un droit ; privilège OWNERSHIP : le propriétaire
```

| Message | Cause probable | Correction |
|---|---|---|
| `Role 'X' does not exist or not authorized` | le rôle n'a pas été créé (script exécuté partiellement), ou le rôle actif n'a aucun droit dessus | `SHOW ROLES LIKE 'X'` ; relancer le script en entier |
| `Object 'X' does not exist or not authorized` | il manque un maillon de la chaîne (`USAGE` sur la base ou le schéma, droit sur l'objet), ou l'objet appartient à un autre rôle | `SHOW GRANTS ON ...` à chaque étage ; vérifier le propriétaire |
| `Insufficient privileges to operate on schema 'X'` | pas de `CREATE TABLE` (ou `CREATE VIEW`...) sur le schéma | `GRANT CREATE TABLE ON SCHEMA ...` |
| `Insufficient privileges to operate on table 'X'` | l'outil veut remplacer ou supprimer une table dont son rôle n'est pas propriétaire | `GRANT OWNERSHIP ... COPY CURRENT GRANTS`, ou supprimer la table avec le rôle propriétaire |
| `No active warehouse selected in the current session` | pas de `USAGE` sur le warehouse, ou aucun warehouse par défaut | `GRANT USAGE ON WAREHOUSE ...` ; `DEFAULT_WAREHOUSE` sur l'utilisateur |
| `Role 'X' specified in the connect string is not granted to this user` | `DEFAULT_ROLE` défini mais rôle jamais donné | `GRANT ROLE X TO USER ...` |
| `New public key rejected by current policy. Reason: 'Invalid Public key'` | valeur d'exemple non remplacée, clé tronquée, lignes `BEGIN`/`END` collées | recoller la clé produite par la commande de la section 5.3 |
| `JWT token is invalid` | identifiant de compte au mauvais format, clé privée qui ne correspond pas à la clé publique enregistrée, nom d'utilisateur erroné | comparer les empreintes (section 5.4) ; vérifier l'identifiant (section 5.5) |
| Un lecteur perd l'accès à une table après une exécution de l'outil | la table a été recréée, les droits directs ont disparu | droits futurs (section 3.4) |

---

## 7. Bonnes pratiques

### ✅ À faire
1. Écrire les droits dans un script SQL versionné et rejouable (`IF NOT EXISTS`), plutôt que de cliquer.
2. Un rôle par usage (outil, lecteur), rattaché à `SYSADMIN`.
3. Lister les privilèges nécessaires au lieu de donner `ALL PRIVILEGES`.
4. Un utilisateur de service par outil ou par équipe, avec sa propre paire de clés.
5. Créer les objets avec le rôle qui doit en être propriétaire.
6. Tester chaque rôle, y compris ce qui doit être refusé.

### ❌ À éviter
1. Faire tourner un outil avec `ACCOUNTADMIN`.
2. Donner un privilège directement dans `PUBLIC`.
3. Partager une clé privée entre plusieurs personnes ou la versionner dans Git.
4. Créer des tables à la main avec `ACCOUNTADMIN` dans un schéma géré par un outil.
5. Oublier les droits futurs sur un schéma dont les tables sont reconstruites.

---

## 8. Exercice d'application

Une équipe RH veut un entrepôt `HR_DB` avec deux schémas, `LANDING` et `REPORTING`.

1. Écrire le script qui crée un warehouse `HR_WH` (XS, suspension après 60 s), la base, les deux schémas, un rôle `HR_LOADER` qui charge `LANDING` et construit `REPORTING`, et un rôle `HR_READER` qui lit uniquement `REPORTING`.
2. Créer un utilisateur de service `HR_PIPELINE_SVC` avec une nouvelle paire de clés et lui donner `HR_LOADER`.
3. Prouver par trois requêtes que `HR_READER` ne peut ni lire `LANDING` ni créer de table.
4. Créer une table dans `REPORTING` avec `HR_LOADER`, puis vérifier que `HR_READER` peut la lire sans nouveau `GRANT`.
5. Supprimer tout ce qui a été créé, dans l'ordre inverse des dépendances.

Questions : quel rôle est propriétaire de la table créée à l'étape 4 ? Que se passerait-il si elle avait été créée avec `ACCOUNTADMIN` ? Pourquoi `HR_READER` n'a-t-il pas besoin de `OPERATE` sur le warehouse si `AUTO_RESUME` est activé ?

## ✅ Points de vérification
- [ ] Rôles créés et rattachés à `SYSADMIN`
- [ ] Chaîne `USAGE` complète pour chaque rôle (warehouse, base, schéma)
- [ ] Droits futurs en place sur le schéma lu par le rôle lecteur
- [ ] Utilisateur de service de type `SERVICE` avec clé publique, empreinte vérifiée
- [ ] Test de connexion par clé réussi depuis le poste
- [ ] Tests positifs et négatifs passés pour chaque rôle

## Documentation officielle
- [Vue d'ensemble du contrôle d'accès](https://docs.snowflake.com/en/user-guide/security-access-control-overview)
- [Liste des privilèges par objet](https://docs.snowflake.com/en/user-guide/security-access-control-privileges)
- [Bonnes pratiques de contrôle d'accès](https://docs.snowflake.com/en/user-guide/security-access-control-considerations)
- [GRANT privilèges](https://docs.snowflake.com/en/sql-reference/sql/grant-privilege)
- [CREATE USER](https://docs.snowflake.com/en/sql-reference/sql/create-user)
- [Authentification par paire de clés](https://docs.snowflake.com/en/user-guide/key-pair-auth)
- [Identifiants de compte](https://docs.snowflake.com/en/user-guide/admin-account-identifier)

---

[← Retour au sommaire](README.md)
