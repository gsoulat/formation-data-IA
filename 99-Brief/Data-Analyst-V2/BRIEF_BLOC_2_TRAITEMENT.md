# Brief Bloc 2 — Automatiser le traitement des données de NordRetail

## Informations

| Critère | Valeur |
|---------|--------|
| **Bloc** | Bloc 2 — Automatisation du traitement : nettoyage, complétion, correction, uniformisation |
| **Durée** | ~2 semaines (10 jours) |
| **Niveau** | Intermédiaire |
| **Modalité** | Binôme |
| **Technologies** | Python 3, pandas, expressions régulières, pytest, Git/GitHub |
| **Prérequis** | [Python](../../01-Fondamentaux/Python/) · [Pandas](../../01-Fondamentaux/Python/06-Data-Engineering/) · [RegEx](../../01-Fondamentaux/Python/04-Bibliotheque-Standard/) · [Nettoyage](../../15-Business-Intelligence/16-Nettoyage-Donnees/) |

## Description rapide

En binôme, vous transformez un export de production **sale** de NordRetail en un jeu de données
**propre et fiable**, non pas à la main, mais via un **programme de traitement réutilisable**.
Vous structurez votre code (fonctions, bonnes pratiques), manipulez les DataFrames avec pandas,
traitez outliers et valeurs manquantes, et utilisez les **expressions régulières** pour
normaliser et anonymiser les données textuelles. Livrable : un outil de nettoyage documenté et
automatisé.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **Structurer un programme de traitement** en fonctions réutilisables (clean code, PEP8).
- **Manipuler des DataFrames** (pandas) pour importer, fusionner et transformer des données.
- **Nettoyer** : détecter et traiter les valeurs aberrantes (outliers) et manquantes, avec méthode.
- **Uniformiser** des données textuelles avec les **expressions régulières** (RegEx).
- **Anonymiser** des données personnelles dans le cadre du RGPD.
- **Documenter** vos choix méthodologiques avec clarté.

## Contexte

**L'entreprise et son problème**

La collecte du bloc précédent a rempli la base, mais l'export de caisse est **truffé
d'imperfections** : villes en casse incohérente (`LILLE`, `roubaix`, `Valencienne`), dates au
format mélangé, décimales à virgule, doublons, retours (montants négatifs), `client_id`
manquants, e-mails clients en clair. Chaque mois, un stagiaire « nettoie à la main » dans Excel —
lent, non reproductible, source d'erreurs. La direction veut **industrialiser** ce nettoyage.

**La question centrale**

> « Comment transformer un export brut et imparfait en un jeu de données fiable, de façon
> **automatisée, documentée et reproductible** ? »

**Les données fournies**

Le fichier **sale** [`../Data-Analyst/data/ventes_sales.csv`](../Data-Analyst/data/ventes_sales.csv)
(la version propre `ventes_magasins.csv` sert de contrôle). Vous pouvez aussi utiliser
`ventes_corrompu.csv` pour tester la robustesse de votre outil.

## Modalités pédagogiques

Projet en BINÔME sur ~10 jours, dépôt GitHub public.

### Phase 1 — Cadrage & choix méthodologiques (J1)

Sans coder : profilez le fichier, listez **chaque type d'anomalie** et décidez, pour chacune, la
stratégie de traitement (supprimer ? corriger ? imputer ? marquer ?) et **justifiez-la**.
Écrivez ce plan méthodologique : c'est le cœur de l'évaluation. Comment traiter une valeur
manquante sans fausser les analyses ? Que faire d'un montant négatif (un retour ≠ une erreur) ?

### Phase 2 — Structurer l'outil de traitement (J2-J3)

Écrivez le squelette de votre programme : **une fonction par étape** (`charger`, `dedupliquer`,
`normaliser_villes`, `traiter_manquants`, `traiter_outliers`, `anonymiser`, `exporter`), avec
docstrings et noms explicites. Appliquez les bonnes pratiques (PEP8, code réutilisable). Le
programme s'exécute d'un bout à l'autre via une fonction `pipeline()`.

### Phase 3 — Nettoyage : manquants & outliers (J4-J6)

Implémentez le traitement des **valeurs manquantes** (selon votre plan) et des **valeurs
aberrantes** : détectez les outliers (méthode de l'IQR ou z-score), décidez de les écarter ou
non, et **argumentez**. Fusionnez au besoin plusieurs sources avec `merge`. Contrôlez que vos
totaux restent cohérents après traitement.

### Phase 4 — Uniformisation & anonymisation par RegEx (J7-J8)

Avec les **expressions régulières** : uniformisez les villes (casse, accents, fautes), validez
et normalisez les formats (dates, e-mails), et **anonymisez** les données personnelles
(masquer/hacher les e-mails, pseudonymiser `client_id`) conformément au RGPD. Chaque RegEx est
commentée.

### Phase 5 — Tests, doc & restitution (J9-J10)

Écrivez quelques **tests** (`pytest`) sur vos fonctions clés (ex. « une ville normalisée est en
Title Case », « aucun e-mail en clair après anonymisation »). Rédigez la documentation
(README + rapport méthodologique). Présentez votre outil et démontrez qu'il retraite un nouveau
fichier sans intervention manuelle.

## Modalités d'évaluation

- **Revue technique (60 %)** : structure et lisibilité du code, justesse et argumentation des
  traitements, pertinence des RegEx, effectivité de l'anonymisation, présence de tests.
- **Restitution orale (40 %)** : 10 min de démonstration (retraiter un fichier en direct) + 10 min
  de justification des choix méthodologiques.

**Validation partielle** : un binôme dont l'outil ne couvre pas tous les cas mais dont le code
est propre, les choix documentés et le nettoyage manquants/outliers rigoureux valide les acquis
de traitement.

## Livrables attendus

- Un **dépôt GitHub public** contenant :
  - le **programme de traitement** Python (modules/fonctions, `pipeline()`), exécutable ;
  - les **tests** `pytest` ;
  - le **jeu de données propre** exporté (ou le script qui le régénère) ;
  - un **rapport méthodologique** (Markdown) : chaque anomalie, la stratégie choisie et sa justification ;
  - un **`README.md`** complet.
- Une **note d'anonymisation RGPD** : quelles données, quelle technique, quel résultat.

## Critères de performance

**Structurer & documenter le code**
- Le code est organisé en fonctions réutilisables, lisibles, conformes à PEP8.
- Les choix méthodologiques sont documentés avec clarté et concision.

**Manipuler & nettoyer avec pandas**
- Import, fusion et transformations sont réalisés avec pandas.
- Les valeurs manquantes et aberrantes sont traitées, la méthode est argumentée.

**Uniformiser avec les RegEx**
- Les expressions régulières identifient et normalisent correctement des formats textuels.
- Les cas traités sont commentés et testés.

**Anonymiser (RGPD)**
- Les données personnelles sont anonymisées/pseudonymisées ; plus aucune donnée en clair ne subsiste.

## Ressources

- Cours — [Nettoyage des données](../../15-Business-Intelligence/16-Nettoyage-Donnees/)
- Cours — [Expressions régulières](../../01-Fondamentaux/Python/04-Bibliotheque-Standard/) · [Pandas](../../01-Fondamentaux/Python/06-Data-Engineering/)
- Cours — [Qualité & tests Python](../../01-Fondamentaux/Python/05-Qualite-Tests/) · [Anonymisation RGPD](../../01-Fondamentaux/RGPD-Gouvernance/05-anonymisation-pseudonymisation.md)
- Données NordRetail : [`../Data-Analyst/data/`](../Data-Analyst/data/)
- Étape précédente : [Bloc 1 — Collecte](BRIEF_BLOC_1_COLLECTE.md) · Suivante : [Bloc 3 — Modélisation](BRIEF_BLOC_3_MODELISATION.md)
