# Brief B17 — Analyse de sentiments et audit éthique : du corpus scrapé à l'explication au client

## Informations

| | |
|---|---|
| **Semaine** | S21 · 15–19 fév 2027 · 5 jours · Guillaume |
| **Modalité · Évaluation** | Binôme · Sommatif |
| **Compétences visées** | C3.5 · C3.6 · C3.7 · C3.4 · C2.7 · C1.5 · C4.8 |

## Description

Une plateforme de réservation croule sous les avis clients. Vous constituez vous-mêmes le corpus par scraping, vous entraînez un modèle à en lire le sentiment — puis vous auditez ce qu'il a compris de travers, car un modèle entraîné sur des avis hérite des préjugés de ceux qui les ont écrits.

## Contexte

Une plateforme régionale de réservation d'activités de loisirs (visites, ateliers, sorties) collecte des milliers d'avis clients par mois. Ces avis sont une mine : ils disent ce qui plaît, ce qui déçoit, ce qui fait renoncer. Mais personne ne les lit en masse, et la note sur cinq étoiles ne suffit pas — un « 3 étoiles » peut cacher un enthousiasme nuancé comme une déception polie.

La responsable de l'expérience client veut savoir, automatiquement, si le sentiment exprimé dans un avis est positif, négatif ou mitigé, indépendamment de la note. Elle veut repérer les signaux faibles : les activités dont les avis se dégradent avant que la note ne baisse.

Vous allez d'abord constituer le corpus vous-mêmes. Le scraper que vous avez construit en B08 va resservir : vous collecterez les avis sur les pages publiques, en respectant le cadre légal que vous maîtrisez maintenant, et vous les anonymiserez (réactivation de B12) car un avis peut contenir le prénom d'un animateur ou d'un autre client.

Puis vous entraînerez un modèle à classer le sentiment. C'est la suite directe de votre première rencontre avec le NLP en B12 : cette fois vous ne vous contentez pas de mots-clés, vous entraînez un classifieur.

Et vous ferez ce que le référentiel exige et que trop de projets négligent : auditer les biais. Un modèle entraîné sur des avis apprend les préjugés de ceux qui les écrivent. Comprend-il mal l'ironie ? Classe-t-il systématiquement mal les avis rédigés dans un français approximatif ? Confond-il « pas cher » et négatif ? Vous le documenterez et l'expliquerez à la responsable, qui n'est pas technicienne.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C3.5** — Traiter automatiquement le langage naturel (NLP) à partir de texte brut afin d'en tirer de la valeur en fonction de classification (analyse de sentiments) *(niveau 2 — adapter)*
- **C3.6** — Contrôler et documenter les biais d'un modèle et des données d'entraînement *(niveau 2 — adapter)*
- **C3.7** — Communiquer et vulgariser le fonctionnement interne d'un algorithme *(niveau 2 — adapter)*
- **C3.4** — Modéliser des classifications et interpréter les métriques *(niveau 2 — adapter)*
- **C2.7** — Utiliser les expressions régulières / anonymisation *(niveau 3 — transposer)*
- **C1.5** — Automatiser des collectes par web scraping *(niveau 3 — transposer)*
- **C4.8** — Présenter à l'oral et à l'écrit *(niveau 2 — adapter)*

## Modalités pédagogiques

**Organisation** : binôme, dépôt commun.

**Jour 1 — matin (lancement, 2 h)**. Le formateur joue la responsable expérience client. Vous cadrez : quelles pages, quels avis, quel volume. Vous réactivez le scraper de B08.

**Jour 1 — après-midi**. Collecte du corpus et anonymisation (réactivation B12).

**Jour 2 — matin (apport flash, 2 h 30)**. NLP pour la classification : nettoyage, tokenisation, TF-IDF (rappel de B12), puis entraînement d'un classifieur de sentiment. Constitution d'un jeu étiqueté. Métriques adaptées.

**Jour 3 — matin (apport flash, 1 h 30)**. Audit de biais en NLP : sur quels types d'avis le modèle se trompe-t-il ? Erreurs sur l'ironie, la négation, les registres de langue. Vulgarisation d'un modèle de texte.

**Jours 2 à 4 — production**.
1. **Collecter** — le corpus d'avis, par scraping respectueux.
2. **Anonymiser** — retirer les données personnelles.
3. **Étiqueter** — constituez un jeu d'entraînement étiqueté (une partie des avis annotés à la main en sentiment).
4. **Classer** — entraînez un classifieur, évaluez-le (réactivation B16 : matrice de confusion, précision, rappel).
5. **Auditer** — cherchez systématiquement où le modèle se trompe. Formulez les biais.
6. **Vulgariser** — expliquez à la responsable comment le modèle décide et où lui faire confiance.

**Questions guidantes.** « Ce n'était pas mauvais » est-il positif ou négatif pour votre modèle ? Un avis ironique — « génial, deux heures d'attente » — est-il correctement classé ? Si le modèle classe mal les avis courts, est-ce grave pour l'usage visé ? Un jeu d'entraînement de 200 avis annotés par vous deux est-il représentatif, ou reflète-t-il votre propre subjectivité ? Comment dire à la responsable « faites confiance au modèle ici, mais pas là » ?

**Jour 4 — après-midi (revue croisée)**. Un autre binôme soumet à votre modèle dix avis pièges (ironie, négation, langue mêlée) et mesure ses échecs.

**Jour 5**. Finalisation, publication, restitution 8 minutes à la responsable non technicienne.

## Modalités d'évaluation

Brief **sommatif**, checklist complète.

Trois exigences pèsent également : le **NLP fonctionne** (le modèle classe et il est évalué correctement), les **biais sont audités** (pas seulement mentionnés — cherchés, illustrés, documentés), et l'**explication est accessible** à un non-technicien.

C3.6 et C3.7 passent ici au niveau adapter, entre leur introduction en B16 et leur niveau transposer au palier 3. Un binôme qui produit un bon classifieur sans audit de biais ne valide pas le brief : le référentiel lie explicitement modélisation et documentation des biais.

Ce brief revalide C1.5 et C2.7 au niveau transposer — la collecte et l'anonymisation ne sont plus l'objet du brief mais des acquis mobilisés au service d'autre chose.

## Données fournies (source exacte)

> Corpus **synthétique** (la plateforme est fictive) : aucun site public ne réunit avis en français
> **+ prénoms à anonymiser + pièges d'ironie/négation contrôlés**, les trois requis ici pour valider
> C1.5, C2.7 et C3.6.

- **Corpus** : ~577 avis générés à graine figée (`generer_corpus.py`), publiés en **pages HTML** que
  le scraper collecte comme des pages réelles. 17 **pièges** volontaires (ironie, négation, avis
  courts, registre familier) alimentent l'audit de biais.
- **Anonymisation** : les avis contiennent prénoms d'animateurs, e-mails et téléphones à masquer.
- **Équivalent réel** : le corpus **Allociné** (≈ 100 000 critiques FR, sentiment binaire, Hugging
  Face `datasets`) — réentraîne le même pipeline TF-IDF, mais sans PII ni scraping (ne valide donc ni
  C1.5 ni C2.7). https://huggingface.co/datasets/tblard/allocine

## Livrables attendus

**Un dépôt GitHub public** par binôme :

1. `README.md` — projet, chaîne complète, auteurs.
2. `01-collecte/scraper-avis.py` — la collecte (réemploi documenté de B08).
3. `01-collecte/anonymisation.py` — le retrait des données personnelles.
4. `02-nlp/classification.ipynb` — préparation, étiquetage, entraînement, évaluation.
5. `jeu-etiquete.csv` — le corpus annoté.
6. `audit-biais.md` — les cas d'échec identifiés, illustrés, classés par type de biais.
7. `note-responsable.md` — vulgarisation : comment le modèle décide, où lui faire confiance, où s'en méfier.

## Critères de performance

**C3.5 — NLP, niveau adapter**
• Le texte est préparé (nettoyage, tokenisation, vectorisation TF-IDF).
• Un classifieur de sentiment est entraîné sur un jeu étiqueté.
• Le corpus est catégorisé automatiquement et la répartition des sentiments est produite.

**C3.6 — Biais, niveau adapter**
• Les cas d'erreur du modèle sont recherchés systématiquement, pas seulement mentionnés.
• Au moins trois types de biais ou de faiblesse sont illustrés par des exemples réels.
• L'origine des biais (jeu d'entraînement, subjectivité de l'étiquetage) est discutée.

**C3.7 — Vulgarisation, niveau adapter**
• La note à la responsable explique le fonctionnement sans jargon.
• Elle indique explicitement où faire confiance au modèle et où s'en méfier.

**C3.4 — Réactivation, niveau adapter**
• Le modèle est évalué par matrice de confusion et métriques adaptées, pas par la seule justesse.

**C2.7 / C1.5 — Réactivation, niveau transposer**
• La collecte par scraping est autonome et respectueuse du cadre légal.
• L'anonymisation est effective et vérifiée.

**C4.8 — Restitution, niveau adapter**
• La restitution s'adresse à un public non technique et reste actionnable.

## Ressources

- scikit-learn — classification de texte : https://scikit-learn.org/stable/tutorial/text_analytics/working_with_text_data.html
- scikit-learn — TF-IDF : https://scikit-learn.org/stable/modules/feature_extraction.html#tfidf-term-weighting
- spaCy — modèles français : https://spacy.io/models/fr
- NLTK — analyse de sentiments : https://www.nltk.org/howto/sentiment.html
- Bac à sable scraping : https://books.toscrape.com/
- Comprendre les biais des modèles de NLP : https://developers.google.com/machine-learning/fairness-overview
