# 04 - Scripts Shell et Automatisation

[← 03 - Texte](03-manipulation-texte.md) | [🏠 Accueil](../README.md) | [05 - Structures de Contrôle →](05-structures-controle.md)

---

## 1. Créer un script
<!-- videos:NT5jWC8Svec,Nk8Dk4ljpFs,FZrnsLno7IA -->
> 🎬 **En vidéo** (3 épisodes)
>
> <a href="https://www.youtube.com/watch?v=NT5jWC8Svec" title="Bash : Ton premier script (éditeur, shebang, bash script.sh)"><img src="https://i.ytimg.com/vi/NT5jWC8Svec/mqdefault.jpg" alt="▶ Bash : Ton premier script (éditeur, shebang, bash script.sh)" width="260"></a> <a href="https://www.youtube.com/watch?v=Nk8Dk4ljpFs" title="Éditer dans le terminal : nano et Vim : nano : écrire et enregistrer"><img src="https://i.ytimg.com/vi/Nk8Dk4ljpFs/mqdefault.jpg" alt="▶ Éditer dans le terminal : nano et Vim : nano : écrire et enregistrer" width="260"></a> <a href="https://www.youtube.com/watch?v=FZrnsLno7IA" title="Éditer dans le terminal : nano et Vim : Vim : insérer du texte (i, a)"><img src="https://i.ytimg.com/vi/FZrnsLno7IA/mqdefault.jpg" alt="▶ Éditer dans le terminal : nano et Vim : Vim : insérer du texte (i, a)" width="260"></a>
>
> ▶ [Bash : Ton premier script (éditeur, shebang, bash script.sh)](https://www.youtube.com/watch?v=NT5jWC8Svec) · ▶ [Éditer dans le terminal : nano et Vim : nano : écrire et enregistrer](https://www.youtube.com/watch?v=Nk8Dk4ljpFs) · ▶ [Éditer dans le terminal : nano et Vim : Vim : insérer du texte (i, a)](https://www.youtube.com/watch?v=FZrnsLno7IA)

1. Fichier `.sh`.
2. **Shebang** en première ligne : `#!/usr/bin/env bash`.
3. Droits d'exécution : `chmod +x script.sh`.

---

## 2. Variables et Substitution

```bash
NAME="Alice"
echo "Hello, ${NAME}"

# Capturer le résultat d'une commande
DATE=$(date +%Y-%m-%d)
```

---

## 3. Paramètres et Arguments
- `$0` : Nom du script.
- `$1, $2...` : Premier, deuxième argument.
- `$#` : Nombre total d'arguments.
- `$@` : Tous les arguments.

---

## 4. Mode Strict (set -euo pipefail)
⚠️ **INDISPENSABLE en production :**
- `set -e` : Arrête le script si une commande échoue.
- `set -u` : Erreur si une variable n'est pas définie.
- `set -o pipefail` : Échoue si un élément d'un pipeline échoue.

---

## 5. Gestion d'erreurs et Debugging
- `exit 0` : Succès.
- `exit 1` : Erreur.
- `bash -x script.sh` : Trace complète de l'exécution (debug).

---

## 6. Lecture utilisateur
```bash
read -p "Entrez le nom de la table : " table_name
```

---

[← 03 - Texte](03-manipulation-texte.md) | [🏠 Accueil](../README.md) | [05 - Structures de Contrôle →](05-structures-controle.md)
