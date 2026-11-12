# 04 - Scripts Shell et Automatisation

[← 03 - Texte](03-manipulation-texte.md) | [🏠 Accueil](../README.md) | [05 - Structures de Contrôle →](05-structures-controle.md)

---

## 1. Créer un script
<!-- videos:LQ7LA529KXY,AcJruOPFe_o,g8Ce48sX26E -->
> 🎬 **En vidéo** (3 épisodes)
>
> <a href="https://www.youtube.com/watch?v=LQ7LA529KXY" title="Bash 13 : Ton premier script (éditeur, shebang, bash script.sh)"><img src="https://i.ytimg.com/vi/LQ7LA529KXY/mqdefault.jpg" alt="▶ Bash 13 : Ton premier script (éditeur, shebang, bash script.sh)" width="260"></a> <a href="https://www.youtube.com/watch?v=AcJruOPFe_o" title="Éditer dans le terminal : nano et Vim 01 : nano : écrire et enregistrer"><img src="https://i.ytimg.com/vi/AcJruOPFe_o/mqdefault.jpg" alt="▶ Éditer dans le terminal : nano et Vim 01 : nano : écrire et enregistrer" width="260"></a> <a href="https://www.youtube.com/watch?v=g8Ce48sX26E" title="Éditer dans le terminal : nano et Vim 06 : Vim : insérer du texte (i)"><img src="https://i.ytimg.com/vi/g8Ce48sX26E/mqdefault.jpg" alt="▶ Éditer dans le terminal : nano et Vim 06 : Vim : insérer du texte (i)" width="260"></a>
>
> ▶ [Bash 13 : Ton premier script (éditeur, shebang, bash script.sh)](https://www.youtube.com/watch?v=LQ7LA529KXY) · ▶ [Éditer dans le terminal : nano et Vim 01 : nano : écrire et enregistrer](https://www.youtube.com/watch?v=AcJruOPFe_o) · ▶ [Éditer dans le terminal : nano et Vim 06 : Vim : insérer du texte (i)](https://www.youtube.com/watch?v=g8Ce48sX26E)

1. Fichier `.sh`.
2. **Shebang** en première ligne : `#!/usr/bin/env bash`.
3. Droits d'exécution : `chmod +x script.sh`.

---

## 2. Variables et Substitution

<!-- videos:Hx62PKD8up8 -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=Hx62PKD8up8" title="Bash 20 : Une commande dans une commande ($(...), xargs)"><img src="https://i.ytimg.com/vi/Hx62PKD8up8/mqdefault.jpg" alt="▶ Bash 20 : Une commande dans une commande ($(...), xargs)" width="320"></a>
>
> ▶ [Bash 20 : Une commande dans une commande ($(...), xargs)](https://www.youtube.com/watch?v=Hx62PKD8up8)

```bash
NAME="Alice"
echo "Hello, ${NAME}"

# Capturer le résultat d'une commande
DATE=$(date +%Y-%m-%d)
```

---

## 3. Paramètres et Arguments
<!-- videos:7zCEJ4hVGQo -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=7zCEJ4hVGQo" title="Bash 14 : Variables et arguments (variable, $1, guillemets)"><img src="https://i.ytimg.com/vi/7zCEJ4hVGQo/mqdefault.jpg" alt="▶ Bash 14 : Variables et arguments (variable, $1, guillemets)" width="320"></a>
>
> ▶ [Bash 14 : Variables et arguments (variable, $1, guillemets)](https://www.youtube.com/watch?v=7zCEJ4hVGQo)

- `$0` : Nom du script.
- `$1, $2...` : Premier, deuxième argument.
- `$#` : Nombre total d'arguments.
- `$@` : Tous les arguments.

---

## 4. Mode Strict (set -euo pipefail)
<!-- videos:x1Z331qZD9g -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=x1Z331qZD9g" title="Bash 25 : Un script solide (fonctions, case, while read)"><img src="https://i.ytimg.com/vi/x1Z331qZD9g/mqdefault.jpg" alt="▶ Bash 25 : Un script solide (fonctions, case, while read)" width="320"></a>
>
> ▶ [Bash 25 : Un script solide (fonctions, case, while read)](https://www.youtube.com/watch?v=x1Z331qZD9g)

⚠️ **INDISPENSABLE en production :**
- `set -e` : Arrête le script si une commande échoue.
- `set -u` : Erreur si une variable n'est pas définie.
- `set -o pipefail` : Échoue si un élément d'un pipeline échoue.

---

## 5. Gestion d'erreurs et Debugging
<!-- videos:ZgLmogQ6abE -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=ZgLmogQ6abE" title="Bash 19 : Les erreurs aussi se redirigent (2, 2&1, /dev/null)"><img src="https://i.ytimg.com/vi/ZgLmogQ6abE/mqdefault.jpg" alt="▶ Bash 19 : Les erreurs aussi se redirigent (2, 2&1, /dev/null)" width="320"></a>
>
> ▶ [Bash 19 : Les erreurs aussi se redirigent (2, 2&1, /dev/null)](https://www.youtube.com/watch?v=ZgLmogQ6abE)

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
