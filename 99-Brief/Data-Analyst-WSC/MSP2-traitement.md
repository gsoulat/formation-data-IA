# Brief MSP2 — Moteur de traitement réutilisable : ingérer, nettoyer et anonymiser des données

## Informations

| | |
|---|---|
| **Semaine** | S15 (4–8 janv, 5 j) + S16 (11–15 janv, 5 j) · Guillaume & Ayoub · 10 jours |
| **Modalité · Évaluation** | INDIVIDUEL · CERTIFICATIF — évaluation individuelle par un examinateur |
| **Compétences visées** | C2.1 · C2.2 · C2.3 · C2.4 · C2.5 · C2.6 · C2.7 · C1.4 · C1.6 · C4.8 |

## Description

Mise en situation professionnelle du bloc 2. Une association nationale reçoit des données de terrain dans tous les formats et par toutes les voies. Vous concevez le moteur unique qui les ingère, les nettoie, les anonymise et les rend exploitables — un outil, pas un script jetable.

## Contexte

L'association Solidarité Grand Âge fédère 140 structures locales — maisons de retraite associatives, services d'aide à domicile, accueils de jour. Chaque structure remonte mensuellement ses données d'activité au siège national : nombre de bénéficiaires, actes réalisés, incidents, satisfaction.

Le problème est un condensé de tout ce que vous avez rencontré depuis huit semaines. Les 140 structures envoient leurs données par des voies différentes : certaines déposent un fichier dans un espace partagé, d'autres alimentent une petite base commune, quelques-unes exposent leur logiciel métier via une API. Les formats sont hétérogènes. La qualité est inégale : manquants, aberrations, doublons. Et surtout, ces fichiers contiennent des données personnelles de personnes âgées vulnérables — noms, adresses, informations de santé — que le RGPD protège avec une exigence renforcée.

La directrice des systèmes d'information du siège a une vision claire : « Je ne veux plus qu'on bricole chaque mois. Je veux un outil qu'on lance, qui va chercher les données où qu'elles soient, qui les nettoie, qui les anonymise, et qui produit un jeu exploitable. Et je veux qu'un nouveau salarié puisse le reprendre. »

C'est la mise en situation du bloc 2 : vous ne traitez pas un fichier, vous construisez l'outil qui traitera tous les fichiers. Il devra ingérer une base SQL et un flux API — ce qui revalide votre bloc 1 — puis nettoyer et anonymiser selon des choix méthodologiques que vous devrez documenter et défendre devant un examinateur.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C2.1** — Effectuer des choix méthodologiques pour l'automatisation des traitements et les documenter avec clarté et concision *(niveau 3 — transposer)*
- **C2.2** — Utiliser les outils et méthodes modernes : méthodes agiles, outils de suivi de projets, logiciel adapté à la rédaction de code *(niveau 3 — transposer)*
- **C2.3** — Manipuler des structures de données et utiliser l'algorithmie afin de traduire en script des besoins de traitement *(niveau 3 — transposer)*
- **C2.4** — Appliquer les bonnes pratiques de la programmation : code organisé, réutilisable et partageable *(niveau 3 — transposer)*
- **C2.5** — Utiliser les tableaux de données (DataFrames avec Python et Pandas) *(niveau 3 — transposer)*
- **C2.6** — Nettoyer les données, retraiter les valeurs aberrantes et les valeurs manquantes *(niveau 3 — transposer)*
- **C2.7** — Utiliser les expressions régulières pour traiter les valeurs textuelles et permettre une anonymisation RGPD *(niveau 3 — transposer)*
- **C1.4** — Réaliser des requêtes avancées *(niveau 3 — transposer)*
- **C1.6** — Mettre en place une interface standard de partage automatique de données *(niveau 3 — transposer)*
- **C4.8** — Présenter à l'oral et à l'écrit *(niveau 2 — adapter)*

## Modalités pédagogiques

**Organisation** : strictement individuel. Les compétences ont toutes été travaillées de B06 à B12.

**Aucun apport formel.** Le formateur intervient uniquement pour clarifier le besoin.

**Semaine 1 — S15 (5 jours, production)**
- **Lundi** : appropriation du besoin (entretien de cadrage de 20 min avec le formateur en directrice SI), architecture de l'outil, prise en main des sources. *Une courte remise en route est tolérée le lundi matin après les congés.*
- **Mardi à jeudi** : développement du moteur — ingestion multi-sources, nettoyage, anonymisation.
- **Vendredi** : documentation, tests, structuration du dépôt.

**Semaine 2 — S16 (5 jours, finalisation et soutenance)**
- **Lundi, mardi** : robustesse, cas limites, finalisation de la documentation. Gel des livrables mardi 17 h.
- **Mercredi, jeudi** : préparation des soutenances, revue de son propre code.
- **Vendredi** : soutenances individuelles de 20 minutes devant examinateur.

**Attendus de la soutenance.** Vous présentez votre outil à la directrice SI. Trois questions communes : quel choix méthodologique de nettoyage avez-vous le plus hésité à trancher, et comment l'avez-vous tranché ? comment un nouveau salarié reprendrait-il votre outil ? comment garantissez-vous qu'aucune donnée personnelle ne sort du moteur ?

**Cadre référentiel.** Les candidats doivent, à partir d'objectifs définis de traitement, structurer des outils et utiliser des algorithmes afin de manipuler des tableaux de données, et automatiser le nettoyage — notamment des valeurs manquantes et aberrantes. Les objectifs sont fournis dans le dossier de cadrage du lundi de S15.

## Modalités d'évaluation

**Mise en situation professionnelle certificative du bloc 2**, évaluée individuellement par un examinateur.

**Deux temps.** Dossier (gelé mardi 17 h de S16) et soutenance individuelle (vendredi, 20 min).

**Validation** : compétence acquise = 100 % de ses critères. Bloc acquis = les sept compétences C2.

**Revalidation du bloc 1** : ce palier remobilise C1.4 (extraction depuis la base source) et C1.6 (ingestion du flux API) au niveau 3. Une compétence du bloc 1 non acquise au palier 1 peut être rattrapée ici.

**Rattrapage aval** : C1.4 sera de nouveau remobilisé au palier 3, l'ensemble au palier 4.

**Conditions** : internet, documentation et travaux antérieurs autorisés ; aucune assistance humaine.

## Données fournies (source exacte)

> Sources **mixtes** : base SQL et fichiers **synthétiques** (données de personnes vulnérables →
> hors open data) ; le flux API utilise une source **réelle** ouverte.

- **Base commune** : `data/base_structures.db` (SQLite) — remontées de 30 structures × 3 mois, avec
  responsable/commentaire (données personnelles) et défauts de qualité (manquants, aberrations).
- **Fichiers déposés** : `depots/structures_A.csv` (UTF-8, virgule) et `structures_B.csv`
  (Latin-1, `;`, décimale virgule) — colonnes différentes.
- **Flux API** : `recherche-entreprises.api.gouv.fr` (ouverte) pour le référentiel des structures.
- **Reproduction** : `python3 generer_donnees.py`.

## Livrables attendus

**Un dépôt GitHub public**, gelé mardi 17 h de S16 :

1. `README.md` — présentation de l'outil, architecture, installation, lancement, auteur.
2. `docs/objectifs.md` — les objectifs de traitement reformulés depuis le dossier de cadrage.
3. `src/ingestion/` — modules de collecte : lecteur de fichiers, client SQL, client API.
4. `src/nettoyage/` — modules de nettoyage : manquants, aberrations, uniformisation.
5. `src/anonymisation/` — le module RGPD par RegEx.
6. `src/pipeline.py` — l'orchestration, du point d'entrée à la sortie.
7. `docs/choix-methodologiques.md` — chaque décision de traitement, son alternative, sa justification.
8. `docs/gestion-projet.md` — les outils et méthodes de suivi employés (board, historique, conventions).
9. `tests/` — les tests des fonctions critiques.
10. `sortie/jeu-exploitable.csv` + `sortie/rapport-traitement.md` — résultat et bilan chiffré.
11. `docs/registre-rgpd.md` — traitement des données personnelles.

## Critères de performance

**C2.1 — Choix méthodologiques**
• La documentation est présente, correspond aux traitements développés et explique les choix méthodologiques effectués.

**C2.2 — Outils et méthodes**
• Les outils et méthodes de gestion de projet sont présentés (board, historique de commits structuré, conventions).

**C2.3 — Algorithmie**
• L'algorithmie Python, notamment la création de fonctions avancées et optimisées, est utilisée pour l'automatisation des retraitements.

**C2.4 — Clean code**
• Les principes du clean code (PEP 8) sont respectés sur l'ensemble du dépôt.

**C2.5 — Pandas**
• Les traitements et transformations sont effectués, optimisés et automatisés grâce à pandas.

**C2.6 — Nettoyage**
• Le retraitement des valeurs aberrantes et manquantes est effectué et argumenté sur la méthodologie employée.

**C2.7 — RegEx / anonymisation**
• Les expressions régulières sont correctement utilisées pour identifier des formats de valeurs textuelles et permettre une anonymisation.

**C1.4 — Requêtes (revalidation)**
• L'extraction depuis la base source s'appuie sur des requêtes correctes et performantes.

**C1.6 — API (revalidation)**
• Le flux API est ingéré et automatisé ; le format d'échange reste documenté.

**C4.8 — Restitution (niveau adapter)**
• La soutenance présente l'outil à un public non technique et répond aux trois questions communes.

## Ressources

- Dossier de cadrage et sources : Remis par le formateur le lundi de S15
- pandas — documentation : https://pandas.pydata.org/docs/
- pytest — écrire des tests : https://docs.pytest.org/
- PEP 8 : https://peps.python.org/pep-0008/
- CNIL — anonymisation : https://www.cnil.fr/fr/lanonymisation-des-donnees-un-traitement-cle-pour-lopen-data
- Vos travaux B06 à B12 : Consultation autorisée
