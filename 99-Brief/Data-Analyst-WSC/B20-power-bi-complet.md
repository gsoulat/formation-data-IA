# Brief B20 — Tableau de bord Power BI complet : modèle en étoile, Power Query, DAX et commentaires

## Informations

| | |
|---|---|
| **Semaine** | S26 · 22–26 mars 2027 · 5 jours · Ayoub |
| **Modalité · Évaluation** | Binôme · Sommatif — DERNIER BRIEF AVANT L'ENTREPRISE |
| **Compétences visées** | C4.6 · C4.5 · C4.1 · C4.7 · C1.3 |

## Description

C'est le brief le plus important avant votre départ en entreprise : vous devez maîtriser Power BI de bout en bout — modèle en étoile, Power Query, mesures DAX, commentaires stratégiques — pour pouvoir le pratiquer sur les données réelles de votre entreprise d'accueil.

## Contexte

Une enseigne de distribution veut piloter sa performance commerciale avec un vrai outil de Business Intelligence. Le tableur a atteint ses limites : les données viennent de quatre sources (ventes, magasins, produits, calendrier), le volume est important, et la direction veut un tableau de bord stratégique qui oriente les décisions, pas seulement qui affiche des chiffres.

La directrice commerciale décrit son attente : « Je veux ouvrir mon tableau de bord le lundi matin, voir immédiatement où on en est, comprendre pourquoi, et savoir quoi faire. Pas une usine à gaz : un outil de décision. » Elle veut aussi des commentaires écrits sur le tableau de bord — le référentiel le précise : « les commentaires rédigés sur le tableau de bord sont pertinents et correspondent aux questions métier ».

Ce brief est stratégique dans votre parcours pour une raison de calendrier. Dans deux semaines, vous partez 350 heures en entreprise. Beaucoup d'entre vous travailleront sur un projet de tableau de bord. Si vous découvrez Power BI en juin, à votre retour, vous n'aurez pas le temps. Si vous le maîtrisez maintenant, vous passerez votre période en entreprise à le pratiquer sur des données réelles et à en rapporter un livrable solide pour votre certification.

Vous allez donc apprendre Power BI en entier, en une semaine intensive : importer et transformer les données avec Power Query, construire un modèle en étoile (réactivation directe de votre modélisation relationnelle du bloc 1), créer des mesures avec DAX, et composer un tableau de bord commenté et accessible. C'est dense, mais chaque brique s'appuie sur une compétence que vous possédez déjà.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C4.6** — Réaliser des tableaux de bord avec des outils de Business Intelligence (PowerBI ou Tableau) afin d'intégrer et de croiser des informations utiles à des approches stratégiques *(niveau 1 — imiter)*
- **C4.5** — Utiliser un tableur, notamment les TCD *(niveau 3 — transposer)*
- **C4.1** — Identifier et prioriser les informations à présenter *(niveau 2 — adapter)*
- **C4.7** — Prendre en compte les handicaps visuels *(niveau 2 — adapter)*
- **C1.3** — Modéliser des bases de données relationnelles *(niveau 3 — transposer)*

## Modalités pédagogiques

**Organisation** : binôme, dépôt commun.

**Jour 1 — matin (lancement, 2 h)**. Le formateur joue la directrice commerciale. Vous recevez les quatre sources. Vous reconnaissez un problème de modélisation que vous savez traiter : comment organiser ces tables ?

**Jour 1 — après-midi (apport flash, 2 h)**. Power BI et Power Query : import, transformation, nettoyage des sources. Notion de requête.

**Jour 2 — matin (apport flash, 2 h)**. Le modèle en étoile : table de faits, tables de dimensions, relations. C'est votre modélisation relationnelle du bloc 1, appliquée à la BI. Pourquoi l'étoile plutôt qu'un grand tableau plat.

**Jour 3 — matin (apport flash, 2 h)**. DAX : mesures, colonnes calculées, fonctions courantes. Le TCD que vous maîtrisez devient une mesure DAX — même logique, autre écriture.

**Jours 2 à 4 — production**.
1. **Transformer** — importez et nettoyez les quatre sources avec Power Query.
2. **Modéliser** — un modèle en étoile : faits (ventes), dimensions (magasin, produit, temps).
3. **Mesurer** — des mesures DAX répondant aux questions de la directrice (CA, évolution, panier moyen, contribution par famille).
4. **Composer** — un tableau de bord stratégique, priorisé (réactivation B18), accessible (réactivation B18).
5. **Commenter** — des commentaires écrits pertinents, reliés aux questions métier.

**Questions guidantes.** Faut-il un grand tableau plat ou plusieurs tables reliées — et pourquoi l'étoile facilite-t-elle les mesures ? Une mesure DAX et une colonne calculée, quelle différence, et quand utiliser l'une ou l'autre ? Un tableau de bord qui affiche le CA sans le comparer à quoi que ce soit aide-t-il à décider ? Un commentaire « CA en hausse de 4 % » est-il pertinent, ou faut-il dire pourquoi et quoi faire ?

**Jour 4 — après-midi (revue croisée)**. Un autre binôme joue la directrice et cherche : peut-elle décider quelque chose en ouvrant votre tableau de bord ?

**Jour 5**. Finalisation, publication, restitution 10 minutes. Bilan des acquis à emporter en entreprise.

## Modalités d'évaluation

Brief **sommatif**, checklist complète.

C4.6 démarre au niveau imiter — un tableau de bord Power BI fonctionnel, avec modèle en étoile, mesures DAX et commentaires, construit sur un cas guidé. Il sera porté au niveau adapter en B22 (retour d'entreprise) puis transposer au palier 4.

L'enjeu réel dépasse la note : c'est la dernière semaine encadrée sur Power BI avant l'entreprise. Le formateur s'assurera en retour collectif que chaque apprenant repart avec un modèle en étoile fonctionnel qu'il saura reproduire seul — c'est la condition pour que les 350 heures servent le livrable certificatif.

C4.5 atteint le niveau transposer et C1.3 est revalidé au niveau transposer : le modèle en étoile est une base relationnelle.

## Données fournies (source exacte)

> **4 sources synthétiques** d'une enseigne fictive (ventes, magasins, produits, calendrier),
> générées à graine figée (`generer_sources.py`) et volontairement **sales** (décimales en texte,
> doublons, casse des régions) pour exercer Power Query. Après nettoyage → **modèle en étoile**.

- `sources/ventes_brut.csv` (faits), `magasins_brut.csv`, `produits_brut.csv`, `calendrier_brut.csv`.
- Le corrigé fournit le modèle en étoile déjà nettoyé (`etl/star/`) + les mesures DAX validées.
- **Note certification** : en entreprise, la même chaîne se rejoue sur les **données réelles** de la
  structure d'accueil (cf. `guide-reprise.md`).

## Livrables attendus

**Un dépôt GitHub public** par binôme :

1. `README.md` — projet, architecture du modèle, auteurs.
2. `powerbi/tableau-de-bord.pbix` — le fichier Power BI.
3. `modele.md` — le schéma en étoile : faits, dimensions, relations, justification.
4. `mesures-dax.md` — les mesures créées, avec leur formule et la question métier à laquelle elles répondent.
5. `captures/` — captures du tableau de bord.
6. `accessibilite.md` — palette, contrastes, alternatives.
7. `guide-reprise.md` — vos notes personnelles pour reconstruire un modèle en étoile seul en entreprise.

## Critères de performance

**C4.6 — Business Intelligence, niveau imiter**
• Les quatre sources sont importées et transformées via Power Query.
• Un tableau de bord Power BI fonctionnel est produit.
• Il intègre et croise les informations pour une approche stratégique.
• Des commentaires écrits, reliés aux questions métier, figurent sur le tableau de bord.

**C4.5 — Tableur, niveau transposer**
• Les croisements attendus sont réalisés (via TCD en amont ou directement en BI).

**C1.3 — Modélisation, niveau transposer (revalidation)**
• Un modèle en étoile est construit : table de faits, tables de dimensions, relations correctes.
• Le choix de l'étoile est justifié face à un tableau plat.

**Mesures DAX**
• Au moins quatre mesures DAX répondent chacune à une question métier identifiée.
• Au moins une mesure calcule une évolution ou une comparaison.

**C4.1 / C4.7 — Réactivation, niveau adapter**
• Le tableau de bord est priorisé (pas de surcharge) et accessible (palette, alternatives).

## Ressources

- Power BI — documentation Microsoft : https://learn.microsoft.com/fr-fr/power-bi/
- Power Query — transformer les données : https://learn.microsoft.com/fr-fr/power-query/
- Modèle en étoile dans Power BI : https://learn.microsoft.com/fr-fr/power-bi/guidance/star-schema
- DAX — référence des fonctions : https://learn.microsoft.com/fr-fr/dax/
- Power BI — accessibilité des rapports : https://learn.microsoft.com/fr-fr/power-bi/create-reports/desktop-accessibility-creating-reports
- Power BI Desktop — téléchargement gratuit : https://www.microsoft.com/fr-fr/power-platform/products/power-bi/desktop
