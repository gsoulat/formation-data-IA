# 03 - Manipulation de Texte et Données

[← 02 - Navigation](02-navigation-fichiers.md) | [🏠 Accueil](../README.md) | [04 - Scripts et Automatisation →](04-scripts-automatisation.md)

---

## 1. Afficher le contenu

<!-- videos:92vQZCIsb7g -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=92vQZCIsb7g" title="Bash : Lire un fichier (cat, less, head)"><img src="https://i.ytimg.com/vi/92vQZCIsb7g/mqdefault.jpg" alt="▶ Bash : Lire un fichier (cat, less, head)" width="320"></a>
>
> ▶ [Bash : Lire un fichier (cat, less, head)](https://www.youtube.com/watch?v=92vQZCIsb7g)

- **`cat`** : Tout le fichier.
- **`head -n 20`** : Les 20 premières lignes.
- **`tail -f`** : Suivre les nouvelles lignes (logs).
- **`less`** : Navigation interactive (Espace/B pour défiler, Q pour quitter).

---

## 2. Redirections et Pipelines (Le coeur du Shell)

<!-- videos:9EKenVEXqDA,fRhh2XcTjvU,QildRV1TS9w -->
> 🎬 **En vidéo** (3 épisodes)
>
> <a href="https://www.youtube.com/watch?v=9EKenVEXqDA" title="Bash : Rediriger et enchaîner (|)"><img src="https://i.ytimg.com/vi/9EKenVEXqDA/mqdefault.jpg" alt="▶ Bash : Rediriger et enchaîner (|)" width="260"></a> <a href="https://www.youtube.com/watch?v=fRhh2XcTjvU" title="Bash : Trier et compter (sort, uniq, uniq -c)"><img src="https://i.ytimg.com/vi/fRhh2XcTjvU/mqdefault.jpg" alt="▶ Bash : Trier et compter (sort, uniq, uniq -c)" width="260"></a> <a href="https://www.youtube.com/watch?v=QildRV1TS9w" title="Bash : Découper des colonnes (cut, tr)"><img src="https://i.ytimg.com/vi/QildRV1TS9w/mqdefault.jpg" alt="▶ Bash : Découper des colonnes (cut, tr)" width="260"></a>
>
> ▶ [Bash : Rediriger et enchaîner (|)](https://www.youtube.com/watch?v=9EKenVEXqDA) · ▶ [Bash : Trier et compter (sort, uniq, uniq -c)](https://www.youtube.com/watch?v=fRhh2XcTjvU) · ▶ [Bash : Découper des colonnes (cut, tr)](https://www.youtube.com/watch?v=QildRV1TS9w)

- `>` : Écrase le fichier.
- `>>` : Ajoute à la fin du fichier.
- `|` : Envoie la sortie d'une commande vers l'entrée d'une autre.
- `2>` : Redirige uniquement les erreurs.

---

## 3. grep - Recherche de patterns

<!-- videos:bMzLZ7Bsz0s -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=bMzLZ7Bsz0s" title="Bash : Chercher (grep, grep -i -v -c, find)"><img src="https://i.ytimg.com/vi/bMzLZ7Bsz0s/mqdefault.jpg" alt="▶ Bash : Chercher (grep, grep -i -v -c, find)" width="320"></a>
>
> ▶ [Bash : Chercher (grep, grep -i -v -c, find)](https://www.youtube.com/watch?v=bMzLZ7Bsz0s)

| Option | Description |
| --- | --- |
| `-i` | Ignorer la casse |
| `-v` | Inverser (ne contient pas) |
| `-c` | Compter les occurrences |
| `-E` | Regex étendues |

Exemple : `grep -i "error" server.log`

---

## 4. sed - Transformation de texte

<!-- videos:15vjQ9hW_xo -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=15vjQ9hW_xo" title="Bash : Modifier du texte en série (sed, sed -i, awk)"><img src="https://i.ytimg.com/vi/15vjQ9hW_xo/mqdefault.jpg" alt="▶ Bash : Modifier du texte en série (sed, sed -i, awk)" width="320"></a>
>
> ▶ [Bash : Modifier du texte en série (sed, sed -i, awk)](https://www.youtube.com/watch?v=15vjQ9hW_xo)

```bash
# Remplacer "old" par "new" (globalement)
sed 's/old/new/g' file.txt

# Supprimer les lignes vides
sed '/^$/d' data.csv
```

---

## 5. awk - Traitement structuré (CSV/TSV)

`awk` traite les fichiers colonne par colonne.
```bash
# Afficher colonnes 1 et 3 d'un CSV
awk -F',' '{print $1, $3}' data.csv

# Faire une somme
awk -F',' '{sum += $4} END {print "Total:", sum}' sales.csv
```

---

## 6. Pipeline complet : Exemple d'analyse
```bash
cat access.log | awk '{print $1}' | sort | uniq -c | sort -rn | head -10
```
*(Récupère les 10 IPs les plus fréquentes dans un log Apache)*

---

[← 02 - Navigation](02-navigation-fichiers.md) | [🏠 Accueil](../README.md) | [04 - Scripts et Automatisation →](04-scripts-automatisation.md)
