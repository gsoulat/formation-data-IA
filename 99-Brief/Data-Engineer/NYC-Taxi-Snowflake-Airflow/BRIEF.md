━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
📁 BRIEF PROJET — DATA ENGINEER

🏷️ Titre : Pipeline médaillon NYC Yellow Taxi : Snowflake et Airflow

📝 Description rapide :
Hudson Cab Partners, opérateur de 180 taxis jaunes à New York, veut arrêter de préparer ses analyses mensuelles à la main dans des notebooks. Vous construisez l'entrepôt Snowflake (rôles, droits, utilisateur de service, couche RAW) et le pipeline Airflow qui charge chaque mois les fichiers publics de la TLC, exécute les transformations SQL fournies dans le bon ordre et contrôle la qualité des données. Objectif : répondre de façon fiable et rejouable à la question « où et quand la demande est-elle la plus forte, et combien rapporte un trajet ? ». Brief guidé en binôme sur 5 jours, centré sur Snowflake et Airflow : chaque journée s'appuie sur un guide pas à pas, la documentation officielle et des vidéos.

🎯 Compétences et niveaux :
  - C2. Cartographier les données disponibles → Niveau 1 (IMITER)
  - C3. Concevoir le cadre technique d'exploitation des données → Niveau 1 (IMITER)
  - C8. Automatiser l'extraction de données → Niveau 2 (ADAPTER)
  - C9. Développer des requêtes SQL d'extraction → Niveau 2 (ADAPTER)
  - C14. Créer un entrepôt de données → Niveau 2 (ADAPTER)
  - C15. Intégrer les ETL → Niveau 2 (ADAPTER)
  - C16. Gérer l'entrepôt de données → Niveau 2 (ADAPTER)

📖 Contexte :

Hudson Cab Partners gère une flotte de 180 taxis jaunes à New York. Chaque mois, Priya, l'unique analyste de l'entreprise, télécharge à la main le fichier Parquet publié par la Taxi and Limousine Commission (TLC), l'ouvre dans un notebook pandas, applique des filtres qu'elle réécrit à chaque fois, puis copie des chiffres dans un tableur pour la direction. Le notebook plante une fois sur deux par manque de mémoire et personne ne sait d'où vient tel chiffre présenté en comité. Quand Priya est absente, il n'y a pas de reporting.

Priya a déjà écrit en SQL ses règles de nettoyage et ses tables d'analyse. Il lui manque tout le reste : un entrepôt où les exécuter, des données chargées de façon fiable, et un outil qui rejoue le tout chaque mois sans elle. La direction vous recrute en tant que Data Engineer avec une question centrale :

« Où et quand la demande de taxis jaunes est-elle la plus forte à New York, et combien rapporte un trajet selon la zone, l'heure et le mode de paiement ? »

Sources de données (toutes publiques, aucune authentification) :

— Trajets yellow taxi, un fichier Parquet par mois, environ 3,5 millions de lignes et 60 Mo chacun, 20 colonnes. Périmètre : janvier, février et mars 2025. URL : https://d37ci6vzurychx.cloudfront.net/trip-data/yellow\_tripdata\_2025-01.parquet (même motif pour 02 et 03). Page officielle : https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page

— Liste des 265 zones TLC, fichier CSV : https://d37ci6vzurychx.cloudfront.net/misc/taxi\_zone\_lookup.csv

— Dictionnaire de données officiel (PDF) : https://www.nyc.gov/assets/tlc/downloads/pdf/data\_dictionary\_trip\_records\_yellow.pdf

Ces données sont réelles et donc imparfaites : distances nulles, montants négatifs, dates d'une autre année dans un fichier mensuel.

Ce qui vous est fourni (kit de démarrage, lien dans les ressources) :

— Les fichiers SQL de Priya, rangés par couche : staging (renommage), intermediate (nettoyage), marts (tables d'analyse), et un contrôle de qualité qui sert de modèle.
— Le fichier `CONTRAT_RAW.md` : les noms de base, de schémas, de tables et de colonnes que ces fichiers SQL attendent.
— Pour Airflow : la liste des dépendances et un exemple de fichier d'environnement.
— Le schéma du pipeline à construire (`docs/architecture.png`), un modèle de fiche source, un script qui vérifie votre poste, un `.gitignore`.

Ce que vous construisez :

— L'entrepôt Snowflake : warehouse, base, un schéma par couche (RAW, STAGING, INTERMEDIATE, MARTS), rôle des outils, utilisateur de service authentifié par paire de clés.
— La couche RAW conforme au contrat : formats de fichier, stage, tables, chargement rejouable.
— Le script Python qui charge un mois, puis le DAG Airflow qui charge, transforme et contrôle.

Contraintes techniques :
— Snowflake en compte d'essai gratuit (30 jours, sans carte bancaire), un seul warehouse de taille XS, suspendu automatiquement après 60 secondes au plus.
— Aucun secret dans Git : authentification par paire de clés pour le script et pour Airflow. Les outils n'utilisent jamais le rôle ACCOUNTADMIN.
— Les fichiers SQL fournis ne sont pas modifiés : c'est votre entrepôt qui respecte le contrat.
— Apache Airflow 3 via Astro CLI, en local avec Docker.
— Pipeline rejouable : relancer un mois déjà traité ne crée aucun doublon.
— Code versionné sur un dépôt GitHub public, avec un README permettant de reproduire l'installation.

Pour démarrer, avant le premier jour :
1. Installer Python 3.12, Docker, Astro CLI et Git. Le brief fonctionne sous macOS, Linux et Windows ; sous Windows, travailler dans WSL (Ubuntu), car les commandes sont celles d'un terminal Linux. Le `README.md` du kit de démarrage détaille l'installation par système.
2. Télécharger le kit de démarrage (lien dans les ressources), le décompresser, en faire votre dépôt GitHub public, puis lancer `bash verifier_poste.sh` : tout doit afficher OK.
3. Créer un compte d'essai Snowflake (édition Enterprise, région européenne) et noter son identifiant de compte, de la forme ORGANISATION-COMPTE.
4. Lire le `README.md` du kit de démarrage : il montre le schéma du pipeline à construire et indique ce qui est fourni, ce qui est à écrire et dans quel dossier se fait chaque journée.

Vocabulaire :
— Warehouse : dans Snowflake, la puissance de calcul qui exécute les requêtes (et non l'entrepôt de données). XS est la plus petite taille.
— Snowsight : l'interface web de Snowflake.
— Stage : zone de dépôt des fichiers dans Snowflake, avant leur copie dans une table.
— Utilisateur de service : compte utilisé par un programme, pas par une personne.
— Couches RAW, STAGING, INTERMEDIATE, MARTS : données brutes, renommées, nettoyées, prêtes à analyser.
— DAG : dans Airflow, un pipeline, c'est-à-dire des tâches et leur ordre. Une exécution (run) traite une période.
— Date logique : la date de la période qu'une exécution traite, différente de la date du jour.
— Rejouable (idempotent) : relancer donne le même résultat, sans doublon.
— Parquet : format de fichier compact qui contient le nom et le type de ses colonnes.
— Privilège, propriétaire : un droit sur un objet ; le rôle qui crée un objet en est propriétaire.
— Clé privée, clé publique : la première reste secrète sur votre poste et prouve votre identité, la seconde se donne à Snowflake.
— Vue, table : une vue est une requête enregistrée, recalculée à chaque lecture ; une table stocke ses lignes.
— Table de faits, dimension : les événements mesurés (les trajets) et ce qui les décrit (zone, date, mode de paiement).
— Opérateur, provider : dans Airflow, un type de tâche prêt à l'emploi et le paquet Python qui le fournit.
— Catchup : la reprise automatique des périodes passées par Airflow.
— Crédit : l'unité de facturation du calcul dans Snowflake.

🧭 Modalités pédagogiques :

Travail en binôme, 5 jours, en autonomie accompagnée. Chaque journée commence par un guide pas à pas sur un exemple voisin (des ventes) : reproduisez-le ou lisez-le en entier, puis transposez-le à nos données. Les ressources donnent ensuite la documentation officielle et des vidéos. Compte Snowflake : au choix, un compte pour le binôme ou un compte chacun ; de même, un utilisateur de service commun ou un par personne avec sa propre clé. Dans tous les cas, une clé privée ne s'envoie ni par messagerie ni par Git. Répartissez-vous pour que chacun touche à Snowflake et à Airflow.

![Le parcours en cinq journées](https://raw.githubusercontent.com/gsoulat/formation-data-IA/main/99-Brief/Data-Engineer/NYC-Taxi-Snowflake-Airflow/starter-kit/docs/parcours.png)

Le détail de chaque étape, avec les pièges à éviter, est dans le fichier `docs/ETAPES.md` du kit de démarrage. Le guide à suivre en premier chaque jour :
— Jour 1, rôles et droits Snowflake : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/10-securite.md
— Jour 2, chargement des fichiers (format, stage, PUT, COPY INTO) : https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/11-chargement-stage-copy.md
— Jours 3 et 4, Airflow 3 avec Astro CLI (sections 1 à 5, puis section 6) : https://github.com/gsoulat/formation-data-IA/blob/main/06-Data-Engineering/Airflow/06-Airflow3-Astro/01-airflow3-astro-snowflake.md

📊 Modalités d'évaluation :

Évaluation en deux volets, par binôme, chaque membre devant être capable d'expliquer l'ensemble.

Démonstration technique (70 %) : 15 minutes de démonstration en direct suivies de 10 minutes de questions. Déroulé attendu : montrer les droits du rôle des outils et un accès refusé hors de son périmètre, montrer les trois exécutions Airflow et le graphe du DAG, relancer un mois et prouver qu'aucun doublon n'apparaît (historique de chargement Snowflake, nombre de lignes inchangé), faire échouer un contrôle et montrer que la suite ne s'exécute pas, exécuter la requête qui répond à la question centrale, présenter les crédits consommés.

Revue de code et d'architecture (30 %) : lecture du dépôt GitHub (structure, lisibilité du SQL et du Python, absence de secrets, README reproductible), du README et de la fiche source. Les questions porteront sur les choix : pourquoi ces droits et pas davantage, pourquoi un stage, pourquoi la date logique, pourquoi cet ordre de tâches, que se passerait-il avec un quatrième mois.

Chaque compétence est validée séparément à partir des critères de performance ci-dessous. Un binôme dont les transformations ne tournent pas dans Airflow mais dont l'entrepôt, les droits et le DAG de chargement sont solides peut valider C14, C16 et C8 ; C15 ne serait pas validée. À l'inverse, un pipeline qui tourne avec ACCOUNTADMIN ou avec un secret dans Git ne valide pas C16.

📦 Livrables attendus :

1. Dépôt GitHub public contenant :
— `README.md` : description du projet, prérequis, instructions d'installation et de lancement pas à pas (Snowflake, ingestion, Airflow), schéma du pipeline fourni et explication du rôle de chaque partie, choix techniques expliqués, auteurs.
— `snowflake/` : scripts SQL d'infrastructure (warehouse, base, schémas, rôle, utilisateur de service), de couche RAW (formats, stage, tables) et vos requêtes de vérification (comptages, anomalies).
— `ingestion/` : script Python de chargement d'un mois, paramétré et rejouable, avec son `requirements.txt`.
— `airflow/` : projet Astro (DAG, fichiers SQL fournis, vos contrôles, `requirements.txt`, `.env.example`).
— `docs/` : fiche source des trajets.
— `.gitignore` excluant clés privées, `.env` et fichiers téléchargés.

2. Captures d'écran dans `docs/` : les trois exécutions Airflow réussies, le graphe du DAG, un contrôle en échec, l'historique de chargement Snowflake, les droits du rôle des outils, le suivi des crédits.

3. Fichier `docs/REPONSE.md` : la requête SQL finale, le top 10 zones × heures et trois phrases d'interprétation pour la direction d'Hudson Cab Partners.

✅ Critères de performance :

C2 — Cartographier les données
— La fiche source des trajets précise format, fréquence, URL, colonnes et codes.
— Le volume réel est mesuré (nombre de lignes, taille du fichier), pas estimé.

C3 — Concevoir le cadre technique
— Le README explique, à partir du schéma fourni, le rôle de chaque couche et de chaque outil.
— Les choix sont expliqués dans le README (stage, warehouse XS, types larges en RAW).

C8 — Automatiser l'extraction
— Un script Python paramétré par le mois télécharge, dépose et charge un fichier.
— Le DAG dérive le fichier de la date logique de l'exécution et prévoit des relances automatiques.
— Relancer un mois déjà chargé ne crée aucune ligne supplémentaire (preuve en démo).

C9 — Requêtes SQL
— Au moins deux contrôles SQL sont écrits, en plus du modèle fourni, et arrêtent le pipeline en cas d'anomalie.
— Les trajets anormaux d'un mois sont comptés et comparés à `MART_DATA_QUALITY`.
— La requête finale répond à la question centrale et son résultat est commenté.

C14 — Créer l'entrepôt
— Warehouse, base, schémas, rôle et utilisateur de service créés par script versionné et rejouable.
— La couche RAW respecte le contrat et accepte les variations de colonnes entre mois.
— Les colonnes techniques tracent le fichier d'origine et la date de chargement.

C15 — Intégrer les ETL
— Le DAG enchaîne chargement, transformations et contrôles dans un ordre justifié.
— Les tâches sont regroupées par couche ; une tâche correspond à un fichier SQL.
— Trois exécutions réussies ; relancer un mois ne change pas le nombre de lignes.

C16 — Gérer l'entrepôt
— Le rôle des outils n'a que les droits nécessaires ; un accès hors périmètre est refusé (preuve).
— Authentification par paire de clés pour tous les outils, aucun secret dans Git ni dans l'image.
— Suspension automatique configurée, crédits consommés mesurés et présentés.

🔗 Ressources : voir le parcours détaillé par jour dans `RESSOURCES.md` (même contenu à coller dans le champ Ressources de Simplonline).
━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━
