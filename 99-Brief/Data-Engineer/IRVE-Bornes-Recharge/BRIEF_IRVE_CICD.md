# Brief : Les bornes de recharge en France — pipeline API vers PostgreSQL, livré en version avec uv et GitHub Actions

> **Version CI/CD** du brief [IRVE — collecte](BRIEF_IRVE_COLLECTE.md), recentrée sur **une seule source** : l'API
> nationale des bornes de recharge (IRVE). Trois scripts (extraction, nettoyage, consolidation), trois couches dans
> PostgreSQL, un modèle Merise. Il s'y ajoute une contrainte d'industrialisation : **uv obligatoire**, des
> **commits conventionnels vérifiés en CI**, des **versions publiées automatiquement par semantic-release** et une
> **image Docker du pipeline construite à chaque release**. Et l'ordre est inversé par rapport à l'habitude :
> **la chaîne de livraison se construit en premier (J1)**, avant la moindre ligne de pipeline.

## Informations

| Critère | Valeur |
|---------|--------|
| **Durée** | 5 jours (35 heures) |
| **Niveau** | Intermédiaire |
| **Modalité** | Individuel |
| **Technologies** | Python, **uv**, Requests, API REST Opendatasoft, PostgreSQL, Docker, SQL, Merise, Git, **GitHub Actions**, **Conventional Commits**, **commitlint**, **semantic-release**, **GitHub Container Registry (GHCR)** |
| **Prérequis** | [Cours Python](../../../01-Fondamentaux/Python/) + [Cours SQL](../../../01-Fondamentaux/SQL/) + [Cours Docker](../../../02-Containerisation/Docker/) + [Cours Modélisation (Merise)](../../../01-Fondamentaux/Modelisation/) + [Cours Git](../../../01-Fondamentaux/Git/) + [GitHub Actions](../../../07-DevOps/01-CI-CD/03-GitHub-Actions/) |
| **Données** | **100 % réelles** — aucune donnée générée, aucune anomalie injectée |

## Contexte

### L'entreprise

**Voltiq** est un cabinet de conseil en mobilité électrique de 22 personnes, basé à Nantes. Il répond à des appels d'offres de collectivités (départements, métropoles, syndicats d'énergie) qui doivent décider **où implanter les prochaines bornes de recharge** et justifier ces choix devant leurs élus. L'équipe data se résume à Sofiane, chargé d'études, et vous, premier data engineer recruté.

### Le problème

Sofiane travaille aujourd'hui à la main. Pour chaque appel d'offres, il télécharge le fichier national des bornes de recharge, l'ouvre dans Excel, filtre le département concerné, puis fabrique un tableau de synthèse. Trois jours de travail par dossier, un résultat que personne ne peut reproduire, et des chiffres qui ne sont plus à jour au moment de la soutenance.

Le fichier national pose en plus des problèmes qu'Excel ne résout pas : une même station y apparaît autant de fois qu'elle a de points de charge, quelques puissances sont exprimées en watts au milieu de kilowatts, plus d'un quart des lignes n'ont pas de code INSEE de commune, et les coordonnées géographiques y sont rangées sous des noms de champs trompeurs.

La directrice vous confie votre première mission : remplacer ce bricolage par un **pipeline automatisé, rejouable et documenté**, qui alimente une base PostgreSQL que Sofiane pourra interroger directement.

### Ce que la directrice ajoute

Voltiq a déjà vécu l'histoire du « script qui marchait sur le portable de l'ancien stagiaire ». Personne n'a jamais su quelle version avait produit les chiffres d'un dossier rendu à un département, ni avec quelles bibliothèques. La directrice pose donc trois conditions avant de confier des chiffres à un client :

- **un environnement reproductible** : n'importe qui doit retrouver exactement vos dépendances, à la version près. Le cabinet a standardisé ses projets Python sur **uv** ;
- **un historique lisible** : chaque commit dit ce qu'il change, selon une convention commune, et c'est une machine qui le vérifie, pas la bonne volonté ;
- **des versions publiées** : chaque dossier client doit pouvoir citer « chiffres produits par le pipeline v1.3.0 », et cette version doit exister sous forme d'**image Docker** que l'on peut relancer à l'identique dans six mois.

Elle ajoute une consigne d'ordre : « La chaîne de livraison d'abord, le pipeline ensuite. Je ne veux pas d'une CI bricolée la veille de la soutenance. » Votre premier jour est donc consacré à cette chaîne, sur un projet presque vide.

### La question centrale

Tout votre travail doit permettre d'y répondre, et vous devez pouvoir vous y référer à chaque étape :

> **« Comment le réseau public de recharge est-il réparti sur le territoire, département par département, et où la recharge rapide manque-t-elle ? »**

### La source de données

- **API REST — Base nationale des IRVE** : `https://odre.opendatasoft.com/api/explore/v2.1/catalog/datasets/bornes-irve/records`. API Opendatasoft Explore v2.1, publique, sans authentification, réponses JSON. Environ **227 000 points de charge** décrits par une soixantaine de champs (aménageur, opérateur, enseigne, identifiant de station, adresse, code INSEE, coordonnées, puissance nominale, type de prises, date de mise en service, accessibilité, tarification).
- **Base de données — PostgreSQL** : la cible du pipeline, conteneurisée avec Docker. Les trois couches du pipeline y vivent, chacune dans son schéma.

Une seule source, mais pas une source facile : c'est elle qui fait tout le travail d'ingénierie de ce brief.

### Ce qui rend ce brief différent d'un exercice

Les anomalies ne sont pas injectées : elles sont **subies**, exactement comme en production. Vous
les découvrirez vous-même en Phase 2, et vous en trouverez d'autres que ce brief ne mentionne pas.

Les chiffres ci-dessous sont **mesurés sur le jeu complet**. Ne les recopiez pas : refaites la
mesure, c'est le travail de la Phase 2. Ils sont là pour vous montrer l'ampleur du problème.

- **L'API plafonne**. Opendatasoft limite `limit` à 100 et refuse `limit + offset > 10 000` — le
  message d'erreur le dit explicitement. Vous ne récupérerez donc **jamais** les 227 232 lignes par
  simple pagination : il faut une autre stratégie (filtrer, ou utiliser le point d'entrée d'export).
  C'est le premier vrai problème d'ingénierie du brief.
- **Le grain est piégeux**. Une ligne = un **point de charge**, pas une station. Le fichier compte
  **227 232 lignes pour 63 946 stations distinctes**, soit **3,6 points de charge par station**.
  Annoncer « 227 000 bornes en France » à un élu, c'est se tromper d'un facteur 3,6. Comment votre
  modèle distingue-t-il les deux, et lequel comptez-vous quand Sofiane demande « combien de bornes » ?
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
- **uv est obligatoire** pour tout le cycle de vie du projet : création (`uv init`), version de Python (`.python-version`), dépendances (`uv add`, groupes de dépendances de développement), verrouillage (`uv.lock` versionné) et exécution (`uv run`). **Aucun `requirements.txt`, aucun `pip install`, aucun environnement virtuel créé à la main**, ni sur votre poste, ni dans le `Dockerfile`, ni dans la CI.
- **Trois scripts, trois couches, une base** : un script d'**extraction** (API → schéma `raw`), un script de **nettoyage** (`raw` → `staging`), un script de **consolidation** (`staging` → `mart`). Chacun se lance seul, et l'ensemble se rejoue de bout en bout par des commandes `uv run` documentées **et** depuis l'image Docker publiée.
- **Gestion des erreurs, retry et journalisation** obligatoires sur l'extraction : une API publique tombe, ralentit, ou renvoie un 200 avec un corps vide.
- PostgreSQL via Docker uniquement (aucune installation locale de SGBD).
- Tout le code est **versionné avec Git dès la première heure**, sur un repo GitHub public, avec des messages au format **Conventional Commits** (`feat:`, `fix:`, `docs:`, `refactor:`, `chore:`…).
- **RGPD** : le fichier IRVE contient des coordonnées de contact (`contact_amenageur`, `contact_operateur`, `telephone_operateur`), renseignées sur **100 % des lignes**. Ce sont des données professionnelles, mais certaines sont des adresses nominatives de personnes physiques (`prenom.nom@societe.fr`). Vous tenez un registre des traitements basique et tranchez explicitement leur sort, couche par couche.

### Périmètre de la CI/CD — volontairement étroit

La CI/CD de ce brief fait **trois choses, et seulement trois** :

1. **vérifier les messages de commit** (Conventional Commits) à chaque push et à chaque pull request ;
2. **calculer et publier une version** avec semantic-release quand `main` reçoit des commits qui le justifient : tag SemVer, GitHub Release avec ses notes, `CHANGELOG.md` ;
3. **construire l'image Docker du pipeline et la publier sur GHCR**, taguée avec cette version, **uniquement quand une release vient d'être créée**.

Les tests, le lint et tout déploiement sont **hors périmètre** de la CI dans ce brief (les tests restent possibles en bonus, en local). Un workflow qui en fait plus que demandé n'apporte pas de points ; un workflow qui en fait moins fait perdre la compétence.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **Concevoir le cadre technique d'exploitation d'un pipeline** : environnement reproductible avec uv, convention de commits contrôlée en CI, versionnement sémantique automatique et image Docker publiée à chaque version ;
- **Automatiser l'extraction de données depuis un service web (API REST)** — **aucun script d'exemple n'est fourni** : vous concevez seul le point de lancement, la stratégie de pagination, la gestion des erreurs, le retry, les logs et la sauvegarde des résultats bruts ;
- **Contourner une limite d'API réelle** en concevant une stratégie de découpage documentée et justifiée ;
- **Développer des règles de nettoyage et de consolidation** sur des anomalies non annoncées : doublons de grain, unités mélangées, codes géographiques manquants, coordonnées à parser ;
- **Créer une base de données** modélisée selon la méthode Merise (MCD/MPD), avec script DDL versionné et registre RGPD ;
- **Développer des requêtes SQL** d'extraction (sélections, filtrages, jointures, agrégats) répondant à la question centrale.

## Architecture cible

### Le pipeline de données

Un pipeline batch en trois couches, inspiré de l'architecture Medallion, **entièrement dans PostgreSQL** :

- schéma `raw` : les réponses de l'API telles que collectées, horodatées, jamais modifiées ;
- schéma `staging` : les données nettoyées et homogénéisées, toujours au grain du point de charge ;
- schéma `mart` : le modèle relationnel issu de votre MPD Merise, prêt à être interrogé par Sofiane.

```
              +--------------------------------------+
              |   API ODRE IRVE (227k pts de charge) |
              +------------------+-------------------+
                                 |
                 [1. extraction : découpage, retry, logs]
                                 |
   +-----------------------------v------------------------------+
   |  PostgreSQL (Docker)                                        |
   |                                                             |
   |   schéma raw      réponses brutes, horodatées, immuables    |
   |        |                                                    |
   |   [2. nettoyage : unités, booléens, coordonnées, INSEE]     |
   |        v                                                    |
   |   schéma staging  propre, grain point de charge             |
   |        |                                                    |
   |   [3. consolidation : stations, opérateurs, communes…]      |
   |        v                                                    |
   |   schéma mart     modèle Merise (MPD) + requêtes SQL        |
   +-------------------------------------------------------------+
```

### La chaîne de livraison

```
 branche feat/…  ──push / PR──▶  [commitlint]  ── commit non conforme ──▶ ❌ PR bloquée
                                       │ ✅
                                  fusion dans main
                                       │
                                       ▼
                              [semantic-release]
                     feat → mineure · fix → correctif · BREAKING CHANGE → majeure
                     tag vX.Y.Z + GitHub Release + CHANGELOG.md
                                       │  (seulement si une release a été créée)
                                       ▼
                      [docker build (uv) → push GHCR]
                  ghcr.io/<compte>/<repo>:X.Y.Z  et  :latest
                                       │
                                       ▼
            docker run … ghcr.io/<compte>/<repo>:X.Y.Z  →  pipeline rejoué à l'identique
```

> Vous produirez votre propre schéma d'architecture **au format image** (draw.io ou équivalent, pas d'ASCII art), qui montre **les deux** : les couches de données et la chaîne de livraison.

## Données fournies

Le kit de démarrage se trouve dans le dossier [`starter-kit/`](starter-kit/), commun aux deux versions du brief :

- `docker-compose.yml` — pour lancer PostgreSQL 16 en local (`docker compose up -d`) ;
- `.env.example` — variables d'environnement d'exemple (aucun secret réel) ;
- `sources.md` — les URL des sources. **Dans cette version, seule l'API IRVE est utilisée** : ignorez Wikipédia et le CSV Crit'Air E.

**Aucune donnée n'est fournie, aucun script, aucun workflow, aucun Dockerfile non plus.** Vous allez chercher les données réelles vous-même, et vous écrivez vous-même toute la chaîne de livraison : c'est le sujet du brief.

## Travail demandé

Travail individuel sur 5 jours. L'entraide est encouragée (partage de blocages, debug entre pairs), mais chacun rend son propre code et doit pouvoir l'expliquer ligne par ligne, workflows compris.

> **Règle des 2 heures.** Ces données sont réelles : vous rencontrerez des obstacles que ce brief ne mentionne pas. Chercher par soi-même fait partie du métier, s'enliser non. **Bloqué plus de 2 heures sur le même point ? Demandez un indice au formateur.** Ce n'est pas un aveu d'échec, c'est ce que vous ferez en entreprise. Notez simplement le blocage et sa résolution dans votre journal de bord : il fera partie du rendu.

### Phase 1 — La chaîne de livraison d'abord (J1)

Avant la moindre ligne de pipeline, vous construisez **la chaîne qui livrera ce pipeline**, et vous la faites tourner de bout en bout sur un projet presque vide. C'est l'approche du « squelette qui marche » : quand le premier vrai code arrivera, il sera vérifié, versionné et empaqueté dès sa fusion, sans effort supplémentaire. À l'inverse, une CI ajoutée en fin de projet arrive toujours trop tard : l'historique est déjà fait de commits « wip » et « fix final », et le `Dockerfile` découvre le dernier jour des dépendances qu'on aurait voulu voir le deuxième.

Créez le repo GitHub public et initialisez le projet avec uv. Quelle version de Python fixez-vous, et pourquoi celle-là ? Où rangerez-vous les dépendances qui ne servent qu'au développement, comme Jupyter pour vos notebooks d'exploration, pour qu'elles n'atterrissent jamais dans l'image ? Donnez au projet un **point d'entrée minimal** : une commande qui, pour l'instant, se contente d'écrire dans les logs qu'elle a démarré et avec quelle version. C'est elle que l'image lancera, et c'est elle qui grandira jusqu'aux trois scripts du pipeline.

Écrivez le **premier workflow GitHub Actions**, celui qui vérifie les messages de commit. Sur une pull request, vérifie-t-il seulement le dernier commit ou tous ceux de la branche ? Faites-le échouer volontairement avec un commit « wip » pour vous assurer qu'il mord. Protégez ensuite `main` : personne, vous compris, ne pousse directement dessus.

Écrivez le `Dockerfile`, avec uv. D'où vient uv dans l'image, et figez-vous sa version ? Comment installez-vous les dépendances à partir de `uv.lock` sans jamais le résoudre de nouveau, et sans embarquer les dépendances de développement ? Dans quel ordre copiez-vous les fichiers pour que modifier une ligne de code ne réinstalle pas toutes les bibliothèques ? Aujourd'hui l'image n'a presque rien à installer ; dans deux jours elle aura Requests et un pilote PostgreSQL, et c'est maintenant que ce découpage en couches se décide. Votre conteneur tourne-t-il en `root` ? Que contient votre `.dockerignore` — et êtes-vous sûr que ni `.env`, ni `data/`, ni `.venv/` n'y entreront le jour où ces dossiers existeront ?

Mettez enfin en place **semantic-release** sur `main`, enchaîné avec la **construction et la publication de l'image sur GHCR**. Le choix de l'outil vous revient (semantic-release côté Node, python-semantic-release côté Python), mais il doit être justifié. Où vit le numéro de version de votre projet, et comment évitez-vous qu'il diffère entre le tag Git, le `pyproject.toml` et l'image ? semantic-release écrit un `CHANGELOG.md` et parfois un commit sur `main` : comment cela se passe-t-il avec la protection de branche que vous venez de poser, et comment empêchez-vous ce commit de relancer la chaîne en boucle ? Comment le job Docker sait-il qu'une release vient d'avoir lieu, et quel numéro elle porte ? De quelles permissions le `GITHUB_TOKEN` a-t-il besoin, et pourquoi pas plus ? Taguez l'image avec la version exacte et avec `latest` : lequel des deux un dossier client doit-il citer ? Commencez-vous en `0.x` ou en `1.0.0`, et que signifie ce choix pour Sofiane ?

Vérifiez pour finir qu'un commit `docs:` seul **ne déclenche pas** de nouvelle version : c'est le comportement attendu, pas un bug. Rédigez une première version de `docs/ci-cd.md` tant que tout est frais.

**Résultat testable en fin de J1 (point de contrôle formateur) :** une pull request avec un commit non conforme est refusée ; une fusion `feat:` dans `main` produit, sans action manuelle, un tag, une GitHub Release, un `CHANGELOG.md` et une image sur GHCR ; `docker run ghcr.io/<compte>/<repo>:<version>` affiche le message de démarrage avec le bon numéro de version. **Le formateur ne valide pas le passage à la Phase 2 tant que cette chaîne ne tourne pas.**

### Phase 2 — Cadrage et exploration de l'API (J2, matin)

Aucune ligne de code de production. Explorez l'API comme le ferait un auditeur.

Interrogez-la dans le navigateur ou avec `curl` : que renvoie-t-elle avec `limit=1` ? Combien annonce-t-elle de résultats dans `total_count` ? Que se passe-t-il quand vous demandez `limit=100&offset=15000` — et que vous dit le message d'erreur ? C'est le moment de comprendre le mur avant de foncer dedans. Le point d'entrée d'export ou un découpage par filtre vous permettent-ils de passer ? Quels champs vous serviront réellement pour la question centrale, et lesquels sont du bruit ?

Téléchargez une centaine de lignes et regardez-les vraiment : les booléens, les puissances, les coordonnées, les codes INSEE vides. Vérifiez une coordonnée sur une carte.

Documentez la source dans `docs/sources.md` : URL, format, volume, champs retenus, **pièges identifiés**, stratégie de contournement de la limite. Créez votre **Kanban public** (GitHub Projects, Trello…) avec des user stories tirées de la question centrale — par exemple : « En tant que chargé d'études, je veux la part de points de charge rapides par département ». Ces documents passent eux aussi par pull request : quel type de commit leur donnez-vous, et doivent-ils produire une version ?

**Résultat testable en fin de matinée :** documentation de la source relue par un pair, stratégie de contournement écrite noir sur blanc, Kanban rempli.

### Phase 3 — Script d'extraction vers la couche `raw` (J2-J3)

Développez le script d'extraction. Chaque bibliothèque entre dans le projet par `uv add`, jamais autrement — et vous verrez la CI reconstruire une image qui la contient à la release suivante.

Appliquez la stratégie décidée en Phase 2 : si vous découpez par département, comment obtenez-vous la liste des départements, et que faites-vous des lignes dont le code département est vide ? Si une requête échoue au 47ᵉ département, votre script s'arrête-t-il, réessaie-t-il, journalise-t-il l'échec ? À quel rythme appelez-vous une API publique gratuite sans l'agresser ?

Le schéma `raw` garde la réponse **telle qu'elle est arrivée**. Sous quelle forme la stockez-vous : une colonne par champ, ou le JSON entier dans une colonne `jsonb` ? Que perdez-vous dans le premier cas le jour où l'API ajoute un champ ? Comment savez-vous, six mois plus tard, quand chaque ligne a été collectée et par quelle version du pipeline ? Relancer l'extraction ajoute-t-il un nouveau lot daté ou écrase-t-il le précédent ?

Le script a un **point de lancement clair**, initialise ses dépendances et sa connexion, gère erreurs et exceptions, écrit des **logs exploitables**. Il tournera dans l'image : un chemin écrit en dur ou un mot de passe dans le code y échouera. D'où lit-il sa configuration, et comment le conteneur trouve-t-il la base du `docker-compose.yml` ?

Travaillez par **branches et pull requests** : une fonctionnalité, une branche, des commits petits et typés. `feat(extraction): …` ou `fix(api): …` ? Le type choisi n'est pas cosmétique : c'est lui qui décide du prochain numéro de version. **L'historique Git fait partie de l'évaluation.**

Consacrez la fin de la phase à **éprouver votre robustesse** : coupez votre connexion réseau en pleine extraction, relancez, et regardez ce qui se passe. Reprend-elle où elle s'était arrêtée, ou repart-elle de zéro ? Le schéma `raw` contient-il un lot à moitié chargé ? C'est ce test-là, pas le chemin nominal, qui distingue un script d'un pipeline.

**Résultat testable en fin de J3 :** l'extraction se relance par une commande `uv run` unique **et** depuis la dernière image publiée ; `raw` contient l'ensemble des points de charge, lot daté ; les logs racontent le déroulement, y compris les échecs ; une interruption ne laisse pas `raw` dans un état incohérent ; au moins une nouvelle version est sortie depuis J1.

### Phase 4 — Script de nettoyage vers la couche `staging` (J3-J4)

Le script de nettoyage lit `raw` et écrit `staging`, toujours au grain du point de charge.

Homogénéisez les **puissances** : comment distinguez-vous un 22 kW d'un 22 000 W autrement qu'à l'œil, et que faites-vous des puissances nulles ou négatives ? Convertissez les **booléens** sans tomber dans le piège de `bool("False")`. Parsez les **coordonnées** en remettant latitude et longitude à leur place. Que faites-vous des lignes sans code INSEE : vous les rejetez, vous les rattachez autrement (code postal de l'adresse, coordonnées), ou vous les gardez en les marquant ? Où vont les lignes rejetées — disparaissent-elles, ou restent-elles consultables avec la raison du rejet ? Et les coordonnées nominatives des opérateurs : passent-elles en `staging` ?

Chaque règle est **écrite en code** (aucune correction manuelle) et documentée : quelle règle, sur quels champs, combien de lignes affectées. Le script affiche ce décompte à chaque exécution. Une règle corrigée après coup, par exemple un seuil de conversion des watts mal choisi, est un `fix:` : regardez quel numéro de version il produit.

**Résultat testable en fin de J4 (point de contrôle formateur) :** `staging` se reconstruit à l'identique depuis `raw` par une commande unique, et le script affiche le nombre de lignes corrigées et rejetées par règle.

### Phase 5 — Modèle Merise et script de consolidation vers `mart` (J4-J5)

Modélisez la couche `mart` selon la méthode **Merise** : MCD puis MPD, exportés en images. Quelles entités distinguez-vous — une station, un point de charge, un aménageur, un opérateur, une commune, un département ? Un point de charge est-il un attribut de la station ou une entité à part entière ? Un opérateur peut-il exploiter des stations de plusieurs aménageurs ? Les cardinalités que vous posez sont-elles vraies **dans les données**, ou seulement dans votre tête ? Vérifiez-les par une requête sur `staging` avant de les figer.

Traduisez le MPD en **script DDL versionné** (clés primaires, clés étrangères, contraintes, index) pour le schéma `mart`. Écrivez ensuite le **script de consolidation** : il passe du grain point de charge de `staging` à votre modèle, en dédoublonnant les stations, les opérateurs et les communes. Sur quelle clé reconnaissez-vous qu'une station est la même d'une ligne à l'autre, et que faites-vous si deux lignes d'une même station se contredisent ? Le script peut-il être relancé sans créer de doublons ?

Rédigez le **registre RGPD basique** : pour chaque couche, quelles données à caractère personnel y sont, pour quelle finalité, combien de temps. Les coordonnées nominatives d'opérateurs ont-elles leur place dans `mart` ?

Écrivez enfin au moins **trois requêtes SQL** sur `mart` qui répondent à la question centrale : nombre de stations et de points de charge par département, puissance cumulée installée, part des points de charge rapides, départements les moins équipés. Chaque requête est documentée : sélections, filtrages, jointures et leur justification.

**Résultat testable :** depuis une base vide, `docker compose up`, le DDL puis les trois scripts reconstruisent `raw`, `staging` et `mart` ; les requêtes s'exécutent ; la consolidation tourne depuis une version publiée de l'image.

### Phase 6 — Clone propre et démonstration (J5, après-midi)

Finalisez le README, `docs/ci-cd.md` et le schéma d'architecture, et vérifiez que **tout se rejoue depuis un clone propre** : effacez votre dossier de travail, reclonez votre propre repo et déroulez votre README à la lettre, avec `uv sync` puis `uv run`. Faites ensuite la même chose avec la dernière image publiée, sans le repo. C'est le seul test qui compte, et il révèle presque toujours une dépendance non verrouillée, une variable d'environnement non documentée ou un fichier oublié dans le `.dockerignore`.

Rédigez enfin votre **journal de bord** : les blocages rencontrés, ce que vous avez essayé, ce qui a débloqué. C'est un livrable, et c'est aussi ce dont vous parlerez le mieux en démonstration.

Préparez une démonstration de **15 minutes** articulée autour de la question centrale.

### Socle commun (obligatoire)

- Chaîne de livraison **opérationnelle dès J1** : workflow de **vérification des commits**, **semantic-release** sur `main`, **image Docker publiée sur GHCR** à chaque release ; au moins **trois releases** réelles (le squelette de J1, puis au moins deux versions portant du code data).
- Projet entièrement géré avec **uv** (`pyproject.toml`, `uv.lock`, `.python-version` versionnés).
- Les **trois scripts** (extraction, nettoyage, consolidation) fonctionnels, la limite d'API effectivement contournée et documentée.
- Les trois schémas `raw`, `staging` et `mart` dans PostgreSQL ; `mart` conforme au MPD Merise ; au moins **3 requêtes SQL** documentées.
- MCD/MPD, DDL, registre RGPD, `docs/sources.md`, `docs/ci-cd.md`, README, schéma d'architecture, Kanban public.

### Pour aller plus loin (bonus)

- Hook Git local (`commit-msg`) qui refuse un message non conforme avant même le push.
- Rattachement des points de charge sans code INSEE par géocodage inverse via l'API Adresse (`https://api-adresse.data.gouv.fr`).
- Tests unitaires sur les fonctions de nettoyage (conversion des unités, booléens, coordonnées), lancés par `uv run pytest`.
- Image multi-étapes plus légère, et analyse de vulnérabilités de l'image (Trivy ou équivalent).
- Actions tierces épinglées par leur SHA de commit plutôt que par leur tag.
- Extraction incrémentale : détecter les stations nouvelles ou disparues entre deux lots de `raw`.

Les bonus ne compensent jamais un socle incomplet : **terminez d'abord le socle**.

## Livrables

À rendre au plus tard J5 à 17 h (lien du repo posté sur la plateforme) :

- Un **repo GitHub public** avec un README structuré : description du projet et rappel de la question centrale, technologies utilisées et justification, instructions d'installation et de lancement depuis zéro (avec uv **et** avec l'image Docker), architecture, lien vers la dernière release, auteur.
- Les **trois scripts** du pipeline (extraction, nettoyage, consolidation), avec un historique de commits conventionnels réparti sur les 5 jours (pas un commit final unique).
- Le **script DDL** des trois schémas.
- Les **fichiers uv** : `pyproject.toml`, `uv.lock`, `.python-version`.
- Le **`Dockerfile`** et le **`.dockerignore`** du pipeline.
- Les **workflows** dans `.github/workflows/` : vérification des commits, release, construction et publication de l'image.
- Le **`CHANGELOG.md`** généré, **au moins trois GitHub Releases** et l'**image publiée sur GHCR** (paquet public) avec le tag de chaque version.
- Une **note CI/CD** (`docs/ci-cd.md`, une page max) : ce que fait chaque workflow, ses déclencheurs, ses permissions, comment la version est calculée et où elle est écrite, et la commande exacte pour relancer une version donnée.
- Une **note de stratégie d'extraction** (une page max) expliquant comment vous avez contourné la limite `limit + offset ≤ 10 000` et pourquoi cette stratégie plutôt qu'une autre.
- Le **schéma d'architecture** au format image (PNG ou export draw.io), montrant les schémas `raw`, `staging`, `mart` et la chaîne de livraison.
- Les **modèles de données** : MCD et MPD au format image, avec une courte note sur les choix de modélisation (grain, entités, cardinalités vérifiées).
- La **documentation de la source** (`docs/sources.md`) et des **règles de nettoyage** (règle, champs, nombre de lignes affectées).
- La **documentation des requêtes SQL** : pour chaque requête, son objectif métier, ses sélections/filtrages/jointures.
- Le **registre RGPD** des traitements, couche par couche.
- Le lien vers le **Kanban public** (dans le README), avec les user stories et leur historique.
- Le **journal de bord** (`docs/journal.md`) : les blocages rencontrés sur les données réelles et sur la CI, ce que vous avez essayé, ce qui a débloqué. Une ligne par blocage suffit. Il n'est pas noté sur la quantité de galères, mais sur la qualité du diagnostic.

## Démonstration finale

L'évaluation repose sur deux volets pondérés.

**Volet 1 — Démonstration technique individuelle : 70 %.** 15 minutes de démonstration en direct + 10 minutes de questions. Vous relancez le pipeline **depuis l'image publiée** (`docker run` d'une version précise) : extraction, nettoyage, consolidation, avec leurs logs. Vous montrez les trois schémas peuplés, puis exécutez 2 ou 3 requêtes SQL qui répondent à la question centrale. Vous montrez ensuite la chaîne de livraison en direct : un commit non conforme refusé par la CI, puis la page Releases, le `CHANGELOG.md` et le paquet GHCR.

Pour tenir les 15 minutes, l'extraction peut prévoir un **mode échantillon** (paramètre limitant le nombre de départements), à condition de présenter aussi les preuves d'une exécution complète (logs datés, volumes collectés). Les questions porteront sur vos choix : stratégie de contournement de l'API, forme de stockage dans `raw`, règles de nettoyage, modélisation, calcul des versions et contenu de l'image.

**Volet 2 — Revue de code et d'architecture : 30 %.** Structure et lisibilité des trois scripts, gestion des erreurs et des logs, qualité du README et de la documentation, cohérence du schéma d'architecture et des modèles Merise, lisibilité des workflows et du `Dockerfile`, régularité et typage des commits.

> **Validation partielle** : un pipeline qui ne fonctionne pas en démonstration mais dont le code est structuré, versionné et documenté peut valider partiellement les compétences concernées. De même, une chaîne de release incomplète (par exemple, image construite mais non publiée) n'invalide pas les compétences data si le reste est en place. À l'inverse, une démonstration réussie sans documentation ne valide pas les critères documentaires.

Sans repo GitHub public accessible et sans code versionné, le travail ne peut pas être évalué.

## Critères de validation

### Cadre technique d'exploitation : uv, commits, versions et image

- Le projet est géré exclusivement avec uv : `pyproject.toml`, `uv.lock` et `.python-version` sont versionnés, aucun `requirements.txt` ni `pip install` n'apparaît dans le repo, le `Dockerfile` ou les workflows, et le pipeline se lance par `uv run` depuis un clone propre.
- Les commits de `main` respectent Conventional Commits, et un workflow les vérifie à chaque push et pull request : un commit non conforme fait échouer la vérification (démontré en séance).
- Chaque fusion dans `main` contenant un `feat` ou un `fix` produit sans action manuelle un tag SemVer, une GitHub Release et une entrée de `CHANGELOG.md` cohérents entre eux ; la première release date de J1 et au moins trois releases existent.
- L'image Docker est construite avec uv à partir de `uv.lock`, sans dépendances de développement ni secret, publiée sur GHCR uniquement lors d'une release et taguée avec la version ; `docker run` d'une version publiée exécute le pipeline.
- Les workflows ne contiennent aucun secret en clair, limitent les permissions du `GITHUB_TOKEN` au nécessaire, et sont expliqués dans `docs/ci-cd.md`.

### Extraction automatisée depuis l'API (conception en autonomie complète, aucun modèle fourni)

- Le script d'extraction est fonctionnel : l'ensemble des points de charge est effectivement chargé dans `raw` à l'issue de l'exécution.
- La limite de pagination de l'API est effectivement contournée, et la stratégie retenue est documentée et justifiée.
- Le script comprend un point de lancement, l'initialisation des dépendances et de la connexion, la gestion des erreurs et des exceptions (avec retry), des logs exploitables, et un chargement daté qui ne laisse pas `raw` incohérent en cas d'interruption.
- Le script est versionné et accessible depuis un dépôt Git public, avec un historique de commits réparti sur la durée du projet.

### Règles de nettoyage et de consolidation

- Le script de nettoyage est fonctionnel : `staging` se reconstruit depuis `raw` par une commande unique.
- Les unités de puissance, les booléens et les coordonnées sont homogénéisés selon des règles écrites et vérifiables ; les lignes sans code géographique exploitable sont traitées selon une règle explicite (rejet tracé ou rattachement).
- Le script de consolidation passe du grain point de charge au modèle `mart` sans doublons, et peut être relancé sans en créer.
- La documentation précise, pour chaque règle, les champs concernés et le nombre de lignes affectées.

### Création de la base de données

- Les modélisations respectent la méthode et le formalisme Merise ; MCD et MPD sont cohérents entre eux, avec le grain retenu et avec les cardinalités observées dans les données.
- Le choix du SGBD et l'organisation en trois schémas sont justifiés dans le README.
- Le modèle physique est fonctionnel : la base se crée sans erreur depuis le script DDL versionné, et le schéma `mart` est effectivement alimenté par la consolidation.
- Le registre RGPD couvre les données à caractère personnel de chaque couche, et le sort réservé aux coordonnées d'opérateurs est tranché et motivé.

### Requêtes SQL d'extraction

- Les requêtes sont fonctionnelles : les données visées sont effectivement extraites à l'exécution.
- Au moins 3 requêtes mobilisent sélections, filtrages, jointures et agrégats en lien direct avec la question centrale.
- La documentation met en lumière les choix de sélections, filtrages et jointures au regard des objectifs.

## Ressources

Commencez par les cours du dépôt : ils sont écrits pour ce parcours. La documentation officielle sert ensuite de référence pendant le projet.

### GitHub Actions et CI/CD — ce que c'est

<!-- videos:nRXKkMcoDEQ,J38p0Le7tOQ,ruJRPkzcnMs,vLnjO5hvnPc,BiLbI_uNCvg,zgstTcSVBxw,CQMV9-1ho8A,27N697pc3ag -->
> 🎬 **En vidéo** (8 épisodes)
>
> <a href="https://www.youtube.com/watch?v=nRXKkMcoDEQ" title="CI/CD 00 : Pourquoi la CI ? (pipeline)"><img src="https://i.ytimg.com/vi/nRXKkMcoDEQ/mqdefault.jpg" alt="▶ CI/CD 00 : Pourquoi la CI ? (pipeline)" width="260"></a> <a href="https://www.youtube.com/watch?v=J38p0Le7tOQ" title="Git 12 : Écrire de bons commits"><img src="https://i.ytimg.com/vi/J38p0Le7tOQ/mqdefault.jpg" alt="▶ Git 12 : Écrire de bons commits" width="260"></a> <a href="https://www.youtube.com/watch?v=ruJRPkzcnMs" title="CI/CD 05 : Lire un pipeline rouge (corriger, relancer)"><img src="https://i.ytimg.com/vi/ruJRPkzcnMs/mqdefault.jpg" alt="▶ CI/CD 05 : Lire un pipeline rouge (corriger, relancer)" width="260"></a> <a href="https://www.youtube.com/watch?v=vLnjO5hvnPc" title="Git 07 : Les branches (git switch -c, git branch, git merge)"><img src="https://i.ytimg.com/vi/vLnjO5hvnPc/mqdefault.jpg" alt="▶ Git 07 : Les branches (git switch -c, git branch, git merge)" width="260"></a> <a href="https://www.youtube.com/watch?v=BiLbI_uNCvg" title="Git 13 : Bonus : la pull request (GitHub, pull request, revue de code)"><img src="https://i.ytimg.com/vi/BiLbI_uNCvg/mqdefault.jpg" alt="▶ Git 13 : Bonus : la pull request (GitHub, pull request, revue de code)" width="260"></a> <a href="https://www.youtube.com/watch?v=zgstTcSVBxw" title="Git 09 : Pousser vers un dépôt distant (git remote, git push)"><img src="https://i.ytimg.com/vi/zgstTcSVBxw/mqdefault.jpg" alt="▶ Git 09 : Pousser vers un dépôt distant (git remote, git push)" width="260"></a> <a href="https://www.youtube.com/watch?v=CQMV9-1ho8A" title="Git 11 : Mettre de côté et étiqueter (git stash, git tag)"><img src="https://i.ytimg.com/vi/CQMV9-1ho8A/mqdefault.jpg" alt="▶ Git 11 : Mettre de côté et étiqueter (git stash, git tag)" width="260"></a> <a href="https://www.youtube.com/watch?v=27N697pc3ag" title="Git 06 : Ignorer des fichiers (.gitignore, données, secrets)"><img src="https://i.ytimg.com/vi/27N697pc3ag/mqdefault.jpg" alt="▶ Git 06 : Ignorer des fichiers (.gitignore, données, secrets)" width="260"></a>
>
> ▶ [CI/CD 00 : Pourquoi la CI ? (pipeline)](https://www.youtube.com/watch?v=nRXKkMcoDEQ) · ▶ [Git 12 : Écrire de bons commits](https://www.youtube.com/watch?v=J38p0Le7tOQ) · ▶ [CI/CD 05 : Lire un pipeline rouge (corriger, relancer)](https://www.youtube.com/watch?v=ruJRPkzcnMs) · ▶ [Git 07 : Les branches (git switch -c, git branch, git merge)](https://www.youtube.com/watch?v=vLnjO5hvnPc) · ▶ [Git 13 : Bonus : la pull request (GitHub, pull request, revue de code)](https://www.youtube.com/watch?v=BiLbI_uNCvg) · ▶ [Git 09 : Pousser vers un dépôt distant (git remote, git push)](https://www.youtube.com/watch?v=zgstTcSVBxw) · ▶ [Git 11 : Mettre de côté et étiqueter (git stash, git tag)](https://www.youtube.com/watch?v=CQMV9-1ho8A) · ▶ [Git 06 : Ignorer des fichiers (.gitignore, données, secrets)](https://www.youtube.com/watch?v=27N697pc3ag)

- [Cours CI/CD — introduction](../../../07-DevOps/01-CI-CD/01-Introduction/) : intégration continue, livraison continue, pourquoi automatiser.
- [Cours GitHub Actions](../../../07-DevOps/01-CI-CD/03-GitHub-Actions/) : workflows, jobs, déclencheurs, avec des exemples de workflows (dont la construction d'une image Docker).
- [Cours Git](../../../01-Fondamentaux/Git/) — notamment [Conventional Commits](../../../01-Fondamentaux/Git/07-meilleures-pratiques-data.md) et sa vidéo « Écrire de bons commits ».
- GitHub — comprendre GitHub Actions : https://docs.github.com/fr/actions/about-github-actions/understanding-github-actions
- GitHub — démarrage rapide, premier workflow : https://docs.github.com/fr/actions/writing-workflows/quickstart
- GitHub — publier des images Docker (GHCR) : https://docs.github.com/fr/actions/use-cases-and-examples/publishing-packages/publishing-docker-images
- GitHub — permissions du `GITHUB_TOKEN` : https://docs.github.com/fr/actions/security-for-github-actions/security-guides/automatic-token-authentication
- Conventional Commits 1.0.0 : https://www.conventionalcommits.org/fr/v1.0.0/
- commitlint : https://commitlint.js.org/
- Versionnage sémantique 2.0.0 : https://semver.org/lang/fr/
- semantic-release : https://semantic-release.gitbook.io/semantic-release/
- python-semantic-release : https://python-semantic-release.readthedocs.io/

### Les couches raw, staging et mart

- [Cours Data Warehouse — architecture Medallion](../../../05-Databases/DataWarehouse/cours/08-medallion.md) : le même principe sous les noms bronze / silver / gold (bronze = `raw`, silver = `staging`, gold = `mart`).
- [Cours Data Warehouse — architectures](../../../05-Databases/DataWarehouse/cours/04-architectures.md)
- dbt — structurer un projet en staging / intermediate / marts (le vocabulaire le plus répandu) : https://docs.getdbt.com/best-practices/how-we-structure/1-guide-overview
- Databricks — l'architecture Medallion : https://www.databricks.com/glossary/medallion-architecture
- PostgreSQL — les schémas : https://www.postgresql.org/docs/current/ddl-schemas.html
- PostgreSQL — les types JSON (`jsonb`), pour la couche `raw` : https://www.postgresql.org/docs/current/datatype-json.html

### Merise : MCD et MPD

- [Cours Modélisation](../../../01-Fondamentaux/Modelisation/) : [introduction](../../../01-Fondamentaux/Modelisation/01-introduction-modelisation.md), [dictionnaire de données](../../../01-Fondamentaux/Modelisation/02-dictionnaire-donnees.md), [MCD](../../../01-Fondamentaux/Modelisation/03-modele-conceptuel-mcd.md), [MLD](../../../01-Fondamentaux/Modelisation/04-modele-logique-mld.md), [MPD](../../../01-Fondamentaux/Modelisation/05-modele-physique-mpd.md), [outils](../../../01-Fondamentaux/Modelisation/06-outils-pratiques.md) et [exercices](../../../01-Fondamentaux/Modelisation/07-exercices.md).
- Merise (présentation de la méthode) : https://fr.wikipedia.org/wiki/Merise_(informatique)
- Looping, logiciel gratuit de modélisation MCD/MLD avec génération du script SQL : https://www.looping-mcd.fr/

### Docker

- [Cours Docker](../../../02-Containerisation/Docker/) : en priorité [le Dockerfile](../../../02-Containerisation/Docker/04-dockerfile-construction.md), [volumes, réseaux et variables](../../../02-Containerisation/Docker/05-volumes-reseaux-variables.md), [Docker Compose](../../../02-Containerisation/Docker/06-docker-compose-orchestration.md) et [bonnes pratiques](../../../02-Containerisation/Docker/07-concepts-avances-best-practices.md).
- Docker — bien démarrer : https://docs.docker.com/get-started/
- Docker Compose : https://docs.docker.com/compose/
- Image Docker officielle PostgreSQL : https://hub.docker.com/_/postgres

### uv et Python

<!-- videos:X5Q50MLWj60,lFIUbJmwqCk,rHj8HVxq-HA -->
> 🎬 **En vidéo** (3 épisodes)
>
> <a href="https://www.youtube.com/watch?v=X5Q50MLWj60" title="Python 09 : Modules, paquets et API (import, pip, JSON)"><img src="https://i.ytimg.com/vi/X5Q50MLWj60/mqdefault.jpg" alt="▶ Python 09 : Modules, paquets et API (import, pip, JSON)" width="260"></a> <a href="https://www.youtube.com/watch?v=lFIUbJmwqCk" title="Lire le JSON d'une API avec Python et requests, pas à pas"><img src="https://i.ytimg.com/vi/lFIUbJmwqCk/mqdefault.jpg" alt="▶ Lire le JSON d'une API avec Python et requests, pas à pas" width="260"></a> <a href="https://www.youtube.com/watch?v=rHj8HVxq-HA" title="Python 08 : Lire un fichier, gérer les erreurs (with open, csv)"><img src="https://i.ytimg.com/vi/rHj8HVxq-HA/mqdefault.jpg" alt="▶ Python 08 : Lire un fichier, gérer les erreurs (with open, csv)" width="260"></a>
>
> ▶ [Python 09 : Modules, paquets et API (import, pip, JSON)](https://www.youtube.com/watch?v=X5Q50MLWj60) · ▶ [Lire le JSON d'une API avec Python et requests, pas à pas](https://www.youtube.com/watch?v=lFIUbJmwqCk) · ▶ [Python 08 : Lire un fichier, gérer les erreurs (with open, csv)](https://www.youtube.com/watch?v=rHj8HVxq-HA)

- [Cours Python](../../../01-Fondamentaux/Python/)
- uv — documentation officielle : https://docs.astral.sh/uv/
- uv — utiliser uv dans Docker : https://docs.astral.sh/uv/guides/integration/docker/
- uv — utiliser uv dans GitHub Actions : https://docs.astral.sh/uv/guides/integration/github/
- Requests (documentation officielle) : https://requests.readthedocs.io/

### Données, SQL et RGPD

<!-- videos:64_I31Nfukw -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=64_I31Nfukw" title="Bash 21 : Télécharger et archiver (curl, wget, tar)"><img src="https://i.ytimg.com/vi/64_I31Nfukw/mqdefault.jpg" alt="▶ Bash 21 : Télécharger et archiver (curl, wget, tar)" width="320"></a>
>
> ▶ [Bash 21 : Télécharger et archiver (curl, wget, tar)](https://www.youtube.com/watch?v=64_I31Nfukw)

- [Cours SQL](../../../01-Fondamentaux/SQL/)
- Base nationale des IRVE sur ODRE (jeu de données et API) : https://odre.opendatasoft.com/explore/dataset/bornes-irve/
- Documentation de l'API Opendatasoft Explore v2.1 (pagination, filtres, exports) : https://help.opendatasoft.com/apis/ods-explore-v2/
- Fichier consolidé des IRVE sur data.gouv.fr (fiche et schéma du jeu de données) : https://www.data.gouv.fr/datasets/fichier-consolide-des-bornes-de-recharge-pour-vehicules-electriques-irve-statique
- API Adresse (géocodage inverse, pour le bonus) : https://adresse.data.gouv.fr/api-doc/adresse
- CNIL — Le registre des activités de traitement : https://www.cnil.fr/fr/RGPD-le-registre-des-activites-de-traitement
