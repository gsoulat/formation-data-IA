# 03 - Premiers pas : Créer et gérer un dépôt

[← 02 - Configuration](02-installation-configuration.md) | [🏠 Accueil](README.md) | [04 - Maîtrise des branches →](04-maitrise-branches.md)

---

## 1. Initialiser ou Cloner un dépôt

<!-- videos:TZBoKJtJ1hc -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=TZBoKJtJ1hc" title="Git : Ton premier dépôt (git init, git status)"><img src="https://i.ytimg.com/vi/TZBoKJtJ1hc/mqdefault.jpg" alt="▶ Git : Ton premier dépôt (git init, git status)" width="320"></a>
>
> ▶ [Git : Ton premier dépôt (git init, git status)](https://www.youtube.com/watch?v=TZBoKJtJ1hc)

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

<!-- videos:mPUDu9emOD4 -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=mPUDu9emOD4" title="Git : Les trois zones (git add, git commit -m)"><img src="https://i.ytimg.com/vi/mPUDu9emOD4/mqdefault.jpg" alt="▶ Git : Les trois zones (git add, git commit -m)" width="320"></a>
>
> ▶ [Git : Les trois zones (git add, git commit -m)](https://www.youtube.com/watch?v=mPUDu9emOD4)

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

<!-- videos:YR9NlTpS0CQ -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=YR9NlTpS0CQ" title="Git : Lire l'historique (git diff, git show)"><img src="https://i.ytimg.com/vi/YR9NlTpS0CQ/mqdefault.jpg" alt="▶ Git : Lire l'historique (git diff, git show)" width="320"></a>
>
> ▶ [Git : Lire l'historique (git diff, git show)](https://www.youtube.com/watch?v=YR9NlTpS0CQ)

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
