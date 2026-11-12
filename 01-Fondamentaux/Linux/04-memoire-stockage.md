# 04 - Mémoire et Stockage

[← 03 - Processus](03-gestion-processus.md) | [🏠 Accueil](README.md) | [05 - Réseau sous Linux →](05-reseau-linux.md)

---

## 1. Gestion de la RAM et du Swap

Linux utilise la mémoire vive (RAM) de manière très agressive pour le cache disque. Un serveur Linux qui affiche "0 MB free" n'est pas forcément saturé, il utilise juste le reste pour accélérer les accès fichiers.

### Commandes :
- `free -h` : Affiche l'utilisation de la RAM et du Swap.
- `vmstat` : Statistiques sur la mémoire virtuelle.

### Le Swap :
C'est un espace sur le disque utilisé quand la RAM est pleine. 
*💡 Conseil Data Eng : Évitez le swap excessif, car les performances s'effondrent.*

---

## 2. Stockage Physique vs Logique

### Partitionnement
Découpage physique du disque (`/dev/sda1`, `/dev/sda2`).

### LVM (Logical Volume Manager)
Couche d'abstraction (recommandée) qui permet de :
- Fusionner plusieurs disques physiques en un seul groupe.
- Redimensionner des partitions "à chaud" sans redémarrer.
- Faire des Snapshots.

---

## 3. Montage des systèmes de fichiers

Sous Linux, pour accéder à un disque, il faut le "monter" dans un dossier.
```bash
mount /dev/sdb1 /mnt/data
```

### Le fichier /etc/fstab
C'est ici qu'on définit quels disques doivent être montés automatiquement au démarrage. Une erreur dans ce fichier peut empêcher le serveur de booter !

---

## 4. Inodes et espace disque

<!-- videos:3U0CCfr2b8Y -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=3U0CCfr2b8Y" title="Bash 22 : Installer et faire de la place (sudo, apt install, brew)"><img src="https://i.ytimg.com/vi/3U0CCfr2b8Y/mqdefault.jpg" alt="▶ Bash 22 : Installer et faire de la place (sudo, apt install, brew)" width="320"></a>
>
> ▶ [Bash 22 : Installer et faire de la place (sudo, apt install, brew)](https://www.youtube.com/watch?v=3U0CCfr2b8Y)

Chaque fichier consomme :
1. De l'espace disque (les octets).
2. Un **Inode** (l'index du fichier).

Si vous créez des millions de petits fichiers (ex: logs Spark non agrégés), vous pouvez saturer les Inodes avant de saturer le disque.
```bash
df -h # Espace disque
df -i # Inodes libres
```

---

[← 03 - Processus](03-gestion-processus.md) | [🏠 Accueil](README.md) | [05 - Réseau sous Linux →](05-reseau-linux.md)
