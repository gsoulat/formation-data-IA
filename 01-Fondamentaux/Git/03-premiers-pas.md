# 03 - Premiers pas : Créer et gérer un dépôt

[← 02 - Configuration](02-installation-configuration.md) | [🏠 Accueil](README.md) | [04 - Maîtrise des branches →](04-maitrise-branches.md)

---

## 1. Initialiser ou Cloner un dépôt

<!-- videos:8hZqT0y1Ke4 -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=8hZqT0y1Ke4" title="Git 02 : Ton premier dépôt (git init, git status)"><img src="https://i.ytimg.com/vi/8hZqT0y1Ke4/mqdefault.jpg" alt="▶ Git 02 : Ton premier dépôt (git init, git status)" width="320"></a>
>
> ▶ [Git 02 : Ton premier dépôt (git init, git status)](https://www.youtube.com/watch?v=8hZqT0y1Ke4)

### Nouveau projet local
```bash
mkdir mon-projet-data
cd mon-projet-data
git init
```

### Récupérer un projet existant
```bash
git clone https://github.com/username/projet.git
```

---

## 2. Le cycle de vie d'un fichier

<!-- videos:pIzqeydu9jU,sYoazNOseQQ -->
> 🎬 **En vidéo** (2 épisodes)
>
> <a href="https://www.youtube.com/watch?v=pIzqeydu9jU" title="Git 03 : Les trois zones (git add, git commit -m)"><img src="https://i.ytimg.com/vi/pIzqeydu9jU/mqdefault.jpg" alt="▶ Git 03 : Les trois zones (git add, git commit -m)" width="260"></a> <a href="https://www.youtube.com/watch?v=sYoazNOseQQ" title="VS Code 08 : Git dans VS Code (modifications, indexer, valider)"><img src="https://i.ytimg.com/vi/sYoazNOseQQ/mqdefault.jpg" alt="▶ VS Code 08 : Git dans VS Code (modifications, indexer, valider)" width="260"></a>
>
> ▶ [Git 03 : Les trois zones (git add, git commit -m)](https://www.youtube.com/watch?v=pIzqeydu9jU) · ▶ [VS Code 08 : Git dans VS Code (modifications, indexer, valider)](https://www.youtube.com/watch?v=sYoazNOseQQ)

### Vérifier l'état
```bash
git status
```

### Ajouter des modifications (Staging)
```bash
git add script.py      # Fichier spécifique
git add .              # Tout le dossier actuel
```

### Créer un commit (Snapshot)
```bash
git commit -m "feat: add initial data extraction script"
```

---

## 3. Consulter l'historique

<!-- videos:yz4V0QwIXXA -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=yz4V0QwIXXA" title="Git 04 : Lire l'historique (git diff, git show)"><img src="https://i.ytimg.com/vi/yz4V0QwIXXA/mqdefault.jpg" alt="▶ Git 04 : Lire l'historique (git diff, git show)" width="320"></a>
>
> ▶ [Git 04 : Lire l'historique (git diff, git show)](https://www.youtube.com/watch?v=yz4V0QwIXXA)

### Liste des commits
```bash
git log                # Complet
git log --oneline      # Résumé
git log --graph        # Vue graphique des branches
```

### Voir un commit spécifique
```bash
git show <commit_hash>
```

---

## 💡 Conseil : Commits atomiques
Évitez de créer des commits géants. Un commit doit représenter une seule modification logique (ex: une fonction, une correction de bug). Cela facilite grandement la revue de code et le retour en arrière.

---

[← 02 - Configuration](02-installation-configuration.md) | [🏠 Accueil](README.md) | [04 - Maîtrise des branches →](04-maitrise-branches.md)
