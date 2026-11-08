# 02 - Navigation et Gestion de Fichiers

[← 01 - Introduction](01-introduction-shell.md) | [🏠 Accueil](../README.md) | [03 - Manipulation de Texte →](03-manipulation-texte.md)

---

## 1. Navigation dans le système de fichiers

<!-- videos:vIJzK6_95jQ,gmwMoMyOKO8 -->
> 🎬 **En vidéo** (2 épisodes)
>
> <a href="https://www.youtube.com/watch?v=vIJzK6_95jQ" title="Bash : Où suis-je ? (pwd, ls)"><img src="https://i.ytimg.com/vi/vIJzK6_95jQ/mqdefault.jpg" alt="▶ Bash : Où suis-je ? (pwd, ls)" width="260"></a> <a href="https://www.youtube.com/watch?v=gmwMoMyOKO8" title="Bash : Se déplacer (cd, ~, cd -)"><img src="https://i.ytimg.com/vi/gmwMoMyOKO8/mqdefault.jpg" alt="▶ Bash : Se déplacer (cd, ~, cd -)" width="260"></a>
>
> ▶ [Bash : Où suis-je ? (pwd, ls)](https://www.youtube.com/watch?v=vIJzK6_95jQ) · ▶ [Bash : Se déplacer (cd, ~, cd -)](https://www.youtube.com/watch?v=gmwMoMyOKO8)

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

<!-- videos:4wrVTJ8jUsk -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=4wrVTJ8jUsk" title="Bash : Les options et l'aide (ls -l, ls -a, . et ..)"><img src="https://i.ytimg.com/vi/4wrVTJ8jUsk/mqdefault.jpg" alt="▶ Bash : Les options et l'aide (ls -l, ls -a, . et ..)" width="320"></a>
>
> ▶ [Bash : Les options et l'aide (ls -l, ls -a, . et ..)](https://www.youtube.com/watch?v=4wrVTJ8jUsk)

| Option | Description |
| --- | --- |
| `ls -l` | Format long (détails) |
| `ls -a` | Afficher les fichiers cachés (commençant par .) |
| `ls -h` | Tailles lisibles (Human Readable) |
| `ls -lhS` | Trier par taille |
| `ls -lt` | Trier par date de modification |

---

## 3. Créer, Copier et Déplacer

<!-- videos:nFgqBNVfeRc -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=nFgqBNVfeRc" title="Bash : Créer et ranger (mkdir -p, touch, cp)"><img src="https://i.ytimg.com/vi/nFgqBNVfeRc/mqdefault.jpg" alt="▶ Bash : Créer et ranger (mkdir -p, touch, cp)" width="320"></a>
>
> ▶ [Bash : Créer et ranger (mkdir -p, touch, cp)](https://www.youtube.com/watch?v=nFgqBNVfeRc)

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
<!-- videos:J-3CZfjWwgs -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=J-3CZfjWwgs" title="Bash : Supprimer, et les jokers (rm, rm -r, *)"><img src="https://i.ytimg.com/vi/J-3CZfjWwgs/mqdefault.jpg" alt="▶ Bash : Supprimer, et les jokers (rm, rm -r, *)" width="320"></a>
>
> ▶ [Bash : Supprimer, et les jokers (rm, rm -r, *)](https://www.youtube.com/watch?v=J-3CZfjWwgs)

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

<!-- videos:JnZLSu84vY4 -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=JnZLSu84vY4" title="Bash : Les permissions (ls -l, chmod +x, ./)"><img src="https://i.ytimg.com/vi/JnZLSu84vY4/mqdefault.jpg" alt="▶ Bash : Les permissions (ls -l, chmod +x, ./)" width="320"></a>
>
> ▶ [Bash : Les permissions (ls -l, chmod +x, ./)](https://www.youtube.com/watch?v=JnZLSu84vY4)

```bash
-rw-r--r--  (r=4, w=2, x=1)
# 755 : rwxr-xr-x (Exécutable par tous)
# 600 : rw------- (Privé)

chmod +x script.sh  # Rendre exécutable
chown user:group file.csv  # Changer le propriétaire
```

---

[← 01 - Introduction](01-introduction-shell.md) | [🏠 Accueil](../README.md) | [03 - Manipulation de Texte →](03-manipulation-texte.md)
