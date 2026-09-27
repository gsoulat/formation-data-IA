# Brief : Maintenir l'entrepôt des prix des carburants — SCD, nouvelle source temps réel et supervision

## Informations

| Critère | Valeur |
|---------|--------|
| **Durée** | 5 jours (35 heures) |
| **Niveau** | Intermédiaire-Avancé |
| **Modalité** | Individuel |
| **Technologies** | PostgreSQL, Python, SQL, schéma en étoile, SCD Type 2, ETL, XML (iterparse), Docker, cron, SMTP de test (MailHog/Mailtrap), Git |
| **Prérequis** | [Cours SQL](../../../01-Fondamentaux/SQL/) + [Cours Python](../../../01-Fondamentaux/Python/) + [Cours Docker](../../../02-Containerisation/Docker/) + [Data Warehouse](../../../05-Databases/DataWarehouse/) |
| **Données** | **100 % réelles** — archive officielle des prix des carburants (386 Mo de XML, 5,3 M de relevés) + flux temps réel |

## Contexte

### L'entreprise

**Rouleo** édite une application mobile de comparaison des prix des carburants, utilisée par environ 900 000 automobilistes. Elle vit de la publicité et d'un abonnement professionnel vendu à des gestionnaires de flottes. L'équipe compte 18 personnes, dont une data analyst, un CTO — et vous, le seul data engineer.

### Le problème

Il y a huit mois, votre prédécesseur a mis en production l'entrepôt des prix : un schéma en étoile sous PostgreSQL, une table de faits `fait_prix` entourée de dimensions station, carburant et temps, initialisé à partir de l'archive annuelle officielle publiée par l'État. Il fonctionne… la plupart du temps. Et c'est précisément le problème.

**Première douleur.** L'ETL met à jour la dimension station **par écrasement**. Or le réseau bouge en permanence : une station est reclassée d'un type de voirie à l'autre, une autre ouvre un service 24/24, une troisième corrige son adresse. Résultat, l'analyse « écart de prix entre autoroute et réseau ordinaire » que la data analyst publie chaque trimestre **change rétroactivement** : une station reclassée en juin fait bouger la moyenne autoroute de janvier. Le CTO a dû retirer un communiqué de presse le mois dernier.

**Deuxième douleur.** L'entrepôt ne connaît que le passé. L'État publie aussi un **flux temps réel** des prix, mis à jour en continu, dans un format totalement différent de l'archive annuelle. L'application, elle, l'interroge en direct — si bien que les prix affichés aux utilisateurs et les prix analysés par la data analyst ne viennent pas de la même chaîne, et divergent régulièrement. La direction veut les réconcilier dans l'entrepôt.

**Troisième douleur.** En avril, le chargement nocturne a planté deux nuits d'affilée. Personne n'a été prévenu. L'application a servi pendant quatre jours des prix périmés à 900 000 utilisateurs, et Rouleo l'a appris par un tweet.

### La question centrale

Une question doit guider chacun de vos choix, et vous devez pouvoir vous y référer à chaque étape :

> **« Comment garantir un entrepôt fiable qui absorbe les évolutions du réseau de stations sans fausser l'historique des prix ? »**

### Les trois demandes

Trois demandes atterrissent dans le même sprint :

- **Demande 1 (data analyst)** : historiser les changements de caractéristiques des stations, pour que les analyses passées restent justes.
- **Demande 2 (direction produit)** : intégrer le flux temps réel comme seconde source d'alimentation et créer un datamart « tension des prix » pour la data analyst, sans casser l'existant.
- **Demande 3 (CTO)** : plus jamais de panne silencieuse — journalisation, alertes, sauvegardes, indicateurs de service et conformité RGPD.

### Les sources de données

Vous n'inventez rien, vous **héritez** — et les données sont réelles.

- **L'existant — archive annuelle des prix des carburants** : `https://donnees.roulez-eco.fr/opendata/annee/2025` (également disponible pour les années précédentes). Une archive ZIP d'environ 32 Mo qui se décompresse en **386 Mo de XML**, contenant **14 420 stations** et **5,3 millions de relevés de prix** sur six carburants. C'est la source qui a servi à initialiser l'entrepôt.
- **La nouvelle source — flux temps réel** : `https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/records`. API Opendatasoft Explore v2.1, publique, sans authentification, réponses JSON, environ **9 800 stations** avec leur état courant : prix par carburant, horodatage de dernière mise à jour, ruptures de stock, services, horaires, département et région.
- **Cible** : PostgreSQL conteneurisé.

### Ce qui rend ce brief différent d'un exercice

Aucune anomalie n'a été injectée. Celles que vous rencontrerez sont dans la donnée publique depuis toujours.

- **L'archive est en ISO-8859-1**, pas en UTF-8. Les noms de villes accentués vous le rappelleront brutalement.
- **Les coordonnées ne sont pas des degrés.** Dans le XML, latitude et longitude sont des entiers exprimés dans une autre unité. Une carte construite sans conversion place la France quelque part au large de l'Afrique.
- **Un tiers des stations n'a aucun prix.** Sur 14 420 stations de l'archive 2025, **4 694 ne portent pas le moindre relevé** : fermées, inactives, ou jamais alimentées. Les compter comme des stations actives fausse toutes les moyennes par département.
- **Une valeur de code non documentée.** Le champ décrivant le type de voirie prend deux valeurs attendues… et une troisième, présente sur une seule station de tout le fichier. Que fait votre ETL quand il la rencontre ?
- **Des prix aberrants existent.** On trouve des relevés sous 0,50 € le litre. Erreur de saisie ou promotion réelle ? Vous devez trancher, écrire la règle, et assumer le nombre de lignes rejetées.
- **Le « temps réel » ne l'est pas toujours.** Sur environ 33 000 relevés du flux instantané, quelques centaines n'ont pas été mis à jour depuis plus d'un mois, et l'un d'eux date de plus de 600 jours. Un prix affiché n'est pas un prix frais : c'est exactement ce que le SLA de fraîcheur doit rendre visible.
- **Le serveur répond en gzip même quand on ne le lui demande pas.** Une lecture naïve du flux échoue sur un octet illisible. Vous ne le devinerez pas : vous le découvrirez.
- **Les deux sources ne se ressemblent pas.** L'archive est un XML de 386 Mo où chaque station porte la liste de ses relevés ; le flux temps réel est un JSON paginé où chaque station porte son état courant sur des colonnes dépliées. Même métier, structures opposées.
- **386 Mo de XML ne se chargent pas en mémoire.** La méthode de parsing que vous choisissez n'est pas un détail de style.

### Contraintes techniques

- **PostgreSQL imposé** (c'est l'existant) ; **Python** pour les ETL.
- Toute évolution se conçoit et se valide **avant application** : l'existant doit continuer à fonctionner à chaque étape (**non-régression**).
- Les **migrations de schéma sont scriptées, numérotées et rejouables** : aucune modification manuelle non tracée.
- L'alerte e-mail s'appuie sur un **serveur SMTP de test** (MailHog, Mailtrap ou équivalent) ; **aucun identifiant en clair dans le code**.
- Le **périmètre de chargement est paramétrable** (par département) : travaillez sur quelques départements pour itérer vite, et démontrez au moins un chargement large.
- **Volet RGPD** : l'entrepôt lui-même ne contient pas de données personnelles, mais votre application en produit (identifiants d'appareils, historiques de recherche des utilisateurs). Vous tenez le registre des traitements correspondant et rédigez la procédure de purge associée.
- Tout le travail est **versionné sur Git dès le premier jour**, avec des commits réguliers.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **Auditer un ETL hérité** et démontrer, preuve à l'appui, en quoi il corrompt les analyses passées ;
- **Historiser les dimensions d'un entrepôt** en implémentant un **SCD Type 2** (dates de validité, drapeau courant, clé de substitution) sur une dimension existante, sans perdre l'historique déjà accumulé ;
- **Faire évoluer les ETL** pour intégrer une seconde source au format radicalement différent, avec chargement **idempotent**, nettoyage documenté et respect des schémas physiques des zones de sortie (staging, entrepôt, datamart) ;
- **Traiter un fichier volumineux** sans saturer la mémoire, et justifier la méthode retenue ;
- **Gérer et superviser un entrepôt en production** : journalisation catégorisée, alertes, sauvegardes testées, indicateurs de service adossés à des **SLA** que vous définissez ;
- **Assurer la non-régression** et **documenter l'exploitation** par cas d'usage.

## Architecture cible

L'entrepôt reste un schéma en étoile sous PostgreSQL. Vous le faites évoluer en ajoutant l'historisation SCD Type 2 sur la dimension station, une chaîne d'intégration du flux temps réel en `staging → entrepôt → datamart`, et une couche de supervision.

```
   Archive annuelle XML             Flux temps réel JSON
   (386 Mo, 5,3 M relevés)          (~9 800 stations, API)
   [ l'existant ]                   [ la nouvelle source ]
            |                                 |
            |                                 |
   +--------v---------+             +---------v---------+
   |  ETL ANNUEL      |             |  ETL QUOTIDIEN    |
   |  (hérité, à      |             |  (à construire)   |
   |   faire évoluer) |             |                   |
   +--------+---------+             +---------+---------+
            |                                 |
            |                       +---------v---------+
            |                       |   ZONE STAGING    |
            |                       |  mapping, unités, |
            |                       |  dédoublonnage    |
            |                       |  (idempotent)     |
            |                       +---------+---------+
            |                                 |
   +--------v---------------------------------v---------------+
   |   ENTREPOT — SCHEMA EN ETOILE (PostgreSQL)               |
   |                                                          |
   |      dim_station*        dim_carburant      dim_temps    |
   |      (SCD Type 2)                                        |
   |            \                  |                /         |
   |             +------->   fait_prix    <-------+           |
   |                                                          |
   +--------+---------------------------------+---------------+
            |                                   |
   +--------v----------+            +-----------v-----------+
   |  DATAMART         |            |  SUPERVISION          |
   |  "tension des     |            |  - journal catégorisé |
   |   prix"           |            |  - alerte e-mail SMTP |
   |  (agrégations     |            |  - sauvegardes plan.  |
   |   data analyst)   |            |  - SLA + tableau bord |
   +-------------------+            +-----------------------+

   * dimension historisée en SCD Type 2 (dates de validité + drapeau courant)
```

> Vous produirez votre propre schéma d'architecture **au format image** (draw.io ou équivalent, pas d'ASCII art), montrant l'entrepôt **avant et après évolution**, à joindre au rendu.

## Données fournies

Le kit de démarrage se trouve dans le dossier [`starter-kit/`](starter-kit/). Il contient **l'existant dont vous héritez** — pas les données, que vous téléchargez vous-même depuis les sources officielles :

- `docker-compose.yml` — PostgreSQL 16 et un serveur SMTP de test (MailHog) ;
- `.env.example` — variables d'environnement d'exemple (aucun secret réel) ;
- `ddl/01_schema_etoile.sql` — le schéma en étoile existant : `dim_station`, `dim_carburant`, `dim_temps`, `fait_prix`, contraintes et index ;
- `bootstrap.py` — le chargement initial : télécharge l'archive annuelle réelle et alimente l'entrepôt. **C'est lui qui constitue votre historique de départ** ;
- `etl_nocturne.py` — **l'ETL hérité, volontairement défaillant** : il met à jour `dim_station` **par écrasement**, ne produit **aucun log** et n'est **pas idempotent**. Vous devez l'**auditer puis le remplacer** ; ne cherchez pas à le rafistoler ;
- `README.md` — la mise en route pas à pas.

## Travail demandé

Travail individuel sur 5 jours. L'entraide est encouragée — revue de pair, débogage à deux — mais chacun rend son propre travail et doit pouvoir expliquer chaque ligne de son code. Le formateur joue le rôle du CTO : sollicitez-le pour arbitrer les priorités ou valider vos SLA, comme vous le feriez en entreprise.

> **Règle des 2 heures.** Les données sont réelles et l'existant est volontairement défaillant. **Bloqué plus de 2 heures sur le même point ? Demandez un indice au formateur.** Notez le blocage et sa résolution dans votre journal de bord, qui fait partie du rendu.
>
> **Travaillez petit.** Chargez deux ou trois départements, pas la France entière. Un cycle de test qui dure 12 secondes vous fera progresser dix fois plus vite qu'un cycle de 20 minutes. Vous démontrerez un chargement large une seule fois, à la fin.

### Phase 1 — Cadrage et audit de l'existant (J1)

Aucune ligne de code de production : on commence par comprendre ce dont on hérite.

Montez l'environnement, lancez `bootstrap.py` sur quelques départements, explorez le modèle en étoile. Documentez les deux sources (format, encodage, volume, fréquence, qualité constatée) — et allez y voir vous-même plutôt que de recopier ce brief : vous trouverez des anomalies qui n'y sont pas mentionnées.

Auditez ensuite l'existant à la lumière de la question centrale. Que se passe-t-il exactement, table par table, quand une station change de caractéristiques aujourd'hui ? **Écrivez la requête SQL qui démontre le problème** : celle qui prouve qu'une moyenne passée est fausse. Et si l'ETL plante à 3 h du matin, qui le sait, quand, et que voient les 900 000 utilisateurs ?

Formalisez un court **rapport d'audit** et ouvrez un **Kanban public** : les trois demandes deviennent des user stories découpées, priorisées et estimées. Laquelle traitez-vous en premier, et comment le justifierez-vous devant le CTO ?

**Résultat testable en fin de J1 (point de contrôle formateur) :** environnement fonctionnel, sources documentées, requête qui démontre le bug, Kanban publié.

### Phase 2 — Historiser la dimension station (J2)

Attaquez la demande de la data analyst.

Quels attributs de la station méritent d'être historisés, et lesquels ne le méritent pas ? Le type de voirie, les services, les horaires, l'adresse — traitez-vous tout de la même façon ? Quel type de SCD correspond à chaque changement, et pourquoi le Type 2 est-il attendu ici ?

Quelles colonnes ajoutez-vous, et faut-il introduire une **clé de substitution** — auquel cas, que deviennent les jointures de `fait_prix` ? Comment migrez-vous les données déjà en place sans perdre l'historique existant ? Faites évoluer l'ETL pour qu'il **détecte les changements et crée de nouvelles versions** au lieu d'écraser.

**Résultat testable en fin de J2 :** en rejouant un changement de caractéristiques, une requête SQL démontre que l'analyse « autoroute vs réseau ordinaire » d'un mois passé ne bouge plus, tandis que la version courante de la station reste immédiatement accessible.

### Phase 3 — Intégrer le flux temps réel et son datamart (J3)

Place à la demande produit.

Créez une zone de **staging** pour le flux JSON, établissez le **mapping** de ses champs vers vos conventions et appliquez les nettoyages nécessaires. Les stations du flux et celles de l'archive se rattachent-elles ? Sur quelle clé, et que faites-vous des stations présentes dans l'un et absentes de l'autre ?

Comment rendez-vous le chargement **idempotent**, c'est-à-dire qu'une même exécution rejouée deux fois ne crée aucun doublon ? Quelles lignes rejetez-vous — prix aberrants, ruptures de stock, horodatages incohérents — et où tracez-vous ces rejets pour pouvoir en rendre compte ?

Construisez ensuite le **datamart « tension des prix »** destiné à la data analyst : quelles agrégations lui seront réellement utiles pour repérer où les prix s'écartent le plus de la moyenne nationale ?

Et surtout : comment **prouvez-vous que l'existant n'a pas régressé** ?

**Résultat testable en fin de J3 (point de contrôle formateur) :** deux exécutions successives du chargement temps réel ne créent aucun doublon, le datamart est interrogeable, l'ETL annuel fonctionne toujours.

### Phase 4 — Superviser, sauvegarder, se conformer (J4)

La demande du CTO : plus jamais de panne silencieuse.

Mettez en place une **journalisation** qui catégorise au minimum les alertes et les erreurs — au fait, qu'est-ce qui distingue une alerte d'une simple erreur journalisée ? Branchez un **envoi d'e-mail automatique** en cas d'erreur.

Planifiez des **sauvegardes** partielle et complète, et **testez une restauration** dans une base vierge : une sauvegarde jamais restaurée n'existe pas.

Définissez au moins **trois SLA** — fraîcheur des données, volumétrie chargée, taux de rejet. Quels seuils déclarez-vous acceptables, et au nom de quel besoin métier ? Sachant que l'application sert 900 000 utilisateurs, à partir de combien d'heures un prix périmé devient-il un incident ? Restituez ces indicateurs dans un tableau de bord de service.

Complétez le volet **RGPD** : registre des traitements de l'application et procédure de purge ou d'anonymisation des historiques de recherche.

**Résultat testable en fin de J4 :** provoquez une panne (source injoignable, fichier tronqué, base arrêtée) et montrez la chaîne complète **journal → alerte → diagnostic**, puis restaurez une sauvegarde.

### Phase 5 — Documenter et démontrer (J5)

Rédigez la **documentation d'exploitation** structurée par cas d'usage : que faire quand le chargement plante ? Comment ajouter une nouvelle source ? Comment restaurer une sauvegarde ? Mettez à jour le **schéma d'architecture** (image) et le **dictionnaire des modèles de données**, colonnes d'historisation comprises. Répétez votre démonstration.

### Socle commun (obligatoire)

- **SCD Type 2 fonctionnel** sur `dim_station`, migration de l'existant comprise.
- **Flux temps réel intégré** avec chargement idempotent et **datamart** créé.
- **Journalisation catégorisée** et **alerte e-mail** active.
- Une **sauvegarde complète planifiée et restaurée** avec succès.
- **Trois SLA** et leur **tableau de bord** (une page HTML, un notebook ou un dashboard simple suffisent).
- **Registre RGPD** et procédure de purge.
- **Documentation d'exploitation par cas d'usage** et **non-régression démontrée**.

### Pour aller plus loin (bonus)

- Charger **plusieurs années** d'archive et mesurer le comportement de votre ETL à l'échelle.
- Implémenter les SCD avec des **snapshots dbt** et couvrir les modèles de tests.
- Remplacer la planification cron par un **DAG Airflow**.
- Identifier un attribut où un **SCD Type 3** serait plus pertinent que le Type 2, l'implémenter et argumenter.
- Ajouter une **sauvegarde incrémentale** ou une stratégie PITR.

Les bonus ne compensent jamais un socle incomplet : **terminez d'abord le socle**.

## Livrables

**Repo GitHub public (obligatoire)**, contenant :

- un **README complet** : description du projet, technologies utilisées, instructions d'installation et de lancement pas à pas depuis le kit, architecture, auteur ;
- le **rapport d'audit** de l'existant, avec la requête SQL qui démontre la corruption des analyses passées ;
- les **scripts de migration SQL** numérotés et rejouables (colonnes SCD, clé de substitution, datamart) ;
- les **ETL mis à jour** : détection des changements et historisation, chargement temps réel idempotent avec nettoyages, traitement du XML volumineux ;
- la **configuration de journalisation et d'alerte e-mail** (`.env.example` fourni, aucun secret commité) ;
- les **scripts de sauvegarde** partielle et complète, leur planification et la **procédure de restauration** ;
- les **requêtes de vérification** : rejeu du scénario d'historisation et contrôle de non-régression.

**Livrables non-code :**

- le **schéma d'architecture** au format image (PNG ou export draw.io) montrant l'entrepôt avant et après évolution — jamais en ASCII ;
- le lien vers le **Kanban public** avec les user stories des trois demandes, priorisées, et l'historique de leur avancement ;
- la **documentation d'exploitation par cas d'usage** : pipeline en panne, ajout d'une source, restauration d'une sauvegarde, purge ;
- la **documentation des sources** : format, encodage, volume, unités, anomalies constatées et règles de traitement retenues, avec le **nombre de lignes rejetées** par règle ;
- le **dictionnaire des modèles de données** à jour, colonnes d'historisation comprises ;
- le **registre RGPD** et la procédure de purge ou d'anonymisation ;
- le **tableau de bord des indicateurs de service** (lien ou captures) avec la **définition écrite des SLA** retenus ;
- le **journal de bord** (`docs/journal.md`) : les blocages rencontrés sur les données réelles et sur l'existant hérité, ce que vous avez essayé, ce qui a débloqué.

## Démonstration finale

L'évaluation reproduit le format d'une étude de cas : maintenir un entrepôt existant en conditions opérationnelles. Deux volets pondérés.

**Volet 1 — Démonstration technique individuelle : 70 %.** 15 minutes de démonstration en direct + 10 minutes de questions. Le formateur, dans le rôle du CTO, impose le scénario suivant :

- **rejouer un changement de caractéristiques de station** et prouver, requête à l'appui, que l'historique est conservé et qu'une analyse passée ne bouge plus ;
- **lancer deux fois le chargement temps réel** et montrer qu'aucun doublon n'apparaît, puis provoquer une panne et montrer la chaîne **journalisation → alerte → diagnostic** ;
- **présenter le tableau de bord** des indicateurs de service et **restaurer une sauvegarde** dans une base vierge ;
- **présenter le registre RGPD** et dérouler la procédure de purge.

Les questions portent sur la justification des choix : type de SCD retenu, attributs historisés ou non, seuils des SLA, règles de rejet, méthode de parsing du fichier volumineux, priorisation des trois demandes.

**Volet 2 — Revue de code et d'architecture : 30 %.** Structure et lisibilité du code, migrations scriptées et rejouables, qualité de la documentation par cas d'usage, dictionnaire de données à jour, cohérence du schéma d'architecture, historique de commits témoignant d'un travail régulier.

> **Validation partielle** : un apprenant dont le pipeline ne fonctionne pas en démonstration mais dont le code est structuré et documenté peut valider partiellement les compétences concernées. L'historisation, l'intégration de la nouvelle source et la supervision sont évaluées **indépendamment** : un échec sur l'une n'entraîne pas l'échec des autres. Les bonus ne conditionnent la validation d'aucune compétence.

## Critères de validation

### Intégration des ETL

- Les formats, encodages et volumes de chaque source sont documentés, connus et expliqués.
- La méthode de traitement du fichier volumineux est adaptée et justifiée (aucun chargement intégral en mémoire).
- Les ETL appliquent les traitements de nettoyage attendus : unités converties, doublons éliminés, prix aberrants et stations sans relevé traités selon des règles explicites, avec décompte des lignes affectées — vérifiable en rejouant deux fois la même exécution.
- Les données en sortie respectent les schémas physiques des zones de sortie (staging, entrepôt, datamart), et le fonctionnement de chaque ETL est explicité sans ambiguïté dans la documentation.

### Historisation des dimensions (SCD)

- Le type de SCD retenu est adapté à chaque type de changement, et le choix des attributs historisés est justifié dans la documentation.
- L'historisation est fonctionnelle : le rejeu d'un changement crée une nouvelle version datée (dates de validité, drapeau courant) et les anciennes valeurs restent interrogeables.
- Une requête démontre qu'une analyse portant sur une période passée donne le même résultat avant et après un changement de caractéristiques.
- Les ETL sont mis à jour en conséquence, l'intégration respecte la modélisation initiale, et la non-régression de l'existant est démontrée.

### Gestion et supervision de l'entrepôt

- Une journalisation de l'activité est en place et catégorise au minimum les alertes et les erreurs.
- Un système d'alerte e-mail est activé et envoie effectivement un message en cas d'erreur notifiée dans les journaux (démontré en direct).
- Des tâches planifiées de sauvegarde partielle et complète sont programmées, et une restauration est démontrée dans une base vierge.
- Les indicateurs de service s'appuient sur des SLA explicites et justifiés, restitués dans un tableau de bord ; les tâches de maintenance sont priorisées et l'arbitrage est argumenté (Kanban à l'appui).
- La documentation est structurée par cas d'usage, le registre RGPD est complet et la procédure de tri des données personnelles est rédigée.

## Ressources

- [Cours SQL](../../../01-Fondamentaux/SQL/)
- [Cours Python](../../../01-Fondamentaux/Python/)
- [Cours Docker](../../../02-Containerisation/Docker/)
- [Data Warehouse](../../../05-Databases/DataWarehouse/)
- Archives annuelles des prix des carburants (données officielles) : https://donnees.roulez-eco.fr/opendata/annee/2025
- Prix des carburants — flux instantané (jeu de données et API) : https://data.economie.gouv.fr/explore/dataset/prix-des-carburants-en-france-flux-instantane-v2/
- Documentation de l'API Opendatasoft Explore v2.1 : https://help.opendatasoft.com/apis/ods-explore-v2/
- Python — `xml.etree.ElementTree.iterparse` (parsing incrémental) : https://docs.python.org/3/library/xml.etree.elementtree.html#iterparse
- Python — tutoriel officiel du module `logging` : https://docs.python.org/3/howto/logging.html
- Kimball Group — Slowly Changing Dimension Type 2 : https://www.kimballgroup.com/data-warehouse-business-intelligence-resources/kimball-techniques/dimensional-modeling-techniques/type-2/
- PostgreSQL — sauvegarde et restauration : https://www.postgresql.org/docs/current/backup.html
- PostgreSQL — `pg_dump` : https://www.postgresql.org/docs/current/app-pgdump.html
- PostgreSQL — `INSERT ... ON CONFLICT` (idempotence) : https://www.postgresql.org/docs/current/sql-insert.html
- MailHog, serveur SMTP de test : https://github.com/mailhog/MailHog
- CNIL — Le registre des activités de traitement : https://www.cnil.fr/fr/RGPD-le-registre-des-activites-de-traitement
- dbt — documentation des snapshots (bonus) : https://docs.getdbt.com/docs/build/snapshots
