# 05 - Collaboration avec des dépôts distants

[← 04 - Branches](04-maitrise-branches.md) | [🏠 Accueil](README.md) | [06 - Commandes Avancées →](06-commandes-avancees-debogage.md)

---

## 1. Qu'est-ce qu'un remote ?
C'est la version de votre projet hébergée sur un serveur (GitHub, GitLab, Bitbucket).

### Gérer les remotes
```bash
git remote add origin https://github.com/user/repo.git
git remote -v          # Voir la liste
```

---

## 2. Synchroniser le code

### Envoyer (Push)
<!-- videos:Pf6TEMU_reU -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=Pf6TEMU_reU" title="Git : Pousser vers un dépôt distant (git remote, git push, git clone)"><img src="https://i.ytimg.com/vi/Pf6TEMU_reU/mqdefault.jpg" alt="▶ Git : Pousser vers un dépôt distant (git remote, git push, git clone)" width="320"></a>
>
> ▶ [Git : Pousser vers un dépôt distant (git remote, git push, git clone)](https://www.youtube.com/watch?v=Pf6TEMU_reU)

```bash
git push origin main
git push -u origin feature/X   # -u lie la branche locale à la distante
```

### Récupérer (Fetch / Pull)
<!-- videos:DTxdCRIRx2I -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=DTxdCRIRx2I" title="Git : Récupérer les changements (git fetch, git pull)"><img src="https://i.ytimg.com/vi/DTxdCRIRx2I/mqdefault.jpg" alt="▶ Git : Récupérer les changements (git fetch, git pull)" width="320"></a>
>
> ▶ [Git : Récupérer les changements (git fetch, git pull)](https://www.youtube.com/watch?v=DTxdCRIRx2I)

- **Fetch** : Télécharge les commits sans les fusionner.
- **Pull** : Télécharge ET fusionne (Fetch + Merge).
```bash
git pull origin main
```

---

## 3. Workflow collaboratif complet
1. **Pull** les dernières modifs de `main`.
2. Créer une branche **Feature**.
3. Développer et **Commit**.
4. **Push** votre branche vers GitHub.
5. Ouvrir une **Pull Request (PR)** pour review.
6. Une fois validée, **Merge** dans `main`.

---

[← 04 - Branches](04-maitrise-branches.md) | [🏠 Accueil](README.md) | [06 - Commandes Avancées →](06-commandes-avancees-debogage.md)
