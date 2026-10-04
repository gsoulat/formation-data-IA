# Les étapes, journée par journée

![Le parcours en cinq journées](docs/parcours.png)

Chaque journée suit le même plan : le guide à suivre d'abord, les étapes, les pièges à éviter, le résultat à obtenir avant de passer à la suite.

---

## Jour 1 — Comprendre le pipeline et créer l'entrepôt Snowflake

**Dossiers de travail** : `docs/`, `snowflake/`
**Guide à suivre d'abord** : [Sécurité Snowflake : rôles, droits et utilisateurs de service](https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/10-securite.md)

### Étapes

1. **Lire le schéma du pipeline** (`docs/architecture.png`) : repérer les sources, les quatre couches et ce que fait chaque outil.
2. **Explorer le fichier de janvier** et remplir la fiche source des trajets, à partir du modèle `docs/FICHE_SOURCE_MODELE.md`.
3. **Suivre le guide** sur son exemple (`SALES_DB`), dans votre compte Snowflake.
4. **Écrire le script SQL qui crée l'entrepôt**, dans `snowflake/` : warehouse, base, schémas, rôle des outils, utilisateur de service.
5. **Générer la paire de clés** et vérifier que l'utilisateur de service se connecte depuis votre poste.

### Coup de pouce

Pour compter les lignes d'un fichier Parquet sans le charger en mémoire :

```bash
pip install duckdb
python3 -c "import duckdb; print(duckdb.sql(\"SELECT COUNT(*) FROM 'yellow_tripdata_2025-01.parquet'\"))"
```

### Pièges à éviter

- Dans Snowsight, le raccourci d'exécution ne lance que l'instruction sous le curseur : utilisez **Run All** pour exécuter tout le script.
- La clé publique se colle sur une seule ligne, sans les lignes `BEGIN` et `END`.
- L'identifiant de compte a la forme `ORGANISATION-COMPTE` : ce n'est pas votre nom d'utilisateur.

### Pour vous guider

Quels droits minimaux faut-il au rôle pour charger RAW et créer des tables et des vues dans les trois autres schémas ?

### Résultat à obtenir

Le test de connexion du guide affiche votre utilisateur de service, son rôle et son warehouse.

---

## Jour 2 — Charger les fichiers dans la couche RAW

**Dossiers de travail** : `snowflake/`, `ingestion/`
**Guide à suivre d'abord** : [Charger des fichiers : format, stage, PUT, COPY INTO](https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/11-chargement-stage-copy.md)

### Étapes

1. **Lire `CONTRAT_RAW.md`** : les tables et les colonnes que votre entrepôt doit contenir, avec leurs noms exacts.
2. **Suivre le guide** sur son exemple.
3. **Créer les formats de fichier, le stage et les deux tables**, avec le rôle des outils.
4. **Charger le fichier de janvier** : l'envoyer sur le stage (`PUT`, depuis Python), puis le copier dans la table (`COPY INTO`).
5. **Relancer le même chargement** et vérifier qu'aucune ligne n'est ajoutée en double.
6. **Écrire un script Python** qui fait ce chargement pour le mois qu'on lui donne, dans `ingestion/`, avec son `requirements.txt`.
7. **Charger la liste des 265 zones.**

### Coup de pouce

Le script a besoin de trois paquets : `requests`, `snowflake-connector-python` et `cryptography`.

### Pièges à éviter

- `PUT` ne fonctionne pas dans Snowsight : il s'exécute depuis Python.
- Créez les objets avec le rôle des outils, pas avec ACCOUNTADMIN : sinon vos outils ne les verront pas.
- Pour vider une table et la recharger, utilisez `TRUNCATE`. Après un `DELETE`, Snowflake considère toujours le fichier comme déjà chargé.
- Un nombre sans décimales arrondit les montants : relisez la section 4 du guide avant de choisir les types.

### Résultat à obtenir

3 475 226 lignes pour janvier, 265 zones, colonnes techniques remplies. Un second chargement de janvier n'ajoute rien.

---

## Jour 3 — Premier pipeline Airflow : automatiser le chargement

**Dossier de travail** : `airflow/`
**Guide à suivre d'abord** : [Airflow 3 avec Astro CLI](https://github.com/gsoulat/formation-data-IA/blob/main/06-Data-Engineering/Airflow/06-Airflow3-Astro/01-airflow3-astro-snowflake.md), sections 1 à 5

### Étapes

1. **Lire les sections 1 à 5 du guide.** Son exemple ne se lance pas tel quel : il se lit, puis se transpose.
2. **Créer le projet Airflow** dans le dossier `airflow/` (commandes dans le `README.md` du kit) et le démarrer.
3. **Donner à Airflow l'accès à Snowflake** sans écrire la clé dans le code ni dans l'image Docker : le fichier `airflow/.env`, créé à partir de `.env.example`.
4. **Prouver la connexion** avec un DAG d'une seule tâche qui exécute `SELECT CURRENT_ROLE()`.
5. **Écrire le DAG de chargement** : vérifier que le fichier du mois existe, le télécharger, l'envoyer sur le stage, le copier dans la table avec les mêmes options qu'au jour 2.
6. **Calculer le nom du fichier** à partir du mois traité par l'exécution, pas à partir de la date du jour.
7. **Activer le DAG** avec son interrupteur et le laisser rejouer janvier, février et mars.

### Pièges à éviter

- Ne cliquez pas sur **Trigger** pour le DAG de chargement : une exécution lancée à la main prend la date du jour, et le fichier de ce mois n'existe pas.
- Après toute modification de `.env`, relancez `astro dev restart`.
- Beaucoup de tutoriels utilisent Airflow 2, dont le code diffère : la section 1 du guide donne les correspondances.
- L'identifiant de connexion utilisé dans votre code est `snowflake_nyc_taxi` (celui de `.env.example`).

### Pour vous guider

Pourquoi la date du jour empêcherait-elle de rejouer un ancien mois ?

### Résultat à obtenir

Trois exécutions réussies : janvier, février et mars.

---

## Jour 4 — Transformer et contrôler les données avec Airflow

**Dossiers de travail** : `airflow/dags/`, `airflow/include/sql/controles/`
**Guide à suivre d'abord** : [Airflow 3 avec Astro CLI](https://github.com/gsoulat/formation-data-IA/blob/main/06-Data-Engineering/Airflow/06-Airflow3-Astro/01-airflow3-astro-snowflake.md), section 6

### Étapes

1. **Lire la section 6 du guide** : fichiers SQL, paramètres, contrôles, groupes de tâches.
2. **Lire les fichiers SQL fournis** (`airflow/include/sql/`) : que fait chaque fichier, quelles tables lit-il, laquelle crée-t-il ?
3. **En déduire l'ordre d'exécution** et l'ajouter au DAG : une tâche par fichier, regroupées par couche.
4. **Brancher le contrôle fourni** (`controles/raw_mois_charge.sql`), puis en écrire au moins deux autres sur ce modèle : trajet en double, trop de trajets écartés.
5. **Faire échouer un contrôle exprès**, en durcissant son seuil, et vérifier que les tâches suivantes ne s'exécutent pas. Remettre ensuite le seuil.
6. **Relancer l'exécution de février** : le nombre de lignes de chaque table doit rester identique.

### Pièges à éviter

- Les trois exécutions de la veille sont déjà terminées : pour que les nouvelles tâches s'exécutent, relancez chaque exécution avec **Clear**.
- Les fichiers qui contiennent plusieurs instructions (`DELETE` puis `INSERT`) demandent l'option `split_statements=True` sur la tâche.
- Pas de relance automatique sur les contrôles (`retries=0`) : sinon la tâche attend plusieurs minutes avant d'échouer.
- Pour tester un fichier SQL dans Snowsight, remplacez d'abord `{{ ds }}` par une date, par exemple `2025-01-01`.

### Résultat à obtenir

Trois exécutions réussies et 10 382 378 trajets valides dans `FCT_TRIPS`.

---

## Jour 5 — Contrôler, documenter et présenter

**Dossiers de travail** : `docs/`, `README.md`

### Étapes

1. **Écrire la requête SQL qui répond à la direction**, et remplir `docs/REPONSE.md` à partir du modèle `docs/REPONSE_MODELE.md`.
2. **Compter vous-mêmes les trajets anormaux** d'un mois et comparer avec la table `MART_DATA_QUALITY`.
3. **Mesurer les crédits consommés** (requête d'exemple dans les ressources, à lancer avec le rôle ACCOUNTADMIN).
4. **Lister les droits du rôle des outils** et prouver qu'il ne peut pas sortir de son périmètre.
5. **Terminer le README et les captures d'écran.**
6. **Préparer puis présenter la démonstration.**

### Piège à éviter

Vos comptages ne tomberont pas exactement sur ceux de `MART_DATA_QUALITY` : chaque trajet n'y reçoit qu'une seule raison de rejet, la première rencontrée. Les règles sont dans `int_trips__flagged.sql`.

### Bonus

- **Bonus 1** : faire envoyer par Airflow un message sur un salon Discord à la fin de chaque exécution, pour dire si elle a réussi ou échoué. L'adresse du webhook est un secret.
- **Bonus 2** : déployer le même pipeline sur Astro (Airflow hébergé, essai gratuit), sans aucun secret dans l'image.

### Résultat à obtenir

Une démonstration de 15 minutes, et un dépôt qu'un autre binôme pourrait relancer.
