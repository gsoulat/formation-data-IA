# Les deux flux du brief — points d'entrée

Ce fichier ne contient **que les URL de départ et les premières commandes d'exploration**.
La conception (format d'événement, topics, producteur, consommateurs) est votre travail.

Les deux flux sont **publics, réels, sans authentification**. Ce sont des services publics
gratuits : identifiez-vous avec un `User-Agent` explicite et ne les sondez pas plus vite
que nécessaire.

---

## 1. Vélib' Métropole (Paris) — API Opendatasoft Explore v2.1

- Fiche du jeu de données : https://opendata.paris.fr/explore/dataset/velib-disponibilite-en-temps-reel/
- Point d'entrée `records` : https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records
- Documentation de l'API : https://help.opendatasoft.com/apis/ods-explore-v2/

Premier appel :

```bash
curl -s --compressed \
  "https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records?limit=1" \
  | python3 -m json.tool
```

Questions à vous poser tout de suite : que vaut `total_count` ? Quel est le type de
`is_renting` ? Sous quel format est l'horodatage ? Rappelez-vous que cette API, comme
toutes les API Opendatasoft, plafonne `limit` et `offset`.

## 2. Vélo'v (Lyon) — flux GBFS 2.3

- Index GBFS : https://download.data.grandlyon.com/files/rdata/jcd_jcdecaux.jcdvelov/gbfs.json
- Spécification GBFS : https://gbfs.org/specification/reference/

Premier appel :

```bash
curl -s --compressed \
  "https://download.data.grandlyon.com/files/rdata/jcd_jcdecaux.jcdvelov/gbfs.json" \
  | python3 -m json.tool
```

Ce fichier ne contient **aucune donnée de station** : c'est un index qui pointe vers
d'autres fichiers. Lesquels vous servent ? Combien devez-vous en joindre, et sur quelle clé ?
Regardez aussi `ttl` et `last_updated` : ils vous disent à quelle fréquence la source
se rafraîchit réellement, et donc à quelle fréquence il est utile de la sonder.

## 3. Autres réseaux GBFS français (bonus)

- Liste complète : https://transport.data.gouv.fr/datasets?type=vehicles-sharing

Brancher un troisième réseau est le vrai test de votre normalisation : si votre plateforme
est bien conçue, seule la configuration devrait changer.

## 4. Flux haut débit (bonus)

- Wikimedia EventStreams (SSE) : https://stream.wikimedia.org/v2/stream/recentchange
- Documentation : https://wikitech.wikimedia.org/wiki/Event_Platform/EventStreams

---

## Rappel

Aucun `docker-compose.yml`, aucun code de producteur ni de consommateur n'est fourni.
C'est le sujet du brief.
