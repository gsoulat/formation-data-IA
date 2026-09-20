# Brief MSP1 — Observatoire de la mobilité : mettre en place une collecte de données de bout en bout

## Informations

| | |
|---|---|
| **Semaine** | S9 (9–10 nov, 2 j) + S10 (16–20 nov, 5 j) · Guillaume · 7 jours |
| **Modalité · Évaluation** | INDIVIDUEL · CERTIFICATIF — évaluation individuelle par un examinateur |
| **Compétences visées** | C1.1 · C1.2 · C1.3 · C1.4 · C1.5 · C1.6 · C1.7 · C4.8 |

## Description

Mise en situation professionnelle du bloc 1. Une autorité organisatrice de mobilité vous confie la création de son observatoire : trois sources de nature différente à collecter, une base à modéliser, un cadre RGPD à établir, et une soutenance individuelle devant examinateur.

## Contexte

Le syndicat mixte des transports du Grand Bassin regroupe 74 communes et 310 000 habitants. Il délègue l'exploitation de son réseau à un opérateur privé, dont le contrat arrive à échéance dans dix-huit mois.

Le directeur général se prépare à la renégociation et découvre un problème embarrassant : le syndicat ne dispose d'aucune donnée propre. Tout ce qu'il sait de son réseau lui vient des rapports de l'opérateur, produits par l'opérateur, selon des méthodes définies par l'opérateur. En négociation, cette asymétrie coûte cher.

Il lance donc la création d'un observatoire indépendant, et vous en confie la mise en place. Trois sources sont disponibles, de nature radicalement différente :

**Une base de données** — l'historique de validation des titres de transport sur trois ans, restitué par l'opérateur au format brut. Volumineuse, non documentée, avec des trous correspondant à des pannes de matériel.

**Une API** — le système d'information voyageurs régional expose en temps réel les horaires théoriques et les perturbations déclarées.

**Des pages web** — les horaires affichés au public, ainsi que les avis d'usagers publiés sur une plateforme de signalement, n'existent que sous forme de pages.

Le directeur général formule sa demande en une phrase : « Je veux, à l'issue de votre mission, pouvoir dire à l'opérateur ce que je constate, avec mes propres chiffres, et pouvoir le prouver. »

La déléguée à la protection des données du syndicat suit le dossier de près : les validations de titres nominatifs sont des données personnelles, et le croisement avec des horaires permet de reconstituer des déplacements individuels.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C1.1** — Identifier les possibilités d'utilisation des données, être force de proposition dans l'exploration, l'évaluation de la qualité et l'interprétation *(niveau 3 — transposer)*
- **C1.2** — Définir une stratégie de prise de décision par les données suivant les besoins métier *(niveau 3 — transposer)*
- **C1.3** — Modéliser des bases de données relationnelles afin de répondre avec rigueur aux besoins des utilisateurs *(niveau 3 — transposer)*
- **C1.4** — Réaliser des requêtes avancées : agrégations, jointures, vues et sous-requêtes, en s'assurant de l'intégrité *(niveau 3 — transposer)*
- **C1.5** — Automatiser des collectes de données par web scraping dans le respect de la réglementation *(niveau 3 — transposer)*
- **C1.6** — Mettre en place une interface standard de partage automatique de données entre applications et langages *(niveau 3 — transposer)*
- **C1.7** — Contrôler les modalités de collecte et d'utilisation de données et mesurer les enjeux du RGPD *(niveau 3 — transposer)*
- **C4.8** — Présenter à l'oral et à l'écrit de manière claire, concise et sans ambiguïté *(niveau 2 — adapter)*

## Modalités pédagogiques

**Organisation** : strictement individuel. Aucune entraide n'est autorisée sur la production. Le formateur reste disponible pour des questions de compréhension du besoin, pas de méthode.

**Aucun apport formel** n'est délivré pendant les sept jours. Toutes les compétences mobilisées ont été travaillées en B01 à B08.

**Semaine 1 — S9 (2 jours, cadrage)**
- **Lundi** : appropriation du besoin. Entretien de 20 minutes avec le formateur en directeur général : vous posez vos questions, il répond en commanditaire, pas en formateur. Exploration de la base livrée.
- **Mardi** : production du cahier des charges et du rapport d'exploration initial. Livraison obligatoire mardi 17 h — ces deux documents sont évalués.

**Semaine 2 — S10 (5 jours, production et soutenance)**
- **Lundi à mercredi** : modélisation, collecte des trois sources, alimentation de la base, registre RGPD.
- **Jeudi** : requêtes d'analyse, note de performance, finalisation du dépôt. Gel des livrables jeudi 17 h.
- **Vendredi** : soutenances individuelles de 20 minutes devant examinateur (15 minutes de présentation, 5 de questions).

**Attendus de la soutenance.** Vous présentez votre observatoire à un décideur non technique. Vous devez pouvoir répondre à trois questions qui seront posées à tous : quelle est la donnée dont vous vous méfiez le plus dans votre dispositif et pourquoi ? quelle décision de renégociation vos chiffres permettent-ils d'appuyer ? qu'avez-vous fait des données personnelles ?

**Cadre.** Le référentiel prévoit que les candidats effectuent des recherches à partir de questions proposées et automatisent la récupération des données depuis une base. Les questions métier vous sont fournies dans le dossier de cadrage remis le lundi de S9.

## Modalités d'évaluation

**Mise en situation professionnelle certificative du bloc 1**, évaluée individuellement par un examinateur, conformément au référentiel WCS.

**Deux temps d'évaluation.**
1. **Dossier** (livrables gelés jeudi 17 h de S10). L'examinateur vérifie chaque critère du référentiel sur le dépôt.
2. **Soutenance individuelle** (vendredi, 20 minutes). Présentation devant examinateur, suivie de questions.

**Règle de validation** : la compétence est acquise lorsque 100 % de ses critères sont validés. Le bloc est acquis lorsque les sept compétences le sont.

**Rattrapage.** Une compétence non acquise à ce palier pourra être revalidée lors d'un palier ultérieur : le palier 2 remobilise C1.4 et C1.6 au niveau 3, le palier 3 remobilise C1.4, le palier 4 remobilise l'ensemble de la chaîne. Cette possibilité est à confirmer avec le certificateur.

**Conditions matérielles** : accès internet autorisé, documentation autorisée, travaux personnels antérieurs autorisés. Aucune assistance humaine.

## Données fournies (source exacte)

> Sources **mixtes** : la base de validations est **synthétique** (des données personnelles sont
> nécessaires au scénario RGPD, absentes de l'open data) ; l'API et le scraping utilisent des
> sources **réelles**.

- **Base de validations** : `validations_brutes.csv` — export brut (~120 000 validations sur 3 ans,
  titres nominatifs, trous correspondant à des pannes). Reproductible : `python3 generer_base.py`.
- **API réseau** : `transport.data.gouv.fr/api/datasets` (ouverte, sans clé) — référence des réseaux
  (le SIV temps réel de l'opérateur exigerait une clé).
- **Pages web** : `books.toscrape.com` (bac à sable légal) pour horaires et avis.

## Livrables attendus

**Un dépôt GitHub public**, gelé jeudi 17 h de S10 :

1. `README.md` — présentation de l'observatoire, architecture, installation, auteur.
2. `01-cadrage/cahier-des-charges.md` — besoin reformulé, périmètre, sources retenues, questions métier traitées *(livré à la fin de S9)*.
3. `01-cadrage/rapport-exploration.md` — exploration de la base livrée : volumétrie, qualité, trous, anomalies, enjeux et possibilités métier *(livré à la fin de S9)*.
4. `02-modele/schema.png` + `schema.sql` — modèle relationnel avec contraintes d'intégrité.
5. `03-collecte/api_siv.py` — client API du système d'information voyageurs.
6. `03-collecte/scraper_horaires.py` et `scraper_avis.py` — extraction des pages web.
7. `03-collecte/format-echange.md` — documentation du format d'échange entre langages.
8. `04-analyse/requetes.sql` — les requêtes répondant aux questions métier, dont vue et sous-requête.
9. `04-analyse/rapport-performance.md` — temps avant, index, temps après, plan d'exécution.
10. `05-rgpd/registre.md` — registre des traitements complet.
11. `05-rgpd/analyse-risques.md` — enjeux, responsabilités, risques, mesures prises.
12. `strategie-data-driven.md` — la stratégie de décision par les données proposée au directeur général.

**Support de soutenance** : libre (le tableau de bord viendra plus tard dans la formation).

## Critères de performance

**C1.1 — Exploration et qualité**
• Une exploration de la base est effectuée et documentée : volumétrie, taux de remplissage, doublons, incohérences, périodes manquantes.
• Les enjeux et les possibilités métier sont présentés explicitement.
• Au moins une proposition non demandée est formulée (posture de force de proposition).

**C1.2 — Stratégie data-driven**
• Une stratégie de prise de décision par les données est décrite, reliée à la renégociation du contrat.
• Chaque décision visée est associée à un indicateur et à sa fréquence de production.

**C1.3 — Modélisation**
• Le modèle correspond au besoin métier exprimé et couvre les trois sources.
• Les contraintes d'intégrité sont posées et justifiées.
• Le modèle est optimisé pour un usage professionnel : choix d'index, de types, de granularité, argumentés.

**C1.4 — Requêtes**
• Les requêtes répondent aux questions posées dans le dossier de cadrage.
• Agrégations, jointures, vue et sous-requête sont présentes.
• L'intégrité est vérifiée par des requêtes de contrôle.
• La performance et les optimisations sont présentées : mesure avant/après et plan d'exécution.

**C1.5 — Scraping**
• Les données sont collectées automatiquement depuis les pages web.
• Le respect de la réglementation est documenté et les mesures de limitation appliquées.

**C1.6 — API REST**
• Les requêtes API sont utilisées et automatisées pour compléter la base.
• Le format d'échange entre langages est précisé et documenté.

**C1.7 — RGPD**
• Chaque donnée personnelle entrant dans le cadre du RGPD est décrite.
• Les enjeux, responsabilités et risques sont explicités.
• Les mesures à prendre sont précisées et, lorsqu'elles sont applicables, mises en œuvre.

**C4.8 — Restitution (niveau adapter)**
• La soutenance tient dans le temps imparti et s'adresse à un non-technicien.
• Les trois questions communes reçoivent une réponse argumentée.

## Ressources

- Dossier de cadrage et jeu de données : Remis par le formateur le lundi de S9
- CNIL — registre des activités de traitement : https://www.cnil.fr/fr/RGPD-le-registre-des-activites-de-traitement
- CNIL — analyse d'impact (PIA) : https://www.cnil.fr/fr/analyse-dimpact-relative-la-protection-des-donnees-pia
- PostgreSQL — EXPLAIN : https://www.postgresql.org/docs/current/using-explain.html
- transport.data.gouv.fr — données de mobilité : https://transport.data.gouv.fr/
- Vos travaux B01 à B08 : Consultation de vos propres dépôts autorisée
