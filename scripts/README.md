# Scripts du dépôt

## `inserer_videos.py` — vidéos YouTube du Studio Formation dans les cours

Ajoute sous les sections des cours (`01-Fondamentaux/`) une miniature cliquable vers l'épisode correspondant
de la chaîne, avec son titre en lien.

```bash
python3 scripts/inserer_videos.py --dry-run   # ce qui changerait
python3 scripts/inserer_videos.py             # applique
```

**À relancer après chaque envoi YouTube depuis le studio.** Les épisodes pas encore en ligne sont déjà prévus
dans le plan : ils apparaissent tout seuls dès que YouTube les sert. Le script affiche à la fin la liste de
ceux qui manquent encore.

- **Source** : les `etat.json` du studio (`$FORMATION_VIDEOS`, par défaut `~/Movies/Formation-Videos`).
  Le script ne marche donc que sur le Mac où tourne le studio.
- **Filtre** : seules les vidéos lisibles publiquement (publiques ou non répertoriées) sont insérées. Une vidéo
  privée n'apparaît pas.
- **Relançable** : le bloc de chaque section porte un marqueur `<!-- videos:… -->` et il est régénéré à chaque
  passage, jamais dupliqué. Ne modifie pas ces blocs à la main.
- **Associer un nouvel épisode à une section** : ajoute une ligne `(fichier, "## titre exact", ["module/épisode"])`
  dans `PLAN`. Si un titre de section change dans un cours, le script s'arrête sur une `ValueError` : il faut
  alors mettre à jour le titre dans `PLAN`.
- **Pourquoi une miniature et pas un lecteur** : GitHub retire les `<iframe>` du Markdown. Le lien
  `<a><img></a>` est le seul format qui s'affiche partout.
