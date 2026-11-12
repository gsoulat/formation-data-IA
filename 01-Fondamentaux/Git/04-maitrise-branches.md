# 04 - Maîtriser les branches

[← 03 - Premiers pas](03-premiers-pas.md) | [🏠 Accueil](README.md) | [05 - Collaboration et Remotes →](05-collaboration-remotes.md)

---

## 1. Pourquoi utiliser des branches ?
Les branches permettent d'isoler le développement. Vous travaillez sur une nouvelle feature ou un bug fix sans casser la branche principale (`main`).

---

## 2. Gérer les branches

<!-- videos:vLnjO5hvnPc -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=vLnjO5hvnPc" title="Git 07 : Les branches (git switch -c, git branch, git merge)"><img src="https://i.ytimg.com/vi/vLnjO5hvnPc/mqdefault.jpg" alt="▶ Git 07 : Les branches (git switch -c, git branch, git merge)" width="320"></a>
>
> ▶ [Git 07 : Les branches (git switch -c, git branch, git merge)](https://www.youtube.com/watch?v=vLnjO5hvnPc)

### Créer et naviguer
```bash
git branch feature/etl-module      # Créer
git switch feature/etl-module      # Basculer
# OU (syntaxe moderne pour créer et changer)
git switch -c feature/etl-module
```

### Fusionner (Merge)
```bash
git switch main
git merge feature/etl-module
```

---

## 3. Stratégies courantes
- **GitHub Flow** : Une branche `main` stable, chaque feature part de `main` et y retourne après review.
- **Git Flow** : Plus complexe, avec branches `develop`, `release` et `hotfix`. Recommandé pour les gros projets Data.

---

## 4. Résoudre les conflits
<!-- videos:yxS9WDdya2Y -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=yxS9WDdya2Y" title="Git 08 : Résoudre un conflit (marqueurs, résolution)"><img src="https://i.ytimg.com/vi/yxS9WDdya2Y/mqdefault.jpg" alt="▶ Git 08 : Résoudre un conflit (marqueurs, résolution)" width="320"></a>
>
> ▶ [Git 08 : Résoudre un conflit (marqueurs, résolution)](https://www.youtube.com/watch?v=yxS9WDdya2Y)

Un conflit survient quand deux branches modifient la même ligne.
1. Tentez le merge : `git merge feature/X`.
2. Si conflit, ouvrez le fichier et cherchez les marqueurs `<<<<<<<`, `=======`, `>>>>>>>`.
3. Éditez pour garder le bon code.
4. Marquez comme résolu : `git add <fichier>`.
5. Finalisez : `git commit`.

---

[← 03 - Premiers pas](03-premiers-pas.md) | [🏠 Accueil](README.md) | [05 - Collaboration et Remotes →](05-collaboration-remotes.md)
