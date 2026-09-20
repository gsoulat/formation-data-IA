# Brief B12 — Tickets support : anonymiser par RegEx, puis catégoriser automatiquement

## Informations

| | |
|---|---|
| **Semaine** | S14 · 14–18 déc 2026 · 5 jours · Ayoub |
| **Modalité · Évaluation** | Binôme · Sommatif |
| **Compétences visées** | C2.7 · C2.6 · C3.5 · C1.7 · C4.8 |

## Description

Un service client veut analyser 8 000 tickets pour comprendre ce qui fait souffrir ses usagers. Impossible tant qu'ils contiennent des noms, des IBAN, des adresses. Vous les anonymisez d'abord — puis vous découvrez que la machine peut deviner de quoi parle un ticket.

## Contexte

Une mutuelle santé de taille moyenne reçoit environ 8 000 demandes écrites par mois via son formulaire de contact : réclamations, questions de remboursement, changements de situation, résiliations. Le service qualité aimerait analyser ce flux pour identifier les motifs récurrents d'insatisfaction et prioriser les chantiers d'amélioration.

Deux obstacles se dressent. Le premier est juridique : ces messages sont truffés de données personnelles. Noms, prénoms, numéros de sécurité sociale, IBAN pour les remboursements, adresses postales, numéros de téléphone. Aucune analyse ne peut commencer avant que ces données soient retirées — le délégué à la protection des données de la mutuelle y veillera.

Le second est volumétrique : personne ne va lire 8 000 messages par mois pour les classer à la main. Le service qualité classe aujourd'hui un échantillon de 200 tickets, ce qui ne représente rien.

Votre mission se déroule donc en deux temps qui s'enchaînent naturellement. D'abord, anonymiser : construire un traitement qui repère et neutralise les données personnelles par expressions régulières — c'est le prolongement direct de ce que vous avez fait la semaine dernière sur le registre patients. Ensuite, découvrir que le texte anonymisé peut être exploité : une fois nettoyé, un corpus peut être catégorisé automatiquement selon son thème. C'est votre première rencontre avec le traitement automatique du langage — et elle naît, logiquement, du nettoyage de texte que vous savez déjà faire.

Vous présenterez le résultat au délégué à la protection des données, qui validera l'anonymisation, et au service qualité, qui jugera de l'utilité de la catégorisation.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C2.7** — Utiliser les expressions régulières (RegEx) pour traiter les valeurs textuelles et permettre une anonymisation des données personnelles dans le cadre du RGPD *(niveau 2 — adapter)*
- **C2.6** — Nettoyer les données, retraiter les valeurs aberrantes et manquantes *(niveau 2 — adapter)*
- **C3.5** — Traiter automatiquement le langage naturel (NLP) à partir de texte brut afin d'en tirer de la valeur en fonction de classification *(niveau 1 — imiter)*
- **C1.7** — Contrôler les enjeux du RGPD *(niveau 3 — transposer)*
- **C4.8** — Présenter à l'oral et à l'écrit *(niveau 2 — adapter)*

## Modalités pédagogiques

**Organisation** : binôme, dépôt commun.

**Jour 1 — matin (lancement, 2 h)**. Le formateur joue le responsable qualité et le DPO. Vous recevez un corpus de tickets. Première tâche : recensez tous les types de données personnelles présents, avec des exemples.

**Jour 1 — après-midi**. Vous commencez à écrire les expressions régulières d'anonymisation, en réactivant B11.

**Jour 2 — matin (apport flash, 1 h 30)**. RegEx avancées : IBAN, numéros de sécurité sociale, formats de téléphone multiples, noms précédés d'une civilité. Stratégies de remplacement : masquage, pseudonymisation, substitution par un jeton typé (`[NOM]`, `[IBAN]`).

**Jour 3 — matin (apport flash, 2 h)**. Introduction au NLP : nettoyage de texte (minuscules, ponctuation, mots vides), tokenisation, sac de mots et TF-IDF. Association d'un ticket à un thème par mots-clés pondérés, puis par un classifieur simple.

**Jours 2 à 4 — production**.
1. **Anonymiser** — traitement qui neutralise toutes les catégories de données personnelles recensées. Le DPO exigera un taux de couverture, pas une intention.
2. **Vérifier** — comment prouvez-vous qu'il ne reste rien ? Construisez un contrôle.
3. **Préparer** — nettoyez le texte anonymisé pour l'analyse.
4. **Catégoriser** — associez chaque ticket à un thème parmi une liste que vous définissez (remboursement, résiliation, réclamation, changement de situation, autre). Par mots-clés d'abord, par classifieur ensuite si vous y arrivez.
5. **Restituer** — au service qualité : quels thèmes dominent, lesquels progressent.

**Questions guidantes.** Une expression régulière qui capture 95 % des IBAN est-elle acceptable pour un DPO, ou faut-il 100 %, et à quel prix ? Un prénom courant comme « Rose » est-il un nom de personne ou une couleur — comment traiter l'ambiguïté ? Anonymiser, est-ce supprimer ou remplacer, et qu'est-ce qui change pour l'analyse ensuite ? Un thème « autre » qui capte 40 % des tickets est-il un échec de classification ou une information ?

**Jour 4 — après-midi (revue croisée)**. Un autre binôme joue le DPO et cherche une donnée personnelle que votre traitement a laissé passer.

**Jour 5**. Finalisation, publication, double restitution 8 minutes : validation DPO puis utilité qualité.

## Modalités d'évaluation

Brief **sommatif**, checklist complète.

L'anonymisation (C2.7, C1.7) est la partie critique et non négociable : un traitement qui laisse passer des données personnelles ne valide pas le brief, quelle que soit la qualité de la catégorisation. Le contrôle de couverture est aussi important que le traitement lui-même.

Le NLP (C3.5) est évalué au **niveau imiter** : une catégorisation par mots-clés fonctionnelle suffit. Le classifieur entraîné est un bonus, approfondi en B17. L'enjeu de la semaine est de faire naître le NLP du nettoyage de texte, pas de produire un modèle sophistiqué.

## Données fournies (source exacte)

> Corpus de tickets **100 % synthétique** (santé + données personnelles → hors open data), reproductible.

- **Fichier** : `data/tickets_bruts.csv` — 2 000 tickets d'une mutuelle santé, chacun combinant un
  message thématique et des données personnelles injectées (nom, IBAN, n° de sécurité sociale,
  téléphone, e-mail, adresse). `data/pii_injectees.json` donne le compte injecté par catégorie
  (base du contrôle de couverture).
- **Reproduction** : `python3 generer_tickets.py`.

## Livrables attendus

**Un dépôt GitHub public** par binôme :

1. `README.md` — projet, méthode, installation, auteurs.
2. `inventaire-donnees-personnelles.md` — les catégories recensées le jour 1, avec exemples.
3. `anonymisation/anonymiseur.py` — le traitement RegEx, une fonction par catégorie de donnée.
4. `anonymisation/controle-couverture.md` — la méthode de vérification et le taux atteint par catégorie.
5. `nlp/categorisation.py` — le nettoyage de texte et la catégorisation.
6. `sortie/tickets-anonymises.csv` — le corpus traité.
7. `rapport-qualite.md` — répartition des thèmes, thèmes dominants, lecture pour le service qualité.

## Critères de performance

**C2.7 — RegEx / anonymisation, niveau adapter**
• Toutes les catégories de données personnelles recensées sont traitées par RegEx.
• Le remplacement se fait par jeton typé, préservant l'analysabilité du texte.
• Un taux de couverture est mesuré et présenté par catégorie.
• Les expressions complexes (IBAN, n° de sécurité sociale) sont fonctionnelles et commentées.

**C2.6 — Nettoyage, niveau adapter**
• Le texte est préparé pour l'analyse : casse, ponctuation, mots vides traités.
• Les tickets vides ou inexploitables sont détectés et écartés avec trace.

**C3.5 — NLP, niveau imiter**
• Chaque ticket est associé à un thème d'une liste définie.
• La méthode (mots-clés pondérés au minimum) est explicitée.
• La répartition des thèmes est chiffrée et représentée.

**C1.7 — RGPD, niveau transposer**
• Le contrôle de couverture démontre l'efficacité de l'anonymisation.
• Aucune donnée personnelle détectable ne subsiste dans l'échantillon vérifié par la revue croisée.
• La stratégie (masquage / pseudonymisation) est justifiée au regard de l'usage.

**C4.8 — Restitution, niveau adapter**
• La restitution DPO démontre l'anonymisation par des preuves, pas par des affirmations.
• La restitution qualité présente une lecture actionnable des thèmes.

## Ressources

- Python — module re : https://docs.python.org/fr/3/library/re.html
- regex101 — testeur en ligne : https://regex101.com/
- CNIL — anonymisation et pseudonymisation : https://www.cnil.fr/fr/lanonymisation-des-donnees-un-traitement-cle-pour-lopen-data
- scikit-learn — extraction de caractéristiques de texte (TF-IDF) : https://scikit-learn.org/stable/modules/feature_extraction.html#text-feature-extraction
- NLTK — liste de mots vides français : https://www.nltk.org/
- spaCy — traitement du français : https://spacy.io/models/fr
