# Ressources — parcours d'apprentissage par jour

Les liens de chaque jour. Ce qu'il faut en faire, et dans quel ordre, est dans `GUIDE_BRIEF_GOUVERNANCE.md`. Les vidéos en anglais ont des sous-titres automatiques français sur YouTube (Paramètres → Sous-titres → Traduire automatiquement).

## Kit de démarrage

- Le kit : à parcourir sur https://github.com/gsoulat/formation-data-IA/tree/main/99-Brief/Data-Engineer/Snowflake/Snowflake+Gouvernance/starter-kit ; pour l'installer, voir l'étape 0 de `GUIDE_BRIEF_GOUVERNANCE.md`

## Avant le premier jour

Préparer (étape 0 du guide) :
- Créer un compte d'essai Snowflake, en édition Enterprise : https://signup.snowflake.com/

Regarder :
- Vidéo (FR) — RGPD : Qu'est-ce qu'une donnée personnelle ?, Leto : https://www.youtube.com/watch?v=muSdwpDrYEY
- Vidéo (EN) — Snowflake Horizon Demo For Data Engineers, Snowflake Inc. : https://www.youtube.com/watch?v=MdZ1PaJWH2w

Lire :
- CNIL, définition d'une donnée personnelle : https://www.cnil.fr/fr/definition/donnee-personnelle

## Jour 1 — matin : la veille réglementaire

Textes de référence :
- Le RGPD, texte officiel au Journal officiel de l'Union européenne (EUR-Lex) : https://eur-lex.europa.eu/legal-content/FR/TXT/?uri=CELEX:32016R0679
- Le RGPD article par article, présenté par la CNIL : https://www.cnil.fr/fr/reglement-europeen-protection-donnees
- Comité européen de la protection des données (CEPD), lignes directrices 3/2018 sur le champ d'application territorial : https://www.edpb.europa.eu/our-work-tools/our-documents/guidelines/guidelines-32018-territorial-scope-gdpr-article-3-version_fr

Recommandations de la CNIL :
- Référentiel relatif à la gestion du personnel (2019, PDF) : https://www.cnil.fr/sites/cnil/files/atoms/files/referentiel_grh_novembre_2019_0.pdf
- Les durées de conservation des données : https://www.cnil.fr/fr/les-durees-de-conservation-des-donnees
- Les bases légales d'un traitement : https://www.cnil.fr/fr/les-bases-legales
- Sécurité des données : https://www.cnil.fr/fr/securite-des-donnees

Pour suivre l'actualité (dispositif de veille) :
- Actualités de la CNIL : https://www.cnil.fr/fr/actualites
- Flux RSS de la CNIL, à brancher dans un lecteur de flux : https://www.cnil.fr/fr/rss.xml
- Actualités du CEPD : https://edpb.europa.eu/news/news_fr

## Jour 1 — après-midi : charger et cataloguer

Guide à suivre en premier (FR) :
- Authentification et gouvernance des données, section 5.3 (tags, héritage, classification) : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/15-gouvernance.md
- Charger des fichiers dans Snowflake, sections 2 (format de fichier), 3 (stage), 4 (table), 6 (COPY INTO) et 7 (vérifier) : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/11-chargement-stage-copy.md. Ignorez les sections 5 et 8 (`PUT` et Python) : dans ce brief, les fichiers se déposent sur le stage depuis Snowsight.
- Déposer des fichiers sur un stage depuis Snowsight : https://docs.snowflake.com/en/user-guide/data-load-local-file-system-stage-ui

Documentation officielle Snowflake :
- Tags d'objets (création, valeurs autorisées, héritage, privilèges) : https://docs.snowflake.com/en/user-guide/object-tagging/introduction
- COMMENT (décrire une table ou une colonne) : https://docs.snowflake.com/en/sql-reference/sql/comment
- Fonction TAG_REFERENCES_ALL_COLUMNS (lister les tags d'une table et de ses colonnes) : https://docs.snowflake.com/en/sql-reference/functions/tag_references_all_columns
- INFORMATION_SCHEMA (vues `TABLES` et `COLUMNS`, colonne `comment`) : https://docs.snowflake.com/en/sql-reference/info-schema
- Lignage des données dans Snowsight : https://docs.snowflake.com/en/user-guide/ui-snowsight-lineage
- Privilèges du contrôle d'accès (qui peut créer un tag, qui peut le poser) : https://docs.snowflake.com/en/user-guide/security-access-control-privileges

Vidéos :
- Vidéo (EN) — Creating a Data Classification Process Using Tags in Snowflake, ness-intricity101 : https://www.youtube.com/watch?v=uTQ_3BA3qbc

## Jour 2 — Protéger : qui voit quoi

Guide à suivre en premier (FR) :
- Le même guide, sections 5.1 (masquage dynamique) et 5.2 (politiques d'accès par ligne) : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/15-gouvernance.md
- Rappel sur les rôles et les droits : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/10-securite.md

Documentation officielle Snowflake :
- Sécurité au niveau des colonnes (masquage, comportement avec CREATE TABLE AS SELECT et les vues) : https://docs.snowflake.com/en/user-guide/security-column-intro
- Masquage attaché à un tag : https://docs.snowflake.com/en/user-guide/tag-based-masking-policies
- Politiques d'accès par ligne (dont l'exemple avec une table de correspondance) : https://docs.snowflake.com/en/user-guide/security-row-intro
- Fonction POLICY_REFERENCES (où une politique est-elle attachée ?) : https://docs.snowflake.com/en/sql-reference/functions/policy_references
- INSERT, option OVERWRITE : https://docs.snowflake.com/en/sql-reference/sql/insert
- Les privilèges, objet par objet (qui peut créer un tag, le poser, attacher une politique) : https://docs.snowflake.com/en/user-guide/security-access-control-privileges
- USE SECONDARY ROLES (tester un rôle seul) : https://docs.snowflake.com/en/sql-reference/sql/use-secondary-roles
- ALTER MASKING POLICY (changer le corps d'une politique attachée) : https://docs.snowflake.com/en/sql-reference/sql/alter-masking-policy

Vidéos :
- Vidéo (EN) — Snowflake Data Governance Features - 1 - Data Masking & Row Access, Anupam Kushwah : https://www.youtube.com/watch?v=FTLrAGpXgsQ
- Vidéo (EN) — Protect Sensitive Data in Snowflake with Dynamic Masking, Mastering Snowflake : https://www.youtube.com/watch?v=u4fHBJUMulg
- Vidéo (EN) — Tag Based Dynamic Data Masking In Snowflake, Data Engineering Simplified : https://www.youtube.com/watch?v=80l8943gGk0
- Vidéo (EN) — Snowflake Row-level Security In-depth explanation, Knowledge Amplifier : https://www.youtube.com/watch?v=hUNWmJG0OkY

## Jour 3 — Conserver, contrôler, auditer, présenter

Guides à suivre en premier (FR) :
- Stockage et protection des données, sections 4 (Time Travel) et 5 (Fail-safe) : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/13-stockage-protection.md
- Gouvernance, section 6 (auditer : `ACCOUNT_USAGE`, `ACCESS_HISTORY`, latences) : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/15-gouvernance.md
- Transformer dans Snowflake, section 7 (tâches planifiées) : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/18-transformation.md

Documentation officielle :
- Time Travel (durée de rétention, clause AT) : https://docs.snowflake.com/en/user-guide/data-time-travel
- Fail-safe : https://docs.snowflake.com/en/user-guide/data-failsafe
- REMOVE (retirer un fichier d'un stage) : https://docs.snowflake.com/en/sql-reference/sql/remove
- Vue ACCESS_HISTORY : https://docs.snowflake.com/en/sql-reference/account-usage/access_history
- Vue QUERY_HISTORY (le rôle de chaque requête) : https://docs.snowflake.com/en/sql-reference/account-usage/query_history
- Les tâches et les graphes de tâches : https://docs.snowflake.com/en/user-guide/tasks-intro et https://docs.snowflake.com/en/user-guide/tasks-graphs
- CREATE TASK et EXECUTE TASK : https://docs.snowflake.com/en/sql-reference/sql/create-task et https://docs.snowflake.com/en/sql-reference/sql/execute-task
- TASK_HISTORY (l'historique des exécutions) : https://docs.snowflake.com/en/sql-reference/functions/task_history
- Lever une erreur dans un script (RAISE) : https://docs.snowflake.com/en/developer-guide/snowflake-scripting/exceptions

Réglementation :
- CNIL, les durées de conservation des données : https://www.cnil.fr/fr/les-durees-de-conservation-des-donnees
- CNIL, le registre des activités de traitement (trame complète) : https://www.cnil.fr/fr/RGPD-le-registre-des-activites-de-traitement
- Vidéo (FR) — Comment déterminer la durée de conservation d'une donnée personnelle ?, Leto : https://www.youtube.com/watch?v=idQwBOcYcbI

## Bonus

- Bonus 1, classification automatique : https://docs.snowflake.com/en/user-guide/classify-intro et la procédure `SYSTEM$CLASSIFY` https://docs.snowflake.com/en/sql-reference/stored-procedures/system_classify (elle consomme des crédits)
- Bonus 2, alertes : https://docs.snowflake.com/en/user-guide/alerts
- Bonus 3, politiques d'agrégation : https://docs.snowflake.com/en/user-guide/aggregation-policies

## À savoir

- Les fonctions de mesure de la qualité intégrées à Snowflake (*data metric functions*) ne sont pas disponibles sur un compte d'essai : les règles de qualité de ce brief s'écrivent en SQL et s'exécutent dans une tâche planifiée.
- La propagation automatique des tags existe (https://docs.snowflake.com/en/user-guide/object-tagging/propagation) mais n'est pas demandée : comprenez d'abord ce qui se passe sans elle.
