# Brief projet Data Engineer

## 🏷️ Titre

Pipeline médaillon NYC Yellow Taxi : Snowflake et Airflow

## 📝 Description rapide

Hudson Cab Partners, opérateur de 180 taxis jaunes à New York, veut arrêter de préparer ses analyses mensuelles à la main dans des notebooks. Vous construisez l'entrepôt Snowflake (rôles, droits, utilisateur de service, couche RAW) et le pipeline Airflow qui charge chaque mois les fichiers publics de la TLC, exécute les transformations SQL fournies dans le bon ordre et contrôle la qualité des données. Objectif : répondre de façon fiable et rejouable à la question « où et quand la demande est-elle la plus forte, et combien rapporte un trajet ? ». Brief guidé en binôme sur 5 jours, centré sur Snowflake et Airflow : chaque journée s'appuie sur un guide pas à pas, la documentation officielle et des vidéos.

## 🎯 Compétences et niveaux

| Compétence | Niveau |
|---|---|
| C2. Cartographier les données disponibles | 1 (imiter) |
| C3. Concevoir le cadre technique d'exploitation des données | 1 (imiter) |
| C8. Automatiser l'extraction de données | 2 (adapter) |
| C9. Développer des requêtes SQL d'extraction | 2 (adapter) |
| C14. Créer un entrepôt de données | 2 (adapter) |
| C15. Intégrer les ETL | 2 (adapter) |
| C16. Gérer l'entrepôt de données | 2 (adapter) |

## 📖 Contexte

### La situation

Hudson Cab Partners gère une flotte de 180 taxis jaunes à New York. Chaque mois, Priya, l'unique analyste de l'entreprise, télécharge à la main le fichier publié par la Taxi and Limousine Commission (TLC), l'ouvre dans un notebook, applique des filtres qu'elle réécrit à chaque fois, puis copie des chiffres dans un tableur pour la direction. Le notebook plante une fois sur deux par manque de mémoire, et personne ne sait d'où vient tel chiffre présenté en comité. Quand Priya est absente, il n'y a pas de reporting.

Priya a déjà écrit en SQL ses règles de nettoyage et ses tables d'analyse. Il lui manque tout le reste : un entrepôt où les exécuter, des données chargées de façon fiable, et un outil qui rejoue le tout chaque mois sans elle. La direction vous recrute comme Data Engineer.

### La question à laquelle répondre

> Où et quand la demande de taxis jaunes est-elle la plus forte à New York, et combien rapporte un trajet selon la zone, l'heure et le mode de paiement ?

### Ce que vous allez construire

![Schéma du pipeline](starter-kit/docs/architecture.png)

- **L'entrepôt Snowflake** : un warehouse, une base, un schéma par couche (RAW, STAGING, INTERMEDIATE, MARTS), un rôle pour les outils, un utilisateur de service authentifié par paire de clés.
- **La couche RAW** : formats de fichier, stage, tables, chargement rejouable.
- **Le script Python** qui charge un mois de données.
- **Le DAG Airflow** qui charge, transforme et contrôle, mois par mois.

### Les sources de données

Toutes sont publiques, sans authentification. Périmètre : janvier, février et mars 2025.

| Source | Format | Volume | Adresse |
|---|---|---|---|
| Trajets des taxis jaunes | 1 fichier Parquet par mois | environ 3,5 millions de lignes, 60 Mo | [fichier de janvier 2025](https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2025-01.parquet) (même adresse avec `02` et `03`) |
| Liste des zones | 1 fichier CSV | 265 lignes | [taxi_zone_lookup.csv](https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv) |
| Dictionnaire de données | PDF | documentation | [dictionnaire TLC](https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf) |

Ces données sont réelles, donc imparfaites : distances nulles, montants négatifs, dates d'une autre année dans un fichier mensuel.

### Ce qui vous est fourni

Le kit de démarrage (commandes pour le récupérer dans les ressources) contient :

- les fichiers SQL de Priya, rangés par couche, et un contrôle de qualité qui sert de modèle ;
- `CONTRAT_RAW.md` : les noms de base, de schémas, de tables et de colonnes que ces fichiers attendent ;
- `ETAPES.md` : le détail de chaque journée ;
- le schéma du pipeline, un modèle de fiche source, un modèle de réponse ;
- pour Airflow : la liste des dépendances et un exemple de fichier d'environnement ;
- un script qui vérifie votre poste et un `.gitignore`.

### Contraintes techniques

- Snowflake en compte d'essai gratuit (30 jours, sans carte bancaire), un seul warehouse de taille XS, suspendu automatiquement après 60 secondes au plus.
- Aucun secret dans Git : authentification par paire de clés pour le script et pour Airflow. Les outils n'utilisent jamais le rôle ACCOUNTADMIN.
- Les fichiers SQL fournis ne sont pas modifiés : c'est votre entrepôt qui respecte le contrat.
- Apache Airflow 3 via Astro CLI, en local avec Docker.
- Pipeline rejouable : relancer un mois déjà traité ne crée aucun doublon.
- Code versionné sur un dépôt GitHub public, avec un README qui permet de reproduire l'installation.

### Pour démarrer, avant le premier jour

1. Installer Python (3.10 ou plus récent), Docker, Astro CLI et Git. Le brief fonctionne sous macOS, Linux et Windows ; sous Windows, travailler dans WSL (Ubuntu), car les commandes sont celles d'un terminal Linux.
2. Récupérer le kit de démarrage avec les commandes données dans les ressources, et en faire votre dépôt GitHub public.
3. Lancer `bash verifier_poste.sh` dans le kit : tout doit afficher OK.
4. Créer un compte d'essai Snowflake (édition Enterprise, région européenne) et noter son identifiant de compte, de la forme `ORGANISATION-COMPTE`.
5. Lire le `README.md` du kit : il indique l'ordre de lecture des documents.

### Vocabulaire

| Terme | Sens |
|---|---|
| Warehouse | dans Snowflake, la puissance de calcul qui exécute les requêtes (et non l'entrepôt). XS est la plus petite taille |
| Snowsight | l'interface web de Snowflake |
| Stage | zone de dépôt des fichiers dans Snowflake, avant leur copie dans une table |
| Rôle, privilège, propriétaire | un droit se donne à un rôle ; le rôle qui crée un objet en est propriétaire |
| Utilisateur de service | compte utilisé par un programme, pas par une personne |
| Clé privée, clé publique | la première reste secrète sur votre poste, la seconde se donne à Snowflake |
| RAW, STAGING, INTERMEDIATE, MARTS | données brutes, renommées, nettoyées, prêtes à analyser |
| Parquet | format de fichier compact qui contient le nom et le type de ses colonnes |
| Vue, table | une vue est une requête enregistrée ; une table stocke ses lignes |
| Table de faits, dimension | les événements mesurés (les trajets) et ce qui les décrit (zone, date) |
| DAG | dans Airflow, un pipeline : des tâches et leur ordre |
| Exécution (run) | un passage du DAG, qui traite une période |
| Date logique | la date de la période qu'une exécution traite, différente de la date du jour |
| Catchup | la reprise automatique des périodes passées par Airflow |
| Rejouable (idempotent) | relancer donne le même résultat, sans doublon |
| Crédit | l'unité de facturation du calcul dans Snowflake |

## 🧭 Modalités pédagogiques

### Organisation

- **Durée et format** : 5 jours, en binôme, en autonomie accompagnée.
- **Méthode** : chaque journée commence par un guide pas à pas sur un exemple voisin (des ventes). Reproduisez-le ou lisez-le en entier, puis transposez-le à nos données.
- **Compte Snowflake** : au choix, un compte pour le binôme ou un compte chacun ; de même, un utilisateur de service commun ou un par personne avec sa propre clé.
- **Règle d'or** : une clé privée ne s'envoie ni par messagerie ni par Git.
- **Répartition** : chacun doit toucher à Snowflake et à Airflow.

### Le parcours

![Le parcours en cinq journées](starter-kit/docs/parcours.png)

Le détail de chaque étape, avec les pièges à éviter, est dans `ETAPES.md` à la racine du kit de démarrage.

### Jour 1 — Comprendre le pipeline et créer l'entrepôt Snowflake

**Guide du jour** : [Sécurité Snowflake : rôles, droits et utilisateurs de service](https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/10-securite.md)

1. Lire le schéma du pipeline fourni.
2. Explorer le fichier de janvier et remplir la fiche source des trajets.
3. Suivre le guide, puis écrire le script SQL qui crée l'entrepôt.
4. Générer la paire de clés et tester la connexion.

**Résultat à obtenir** : l'utilisateur de service se connecte depuis votre poste avec sa clé.

### Jour 2 — Charger les fichiers dans la couche RAW

**Guide du jour** : [Charger des fichiers : format, stage, PUT, COPY INTO](https://github.com/gsoulat/formation-data-IA/blob/main/04-Cloud-Platforms/snowflake/11-chargement-stage-copy.md)

1. Lire le contrat de la couche RAW, puis suivre le guide.
2. Créer les formats de fichier, le stage et les deux tables.
3. Charger janvier, puis relancer : aucune ligne en double.
4. Écrire le script Python qui charge le mois qu'on lui donne, puis charger les zones.

**Résultat à obtenir** : 3 475 226 lignes pour janvier, 265 zones.

### Jour 3 — Premier pipeline Airflow : automatiser le chargement

**Guide du jour** : [Airflow 3 avec Astro CLI](https://github.com/gsoulat/formation-data-IA/blob/main/06-Data-Engineering/Airflow/06-Airflow3-Astro/01-airflow3-astro-snowflake.md), sections 1 à 5

1. Créer et démarrer le projet Astro.
2. Connecter Airflow à Snowflake sans écrire la clé dans le code, et le prouver.
3. Écrire le DAG de chargement, qui déduit le fichier du mois traité.
4. Activer le DAG : janvier, février et mars sont rejoués.

**Résultat à obtenir** : trois exécutions réussies.

### Jour 4 — Transformer et contrôler les données avec Airflow

**Guide du jour** : le même guide Airflow, section 6

1. Lire les fichiers SQL fournis et en déduire l'ordre d'exécution.
2. Ajouter une tâche par fichier, regroupées par couche.
3. Brancher le contrôle fourni et en écrire au moins deux autres.
4. Faire échouer un contrôle exprès, puis relancer un mois.

**Résultat à obtenir** : 10 382 378 trajets valides dans `FCT_TRIPS`.

### Jour 5 — Contrôler, documenter et présenter

1. Écrire la requête SQL qui répond à la direction.
2. Compter les trajets anormaux et comparer avec `MART_DATA_QUALITY`.
3. Mesurer les crédits consommés et vérifier les droits du rôle.
4. Terminer le README et les captures, puis présenter.

**Bonus** : notification Discord à la fin de chaque exécution ; déploiement sur Astro, l'Airflow hébergé.

## 📊 Modalités d'évaluation

L'évaluation se fait par binôme, en deux volets. Chaque membre doit pouvoir expliquer l'ensemble.

### Démonstration technique (70 %)

15 minutes de démonstration en direct, puis 10 minutes de questions. Déroulé attendu :

1. Montrer les droits du rôle des outils, et un accès refusé hors de son périmètre.
2. Montrer les trois exécutions Airflow et le graphe du DAG.
3. Relancer un mois et prouver qu'aucun doublon n'apparaît.
4. Faire échouer un contrôle et montrer que la suite ne s'exécute pas.
5. Exécuter la requête qui répond à la question centrale.
6. Présenter les crédits consommés.

### Revue de code et d'architecture (30 %)

Lecture du dépôt GitHub : structure, lisibilité du SQL et du Python, absence de secrets, README reproductible, fiche source. Les questions portent sur les choix : pourquoi ces droits et pas davantage, pourquoi un stage, pourquoi la date logique, pourquoi cet ordre de tâches, que se passerait-il avec un quatrième mois.

### Validation partielle

Chaque compétence est validée séparément. Un binôme dont les transformations ne tournent pas dans Airflow, mais dont l'entrepôt, les droits et le DAG de chargement sont solides, peut valider C14, C16 et C8 ; C15 ne serait pas validée. À l'inverse, un pipeline qui tourne avec ACCOUNTADMIN ou avec un secret dans Git ne valide pas C16.

## 📦 Livrables attendus

**1. Un dépôt GitHub public**

| Dossier ou fichier | Contenu |
|---|---|
| `README.md` | description, prérequis, installation et lancement pas à pas, schéma fourni et rôle de chaque partie, choix techniques, auteurs |
| `snowflake/` | scripts SQL d'infrastructure, de couche RAW, et vos requêtes de vérification |
| `ingestion/` | script Python de chargement d'un mois, avec son `requirements.txt` |
| `airflow/` | projet Astro : DAG, fichiers SQL fournis, vos contrôles, `requirements.txt`, `.env.example` |
| `docs/` | fiche source des trajets, captures d'écran, `REPONSE.md` |
| `.gitignore` | exclut clés privées, `.env` et fichiers téléchargés |

**2. Les captures d'écran**, dans `docs/` : les trois exécutions réussies, le graphe du DAG, un contrôle en échec, l'historique de chargement Snowflake, les droits du rôle des outils, le suivi des crédits.

**3. Le fichier `docs/REPONSE.md`** : la requête SQL finale, le top 10 zones × heures et trois phrases d'interprétation pour la direction.

## ✅ Critères de performance

### C2 — Cartographier les données

- La fiche source des trajets précise format, fréquence, adresse, colonnes et codes.
- Le volume réel est mesuré (nombre de lignes, taille du fichier), pas estimé.

### C3 — Concevoir le cadre technique

- Le README explique, à partir du schéma fourni, le rôle de chaque couche et de chaque outil.
- Les choix sont expliqués (stage, warehouse XS, types larges en RAW).

### C8 — Automatiser l'extraction

- Un script Python paramétré par le mois télécharge, dépose et charge un fichier.
- Le DAG déduit le fichier de la date logique et prévoit des relances automatiques.
- Relancer un mois déjà chargé ne crée aucune ligne supplémentaire.

### C9 — Requêtes SQL

- Au moins deux contrôles SQL sont écrits, en plus du modèle fourni, et arrêtent le pipeline en cas d'anomalie.
- Les trajets anormaux d'un mois sont comptés et comparés à `MART_DATA_QUALITY`.
- La requête finale répond à la question centrale et son résultat est commenté.

### C14 — Créer l'entrepôt

- Warehouse, base, schémas, rôle et utilisateur de service sont créés par un script versionné et rejouable.
- La couche RAW respecte le contrat et accepte les variations de colonnes entre mois.
- Les colonnes techniques tracent le fichier d'origine et la date de chargement.

### C15 — Intégrer les ETL

- Le DAG enchaîne chargement, transformations et contrôles dans un ordre justifié.
- Une tâche correspond à un fichier SQL ; les tâches sont regroupées par couche.
- Trois exécutions réussies ; relancer un mois ne change pas le nombre de lignes.

### C16 — Gérer l'entrepôt

- Le rôle des outils n'a que les droits nécessaires ; un accès hors périmètre est refusé.
- Authentification par paire de clés pour tous les outils, aucun secret dans Git ni dans l'image.
- Suspension automatique configurée, crédits consommés mesurés et présentés.

## 🔗 Ressources

Voir `RESSOURCES.md` : guides, documentation et vidéos, jour par jour.
