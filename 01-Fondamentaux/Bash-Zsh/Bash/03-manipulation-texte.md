# 03 - Manipulation de Texte et Données

[← 02 - Navigation](02-navigation-fichiers.md) | [🏠 Accueil](../README.md) | [04 - Scripts et Automatisation →](04-scripts-automatisation.md)

---

## 1. Afficher le contenu

<!-- videos:3s1FTeRD4Dg -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=3s1FTeRD4Dg" title="Bash 07 : Lire un fichier (cat, less, head)"><img src="https://i.ytimg.com/vi/3s1FTeRD4Dg/mqdefault.jpg" alt="▶ Bash 07 : Lire un fichier (cat, less, head)" width="320"></a>
>
> ▶ [Bash 07 : Lire un fichier (cat, less, head)](https://www.youtube.com/watch?v=3s1FTeRD4Dg)

- **`cat`** : Tout le fichier.
- **`head -n 20`** : Les 20 premières lignes.
- **`tail -f`** : Suivre les nouvelles lignes (logs).
- **`less`** : Navigation interactive (Espace/B pour défiler, Q pour quitter).

---

## 2. Redirections et Pipelines (Le coeur du Shell)

<!-- videos:G_spMI9-5jI,JHU9102Wf5Q,FHZ3eiAHCXc -->
> 🎬 **En vidéo** (3 épisodes)
>
> <a href="https://www.youtube.com/watch?v=G_spMI9-5jI" title="Bash 09 : Rediriger et enchaîner (|)"><img src="https://i.ytimg.com/vi/G_spMI9-5jI/mqdefault.jpg" alt="▶ Bash 09 : Rediriger et enchaîner (|)" width="260"></a> <a href="https://www.youtube.com/watch?v=JHU9102Wf5Q" title="Bash 10 : Trier et compter (sort, uniq, uniq -c)"><img src="https://i.ytimg.com/vi/JHU9102Wf5Q/mqdefault.jpg" alt="▶ Bash 10 : Trier et compter (sort, uniq, uniq -c)" width="260"></a> <a href="https://www.youtube.com/watch?v=FHZ3eiAHCXc" title="Bash 11 : Découper des colonnes (cut, tr)"><img src="https://i.ytimg.com/vi/FHZ3eiAHCXc/mqdefault.jpg" alt="▶ Bash 11 : Découper des colonnes (cut, tr)" width="260"></a>
>
> ▶ [Bash 09 : Rediriger et enchaîner (|)](https://www.youtube.com/watch?v=G_spMI9-5jI) · ▶ [Bash 10 : Trier et compter (sort, uniq, uniq -c)](https://www.youtube.com/watch?v=JHU9102Wf5Q) · ▶ [Bash 11 : Découper des colonnes (cut, tr)](https://www.youtube.com/watch?v=FHZ3eiAHCXc)

- `>` : Écrase le fichier.
- `>>` : Ajoute à la fin du fichier.
- `|` : Envoie la sortie d'une commande vers l'entrée d'une autre.
- `2>` : Redirige uniquement les erreurs.

---

## 3. grep - Recherche de patterns

<!-- videos:jVJ4J2vDYUI -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=jVJ4J2vDYUI" title="Bash 08 : Chercher (grep, grep -i -v -c, find)"><img src="https://i.ytimg.com/vi/jVJ4J2vDYUI/mqdefault.jpg" alt="▶ Bash 08 : Chercher (grep, grep -i -v -c, find)" width="320"></a>
>
> ▶ [Bash 08 : Chercher (grep, grep -i -v -c, find)](https://www.youtube.com/watch?v=jVJ4J2vDYUI)

| Option | Description |
| --- | --- |
| `-i` | Ignorer la casse |
| `-v` | Inverser (ne contient pas) |
| `-c` | Compter les occurrences |
| `-E` | Regex étendues |

Exemple : `grep -i "error" server.log`

---

## 4. sed - Transformation de texte

<!-- videos:S7U2zumq6XU -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=S7U2zumq6XU" title="Bash 24 : Modifier du texte en série (sed, sed -i, awk)"><img src="https://i.ytimg.com/vi/S7U2zumq6XU/mqdefault.jpg" alt="▶ Bash 24 : Modifier du texte en série (sed, sed -i, awk)" width="320"></a>
>
> ▶ [Bash 24 : Modifier du texte en série (sed, sed -i, awk)](https://www.youtube.com/watch?v=S7U2zumq6XU)

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
