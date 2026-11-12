# 05 - Structures de Contrôle

[← 04 - Scripts](04-scripts-automatisation.md) | [🏠 Accueil](../README.md) | [06 - Fonctions et Avancé →](06-fonctions-avance.md)

---

## 1. Conditions (if / elif / else)

<!-- videos:GAKfQRTfZ-g -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=GAKfQRTfZ-g" title="Bash 15 : Les conditions (if, [ -f ], $?)"><img src="https://i.ytimg.com/vi/GAKfQRTfZ-g/mqdefault.jpg" alt="▶ Bash 15 : Les conditions (if, [ -f ], $?)" width="320"></a>
>
> ▶ [Bash 15 : Les conditions (if, [ -f ], $?)](https://www.youtube.com/watch?v=GAKfQRTfZ-g)

Préférer la syntaxe `[[ ]]` (Bash/Zsh) à `[ ]` (POSIX).

```bash
if [[ $VAR == "test" ]]; then
    echo "Match"
elif [[ $VAR -gt 10 ]]; then
    echo "Supérieur à 10"
else
    echo "Autre"
fi
```

### Tests fréquents :
- `-f file` : Le fichier existe.
- `-d dir` : Le dossier existe.
- `-z str` : La chaîne est vide.

---

## 2. Boucles (for)

<!-- videos:PQJGla-laEs -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=PQJGla-laEs" title="Bash 16 : Les boucles (for)"><img src="https://i.ytimg.com/vi/PQJGla-laEs/mqdefault.jpg" alt="▶ Bash 16 : Les boucles (for)" width="320"></a>
>
> ▶ [Bash 16 : Les boucles (for)](https://www.youtube.com/watch?v=PQJGla-laEs)

```bash
# Sur une liste de fichiers
for file in data/*.csv; do
    echo "Traitement de $file"
done

# Sur une séquence
for i in {1..5}; do
    echo "Numéro $i"
done
```

---

## 3. Boucles (while / until)

```bash
# Lire un fichier ligne par ligne
while IFS= read -r line; do
    echo "Ligne : $line"
done < input.txt

# Attendre qu'un service soit prêt
until curl -s http://localhost:8080 > /dev/null; do
    sleep 5
done
```

---

## 4. Case statements (Switch)

```bash
case $filename in
    *.csv) echo "Type CSV" ;;
    *.json) echo "Type JSON" ;;
    *) echo "Inconnu" ;;
esac
```

---

[← 04 - Scripts](04-scripts-automatisation.md) | [🏠 Accueil](../README.md) | [06 - Fonctions et Avancé →](06-fonctions-avance.md)
