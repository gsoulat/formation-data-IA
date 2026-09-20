# Brief B01 — Enquête sur données ouvertes : première analyse et publication GitHub

## Informations

| | |
|---|---|
| **Semaine** | S1 · 14–18 sept 2026 · 5 jours · Ayoub |
| **Modalité · Évaluation** | Individuel · Formatif (auto-évaluation + revue par les pairs) |
| **Compétences visées** | C1.1 · C4.5 · C2.2 · C4.8 |

## Description

La communauté de communes vient de publier ses équipements publics en open data. Personne n'a encore ouvert le fichier. Vous êtes le premier à regarder ce que ces données contiennent vraiment, et à dire ce qu'on peut en faire. Vous rendez votre travail sur GitHub — votre premier dépôt.

## Contexte

La communauté de communes du Val d'Escaut a mis en ligne son premier jeu de données ouvertes : la liste de ses équipements publics (gymnases, bibliothèques, salles des fêtes, aires de jeux). L'élu à l'innovation en a fait une annonce sur les réseaux sociaux. Depuis, le service communication reçoit des questions de journalistes locaux et d'associations : combien d'équipements par commune ? Y a-t-il des communes sous-dotées ? Les horaires sont-ils à jour ?

Problème : personne, au sein de la collectivité, n'a jamais ouvert ce fichier autrement que pour le publier. Il a été extrait d'un vieux logiciel de gestion patrimoniale par un prestataire parti depuis. Les colonnes ne sont pas documentées. Certaines lignes semblent en double. Des dates ont l'air aberrantes.

La directrice de cabinet vous confie une mission simple à formuler et moins simple à exécuter : « Dites-moi ce qu'il y a réellement dans ce fichier, ce qu'on peut en faire, et ce qui nous empêcherait de nous en servir. » Elle veut une réponse écrite en une page, compréhensible par un élu, et elle veut pouvoir la retrouver dans six mois.

Vous n'avez pas encore d'outil d'analyse. Vous avez un tableur, un navigateur, et à partir de cette semaine un compte GitHub. C'est suffisant : le métier de data analyst commence toujours par ce geste — ouvrir un fichier qu'on ne connaît pas et le regarder honnêtement.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C1.1** — Identifier les possibilités d'utilisation des données, être force de proposition dans l'exploration et l'évaluation de la qualité *(niveau 1 — imiter)*
- **C4.5** — Utiliser un tableur pour proposer des croisements de variables *(niveau 1 — imiter)*
- **C2.2** — Utiliser les outils et méthodes modernes : outils de suivi, logiciel adapté à la rédaction de code *(niveau 1 — imiter)*
- **C4.8** — Présenter à l'oral et à l'écrit de manière claire, concise et sans ambiguïté *(niveau 1 — imiter)*

## Modalités pédagogiques

**Organisation** : travail individuel. Chaque apprenant crée son propre dépôt GitHub, qui servira de portfolio pendant toute la formation.

**Jour 1 — matin (lancement, 2 h)**. Présentation du contexte par le formateur, qui joue le rôle de la directrice de cabinet. Vous récupérez le jeu de données sur data.gouv.fr. Vous l'ouvrez. Vous n'écrivez rien encore : vous regardez.

**Jour 1 — après-midi**. Première exploration libre, avec ce que vous savez déjà faire. Notez tout ce qui vous surprend, tout ce que vous ne comprenez pas, tout ce qui vous paraît faux. Cette liste est le vrai livrable intermédiaire.

**Jour 2 — matin (apport flash, 1 h)**. Prise en main du tableur : structure d'un classeur, formules, références absolues et relatives, tri et filtre. Puis Git et GitHub : créer un dépôt, committer, pousser, rédiger un README.

**Jours 2 à 4 — production**. Répondez par écrit à cinq questions que la collectivité se pose réellement :
1. Combien d'équipements le fichier contient-il, et combien de communes sont concernées ?
2. Quelle commune en a le plus, laquelle en a le moins ?
3. Combien de types d'équipements différents recense-t-on ?
4. Quelle proportion de lignes est incomplète ?
5. Repérez-vous des doublons, et à quoi les reconnaissez-vous ?

**Questions guidantes — ne les sautez pas.** Qu'est-ce qui vous prouve qu'une ligne est un doublon plutôt que deux équipements homonymes ? Une cellule vide et une cellule contenant « NC » sont-elles la même chose ? Si deux communes ont un nombre d'équipements identique mais des populations très différentes, la comparaison est-elle honnête ? Que faudrait-il pour qu'elle le devienne ?

**Jour 4 — après-midi (revue croisée, 2 h)**. Vous relisez le dépôt d'un autre apprenant à partir d'une grille fournie, et vous lui rendez un avis écrit. Un dépôt qu'on ne comprend pas en trois minutes est un dépôt à retravailler.

**Jour 5**. Mise au propre, rédaction du README, publication. L'après-midi, restitution orale de 5 minutes devant le groupe : ce que contient le fichier, ce qu'on peut en faire, ce qui bloque. Puis rétrospective collective.

## Modalités d'évaluation

Brief **formatif** : il ne donne pas lieu à une note individuelle. L'évaluation se fait en trois temps.

1. **Auto-évaluation** : vous complétez la grille fournie avant la restitution, en cochant ce que vous estimez avoir réussi.
2. **Revue par les pairs** : le jour 4, un autre apprenant relit votre dépôt et rend un avis écrit sur la clarté du README, la lisibilité du classeur et la solidité de vos réponses.
3. **Retour collectif** : le formateur reprend en fin de semaine les points communs observés dans les dépôts, sans nommer personne.

L'objectif de cette première semaine n'est pas de produire une analyse parfaite mais d'installer trois réflexes : ouvrir des données sans a priori, écrire ce qu'on trouve, publier son travail.

## Données fournies (source exacte)

> Le scénario (« communauté de communes du Val d'Escaut ») est **fictif** ; les **données réelles**
> qui servent de support — et sur lesquelles porte la correction — sont celles de la
> **CC du Pays de Mormal** (Nord).

- **Jeu** : Recensement des équipements sportifs (RES) — Ministère chargé des Sports.
- **Page** : https://www.data.gouv.fr/datasets/recensement-des-equipements-sportifs-espaces-et-sites-de-pratiques
- **Périmètre** : équipements de la **CC du Pays de Mormal** (278 lignes).
- **Extraction reproductible** :

```bash
curl -sG "https://equipements.sports.gouv.fr/api/explore/v2.1/catalog/datasets/data-es/exports/csv" \
  --data-urlencode 'where=epci_nom="CC du Pays de Mormal"' \
  --data-urlencode 'use_labels=false' --data-urlencode 'delimiter=;' \
  -o equipements.csv
```

- **Licence** : Licence Ouverte (Etalab).

## Livrables attendus

**Un dépôt GitHub public** contenant :

1. `README.md` — description du projet, source des données, méthode suivie, auteur.
2. `analyse.xlsx` (ou lien Google Sheets) — le classeur de travail, avec les formules apparentes et un onglet par question traitée.
3. `note-de-synthese.md` — une page maximum, rédigée pour un élu : ce que contient le fichier, trois usages possibles, trois limites de qualité qui empêcheraient de s'en servir tel quel.
4. `journal.md` — la liste des étonnements du jour 1, conservée telle quelle. Elle montre votre progression.

**Support de restitution** : 5 minutes, sans diapositives cette semaine — vous montrez directement votre dépôt.

## Critères de performance

**C1.1 — Exploration et qualité**
• Les cinq questions reçoivent une réponse chiffrée, et le chiffre est reproductible depuis le classeur.
• Au moins trois anomalies de qualité distinctes sont identifiées et illustrées par un exemple précis (numéro de ligne ou valeur).
• Au moins deux usages métier des données sont proposés, en lien avec les préoccupations exprimées par la collectivité.

**C4.5 — Tableur**
• Les résultats sont obtenus par des formules, non saisis à la main : la formule est visible dans la cellule.
• Le classeur comporte un onglet distinct par question, nommé de façon explicite.
• Au moins un tri et un filtre sont utilisés à bon escient.

**C2.2 — Outils**
• Le dépôt GitHub est public et contient au minimum trois commits distincts, avec des messages compréhensibles.
• Le README permet à un lecteur extérieur de comprendre le projet en moins de trois minutes.

**C4.8 — Restitution**
• La note de synthèse tient en une page et n'emploie aucun terme technique non expliqué.
• La restitution orale respecte les 5 minutes et présente une conclusion, pas seulement des chiffres.

## Ressources

- Jeu de données (exact) — Recensement des équipements sportifs (RES) : https://www.data.gouv.fr/datasets/recensement-des-equipements-sportifs-espaces-et-sites-de-pratiques
- Pro Git — le livre officiel, en français : https://git-scm.com/book/fr/v2
- GitHub Docs — démarrage rapide : https://docs.github.com/fr/get-started
- Rédiger un bon README : https://www.makeareadme.com/
- Aide Google Sheets — fonctions : https://support.google.com/docs/table/25273
