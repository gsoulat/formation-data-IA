# Brief : Gouverner une base publique nominative — catalogue, PII et RGPD sur Transparence-Santé

## Informations

| Critère | Valeur |
|---------|--------|
| **Durée** | 5 jours (35 heures) |
| **Niveau** | Intermédiaire |
| **Modalité** | Individuel |
| **Technologies** | OpenMetadata, MinIO (stockage objet S3), PostgreSQL, Docker & Docker Compose, Python (boto3), SQL, RBAC & Row Level Security, RGPD, Git |
| **Prérequis** | [Cours SQL](../../../01-Fondamentaux/SQL/) + [Cours Docker](../../../02-Containerisation/Docker/) + [RGPD & Gouvernance](../../../01-Fondamentaux/RGPD-Gouvernance/) + [Cours OpenMetadata](../../../06-Data-Engineering/OpenMetadata/) + [Cours Data Lake](../../../05-Databases/DataLake/) |
| **Données** | **100 % réelles et nominatives** — base publique de l'État, ~10,1 M de déclarations, ~1 M de personnes nommées |

## Contexte

### L'organisation

**Éclairage** est une association loi 1901 de 12 personnes qui publie des analyses sur les liens entre l'industrie de santé et les professionnels de santé. Elle vit de subventions et de dons, travaille avec des journalistes et des chercheurs, et n'a aucun budget de licence logicielle. Vous êtes son premier data engineer ; la déléguée à la protection des données est une bénévole juriste, disponible une demi-journée par semaine.

### La matière première

L'État publie **Transparence-Santé**, la base des avantages, conventions et rémunérations versés par les industriels de santé aux professionnels de santé, au titre du dispositif de transparence des liens d'intérêts prévu par le code de la santé publique. Elle est ouverte, réutilisable, et **nominative** : environ **10,1 millions de déclarations** rattachées à environ **1 million de bénéficiaires nommés** (nom, prénom, profession, spécialité, commune d'exercice) et **4 600 entreprises déclarantes**.

C'est précisément ce qui rend le sujet sérieux. Une donnée personnelle **publiée légalement** ne devient pas une donnée libre de tout droit : la réutiliser dans vos propres traitements reste un **traitement de données à caractère personnel** soumis au RGPD. Éclairage a donc les mêmes obligations qu'une entreprise qui traiterait un fichier client.

### Le problème

Trois incidents ont eu lieu ce trimestre.

Un stagiaire a récupéré un export nominatif de 200 000 lignes **déposé sur l'espace de stockage partagé** de l'association et l'a recopié sur son ordinateur portable personnel pour « travailler le week-end ». Personne ne savait qu'il en avait le droit ou non, parce que personne n'avait écrit la règle — et surtout, personne ne savait que ce fichier était là.

Un partenaire presse a demandé un accès à la base pour préparer une enquête. La question « on lui donne quoi, exactement ? » est restée sans réponse pendant trois semaines, faute de savoir quelles tables contiennent quoi.

Enfin, une analyse publiée en mars s'est révélée fausse. Le chargé d'études avait travaillé sur un jeu dont il ignorait qu'il n'était pas celui qui fait foi : le catalogue public expose plusieurs jeux aux noms très voisins, dont certains portent visiblement des suffixes de recette ou de copie, avec des volumétries presque — mais pas tout à fait — identiques. Personne, chez Éclairage, ne savait lequel était la référence.

Votre mission : mettre en place le catalogue et les règles de gouvernance qui rendent ces trois incidents impossibles.

### La question centrale

Tout votre travail doit permettre d'y répondre, et vous devez pouvoir vous y référer à chaque étape :

> **« Qui a le droit de voir le nom d'un professionnel de santé, et cette donnée est-elle digne de confiance ? »**

### Les deux zones de stockage

Le premier incident dit l'essentiel : **la donnée d'Éclairage ne vit pas qu'en base**. Elle arrive d'abord sous forme de fichiers d'export, déposés dans un espace de stockage objet, avant qu'un sous-ensemble travaillé ne rejoigne la base analytique. Un catalogue qui ne verrait que la base documenterait la fin de la chaîne en ignorant son début — et l'export du stagiaire resterait invisible.

Vous travaillerez donc sur **deux zones**, et vous les cataloguerez toutes les deux :

- **Zone brute — MinIO** (stockage objet compatible S3, fourni dans le kit) : les fichiers d'export tels que récupérés depuis l'API publique, horodatés, jamais modifiés. C'est ici qu'atterrissent les données nominatives, et c'est ici que dormait le fichier du stagiaire.
- **Zone travaillée — PostgreSQL** (fourni dans le kit) : le périmètre retenu, chargé et exploitable par les chargés d'études.

L'**organisation interne** de ces zones — combien de buckets, quel nommage, quel partitionnement, quelle politique de rétention — n'est pas donnée : c'est votre travail de conception, et vous la justifierez.

### La source de données

Une seule source, réelle et publique, exposée par une API Opendatasoft Explore v2.1 sans authentification :

- **Portail** : `https://www.transparence.sante.gouv.fr`
- **Catalogue des jeux** : `https://www.transparence.sante.gouv.fr/api/explore/v2.1/catalog/datasets`
- **Enregistrements d'un jeu** : `.../api/explore/v2.1/catalog/datasets/{dataset_id}/records`

Le catalogue expose une **dizaine de jeux** dont, notamment, les déclarations (~10,1 M de lignes), les bénéficiaires (~1 M, nominatifs), les entreprises déclarantes (~4 600), les semestres de référence et plusieurs référentiels. **C'est à vous d'aller inventorier ce catalogue en Phase 1** : ce brief ne vous en donne pas la liste.

### Ce qui rend ce brief différent d'un exercice

Le « grenier » que vous devez ranger n'a pas été fabriqué pour vous : c'est le catalogue réel d'une plateforme de l'État, avec ce qu'un catalogue réel contient toujours.

- **Des jeux qui se ressemblent trop.** Vous trouverez des identifiants portant des suffixes évoquant la recette ou la copie, parfois empilés (`...-copie-copie`, `...-copie0`), à côté du jeu principal. Sur les déclarations, deux jeux affichent une volumétrie qui ne diffère que de quelques centaines de lignes sur plus de dix millions. Lequel fait foi ? Comment le prouvez-vous, autrement qu'en croyant le nom ?
- **Des données personnelles qui n'ont pas l'air d'en être.** Le nom d'un médecin est une donnée personnelle évidente. Mais le montant qu'il a reçu ? Sa spécialité croisée avec sa commune d'exercice, dans un village de 400 habitants ? Où s'arrête l'identification indirecte ?
- **Une base légale à établir, pas à recopier.** Le fait que la source soit publique ne vous dispense pas de déterminer sur quel fondement Éclairage traite ces données, ni pendant combien de temps elle peut les conserver.
- **Une volumétrie qui ne rentre pas dans la journée.** Dix millions de lignes via une API paginée qui plafonne, ce n'est pas une extraction, c'est une décision de périmètre. Laquelle prenez-vous, et comment la justifiez-vous ?
- **Un catalogue ne scanne pas un bucket comme une base.** Une base expose un schéma ; un stockage objet n'expose que des chemins et des fichiers. Le format que vous choisissez pour vos exports et la façon dont vous organisez vos préfixes déterminent ce que le catalogue saura en dire. Ce n'est pas un détail de rangement.

### Contraintes techniques

- **Le périmètre de données est à maîtriser, pas à maximiser** : vous ingérez un sous-ensemble raisonné (un ou deux semestres, ou un échantillon d'entreprises déclarantes) et vous **justifiez ce découpage**. Charger dix millions de lignes n'apporte aucun point.
- **Toute l'infrastructure est fournie** en un seul `docker compose up -d` : MinIO, PostgreSQL et OpenMetadata.
- **Contrainte RAM — lisez ceci en premier.** La stack complète demande **environ 4,7 Go** (mesuré : moteur de recherche 1,6 Go, service d'ingestion 1,9 Go, serveur 0,9 Go, le reste négligeable). Sur une machine de 8 Go, c'est jouable mais serré : fermez navigateur superflu et IDE lourds. **Vérifiez `docker info | grep "Total Memory"` dès la première heure** et signalez tout blocage. Deux soupapes sont documentées dans l'en-tête du `docker-compose.yml` : arrêter le service d'ingestion planifiée (~1 Go gagné, les ingestions se lancent alors en ligne de commande) et réduire la mémoire du moteur de recherche. En dernier recours seulement, la **sandbox en ligne** (https://sandbox.open-metadata.org) est un repli acceptable pour les fonctionnalités d'enrichissement, à condition de le documenter précisément.
- Les droits d'accès sont portés par des **groupes ou des rôles**, jamais par des comptes individuels.
- **Aucun secret** (mot de passe, token, clé d'accès S3) versionné dans le dépôt.
- **Aucune donnée nominative versionnée** dans le dépôt Git, sous aucune forme, même en extrait de test. Cette règle n'est pas négociable : la violer suffit à invalider le rendu.
- Tout le travail est **versionné avec Git**, sur un repo GitHub public.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **Concevoir les zones de stockage** d'un data lake : définir leur découpage, leur nommage, leurs formats et leurs règles d'accès, et justifier ces choix ;
- **Intégrer les composants d'une infrastructure de données** : connecter un catalogue à un **stockage objet** et à une **base relationnelle**, en maîtrisant la topologie réseau qui les relie, et documenter une procédure reproductible ;
- **Cartographier les données disponibles** en référençant leurs usages, leurs sources et leurs métadonnées, et en formalisant une topographie en quatre parties ;
- **Établir quel jeu fait foi** dans un catalogue réel encombré de doublons, par l'analyse et non par la confiance dans les noms ;
- **Gérer le catalogue des données** avec OpenMetadata : ingestion des métadonnées, descriptions, glossaire métier, lignage, tests de qualité ;
- **Classifier des données personnelles** en distinguant identification directe et indirecte, et en justifiant chaque classement ;
- **Implémenter les règles de gouvernance** en traduisant des besoins d'accès réels en rôles, politiques et masquage conformes au RGPD.

## Architecture cible

Le pattern visé est un **catalogue centralisé couvrant deux zones de stockage, adossé à une gouvernance par rôles** : extraction raisonnée depuis l'API publique → dépôt des fichiers bruts dans MinIO → chargement du périmètre travaillé dans PostgreSQL → OpenMetadata ingère les métadonnées **des deux zones**, les enrichit (descriptions, glossaire, tags PII), y exécute des tests de qualité, et sert de support aux politiques d'accès.

```
        +------------------------------------------------------+
        |   API publique Transparence-Santé (Explore v2.1)      |
        |   déclarations / bénéficiaires / entreprises / réf.   |
        |   + jeux "recette", "copie", "copie-copie"...         |
        +--------------------------+---------------------------+
                                   |
                [ Extraction raisonnée — périmètre justifié ]
                                   |
         +-------------------------+-------------------------+
         |                                                   |
+--------v---------------------+              +--------------v---------------+
|   ZONE BRUTE — MinIO (S3)    |              | ZONE TRAVAILLEE — PostgreSQL |
|   fichiers d'export datés,   |  --------->  | périmètre retenu, exploitable|
|   immuables, nominatifs      |              | par les chargés d'études     |
|   (buckets/préfixes : à VOUS)|              | (schémas : à VOUS)           |
+--------+---------------------+              +--------------+---------------+
         |                                                   |
         +------------------+--------------------------------+
                            |
              [ Ingestion des métadonnées des DEUX zones ]
                            |
        +-------------------v----------------------------------+
        |                  OPENMETADATA                        |
        |          (Docker Compose officiel, ou sandbox)       |
        +-------------------+----------------------------------+
                            |
        +-----------+-------+--------+-----------------+
        |           |                |                 |
  +-----v-----+ +---v--------+  +----v---------+ +-----v--------+
  | CATALOGUE | |  QUALITE   |  |    ACCES     | | CYCLE DE VIE |
  | glossaire | | fraîcheur  |  | rôles / PG   | | registre des |
  | descript. | | complétude |  | policies OM  | | traitements  |
  | tags PII  | | unicité    |  | masquage     | | rétention    |
  | lignage   | | jeu qui    |  | (analyste /  | | suppression  |
  |           | | fait foi   |  |  presse / DE)| | des exports  |
  +-----+-----+ +---+--------+  +----+---------+ +-----+--------+
        |           |                |                 |
        +-----------+-------+--------+-----------------+
                            |
        +-------------------v----------------------------------+
        |  TOPOGRAPHIE EN 4 PARTIES                            |
        |  sémantique / modèles / traitements et flux /        |
        |  mise à disposition et conditions d'accès            |
        +------------------------------------------------------+
```

> Vous produirez votre propre schéma d'architecture **au format image** (draw.io ou équivalent, pas d'ASCII art) à joindre au rendu, faisant apparaître les deux zones.

## Données fournies

Le kit de démarrage se trouve dans le dossier [`starter-kit/`](starter-kit/). Il fournit **toute l'infrastructure, en une seule commande** :

```bash
cp .env.example .env      # puis adaptez les mots de passe
docker compose up -d
docker compose ps         # attendez que tout soit "healthy" (5 à 10 min au 1er lancement)
```

- `docker-compose.yml` — **MinIO** (zone brute, S3), **PostgreSQL 16** (zone travaillée) et **OpenMetadata**, assemblés et testés. Son en-tête documente les précautions RAM, les soupapes en cas de machine juste, et les pièges connus ;
- `openmetadata/docker-compose-postgres.yml` — le compose **officiel** d'OpenMetadata 1.13.1, **non modifié**, simplement inclus par le précédent. Le garder intact permet de le mettre à jour en remplaçant le fichier ;
- `.env.example` — variables d'environnement d'exemple (aucun secret réel) ;
- `source.md` — le point d'entrée de l'API et les premières commandes d'exploration ;
- `.gitignore` — pré-rempli pour empêcher tout versionnement accidentel de données nominatives ;
- `dbt/` — un squelette de projet dbt **pour le bonus lignage uniquement**. Il ne fait pas partie du socle.

L'infrastructure vous est donnée parce que **taper un `docker compose` d'outil n'est pas une compétence** : la recopie de la documentation officielle ne s'évalue pas. Ce qui s'évalue, et qui constitue le sujet du brief :

- **la conception des zones** : quels buckets, quel nommage, quels formats, quelle rétention — aucun bucket n'est créé ;
- **la connexion du catalogue à vos deux sources**, qui suppose de comprendre la topologie réseau (depuis OpenMetadata, votre base n'est pas sur `localhost`) ;
- les **schémas PostgreSQL**, les **scripts d'extraction et de chargement**, et **toute la configuration du catalogue** : ingestion, glossaire, tags, tests, rôles.

Vous devez en revanche **savoir expliquer ce que démarre ce compose** : serveur, base de métadonnées, moteur de recherche, service d'ingestion. On vous le demandera en soutenance.

## Travail demandé

Travail individuel sur 5 jours. L'entraide est encouragée — confrontez vos classifications PII, elles feront débat — mais chaque configuration et chaque livrable est personnel. Le formateur joue le rôle de la déléguée à la protection des données : sollicitez-le pour arbitrer vos décisions RGPD, comme vous le feriez en association.

> **Règle des 2 heures.** Le catalogue est réel, avec ses incohérences, et OpenMetadata est un outil lourd. **Bloqué plus de 2 heures sur le même point ? Demandez un indice au formateur.** Notez le blocage et sa résolution dans votre journal de bord, qui fait partie du rendu.
>
> **Vérifiez votre RAM à la première heure.** `docker info | grep "Total Memory"`. Si Docker dispose de moins de 6 Go, dites-le tout de suite : le repli sandbox se prépare, il ne s'improvise pas le matin de J3.

### Phase 1 — Inventaire du catalogue public et enquête sur le jeu qui fait foi (J1)

Aucun chargement de données. Vous auditez.

Appelez le point d'entrée `catalog/datasets` et listez **tous** les jeux exposés, avec pour chacun son identifiant, sa volumétrie annoncée et ce qu'il semble contenir. Combien y en a-t-il ? Combien vous paraissent redondants ?

Menez ensuite l'enquête qui manquait à Éclairage en mars. Deux jeux de déclarations affichent des volumétries presque identiques : lequel fait foi ? Que disent leurs dates de dernière mise à jour, leurs métadonnées, un échantillon comparé ligne à ligne ? Écrivez votre conclusion **et la méthode qui vous y a mené** : c'est cette méthode qu'un collègue rejouera dans six mois.

Repérez enfin où se trouvent les données personnelles, et lesquelles identifient une personne **directement** (le nom) ou **indirectement** (un croisement). Ouvrez votre **Kanban public** avec des user stories formulées du point de vue des utilisateurs : « En tant que chargé d'études, je veux savoir en moins de deux minutes quelle table de déclarations fait foi ».

Terminez par la conception de vos **zones de stockage**, sur papier : combien de buckets, quel nommage, quels préfixes, quel format de fichier, quelle durée de rétention pour la zone brute ? Anticipez la suite — un catalogue saura décrire un Parquet ou un CSV bien rangé bien mieux qu'un JSON imbriqué déposé en vrac.

**Résultat testable en fin de J1 (point de contrôle formateur) :** inventaire complet du catalogue public, conclusion argumentée sur le jeu qui fait foi, premier repérage des données personnelles, conception écrite des zones, Kanban alimenté, RAM vérifiée.

### Phase 2 — Démarrage de la stack et alimentation des deux zones (J2)

Démarrez toute la stack (`docker compose up -d` — comptez 5 à 10 min au premier lancement, le temps de télécharger les images) et **créez vos buckets** selon la conception de la Phase 1. OpenMetadata démarre en même temps ; vous ne vous en servirez qu'en Phase 3, mais vérifiez dès maintenant que son interface répond sur `http://localhost:8585`, pour ne pas découvrir un problème de mémoire demain matin.

Décidez votre **périmètre** et défendez-le : quel semestre, quelles entreprises, quel volume — et pourquoi celui-là sert la question centrale. Un périmètre étroit et justifié vaut mieux qu'un périmètre large et subi.

Extrayez ensuite, en alimentant les **deux zones** : les fichiers d'export bruts, datés, dans MinIO ; le périmètre travaillé dans PostgreSQL. L'API plafonne sa pagination : comment contournez-vous la limite, et que faites-vous si l'extraction s'interrompt à mi-parcours ? Vos scripts doivent journaliser ce qu'ils font et pouvoir être relancés sans tout recommencer.

Documentez au fil de l'eau la **procédure d'installation** : un tiers doit pouvoir la dérouler sans erreur.

**Résultat testable en fin de J2 :** buckets créés et peuplés de fichiers datés, périmètre chargé dans PostgreSQL, procédure d'installation rédigée, et aucune donnée nominative dans le dépôt Git.

### Phase 3 — Connecter le catalogue aux deux sources et donner du sens (J3)

La journée la plus technique. OpenMetadata tourne déjà — il est démarré par le même `docker compose` que le reste depuis la Phase 2. Ouvrez son interface sur `http://localhost:8585` et connectez-vous.

Avant de configurer quoi que ce soit, prenez vingt minutes pour comprendre **ce que vous avez démarré** : `docker compose ps` liste six services. Lesquels appartiennent à OpenMetadata, et à quoi sert chacun — le serveur, sa base de métadonnées, le moteur de recherche, le service d'ingestion ? Pourquoi un catalogue a-t-il besoin d'un moteur de recherche ? Et surtout : la base PostgreSQL qu'OpenMetadata embarque, contient-elle vos données ou les siennes ? Cette question sera posée en soutenance.

Connectez ensuite **les deux sources**. La base PostgreSQL est le cas simple et documenté… à une chose près, qui bloque presque tout le monde : **depuis OpenMetadata, votre base n'est pas sur `localhost`**. Le catalogue tourne dans le réseau Docker, vos scripts Python tournent sur votre machine ; les deux ne désignent pas le même hôte. Trouvez la bonne adresse avant de vous acharner sur les identifiants.

Le stockage objet est moins documenté : quel type de service OpenMetadata correspond à un bucket S3, et comment le pointer vers un MinIO local plutôt que vers Amazon ? Que voit exactement le catalogue dans un bucket — des fichiers, des colonnes, les deux ? Et si ce que vous obtenez est décevant, est-ce le connecteur qui est en cause, ou la façon dont vous avez rangé vos fichiers en Phase 2 ?

Quels jeux incluez-vous ou excluez-vous de l'ingestion, et pourquoi ? Comment rejouerez-vous cette ingestion demain sans tout refaire à la main ?

Attaquez enfin la sémantique : décrivez vos tables et vos conteneurs de stockage, et construisez un **glossaire de 10 à 15 termes** — chez Éclairage, qu'est-ce qu'un « avantage » ? En quoi diffère-t-il d'une « convention » et d'une « rémunération » ? Qu'appelle-t-on un « bénéficiaire » quand la ligne concerne un établissement et non une personne ? Rattachez ces termes aux tables et colonnes.

**Résultat testable en fin de J3 (point de contrôle formateur) :** les métadonnées des **deux zones** sont visibles et navigables dans OpenMetadata, l'ingestion se rejoue, le glossaire est amorcé.

### Phase 4 — Classification PII, qualité et accès (J4)

Instaurez la confiance, puis le contrôle.

Posez vos **tags PII** colonne par colonne, et surtout **justifiez les cas limites** : la commune d'exercice seule, est-ce une donnée personnelle ? Croisée avec la spécialité ? Le montant versé ? Et le fichier brut déposé dans le bucket — il porte les mêmes données que la table, mérite-t-il le même traitement ?

Instrumentez la **qualité** : fraîcheur (le dernier semestre est-il présent et complet ?), complétude (taux de valeurs manquantes sur les colonnes critiques), unicité (les identifiants de déclaration sont-ils uniques ?), cohérence (des montants négatifs, ça existe ?). Quels seuils retenez-vous, et **que se passe-t-il concrètement quand un test échoue** — le pipeline s'arrête, il alerte, il publie quand même ?

Traduisez enfin les besoins d'accès en règles opposables. Créez des **rôles** correspondant aux utilisateurs réels : chargé d'études, partenaire presse, data engineer. Le partenaire presse doit pouvoir analyser les flux financiers **sans accéder aux noms** — comment le garantissez-vous techniquement : vues dédiées, colonnes masquées, Row Level Security, pseudonymisation ? Et côté bucket, qui a le droit de lire les exports bruts ? Comment **prouvez-vous** qu'une règle fonctionne, autrement qu'en l'affirmant ?

**Résultat testable en fin de J4 :** tags PII posés sur les deux zones, tests de qualité exécutés avec résultats visibles, deux rôles distincts démontrés côte à côte dont un qui ne voit aucun nom.

### Phase 5 — Cycle de vie, topographie et démonstration (J5)

Rédigez le **registre des traitements** : finalité, base légale, catégories de données et de personnes concernées, destinataires, durée de conservation. Sur quel fondement Éclairage traite-t-elle ces données, et combien de temps peut-elle les garder après la publication d'une analyse ?

Rédigez les **procédures de cycle de vie**. Que se passe-t-il quand un professionnel de santé exerce son droit d'opposition — et surtout, **comment le propagez-vous jusqu'au fichier brut dans le bucket** ? Supprimer une ligne en base ne supprime rien de l'export qui l'a produite. Quand un semestre devient trop ancien : suppression ou anonymisation, et quelle différence cela fait-il réellement ? Et le portable du stagiaire, on en fait quoi ?

Formalisez la **topographie des données en quatre parties** : sémantique (glossaire), modèles de données, traitements et flux, mise à disposition et conditions d'accès. Finalisez le README, le schéma d'architecture et le **journal de bord**, vérifiez que la procédure d'installation se rejoue depuis zéro, puis préparez une démonstration scénarisée qui répond à la question centrale.

### Socle commun (obligatoire)

- Inventaire complet du catalogue public et **conclusion argumentée sur le jeu qui fait foi**, méthode incluse.
- **Zones de stockage conçues et justifiées** : buckets, nommage, formats, rétention.
- Périmètre justifié, extrait, déposé dans MinIO **et** chargé dans PostgreSQL, procédure d'installation rejouable.
- **OpenMetadata connecté aux deux sources** (ou sandbox justifiée), ingestion rejouable et configuration versionnée.
- Catalogue enrichi : descriptions, lignage, **glossaire de 10 à 15 termes** rattachés aux tables et colonnes.
- **Tags PII** posés sur les deux zones, avec justification des cas d'identification indirecte.
- Tests de qualité couvrant **fraîcheur, complétude et unicité**, avec seuils et conduite à tenir en cas d'échec.
- Au moins **2 rôles** avec des droits effectifs, dont un privé d'accès aux noms, démontrés en direct.
- **Registre des traitements** et procédures de suppression ou d'anonymisation, **couvrant aussi la zone brute**.
- **Topographie des données en 4 parties**.
- Zéro donnée nominative dans le dépôt Git.

### Pour aller plus loin (bonus)

- **Lignage via dbt** : un squelette de projet dbt est fourni dans le kit ; modélisez la zone travaillée avec dbt et branchez le **connecteur dbt d'OpenMetadata** pour obtenir un lignage automatique bucket → base → modèles.
- **Alertes** : notifier (webhook, e-mail) l'échec d'un test de qualité.
- **Pseudonymisation réversible** des bénéficiaires, avec gestion documentée de la table de correspondance.
- **Politique de rétention automatisée** côté MinIO (règles de cycle de vie sur les objets) plutôt que documentée à la main.
- Étendre le périmètre à un second semestre et mesurer ce que cela change sur les tests de fraîcheur.

Les bonus ne compensent jamais un socle incomplet : **terminez d'abord le socle**.

## Livrables

À rendre au plus tard J5 à 17 h (lien du repo posté sur la plateforme) :

- Un **repo GitHub public** avec un README complet : description du projet, technologies utilisées et justification, instructions d'installation et de lancement (précautions RAM comprises), architecture, auteur.
- Les **scripts d'extraction et de chargement** versionnés, alimentant les deux zones, avec journalisation et reprise possible.
- La **conception des zones de stockage** : buckets, conventions de nommage et de préfixes, formats retenus, politique de rétention — et la justification de chaque choix.
- La **configuration d'ingestion OpenMetadata** versionnée (YAML ou export) pour les **deux** connecteurs, sans aucun secret.
- Les **scripts SQL de gouvernance** : création des rôles, vues masquées ou politiques RLS, attributions de droits.
- La **note d'enquête sur le jeu qui fait foi** : la conclusion, la méthode, les preuves.
- La **note de périmètre** : ce que vous avez chargé, ce que vous avez écarté, et pourquoi.
- Le **schéma d'architecture** au format image (PNG ou export draw.io) faisant apparaître les deux zones — pas d'ASCII.
- La **topographie des données en 4 parties** : sémantique, modèles, traitements et flux, mise à disposition.
- Le **registre des traitements** et les **procédures de suppression ou d'anonymisation**, couvrant la base **et** les exports bruts, avec la base légale retenue.
- La **documentation des rôles**, des droits associés et de la procédure de mise à jour des règles.
- Des **captures d'écran datées** versionnées : glossaire, tags PII sur les deux zones, résultats des tests de qualité, écran des rôles — et la même requête exécutée par deux rôles différents, avec deux résultats différents. Indispensables si la sandbox est utilisée.
- Le lien vers le **Kanban public** avec les user stories et leur historique.
- Le **journal de bord** (`docs/journal.md`) : blocages rencontrés, tentatives, résolution. C'est la qualité du diagnostic qui compte.
- Un fichier **`.gitignore`** effectif et un dépôt exempt de toute donnée nominative.

## Démonstration finale

L'évaluation repose sur deux volets pondérés.

**Volet 1 — Démonstration technique individuelle : 70 %.** 15 minutes de démonstration en direct + 10 minutes de questions, pilotées par la question centrale. Scénario attendu :

- exposer en 2 minutes la conclusion de l'enquête sur le jeu qui fait foi, et la méthode qui y mène ;
- ouvrir le catalogue et montrer que **les deux zones y figurent** : retrouver une table et un conteneur de stockage, lire leur description, leur terme de glossaire, leurs tags PII et leur lignage ;
- montrer les résultats des tests de qualité, dont un test en échec volontaire, et dire ce qui se passe alors ;
- **prouver le contrôle d'accès** : la même requête, exécutée par deux rôles distincts, doit donner deux résultats différents — dont un sans aucun nom ;
- présenter le registre des traitements et dérouler une procédure de suppression, **en montrant ce qu'elle fait au fichier brut du bucket**.

Les questions porteront sur vos arbitrages : pourquoi ce découpage de buckets ? pourquoi ce seuil de complétude ? pourquoi avoir classé cette colonne en donnée personnelle et pas celle-là ? sur quelle base légale ? pourquoi ce périmètre ?

**Volet 2 — Revue de dépôt et d'architecture : 30 %.** Lisibilité du README, reproductibilité de la procédure d'installation, conception des zones, complétude de la topographie en 4 parties, qualité de la note d'enquête, cohérence du schéma d'architecture, absence de secrets **et de données nominatives** dans le dépôt, régularité des commits.

> **Validation partielle** : un catalogue incomplet ou des tests partiellement fonctionnels n'invalident pas les livrables documentaires — registre, topographie, note d'enquête, conception des zones et procédures sont évalués indépendamment. Le recours à la **sandbox** en ligne n'est pas pénalisant s'il est documenté et si la procédure d'installation Docker est malgré tout rédigée. À l'inverse, une démonstration réussie sans documentation ne valide pas les critères documentaires. La présence de données nominatives dans le dépôt, elle, invalide le rendu quel que soit le reste.

## Critères de validation

### Conception et intégration de l'infrastructure de stockage

- Les zones de stockage sont conçues et documentées : découpage en buckets, conventions de nommage et de préfixes, formats de fichiers, politique de rétention — chaque choix étant justifié.
- Les deux zones sont effectivement alimentées : fichiers bruts datés dans le stockage objet, périmètre travaillé dans la base.
- OpenMetadata est fonctionnel et **connecté aux deux sources** (ou la sandbox est utilisée avec justification documentée) ; l'ingestion s'exécute sans erreur et se rejoue.
- L'apprenant sait expliquer le rôle de chaque service démarré par le `docker compose` et distinguer la base de métadonnées du catalogue de la base contenant les données d'Éclairage.
- La documentation couvre l'installation et la configuration, précautions RAM et ordre de démarrage compris, et permet à un tiers de dérouler la procédure sans erreur ; aucun secret n'est versionné.

### Cartographie et topographie des données

- L'inventaire couvre l'ensemble des jeux exposés par le catalogue public, avec identifiant, volumétrie et contenu présumé.
- Le jeu qui fait foi pour les déclarations est identifié, et la **méthode** qui a permis de le déterminer est documentée et rejouable.
- La topographie est complète et structurée en 4 parties : sémantique, modèles de données, traitements et flux, mise à disposition.
- Le glossaire compte 10 à 15 termes définis et rattachés à des tables ou colonnes du catalogue.

### Gestion du catalogue et cycle de vie RGPD

- Les métadonnées des deux zones sont intégrées et enrichies dans le catalogue : descriptions, tags, termes de glossaire, lignage visible.
- Le périmètre d'extraction et les inclusions/exclusions d'ingestion sont explicitement justifiés.
- Les colonnes et fichiers sont classés selon leur caractère personnel, en distinguant identification directe et indirecte, chaque cas limite étant argumenté.
- Le registre des traitements couvre finalité, base légale, catégories de données, destinataires et durée de conservation ; les procédures de suppression ou d'anonymisation sont rédigées et **traitent explicitement le sort des exports bruts**, pas seulement des tables.

### Qualité des données

- Des tests couvrent au minimum la fraîcheur, la complétude et l'unicité, et s'exécutent sans intervention manuelle.
- Les seuils retenus sont explicites et justifiés au regard de l'usage des données.
- La conduite à tenir en cas d'échec est documentée, et un échec est démontré en direct.

### Règles de gouvernance et accès

- Les droits sont portés par des rôles ou des groupes, et non par des comptes individuels.
- Les accès sont limités au nécessaire : au moins un rôle peut analyser les données financières sans accéder aux identités, démontré par la même requête exécutée sous deux rôles.
- L'accès à la zone brute est traité explicitement, et pas seulement celui de la base.
- Le dispositif technique retenu (vues, masquage, RLS, policies du catalogue, pseudonymisation) est documenté et justifié ; la documentation couvre les rôles, leurs droits et la procédure de mise à jour des règles.

## Ressources

- [Cours SQL](../../../01-Fondamentaux/SQL/)
- [Cours Docker](../../../02-Containerisation/Docker/)
- [RGPD & Gouvernance](../../../01-Fondamentaux/RGPD-Gouvernance/)
- [Cours OpenMetadata](../../../06-Data-Engineering/OpenMetadata/) — installation (ch. 2), connecteurs et ingestion (ch. 3), documentation (ch. 4), lignage (ch. 5), qualité (ch. 6), glossaire et classification (ch. 7)
- [Cours Data Lake](../../../05-Databases/DataLake/) — zones de stockage, formats, gouvernance
- Portail Transparence-Santé : https://www.transparence.sante.gouv.fr
- Catalogue des jeux de données (API) : https://www.transparence.sante.gouv.fr/api/explore/v2.1/catalog/datasets
- Documentation de l'API Opendatasoft Explore v2.1 : https://help.opendatasoft.com/apis/ods-explore-v2/
- Déploiement local d'OpenMetadata avec Docker : https://docs.open-metadata.org/latest/quick-start/local-docker-deployment
- Connecteur PostgreSQL d'OpenMetadata : https://docs.open-metadata.org/latest/connectors/database/postgres
- Connecteurs de stockage objet (S3) d'OpenMetadata : https://docs.open-metadata.org/latest/connectors/storage/s3
- Sandbox OpenMetadata en ligne (repli si RAM insuffisante) : https://sandbox.open-metadata.org
- MinIO — documentation et compatibilité S3 : https://min.io/docs/minio/linux/index.html
- boto3 — client S3 en Python : https://boto3.amazonaws.com/v1/documentation/api/latest/reference/services/s3.html
- PostgreSQL — rôles et privilèges : https://www.postgresql.org/docs/current/user-manag.html
- PostgreSQL — Row Level Security : https://www.postgresql.org/docs/current/ddl-rowsecurity.html
- CNIL — Le registre des activités de traitement : https://www.cnil.fr/fr/RGPD-le-registre-des-activites-de-traitement
- CNIL — Anonymisation et pseudonymisation : https://www.cnil.fr/fr/lanonymisation-de-donnees-personnelles
- CNIL — Les durées de conservation : https://www.cnil.fr/fr/les-durees-de-conservation-des-donnees
