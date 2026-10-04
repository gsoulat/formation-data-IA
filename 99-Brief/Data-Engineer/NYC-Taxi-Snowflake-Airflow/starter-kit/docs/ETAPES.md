# Les étapes, journée par journée

![Le parcours en cinq journées](parcours.png)

Le graphique résume le parcours. Le détail de chaque étape, avec les liens des guides et les pièges à éviter, est ci-dessous.

## Jour 1 — Comprendre le pipeline et créer l'entrepôt Snowflake

1. Lire le schéma du pipeline fourni (`docs/architecture.png`) : repérer les sources, les quatre couches et ce que fait chaque outil.
2. Ouvrir le fichier de janvier avec DuckDB ou pandas et remplir la fiche source des trajets, à partir du modèle `docs/FICHE_SOURCE_MODELE.md`.
3. Suivre le guide sur les rôles et les droits Snowflake : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/10-securite.md
4. Écrire le script SQL qui crée l'entrepôt : warehouse, base, schémas, rôle des outils, utilisateur de service.
5. Générer la paire de clés et vérifier que l'utilisateur de service se connecte depuis votre poste.

**Pour vous guider :** quels droits minimaux faut-il au rôle pour charger RAW et créer des tables et des vues dans les trois autres schémas ?

## Jour 2 — Charger les fichiers dans la couche RAW

1. Lire `CONTRAT_RAW.md` : les tables et les colonnes que votre entrepôt doit contenir, avec leurs noms exacts.
2. Suivre le guide de chargement (format de fichier, stage, PUT, COPY INTO) : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/11-chargement-stage-copy.md
3. Créer, avec le rôle des outils, les formats de fichier, le stage et les deux tables.
4. Charger le fichier de janvier : l'envoyer sur le stage (PUT, depuis Python), puis le copier dans la table (COPY INTO).
5. Relancer le même chargement et vérifier qu'aucune ligne n'est ajoutée en double. Pour vider une table et la recharger, utilisez `TRUNCATE` : après un `DELETE`, Snowflake considère toujours le fichier comme déjà chargé.
6. Écrire un script Python qui fait ce chargement pour le mois qu'on lui donne, puis charger la liste des 265 zones.

**Résultat attendu :** environ 3,47 millions de lignes pour janvier, 265 zones, colonnes techniques remplies.

## Jour 3 — Premier pipeline Airflow : automatiser le chargement

1. Suivre les sections 1 à 5 du guide Airflow 3 : https://github.com/gsoulat/formation-data-IA/blob/main/06-Data-Engineering/Airflow/06-Airflow3-Astro/01-airflow3-astro-snowflake.md
2. Créer le projet Airflow avec Astro dans le dossier `airflow/` du dépôt (les dépendances y sont déjà) et le démarrer.
3. Donner à Airflow l'accès à Snowflake sans écrire la clé dans le code ni dans l'image Docker, puis le prouver avec un DAG d'une seule tâche qui exécute `SELECT CURRENT_ROLE()`.
4. Écrire le DAG de chargement : vérifier que le fichier du mois existe, le télécharger, l'envoyer sur le stage, le copier dans la table avec les mêmes options qu'au jour 2.
5. Calculer le nom du fichier à partir du mois traité par l'exécution, pas à partir de la date du jour.
6. Activer le DAG avec son interrupteur et le laisser rejouer janvier, février et mars : trois exécutions réussies. Ne cliquez pas sur Trigger : une exécution lancée à la main prend la date du jour, et le fichier de ce mois n'existe pas.

**Pour vous guider :** pourquoi la date du jour empêcherait-elle de rejouer un ancien mois ? Attention : beaucoup de tutoriels utilisent Airflow 2, dont le code diffère.

## Jour 4 — Transformer et contrôler les données avec Airflow

1. Suivre la section 6 du guide Airflow 3 (fichiers SQL, paramètres, contrôles, groupes de tâches).
2. Lire les fichiers SQL fournis, déjà rangés dans `airflow/include/sql/` : que fait chaque fichier, quelles tables lit-il, laquelle crée-t-il ?
3. En déduire l'ordre d'exécution et l'ajouter au DAG : une tâche par fichier, regroupées par couche. Les trois exécutions de la veille sont déjà terminées : pour que les nouvelles tâches s'exécutent, relancez chaque exécution avec Clear.
4. Brancher le contrôle fourni (`controles/raw_mois_charge.sql`), puis en écrire au moins deux autres sur ce modèle (trajet en double, trop de trajets écartés). Un contrôle arrête le pipeline si les données sont mauvaises ; pas de relance automatique sur ces tâches.
5. Faire échouer un contrôle exprès, en durcissant son seuil, et vérifier que les tâches suivantes ne s'exécutent pas. Remettre ensuite le seuil.
6. Relancer l'exécution de février : le nombre de lignes de chaque table doit rester identique.

**Résultat attendu :** trois exécutions réussies, 10 382 378 trajets valides dans `FCT_TRIPS`.

## Jour 5 — Contrôler, documenter et présenter

1. Écrire la requête SQL qui répond à la question de la direction.
2. Compter vous-mêmes les trajets anormaux d'un mois et comparer avec la table `MART_DATA_QUALITY`. Les règles sont dans `int_trips__flagged.sql` ; chaque trajet n'y reçoit qu'une seule raison de rejet, la première rencontrée.
3. Mesurer ce que le projet a coûté en crédits Snowflake (requête d'exemple dans les ressources, à lancer avec le rôle ACCOUNTADMIN).
4. Lister les droits du rôle des outils et prouver qu'il ne peut pas sortir de son périmètre.
5. Terminer le README et les captures d'écran, puis préparer et présenter la démonstration.
6. Bonus 1 : faire envoyer par Airflow un message sur un salon Discord à la fin de chaque exécution, pour dire si elle a réussi ou échoué. L'adresse du webhook est un secret.
7. Bonus 2 : déployer le même pipeline sur Astro (Airflow hébergé, essai gratuit), sans aucun secret dans l'image.
