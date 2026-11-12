# 03 - Pull Requests et Code Review

[← 02 - Premiers pas](02-premiers-pas-ssh.md) | [🏠 Accueil](README.md) | [04 - Issues et Projects →](04-issues-gestion-projet.md)

---

## Objectifs de cette partie

- Comprendre le rôle central des Pull Requests
- Créer une Pull Request complète et bien documentée
- Effectuer des code reviews constructives
- Connaître les bonnes pratiques pour auteurs et reviewers
- Choisir le bon type de merge

## Qu'est-ce qu'une Pull Request ?

<!-- videos:BiLbI_uNCvg -->
> 🎬 **En vidéo**
>
> <a href="https://www.youtube.com/watch?v=BiLbI_uNCvg" title="Git 13 : Bonus : la pull request (GitHub, pull request, revue de code)"><img src="https://i.ytimg.com/vi/BiLbI_uNCvg/mqdefault.jpg" alt="▶ Git 13 : Bonus : la pull request (GitHub, pull request, revue de code)" width="320"></a>
>
> ▶ [Git 13 : Bonus : la pull request (GitHub, pull request, revue de code)](https://www.youtube.com/watch?v=BiLbI_uNCvg)

Une **Pull Request** (ou PR) est le mécanisme central de collaboration sur GitHub.
C'est une demande pour intégrer des modifications d'une branche vers une autre, généralement de
votre
branche feature vers `main`.

```bash
┌──────────────┐
│  main branch │
└──────┬───────┘
       │
       │ (créer feature branch)
       ↓
┌──────────────────┐
│ feature/new-etl  │ ← Développement
└──────┬───────────┘
       │
       │ (push + create PR)
       ↓
┌──────────────────┐
│   Pull Request   │ ← Review, Discussion, Tests
└──────┬───────────┘
       │
       │ (merge après approbation)
       ↓
┌──────────────┐
│  main branch │ ← Code intégré
└──────────────┘
```

### Créer une Pull Request : Workflow complet

#### Étape 1 : Créer une branche

```bash
# S'assurer d'être à jour
git checkout main
git pull origin main

# Créer une branche feature
git checkout -b feature/add-data-validation

# Développer votre fonctionnalité
# ... modifiez vos fichiers ...

# Committer vos changements
git add .
git commit -m "feat: add data validation module"
```

#### Étape 2 : Pousser la branche

```bash
# Pousser la branche vers GitHub
git push -u origin feature/add-data-validation

# GitHub affiche un lien direct pour créer la PR
```

#### Étape 3 : Créer la PR sur GitHub

1. Allez sur votre repository sur GitHub
2. Cliquez sur **Compare & pull request**
3. Ou allez dans l'onglet **Pull requests** → **New pull request**
4. Sélectionnez les branches :
   - **base** : `main` (branche de destination)
   - **compare** : `feature/add-data-validation` (votre branche)

#### Étape 4 : Rédiger une description complète

Une bonne PR contient :

```bash
## 🎯 Objectif

Ajout d'un module de validation des données pour détecter les problèmes de qualité avant le chargement.

## 📝 Changements

- Nouveau fichier `src/validate.py` avec deux fonctions principales
- `validate_schema()` : vérifie que les colonnes attendues sont présentes
- `validate_data_quality()` : détecte les valeurs nulles et doublons
- Ajout de tests unitaires dans `tests/test_validate.py`
- Mise à jour du README avec documentation du module

## ✅ Tests

- [x] Tests unitaires passent localement (`pytest tests/`)
- [x] Testé manuellement avec un dataset de 10 000 lignes
- [x] Pas de régression sur les pipelines existants

## 🔗 Liens

Closes #42

## 📸 Captures d'écran (si UI)

N/A

## ⚠️ Points d'attention pour les reviewers

- Vérifier si la logique de détection des doublons est suffisante
- Suggérer des validations supplémentaires à implémenter
```

#### Étape 5 : Assigner des reviewers

Sur la droite de la PR :

- **Reviewers** : Sélectionnez les personnes qui doivent relire le code
- **Assignees** : Vous-même (personne responsable de la PR)
- **Labels** : Exemple : `enhancement`, `bug`,
  `documentation`
- **Projects** : Lier à un projet si vous utilisez GitHub Projects
- **Milestone** : Si applicable (exemple : v1.0.0)

### Code Review : Bonnes pratiques

#### Pour l'auteur de la PR

#### ✅ À faire

- PR petite et focalisée (< 400 lignes)
- Description claire et complète
- Tests qui passent avant de demander review
- Répondre rapidement aux commentaires
- Accepter les critiques constructives

#### ❌ À éviter

- PR massive avec des milliers de lignes
- Mélanger plusieurs features non liées
- Ignorer les commentaires des reviewers
- Push force sans prévenir
- Description vide ou "fix"

#### Pour le reviewer

#### ✅ À faire

- Lire toute la PR avant de commenter
- Être constructif et respectueux
- Proposer des solutions, pas juste critiquer
- Valider la logique métier
- Vérifier les tests et edge cases

#### ❌ À éviter

- Commentaires vagues ("c'est moche")
- Imposer son style personnel
- Bloquer pour des détails mineurs
- Ignorer la PR pendant des jours
- Approuver sans vraiment lire

#### Types de commentaires sur une PR

- **Comment** : Simple commentaire, pas bloquant
- **Approve** : ✅ Validation de la PR, prête à merger
- **Request changes** : ❌ Modifications nécessaires avant merge

### Intégrer les modifications demandées

```bash
# Effectuer les modifications demandées
# ... éditer les fichiers ...

# Committer les changements
git add .
git commit -m "fix: address review comments - improve error handling"

# Pousser les modifications
git push origin feature/add-data-validation

# La PR se met automatiquement à jour sur GitHub
```

#### Git Push automatique

Chaque fois que vous push un nouveau commit on la branche, la PR est automatiquement mise à
jour.
Les reviewers sont notifiés des nouveaux changements.

### Merger la Pull Request

Une fois que la PR est approuvée et que les tests passent :

#### Trois types de merge

| Type | Description | Quand l'utiliser ? |
| --- | --- | --- |
| **Merge commit** | Crée un commit de merge, garde tout l'historique | Projets où l'historique complet est important |
| **Squash and merge** | Combine tous les commits en un seul | Garder un historique propre sur main (recommandé) |
| **Rebase and merge** | Réapplique les commits sur main sans commit de merge | Historique linéaire strict |

#### Recommandation

Pour la plupart des projets, **Squash and merge** est le meilleur choix.
Cela crée un historique propre sur main avec un commit par feature.

#### Après le merge

```bash
# Mettre à jour votre branche main locale
git checkout main
git pull origin main

# Supprimer la branche feature localement
git branch -d feature/add-data-validation

# GitHub propose automatiquement de supprimer la branche distante
```

### 💡 Points clés à retenir

- Les Pull Requests sont le mécanisme central de collaboration sur GitHub
- Une PR doit être petite (< 400 lignes), focalisée et bien documentée
- Les code reviews sont constructives, respectueuses et proposent des solutions
- Squash and merge est recommandé pour garder un historique propre
- Ne mergez qu'après approbation et tests qui passent

---

[← 02 - Premiers pas](02-premiers-pas-ssh.md) | [🏠 Accueil](README.md) | [04 - Issues et Projects →](04-issues-gestion-projet.md)
