# 02 - Installation et Configuration

[← 01 - Introduction](01-introduction-concepts.md) | [🏠 Accueil](README.md) | [03 - Premiers pas →](03-premiers-pas.md)

---

## 1. Installation de Git

<!-- videos:06v5AdOfRaY -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=06v5AdOfRaY" title="Git : Installer et configurer Git (git --version, git config)"><img src="https://i.ytimg.com/vi/06v5AdOfRaY/mqdefault.jpg" alt="▶ Git : Installer et configurer Git (git --version, git config)" width="320"></a>
>
> ▶ [Git : Installer et configurer Git (git --version, git config)](https://www.youtube.com/watch?v=06v5AdOfRaY)

### 🍎 macOS
```bash
# Avec Homebrew
brew install git
# Ou via Xcode
xcode-select --install
```

### 🐧 Linux (Debian/Ubuntu)
```bash
sudo apt-get update
sudo apt-get install git
```

### 🪟 Windows
Téléchargez Git depuis [git-scm.com](https://git-scm.com/download/win) ou installez [Git for Windows](https://gitforwindows.org/).

---

## 2. Configuration initiale (OBLIGATOIRE)

Avant votre premier commit, vous devez configurer votre identité :

```bash
# Identité (apparaîtra dans l'historique)
git config --global user.name "Votre Prénom Nom"
git config --global user.email "votre.email@example.com"

# Éditeur par défaut (ex: VS Code)
git config --global core.editor "code --wait"

# Branche par défaut
git config --global init.defaultBranch main
```

### Voir la configuration
```bash
git config --list
```

---

## 3. Les Alias : Gagner du temps
Créez des raccourcis pour les commandes fréquentes :

```bash
git config --global alias.st status
git config --global alias.co checkout
git config --global alias.br branch
git config --global alias.ci commit
git config --global alias.lg 'log --oneline --graph --all --decorate'
```

Usage : `git st` au lieu de `git status`.

---

[← 01 - Introduction](01-introduction-concepts.md) | [🏠 Accueil](README.md) | [03 - Premiers pas →](03-premiers-pas.md)
