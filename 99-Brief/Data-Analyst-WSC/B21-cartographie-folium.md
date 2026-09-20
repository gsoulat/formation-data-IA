# Brief B21 — Diagnostic territorial : cartographie interactive et agrégée avec Folium

## Informations

| | |
|---|---|
| **Semaine** | S27 · 30 mars + 1er avril 2027 · 2 jours · Ayoub & Guillaume |
| **Modalité · Évaluation** | Binôme · Formatif — dernier brief avant l'entreprise |
| **Compétences visées** | C4.4 · C4.3 · C1.6 |

## Description

Une agence d'urbanisme veut voir ses données sur une carte, pas dans un tableau. En deux jours, vous produisez une cartographie interactive qui agrège les données par commune — la dernière brique de visualisation avant votre départ en entreprise.

## Contexte

L'agence d'urbanisme de la métropole prépare un diagnostic territorial : équipements, population, services, accessibilité, répartis sur 95 communes. Ces données existent, mais présentées en tableaux elles ne parlent pas. Une inégalité d'équipement entre le nord et le sud du territoire saute aux yeux sur une carte et reste invisible dans un tableur.

La chargée d'études le dit simplement : « Mes élus ne lisent pas les tableaux. Ils lisent les cartes. Montrez-moi le territoire, pas des chiffres alignés. »

Cette semaine est courte — deux jours seulement, à cause du férié du lundi de Pâques et du pont. C'est volontairement le dernier apport de visualisation avant votre départ en entreprise : une brique ciblée, la cartographie, qui complète votre palette de restitution.

Vous utiliserez Folium, qui produit des cartes interactives dans le navigateur. Vous agrégerez les données par commune — le référentiel précise « de manière agrégée » — et vous les représenterez par des aplats de couleur ou des marqueurs proportionnels. La carte sera interactive : l'utilisateur survole une commune et voit ses données.

Vous réactiverez la collecte par API (B07) pour récupérer les contours géographiques des communes, et vos acquis de dataviz pour choisir la bonne représentation et rester accessible.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C4.4** — Réaliser de la cartographie (notamment avec Folium) afin de représenter des informations géographiques *(niveau 1 — imiter)*
- **C4.3** — Manipuler la dataviz interactive et dynamique *(niveau 2 — adapter)*
- **C1.6** — Mettre en place une interface standard de partage automatique de données (API) *(niveau 3 — transposer)*

## Modalités pédagogiques

**Organisation** : binôme, dépôt commun. Deux jours, donc un périmètre resserré.

**Jour 1 — matin (lancement + apport flash, 2 h 30)**. Le formateur joue la chargée d'études. Puis apport : Folium, fonds de carte, marqueurs, agrégation par zone, cartes choroplèthes (aplats de couleur proportionnels). Récupération des contours communaux par API.

**Jour 1 — après-midi et jour 2 — matin (production)**.
1. **Récupérer** — les contours des communes par API (réactivation B07).
2. **Agréger** — vos données par commune.
3. **Cartographier** — une carte choroplèthe interactive : chaque commune colorée selon un indicateur.
4. **Rendre interactif** — survol affichant le détail de la commune.
5. **Rendre accessible** — palette lisible, y compris daltonisme.

**Questions guidantes.** Une carte choroplèthe convient-elle à une donnée absolue (population) ou faut-il une densité ? Comment éviter qu'une grande commune peu peuplée domine visuellement ? Quelle palette pour que la lecture reste juste, sans exagérer les écarts ? Que montre-t-on au survol, et qu'est-ce qui surcharge ?

**Jour 2 — après-midi**. Finalisation, publication, restitution 6 minutes.

## Modalités d'évaluation

Brief **formatif**. Auto-évaluation, revue croisée express, retour collectif.

Format court : l'objectif est qu'une carte interactive fonctionnelle et accessible existe, pas une œuvre. C4.4 démarre au niveau imiter et sera porté au niveau adapter en B22 puis transposer au palier 4.

C1.6 est revalidé au niveau transposer via la récupération des contours par API.

## Données fournies (source exacte)

> Données **réelles** — pas de synthétique ici : l'**API Géo** (geo.api.gouv.fr, open data, sans clé)
> fournit contours + population + surface des communes.

- **API Géo** — communes de la **MEL** (EPCI `200093201`, **95 communes**) :
  `https://geo.api.gouv.fr/epcis/200093201/communes?fields=nom,code,population,surface,contour&format=geojson&geometry=contour`
- Indicateur cartographié : **densité (hab/km²)**, calculée depuis population/surface INSEE réelles.
- Variante : changer le code EPCI/département pour un autre territoire.

## Livrables attendus

**Un dépôt GitHub public** par binôme :

1. `README.md` — projet, données, auteurs.
2. `collecte-contours.py` — récupération API des géométries communales.
3. `carte.py` — le code Folium.
4. `carte.html` — la carte interactive autonome.
5. `note-lecture.md` — ce que la carte révèle sur le territoire.

## Critères de performance

**C4.4 — Cartographie, niveau imiter**
• Une carte Folium interactive est produite.
• Les données sont agrégées par commune.
• Une représentation adaptée est choisie (choroplèthe ou marqueurs proportionnels) et justifiée.
• L'interactivité fonctionne (survol ou clic affichant le détail).

**C4.3 — Dataviz interactive, niveau adapter**
• L'export HTML s'ouvre sans installation.
• La palette est accessible.

**C1.6 — API, niveau transposer (revalidation)**
• Les contours géographiques sont récupérés par API de façon autonome.

## Ressources

- Folium — documentation : https://python-visualization.github.io/folium/
- Folium — cartes choroplèthes : https://python-visualization.github.io/folium/latest/user_guide/geojson/geojson.html
- API Géo — contours des communes : https://geo.api.gouv.fr/decoupage-administratif/communes
- France GeoJSON — contours administratifs : https://github.com/gregoiredavid/france-geojson
- ColorBrewer — palettes pour cartes : https://colorbrewer2.org/
