# Brief B10 — Squad de refactoring : clean code, pull requests et suivi agile

## Informations

| | |
|---|---|
| **Semaine** | S12 · 30 nov–1er déc + 4 déc 2026 · 3 jours · Guillaume & Ayoub |
| **Modalité · Évaluation** | Squad (3–4) · Formatif — méthodes agiles |
| **Compétences visées** | C2.2 · C2.4 · C2.3 · C2.5 · C4.8 |

## Description

Le pipeline de consolidation existe, mais chaque binôme a écrit le sien dans son coin. La direction veut un seul outil, maintenu par l'équipe. Vous formez une squad, vous reprenez le code des autres, et vous le rendez présentable — en trois jours, avec les rituels d'une vraie équipe.

## Contexte

Le groupement Saveurs de France a récupéré, la semaine dernière, plusieurs pipelines de consolidation fonctionnels — un par binôme. Ils marchent, mais ils sont incompatibles entre eux : noms de fonctions différents, structures de fichiers différentes, aucune convention commune. La DSI refuse de maintenir cinq versions du même outil.

La décision tombe : un seul pipeline, tenu par une équipe, avec des règles communes. C'est un scénario que vous rencontrerez dans toutes les entreprises — le moment où le code cesse d'être une affaire personnelle pour devenir un bien collectif.

Cette semaine est courte (trois jours, à cause des journées de recherche d'entreprise du 2 et 3 décembre) et elle change de nature. Vous ne produisez pas une nouvelle analyse : vous transformez du code existant en code d'équipe. Vous adoptez les outils et les rituels qui rendent ce travail possible — le suivi de tâches, les branches, les pull requests, la revue de code entre pairs.

Le critère du référentiel est explicite : « méthodes agiles afin de permettre le travail en équipe, outils de suivi de projets ». Ce brief l'incarne. La compétence évaluée n'est pas de coder mieux tout seul, mais de coder ensemble.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C2.2** — Utiliser les outils et méthodes modernes : méthodes agiles pour le travail en équipe, outils de suivi de projets, logiciel adapté à la rédaction de code *(niveau 2 — adapter)*
- **C2.4** — Appliquer les bonnes pratiques de la programmation : code organisé, réutilisable et partageable dans un cadre professionnel *(niveau 2 — adapter)*
- **C2.3** — Manipuler des structures de données et utiliser l'algorithmie *(niveau 2 — adapter)*
- **C2.5** — Utiliser les DataFrames avec pandas *(niveau 2 — adapter)*
- **C4.8** — Présenter à l'oral et à l'écrit *(niveau 2 — adapter)*

## Modalités pédagogiques

**Organisation** : squads de 3 à 4. Chaque squad récupère les pipelines de deux binômes (dont le sien) et doit en produire une version unique, propre et documentée.

**Jour 1 — matin (lancement + apport flash, 2 h)**. Constitution des squads. Apport : le flux de travail Git en équipe — branches, commits atomiques, pull requests, revue, fusion. Mise en place d'un board Kanban (GitHub Projects). Définition collective des conventions : nommage, structure des fichiers, style.

**Jour 1 — après-midi**. La squad lit les deux pipelines hérités. Elle décide ce qu'elle garde, ce qu'elle jette, ce qu'elle réécrit. Elle découpe le travail en tâches sur le board.

**Jour 2 — production**. Chaque membre travaille sur sa branche, ouvre des pull requests, relit celles des autres. **Règle stricte** : aucun code n'est fusionné sans avoir été relu et approuvé par un autre membre. Le stand-up de 15 minutes ouvre la journée.

**Jour 3 — matin**. Finalisation, documentation, README commun. Nettoyage du dépôt.

**Jour 3 — après-midi (démo + rétrospective)**. Chaque squad présente en 10 minutes son outil et sa manière de travailler : montrez le board, l'historique des PR, une revue de code réelle. Puis rétrospective d'équipe : qu'est-ce qui a bloqué la collaboration, que garderiez-vous, que changeriez-vous ?

**Questions guidantes.** Comment découper le travail pour que trois personnes avancent sans se marcher dessus ? Que fait-on quand deux membres modifient la même fonction — comment l'évite-t-on plutôt que de le subir ? Une pull request de 400 lignes est-elle relisible ? Qu'est-ce qu'un bon message de commit, du point de vue de celui qui lira l'historique dans six mois ? Une revue de code sert-elle à corriger, à comprendre, ou à décider ensemble ?

## Modalités d'évaluation

Brief **formatif**, centré sur le collectif.

L'évaluation ne porte pas sur la performance individuelle mais sur la **preuve de collaboration**, lisible dans les traces : le board de suivi, l'historique des pull requests, les commentaires de revue. Une squad dont tout le code a été poussé par une seule personne n'a pas atteint l'objectif, même si le code est excellent.

La rétrospective du jour 3 fait partie de l'exercice : savoir dire ce qui n'a pas fonctionné dans le travail d'équipe est une compétence professionnelle en soi. Retour collectif du formateur en clôture.

## Données fournies (source exacte)

> B10 **ne produit pas de nouvelle donnée** : il refactore le pipeline de B09 sur les **mêmes 4
> sources** (Saveurs de France). Un test de **non-régression** vérifie que le résultat reste identique.

- **Sources** : les 4 exports de B09 (`enseigne_A.csv` … `enseigne_D.txt`) + `data/produits_reference.csv`
  (produits **OpenFoodFacts** réels). Reproductibles : `python3 generer_sources.py`.

## Livrables attendus

**Un dépôt GitHub public** par squad :

1. `README.md` — l'outil consolidé, son installation, les conventions adoptées, les membres.
2. `CONTRIBUTING.md` — les règles de travail que la squad s'est données : convention de nommage, format des commits, processus de revue.
3. Le pipeline consolidé, propre et découpé.
4. **Le board de suivi** (GitHub Projects) — laissé ouvert et accessible.
5. **L'historique des pull requests** — au moins une PR par membre, chacune relue et commentée par un autre.
6. `retrospective.md` — le compte rendu de la rétrospective d'équipe.

## Critères de performance

**C2.2 — Méthodes agiles, niveau adapter**
• Un board de suivi est utilisé, avec des tâches réparties et déplacées au fil des jours.
• Le flux par branches et pull requests est effectivement suivi.
• Au moins une pull request par membre existe et a été relue par un autre membre.
• Le stand-up quotidien a eu lieu (traces ou témoignage).

**C2.4 — Clean code, niveau adapter**
• Le dépôt suit une convention de nommage unique, documentée dans `CONTRIBUTING.md`.
• Le code est découpé en fonctions cohérentes, sans duplication entre les anciens pipelines.
• Les messages de commit sont explicites et atomiques.
• Le code final respecte PEP 8.

**C2.3 / C2.5 — Réactivation**
• Le pipeline consolidé reste fonctionnel après refactoring : il produit le même résultat qu'avant.
• Un test ou une vérification le prouve.

**C4.8 — Restitution, niveau adapter**
• La démo de 10 minutes montre le fonctionnement collectif, pas seulement le résultat.
• La rétrospective identifie au moins un point de friction et une amélioration.

## Ressources

- GitHub — flux de travail avec les branches : https://docs.github.com/fr/get-started/quickstart/github-flow
- GitHub — à propos des pull requests : https://docs.github.com/fr/pull-requests/collaborating-with-pull-requests/proposing-changes-to-your-work-with-pull-requests/about-pull-requests
- GitHub Projects — suivi de tâches : https://docs.github.com/fr/issues/planning-and-tracking-with-projects
- Conventional Commits — format des messages : https://www.conventionalcommits.org/fr/v1.0.0/
- PEP 8 — guide de style : https://peps.python.org/pep-0008/
