# Brief : Où positionner les taxis new-yorkais — pipeline 100 % cloud BigQuery + dbt + Cloud Composer

## Informations

| Critère | Valeur |
|---------|--------|
| **Durée** | 5 jours (35 heures) |
| **Niveau** | Intermédiaire-Avancé |
| **Modalité** | Individuel |
| **Technologies** | Google Cloud (BigQuery, Cloud Storage, Cloud Composer), dbt Core (dbt-bigquery), Apache Airflow, Python, Parquet, SQL, Git |
| **Prérequis** | [Cours Python](../../../01-Fondamentaux/Python/) + [Cours SQL](../../../01-Fondamentaux/SQL/) + [Cours dbt](../../../06-Data-Engineering/Dbt/) + [Cours Airflow](../../../06-Data-Engineering/Airflow/) + notions de cloud |
| **Données** | **100 % réelles** — NYC Taxi & Limousine Commission, ~40 M de trajets, ~8 Go de Parquet |
| **Coût** | ⚠️ **Facturé à l'usage.** Crédits d'essai GCP requis. Voir l'avertissement ci-dessous. |

> ## ⚠️ Avertissement coût — à lire avant toute chose
>
> Cette variante est la seule des trois qui engage de l'argent réel. **Cloud Composer n'a pas
> d'offre gratuite** : un environnement facturé à l'heure tourne tant qu'il existe, même quand
> aucun DAG ne s'exécute, même la nuit, même le week-end. Un environnement oublié après la
> formation continue de coûter.
>
> Trois règles non négociables :
>
> 1. **Consultez la grille tarifaire officielle avant de créer quoi que ce soit** :
>    https://cloud.google.com/composer/pricing — et calculez ce que coûtent 5 jours.
> 2. **Posez un budget avec alerte** sur votre projet GCP dès la première heure.
> 3. **La destruction de l'environnement Composer est un livrable**, avec preuve. Un projet non
>    détruit à la fin du brief est un échec sur le critère de maîtrise des coûts, quelle que soit
>    la qualité du pipeline.
>
> BigQuery et Cloud Storage, eux, disposent d'offres gratuites généreuses au regard de ce projet
> (le jeu de données fait environ 8 Go). Le poste de coût, c'est Composer.

## Contexte

### L'entreprise

**Fleetwise** est une société de 30 personnes qui vend un logiciel d'aide au pilotage de flottes
de VTC et de taxis. Ses clients sont des exploitants de 50 à 500 véhicules. Elle prépare son
entrée sur le marché nord-américain et veut étayer son argumentaire avec des données publiques
réelles plutôt qu'avec des projections. Vous êtes data engineer dans l'équipe produit.

### Le problème

L'équipe commerciale affirme depuis des mois qu'« il faut positionner les véhicules à Manhattan
le vendredi soir ». Personne n'a vérifié. Les analyses existantes tiennent dans un notebook que
son auteur a quitté l'entreprise, qui charge un seul mois de données, plante une fois sur deux
et que personne ne sait relancer.

Fleetwise vient de signer avec un premier client nord-américain et a décidé d'héberger sa
plateforme data entièrement dans le cloud : plus de machine sous un bureau, un service managé qui
tourne sans administrateur système. La directrice technique veut un pipeline qui se relance seul
chaque mois — **et une facture qu'elle peut prévoir**. C'est la condition qu'elle a posée devant
les associés.

### La question centrale

Tout votre travail doit permettre d'y répondre, et vous devez pouvoir vous y référer à chaque
étape :

> **« Où et quand faut-il positionner les véhicules pour maximiser le revenu par heure de service ? »**

Notez ce qu'elle n'est pas : « combien de trajets par mois ». Un décompte n'est pas une réponse.
Le revenu **par heure de service** met en tension la course lucrative et la course rapide, et
c'est là que se trouve l'intérêt du sujet.

### Les sources de données

- **Trajets — NYC TLC Yellow Taxi** : `https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_YYYY-MM.parquet`.
  Un fichier **Parquet par mois**, de 48 à 70 Mo chacun, soit environ **3 millions de trajets
  mensuels**. Les données sont publiées avec environ deux mois de décalage. Sur 2024 à
  aujourd'hui, comptez **~40 millions de lignes et ~8 Go**.
- **Référentiel des zones** : `https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv`
  (12 Ko) — sans lui, vos analyses parlent de « la zone 132 » plutôt que de « JFK ».
- **Dictionnaire officiel des données** : https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf

### Ce qui rend ce brief différent d'un exercice

Ce sont des données de production d'une administration, avec leurs défauts d'origine. Voici ce
que donne une mesure réelle sur deux mois éloignés. **Ne recopiez pas ces chiffres :
refaites la mesure, c'est le travail de la Phase 1.** Ils sont là pour vous montrer que les
défauts ne sont ni stables ni négligeables.

| | 2024-01 | 2026-05 |
|---|---|---|
| Lignes | 2 964 624 | 4 090 836 |
| Montants totaux négatifs | 1,20 % | 0,36 % |
| Distance nulle | 2,04 % | 2,76 % |
| `passenger_count` absent | 4,73 % | **23,35 %** |
| Dépose avant prise en charge | 0,03 % | **1,27 %** |
| Distance > 1 000 miles | 0,0008 % | 0,0016 % |

Deux enseignements s'y cachent, et ils valent mieux qu'un cours. D'abord, **la qualité se dégrade
dans le temps** : un champ renseigné à 95 % en 2024 ne l'est plus qu'à 77 % en 2026. Une règle de
nettoyage calibrée sur un mois peut donc être absurde sur un autre. Ensuite, **un montant négatif
n'est pas forcément une erreur** : ce sont souvent des annulations et régularisations comptables.
Que faites-vous d'un trajet à −8 $ — vous le jetez, ou vous le gardez parce qu'il existe
vraiment ?

Enfin, **le schéma change**, et pas de façon théorique : les fichiers de 2024 comptent
**19 colonnes**, ceux de 2026 en comptent **20**. La nouvelle s'appelle `cbd_congestion_fee` —
le péage urbain de Manhattan, entré en vigueur début 2025. Un pipeline qui suppose un schéma figé
cassera au moment précis où le backfill franchira cette frontière. C'est le vrai piège du brief,
et c'est ce qui distingue un chargement d'un pipeline.

Sur BigQuery, ce dernier point mérite une attention particulière : un chargement en
**auto-détection de schéma** passera sans broncher aujourd'hui et vous le fera payer au backfill,
avec des tables aux schémas divergents selon le mois chargé.

S'y ajoutent deux contraintes propres au cloud facturé à l'usage : **chaque requête a un coût**
(BigQuery facture les octets lus, donc un `SELECT *` sur 40 millions de lignes est une décision,
pas un réflexe), et **l'infrastructure coûte même à l'arrêt**.

### Contraintes techniques

- **Google Cloud** : BigQuery comme entrepôt, Cloud Storage comme zone d'atterrissage, **Cloud
  Composer** comme orchestrateur managé. **dbt Core** avec l'adaptateur `dbt-bigquery`.
- **Budget et alerte configurés dès la première heure**, avant toute création de ressource.
- **Aucune clé de compte de service dans le dépôt.** Ni fichier JSON, ni variable en clair, ni
  dans l'historique Git. Privilégiez les identités managées ; si vous devez générer une clé,
  elle vit dans un `.env` non versionné et vous la révoquez à la fin.
- **Principe du moindre privilège** : les comptes de service que vous créez n'ont que les rôles
  nécessaires. `Éditeur` sur le projet n'est pas une réponse acceptable.
- Le pipeline est **rejouable et idempotent**, et doit supporter un **backfill** depuis janvier
  2024 avant de fonctionner mensuellement.
- **Développez en local, déployez ensuite.** Un DAG mis au point directement sur Composer coûte
  cher en temps et en argent : chaque correction demande un redéploiement et une attente.
- Tout le code est **versionné sur GitHub dès le premier jour**.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **Concevoir et provisionner une plateforme data cloud** : zone d'atterrissage objet, entrepôt
  en couches, orchestrateur managé, avec des accès au moindre privilège ;
- **Automatiser l'ingestion** de fichiers volumineux vers une zone objet puis vers l'entrepôt,
  avec gestion des erreurs, reprise et journalisation ;
- **Transformer les données avec dbt Core** : modèles en couches, tests, documentation et lignage ;
- **Orchestrer en utilisateur avancé d'Airflow** : API TaskFlow, mapping dynamique de tâches,
  capteurs différés, déclenchement piloté par la donnée, branchement conditionnel, reprises,
  pools, rappels de défaillance, gestion des secrets et **tests automatisés de DAG** — le tout
  en maîtrisant la distinction entre date logique et date du jour ;
- **Traiter une évolution de schéma** entre deux périodes sans casser l'historique déjà chargé ;
- **Piloter et restituer le coût** d'une plateforme cloud, et **démanteler** proprement une
  infrastructure en fin de projet.

## Airflow : le socle avancé attendu

Ce brief ne se contente pas d'un DAG qui tourne. L'objectif est que vous sortiez **utilisateur
avancé d'Airflow**, capable de tenir un pipeline en production et d'en discuter les choix. Les
dix points ci-dessous constituent le socle : ils sont tous exigés, tous démontrables, et tous
questionnés en soutenance.

1. **API TaskFlow** (`@dag`, `@task`) plutôt que des opérateurs instanciés à la main — et vous
   saurez dire ce que vous y gagnez et ce que vous y perdez.
2. **Mapping dynamique de tâches** (`.expand()`) : le nombre de tâches est déduit des mois à
   traiter, il n'est pas écrit en dur. Ajouter une année ne doit modifier aucune ligne de DAG.
3. **Capteur différé** (*deferrable sensor*) qui attend la publication du fichier mensuel sans
   monopoliser un worker. Un capteur bloquant fonctionne aussi — mais vous devrez expliquer
   pourquoi le différé est meilleur, et le mettre en œuvre.
4. **Planification pilotée par les données** : la transformation ne se déclenche pas à une heure
   fixe en espérant que l'ingestion soit finie, elle se déclenche **parce que** la couche brute a
   été mise à jour. C'est le passage du « toutes les nuits à 3 h » au « quand la donnée est prête ».
5. **Branchement conditionnel** (`@task.branch`) : que fait le pipeline quand le mois n'est pas
   encore publié, ou quand il l'est déjà et n'a pas changé ?
6. **Reprises et temporisation** : nombre de tentatives, délai croissant entre essais, délai
   maximal. Une source publique gratuite qui répond en 503 ne se martèle pas.
7. **Contrôle de la concurrence** : un *pool* qui limite les téléchargements simultanés vers la
   source, et une limite d'exécutions parallèles du DAG. Justifiez vos valeurs.
8. **Rappels et alerte** (`on_failure_callback`) : une défaillance produit une notification
   exploitable, pas seulement une case rouge dans l'interface.
9. **Connexions et variables Airflow** plutôt que des constantes en dur : aucun identifiant,
   aucun chemin de production dans le code du DAG.
10. **Tests automatisés de vos DAG** : au minimum un test qui vérifie qu'aucun DAG n'a d'erreur
    d'import et que la structure attendue est là. Un DAG cassé doit se voir avant le déploiement,
    pas dans l'interface.

Un point de vigilance, enfin, qui sépare l'utilisateur avancé du débutant : **la date logique
d'exécution n'est pas la date d'aujourd'hui**. Un DAG mensuel qui utilise `datetime.now()` pour
choisir le mois à traiter produira n'importe quoi au backfill — et c'est exactement ce qui vous
attend en Phase 4.

## Architecture cible

Un pipeline ELT entièrement managé : atterrissage sur Cloud Storage, entrepôt en couches dans
BigQuery, orchestration par Cloud Composer.

```
   NYC TLC — fichiers Parquet mensuels (~3 M lignes / mois)
   + référentiel des zones (CSV)
                    |
        +-----------v------------------------------------+
        |  CLOUD COMPOSER (Airflow managé)               |
        |  DAG mensuel + backfill depuis 2024-01         |
        |                                                |
        |  [-> GCS] -> [-> BigQuery RAW] -> [dbt run]    |
        |                                 -> [dbt test]  |
        +-----------+------------------------------------+
                    |
        +-----------v------------------------------------+
        |  CLOUD STORAGE — zone d'atterrissage           |
        |  fichiers Parquet datés, immuables             |
        +-----------+------------------------------------+
                    |
        +-----------v------------------------------------+
        |  BIGQUERY                                      |
        |   dataset RAW      : données brutes            |
        |        |             (tables ou tables externes)|
        |        v                                       |
        |   dataset STAGING  : nettoyage, typage,        |
        |        |             règles de rejet tracées   |
        |        v                                       |
        |   dataset MARTS    : tables d'analyse (dbt)    |
        +-----------+------------------------------------+
                    |
        +-----------v------------------------------------+
        |  RESTITUTION + SUIVI DES COÛTS + DÉMANTÈLEMENT |
        +------------------------------------------------+
```

> Vous produirez votre propre schéma d'architecture **au format image** (draw.io ou équivalent,
> pas d'ASCII art) à joindre au rendu.

## Données fournies

Le kit de démarrage se trouve dans le dossier [`starter-kit-local/`](starter-kit-local/) — celui
de la variante locale, réutilisé ici pour une raison précise : **vous développerez votre DAG et
vos modèles dbt en local avant de les déployer sur Composer**. C'est la seule façon raisonnable
de travailler sur un orchestrateur facturé à l'heure.

- `docker-compose.yml` — Airflow local pour la mise au point ;
- `dbt/` — squelette dbt (vous remplacerez le profil DuckDB par un profil BigQuery) ;
- `.gitignore` — empêche de committer clés, données et secrets ;
- `README.md` — mise en route.

**Ne sont pas fournis, et constituent le sujet du brief** : le projet GCP et son budget, le
bucket, les datasets BigQuery, les comptes de service et leurs rôles, l'environnement Composer,
le DAG, les scripts d'ingestion, les modèles dbt et les tests.

## Travail demandé

Travail individuel sur 5 jours. L'entraide est encouragée, mais chacun rend son propre code.

> **Règle des 2 heures.** **Bloqué plus de 2 heures sur le même point ? Demandez un indice au
> formateur.** Notez le blocage et sa résolution dans votre journal de bord.
>
> **Règle du portefeuille.** Avant de créer une ressource, sachez ce qu'elle coûte à l'heure.
> Avant de partir le soir, sachez ce qui tourne encore. Le formateur jouera la directrice
> technique : il vous demandera votre facture prévisionnelle, pas votre enthousiasme.

### Phase 1 — Cadrage, projet GCP, budget et exploration (J1)

**Commencez par le budget, pas par le code.** Créez votre projet GCP, activez la facturation sur
vos crédits d'essai, puis posez immédiatement un **budget avec alerte par e-mail**. Consultez la
grille tarifaire de Composer et calculez ce que coûteraient 5 jours d'environnement : écrivez ce
chiffre, il fera partie du rendu et vous le comparerez au réel en Phase 5.

Explorez ensuite le jeu de données **sans rien déployer** : téléchargez un mois et regardez-le
localement (DuckDB ou pandas font très bien l'affaire, gratuitement). Combien de lignes, quelles
colonnes, quels types ? Comparez le schéma de `2024-01` et celui du mois le plus récent :
qu'est-ce qui a changé ?

Mesurez vous-même les anomalies annoncées plutôt que de les recopier, et décidez ce que vous en
ferez — et **pourquoi**. Définissez vos indicateurs : qu'est-ce, précisément, qu'une « heure de
service » quand on ne dispose que des trajets facturés ?

Concevez enfin votre architecture cloud : quels datasets, quel bucket, quels comptes de service
avec quels rôles ? Documentez les sources dans `docs/sources.md` et ouvrez un **Kanban public**.

**Résultat testable en fin de J1 (point de contrôle formateur) :** projet GCP créé, **budget et
alerte configurés**, coût prévisionnel calculé et écrit, anomalies mesurées, différences de schéma
identifiées, indicateurs définis, architecture conçue, Kanban rempli.

### Phase 2 — Zone d'atterrissage et couche brute (J2)

Créez le bucket Cloud Storage et les datasets BigQuery, **par script ou par commande versionnée**
plutôt qu'en cliquant dans la console — vous devrez pouvoir tout recréer, et tout détruire.

Chargez **un mois** : téléchargement, dépôt dans le bucket avec un nommage daté, puis chargement
dans le dataset brut. Table native ou table externe pointant sur le bucket ? Les deux se
défendent ; choisissez au regard du coût de requête et de la fraîcheur, et justifiez.

Que fait votre chargement si le fichier n'existe pas encore parce que la commission n'a pas
publié ? S'il est interrompu ? Si vous relancez le même mois deux fois ? Et attention ici :
laisser BigQuery **auto-détecter le schéma** vous simplifiera la vie aujourd'hui et vous la
compliquera beaucoup au backfill. Vous êtes prévenu.

**Résultat testable en fin de J2 :** deux mois déposés dans le bucket et chargés en couche brute,
un rechargement du même mois ne crée aucun doublon, le référentiel des zones est joignable.

### Phase 3 — Transformation dbt (J3)

Construisez vos modèles dbt en deux niveaux : **staging** (nettoyage, typage, règles de rejet) puis
**marts** (tables d'analyse). Travaillez en local contre BigQuery — pas encore sur Composer.

Chaque règle de rejet est **écrite dans le modèle** et son effet est mesurable : combien de lignes
écartées, pour quelle raison, tracées où ? Écrivez des **tests dbt** : unicité, non-nullité,
valeurs acceptées, cohérence métier.

Surveillez le coût : BigQuery facture les octets lus. Le **partitionnement** par date et le
**clustering** par zone changent radicalement la facture d'une requête d'analyse. Mettez-les en
place et **mesurez la différence** — c'est un des enseignements les plus concrets de ce brief.

Générez la documentation dbt et vérifiez que le **lignage** est lisible.

**Résultat testable en fin de J3 (point de contrôle formateur) :** `dbt run` et `dbt test` passent
sur deux mois, `dbt docs` montre le lignage, le partitionnement est en place avec une mesure avant
/ après sur les octets lus, et une requête sur les marts propose une première réponse à la
question centrale.

### Phase 4 — Du script au DAG : orchestration et backfill (J4)

Transformez votre chaîne en **DAG Airflow**, écrit avec l'**API TaskFlow**. Les dépendances entre
tâches doivent refléter la réalité — que se passe-t-il si `dbt test` échoue, les marts
sont-ils quand même publiés ?

La première décision structurante est le **choix du mois à traiter**. Votre DAG doit le déduire
de la **date logique de l'exécution**, pas de la date du jour. Écrivez `datetime.now()` quelque
part et votre backfill produira 24 fois le même mois : c'est le piège classique, et vous le
rencontrerez.

La seconde est le **mapping dynamique** : plutôt qu'un DAG qui traite un mois et qu'on relance,
générez vos tâches à partir de la liste des mois à traiter avec `.expand()`. Combien de tâches
votre interface affiche-t-elle alors, et que se passe-t-il si une seule échoue ?

Ajoutez les **reprises** : combien de tentatives, avec quel délai croissant ? Une source publique
gratuite qui répond en 503 se laisse le temps de respirer. Posez aussi un **pool** limitant les
téléchargements simultanés — vous interrogez un service public, pas une API commerciale.

Lancez enfin le **backfill** depuis janvier 2024. C'est ici que tout se joue : votre pipeline
supporte-t-il d'être exécuté sur toute la période ? Combien de temps y passe-t-il ? Et surtout,
**que se passe-t-il quand il atteint le mois où `cbd_congestion_fee` apparaît** ? Si ça casse,
c'est normal — c'est le problème à résoudre, pas un accident.

**Résultat testable en fin de J4 (point de contrôle formateur) :** le backfill complet s'exécute
sans intervention manuelle, les tâches sont générées dynamiquement, un mois rejoué ne duplique
rien, et les logs permettent de dire ce qui s'est passé.

### Phase 5 — Airflow avancé : réactivité, fiabilité et tests (J5)

La journée qui sépare « j'ai fait tourner un DAG » de « je tiens un pipeline en production ».
Reprenez le socle avancé listé plus haut et complétez ce qui manque.

**Rendez le pipeline réactif.** Aujourd'hui, il se déclenche à une heure fixe en espérant que la
source ait publié. Remplacez cet espoir par un **capteur** qui attend réellement la publication
du fichier mensuel — puis rendez-le **différé**, pour qu'il n'occupe pas un worker pendant des
heures. Quelle différence cela fait-il quand vingt-quatre exécutions attendent en même temps ?

**Déclenchez par la donnée, pas par l'horloge.** Faites en sorte que la transformation démarre
**parce que** la couche brute vient d'être mise à jour, et non parce qu'il est 3 h du matin. Vos
deux DAG deviennent alors indépendants tout en restant enchaînés.

**Traitez les cas de bord.** Un **branchement conditionnel** décide quoi faire quand le mois
n'est pas publié, ou quand il l'est déjà et n'a pas changé. Sortir proprement vaut mieux
qu'échouer bruyamment.

**Rendez les défaillances visibles.** Un `on_failure_callback` produit une notification
exploitable — qui contient quoi ? Le nom de la tâche suffit-il pour diagnostiquer à 3 h du matin ?

**Sortez les secrets et les chemins du code**, dans les connexions et variables Airflow.

**Testez vos DAG.** Écrivez au minimum un test qui échoue si un DAG ne s'importe pas, et un test
qui vérifie la structure attendue. Lancez-le avant chaque commit : un DAG cassé doit se voir dans
votre terminal, pas dans l'interface le lendemain.

Finalisez enfin la **note de restitution** (rédigée au fil de l'eau depuis la Phase 3), le README,
le schéma d'architecture et le journal de bord, puis répétez votre démonstration.

**Résultat testable :** le capteur attend réellement, la transformation se déclenche sur mise à
jour de la donnée, une défaillance provoquée émet une notification, et `pytest` passe sur vos DAG.

#### Et en fin de journée, le volet spécifique à cette variante

Produisez le **relevé de coûts réels** et confrontez-le à votre prévision de J1 : où vous
êtes-vous trompé, et pourquoi ? Qu'est-ce qui a coûté le plus cher — le stockage, les requêtes,
ou l'orchestrateur qui tournait pendant que vous dormiez ?

**Puis démantelez.** Détruisez l'environnement Composer et les ressources créées, et **conservez
la preuve** (capture, sortie de commande, budget retombé à zéro). Vérifiez qu'aucune clé de
compte de service ne survit. C'est un livrable au même titre que le code.

Prévoyez enfin un **plan B pour la soutenance** : votre environnement sera détruit au moment de
soutenir, donc appuyez-vous sur des captures et des exports préparés à l'avance.

### Socle commun (obligatoire)

- Projet GCP avec **budget et alerte** configurés dès J1, et coût prévisionnel écrit.
- Bucket et datasets créés **par script ou commande versionnée**, comptes de service au moindre
  privilège.
- Ingestion automatisée avec gestion des erreurs, reprise et journalisation.
- Modèles dbt en couches avec **tests** et **documentation générée**, règles de rejet écrites,
  tracées et chiffrées.
- **Partitionnement et clustering** en place, avec mesure de leur effet sur les octets lus.
- **DAG déployé sur Cloud Composer**, écrit en **API TaskFlow**, avec **mapping dynamique** des mois, reprises et
  temporisation, **pool** limitant la concurrence, **backfill complet depuis 2024-01** et
  idempotence démontrée. Le mois traité est déduit de la **date logique**, jamais de `now()`.
- **Airflow avancé** : capteur **différé** sur la publication du fichier, **déclenchement piloté
  par la donnée** entre ingestion et transformation, **branchement conditionnel** sur les cas de
  bord, **rappel de défaillance** produisant une notification exploitable, secrets et chemins
  sortis du code via connexions et variables.
- **Tests automatisés des DAG** : au minimum absence d'erreur d'import et vérification de la
  structure attendue.
- **Traitement documenté du changement de schéma** entre périodes.
- **Relevé de coûts réels** confronté à la prévision, et **preuve de démantèlement**.
- Réponse chiffrée à la question centrale.
- Repo public documenté, schéma d'architecture, Kanban, journal de bord, **aucun secret versionné**.

### Pour aller plus loin (bonus)

- **Provisionner en Terraform** l'ensemble des ressources, et détruire par `terraform destroy`
  — le démantèlement devient alors une commande plutôt qu'une checklist.
- Ajouter les taxis **verts** (`green_tripdata_*`) et réconcilier les deux jeux.
- Comparer le coût d'une même analyse avec et sans partitionnement, chiffres à l'appui.
- Tableau de bord **Looker Studio** branché sur les marts.
- Alerte sur échec de `dbt test` (Cloud Monitoring ou notification Airflow).

Les bonus ne compensent jamais un socle incomplet : **terminez d'abord le socle**.

## Livrables

À rendre au plus tard J5 à 17 h (lien du repo posté sur la plateforme) :

- Un **repo GitHub public** avec un README structuré : description, question centrale,
  technologies et justification, procédure de création **et de destruction** de l'infrastructure,
  architecture, auteur.
- Les **scripts ou commandes versionnés** de création des ressources (bucket, datasets, comptes de
  service et rôles).
- Le **DAG** et les **scripts d'ingestion**, avec gestion des erreurs et journalisation.
- Les **tests automatisés des DAG** (dossier `tests/`) et la commande pour les lancer.
- Le **projet dbt** : modèles staging et marts, tests, documentation générée (ou captures),
  configuration du partitionnement et du clustering.
- La **documentation des sources** (`docs/sources.md`) : format, volume, colonnes, anomalies
  **mesurées** avec leurs pourcentages réels.
- La **note sur le changement de schéma** et le **décompte des rejets** par règle.
- La **note de coûts** : prévision de J1, coût réel constaté, écart et explication, mesure de
  l'effet du partitionnement sur les octets lus.
- La **preuve de démantèlement** : environnement Composer détruit, ressources supprimées, clés
  révoquées.
- Le **schéma d'architecture** au format image — pas d'ASCII.
- La **note de restitution** (une page) répondant à la question centrale.
- Le lien vers le **Kanban public**, le **journal de bord**, et une **preuve du backfill**
  (captures de la grille Airflow ou logs exportés).
- Un `.env.example` sans secret, et **aucune clé de compte de service dans l'historique Git**.

## Démonstration finale

**Volet 1 — Démonstration technique individuelle : 70 %.** 15 minutes + 10 minutes de questions.
Votre environnement étant détruit, la démonstration s'appuie sur des **captures et exports
préparés** : interface Composer avec la grille du backfill, logs d'une exécution, résultats des
tests dbt, lignage, requêtes sur les marts, et tableau de coûts. Vous pouvez conserver les
datasets BigQuery (peu coûteux) pour exécuter des requêtes en direct — c'est même recommandé.

Les questions porteront sur vos choix : table native ou externe, partitionnement, rôles attribués
aux comptes de service, gestion des identifiants, stratégie de backfill, et **ce que vous feriez
différemment pour diviser la facture par deux**.

**Volet 2 — Revue de code et d'architecture : 30 %.** Structure du repo, lisibilité du DAG et des
modèles, qualité des tests, reproductibilité de la création **et de la destruction** de
l'infrastructure, **absence de secrets versionnés**, régularité des commits.

> **Validation partielle** : un pipeline non fonctionnel en démonstration mais dont le code est
> structuré, versionné et documenté peut valider partiellement les compétences concernées.
> En revanche, une clé de compte de service trouvée dans l'historique Git invalide le critère de
> sécurité, et une infrastructure non détruite invalide celui de maîtrise des coûts — quelle que
> soit la qualité du reste.

## Critères de validation

### Conception et provisionnement de la plateforme cloud

- Les ressources (bucket, datasets, comptes de service) sont créées par script ou commande
  versionnée, et recréables à l'identique.
- Les comptes de service respectent le moindre privilège ; les rôles attribués sont justifiés.
- Un budget avec alerte est configuré **avant** la création des ressources facturées.
- Aucune clé ni identifiant n'apparaît dans le dépôt ni dans son historique.

### Automatisation de l'ingestion

- Le chargement est fonctionnel ; le choix table native ou externe est justifié.
- Les erreurs (fichier absent, chargement interrompu) sont gérées selon une stratégie explicite et
  journalisées.
- Le rechargement d'un mois déjà traité ne crée ni doublon ni perte, vérifiable dans l'entrepôt.
- Le code est versionné avec un historique réparti sur la durée du projet.

### Transformation et qualité (dbt)

- Les modèles sont organisés en couches et produisent des résultats corrects et vérifiables.
- Les règles de nettoyage sont écrites en code et le nombre de lignes écartées par règle est
  mesurable.
- Des tests dbt couvrent unicité, non-nullité et cohérence métier ; leur conduite en cas d'échec
  est explicite.
- Le partitionnement et le clustering sont en place, et **leur effet sur les octets lus est
  mesuré et documenté**.

### Orchestration managée (Cloud Composer)

- Le DAG s'exécute sans intervention manuelle ; il est écrit en API TaskFlow et ses dépendances
  sont correctes.
- Les tâches sont **générées dynamiquement** à partir des mois à traiter : ajouter une période ne
  demande aucune modification du DAG.
- Le mois traité est déduit de la **date logique d'exécution** ; le **backfill depuis janvier
  2024** est réalisé et prouvé (grille d'exécutions ou logs).
- Un **capteur différé** attend la publication du fichier sans monopoliser de worker, et un
  **branchement** traite le cas du mois non publié.
- La transformation est déclenchée **par la mise à jour de la donnée**, non par une heure fixe.
- Reprises, temporisation croissante et **pool** de concurrence sont paramétrés et justifiés ;
  un **rappel de défaillance** produit une notification exploitable.
- Les secrets et chemins passent par les **connexions et variables** Airflow, jamais en dur.
- Des **tests automatisés** échouent si un DAG ne s'importe pas ou si sa structure change.
- Le changement de schéma (`cbd_congestion_fee`) est absorbé sans casser l'historique déjà chargé,
  et le traitement retenu est documenté.

### Maîtrise des coûts et démantèlement

- Un coût prévisionnel a été calculé en J1 et confronté au coût réel en J5, écart expliqué.
- Les postes de coût sont identifiés et hiérarchisés.
- L'infrastructure facturée est **effectivement détruite**, preuve à l'appui, et les clés sont
  révoquées.

### Restitution

- Les indicateurs répondent à la question centrale, et non à un simple décompte.
- La définition de chaque indicateur est écrite : formule, granularité, période.
- La note de restitution tranche et s'appuie sur des chiffres issus du pipeline.

## Ressources

- [Cours Python](../../../01-Fondamentaux/Python/) · [Cours SQL](../../../01-Fondamentaux/SQL/)
- [Cours dbt](../../../06-Data-Engineering/Dbt/) · [Cours Airflow](../../../06-Data-Engineering/Airflow/)
- NYC TLC — page officielle des données de trajets : https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- Dictionnaire officiel des données (Yellow Taxi) : https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
- Référentiel des zones : https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
- **Cloud Composer — tarification (à lire en premier)** : https://cloud.google.com/composer/pricing
- Cloud Composer — documentation : https://cloud.google.com/composer/docs
- Budgets et alertes de facturation : https://cloud.google.com/billing/docs/how-to/budgets
- BigQuery — tarification : https://cloud.google.com/bigquery/pricing
- BigQuery — tables partitionnées : https://cloud.google.com/bigquery/docs/partitioned-tables
- BigQuery — clustering : https://cloud.google.com/bigquery/docs/clustered-tables
- BigQuery — chargement de fichiers Parquet : https://cloud.google.com/bigquery/docs/loading-data-cloud-storage-parquet
- Cloud Storage — documentation : https://cloud.google.com/storage/docs
- IAM — bonnes pratiques et moindre privilège : https://cloud.google.com/iam/docs/using-iam-securely
- dbt-bigquery (adaptateur) : https://docs.getdbt.com/docs/core/connect-data-platform/bigquery-setup
- dbt — tests de données : https://docs.getdbt.com/docs/build/data-tests
- Airflow — backfill et rattrapage : https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dag-run.html
- Airflow — API TaskFlow : https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/taskflow.html
- Airflow — mapping dynamique de tâches : https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/dynamic-task-mapping.html
- Airflow — opérateurs différés et capteurs : https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/deferring.html
- Airflow — planification pilotée par les données (assets) : https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/asset-scheduling.html
- Airflow — branchement conditionnel : https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html#branching
- Airflow — pools et contrôle de la concurrence : https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/pools.html
- Airflow — rappels et notifications : https://airflow.apache.org/docs/apache-airflow/stable/administration-and-deployment/logging-monitoring/callbacks.html
- Airflow — connexions et variables : https://airflow.apache.org/docs/apache-airflow/stable/authoring-and-scheduling/connections.html
- Airflow — tester ses DAG : https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html#testing-a-dag
- Airflow — bonnes pratiques d'écriture : https://airflow.apache.org/docs/apache-airflow/stable/best-practices.html
- Terraform — provider Google (bonus) : https://registry.terraform.io/providers/hashicorp/google/latest/docs
