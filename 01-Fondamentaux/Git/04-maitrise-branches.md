# 04 - Maîtriser les branches

[← 03 - Premiers pas](03-premiers-pas.md) | [🏠 Accueil](README.md) | [05 - Collaboration et Remotes →](05-collaboration-remotes.md)

---

## 1. Pourquoi utiliser des branches ?
Les branches permettent d'isoler le développement. Vous travaillez sur une nouvelle feature ou un bug fix sans casser la branche principale (`main`).

---

## 2. Gérer les branches

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
<!-- videos:_crDzJ8HiPI -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=_crDzJ8HiPI" title="Git : Résoudre un conflit (marqueurs, résolution)"><img src="https://i.ytimg.com/vi/_crDzJ8HiPI/mqdefault.jpg" alt="▶ Git : Résoudre un conflit (marqueurs, résolution)" width="320"></a>
>
> ▶ [Git : Résoudre un conflit (marqueurs, résolution)](https://www.youtube.com/watch?v=_crDzJ8HiPI)

Un conflit survient quand deux branches modifient la même ligne.
1. Tentez le merge : `git merge feature/X`.
2. Si conflit, ouvrez le fichier et cherchez les marqueurs `<<<<<<<`, `=======`, `>>>>>>>`.
3. Éditez pour garder le bon code.
4. Marquez comme résolu : `git add <fichier>`.
5. Finalisez : `git commit`.

---

[← 03 - Premiers pas](03-premiers-pas.md) | [🏠 Accueil](README.md) | [05 - Collaboration et Remotes →](05-collaboration-remotes.md)
