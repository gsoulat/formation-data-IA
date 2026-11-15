# 01 - Introduction au Shell (Bash/Zsh)

[🏠 Accueil](../README.md) | [02 - Navigation et Fichiers →](02-navigation-fichiers.md)

---

## 1. Qu'est-ce que le Shell ?

<!-- videos:b3VIbr5cFlo -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=b3VIbr5cFlo" title="Bash 00 : Installer ton terminal (Linux, Windows (WSL))"><img src="https://i.ytimg.com/vi/b3VIbr5cFlo/mqdefault.jpg" alt="▶ Bash 00 : Installer ton terminal (Linux, Windows (WSL))" width="320"></a>
>
> ▶ [Bash 00 : Installer ton terminal (Linux, Windows (WSL))](https://www.youtube.com/watch?v=b3VIbr5cFlo)

Le **shell** est un interpréteur de commandes qui permet d'interagir avec le système
d'exploitation via des commandes textuelles. C'est l'interface entre l'utilisateur et le noyau
(kernel) du système.

#### Shell vs Terminal

**Terminal** : L'application graphique qui affiche le shell (iTerm, GNOME
Terminal, Windows Terminal...)
**Shell** : Le programme qui interprète vos commandes (Bash, Zsh, Fish...)

### Les principaux shells

| Shell | Avantages | Utilisation |
| --- | --- | --- |
| **Bash** (Bourne Again Shell) | Universel, compatible partout, documentation abondante | Shell par défaut sur Linux et macOS (avant Catalina) |
| **Zsh** (Z Shell) | Autocomplétion puissante, plugins, thèmes, historique partagé | Shell par défaut sur macOS depuis Catalina |
| **Fish** | Syntaxe moderne, autocomplétion intelligente | Alternative moderne mais syntaxe différente |
| **sh** (Bourne Shell) | Minimaliste, scripts portables | Scripts système, compatibilité maximale |

---

## 2. Pourquoi le Shell en Data Engineering ?

### 💡 Cas d'usage essentiels

- **Traitement de fichiers volumineux** : Filtrer des fichiers de logs de plusieurs Go avec grep/awk.
- **Automatisation de pipelines** : Créer des scripts ETL légers et rapides.
- **Manipulation de données** : Nettoyer des CSV, extraire des colonnes, calculer des agrégations.
- **Surveillance système** : Monitorer l'utilisation CPU/mémoire des processus de données.
- **Déploiement** : Automatiser le déploiement de pipelines avec des scripts shell.

### Exemple concret en Data Engineering

Imaginez que vous devez analyser des logs de serveur pour identifier les erreurs :

```bash
# Extraire toutes les erreurs, compter par type, et trier
grep "ERROR" server.log | \
  awk '{print $5}' | \
  sort | \
  uniq -c | \
  sort -rn | \
  head -10
```

---

## 3. Vérifier et changer son shell

```bash
# Afficher le shell actuel
echo $SHELL

# Afficher la version
bash --version

# Lister tous les shells disponibles
cat /etc/shells
```

---

## 4. Premières commandes essentielles

<!-- videos:TUcts03vOrE -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=TUcts03vOrE" title="Bash 01 : Découvrir le terminal (prompt, echo, whoami)"><img src="https://i.ytimg.com/vi/TUcts03vOrE/mqdefault.jpg" alt="▶ Bash 01 : Découvrir le terminal (prompt, echo, whoami)" width="320"></a>
>
> ▶ [Bash 01 : Découvrir le terminal (prompt, echo, whoami)](https://www.youtube.com/watch?v=TUcts03vOrE)

| Commande | Description | Exemple |
| --- | --- | --- |
| `pwd` | Afficher le répertoire courant | `pwd` |
| `whoami` | Afficher le nom d'utilisateur | `whoami` |
| `date` | Afficher la date et l'heure | `date` |
| `echo` | Afficher du texte | `echo "Hello Data"` |
| `clear` | Effacer l'écran | `Ctrl+L` |
| `history` | Afficher l'historique | `history` |

### Raccourcis clavier à connaître
- `Ctrl + C` : Interrompre la commande en cours.
- `Ctrl + R` : Rechercher dans l'historique (INDISPENSABLE).
- `Tab` : Autocomplétion automatique.

---

[🏠 Accueil](../README.md) | [02 - Navigation et Fichiers →](02-navigation-fichiers.md)
