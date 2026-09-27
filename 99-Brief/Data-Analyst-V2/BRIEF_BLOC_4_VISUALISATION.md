# Brief Bloc 4 — Concevoir le tableau de bord de NordRetail

## Informations

| Critère | Valeur |
|---------|--------|
| **Bloc** | Bloc 4 — Visualisation : valorisation, interprétation & tableau de bord |
| **Durée** | ~2 semaines (10 jours) |
| **Niveau** | Intermédiaire → avancé |
| **Modalité** | Binôme |
| **Technologies** | Python (Plotly, Folium), Power BI ou Tableau, tableur (Excel/Sheets), Git/GitHub |
| **Prérequis** | [Dataviz interactive](../../15-Business-Intelligence/11-Visualisations-Avancees/02-dataviz-interactive-python.md) · [Cartographie Folium](../../15-Business-Intelligence/11-Visualisations-Avancees/03-cartographie-folium.md) · [Dashboards BI](../../15-Business-Intelligence/07-Dashboards-Fondamentaux/) · [Restitution](../../15-Business-Intelligence/08-Restitution-Storytelling/) |

## Description rapide

En binôme, vous concevez le **tableau de bord** que la direction de NordRetail attend, à partir
d'un **cahier des charges client**. Vous choisissez et priorisez les informations, produisez des
**visualisations descriptives** puis **interactives** (Plotly), une **cartographie** (Folium),
un **tableau de bord Business Intelligence** (Power BI ou Tableau), en respectant
l'**accessibilité** (handicaps visuels). Vous restituez à l'oral et à l'écrit, clairement.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **Identifier et prioriser** les informations à rendre accessibles selon le besoin métier.
- Produire des **visualisations descriptives** (nuages de points, boîtes à moustache, histogrammes).
- Créer des **dataviz interactives** (Plotly/Bokeh) et une **cartographie** (Folium).
- Construire un **tableau de bord BI** (Power BI ou Tableau) pour la décision.
- Respecter l'**accessibilité** (contrastes, code couleur, alternatives textuelles).
- **Présenter** à l'oral et à l'écrit de façon claire, concise et sans ambiguïté.

## Contexte

**L'entreprise et son problème**

NordRetail dispose de données propres, enrichies, et de premières prévisions. Il manque
l'essentiel pour la direction : un **tableau de bord** lisible « en 30 secondes » qui pilote
l'activité. La direction rédige un **cahier des charges** : suivre le CA, comparer magasins et
canaux, visualiser le territoire, et le tout doit être **accessible** (un membre du comité est
malvoyant).

**La question centrale**

> « Comment restituer l'activité de NordRetail dans un tableau de bord clair, interactif et
> accessible, qui aide vraiment la direction à décider ? »

**Les données fournies**

Le jeu propre [`../Data-Analyst/data/`](../Data-Analyst/data/) (schéma en étoile
`Faits_Ventes.csv` + `Dim_*`, `objectifs_2024.xlsx` pour comparer réalisé / objectif).

## Modalités pédagogiques

Projet en BINÔME sur ~10 jours, dépôt GitHub public.

### Phase 1 — Cahier des charges & priorisation (J1)

À partir du besoin client, **identifiez et priorisez** les informations : qui consulte, pour
décider de quoi ? Quels 4-6 indicateurs en tête ? Maquettez le tableau de bord (papier ou
croquis) : quelle info en haut, quel détail dessous, quel graphique pour quelle intention ?

### Phase 2 — Visualisations descriptives (J2-J3)

Produisez les **visualisations descriptives** de base (matplotlib/seaborn) : histogrammes des
montants, boîtes à moustache par magasin, nuages de points (ex. remise vs CA). Chaque graphique
est titré et lisible seul.

### Phase 3 — Interactivité & cartographie (J4-J6)

Passez à l'**interactif** avec **Plotly** (survol, zoom, filtres) et cartographiez le territoire
avec **Folium** (magasins géolocalisés, choroplèthe du CA par département). Exportez au moins une
viz en HTML autonome.

### Phase 4 — Tableau de bord BI & accessibilité (J7-J8)

Construisez le **tableau de bord** dans Power BI ou Tableau (ou combinez avec un tableur pour un
suivi réalisé/objectif via TCD). KPI en évidence, comparaisons, interactivité (filtres).
Appliquez l'**accessibilité** : contrastes suffisants, palette lisible pour daltoniens,
explications textuelles sous les graphiques (lecture vocale). Les chiffres doivent être **exacts**.

### Phase 5 — Restitution (J9-J10)

Rédigez une **note d'analyse** répondant à la question centrale + 2-3 recommandations. Préparez
une **présentation** claire et sans jargon, et entraînez-vous : vous devez défendre vos choix de
KPI, de visualisations et d'accessibilité.

## Modalités d'évaluation

- **Démonstration & oral (60 %)** : 12 min de présentation et démonstration live du tableau de bord
  (filtres, lecture des KPI, carte), 8 min de questions. L'adaptation au public métier et la prise
  en compte de l'accessibilité sont évaluées.
- **Revue technique (40 %)** : dépôt, notebooks de viz, fichier BI, justesse des chiffres,
  respect de l'accessibilité.

**Validation partielle** : un binôme dont le tableau de bord BI n'est pas totalement abouti mais
qui livre des visualisations descriptives, interactives et une cartographie correctes et
accessibles valide les acquis de visualisation.

## Livrables attendus

- Un **dépôt GitHub public** contenant :
  - les **notebooks de visualisation** (descriptives + Plotly + Folium), avec au moins une viz HTML autonome ;
  - le **fichier du tableau de bord BI** (`.pbix` Power BI ou lien Tableau/Looker), avec capture d'écran ;
  - la **note d'analyse** (1-2 pages) + le support de présentation ;
  - un **`README.md`** complet.
- Une **note d'accessibilité** : choix de couleurs/contrastes et alternatives textuelles retenues.

## Critères de performance

**Prioriser & structurer**
- Les informations sont identifiées et priorisées selon le besoin ; la maquette correspond au besoin métier.

**Visualiser**
- Les visualisations descriptives (nuages, boîtes, histogrammes) décrivent correctement les données.
- Les visualisations interactives (Plotly/Bokeh) sont utilisées pour communiquer ; une cartographie Folium agrégée et interactive répond au besoin.

**Tableau de bord BI**
- Un outil de BI (Power BI ou Tableau) permet une lecture stratégique ; les commentaires sont pertinents et les chiffres exacts.
- Les fonctions avancées du tableur (TCD, recherches inter-fichiers) sont mobilisées si pertinent.

**Accessibilité & restitution**
- L'accessibilité est prise en compte (code couleur, explications sous les graphiques).
- La présentation orale et écrite est claire, concise et sans ambiguïté.

## Ressources

- Cours — [Dataviz interactive (Plotly/Bokeh)](../../15-Business-Intelligence/11-Visualisations-Avancees/02-dataviz-interactive-python.md) · [Cartographie Folium](../../15-Business-Intelligence/11-Visualisations-Avancees/03-cartographie-folium.md)
- Cours — [Tableur avancé (TCD)](../../15-Business-Intelligence/19-Tableur-Avance/01-tableur-tcd.md) · [Dashboards](../../15-Business-Intelligence/07-Dashboards-Fondamentaux/)
- Cours — [Restitution & storytelling](../../15-Business-Intelligence/08-Restitution-Storytelling/) · [Accessibilité](../../11-Gestion-Projet/07-accessibilite-eco-conception.md)
- Données NordRetail : [`../Data-Analyst/data/`](../Data-Analyst/data/)
- Étape précédente : [Bloc 3 — Modélisation](BRIEF_BLOC_3_MODELISATION.md) · Suivante : [Projet final](BRIEF_PROJET_FINAL.md)
