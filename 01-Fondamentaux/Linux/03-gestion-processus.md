# 03 - Gestion des Processus

[← 02 - Filesystem](02-filesystem-hierarchie.md) | [🏠 Accueil](README.md) | [04 - Mémoire et Stockage →](04-memoire-stockage.md)

---

## 1. Qu'est-ce qu'un processus ?

Un processus est une instance d'un programme en cours d'exécution. Chaque processus possède un identifiant unique appelé **PID** (Process ID).

### Les états d'un processus :
- **Running (R)** : En cours d'utilisation du CPU.
- **Sleeping (S)** : En attente d'une ressource (disque, réseau).
- **Stopped (T)** : Mis en pause par l'utilisateur.
- **Zombie (Z)** : Terminé mais attend que son parent lise son code de sortie.

---

## 2. Observer les processus

<!-- videos:Ue8XzVwWt9Q -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=Ue8XzVwWt9Q" title="Bash 18 : Surveiller ce qui tourne (ps, top, kill)"><img src="https://i.ytimg.com/vi/Ue8XzVwWt9Q/mqdefault.jpg" alt="▶ Bash 18 : Surveiller ce qui tourne (ps, top, kill)" width="320"></a>
>
> ▶ [Bash 18 : Surveiller ce qui tourne (ps, top, kill)](https://www.youtube.com/watch?v=Ue8XzVwWt9Q)

| Commande | Usage |
| --- | --- |
| `ps aux` | Liste statique de tous les processus. |
| `top` | Tableau de bord dynamique (CPU, RAM). |
| `htop` | Version moderne et colorée de top (recommandé). |
| `pstree` | Affiche la hiérarchie parent/enfant. |

---

## 3. Envoyer des signaux

On communique avec les processus via des signaux.
```bash
kill -SIGNAL PID
```

### Signaux principaux :
- **SIGTERM (15)** : Demande polie de s'arrêter (par défaut). Laisse le temps au programme de sauvegarder.
- **SIGKILL (9)** : Arrêt brutal et immédiat par le Kernel.
- **SIGHUP (1)** : Relance la configuration (souvent pour les serveurs).

---

## 4. Priorité et "Niceness"

Le Kernel décide quel processus passe sur le CPU. On peut influencer cela avec le **Nice** (de -20 à 19).
- Un processus avec un Nice de 19 est très "gentil" : il laisse passer les autres.
- Un processus avec un Nice de -20 est prioritaire.

```bash
nice -n 10 python my_heavy_job.py
renice -n 5 -p 1234
```

---

[← 02 - Filesystem](02-filesystem-hierarchie.md) | [🏠 Accueil](README.md) | [04 - Mémoire et Stockage →](04-memoire-stockage.md)
