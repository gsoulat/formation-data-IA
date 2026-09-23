# Brief : Le maillage de recharge électrique en France — pipeline API + scraping vers PostgreSQL

## Informations

| Critère | Valeur |
|---------|--------|
| **Durée** | 5 jours (35 heures) |
| **Niveau** | Débutant-Intermédiaire |
| **Modalité** | Individuel |
| **Technologies** | Python (Requests, BeautifulSoup), API REST Opendatasoft, Web Scraping, PostgreSQL, Docker, SQL, Merise, Git |
| **Prérequis** | [Cours Python](../../../01-Fondamentaux/Python/) + [Cours SQL](../../../01-Fondamentaux/SQL/) + [Cours Docker](../../../02-Containerisation/Docker/) |
| **Données** | **100 % réelles** — aucune donnée générée, aucune anomalie injectée |

## Contexte

### L'entreprise

**Voltiq** est un cabinet de conseil en mobilité électrique de 22 personnes, basé à Nantes. Il répond à des appels d'offres de collectivités (départements, métropoles, syndicats d'énergie) qui doivent décider **où implanter les prochaines bornes de recharge** et justifier ces choix devant leurs élus. L'équipe data se résume à Sofiane, chargé d'études, et vous, premier data engineer recruté.

### Le problème

Sofiane travaille aujourd'hui à la main. Pour chaque appel d'offres, il télécharge le fichier national des bornes de recharge, l'ouvre dans Excel, filtre le département concerné, recopie les chiffres de population trouvés ailleurs, puis fabrique un tableau de synthèse. Trois jours de travail par dossier, un résultat que personne ne peut reproduire, et des chiffres qui ne sont plus à jour au moment de la soutenance.

Le fichier national pose en plus des problèmes qu'Excel ne résout pas : une même station y apparaît autant de fois qu'elle a de points de charge, quelques puissances sont exprimées en watts au milieu de kilowatts, plus d'un quart des lignes n'ont pas de code INSEE de commune, et les coordonnées géographiques y sont rangées sous des noms de champs trompeurs.

La directrice vous confie votre première mission : remplacer ce bricolage par un **pipeline de collecte automatisé, rejouable et documenté**.

### La question centrale

Tout votre travail doit permettre d'y répondre, et vous devez pouvoir vous y référer à chaque étape :

> **« Le maillage de bornes de recharge suit-il vraiment le parc de véhicules électriques, département par département ? »**

### Les sources de données

Le mix est imposé par le référentiel : au moins un **service web (API REST)**, un **scraping**, un **fichier de données** et une **base de données**. Ici, les quatre sont réelles et publiques.

- **API REST — Base nationale des IRVE** : `https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/bornes-irve/records`. API Opendatasoft Explore v2.1, publique, sans authentification, réponses JSON. Environ **227 000 points de charge** décrits par une soixantaine de champs (aménageur, opérateur, enseigne, identifiant de station, adresse, code INSEE, coordonnées, puissance nominale, type de prises, date de mise en service, accessibilité, tarification).
- **Scraping — Wikipédia** : `https://en.wikipedia.org/wiki/List_of_production_battery_electric_vehicles`. Environ **960 lignes** réparties sur **9 tableaux HTML de structures différentes** : modèles de véhicules électriques de série, constructeur, année de production, type de carrosserie, origine de la marque, et selon les tableaux le caractère 100 % électrique ou non. Ce catalogue de l'offre n'existe dans **aucun** jeu de données ouvert français — c'est précisément pourquoi il faut aller le chercher dans la page. Complétez avec `https://fr.wikipedia.org/wiki/Borne_de_recharge` pour les types de prises et les paliers de puissance.
  **Attention** : les 9 tableaux n'ont pas les mêmes colonnes (modèles actuels, modèles retirés, utilitaires…). Repérer les colonnes par leur position vous fera produire des données fausses sans erreur visible.
- **Fichier de données — parc automobile électrique** : jeu « Part de voitures particulières électriques (Crit'Air E) dans le parc », `https://www.data.gouv.fr/datasets/part-de-voitures-particulieres-electriques-critair-e-dans-le-parc`. Plusieurs CSV réels (jusqu'à ~1 Mo, granularité communale), publiés par le ministère de la Transition écologique.
- **Base de données — PostgreSQL** : la cible du pipeline. Instance conteneurisée avec Docker, dans laquelle vous chargez le jeu consolidé, puis exécutez vos requêtes SQL d'analyse.

### Ce qui rend ce brief différent d'un exercice

Les anomalies ne sont pas injectées : elles sont **subies**, exactement comme en production. Vous
les découvrirez vous-même en Phase 1, et vous en trouverez d'autres que ce brief ne mentionne pas.

Les chiffres ci-dessous sont **mesurés sur le jeu complet**. Ne les recopiez pas : refaites la
mesure, c'est le travail de la Phase 1. Ils sont là pour vous montrer l'ampleur du problème.

- **L'API plafonne**. Opendatasoft limite `limit` à 100 et refuse `limit + offset > 10 000` — le
  message d'erreur le dit explicitement. Vous ne récupérerez donc **jamais** les 227 232 lignes par
  simple pagination : il faut une autre stratégie (filtrer, ou utiliser le point d'entrée d'export).
  C'est le premier vrai problème d'ingénierie du brief.
- **Le grain est piégeux**. Une ligne = un **point de charge**, pas une station. Le fichier compte
  **227 232 lignes pour 63 946 stations distinctes**, soit **3,6 points de charge par station**.
  Annoncer « 227 000 bornes en France » à un élu, c'est se tromper d'un facteur 3,6. Quel grain
  retenez-vous, et comment le justifiez-vous auprès de Sofiane ?
- **28,4 % des lignes n'ont pas de code INSEE de commune.** Ce n'est pas un cas marginal à ignorer :
  c'est plus d'un quart du fichier. Les jeter, c'est fausser toute analyse départementale. Les
  garder sans les rattacher, c'est ne pas pouvoir les compter. Que faites-vous ?
- **Les unités de puissance sont mélangées**, mais discrètement : 975 lignes (0,43 %) portent une
  valeur supérieure à 1 000, jusqu'à **160 000** — des watts là où le reste du fichier est en
  kilowatts. Une moyenne calculée sans traitement est fausse, et un échantillon de mille lignes
  ne vous les montrera pas. 2,3 % des lignes ont par ailleurs une puissance nulle ou négative.
- **Les coordonnées sont inversées.** Le champ `coordonneesxy` expose une clé `lon` et une clé
  `lat`… dont les valeurs sont permutées : pour une station à Blagnac, `lon` vaut 43,63 et `lat`
  vaut 1,37, alors que Toulouse est à 43,6 de **latitude** et 1,4 de **longitude**. Faites
  confiance au nom du champ et votre carte place la France au large de l'Afrique. Vérifiez
  toujours une coordonnée sur une carte avant de bâtir dessus.
- **Les booléens sont des chaînes de caractères** : `"True"` et `"False"`, pas `true`/`false`. En
  Python, `bool("False")` vaut `True` — de quoi inverser silencieusement un filtre entier.

### Contraintes techniques

- Langage : Python (bibliothèques au choix, choix justifiés dans le README).
- Le pipeline doit être **rejouable de bout en bout** depuis un clone propre du repo, par une ou plusieurs commandes documentées.
- **Gestion des erreurs, retry et journalisation** obligatoires sur les extractions : une API publique tombe, ralentit, ou renvoie un 200 avec un corps vide.
- Respect du site scrapé : `User-Agent` explicite et temporisation entre les requêtes. Wikipédia autorise les robots respectueux — soyez-en un.
- PostgreSQL via Docker uniquement (aucune installation locale de SGBD).
- Tout le code est **versionné avec Git dès la première heure**, sur un repo GitHub public.
- **RGPD** : le fichier IRVE contient des coordonnées de contact (`contact_amenageur`, `contact_operateur`, `telephone_operateur`), renseignées sur **100 % des lignes**. Ce sont des données professionnelles, mais certaines sont des adresses nominatives de personnes physiques (`prenom.nom@societe.fr`). Vous tenez un registre des traitements basique et tranchez explicitement leur sort.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **Automatiser l'extraction de données** depuis un service web (API REST), une page web (scraping) et un fichier de données — cœur du brief, **aucun script d'exemple n'est fourni** : vous concevez seul le point de lancement, la stratégie de pagination, la gestion des erreurs, le retry, les logs et la sauvegarde des résultats ;
- **Contourner une limite d'API réelle** en concevant une stratégie de découpage documentée et justifiée ;
- **Développer des règles d'agrégation et de nettoyage** sur des anomalies non annoncées : doublons de grain, unités mélangées, codes géographiques manquants, coordonnées à parser ;
- **Développer des requêtes SQL** d'extraction (sélections, filtrages, jointures, agrégats) répondant à la question centrale, avec optimisations explicitées ;
- **Créer une base de données** modélisée selon la méthode Merise (MCD/MPD), avec script DDL versionné, script d'import et registre RGPD.

## Architecture cible

Un pipeline batch en trois couches, inspiré de l'architecture Medallion :

- couche `raw` : les réponses brutes telles que collectées, fichiers datés, jamais modifiés ;
- couche `staging` : les données nettoyées et homogénéisées, source par source ;
- couche finale : un jeu consolidé unique, chargé dans PostgreSQL.

```
+------------------+  +------------------+  +------------------+
|  API ODRE IRVE   |  |    Wikipédia     |  |  CSV Crit'Air E  |
| 227k pts charge  |  |  (scraping HTML) |  |  parc communal   |
+---------+--------+  +---------+--------+  +---------+--------+
          |                     |                     |
          +----------+----------+----------+----------+
                     |                     |
          +----------v---------------------v---------+
          |       SCRIPTS D'EXTRACTION (Python)      |
          |  pagination/découpage, retry, logs       |
          +----------+-------------------------------+
                     |
          +----------v-------------------------------+
          |  COUCHE RAW — brut, daté, immuable        |
          +----------+-------------------------------+
                     |
          [Nettoyage : grain, unités, INSEE, géo]
                     |
          +----------v-------------------------------+
          |  COUCHE STAGING — propre, source à source |
          +----------+-------------------------------+
                     |
             [Consolidation / jointures]
                     |
          +----------v-------------------------------+
          |  JEU DE DONNÉES FINAL UNIQUE              |
          +----------+-------------------------------+
                     |
          +----------v-------------------------------+
          |  PostgreSQL (Docker)                      |
          |  Modèle Merise (MCD/MPD) + import         |
          |  Requêtes SQL d'analyse                   |
          +-------------------------------------------+
```

> Vous produirez votre propre schéma d'architecture **au format image** (draw.io ou équivalent, pas d'ASCII art) à joindre au rendu.

## Données fournies

Le kit de démarrage se trouve dans le dossier [`starter-kit/`](starter-kit/). Il est volontairement minimal :

- `docker-compose.yml` — pour lancer PostgreSQL 16 en local (`docker compose up -d`) ;
- `.env.example` — variables d'environnement d'exemple (aucun secret réel) ;
- `sources.md` — les URL exactes des trois sources et rien d'autre.

**Aucune donnée n'est fournie, aucun script non plus.** Vous allez chercher les données réelles vous-même : c'est le sujet du brief.

## Travail demandé

Travail individuel sur 5 jours. L'entraide est encouragée (partage de blocages, debug entre pairs), mais chacun rend son propre code et doit pouvoir l'expliquer ligne par ligne.

> **Règle des 2 heures.** Ces données sont réelles : vous rencontrerez des obstacles que ce brief ne mentionne pas. Chercher par soi-même fait partie du métier, s'enliser non. **Bloqué plus de 2 heures sur le même point ? Demandez un indice au formateur.** Ce n'est pas un aveu d'échec, c'est ce que vous ferez en entreprise. Notez simplement le blocage et sa résolution dans votre journal de bord : il fera partie du rendu.

### Phase 1 — Cadrage et exploration des sources (J1)

Aucune ligne de code de production. Explorez les quatre sources comme le ferait un auditeur.

Interrogez l'API IRVE dans le navigateur ou avec `curl` : que renvoie-t-elle avec `limit=1` ? Combien annonce-t-elle de résultats dans `total_count` ? Que se passe-t-il quand vous demandez `limit=100&offset=15000` — et que vous dit le message d'erreur ? C'est le moment de comprendre le mur avant de foncer dedans. Quels champs vous serviront réellement, et lesquels sont du bruit ?

Ouvrez la page Wikipédia dans l'inspecteur : combien de tableaux, quelles colonnes, les en-têtes sont-ils identiques d'un tableau à l'autre ? Téléchargez les CSV Crit'Air E et regardez leur granularité et leur période de référence.

Documentez chaque source dans `docs/sources.md` : URL, format, volume, champs retenus, **pièges identifiés**. Créez votre **Kanban public** (GitHub Projects, Trello…) avec des user stories tirées de la question centrale — par exemple : « En tant que chargé d'études, je veux le nombre de stations pour 10 000 véhicules électriques par département ». Initialisez le repo GitHub public.

Prenez le temps, en fin de journée, de **valider vos hypothèses à la main** : téléchargez une centaine de lignes de l'API, ouvrez un CSV, extrayez un tableau Wikipédia dans un notebook jetable. Le but n'est pas de produire du code de production, c'est de vous assurer que les données contiennent bien ce que vous croyez avant d'écrire quoi que ce soit.

**Résultat testable en fin de J1 (point de contrôle formateur) :** documentation des trois sources relue par un pair, stratégie de contournement de la limite d'API écrite noir sur blanc, Kanban rempli, repo initialisé.

### Phase 2 — Extraction automatisée multi-sources (J2-J3)

Développez les scripts d'extraction, source par source, en commençant par la plus simple.

Pour l'API, appliquez la stratégie décidée en Phase 1 : si vous découpez par département, comment obtenez-vous la liste des départements, et que faites-vous des lignes dont le code département est vide ? Si une requête échoue au 47ᵉ département, votre script s'arrête-t-il, réessaie-t-il, journalise-t-il l'échec ? À quel rythme appelez-vous une API publique gratuite sans l'agresser ?

Pour le scraping, les 9 tableaux n'ont pas tous la même structure : les traitez-vous par une boucle générique ou un par un, et pourquoi ? Que fait votre script le jour où Wikipédia ajoute une colonne ?

Chaque script doit avoir un **point de lancement clair**, initialiser ses dépendances et connexions, appliquer ses règles de traitement, gérer erreurs et exceptions, écrire des **logs exploitables** et sauvegarder ses résultats bruts, datés, dans la couche `raw`. Committez petit et souvent : **l'historique Git fait partie de l'évaluation**.

Consacrez la fin de la phase à **éprouver votre robustesse** plutôt qu'à ajouter des fonctionnalités : coupez votre connexion réseau en pleine extraction, relancez, et regardez ce qui se passe. Reprend-elle où elle s'était arrêtée, ou repart-elle de zéro ? Vos fichiers `raw` sont-ils dans un état exploitable ou à moitié écrits ? C'est ce test-là, pas le chemin nominal, qui distingue un script d'un pipeline.

**Résultat testable en fin de J3 :** chaque extraction se relance par une commande unique et produit ses fichiers `raw` ; les logs racontent le déroulement, y compris les échecs ; une interruption en cours d'extraction ne laisse pas la couche `raw` dans un état incohérent.

### Phase 3 — Nettoyage, consolidation et jeu final (J3-J4)

Transformez le brut en couche `staging`, puis en jeu consolidé unique.

Tranchez d'abord le **grain** : votre jeu final décrit-il des points de charge ou des stations ? Selon votre réponse, quelle règle de dédoublonnage appliquez-vous, et sur quelle clé ? Homogénéisez les **puissances** — comment distinguez-vous un 22 kW d'un 22 000 W autrement qu'à l'œil ? Parsez les **coordonnées** et récupérez un code géographique fiable pour chaque station : que faites-vous des lignes sans code INSEE, vous les jetez ou vous les rattrapez ?

Joignez enfin les trois sources. Attention : la maille du fichier Crit'Air E n'est pas forcément celle de l'IRVE, et les modèles Wikipédia ne se rattachent à aucune borne — à quel niveau cette source vous sert-elle réellement ?

Chaque règle de nettoyage est **écrite en code** (aucune correction manuelle dans un tableur) et documentée : quelle règle, sur quelles données, combien de lignes affectées.

**Résultat testable en fin de J4 (point de contrôle formateur) :** un script de consolidation rejouable qui produit le jeu final et affiche un décompte des lignes supprimées, corrigées et rejetées.

### Phase 4 — Modélisation Merise, base de données et requêtes SQL (J4-J5)

Modélisez la base cible selon la méthode **Merise** : MCD puis MPD, exportés en images. Quelles entités distinguez-vous — une station, un point de charge, un opérateur, une commune, un modèle de véhicule ? Un point de charge est-il un attribut de la station ou une entité à part entière ?

Créez la base dans PostgreSQL (**script DDL versionné**) et programmez le script d'import. Rédigez le **registre RGPD basique** : les coordonnées d'opérateurs, vous les conservez, les pseudonymisez ou les excluez — et au nom de quelle finalité ?

Écrivez enfin les **requêtes SQL** qui répondent à la question centrale : nombre de stations pour 10 000 véhicules électriques par département, puissance cumulée installée, part des bornes rapides, départements sous-équipés. Chaque requête est documentée : sélections, filtrages, jointures, optimisations et leur justification.

**Résultat testable :** base recréable depuis zéro (conteneur + DDL + import) et requêtes exécutables.

### Phase 5 — Consolidation et démonstration (J5)

Finalisez le README et le schéma d'architecture, et vérifiez que **tout se rejoue depuis un clone propre** : effacez votre dossier de travail, reclonez votre propre repo et déroulez votre README à la lettre. C'est le seul test qui compte, et il révèle presque toujours une dépendance non documentée ou un fichier oublié dans le `.gitignore`.

Rédigez enfin votre **journal de bord** : les blocages rencontrés, ce que vous avez essayé, ce qui a débloqué. C'est un livrable, et c'est aussi ce dont vous parlerez le mieux en démonstration.

Préparez une démonstration de **15 minutes** articulée autour de la question centrale.

### Socle commun (obligatoire)

- Les trois extractions fonctionnelles : API REST, scraping, fichier — avec la limite d'API effectivement contournée et documentée.
- Le jeu final consolidé, chargé dans PostgreSQL, interrogé par au moins **4 requêtes SQL** documentées.
- MCD/MPD, registre RGPD, `docs/sources.md`, README, schéma d'architecture, Kanban public.

### Pour aller plus loin (bonus)

- Géocodage des stations sans code INSEE via l'API Adresse (`https://api-adresse.data.gouv.fr`).
- Planification du pipeline (cron) et détection des nouvelles stations entre deux exécutions.
- Tests unitaires sur les fonctions de nettoyage (conversion des unités, dédoublonnage).
- Backoff exponentiel sur l'API et le scraping.

Les bonus ne compensent jamais un socle incomplet : **terminez d'abord le socle**.

## Livrables

À rendre au plus tard J5 à 17 h (lien du repo posté sur la plateforme) :

- Un **repo GitHub public** avec un README structuré : description du projet et rappel de la question centrale, technologies utilisées et justification, instructions d'installation et de lancement depuis zéro, architecture, auteur.
- Le **code du pipeline** : scripts d'extraction (API, scraping, fichier), script de nettoyage et de consolidation, script DDL, script d'import — avec un historique de commits réparti sur les 5 jours (pas un commit final unique).
- Une **note de stratégie d'extraction** (une page max) expliquant comment vous avez contourné la limite `limit + offset ≤ 10 000` et pourquoi cette stratégie plutôt qu'une autre.
- Le **schéma d'architecture** au format image (PNG ou export draw.io), montrant les couches `raw`, `staging` et finale.
- Les **modèles de données** : MCD et MPD au format image, avec une courte note sur les choix de modélisation (notamment le grain retenu).
- La **documentation des sources** (`docs/sources.md`) : format, volume, champs, pièges de chaque source.
- La **documentation des requêtes SQL** : pour chaque requête, son objectif métier, ses sélections/filtrages/jointures et ses optimisations.
- Le **registre RGPD** des traitements et la décision motivée sur les coordonnées d'opérateurs.
- Le lien vers le **Kanban public** (dans le README), avec les user stories et leur historique.
- Le **jeu de données final**, exporté en CSV dans le repo ou reconstructible via la base.
- Le **journal de bord** (`docs/journal.md`) : les blocages rencontrés sur les données réelles, ce que vous avez essayé, ce qui a débloqué. Une ligne par blocage suffit. Il n'est pas noté sur la quantité de galères, mais sur la qualité du diagnostic.

## Démonstration finale

L'évaluation repose sur deux volets pondérés.

**Volet 1 — Démonstration technique individuelle : 70 %.** 15 minutes de démonstration en direct + 10 minutes de questions. Vous relancez le pipeline (extractions, consolidation, import), montrez les logs produits, la base PostgreSQL peuplée, puis exécutez 2 ou 3 requêtes SQL qui répondent à la question centrale.

Pour tenir les 10 minutes, les scripts peuvent prévoir un **mode échantillon** (paramètre limitant le nombre de départements ou de pages), à condition de présenter aussi les preuves d'une exécution complète (logs datés, volumes collectés). Les questions porteront sur vos choix : stratégie de contournement de l'API, grain retenu, règles de nettoyage, modélisation.

**Volet 2 — Revue de code et d'architecture : 30 %.** Structure et lisibilité du code, gestion des erreurs et des logs, qualité du README et de la documentation des sources, cohérence du schéma d'architecture et des modèles Merise, régularité des commits.

> **Validation partielle** : un pipeline qui ne fonctionne pas en démonstration mais dont le code est structuré, versionné et documenté peut valider partiellement les compétences concernées. À l'inverse, une démonstration réussie sans documentation ne valide pas les critères documentaires.

Sans repo GitHub public accessible et sans code versionné, le travail ne peut pas être évalué.

## Critères de validation

### Extraction automatisée de données (conception en autonomie complète, aucun modèle fourni)

- Les scripts d'extraction sont fonctionnels : les données visées sont effectivement récupérées à l'issue de l'exécution, depuis l'API, la page web et le fichier.
- La limite de pagination de l'API est effectivement contournée, et la stratégie retenue est documentée et justifiée.
- Chaque script comprend un point de lancement, l'initialisation des dépendances et des connexions, les règles de traitement, la gestion des erreurs et des exceptions (avec retry), des logs exploitables et la sauvegarde des résultats bruts datés.
- Les scripts sont versionnés et accessibles depuis un dépôt Git public, avec un historique de commits réparti sur la durée du projet.

### Règles d'agrégation et de nettoyage

- Le script de consolidation est fonctionnel : les données des trois sources sont nettoyées, homogénéisées et agrégées en un jeu final unique.
- Le grain retenu (station ou point de charge) est explicite, appliqué de façon cohérente et justifié.
- Les unités de puissance sont homogénéisées selon une règle écrite et vérifiable ; les lignes sans code géographique exploitable sont traitées selon une règle explicite (rejet tracé ou rattrapage).
- La documentation précise, pour chaque règle, les données concernées et le nombre de lignes affectées.

### Requêtes SQL d'extraction

- Les requêtes sont fonctionnelles : les données visées sont effectivement extraites à l'exécution.
- Au moins 4 requêtes mobilisent sélections, filtrages, conditions, jointures et agrégats en lien direct avec la question centrale.
- La documentation met en lumière les choix de sélections, filtrages et jointures au regard des objectifs, et explicite les optimisations appliquées.

### Création de la base de données

- Les modélisations respectent la méthode et le formalisme Merise ; MCD et MPD sont cohérents entre eux et avec le grain retenu.
- Le choix du SGBD est justifié dans le README au regard de la modélisation et des contraintes du projet.
- Le modèle physique est fonctionnel : la base se crée sans erreur depuis le script DDL versionné, et le script d'import insère effectivement le jeu final.
- Le registre RGPD couvre les traitements de données à caractère personnel du périmètre, et le sort réservé aux coordonnées d'opérateurs est tranché et motivé.

## Ressources

- [Cours Python](../../../01-Fondamentaux/Python/)
- [Cours SQL](../../../01-Fondamentaux/SQL/)
- [Cours Docker](../../../02-Containerisation/Docker/)
- Base nationale des IRVE sur ODRE (jeu de données et API) : https://odre.opendatasoft.com/explore/dataset/bornes-irve/
- Documentation de l'API Opendatasoft Explore v2.1 (pagination, filtres, exports) : https://help.opendatasoft.com/apis/ods-explore-v2/
- Fichier consolidé des IRVE sur data.gouv.fr (fiche du jeu de données) : https://www.data.gouv.fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques-irve-statique
- Part de voitures particulières électriques (Crit'Air E) dans le parc : https://www.data.gouv.fr/datasets/part-de-voitures-particulieres-electriques-critair-e-dans-le-parc
- Liste des véhicules électriques de série (page à scraper) : https://en.wikipedia.org/wiki/List_of_production_battery_electric_vehicles
- Borne de recharge — types de prises et paliers de puissance : https://fr.wikipedia.org/wiki/Borne_de_recharge
- Requests (documentation officielle) : https://requests.readthedocs.io/
- Beautiful Soup 4 (documentation officielle) : https://www.crummy.com/software/BeautifulSoup/bs4/doc/
- API Adresse (géocodage, pour le bonus) : https://adresse.data.gouv.fr/api-doc/adresse
- Image Docker officielle PostgreSQL : https://hub.docker.com/_/postgres
- CNIL — Le registre des activités de traitement : https://www.cnil.fr/fr/RGPD-le-registre-des-activites-de-traitement
