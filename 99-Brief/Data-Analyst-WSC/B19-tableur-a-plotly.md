# Brief B19 — Du croisement expert à l'interactivité : tableur avancé puis Plotly

## Informations

| | |
|---|---|
| **Semaine** | S25 · 15–19 mars 2027 · 5 jours · Guillaume |
| **Modalité · Évaluation** | Individuel · Sommatif |
| **Compétences visées** | C4.5 · C4.3 · C4.2 · C4.1 · C4.7 |

## Description

Les directeurs de magasin d'une enseigne ne veulent pas d'un rapport figé : ils veulent explorer eux-mêmes leurs chiffres. Vous poussez le tableur à son maximum pour croiser les données, puis vous passez à Plotly pour rendre l'exploration interactive.

## Contexte

Une enseigne de distribution spécialisée compte 40 magasins. Chaque directeur de magasin veut suivre sa performance, mais leurs besoins diffèrent : l'un s'intéresse aux familles de produits, l'autre aux heures d'affluence, un troisième à la comparaison avec les magasins voisins. Un rapport figé unique ne satisfait personne.

La directrice réseau formule la demande : « Mes directeurs sont des opérationnels, pas des analystes. Ils veulent cliquer, filtrer, comparer, sans m'appeler. Donnez-leur de quoi explorer leurs chiffres eux-mêmes. »

Vous procédez en deux temps qui montrent une progression d'outil. D'abord, vous poussez le tableur à son plus haut niveau : tableaux croisés dynamiques experts, croisements multiples, recherches inter-fichiers pour rapprocher magasins et référentiels, segments et filtres interactifs. C'est l'aboutissement de la compétence tableur commencée en S1 — son niveau transposer.

Puis vous atteignez la limite du tableur : il n'est ni partageable en ligne facilement, ni aussi fluide qu'une vraie interface interactive. Vous basculez alors sur Plotly, qui produit des graphiques que l'utilisateur manipule dans son navigateur — survol, zoom, filtres. C'est votre première dataviz interactive, destinée à des utilisateurs opérationnels, exactement comme le formule le référentiel.

L'enjeu n'est pas la beauté mais l'autonomie de l'utilisateur : un bon graphique interactif est celui qui répond à la question que l'utilisateur ne vous a pas posée.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C4.5** — Utiliser un tableur, notamment les tableaux croisés dynamiques, afin de proposer des croisements de variables pour obtenir des informations recherchées *(niveau 3 — transposer)*
- **C4.3** — Manipuler la dataviz interactive et dynamique (Plotly ou Bokeh) à destination d'utilisateurs opérationnels *(niveau 1 — imiter)*
- **C4.2** — Utiliser les visualisations descriptives *(niveau 2 — adapter)*
- **C4.1** — Identifier et prioriser les informations à présenter *(niveau 2 — adapter)*
- **C4.7** — Prendre en compte les handicaps visuels *(niveau 2 — adapter)*

## Modalités pédagogiques

**Organisation** : individuel.

**Jour 1 — matin (lancement, 2 h)**. Le formateur joue la directrice réseau. Vous recevez les données de vente des 40 magasins. Vous identifiez les questions différentes que se posent les directeurs.

**Jour 1 — après-midi**. Vous poussez le tableur : TCD multi-niveaux, segments, croisements.

**Jour 2 — matin (apport flash, 1 h 30)**. Tableur expert : segments, chronologies, graphiques croisés dynamiques, consolidation multi-feuilles.

**Jour 3 — matin (apport flash, 2 h)**. Plotly : principe des graphiques interactifs, survol, zoom, filtres, menus déroulants. Export en HTML autonome partageable.

**Jours 2 à 4 — production**.
1. **Croiser (tableur)** — un classeur d'analyse permettant de croiser ventes, magasins, familles de produits, périodes, avec segments et filtres.
2. **Identifier la limite** — documentez ce que le tableur ne permet pas bien pour l'usage visé.
3. **Basculer (Plotly)** — reconstruisez les vues clés en Plotly, interactives : l'utilisateur filtre, survole, compare.
4. **Rendre accessible** — palette et alternatives (réactivation B18).
5. **Livrer** — un HTML autonome que les directeurs ouvrent sans rien installer.

**Questions guidantes.** Un directeur qui veut comparer deux familles de produits doit-il vous appeler ou pouvoir le faire seul ? Qu'apporte l'interactivité que le tableur ne donne pas — et qu'est-ce qui, au contraire, était plus simple au tableur ? Un graphique interactif surchargé de boutons aide-t-il ou perd-il l'utilisateur ? Comment garder l'accessibilité daltonisme dans un graphique Plotly ?

**Jour 4 — après-midi (revue croisée)**. Un autre apprenant, sans explication, doit répondre à trois questions métier en manipulant votre graphique interactif. S'il n'y arrive pas seul, l'interface est à revoir.

**Jour 5**. Finalisation, publication, restitution 8 minutes.

## Modalités d'évaluation

Brief **sommatif**, checklist complète.

C4.5 est ici au **niveau transposer** : c'est l'aboutissement du fil tableur. Le classeur doit démontrer une maîtrise experte — croisements multiples, recherches inter-fichiers, segments — de façon autonome.

C4.3 démarre au niveau imiter : un graphique Plotly interactif fonctionnel, que l'utilisateur peut manipuler, suffit. La sophistication viendra ensuite. Le test décisif est celui de la revue croisée : un opérationnel doit trouver seul ses réponses.

## Données fournies (source exacte)

> Ventes **synthétiques** d'une enseigne fictive (40 magasins), en **deux fichiers** pour permettre
> la recherche inter-fichiers (VLOOKUP magasins ↔ ventes). Générées à graine figée
> (`generer_donnees.py`).

- `data/ventes.csv` — lignes de vente (magasin × famille × mois × heure, CA, quantité) ; ~31 700 lignes.
- `data/magasins.csv` — référentiel des 40 magasins (ville, région, surface, voisins).
- Saisonnalité par famille (Jardin au printemps, Déco en fin d'année) + effet heure d'affluence.

## Livrables attendus

**Un dépôt GitHub public** :

1. `README.md` — projet, démarche tableur → Plotly, auteur.
2. `analyse.xlsx` — le classeur expert : TCD multi-niveaux, segments, recherches inter-fichiers, graphiques croisés.
3. `limites-tableur.md` — ce que le tableur ne permet pas pour l'usage, justifiant la bascule.
4. `interactif/dashboard.py` — le code Plotly.
5. `interactif/dashboard.html` — l'export autonome, ouvrable sans installation.
6. `accessibilite.md` — palette et alternatives.

## Critères de performance

**C4.5 — Tableur, niveau transposer**
• Le classeur croise au moins trois dimensions via TCD.
• Des segments ou filtres interactifs sont en place.
• Au moins une recherche inter-fichiers rapproche deux sources.
• Un graphique croisé dynamique est produit.

**C4.3 — Dataviz interactive, niveau imiter**
• Au moins deux graphiques Plotly interactifs sont produits (survol, zoom ou filtre actifs).
• L'export HTML s'ouvre sans installation.
• Un utilisateur non initié trouve seul des réponses (test de revue croisée réussi).

**C4.2 — Visualisations, niveau adapter**
• Les types de graphiques sont adaptés aux données.
• Titres, légendes et unités présents.

**C4.1 — Priorisation, niveau adapter**
• Les vues répondent aux questions réelles des directeurs, identifiées au jour 1.

**C4.7 — Accessibilité, niveau adapter**
• La palette reste compatible daltonisme, y compris dans Plotly.

## Ressources

- Plotly Python — documentation : https://plotly.com/python/
- Plotly — export HTML autonome : https://plotly.com/python/interactive-html-export/
- Microsoft — segments et chronologies (Excel) : https://support.microsoft.com/fr-fr/office/utiliser-des-segments-pour-filtrer-des-donn%C3%A9es-249f966b-a9d5-4b0f-b31a-12651785d29d
- Google Sheets — tableaux croisés dynamiques avancés : https://support.google.com/docs/answer/1272900
- ColorBrewer — palettes accessibles : https://colorbrewer2.org/
