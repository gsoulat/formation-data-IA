#!/usr/bin/env python3
"""Insère les vidéos YouTube du Studio Formation dans les cours et les briefs Markdown.

Chaque section listée dans PLAN reçoit, sous son titre, un bloc « 🎬 En vidéo » :
miniature cliquable (GitHub retire les <iframe>, d'où <a><img></a>) + titre en lien.

- Les identifiants viennent des etat.json du studio ($FORMATION_VIDEOS,
  par défaut ~/Movies/Formation-Videos/<module>/<épisode>/etat.json).
- Une vidéo n'est insérée que si YouTube la sert publiquement (oEmbed) :
  les vidéos privées ou pas encore envoyées sont ignorées, sans erreur.
- Relançable à volonté : le bloc d'une section est régénéré à chaque passage
  (marqueur <!-- videos:... -->), jamais dupliqué ; s'il n'y a plus de vidéo
  disponible pour une section, le bloc est retiré.

Usage (depuis la racine du dépôt) :
    python3 scripts/inserer_videos.py            # applique
    python3 scripts/inserer_videos.py --dry-run  # montre ce qui changerait
"""
from __future__ import annotations

import argparse
import json
import os
import sys
import urllib.parse
import urllib.request
from pathlib import Path

RACINE = Path(__file__).resolve().parent.parent  # racine du dépôt
STUDIO = Path(os.environ.get("FORMATION_VIDEOS", Path.home() / "Movies" / "Formation-Videos"))

# (fichier relatif à la racine du dépôt, titre de section exact, [épisodes du studio])
# Un épisode pas encore en ligne peut figurer ici : il apparaîtra au prochain passage.
PLAN: list[tuple[str, str, list[str]]] = [
    # --- Bash ---
    ("01-Fondamentaux/Bash-Zsh/Bash/01-introduction-shell.md", "## 1. Qu'est-ce que le Shell ?", ["bash/00-installer-ton-terminal"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/01-introduction-shell.md", "## 4. Premières commandes essentielles", ["bash/01-le-terminal"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/02-navigation-fichiers.md", "## 1. Navigation dans le système de fichiers", ["bash/02-ou-suis-je", "bash/04-se-deplacer"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/02-navigation-fichiers.md", "## 2. Lister les fichiers avec `ls`", ["bash/03-options-et-aide"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/02-navigation-fichiers.md", "## 3. Créer, Copier et Déplacer", ["bash/05-creer-et-ranger"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/02-navigation-fichiers.md", "## 4. Suppression (⚠️ Prudence)", ["bash/06-supprimer-et-jokers"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/02-navigation-fichiers.md", "## 6. Permissions et Droits", ["bash/12-permissions"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/03-manipulation-texte.md", "## 1. Afficher le contenu", ["bash/07-lire-un-fichier"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/03-manipulation-texte.md", "## 2. Redirections et Pipelines (Le coeur du Shell)", ["bash/09-rediriger", "bash/10-trier-et-compter", "bash/11-decouper"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/03-manipulation-texte.md", "## 3. grep - Recherche de patterns", ["bash/08-chercher"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/03-manipulation-texte.md", "## 4. sed - Transformation de texte", ["bash/24-sed-et-awk"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/04-scripts-automatisation.md", "## 1. Créer un script", ["bash/13-premier-script", "editeurs/01-nano-ecrire", "editeurs/06-vim-inserer"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/04-scripts-automatisation.md", "## 2. Variables et Substitution", ["bash/20-substitution"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/04-scripts-automatisation.md", "## 3. Paramètres et Arguments", ["bash/14-variables-et-arguments"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/04-scripts-automatisation.md", "## 4. Mode Strict (set -euo pipefail)", ["bash/25-script-solide"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/04-scripts-automatisation.md", "## 5. Gestion d'erreurs et Debugging", ["bash/19-rediriger-les-erreurs"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/05-structures-controle.md", "## 1. Conditions (if / elif / else)", ["bash/15-conditions"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/05-structures-controle.md", "## 2. Boucles (for)", ["bash/16-boucles"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/07-bonnes-pratiques.md", "## 1. Alias personnalisés (Productivité)", ["bash/17-personnaliser"]),
    ("01-Fondamentaux/Linux/03-gestion-processus.md", "## 2. Observer les processus", ["bash/18-processus"]),
    ("01-Fondamentaux/Linux/04-memoire-stockage.md", "## 4. Inodes et espace disque", ["bash/22-installer-et-faire-de-la-place"]),
    # --- Git / GitHub ---
    ("01-Fondamentaux/Git/01-introduction-concepts.md", "## 1. Qu'est-ce que Git ?", ["git/00-pourquoi-versionner"]),
    ("01-Fondamentaux/Git/02-installation-configuration.md", "## 1. Installation de Git", ["git/01-configurer-git"]),
    ("01-Fondamentaux/Git/03-premiers-pas.md", "## 1. Initialiser ou Cloner un dépôt", ["git/02-premier-depot"]),
    ("01-Fondamentaux/Git/03-premiers-pas.md", "## 3. Consulter l'historique", ["git/04-lire-l-historique"]),
    ("01-Fondamentaux/Git/04-maitrise-branches.md", "## 2. Gérer les branches", ["git/07-branches"]),
    ("01-Fondamentaux/Git/04-maitrise-branches.md", "## 4. Résoudre les conflits", ["git/08-resoudre-un-conflit"]),
    ("01-Fondamentaux/Git/05-collaboration-remotes.md", "### Envoyer (Push)", ["git/09-pousser"]),
    ("01-Fondamentaux/Git/05-collaboration-remotes.md", "### Récupérer (Fetch / Pull)", ["git/10-recuperer"]),
    ("01-Fondamentaux/Git/06-commandes-avancees-debogage.md", "## 1. Annuler des modifications", ["git/05-annuler"]),
    ("01-Fondamentaux/Git/06-commandes-avancees-debogage.md", "## 2. Stash : Mettre de côté", ["git/11-mettre-de-cote"]),
    ("01-Fondamentaux/Git/07-meilleures-pratiques-data.md", "## 1. Le .gitignore : Vital pour la Data", ["git/06-ignorer-des-fichiers"]),
    ("01-Fondamentaux/Git/07-meilleures-pratiques-data.md", "## 2. Conventional Commits", ["git/12-bons-commits"]),
    ("01-Fondamentaux/Github/03-pull-requests-code-review.md", "## Qu'est-ce qu'une Pull Request ?", ["git/13-pull-request"]),
    # --- Éditeurs (nano, Vim) ---
    ("01-Fondamentaux/Bash-Zsh/Bash/04-scripts-automatisation.md", "### Éditer dans le terminal : nano et Vim",
     ["editeurs/00-pourquoi-un-editeur", "editeurs/02-nano-chercher", "editeurs/03-nano-couper-coller", "editeurs/04-vim-sortir"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/04-scripts-automatisation.md", "### Aller plus loin avec Vim",
     ["editeurs/05-vim-se-deplacer", "editeurs/07-vim-couper-coller", "editeurs/08-vim-chercher-remplacer", "editeurs/09-vim-mode-visuel"]),
    ("01-Fondamentaux/Bash-Zsh/Bash/07-bonnes-pratiques.md", "## 2. Configuration .bashrc / .zshrc", ["editeurs/10-vimrc"]),
    # --- VS Code ---
    ("01-Fondamentaux/Python/Niveau-1/00-Parcours-Progressif/00-prerequis-installation/GUIDE-INSTALLATION.md",
     "## 2. Installer VS Code et ses extensions", ["vscode/00-installer-et-decouvrir", "vscode/07-extensions", "vscode/10-reglages"]),
    ("01-Fondamentaux/Python/Niveau-1/00-Parcours-Progressif/00-prerequis-installation/GUIDE-INSTALLATION.md",
     "## 7. Ouvrir le projet dans VS Code et exécuter une cellule",
     ["vscode/01-explorateur", "vscode/06-terminal-integre", "vscode/04-palette-de-commandes", "vscode/02-ecrire-vite",
      "vscode/03-selection-multiple", "vscode/05-chercher-remplacer", "vscode/11-snippets"]),
    ("01-Fondamentaux/Git/03-premiers-pas.md", "## 2. Le cycle de vie d'un fichier", ["git/03-trois-zones", "vscode/08-git-dans-vscode"]),
    ("01-Fondamentaux/Linux/05-reseau-linux.md", "## 2. Ports et Services", ["bash/23-ssh", "vscode/12-travailler-a-distance"]),
    # --- Python débutant (parcours progressif) ---
    *[(f"01-Fondamentaux/Python/Niveau-1/00-Parcours-Progressif/{m}/README.md", titre, eps) for m, titre, eps in [
        ("01-premiers-pas", "# Module 01 — Premiers pas", ["python-debutant/01-premiers-pas"]),
        ("03-conditions", "# Module 03 — Les conditions", ["python-debutant/03-conditions"]),
        ("06-dictionnaires", "# Module 06 — Les dictionnaires, ta fiche (et ton premier tableau)", ["python-debutant/06-dictionnaires"]),
        ("07-fonctions", "# Module 07 — Les fonctions : tes recettes", ["python-debutant/07-fonctions"]),
        ("08-fichiers-erreurs", "# Module 08 — Fichiers et erreurs : lire le vrai fichier",
         ["python-debutant/08-fichiers-erreurs", "vscode/09-deboguer"]),
        ("09-modules-api", "# Module 09 — Modules et API météo", ["python-debutant/09-modules-api", "ressources/00-lire-le-json-d-une-api"]),
        ("11-objets", "# Module 11 — Tes premiers objets", ["python-debutant/11-objets"]),
        ("12-sqlite", "# Module 12 — Ranger les données en base : SQLite", ["python-debutant/12-sqlite"]),
    ]],
    # --- CI/CD ---
    ("07-DevOps/01-CI-CD/01-Introduction/README.md", "## Qu'est-ce que le CI/CD ?", ["cicd/00-pourquoi-la-ci"]),
    ("07-DevOps/01-CI-CD/02-Git-Workflows/README.md", "## Pourquoi un workflow Git ?", ["cicd/01-strategies-branches"]),
    ("07-DevOps/03-Pre-commit/cours/02-pre-commit-framework.md", "## Qu'est-ce que pre-commit ?", ["cicd/02-pre-commit"]),
    ("07-DevOps/01-CI-CD/03-GitHub-Actions/README.md", "## Workflows de base", ["cicd/03-premier-workflow", "cicd/04-tests-a-chaque-push", "cicd/06-vraie-base"]),
    ("07-DevOps/01-CI-CD/03-GitHub-Actions/README.md", "## Débogage et optimisation", ["cicd/05-pipeline-rouge"]),
    ("07-DevOps/01-CI-CD/03-GitHub-Actions/README.md", "## Workflows avancés", ["cicd/08-image-a-chaque-version", "cicd/09-deployer"]),
    # --- Briefs ---
    ("99-Brief/Data-Engineer/IRVE-Bornes-Recharge/BRIEF_IRVE_CICD.md", "### GitHub Actions et CI/CD — ce que c'est",
     ["cicd/00-pourquoi-la-ci", "git/12-bons-commits", "cicd/08-image-a-chaque-version", "cicd/05-pipeline-rouge", "git/07-branches", "git/13-pull-request", "git/09-pousser", "git/11-mettre-de-cote", "git/06-ignorer-des-fichiers"]),
    ("99-Brief/Data-Engineer/IRVE-Bornes-Recharge/BRIEF_IRVE_CICD.md", "### uv et Python",
     ["python-debutant/09-modules-api", "ressources/00-lire-le-json-d-une-api", "python-debutant/08-fichiers-erreurs"]),
    ("99-Brief/Data-Engineer/IRVE-Bornes-Recharge/BRIEF_IRVE_CICD.md", "### Données, SQL et RGPD",
     ["bash/21-telecharger-et-archiver"]),
    ("99-Brief/Data-Engineer/CineNote-API/BRIEF_CINENOTE.md", "### Phase 2 — Découvrir l'ORM (J1, après-midi)",
     ["python-debutant/12-sqlite", "python-debutant/11-objets"]),
]

MARQUEUR = "<!-- videos:"


def video_en_ligne(episode: str) -> tuple[str, str] | None:
    """Renvoie (id, titre) si l'épisode est sur YouTube et lisible publiquement."""
    etat = STUDIO / episode / "etat.json"
    if not etat.exists():
        return None
    vid = (json.loads(etat.read_text()).get("youtube") or {}).get("id")
    if not vid:
        return None
    url = "https://www.youtube.com/oembed?format=json&url=" + urllib.parse.quote(
        f"https://www.youtube.com/watch?v={vid}"
    )
    try:
        with urllib.request.urlopen(url, timeout=10) as r:
            return vid, json.load(r)["title"]
    except Exception:  # 401/403 = privée, 404 = supprimée, réseau…
        return None


def bloc(videos: list[tuple[str, str]]) -> list[str]:
    largeur = 320 if len(videos) == 1 else 260
    miniatures = " ".join(
        f'<a href="https://www.youtube.com/watch?v={v}" title="{t}">'
        f'<img src="https://i.ytimg.com/vi/{v}/mqdefault.jpg" alt="▶ {t}" width="{largeur}"></a>'
        for v, t in videos
    )
    legendes = " · ".join(f"▶ [{t}](https://www.youtube.com/watch?v={v})" for v, t in videos)
    entete = "🎬 **En vidéo**" + (f" ({len(videos)} épisodes)" if len(videos) > 1 else "")
    return [
        f"{MARQUEUR}{','.join(v for v, _ in videos)} -->",
        f"> {entete}",
        ">",
        f"> {miniatures}",
        ">",
        f"> {legendes}",
        "",
    ]


def mettre_a_jour(lignes: list[str], section: str, videos: list[tuple[str, str]]) -> None:
    idx = lignes.index(section)  # ValueError si le titre a changé : à corriger dans PLAN
    pos = idx + 1
    if pos < len(lignes) and lignes[pos].strip() == "":
        pos += 1
    # retire l'ancien bloc s'il existe (marqueur + lignes « > » + ligne vide)
    if pos < len(lignes) and lignes[pos].startswith(MARQUEUR):
        fin = pos + 1
        while fin < len(lignes) and lignes[fin].startswith(">"):
            fin += 1
        if fin < len(lignes) and lignes[fin].strip() == "":
            fin += 1
        del lignes[pos:fin]
    if videos:
        lignes[pos:pos] = bloc(videos)


def main() -> int:
    p = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    p.add_argument("--dry-run", action="store_true", help="n'écrit rien, liste les fichiers modifiés")
    args = p.parse_args()

    if not STUDIO.is_dir():
        print(f"Dossier du studio introuvable : {STUDIO} (variable FORMATION_VIDEOS)", file=sys.stderr)
        return 1

    cache: dict[str, tuple[str, str] | None] = {}
    absents: list[str] = []
    par_fichier: dict[str, list[tuple[str, list[str]]]] = {}
    for fichier, section, episodes in PLAN:
        par_fichier.setdefault(fichier, []).append((section, episodes))

    for fichier, items in par_fichier.items():
        chemin = RACINE / fichier
        avant = chemin.read_text()
        lignes = avant.splitlines()
        for section, episodes in items:
            videos = []
            for ep in episodes:
                if ep not in cache:
                    cache[ep] = video_en_ligne(ep)
                if cache[ep]:
                    videos.append(cache[ep])
                else:
                    absents.append(ep)
            mettre_a_jour(lignes, section, videos)
        apres = "\n".join(lignes) + "\n"
        if apres != avant:
            print(("à modifier " if args.dry_run else "modifié   ") + fichier)
            if not args.dry_run:
                chemin.write_text(apres)

    en_ligne = sum(1 for v in cache.values() if v)
    print(f"\n{en_ligne} vidéo(s) en ligne insérée(s), {len(absents)} épisode(s) pas encore disponible(s) :")
    for ep in absents:
        print("  -", ep)
    return 0


if __name__ == "__main__":
    sys.exit(main())
