# 06 - Commandes avancées et débogage

[← 05 - Collaboration](05-collaboration-remotes.md) | [🏠 Accueil](README.md) | [07 - Meilleures Pratiques Data →](07-meilleures-pratiques-data.md)

---

## 1. Annuler des modifications

<!-- videos:J6EoB6R9SzI -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=J6EoB6R9SzI" title="Git : Annuler des changements (git restore, git revert)"><img src="https://i.ytimg.com/vi/J6EoB6R9SzI/mqdefault.jpg" alt="▶ Git : Annuler des changements (git restore, git revert)" width="320"></a>
>
> ▶ [Git : Annuler des changements (git restore, git revert)](https://www.youtube.com/watch?v=J6EoB6R9SzI)

### Restaurer un fichier (Undo local)
```bash
git restore script.py
```

### Unstage un fichier
```bash
git restore --staged script.py
```

### Annuler des commits (Reset)
- `--soft` : Annule le commit, garde les modifs stagées.
- `--hard` : Annule tout (DANGER : perte de données possible).
```bash
git reset --hard HEAD~1
```

---

## 2. Stash : Mettre de côté
<!-- videos:5oqJkUY_V48 -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=5oqJkUY_V48" title="Git : Mettre de côté et étiqueter (git stash, git tag)"><img src="https://i.ytimg.com/vi/5oqJkUY_V48/mqdefault.jpg" alt="▶ Git : Mettre de côté et étiqueter (git stash, git tag)" width="320"></a>
>
> ▶ [Git : Mettre de côté et étiqueter (git stash, git tag)](https://www.youtube.com/watch?v=5oqJkUY_V48)

Utile pour changer de branche sans committer un travail inachevé.
```bash
git stash              # Sauvegarder
git stash list         # Voir la liste
git stash pop          # Récupérer et supprimer
```

---

## 3. Débogage et Recherche
- **Blame** : Qui a modifié quelle ligne ?
  ```bash
  git blame script.py
  ```
- **Bisect** : Trouver quel commit a introduit un bug via une recherche binaire.
- **Reflog** : L'historique de toutes vos actions Git (votre filet de sécurité !).

---

## 4. Tags
Marquez vos versions importantes (ex: releases prod).
```bash
git tag -a v1.0.0 -m "Production release"
git push origin v1.0.0
```

---

[← 05 - Collaboration](05-collaboration-remotes.md) | [🏠 Accueil](README.md) | [07 - Meilleures Pratiques Data →](07-meilleures-pratiques-data.md)
