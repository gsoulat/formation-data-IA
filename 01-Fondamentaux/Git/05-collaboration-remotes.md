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
<!-- videos:zgstTcSVBxw -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=zgstTcSVBxw" title="Git 09 : Pousser vers un dépôt distant (git remote, git push)"><img src="https://i.ytimg.com/vi/zgstTcSVBxw/mqdefault.jpg" alt="▶ Git 09 : Pousser vers un dépôt distant (git remote, git push)" width="320"></a>
>
> ▶ [Git 09 : Pousser vers un dépôt distant (git remote, git push)](https://www.youtube.com/watch?v=zgstTcSVBxw)

```bash
git push origin main
git push -u origin feature/X   # -u lie la branche locale à la distante
```

### Récupérer (Fetch / Pull)
<!-- videos:W2SC4GhgLxI -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=W2SC4GhgLxI" title="Git 10 : Récupérer les changements (git fetch, git pull)"><img src="https://i.ytimg.com/vi/W2SC4GhgLxI/mqdefault.jpg" alt="▶ Git 10 : Récupérer les changements (git fetch, git pull)" width="320"></a>
>
> ▶ [Git 10 : Récupérer les changements (git fetch, git pull)](https://www.youtube.com/watch?v=W2SC4GhgLxI)

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
