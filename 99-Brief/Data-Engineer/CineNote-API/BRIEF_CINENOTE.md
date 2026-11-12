# Brief : CinéNote, une API FastAPI avec comptes et rôles, et son interface Streamlit

## Informations

| Critère | Valeur |
|---------|--------|
| **Durée** | 5 jours (35 heures) |
| **Niveau** | Débutant-Intermédiaire |
| **Modalité** | Individuel |
| **Technologies** | Python, uv, FastAPI, SQLModel, PostgreSQL, Streamlit, Docker Compose, JWT, Git |
| **Prérequis** | [Cours FastAPI](../../../01-Fondamentaux/Python/08-FastAPI/) + [Cours Streamlit](../../../12-Frontend-IA/02-Streamlit/) + [Cours Docker](../../../02-Containerisation/Docker/) + [Cours SQL](../../../01-Fondamentaux/SQL/) |
| **Données** | MovieLens « latest-small », données réelles et publiques |

## Contexte

Le ciné-club **Bobine**, à Lille, compte 200 adhérents. Ses membres échangent leurs critiques de films sur un groupe de discussion où tout se perd : impossible de retrouver l'avis d'Inès sur un film d'il y a six mois, ni de savoir quels films le club a le mieux notés.

Le bureau veut une application web à lui. Les membres y publient des critiques et notent des films ; les visiteurs lisent sans compte ; des modérateurs retirent les messages hors charte ; un administrateur gère les comptes. Le catalogue de départ vient d'un jeu de données réel que vous importez.

### La question centrale

> **« Qui a le droit de faire quoi dans CinéNote, et comment l'application le garantit-elle ? »**

### Les données

Le jeu [MovieLens « latest-small »](https://grouplens.org/datasets/movielens/) (GroupLens, université du Minnesota), à télécharger en zip : <https://files.grouplens.org/datasets/movielens/ml-latest-small.zip>.

- `movies.csv` : 9 742 films (`movieId`, `title`, `genres`) ;
- `ratings.csv` : 100 836 notes de 610 utilisateurs anonymes (`userId`, `movieId`, `rating`, `timestamp`) ;
- `tags.csv` : 3 683 mots-clés posés par les utilisateurs ;
- `links.csv` : les identifiants IMDb et TMDb de chaque film.

Les données sont réelles, donc imparfaites. Quelques exemples mesurés sur le fichier :

- l'année est collée au titre (`Toy Story (1995)`), et 13 films n'en ont pas ;
- 1 647 titres ont l'article rejeté à la fin (`Usual Suspects, The (1995)`) ;
- les genres tiennent dans une seule colonne, séparés par `|`, et 34 films ont la valeur `(no genres listed)` ;
- les dates sont des timestamps Unix (`964982703`) ;
- les notes vont de 0,5 à 5 par demi-point.

### Les rôles et les droits

C'est le cœur du brief. Quatre rôles, et une règle de plus : **un membre ne touche qu'à ses propres critiques**.

| Action | Visiteur | Membre | Modérateur | Admin |
|---|---|---|---|---|
| Lire les films et les critiques publiées | oui | oui | oui | oui |
| Noter un film, publier une critique | non | oui | oui | oui |
| Modifier ou supprimer **sa** critique | non | oui | oui | oui |
| Masquer ou supprimer la critique **d'un autre** | non | non | oui | oui |
| Importer les données MovieLens | non | non | non | oui |
| Gérer les comptes et attribuer les rôles | non | non | non | oui |

Une route refusée renvoie **401** si la personne n'est pas connectée, **403** si elle est connectée sans en avoir le droit.

### Ce qu'on attend techniquement

- **uv** pour tout le projet Python : `pyproject.toml`, `uv.lock`, lancement par `uv run`. Pas de `pip install`, pas de `requirements.txt`.
- **SQLModel** comme ORM, sans écrire de code SQLAlchemy directement.
- Un back-end **FastAPI organisé en MVC** :
  - `models/` : les tables SQLModel (le modèle) ;
  - `schemas/` : ce que l'API reçoit et renvoie (la vue) ;
  - `controllers/` : les routes, qui restent minces ;
  - `services/` : la logique métier et les contrôles de droits.
- Un front-end **Streamlit dans son propre dossier**. Il parle uniquement à l'API, jamais à la base.
- **PostgreSQL**, et tout démarre par un seul `docker compose up` : la base, l'API, le front.
- Authentification par **jeton JWT**, mots de passe hachés, aucun secret dans le code ni dans Git.

```
cinenote/
├── backend/
│   ├── app/  (models/, schemas/, controllers/, services/, ...)
│   ├── pyproject.toml
│   └── Dockerfile
├── frontend/
│   ├── app.py
│   ├── pyproject.toml
│   └── Dockerfile
├── docker-compose.yml
└── .env.example
```

## Objectifs pédagogiques

À la fin du brief, vous saurez :

- expliquer **à quoi sert un ORM**, ce qu'il vous évite d'écrire et ce qu'il peut vous cacher ;
- modéliser une base relationnelle et la créer avec SQLModel dans PostgreSQL ;
- importer et nettoyer un jeu de données réel par un script ;
- exposer ces données par une API REST, avec authentification et contrôle des droits par rôle et par propriétaire ;
- construire une interface Streamlit qui consomme cette API ;
- lancer l'ensemble avec Docker Compose.

## Travail demandé

Travail individuel. Entraide bienvenue, mais chacun rend son code et sait l'expliquer.

> **Règle des 2 heures.** Bloqué plus de deux heures sur le même point ? Demandez un indice au formateur, et notez le blocage dans votre journal de bord.

### Phase 1 — Cadrage (J1, matin)

Pas de code. Ouvrez les quatre CSV et regardez-les : que représente une ligne de chaque fichier ? Les 610 utilisateurs de `ratings.csv` sont anonymes : en ferez-vous des comptes de l'application, et s'ils n'ont pas de mot de passe, peuvent-ils se connecter ?

Dessinez le **modèle de données** (MCD) : quelles tables, quelles relations ? Les genres restent-ils une chaîne `Comedy|Drama`, ou deviennent-ils une table à part ? Le rôle d'un utilisateur est-il une colonne ou une table ? Où ranger les identifiants IMDb et TMDb ?

Écrivez les user stories dans un Kanban public, une par ligne du tableau des droits. Créez le repo GitHub.

### Phase 2 — Découvrir l'ORM (J1, après-midi)

<!-- videos:Ae7LHdJwMJ4,JpSpovOrecw -->
> 🎬 **En vidéo** (2 épisodes)
>
> <a href="https://www.youtube.com/watch?v=Ae7LHdJwMJ4" title="Python 12 : Une base de données avec SQLite (sqlite3, INSERT, SELECT)"><img src="https://i.ytimg.com/vi/Ae7LHdJwMJ4/mqdefault.jpg" alt="▶ Python 12 : Une base de données avec SQLite (sqlite3, INSERT, SELECT)" width="260"></a> <a href="https://www.youtube.com/watch?v=JpSpovOrecw" title="Python 11 : Les classes et les objets (class, méthode, fit/predict)"><img src="https://i.ytimg.com/vi/JpSpovOrecw/mqdefault.jpg" alt="▶ Python 11 : Les classes et les objets (class, méthode, fit/predict)" width="260"></a>
>
> ▶ [Python 12 : Une base de données avec SQLite (sqlite3, INSERT, SELECT)](https://www.youtube.com/watch?v=Ae7LHdJwMJ4) · ▶ [Python 11 : Les classes et les objets (class, méthode, fit/predict)](https://www.youtube.com/watch?v=JpSpovOrecw)

Lancez PostgreSQL avec Docker Compose. Créez la table des films **à la main, en SQL**, insérez trois films, et écrivez la requête des films de 1995. Faites ensuite la même chose avec **SQLModel** : une classe `Film`, une session, un `select()`.

Comparez les deux. Qu'avez-vous arrêté d'écrire ? Que se passe-t-il si une valeur n'a pas le bon type ? Et maintenant, quelle requête SQL SQLModel envoie-t-il vraiment ? Activez l'affichage des requêtes (`echo=True`) pour le voir. Notez vos conclusions dans `docs/orm.md`, en une demi-page : ce que l'ORM apporte, et un cas où il vaut mieux écrire le SQL soi-même.

### Phase 3 — Base et import (J2)

Créez toutes vos tables avec SQLModel, relations comprises. Écrivez le **script d'import** des CSV : séparer l'année du titre, remettre l'article à sa place, éclater les genres, convertir les timestamps en dates. Que fait votre script des 13 films sans année ? Peut-on le relancer sans créer de doublons ?

Le script affiche à la fin le nombre de lignes importées, corrigées et rejetées.

### Phase 4 — L'API (J3-J4)

Organisez le back-end en MVC. Commencez par les routes de lecture, publiques. Ajoutez ensuite l'inscription, la connexion (jeton JWT) et les routes protégées.

Quelques questions à vous poser en route. Si votre route renvoie directement la table `Utilisateur`, que voit-on dans la réponse ? (Pensez au mot de passe haché.) Où vérifiez-vous les droits : dans chaque route, ou une seule fois dans une dépendance réutilisable ? Comment l'API sait-elle qu'une critique appartient à la personne connectée ? Testez chaque ligne du tableau des droits dans la documentation `/docs`, et vérifiez que vous obtenez bien 401 ou 403 là où il faut.

### Phase 5 — Le front Streamlit et Docker Compose (J4-J5)

Construisez l'interface Streamlit : une page de connexion, le catalogue avec recherche, la fiche d'un film avec ses critiques, et une page d'accueil avec quelques chiffres (films les mieux notés, notes par genre). Où gardez-vous le jeton entre deux pages ? L'interface masque-t-elle les boutons qu'un visiteur n'a pas le droit d'utiliser ? Elle doit le faire, mais l'API doit refuser quand même : pourquoi les deux ?

Terminez par Docker Compose. Depuis un clone propre, `docker compose up` doit suffire à tout lancer. Comment l'API attend-elle que PostgreSQL soit prête ? Comment le conteneur Streamlit trouve-t-il l'API ?

Le dernier après-midi, effacez votre dossier, reclonez votre repo et suivez votre README à la lettre. Préparez la démonstration.

### Pour aller plus loin (bonus)

- Importer `tags.csv`, en regroupant les tags qui ne diffèrent que par la casse (1 589 tags distincts, 1 475 une fois la casse et les espaces ignorés).
- Pagination et filtres sur le catalogue (genre, année, note minimale).
- Tests avec `pytest` sur les droits : un test par ligne du tableau.
- Migrations de schéma avec Alembic.

## Livrables

- Un **repo GitHub public** avec un README : le projet, comment le lancer, les comptes de démonstration (un par rôle), l'architecture, l'auteur.
- Le code du back-end et du front-end, et le `docker-compose.yml`.
- Le script d'import des données MovieLens.
- Le **MCD** au format image.
- `docs/orm.md` : ce que vous avez retenu de la comparaison SQL brut / SQLModel.
- Le lien vers le Kanban.
- Un **journal de bord** (`docs/journal.md`) : une ligne par blocage, avec ce qui l'a résolu.

## Évaluation

**Démonstration : 70 %.** 15 minutes, puis 10 minutes de questions. Lancez tout avec `docker compose up`, puis connectez-vous successivement avec les quatre rôles et montrez ce que chacun peut faire et ne peut pas faire. Montrez aussi un appel refusé directement sur l'API, sans passer par Streamlit.

**Revue du code : 30 %.** Séparation MVC, clarté du code, gestion des droits, README.

> **Validation partielle** : une application qui ne démarre pas en démonstration, mais dont le code est clair, versionné et documenté, peut valider une partie des compétences.

## Critères de validation

### Créer la base de données

- Le MCD est cohérent avec les tables réellement créées.
- Les tables et leurs relations sont créées par SQLModel dans PostgreSQL, sans erreur, depuis un clone propre.
- `docs/orm.md` explique ce que fait un ORM, avec l'exemple comparé SQL brut / SQLModel.

### Importer et nettoyer les données

- Le script importe les films, les genres et les notes MovieLens dans la base.
- L'année, le titre, les genres et les dates sont nettoyés par des règles écrites dans le code.
- Le script peut être relancé sans créer de doublons, et affiche le décompte des lignes importées et rejetées.

### Partager les données par une API REST

- L'API expose le catalogue et les critiques, organisée en MVC (modèles, schémas, contrôleurs, services).
- L'authentification par JWT fonctionne, et les mots de passe sont stockés hachés.
- Chaque ligne du tableau des droits est respectée, avec 401 et 403 aux bons endroits, y compris la règle du propriétaire.
- Aucune réponse de l'API ne contient de mot de passe, haché ou non.

### Interface et déploiement

- L'interface Streamlit consomme l'API et n'accède jamais directement à la base.
- `docker compose up` lance la base, l'API et le front depuis un clone propre, sans autre manipulation que la copie du `.env`.
- Le projet utilise uv, et aucun secret n'est versionné.

## Ressources

- [Cours FastAPI](../../../01-Fondamentaux/Python/08-FastAPI/), notamment [bases de données](../../../01-Fondamentaux/Python/08-FastAPI/05-bases-de-donnees.md) et [authentification](../../../01-Fondamentaux/Python/08-FastAPI/06-authentification.md)
- [Cours ORM](../../../05-Databases/ORM/), [introduction](../../../05-Databases/ORM/cours/01-introduction.md) et [partie SQLModel](../../../05-Databases/ORM/01-Python/02-SQLModel/)
- [Cours Streamlit](../../../12-Frontend-IA/02-Streamlit/), notamment [l'état et les sessions](../../../12-Frontend-IA/02-Streamlit/03-state-sessions.md)
- [Cours Docker](../../../02-Containerisation/Docker/), notamment [Docker Compose](../../../02-Containerisation/Docker/06-docker-compose-orchestration.md)
- [Cours Modélisation (MCD)](../../../01-Fondamentaux/Modelisation/03-modele-conceptuel-mcd.md)
- SQLModel, documentation officielle : <https://sqlmodel.tiangolo.com/>
- SQLModel, des bases de données au code (ce qu'est un ORM) : <https://sqlmodel.tiangolo.com/db-to-code/>
- SQLModel avec FastAPI : <https://sqlmodel.tiangolo.com/tutorial/fastapi/>
- FastAPI, OAuth2 et jetons JWT : <https://fastapi.tiangolo.com/fr/tutorial/security/oauth2-jwt/>
- uv : <https://docs.astral.sh/uv/>
- Streamlit : <https://docs.streamlit.io/>
- Docker Compose : <https://docs.docker.com/compose/>
- MovieLens : <https://grouplens.org/datasets/movielens/>
