# Brief : Où positionner les taxis new-yorkais — pipeline orchestré Snowflake + dbt + Airflow

## Informations

| Critère | Valeur |
|---------|--------|
| **Durée** | 5 jours (35 heures) |
| **Niveau** | Intermédiaire |
| **Modalité** | Individuel |
| **Technologies** | Snowflake, dbt Core (dbt-snowflake), Apache Airflow, Python, Parquet, Docker & Docker Compose, SQL, Git |
| **Prérequis** | [Cours Python](../../../01-Fondamentaux/Python/) + [Cours SQL](../../../01-Fondamentaux/SQL/) + [Cours Docker](../../../02-Containerisation/Docker/) + [Cours dbt](../../../06-Data-Engineering/Dbt/) + [Cours Airflow](../../../06-Data-Engineering/Airflow/) |
| **Données** | **100 % réelles** — NYC Taxi & Limousine Commission, ~40 M de trajets, ~8 Go de Parquet |
| **Coût** | 0 € — essai Snowflake 30 jours (~400 $ de crédits), **sans carte bancaire** |

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

Votre directrice technique veut trois choses : des chiffres reproductibles, un pipeline qui se
relance tout seul chaque mois quand la commission new-yorkaise publie un nouveau fichier, et une
**maîtrise des coûts** — Fleetwise démarre sur un entrepôt cloud facturé à l'usage, et elle ne
veut pas découvrir la facture en fin de mois.

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
  Colonnes principales : horodatages de prise en charge et de dépose, distance, montants
  (course, pourboire, péages, total), zones de départ et d'arrivée, type de paiement, nombre de
  passagers.
- **Référentiel des zones** : `https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv`
  (12 Ko) — correspondance entre les identifiants de zone et leurs noms, arrondissements et
  quartiers de service. Sans lui, vos analyses parlent de « la zone 132 » plutôt que de « JFK ».
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

S'y ajoute une contrainte que les autres variantes de ce brief n'ont pas : **chaque requête
coûte**. Un `SELECT *` lancé par curiosité sur 40 millions de lignes consomme des crédits que
vous ne récupérerez pas. La sobriété n'est pas une posture ici, c'est une compétence évaluée.

### Contraintes techniques

- **Snowflake** comme entrepôt, via l'**essai gratuit de 30 jours** (environ 400 $ de crédits,
  aucune carte bancaire requise). Créez votre compte **le premier jour** : l'essai court à partir
  de la création, pas à partir de votre premier usage.
- **Airflow auto-hébergé** via Docker Compose (fourni) et **dbt Core** avec l'adaptateur
  `dbt-snowflake`.
- **Maîtrise des crédits — c'est un livrable, pas un conseil.** Warehouse de taille modeste,
  `AUTO_SUSPEND` court, et suivi de la consommation. Vous rendrez un relevé de vos crédits
  consommés avec son commentaire.
- **Aucun identifiant Snowflake dans le dépôt.** Ni dans un `profiles.yml`, ni dans un DAG, ni
  dans un notebook. Utilisez des variables d'environnement et un `.env` non versionné.
- Le pipeline est **rejouable et idempotent**, et doit supporter un **backfill** depuis janvier
  2024 avant de fonctionner mensuellement.
- Tout le code est **versionné sur GitHub dès le premier jour**.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **Créer et paramétrer un entrepôt cloud** : base, schémas en couches, warehouse dimensionné et
  suspendu automatiquement, rôles ;
- **Automatiser l'ingestion** de fichiers volumineux vers l'entrepôt, avec gestion des erreurs,
  reprise et journalisation ;
- **Transformer les données avec dbt Core** : modèles en couches, tests de qualité, documentation
  et lignage générés ;
- **Orchestrer en utilisateur avancé d'Airflow** : API TaskFlow, mapping dynamique de tâches,
  capteurs différés, déclenchement piloté par la donnée, branchement conditionnel, reprises,
  pools, rappels de défaillance, gestion des secrets et **tests automatisés de DAG** — le tout
  en maîtrisant la distinction entre date logique et date du jour ;
- **Traiter une évolution de schéma** entre deux périodes sans casser l'historique déjà chargé ;
- **Piloter le coût** d'une plateforme facturée à l'usage, et justifier ses arbitrages.

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

Un pipeline ELT en trois couches dans Snowflake, orchestré par un Airflow auto-hébergé.

```
   NYC TLC — fichiers Parquet mensuels (~3 M lignes / mois)
   + référentiel des zones (CSV)
                    |
        +-----------v------------------------------------+
        |  AIRFLOW (Docker Compose, sur votre machine)   |
        |  DAG mensuel + backfill depuis 2024-01         |
        |                                                |
        |   [charger RAW] -> [dbt run] -> [dbt test]     |
        +-----------+------------------------------------+
                    |
        +-----------v------------------------------------+
        |  SNOWFLAKE                                     |
        |  warehouse dimensionné + AUTO_SUSPEND          |
        |                                                |
        |   schéma RAW      : données brutes, 1 table    |
        |        |            par source, non modifiées  |
        |        v                                       |
        |   schéma STAGING  : nettoyage, typage,         |
        |        |            règles de rejet tracées    |
        |        v                                       |
        |   schéma MARTS    : tables d'analyse (dbt)     |
        +-----------+------------------------------------+
                    |
        +-----------v------------------------------------+
        |  RESTITUTION + SUIVI DES CRÉDITS CONSOMMÉS     |
        +------------------------------------------------+
```

> Vous produirez votre propre schéma d'architecture **au format image** (draw.io ou équivalent,
> pas d'ASCII art) à joindre au rendu.

## Données fournies

Le kit de démarrage se trouve dans le dossier [`starter-kit-airflow/`](starter-kit-airflow/) :

```bash
cp .env.example .env      # renseignez vos identifiants Snowflake
docker compose up -d
# interface Airflow : http://localhost:8080
```

- `docker-compose.yml` — **Airflow** (mode standalone, testé) avec `dbt-snowflake` préinstallé et
  les dossiers `dags/`, `dbt/` montés depuis votre projet ;
- `.env.example` — variables d'environnement, dont la connexion Snowflake (aucun secret réel) ;
- `dbt/` — un squelette dbt : `dbt_project.yml` et un profil Snowflake d'exemple ;
- `.gitignore` — empêche de committer `.env`, `profiles.yml` et les fichiers de données ;
- `README.md` — mise en route et pièges connus.

**Ne sont pas fournis, et constituent le sujet du brief** : la création de l'infrastructure
Snowflake (base, schémas, warehouse, rôles), le DAG, les scripts d'ingestion, les modèles dbt et
les tests.

## Travail demandé

Travail individuel sur 5 jours. L'entraide est encouragée, mais chacun rend son propre code et
doit pouvoir l'expliquer ligne par ligne.

> **Règle des 2 heures.** **Bloqué plus de 2 heures sur le même point ? Demandez un indice au
> formateur.** Notez le blocage et sa résolution dans votre journal de bord, qui fait partie du
> rendu.
>
> **Travaillez sur 2 mois, pas sur 24**, et sur un warehouse modeste. Le backfill complet se
> lance une seule fois, en Phase 4. Développer sur 40 millions de lignes brûle vos crédits sans
> rien vous apprendre de plus.

### Phase 1 — Cadrage, compte Snowflake et exploration (J1)

Créez votre compte d'essai **dès la première heure** — le compte à rebours des 30 jours démarre
là. Créez ensuite la base, les schémas en couches, et un warehouse : quelle taille choisissez-vous,
et quel `AUTO_SUSPEND` ? Sachez justifier les deux, on vous le demandera.

Explorez le jeu de données sans encore tout charger : téléchargez un mois, regardez-le localement
(DuckDB ou pandas font très bien l'affaire pour ça, et gratuitement). Combien de lignes, quelles
colonnes, quels types ? Comparez le schéma de `2024-01` et celui du mois le plus récent :
qu'est-ce qui a changé ?

Mesurez vous-même les anomalies annoncées dans ce brief plutôt que de les recopier. Décidez, pour
chaque anomalie, ce que vous en ferez — et **pourquoi**. Un trajet à montant négatif est-il une
erreur à jeter ou une annulation à conserver ?

Définissez enfin vos indicateurs : qu'est-ce, précisément, qu'une « heure de service » quand on
ne dispose que des trajets facturés ? Documentez les sources dans `docs/sources.md` et ouvrez un
**Kanban public**.

**Résultat testable en fin de J1 (point de contrôle formateur) :** compte créé et infrastructure
Snowflake en place avec ses choix justifiés, anomalies mesurées et chiffrées, différences de
schéma identifiées, indicateurs définis, Kanban rempli.

### Phase 2 — Ingestion et couche brute (J2)

Chargez **un mois** dans le schéma brut, sans transformation, puis le référentiel des zones.
Deux voies s'offrent à vous : un **stage externe** Snowflake qui lit directement depuis la source,
ou un script Python qui télécharge puis charge. Choisissez, et justifiez au regard du coût, de la
robustesse et de ce que vous saurez orchestrer ensuite.

Que fait votre chargement si le fichier n'existe pas encore parce que la commission n'a pas
publié ? S'il est interrompu à mi-parcours ? Si vous relancez le même mois deux fois — la couche
brute double-t-elle ? Comment savez-vous, en interrogeant l'entrepôt, quels mois sont déjà
chargés ?

Ne cherchez pas encore à orchestrer : un chargement paramétré par un mois, lançable à la main,
suffit.

**Résultat testable en fin de J2 :** deux mois chargés en couche brute, un rechargement du même
mois ne crée aucun doublon, le référentiel des zones est joignable.

### Phase 3 — Transformation dbt (J3)

Construisez vos modèles dbt en deux niveaux : **staging** (nettoyage, typage, règles de rejet
décidées en Phase 1) puis **marts** (tables d'analyse).

Chaque règle de rejet est **écrite dans le modèle** et son effet est mesurable : combien de lignes
écartées, pour quelle raison ? Où tracez-vous les rejets pour pouvoir en rendre compte ?

Écrivez des **tests dbt** : unicité, non-nullité, valeurs acceptées, cohérence métier. Quel seuil
rend un test bloquant plutôt qu'informatif ?

Vos marts doivent répondre à la question centrale. Le revenu par heure de service par zone et par
créneau en est le cœur ; ajoutez ce qui l'éclaire. Générez la documentation dbt et vérifiez que le
**lignage** est lisible.

Surveillez vos crédits au passage : un modèle matérialisé en table coûte à chaque exécution, une
vue coûte à chaque lecture. Lequel choisissez-vous, et pour quel modèle ?

**Résultat testable en fin de J3 (point de contrôle formateur) :** `dbt run` et `dbt test` passent
sur deux mois, `dbt docs` montre le lignage, et une requête sur les marts propose une première
réponse à la question centrale.

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

Produisez le **relevé de consommation de crédits** et commentez-le : qu'est-ce qui a coûté le
plus cher — le backfill, les modèles matérialisés en table, un warehouse oublié allumé ? Et
qu'auriez-vous fait autrement en le sachant dès J1 ?

### Socle commun (obligatoire)

- Infrastructure Snowflake créée et justifiée : base, schémas en couches, warehouse dimensionné
  avec `AUTO_SUSPEND`.
- Ingestion automatisée avec gestion des erreurs, reprise et journalisation.
- Modèles dbt en couches avec **tests** et **documentation générée** (lignage lisible), règles de
  rejet écrites, tracées et chiffrées.
- **DAG Airflow** écrit en **API TaskFlow**, avec **mapping dynamique** des mois, reprises et
  temporisation, **pool** limitant la concurrence, **backfill complet depuis 2024-01** et
  idempotence démontrée. Le mois traité est déduit de la **date logique**, jamais de `now()`.
- **Airflow avancé** : capteur **différé** sur la publication du fichier, **déclenchement piloté
  par la donnée** entre ingestion et transformation, **branchement conditionnel** sur les cas de
  bord, **rappel de défaillance** produisant une notification exploitable, secrets et chemins
  sortis du code via connexions et variables.
- **Tests automatisés des DAG** : au minimum absence d'erreur d'import et vérification de la
  structure attendue.
- **Traitement documenté du changement de schéma** entre périodes.
- **Relevé de consommation de crédits** commenté.
- Réponse chiffrée à la question centrale.
- Repo public documenté, schéma d'architecture, Kanban, journal de bord, **aucun identifiant
  versionné**.

### Pour aller plus loin (bonus)

- Chargement incrémental via **Snowpipe** plutôt que par lots.
- Ajouter les taxis **verts** (`green_tripdata_*`) et réconcilier les deux jeux.
- Comparer le coût et la durée du backfill sur deux tailles de warehouse, chiffres à l'appui.
- Dashboard **Streamlit** branché sur Snowflake.
- Alerte Airflow sur échec de `dbt test`.

Les bonus ne compensent jamais un socle incomplet : **terminez d'abord le socle**.

## Livrables

À rendre au plus tard J5 à 17 h (lien du repo posté sur la plateforme) :

- Un **repo GitHub public** avec un README structuré : description, question centrale,
  technologies et justification, installation et lancement pas à pas, architecture, auteur.
- Les **scripts de création de l'infrastructure** Snowflake (SQL versionné) : base, schémas,
  warehouse, rôles.
- Le **DAG Airflow** et les **scripts d'ingestion**, avec gestion des erreurs et journalisation.
- Les **tests automatisés des DAG** (dossier `tests/`) et la commande pour les lancer.
- Le **projet dbt** : modèles staging et marts, tests, documentation générée (ou captures).
- La **documentation des sources** (`docs/sources.md`) : format, volume, colonnes, anomalies
  **mesurées** avec leurs pourcentages réels.
- La **note sur le changement de schéma** et le **décompte des rejets** par règle.
- Le **relevé de consommation de crédits** avec son commentaire : ce qui a coûté, ce que vous
  feriez autrement.
- Le **schéma d'architecture** au format image — pas d'ASCII.
- La **note de restitution** (une page) répondant à la question centrale.
- Le lien vers le **Kanban public**, le **journal de bord**, et une **preuve du backfill**
  (grille Airflow ou logs).
- Un `.env.example` sans secret, et **aucun identifiant Snowflake dans l'historique Git**.

## Démonstration finale

**Volet 1 — Démonstration technique individuelle : 70 %.** 15 minutes + 10 minutes de questions.
Vous montrez l'interface Airflow et le DAG, déclenchez une exécution en direct sur un mois,
montrez les tests dbt, la documentation et le lignage, puis répondez à la question centrale depuis
vos marts. Vous démontrez l'**idempotence** en rejouant un mois déjà chargé, et présentez votre
consommation de crédits.

Les questions porteront sur vos choix : taille du warehouse et `AUTO_SUSPEND`, stage externe ou
chargement Python, matérialisation des modèles, règles de rejet, gestion du changement de schéma.

**Volet 2 — Revue de code et d'architecture : 30 %.** Structure du repo, lisibilité du DAG et des
modèles, qualité des tests, documentation, **absence de secrets versionnés**, régularité des
commits.

> **Validation partielle** : un pipeline non fonctionnel en démonstration mais dont le code est
> structuré, versionné et documenté peut valider partiellement les compétences concernées.
> L'ingestion, la transformation et l'orchestration sont évaluées indépendamment. En revanche, un
> identifiant Snowflake trouvé dans l'historique Git invalide le critère de sécurité, quel que
> soit le reste.

## Critères de validation

### Création et paramétrage de l'entrepôt

- La base, les schémas en couches et le warehouse sont créés par un **script SQL versionné**, pas
  à la main dans l'interface.
- La taille du warehouse et le délai d'`AUTO_SUSPEND` sont justifiés au regard du volume et du
  budget.
- La consommation de crédits est suivie, restituée et commentée.
- Aucun identifiant n'apparaît dans le dépôt ni dans son historique.

### Automatisation de l'ingestion

- Le chargement est fonctionnel et récupère effectivement les données visées ; la voie retenue
  (stage externe ou script) est justifiée.
- Les erreurs (fichier absent, chargement interrompu) sont gérées selon une stratégie explicite et
  journalisées.
- Le rechargement d'un mois déjà traité ne crée ni doublon ni perte, vérifiable en base.
- Le code est versionné avec un historique réparti sur la durée du projet.

### Transformation et qualité (dbt)

- Les modèles sont organisés en couches et produisent des résultats corrects et vérifiables.
- Les règles de nettoyage sont écrites en code et le nombre de lignes écartées par règle est
  mesurable.
- Des tests dbt couvrent unicité, non-nullité et cohérence métier ; leur conduite en cas d'échec
  est explicite.
- La documentation est générée et le lignage est lisible de la source aux marts.

### Orchestration (Airflow)

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

### Restitution

- Les indicateurs répondent à la question centrale, et non à un simple décompte.
- La définition de chaque indicateur est écrite : formule, granularité, période.
- La note de restitution tranche et s'appuie sur des chiffres issus du pipeline.

## Ressources

- [Cours Python](../../../01-Fondamentaux/Python/) · [Cours SQL](../../../01-Fondamentaux/SQL/) · [Cours Docker](../../../02-Containerisation/Docker/)
- [Cours dbt](../../../06-Data-Engineering/Dbt/) · [Cours Airflow](../../../06-Data-Engineering/Airflow/)
- NYC TLC — page officielle des données de trajets : https://www.nyc.gov/site/tlc/about/tlc-trip-record-data.page
- Dictionnaire officiel des données (Yellow Taxi) : https://www.nyc.gov/assets/tlc/downloads/pdf/data_dictionary_trip_records_yellow.pdf
- Référentiel des zones : https://d37ci6vzurychx.cloudfront.net/misc/taxi_zone_lookup.csv
- Snowflake — essai gratuit : https://signup.snowflake.com
- Snowflake — documentation officielle : https://docs.snowflake.com
- Snowflake — warehouses et `AUTO_SUSPEND` : https://docs.snowflake.com/en/user-guide/warehouses-overview
- Snowflake — chargement depuis un stage externe : https://docs.snowflake.com/en/user-guide/data-load-s3
- Snowflake — suivi de la consommation de crédits : https://docs.snowflake.com/en/user-guide/cost-understanding-compute
- dbt-snowflake (adaptateur) : https://docs.getdbt.com/docs/core/connect-data-platform/snowflake-setup
- dbt — tests de données : https://docs.getdbt.com/docs/build/data-tests
- dbt — matérialisations (table, vue, incrémental) : https://docs.getdbt.com/docs/build/materializations
- Airflow — écrire un DAG : https://airflow.apache.org/docs/apache-airflow/stable/core-concepts/dags.html
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
