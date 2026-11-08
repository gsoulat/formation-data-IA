# 07 - Meilleures pratiques pour le Data Engineering

[← 06 - Avancé](06-commandes-avancees-debogage.md) | [🏠 Accueil](README.md) | [08 - Workflows et Automation →](08-workflows-automation.md)

---

## 1. Le .gitignore : Vital pour la Data
<!-- videos:A1uyxPPGJM4 -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=A1uyxPPGJM4" title="Git : Ignorer des fichiers (.gitignore, données, secrets)"><img src="https://i.ytimg.com/vi/A1uyxPPGJM4/mqdefault.jpg" alt="▶ Git : Ignorer des fichiers (.gitignore, données, secrets)" width="320"></a>
>
> ▶ [Git : Ignorer des fichiers (.gitignore, données, secrets)](https://www.youtube.com/watch?v=A1uyxPPGJM4)

Évitez de commiter des données ou des secrets.

```text
# NE JAMAIS VERSIONNER LES DONNÉES
*.csv
*.parquet
data/

# Credentials
.env
config/secrets.yaml

# Notebooks
.ipynb_checkpoints/
```

### 💡 Astuce Jupyter Notebooks
Utilisez des outils comme `nbstripout` pour retirer les résultats d'exécution (images, tables) avant de committer, afin de garder un historique propre et léger.

---

## 2. Conventional Commits
<!-- videos:2wzXzeb8npU -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=2wzXzeb8npU" title="Git : Écrire de bons commits"><img src="https://i.ytimg.com/vi/2wzXzeb8npU/mqdefault.jpg" alt="▶ Git : Écrire de bons commits" width="320"></a>
>
> ▶ [Git : Écrire de bons commits](https://www.youtube.com/watch?v=2wzXzeb8npU)

Utilisez des messages structurés pour automatiser vos changelogs :
- `feat:` Nouvelle fonctionnalité.
- `fix:` Correction de bug.
- `docs:` Documentation.
- `perf:` Amélioration de performance.

---

## 3. Git LFS (Large File Storage)
Si vous **devez** versionner des fichiers volumineux (ex: modèles ML), utilisez Git LFS pour ne pas ralentir le dépôt.

---

[← 06 - Avancé](06-commandes-avancees-debogage.md) | [🏠 Accueil](README.md) | [08 - Workflows et Automation →](08-workflows-automation.md)
