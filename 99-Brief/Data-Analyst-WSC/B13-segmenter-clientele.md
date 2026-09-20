# Brief B13 — Segmenter une clientèle bancaire : multivarié, corrélations et anomalies

## Informations

| | |
|---|---|
| **Semaine** | S17 · 18–22 janv 2027 · 5 jours · Ayoub |
| **Modalité · Évaluation** | Binôme · Formatif |
| **Compétences visées** | C3.1 · C2.5 · C2.6 · C1.4 · C4.5 |

## Description

Une banque veut arrêter de traiter ses 45 000 clients de la même façon. Sans intelligence artificielle, avec les seules statistiques descriptives, vous faites émerger des groupes de clients cohérents et vous les décrivez à la direction marketing.

## Contexte

Une banque de détail régionale sert 45 000 clients particuliers. Sa communication est uniforme : tout le monde reçoit les mêmes offres, les mêmes courriels, les mêmes propositions de produits. Le taux de retour est faible et la direction marketing soupçonne que le message ne touche personne parce qu'il vise tout le monde.

La directrice marketing veut segmenter : constituer des groupes de clients qui se ressemblent, pour adapter le discours à chacun. Mais elle refuse la boîte noire. « Je ne veux pas d'un algorithme mystérieux qui me sort huit segments que je ne comprends pas. Je veux des groupes que je peux nommer, décrire à mon équipe, et justifier devant mon directeur. »

Vous disposez du jeu de données Bank Marketing : 45 000 clients, avec âge, profession, situation familiale, solde moyen, produits détenus, historique de contacts. Des variables numériques et catégorielles mêlées, quelques valeurs manquantes, des distributions déséquilibrées.

Votre mission n'utilise pas encore le machine learning — il arrive la semaine prochaine. Elle mobilise ce que vous savez déjà, porté à son plus haut niveau : les statistiques descriptives multivariées. Croiser les variables, mesurer leurs corrélations, repérer les groupes naturels et les anomalies, et surtout traduire tout cela en segments que la directrice marketing pourra nommer.

C'est le sommet de la compétence C3.1 : faire émerger, des seules statistiques, une information que personne ne voyait dans le tableau brut.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C3.1** — Utiliser les statistiques descriptives afin de modéliser les données et en faire émerger des informations pertinentes *(niveau 3 — transposer)*
- **C2.5** — Utiliser les DataFrames avec pandas *(niveau 3 — transposer)*
- **C2.6** — Nettoyer les données *(niveau 3 — transposer)*
- **C1.4** — Réaliser des requêtes avancées *(niveau 3 — transposer)*
- **C4.5** — Utiliser un tableur, notamment les TCD *(niveau 2 — adapter)*

## Modalités pédagogiques

**Organisation** : binôme, dépôt commun.

**Jour 1 — matin (lancement, 2 h)**. Le formateur joue la directrice marketing. Vous recevez le jeu de données. Première tâche : produisez le profil univarié de chaque variable et repérez celles qui semblent porter de l'information distinctive.

**Jour 1 — après-midi**. Exploration libre. Vous cherchez des relations entre variables.

**Jour 2 — matin (apport flash, 2 h)**. Analyse multivariée descriptive : matrice de corrélation et sa lecture, tableaux croisés à plusieurs entrées, détection d'anomalies multivariées. Construire une segmentation à la main à partir de seuils sur deux ou trois variables discriminantes.

**Jours 2 à 4 — production**.
1. **Explorer** — profil de chaque variable, valeurs manquantes et aberrantes traitées (réactivation B11).
2. **Corréler** — matrice de corrélation entre variables numériques, croisements entre variables catégorielles. Quelles variables vont ensemble ?
3. **Segmenter** — constituez trois à cinq segments à partir des variables les plus discriminantes. La méthode est descriptive : seuils, croisements, règles explicites.
4. **Caractériser** — pour chaque segment : son poids, son profil, ce qui le distingue, et un nom parlant.
5. **Restituer** — une fiche par segment, destinée à l'équipe marketing.

**Questions guidantes.** Deux variables très corrélées apportent-elles deux informations ou une seule ? Un segment qui représente 2 % des clients mérite-t-il d'exister ? Comment nommer un groupe sans le caricaturer ? Un client qui n'entre dans aucun segment est-il une anomalie ou le signe qu'il manque un segment ? La directrice pourra-t-elle expliquer votre segmentation à quelqu'un qui n'était pas là ?

**Jour 4 — après-midi (revue croisée)**. Un autre binôme reçoit vos fiches de segments sans vos données, et doit deviner à quel segment appartiendraient trois clients types. Si les fiches ne le permettent pas, elles sont à revoir.

**Jour 5**. Finalisation, publication, restitution 8 minutes.

## Modalités d'évaluation

Brief **formatif**. Auto-évaluation, revue croisée, retour collectif.

C3.1 est ici au **niveau transposer** : c'est l'aboutissement du fil statistique commencé en S2. L'exigence n'est plus de calculer des indicateurs mais de faire émerger, par eux seuls, une structure exploitable — et de la rendre intelligible à un non-statisticien.

La bascule vers le machine learning aura lieu la semaine prochaine : ce brief sert de point de comparaison. La semaine prochaine, vous laisserez un algorithme trouver les segments, et vous confronterez son résultat au vôtre.

## Données fournies (source exacte)

> Jeu **réel**, sans donnée personnelle directe.

- **Jeu** : **Bank Marketing** (UCI) — https://archive.ics.uci.edu/dataset/222/bank+marketing
  (fichier `bank-full.csv`, **45 211 clients**, séparateur `;`).
- Colonnes : âge, profession, situation familiale, solde, prêts (immo/conso), historique de contact,
  souscription (`y`). Les `unknown` sont des manquants déguisés.

## Livrables attendus

**Un dépôt GitHub public** par binôme :

1. `README.md` — projet, méthode, auteurs.
2. `exploration.ipynb` — profil des variables, valeurs traitées, matrice de corrélation commentée.
3. `segmentation.ipynb` — la construction des segments, avec les règles explicites.
4. `fiches-segments.md` — une fiche par segment : nom, poids, profil, traits distinctifs.
5. `recommandations-marketing.md` — pour chaque segment, une piste d'action.

## Critères de performance

**C3.1 — Statistiques descriptives, niveau transposer**
• Le profil de chaque variable est produit (position, dispersion, distribution).
• Une matrice de corrélation est calculée et lue : les relations fortes sont commentées.
• Trois à cinq segments sont constitués selon des règles explicites et reproductibles.
• Chaque segment est caractérisé quantitativement et nommé.
• Au moins une anomalie ou un groupe atypique est identifié et interprété.

**C2.5 / C2.6 — Réactivation (niveau transposer)**
• L'ensemble est réalisé avec pandas de façon autonome.
• Les valeurs manquantes et aberrantes sont traitées avec une méthode justifiée.

**C1.4 — Réactivation (niveau transposer)**
• Si les données proviennent d'une base, l'extraction est faite par requête.

**C4.5 — Réactivation (niveau adapter)**
• Au moins un croisement est vérifié ou présenté par TCD.

**Restitution**
• Les fiches de segments permettent à un tiers de classer un client type (test de la revue croisée).

## Ressources

- Bank Marketing Dataset (UCI) : https://archive.ics.uci.edu/dataset/222/bank+marketing
- pandas — corrélations : https://pandas.pydata.org/docs/reference/api/pandas.DataFrame.corr.html
- seaborn — heatmap de corrélation : https://seaborn.pydata.org/generated/seaborn.heatmap.html
- Comprendre corrélation et causalité : https://www.insee.fr/fr/metadonnees/definitions
- pandas — groupby et tableaux croisés : https://pandas.pydata.org/docs/user_guide/groupby.html
