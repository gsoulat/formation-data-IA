# Brief Projet final — Chaîne data complète, de la collecte au tableau de bord

## Informations

| Critère | Valeur |
|---------|--------|
| **Portée** | Intégration des 4 blocs (collecte → traitement → modélisation → visualisation) |
| **Durée** | ~3 semaines (15 jours) |
| **Niveau** | Avancé |
| **Modalité** | Individuel (soutenance individuelle) |
| **Technologies** | SQL, Python (pandas, requests/BeautifulSoup, scikit-learn, Plotly, Folium), Power BI ou Tableau |
| **Prérequis** | Les 4 briefs de bloc validés |

## Description rapide

Individuellement, vous menez un **projet data de bout en bout** sur un jeu de données de votre
choix (ou NordRetail élargi) : vous **collectez** et modélisez les données, vous **automatisez**
leur traitement, vous **modélisez** des prévisions par Machine Learning, et vous **restituez** le
tout dans un **tableau de bord** clair et accessible. Ce projet est la synthèse du parcours et le
support de la soutenance.

## Objectifs pédagogiques

Démontrer, sur un projet complet et autonome, la maîtrise des compétences des 4 blocs :

- **Collecte** : modéliser, requêter, automatiser une récupération de données (API/scraping), RGPD.
- **Traitement** : nettoyer et uniformiser via un programme réutilisable (pandas, RegEx).
- **Modélisation** : produire des prévisions (régression/classification) et les interpréter.
- **Visualisation** : concevoir un tableau de bord interactif, accessible, orienté décision.

## Contexte

**Le sujet**

Vous choisissez un **domaine** et une **problématique métier** (NordRetail élargi, ou un jeu de
données open data qui vous intéresse : transport, énergie, santé, culture…). Le sujet doit
permettre de mobiliser **les 4 blocs** : une source à collecter/enrichir, des données à nettoyer,
une question de prévision, et un besoin de restitution.

**La question centrale**

Vous formulez votre propre question centrale, validée par le formateur, et **tout le projet doit
y répondre**. Exemple type : « Comment optimiser l'assortiment de NordRetail en anticipant les
ventes par catégorie et par territoire ? »

## Modalités pédagogiques

Projet INDIVIDUEL sur ~15 jours, dépôt GitHub public, soutenance orale finale.

### Semaine 1 — Cadrage & collecte

Formalisez le besoin et la question centrale. Modélisez la base, écrivez les requêtes d'analyse,
et **automatisez** une collecte (au moins une source externe via API ou scraping, dans le respect
du RGPD et de la légalité).

### Semaine 2 — Traitement & modélisation

Industrialisez le **nettoyage** (programme réutilisable, RegEx, anonymisation). Menez l'analyse
exploratoire, identifiez les corrélations, puis entraînez et évaluez **au moins un modèle de
prévision** (régression ou classification), en interprétant ses métriques et ses biais.

### Semaine 3 — Restitution & soutenance

Concevez le **tableau de bord** final (interactif, cartographie si pertinent, accessible).
Rédigez le **dossier de projet** et préparez la **soutenance** : présentation claire de la
démarche, des résultats, des limites et des recommandations.

## Modalités d'évaluation

- **Soutenance orale individuelle (50 %)** : 20 min de présentation (démarche, démonstration du
  tableau de bord, prévisions, recommandations) + 15 min de questions couvrant les 4 blocs.
- **Dossier & dépôt (50 %)** : complétude de la chaîne (collecte → viz), justesse technique,
  reproductibilité, documentation, prise en compte RGPD et accessibilité.

**Chaque bloc est évalué**. Un projet solide sur 3 blocs mais lacunaire sur un bloc peut valider
partiellement ; les compétences se valident indépendamment.

## Livrables attendus

- Un **dépôt GitHub public** couvrant toute la chaîne :
  - scripts de **collecte** (SQL + API/scraping) et modèle de données ;
  - **programme de traitement** (nettoyage, RegEx, anonymisation) + tests ;
  - **notebooks de modélisation** (prévision + interprétation + biais) ;
  - **tableau de bord** (fichier BI + captures / notebooks de viz) ;
  - un **`README.md`** complet et reproductible.
- Un **dossier de projet** (PDF/Markdown) : contexte, question centrale, démarche par bloc,
  résultats, limites, recommandations, conformité RGPD.
- Le **support de soutenance**.

## Critères de performance

**Collecte** — modèle relationnel correct, requêtes avancées, collecte automatisée, RGPD documenté.
**Traitement** — code structuré et réutilisable, nettoyage argumenté, RegEx, anonymisation effective.
**Modélisation** — process ML correct, métriques interprétées, biais et limites explicités.
**Visualisation** — tableau de bord clair, interactif, accessible ; restitution sans ambiguïté.
**Transversal** — le projet répond à la question centrale de bout en bout et est reproductible.

## Ressources

- Le parcours complet — [PAF Data Analyst V2](../../PATH_DATA_ANALYST_V2.md)
- Les 4 briefs de bloc — [Bloc 1](BRIEF_BLOC_1_COLLECTE.md) · [Bloc 2](BRIEF_BLOC_2_TRAITEMENT.md) · [Bloc 3](BRIEF_BLOC_3_MODELISATION.md) · [Bloc 4](BRIEF_BLOC_4_VISUALISATION.md)
- Données NordRetail : [`../Data-Analyst/data/`](../Data-Analyst/data/)
- Portails d'open data : https://www.data.gouv.fr/ · https://data.europa.eu/
