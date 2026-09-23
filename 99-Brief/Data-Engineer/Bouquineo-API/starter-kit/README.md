# Starter-kit — Mini-brief 2 (API de restitution)

## Contenu

- `docker-compose.yml` — PostgreSQL 16 avec contrôle de santé.
- `.env.example` — variables attendues. Copiez-le en `.env` et adaptez.

## Démarrage

```bash
cp .env.example .env      # puis adaptez les valeurs
docker compose up -d
docker compose ps         # le service doit être "healthy"
```

## Quel jeu de données utiliser

Celui que vous avez collecté au mini-brief 1 : les deux mini-briefs s'enchaînent.

Une collecte incomplète n'est pas bloquante. Ce mini-brief évalue l'API, pas le scraping, et
il ne réclame nulle part les 1 000 livres — quelques centaines de lignes bien structurées
suffisent. Si votre base est vide, relancez votre scraper sur deux ou trois catégories et
passez à la suite.

Aucun squelette d'API n'est fourni : c'est le sujet du mini-brief.
