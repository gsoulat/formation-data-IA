# 02 - Navigation et Gestion de Fichiers

[← 01 - Introduction](01-introduction-shell.md) | [🏠 Accueil](../README.md) | [03 - Manipulation de Texte →](03-manipulation-texte.md)

---

## 1. Navigation dans le système de fichiers

<!-- videos:Ep6gfhfnQFg,5kIWmTg-yxY -->
> 🎬 **En vidéo** (2 épisodes)
>
> <a href="https://www.youtube.com/watch?v=Ep6gfhfnQFg" title="Bash 02 : Où suis-je ? (pwd, ls)"><img src="https://i.ytimg.com/vi/Ep6gfhfnQFg/mqdefault.jpg" alt="▶ Bash 02 : Où suis-je ? (pwd, ls)" width="260"></a> <a href="https://www.youtube.com/watch?v=5kIWmTg-yxY" title="Bash 04 : Se déplacer (cd, ~, cd -)"><img src="https://i.ytimg.com/vi/5kIWmTg-yxY/mqdefault.jpg" alt="▶ Bash 04 : Se déplacer (cd, ~, cd -)" width="260"></a>
>
> ▶ [Bash 02 : Où suis-je ? (pwd, ls)](https://www.youtube.com/watch?v=Ep6gfhfnQFg) · ▶ [Bash 04 : Se déplacer (cd, ~, cd -)](https://www.youtube.com/watch?v=5kIWmTg-yxY)

### Structure des répertoires Linux/Unix
```bash
/                    (root - racine du système)
├── bin/            (binaires essentiels)
├── home/           (répertoires utilisateurs)
├── tmp/            (fichiers temporaires)
├── var/            (données variables: logs, caches)
└── data/           (souvent utilisé pour les données)
```

### Commandes de navigation
| Commande | Description | Exemple |
| --- | --- | --- |
| `pwd` | Print Working Directory | `pwd` |
| `cd` | Change Directory | `cd /home/data` |
| `cd ~` | Retour au Home | `cd ~` |
| `cd -` | Retour au répertoire précédent | `cd -` |
| `cd ..` | Remonter d'un niveau | `cd ..` |

---

## 2. Lister les fichiers avec `ls`

<!-- videos:gJSjNyLxQz8 -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=gJSjNyLxQz8" title="Bash 03 : Les options et l'aide (ls -l, ls -a, . et ..)"><img src="https://i.ytimg.com/vi/gJSjNyLxQz8/mqdefault.jpg" alt="▶ Bash 03 : Les options et l'aide (ls -l, ls -a, . et ..)" width="320"></a>
>
> ▶ [Bash 03 : Les options et l'aide (ls -l, ls -a, . et ..)](https://www.youtube.com/watch?v=gJSjNyLxQz8)

| Option | Description |
| --- | --- |
| `ls -l` | Format long (détails) |
| `ls -a` | Afficher les fichiers cachés (commençant par .) |
| `ls -h` | Tailles lisibles (Human Readable) |
| `ls -lhS` | Trier par taille |
| `ls -lt` | Trier par date de modification |

---

## 3. Créer, Copier et Déplacer

<!-- videos:C4ri36btZBI -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=C4ri36btZBI" title="Bash 05 : Créer et ranger (mkdir -p, touch, cp)"><img src="https://i.ytimg.com/vi/C4ri36btZBI/mqdefault.jpg" alt="▶ Bash 05 : Créer et ranger (mkdir -p, touch, cp)" width="320"></a>
>
> ▶ [Bash 05 : Créer et ranger (mkdir -p, touch, cp)](https://www.youtube.com/watch?v=C4ri36btZBI)

```bash
# Créer un dossier (et ses parents)
mkdir -p data/raw/2024

# Créer un fichier vide
touch script.py

# Copier un dossier entier (récursif)
cp -r data/ backup_data/

# Déplacer ou renommer
mv old_name.csv new_name.csv
```

---

## 4. Suppression (⚠️ Prudence)
<!-- videos:9ePhYilio30 -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=9ePhYilio30" title="Bash 06 : Supprimer, et les jokers (rm, rm -r, *)"><img src="https://i.ytimg.com/vi/9ePhYilio30/mqdefault.jpg" alt="▶ Bash 06 : Supprimer, et les jokers (rm, rm -r, *)" width="320"></a>
>
> ▶ [Bash 06 : Supprimer, et les jokers (rm, rm -r, *)](https://www.youtube.com/watch?v=9ePhYilio30)

La suppression est définitive !
```bash
# Supprimer un fichier
rm data.csv

# Supprimer un dossier et tout son contenu
rm -rf folder/
```

---

## 5. Recherche de fichiers

- **`find`** : Puissant, recherche en temps réel.
  ```bash
  find . -name "*.csv" -size +100M
  ```
- **`locate`** : Ultra-rapide, basé sur une base de données.
  ```bash
  locate config.json
  ```

---

## 6. Permissions et Droits

<!-- videos:O--A2VjWwJc -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=O--A2VjWwJc" title="Bash 12 : Les permissions (ls -l, chmod +x, ./)"><img src="https://i.ytimg.com/vi/O--A2VjWwJc/mqdefault.jpg" alt="▶ Bash 12 : Les permissions (ls -l, chmod +x, ./)" width="320"></a>
>
> ▶ [Bash 12 : Les permissions (ls -l, chmod +x, ./)](https://www.youtube.com/watch?v=O--A2VjWwJc)

```bash
-rw-r--r--  (r=4, w=2, x=1)
# 755 : rwxr-xr-x (Exécutable par tous)
# 600 : rw------- (Privé)

chmod +x script.sh  # Rendre exécutable
chown user:group file.csv  # Changer le propriétaire
```

---

[← 01 - Introduction](01-introduction-shell.md) | [🏠 Accueil](../README.md) | [03 - Manipulation de Texte →](03-manipulation-texte.md)
