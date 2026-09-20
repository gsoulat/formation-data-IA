# Formation Django & Django REST Framework

## Objectifs pédagogiques

À la fin de cette formation, vous serez capable de :

- Créer une application web complète avec Django
- Modéliser des données avec l'ORM Django
- Exposer une API REST avec Django REST Framework
- Sécuriser vos endpoints avec JWT
- Déployer une application Django en production avec Docker

## Prérequis

- Python 3.10+ maîtrisé
- Notions de bases de données relationnelles (SQL)
- Connaissance du protocole HTTP et des API REST
- Git

## Plan de la formation

### 1. Fondamentaux Django

| Module | Contenu |
|--------|---------|
| [01 — Introduction](01-Fondamentaux/01-introduction.md) | MVT, installation, premier projet |
| [02 — Modèles](01-Fondamentaux/02-modeles.md) | ORM, champs, relations |
| [03 — Vues](01-Fondamentaux/03-vues.md) | FBV, CBV, mixins |
| [04 — Templates](01-Fondamentaux/04-templates.md) | Moteur de templates, héritage |
| [05 — Admin](01-Fondamentaux/05-admin.md) | Interface admin, personnalisation |

### 2. ORM Django

| Module | Contenu |
|--------|---------|
| [01 — Requêtes](02-ORM-Django/01-requetes.md) | QuerySet, filter, annotate |
| [02 — Relations](02-ORM-Django/02-relations.md) | FK, M2M, O2O, optimisations |
| [03 — Migrations](02-ORM-Django/03-migrations.md) | makemigrations, data migrations |

### 3. Django REST Framework

| Module | Contenu |
|--------|---------|
| [README DRF](03-DRF/README.md) | Vue d'ensemble DRF |
| [01 — Introduction](03-DRF/01-introduction.md) | Sérialiseurs, vues, routeurs |
| [02 — Sérialiseurs](03-DRF/02-serializers.md) | ModelSerializer, validation |
| [03 — ViewSets](03-DRF/03-viewsets.md) | ViewSet, ModelViewSet, Router |
| [04 — Authentification](03-DRF/04-authentification.md) | Token, JWT |
| [05 — Permissions](03-DRF/05-permissions.md) | Permissions, sécurité |

### 4. Avancé

| Module | Contenu |
|--------|---------|
| [01 — Middleware](04-Avance/01-middleware.md) | Création et usage de middlewares |
| [02 — Signaux](04-Avance/02-signals.md) | Système de signaux Django |
| [03 — Cache](04-Avance/03-cache.md) | Stratégies de cache Redis |

### 5. Déploiement

| Module | Contenu |
|--------|---------|
| [01 — Settings production](05-Deploiement/01-settings-prod.md) | Configuration sécurisée |
| [02 — Docker](05-Deploiement/02-docker.md) | Dockerfile, docker-compose |

### 6. Exercices

| Exercice | Contenu |
|----------|---------|
| [Blog API](exercices/exercice-01-blog-api.md) | API REST blog complet avec auth |
| [Todo App](exercices/exercice-02-todo-app.md) | Application todo complète |

---

## Installation rapide

```bash
# Créer un environnement virtuel
python -m venv venv
source venv/bin/activate  # Linux/macOS
# venv\Scripts\activate   # Windows

# Installer Django et DRF
pip install django djangorestframework

# Créer un projet
django-admin startproject monprojet .

# Lancer le serveur
python manage.py runserver
```

## Stack technique utilisée

- **Django** 4.2 LTS
- **Django REST Framework** 3.15
- **djangorestframework-simplejwt** 5.3
- **PostgreSQL** 15 (en production)
- **Gunicorn** (serveur WSGI)
- **Nginx** (reverse proxy)
- **Docker** + **docker-compose**

## Conventions de nommage utilisées dans ce cours

- Les projets Django s'appellent `config/` (dossier de configuration)
- Les applications Django sont nommées au pluriel et en minuscules : `articles`, `users`, `orders`
- Les modèles sont en PascalCase : `Article`, `UserProfile`
- Les serializers suivent le pattern : `ArticleSerializer`, `ArticleDetailSerializer`
- Les ViewSets suivent le pattern : `ArticleViewSet`
