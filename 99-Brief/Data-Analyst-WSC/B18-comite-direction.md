# Brief B18 — Comité de direction : prioriser les indicateurs, maquetter, rendre lisible par tous

## Informations

| | |
|---|---|
| **Semaine** | S24 · 8–12 mars 2027 · 5 jours · Ayoub |
| **Modalité · Évaluation** | Binôme · Formatif |
| **Compétences visées** | C4.1 · C4.2 · C4.7 · C3.1 · C4.5 · C4.8 |

## Description

Un comité de direction reçoit un tableau de bord de 60 indicateurs que personne ne lit. Vous devez en garder 8. Choisir ce qu'on montre — et ce qu'on renonce à montrer — est le vrai métier de la restitution. Vous maquettez avant de construire, et vous rendez vos graphiques lisibles même par un daltonien.

## Contexte

Un groupe industriel de la plasturgie, 900 salariés sur cinq sites, a fait développer par un prestataire un tableau de bord qualité. Le résultat tient sur un écran surchargé de 60 indicateurs, courbes et jauges. Le comité de direction l'a ouvert deux fois, puis ne l'a plus jamais regardé : illisible.

La directrice qualité reprend le chantier à zéro, avec une conviction : « Un tableau de bord qui montre tout ne montre rien. Je veux huit indicateurs, pas soixante. Ceux qui font qu'un membre du comité, en dix secondes, sait si ça va ou pas. »

Elle ajoute deux exigences que le prestataire avait ignorées. D'abord, elle veut voir une maquette avant qu'on développe quoi que ce soit : « Je ne veux plus découvrir le résultat à la fin. » Ensuite, un des directeurs est daltonien : « Il n'a jamais rien pu lire dans les rouge-vert du précédent. Cette fois, tout le monde doit pouvoir lire. »

Votre mission ouvre le bloc 4, celui de la restitution. Elle ne consiste pas à faire de beaux graphiques mais à décider lesquels méritent d'exister. Prioriser 8 indicateurs parmi 60, c'est renoncer à 52 — et savoir défendre chaque renoncement. Vous maquetterez la disposition avant de la construire, vous produirez les visualisations descriptives qui portent ces 8 indicateurs, et vous les rendrez accessibles, y compris à un daltonien. C'est le premier des critères d'évaluation du bloc : « la synthèse et la maquette correspondent au besoin métier et sont présentées avec un formalisme professionnel ».

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C4.1** — Identifier et prioriser, en fonction du besoin métier, les informations à rendre accessibles et à présenter visuellement, afin de structurer des représentations graphiques de tableaux de bord *(niveau 1 — imiter)*
- **C4.2** — Utiliser les visualisations descriptives : nuages de points, boîtes à moustache, histogrammes *(niveau 2 — adapter)*
- **C4.7** — Prendre en compte les handicaps visuels afin de produire des graphiques lisibles par tous *(niveau 1 — imiter)*
- **C3.1** — Utiliser les statistiques descriptives *(niveau 3 — transposer)*
- **C4.5** — Utiliser un tableur, notamment les TCD *(niveau 2 — adapter)*
- **C4.8** — Présenter à l'oral et à l'écrit *(niveau 2 — adapter)*

## Modalités pédagogiques

**Organisation** : binôme, dépôt commun.

**Jour 1 — matin (lancement, 2 h)**. Le formateur joue la directrice qualité. Vous recevez les 60 indicateurs du prestataire et les données sous-jacentes. Première tâche : classez ces 60 indicateurs par importance pour un comité de direction. Sur quels critères ?

**Jour 1 — après-midi**. Vous confrontez vos choix entre binômes. Les désaccords sur ce qui compte sont le cœur du brief.

**Jour 2 — matin (apport flash, 2 h)**. Priorisation : lier chaque indicateur à une décision. Le maquettage : wireframe, hiérarchie visuelle, ce qu'on met en haut à gauche. Choix du bon graphique selon la donnée (rappel B02). Accessibilité : palettes sûres pour daltoniens, contrastes, alternatives textuelles.

**Jours 2 à 4 — production**.
1. **Prioriser** — sélectionnez 8 indicateurs parmi 60. Pour chacun, la décision qu'il éclaire. Pour les écartés, une ligne justifiant le renoncement.
2. **Maquetter** — une maquette de la disposition, avant toute construction : où va quoi, pourquoi.
3. **Construire** — les 8 visualisations, chacune du bon type, titrée, légendée.
4. **Rendre accessible** — palette compatible daltonisme, contrastes suffisants, chaque graphique doublé d'une phrase de lecture.
5. **Synthétiser** — une note d'une page présentant l'ensemble avec un formalisme professionnel.

**Questions guidantes.** Un indicateur qu'on ne peut relier à aucune décision mérite-t-il l'écran ? Entre deux indicateurs redondants, lequel garder ? Comment vérifier qu'un graphique reste lisible en noir et blanc, ou pour un daltonien — connaissez-vous un outil de simulation ? Une jauge est-elle un bon choix, ou une fausse bonne idée ? La maquette permet-elle à la directrice de valider avant que vous ayez tout construit ?

**Jour 4 — après-midi (revue croisée)**. Un autre binôme regarde votre tableau de bord dix secondes, puis on le lui cache : que retient-il ? S'il ne retient rien, la hiérarchie visuelle est à revoir. Test daltonisme obligatoire via simulateur.

**Jour 5**. Finalisation, publication, restitution 8 minutes au comité (joué par le groupe).

## Modalités d'évaluation

Brief **formatif**. Auto-évaluation, revue croisée, retour collectif.

L'évaluation porte d'abord sur la **priorisation** : le choix des 8 indicateurs est-il argumenté, chaque renoncement est-il assumé ? Puis sur la **maquette**, exigée par le référentiel avant construction. Puis sur l'**accessibilité**, testée concrètement au simulateur de daltonisme.

C4.1 et C4.7 démarrent ici au niveau imiter, C4.2 au niveau adapter (il a été amorcé en B02). Le fil sera repris en B19, B20, B22 et porté au niveau 3 au palier 4.

## Données fournies (source exacte)

> Données qualité **synthétiques** d'un groupe plasturgie fictif (5 sites × 24 mois) : rebut, OTD,
> TRS, coût de non-qualité, réclamations, satisfaction… Générées à graine figée
> (`generer_donnees.py`). Le scénario (60 indicateurs illisibles) n'a pas d'équivalent open data ;
> l'enjeu est la **priorisation** et l'**accessibilité**, pas la source.

- `data/qualite.csv` — une ligne par site × mois, 8 mesures qualité.
- Palettes/outils réels mobilisés : **ColorBrewer**, simulateur **Coblis**, **WCAG** (contrastes).

## Livrables attendus

**Un dépôt GitHub public** par binôme :

1. `README.md` — projet, démarche, auteurs.
2. `priorisation.md` — les 8 retenus avec leur décision associée, les 52 écartés avec justification synthétique.
3. `maquette/` — la maquette de disposition (image ou outil), antérieure à la construction.
4. `dashboard/` — les 8 visualisations, accessibles, avec code.
5. `accessibilite.md` — la palette choisie, les tests daltonisme, les alternatives textuelles.
6. `synthese-comite.md` — la note d'une page, formalisme professionnel.

## Critères de performance

**C4.1 — Prioriser et maquetter, niveau imiter**
• 8 indicateurs sont sélectionnés parmi les 60, chacun relié à une décision.
• Les indicateurs écartés font l'objet d'une justification, même brève.
• Une maquette de disposition est produite avant la construction.
• La synthèse d'une page présente l'ensemble avec un formalisme professionnel.

**C4.2 — Visualisations, niveau adapter**
• Chaque indicateur est porté par le type de graphique adapté à sa nature.
• Les graphiques sont titrés, légendés, avec unités.

**C4.7 — Accessibilité, niveau imiter**
• La palette est compatible avec le daltonisme (testée au simulateur).
• Les contrastes sont suffisants.
• Chaque graphique est doublé d'une phrase de lecture (alternative textuelle).

**C3.1 — Réactivation, niveau transposer**
• Les indicateurs reposent sur des statistiques correctes, calculées et vérifiables.

**C4.5 — Réactivation, niveau adapter**
• Au moins un indicateur est construit via TCD.

**C4.8 — Restitution, niveau adapter**
• La restitution de 8 minutes est structurée et tient dans le temps.

## Ressources

- Datawrapper — bonnes pratiques de dataviz : https://blog.datawrapper.de/
- ColorBrewer — palettes sûres pour daltoniens : https://colorbrewer2.org/
- Coblis — simulateur de daltonisme : https://www.color-blindness.com/coblis-color-blindness-simulator/
- Financial Times — Visual Vocabulary (choisir un graphique) : https://ft-interactive.github.io/visual-vocabulary/
- WCAG — contrastes de couleurs : https://www.w3.org/WAI/WCAG21/quickref/#contrast-minimum
- matplotlib / seaborn — galerie : https://seaborn.pydata.org/examples/index.html
