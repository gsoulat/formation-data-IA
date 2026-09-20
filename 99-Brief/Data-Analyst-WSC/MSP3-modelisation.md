# Brief MSP3 — Réseau de transport : modéliser, prévoir et rendre le modèle explicable

## Informations

| | |
|---|---|
| **Semaine** | S22 (22–26 fév, 5 j) + S23 (1–5 mars, 5 j) · Ayoub & Guillaume · 10 jours |
| **Modalité · Évaluation** | INDIVIDUEL · CERTIFICATIF — évaluation individuelle par un examinateur |
| **Compétences visées** | C3.1 · C3.2 · C3.3 · C3.4 · C3.5 · C3.6 · C3.7 · C1.4 · C2.6 · C4.8 |

## Description

Mise en situation professionnelle du bloc 3. Une autorité de transport vous confie trois questions qui recouvrent toute la modélisation : prévoir une fréquentation, classer des incidents, analyser des retours voyageurs. Vous produisez les modèles, vous documentez leurs biais, et vous les expliquez devant un examinateur.

## Contexte

L'autorité organisatrice des transports d'une agglomération de 400 000 habitants pilote un réseau de bus et de tramways. Elle dispose de trois ans de données mais les exploite peu, faute de compétences internes. Elle vous confie une mission d'analyse prédictive en trois volets, correspondant à trois besoins réels de ses services.

**Prévoir la fréquentation.** Le service exploitation doit dimensionner l'offre — nombre de rames, fréquences — pour les mois à venir. Il veut une prévision de fréquentation par ligne, tenant compte de la saison, des vacances scolaires, des événements. C'est un problème de régression et de tendance.

**Classer les incidents.** Le service qualité reçoit des milliers de signalements d'incidents (retards, pannes, incivilités, problèmes de propreté) saisis en vrac. Il veut les catégoriser automatiquement pour suivre chaque type et prioriser. C'est un problème de classification.

**Écouter les voyageurs.** Une plateforme de signalement recueille les avis des usagers en texte libre. Le service relation client veut en extraire le sentiment et les thèmes dominants. C'est un problème de NLP.

Le directeur de l'exploitation ajoute une exigence qui vaut pour les trois volets : « Je vais présenter vos résultats à des élus. Je ne peux pas leur dire "l'algorithme a décidé". Je dois pouvoir expliquer comment ça marche, ce en quoi on peut s'y fier, et où sont les limites. »

C'est la mise en situation du bloc 3 dans son intégralité. Vous mobiliserez toute la chaîne de modélisation — statistiques, régression, classification, NLP — et vous documenterez les biais et les limites, car le référentiel exige que le modèle soit explicable et non une boîte noire. Les données brutes vous obligeront à rejouer la collecte et le nettoyage des blocs précédents.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C3.1** — Utiliser les statistiques descriptives afin de modéliser les données et en faire émerger des informations pertinentes *(niveau 3 — transposer)*
- **C3.2** — Maîtriser le process d'apprentissage automatique *(niveau 3 — transposer)*
- **C3.3** — Modéliser des régressions et interpréter les métriques, trouver des tendances futures *(niveau 3 — transposer)*
- **C3.4** — Modéliser des classifications et interpréter les métriques *(niveau 3 — transposer)*
- **C3.5** — Traiter automatiquement le langage naturel (NLP), analyse de sentiments *(niveau 3 — transposer)*
- **C3.6** — Contrôler et documenter les biais d'un modèle et des données d'entraînement *(niveau 3 — transposer)*
- **C3.7** — Communiquer et vulgariser le fonctionnement interne d'un algorithme *(niveau 3 — transposer)*
- **C1.4** — Réaliser des requêtes avancées *(niveau 3 — transposer)*
- **C2.6** — Nettoyer les données *(niveau 3 — transposer)*
- **C4.8** — Présenter à l'oral et à l'écrit *(niveau 3 — transposer)*

## Modalités pédagogiques

**Organisation** : strictement individuel. Toutes les compétences ont été travaillées de B13 à B17.

**Aucun apport formel.** Le formateur clarifie le besoin, pas la méthode.

**Semaine 1 — S22 (5 jours, production)**
- **Lundi** : cadrage (entretien de 20 min avec le formateur en directeur d'exploitation), exploration des trois jeux de données, priorisation.
- **Mardi à vendredi** : production des trois volets. Vous n'êtes pas obligé de les mener de front — organisez votre semaine.

**Semaine 2 — S23 (5 jours, finalisation et soutenance)**
- **Lundi, mardi** : consolidation, documentation des biais et limites de chaque modèle, vulgarisation. Gel des livrables mardi 17 h.
- **Mercredi, jeudi** : préparation des soutenances.
- **Vendredi** : soutenances individuelles de 25 minutes devant examinateur (18 min de présentation, 7 de questions).

**Attendus de la soutenance.** Vous présentez à un décideur qui doit ensuite convaincre des élus. Questions communes : pour chacun de vos trois modèles, en quoi peut-on lui faire confiance et où sont ses limites ? quel biais avez-vous identifié et que proposez-vous pour le corriger ? comment expliqueriez-vous votre modèle de prévision à quelqu'un qui n'y connaît rien ?

**Cadre référentiel.** Les candidats présentent une proposition de modélisation de données structurées permettant de décrire les données de manière simple, d'en tirer des tendances, de prévoir des valeurs futures et d'en interpréter les résultats. Les trois volets couvrent régression, classification et NLP, conformément aux critères d'évaluation du bloc.

## Modalités d'évaluation

**Mise en situation professionnelle certificative du bloc 3**, évaluée individuellement par un examinateur.

**Deux temps.** Dossier (gelé mardi 17 h de S23) et soutenance individuelle (vendredi, 25 min).

**Validation** : compétence acquise = 100 % de ses critères. Bloc acquis = les sept compétences C3.

**Revalidation des blocs 1 et 2** : ce palier remobilise C1.4 (extraction des données) et C2.6 (nettoyage) au niveau 3. Une compétence non acquise en amont peut être rattrapée ici.

**Rattrapage aval** : l'ensemble de la chaîne est remobilisé au palier 4.

**Conditions** : internet, documentation et travaux antérieurs autorisés ; aucune assistance humaine.

## Données fournies (source exacte)

> Réseau **fictif**, données **synthétiques à graine figée** réunies dans une base **SQLite**
> (`reseau.db`, 3 tables) → l'extraction se fait par **requêtes SQL** (C1.4), le nettoyage est
> exigé (C2.6). Aucune donnée personnelle réelle.

- **Fréquentation** (volet 1) : validations mensuelles par ligne 2022-2024, **pilotées par le vrai
  calendrier scolaire** (vacances zone B / Lille) → saisonnalité réaliste. Volontairement sale
  (libellés incohérents, valeurs manquantes, doublon). Équivalent réel : **transport.data.gouv.fr**.
- **Incidents** (volet 2) : ~800 signalements en texte libre, 4 types, avec cas ambigus.
- **Avis** (volet 3) : ~210 avis voyageurs (sentiment + thème), **prénoms à anonymiser** ; pièges
  d'ironie/négation réservés au test de robustesse. Équivalent réel : corpus **Allociné** (Hugging Face).

## Livrables attendus

**Un dépôt GitHub public**, gelé mardi 17 h de S23 :

1. `README.md` — présentation des trois volets, architecture, auteur.
2. `00-cadrage/note-cadrage.md` — les trois besoins reformulés, la priorisation retenue.
3. `01-frequentation/` — préparation, régression, projection de tendance, métriques, interprétation.
4. `02-incidents/` — préparation, classification, matrice de confusion, métriques.
5. `03-avis/` — collecte ou chargement, anonymisation, NLP, analyse de sentiments et thèmes.
6. `biais-et-limites.md` — **livrable transversal exigé** : pour chaque modèle, dimensions les plus utilisées, limites, biais potentiels.
7. `vulgarisation.md` — l'explication accessible des trois modèles.
8. `requetes/` — les extractions SQL des données sources.

**Support de soutenance** : libre.

## Critères de performance

**C3.1 — Statistiques descriptives**
• Les statistiques descriptives (variance, quantiles, coefficients de corrélation) sont utilisées pour expliquer les données des trois volets.

**C3.2 — Process ML**
• Le process de Machine Learning est utilisé et intégré à la modélisation (séparation, entraînement, prédiction, mesure), sans fuite.

**C3.3 — Régression**
• Les régressions supervisées sont modélisées et les métriques associées interprétées correctement.
• Une tendance future de fréquentation est produite et encadrée.

**C3.4 — Classification**
• Les classifications supervisées sont modélisées et les métriques associées interprétées correctement.
• Les incidents sont catégorisés automatiquement.

**C3.5 — NLP**
• Un corpus de texte est traité et catégorisé automatiquement grâce à des techniques de NLP.
• Le sentiment et les thèmes dominants des avis sont extraits.

**C3.6 — Biais**
• La documentation fait apparaître, pour chaque modèle, les dimensions les plus utilisées, les limites et les biais potentiels.

**C3.7 — Vulgarisation**
• L'algorithme d'apprentissage est expliqué et ses résultats interprétés, sans effet boîte noire.

**C1.4 / C2.6 — Revalidation**
• Les données sont extraites par requêtes et nettoyées de façon autonome.

**C4.8 — Restitution (niveau transposer)**
• La soutenance de 25 minutes est claire, structurée, adressée à un décideur, et répond aux questions communes.

## Ressources

- Dossier de cadrage et jeux de données : Remis par le formateur le lundi de S22
- scikit-learn — guide utilisateur : https://scikit-learn.org/stable/user_guide.html
- scikit-learn — interprétabilité et importance des variables : https://scikit-learn.org/stable/modules/permutation_importance.html
- transport.data.gouv.fr — données de mobilité : https://transport.data.gouv.fr/
- Google — introduction à l'équité des modèles : https://developers.google.com/machine-learning/fairness-overview
- Vos travaux B13 à B17 : Consultation autorisée
