# 07 - Bonnes Pratiques et Optimisation

[← 06 - Avancé](06-fonctions-avance.md) | [🏠 Accueil](../README.md)

---

## 1. Alias personnalisés (Productivité)

<!-- videos:76Fx5BlrbV4 -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=76Fx5BlrbV4" title="Bash 17 : Personnaliser ton terminal (PATH, export, alias)"><img src="https://i.ytimg.com/vi/76Fx5BlrbV4/mqdefault.jpg" alt="▶ Bash 17 : Personnaliser ton terminal (PATH, export, alias)" width="320"></a>
>
> ▶ [Bash 17 : Personnaliser ton terminal (PATH, export, alias)](https://www.youtube.com/watch?v=76Fx5BlrbV4)

Ajoutez-les dans votre `.bashrc` ou `.zshrc` :
```bash
alias ll='ls -lah'
alias gs='git status'
alias csvhead='head -n 20 | column -t -s,'
```

---

## 2. Configuration .bashrc / .zshrc

C'est ici que vous définissez votre environnement (Path, Variables, Alias).
```bash
export PATH="$HOME/bin:$PATH"
export EDITOR='vim'
```

---

## 3. ShellCheck (Linter)

Utilisez **ShellCheck** pour valider vos scripts. Il détecte :
- Variables non quotées (`$VAR` -> `"$VAR"`).
- Boucles sur `ls` (mauvaise pratique).
- Erreurs de syntaxe communes.

---

## 4. Checklist pour un script en Production

- ✓ `#!/usr/bin/env bash` en shebang.
- ✓ `set -euo pipefail` activé.
- ✓ Validation des arguments d'entrée.
- ✓ Gestion des logs et erreurs.
- ✓ Nettoyage automatique des fichiers temporaires via `trap`.
- ✓ Code commenté (Expliquer le *Pourquoi*, pas le *Quoi*).

---

[← 06 - Avancé](06-fonctions-avance.md) | [🏠 Accueil](../README.md)
