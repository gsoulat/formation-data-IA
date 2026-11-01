# Contrat de gouvernance

Ce document fixe ce qui est imposé : les noms des objets, les besoins d'accès, les durées de conservation et les règles de qualité. La façon de les mettre en œuvre dans Snowflake est à votre charge.

Les décisions de ce contrat ont été prises par la direction de Hudson Cab Partners avec son conseil juridique. Vous les appliquez ; vous ne les réécrivez pas. Si une règle vous paraît inapplicable, écrivez-le dans votre README.

## 1. Les objets imposés

| Objet | Nom | Remarque |
|---|---|---|
| Tables RAW | `NYC_TAXI.RAW.DRIVERS`, `NYC_TAXI.RAW.DRIVER_SHIFTS` | colonnes ci-dessous |
| Schéma de gouvernance | `NYC_TAXI.GOUVERNANCE` | contient les tags, les politiques et les tables de la gouvernance |
| Rôle de gouvernance | `GOUVERNANCE` | propriétaire du schéma, des tags et des politiques ; ne lit pas les données |
| Rôles métier | `ANALYSTE`, `RH_PAIE`, `RESP_DEPOT_QUEENS`, `RESP_DEPOT_BRONX` | voir la matrice des accès |
| Tags | `SENSIBILITE`, `DONNEE_PERSONNELLE`, `DUREE_CONSERVATION` | dans le schéma `GOUVERNANCE` |
| Table de correspondance | `GOUVERNANCE.ACCES_DEPOT` | colonnes `role_name`, `depot` : quel rôle voit quel dépôt |
| Vue du catalogue | `GOUVERNANCE.V_CATALOGUE` | une ligne par colonne cataloguée |
| Résultats de qualité | `GOUVERNANCE.QUALITE_RESULTATS` | colonnes `regle` (texte), `mesure_le` (date et heure), `nb_anomalies` (nombre), `seuil` (nombre à décimales, par exemple `NUMBER(18,2)`), `statut` (texte : `OK` ou `ALERTE`) |
| Tâches planifiées | `MARTS.T_PURGE`, puis `MARTS.T_QUALITE`, puis `MARTS.T_TABLES` | quotidiennes, dans cet ordre : on purge, on contrôle, et on ne reconstruit `MARTS` que si le contrôle est passé |

Le nom des politiques, du stage et des formats de fichier est libre. Le rôle des outils et le warehouse sont ceux créés à l'installation (`snowflake/00_installation.sql`) : `TRANSFORMER` et `NYC_TAXI_WH`.

## 2. Les deux tables RAW

`NYC_TAXI.RAW.DRIVERS` : une ligne par chauffeur, copie fidèle de `data/drivers.csv`.

| Colonne | Nature |
|---|---|
| `driver_id` | texte, identifiant interne (`D0001`) |
| `first_name`, `last_name` | texte |
| `email`, `phone` | texte |
| `birth_date` | date |
| `tlc_license_number` | texte : numéro de licence délivré par la TLC |
| `depot` | texte : dépôt de rattachement |
| `hire_date`, `end_date` | date ; `end_date` vide = chauffeur en poste |
| `_source_file`, `_loaded_at` | colonnes techniques : nom du fichier chargé, date et heure du chargement |

`NYC_TAXI.RAW.DRIVER_SHIFTS` : une ligne par service (une prise de poste), copie fidèle de `data/driver_shifts.csv`.

| Colonne | Nature |
|---|---|
| `shift_id` | texte, identifiant du service (`S000001`) |
| `driver_id` | texte |
| `shift_date` | date |
| `depot` | texte |
| `start_hour` | nombre entier (heure de prise de poste) |
| `hours_worked` | nombre à décimales |
| `trips_count` | nombre entier |
| `revenue_usd` | nombre à décimales |
| `_source_file`, `_loaded_at` | colonnes techniques |

Les fichiers SQL fournis (`snowflake/rh/`) lisent ces deux tables et alimentent `MARTS.DIM_DRIVER` et `MARTS.MART_DRIVER_MONTHLY`, ainsi que le référentiel des dépôts `MARTS.DIM_DEPOT`. **Vous pouvez les modifier** : ils ont été écrits avant que quiconque se pose la question des données personnelles.

## 3. Les valeurs des tags

| Tag | Se pose sur | Valeurs |
|---|---|---|
| `SENSIBILITE` | chaque table cataloguée | `public`, `interne`, `confidentiel` (aucune autre valeur acceptée) |
| `DONNEE_PERSONNELLE` | chaque colonne qui décrit une personne | `nom`, `email`, `telephone`, `date_naissance`, `identifiant_officiel`, `identifiant_interne` |
| `DUREE_CONSERVATION` | chaque table cataloguée | texte libre, par exemple `5 ans après la fin du contrat` |

## 4. La matrice des accès

Les rôles métier ne lisent que le schéma `MARTS`. Personne d'autre que le rôle des outils ne lit `RAW` ni `STAGING`. Les administrateurs (`ACCOUNTADMIN`, `SYSADMIN`) en héritent par la hiérarchie des rôles : ils voient ces tables, mais les colonnes personnelles y sont masquées pour eux.

| Rôle | Qui | Tables du domaine RH | Lignes visibles | Ce qu'il voit en clair |
|---|---|---|---|---|
| `RH_PAIE` | le service paie | oui | tous les dépôts | tout |
| `RESP_DEPOT_QUEENS` | la responsable du dépôt de Queens | oui | dépôt de Queens seulement | nom, prénom, téléphone |
| `RESP_DEPOT_BRONX` | le responsable du dépôt du Bronx | oui | dépôt du Bronx seulement | nom, prénom, téléphone |
| `ANALYSTE` | Priya | oui, et tout le reste de `MARTS` | tous les dépôts | aucune donnée qui identifie directement un chauffeur ; l'année de naissance seulement |
| rôle des outils | le chargement et les tâches planifiées | oui | toutes | ce dont le pipeline a besoin pour fonctionner |
| `GOUVERNANCE` | vous, en tant que responsables des règles | non | aucune | rien |
| `ACCOUNTADMIN` | l'administrateur du compte | | aucune | rien |

Trois précisions :

- « Ne pas voir en clair » ne dit pas comment : une colonne peut être masquée, ou ne pas exister dans la table. À vous de choisir, colonne par colonne, et de le justifier.
- L'identifiant interne `driver_id` reste visible de tous les rôles métier : il permet de compter et de joindre sans nommer.
- Un rôle absent de cette matrice ne voit aucune ligne des tables du domaine RH.
- Les **tables du domaine RH** sont `RAW.DRIVERS`, `RAW.DRIVER_SHIFTS`, `MARTS.DIM_DRIVER` et `MARTS.MART_DRIVER_MONTHLY`. `MARTS.DIM_DEPOT` est un référentiel sans donnée personnelle, lisible par tous les rôles métier, sans filtre de lignes.

## 5. Les durées de conservation

| Règle | Énoncé |
|---|---|
| R1 | Les données d'un chauffeur sont supprimées 5 ans après la fin de son contrat. |
| R2 | Une donnée personnelle supprimée ne doit plus pouvoir être restaurée par Time Travel au-delà de 1 jour. |
| R3 | Le fichier RH ne reste pas sur le stage une fois chargé. |

R1 s'applique partout où la donnée du chauffeur a été copiée, pas seulement à la table où vous la supprimez.

## 6. Les règles de qualité

Chaque règle se mesure sur les tables RAW par une requête qui renvoie le nombre de lignes en anomalie (modèle : `snowflake/rh/controles/licence_unique.sql`).

| Règle | Énoncé | Seuil | En cas de dépassement |
|---|---|---|---|
| `licence_unique` | un numéro de licence n'appartient qu'à un chauffeur | 0 | avertissement |
| `telephone_renseigne` | chaque chauffeur en poste a un téléphone | 5 % des chauffeurs en poste | avertissement |
| `email_valide` | l'e-mail contient un `@` | 0 | avertissement |
| `dates_coherentes` | pas d'embauche dans le futur, pas de fin de contrat avant l'embauche | 0 | avertissement |
| `depot_connu` | le dépôt est écrit exactement `Bronx`, `Brooklyn` ou `Queens` | 0 | avertissement |
| `service_rattache` | chaque service appartient à un chauffeur connu | 50 services | **bloquant** |
| `service_unique` | un identifiant de service n'apparaît qu'une fois | 0 | avertissement |
| `duree_plausible` | un service ne dure pas plus de 16 heures | 0 | avertissement |

Mettez en œuvre la règle fournie et au moins deux autres, dont `service_rattache`.

- **Avertissement** : le résultat est enregistré dans `QUALITE_RESULTATS` avec le statut `ALERTE`, les tâches continuent.
- **Bloquant** : le résultat est enregistré, puis la chaîne s'arrête : `T_TABLES` ne reconstruit pas `MARTS`.
- Une règle respectée est enregistrée avec le statut `OK`. Chaque exécution des tâches ajoute une ligne par règle.

## 7. Vérifier le contrat

```sql
SHOW TAGS IN SCHEMA NYC_TAXI.GOUVERNANCE;
SHOW MASKING POLICIES IN SCHEMA NYC_TAXI.GOUVERNANCE;
SHOW ROW ACCESS POLICIES IN SCHEMA NYC_TAXI.GOUVERNANCE;
SELECT * FROM NYC_TAXI.GOUVERNANCE.ACCES_DEPOT;

-- Où les politiques sont-elles réellement attachées ?
SELECT policy_name, policy_kind, ref_entity_name, ref_column_name, tag_name
FROM TABLE(NYC_TAXI.INFORMATION_SCHEMA.POLICY_REFERENCES(
  REF_ENTITY_NAME => 'NYC_TAXI.MARTS.DIM_DRIVER', REF_ENTITY_DOMAIN => 'TABLE'));
```
