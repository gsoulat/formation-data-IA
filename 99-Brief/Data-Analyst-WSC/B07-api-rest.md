# Brief B07 — Brancher deux systèmes : API REST, format d'échange et repli sur extraction HTML

## Informations

| | |
|---|---|
| **Semaine** | S7 · 26–30 oct 2026 · 5 jours · Guillaume |
| **Modalité · Évaluation** | Binôme · Formatif |
| **Compétences visées** | C1.6 · C1.5 · C2.3 · C1.3 · C1.4 |

## Description

Une place de marché doit enrichir ses fiches produits avec des données publiques : adresses normalisées, données d'entreprise, météo. Trois API, trois logiques différentes. Et pour la quatrième source, il n'y a pas d'API du tout.

## Contexte

Terroir Direct met en relation 340 producteurs des Hauts-de-France avec des restaurateurs. Le catalogue en ligne fonctionne, mais les fiches producteurs sont incomplètes : adresses saisies à la main et souvent fausses, aucune information légale sur les exploitations, aucune donnée sur les conditions de récolte.

Le directeur technique a identifié trois sources publiques qui combleraient ces manques. La Base Adresse Nationale normaliserait les adresses et fournirait des coordonnées géographiques. L'API SIRENE donnerait la forme juridique, l'effectif et la date de création de chaque exploitation. Open-Meteo permettrait d'associer à chaque récolte les conditions météo réelles, argument commercial pour les restaurateurs.

Il vous confie le chantier avec une exigence qui l'obsède : « Le prochain développeur qui reprendra ce code ne doit pas avoir à deviner ce que renvoient ces API. Je veux que le format d'échange soit écrit noir sur blanc. » Il a été échaudé par un prestataire précédent dont le script fonctionnait sans que personne sache ce qu'il produisait.

Une quatrième source pose un problème différent. Un annuaire professionnel régional publie les labels et certifications des producteurs, mais ne propose aucune API : l'information n'existe que dans des pages web. En fin de semaine, vous découvrirez ce qu'on fait dans ce cas — et vous verrez pourquoi c'est à la fois la même chose et tout autre chose.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C1.6** — Mettre en place une interface standard de partage automatique de données entre différentes applications et langages (API REST) *(niveau 1 — imiter)*
- **C1.5** — Automatiser des collectes de données afin d'exploiter les contenus récoltés sur des pages web *(niveau 1 — imiter)*
- **C2.3** — Manipuler des structures de données et utiliser l'algorithmie *(niveau 2 — adapter)*
- **C1.3** — Modéliser des bases de données relationnelles *(niveau 2 — adapter)*
- **C1.4** — Réaliser des requêtes avancées *(niveau 2 — adapter)*

## Modalités pédagogiques

**Organisation** : binôme, dépôt commun.

**Jour 1 — matin (lancement, 2 h)**. Le formateur joue le directeur technique. Vous explorez les trois API à la main, dans le navigateur, avant d'écrire une ligne de code. Vous observez leurs différences : paramètres, structure de réponse, gestion des erreurs.

**Jour 1 — après-midi**. Vous tentez d'appeler une API depuis Python avec vos moyens. Vous butez sur la structure imbriquée du JSON.

**Jour 2 — matin (apport flash, 2 h)**. Le protocole HTTP : verbes, codes de statut, en-têtes. La bibliothèque `requests`. Le format JSON et son parcours en Python. Pagination, quotas, temporisation, gestion des échecs.

**Jour 4 — matin (apport flash, 1 h 30)**. Ce qu'on fait quand il n'y a pas d'API : structure d'une page HTML, sélecteurs, `BeautifulSoup`. Première extraction sur une page de démonstration. Le cadre légal sera traité en profondeur la semaine prochaine.

**Jours 2 à 4 — production**.
1. **Normaliser** — envoyez les adresses des 340 producteurs à la Base Adresse Nationale, récupérez adresse normalisée et coordonnées. Que faites-vous des adresses non reconnues ?
2. **Enrichir** — interrogez SIRENE à partir des numéros SIRET. Gérez les producteurs sans SIRET et les établissements fermés.
3. **Contextualiser** — récupérez les données météo aux coordonnées obtenues, sur une période de récolte donnée.
4. **Stocker** — insérez le tout dans une base relationnelle que vous modélisez.
5. **Documenter** — pour chaque API : point d'entrée, paramètres, structure de la réponse, champs retenus, comportement en cas d'erreur.
6. **Extraire (jeudi–vendredi)** — récupérez les labels depuis les pages de l'annuaire.

**Questions guidantes.** Que faire d'une adresse que la BAN ne reconnaît pas : l'écarter, la conserver telle quelle, la signaler ? Si l'API répond en 3 secondes et que vous avez 340 producteurs, combien de temps dure votre script, et est-ce acceptable ? Que se passe-t-il si l'API tombe à la 200ᵉ requête — recommencez-vous tout ? Un JSON imbriqué sur quatre niveaux doit-il être stocké tel quel ou aplati, et selon quel critère ?

**Jour 4 — après-midi (revue croisée)**. Un autre binôme lit votre documentation d'échange sans voir votre code, et doit prédire ce que renvoie votre script.

**Jour 5**. Finalisation, publication, restitution 8 minutes.

## Modalités d'évaluation

Brief **formatif**. Auto-évaluation, revue croisée, retour collectif.

Le critère structurant du référentiel pour cette compétence est explicite : « le format d'échange entre langage de programmation est précisé et documenté ». La revue croisée du jour 4 le teste directement — si un autre binôme ne peut pas prédire la sortie de votre script à partir de votre seule documentation, elle est insuffisante.

La partie extraction HTML n'est évaluée qu'au niveau imiter : reproduire une extraction simple sur une page fournie suffit. Elle sera reprise et approfondie en B08.

## Données fournies (source exacte)

> Les producteurs sont **réels** (Hauts-de-France) ; les API interrogées sont **publiques et sans clé**.

- **Liste** : `producteurs.csv` — 32 exploitations agricoles réelles (HdF), amorcées depuis l'API
  Recherche d'entreprises (colonnes : nom, siren, adresse_brute, code_postal, commune, coords du siège).
- **API** : Base Adresse Nationale (`api-adresse.data.gouv.fr`) · **Recherche d'entreprises**
  (`recherche-entreprises.api.gouv.fr` — données SIRENE **sans clé** ; l'API SIRENE officielle de
  l'INSEE exige une clé) · Open-Meteo (`archive-api.open-meteo.com`).
- **Repli scraping** (pas d'API) : `books.toscrape.com` (bac à sable légal ; le cadre juridique est approfondi en B08).

## Livrables attendus

**Un dépôt GitHub public** par binôme :

1. `README.md` — projet, sources, installation, lancement, auteurs.
2. `collecte/ban.py`, `collecte/sirene.py`, `collecte/meteo.py` — un module par source.
3. `collecte/labels.py` — l'extraction HTML de fin de semaine.
4. `docs/format-echange.md` — **le livrable central** : pour chaque API, point d'entrée, paramètres, exemple de réponse brute, table de correspondance champ API → champ base, comportement sur erreur et sur absence de résultat.
5. `sql/schema.sql` — le modèle de stockage.
6. `rapport-collecte.md` — volumétrie obtenue, taux de succès par source, cas non résolus et décision prise.

## Critères de performance

**C1.6 — API REST, niveau imiter**
• Les trois API sont interrogées par script et renvoient des données exploitables.
• Les codes de statut HTTP sont vérifiés ; un échec n'interrompt pas la collecte.
• Une temporisation ou une limitation de débit est mise en place et justifiée.
• `docs/format-echange.md` décrit pour chaque API : point d'entrée, paramètres, exemple de réponse, correspondance des champs.
• Le taux de succès est chiffré par source.

**C1.5 — Extraction web, niveau imiter**
• Une extraction fonctionnelle est réalisée sur les pages de l'annuaire.
• Au moins deux informations distinctes sont extraites par page.
• Le script gère l'absence d'un élément sans planter.

**C2.3 — Algorithmie, niveau adapter**
• Le code est organisé en modules, un par source.
• Les réponses JSON imbriquées sont parcourues correctement.
• Une fonction de traitement d'erreur est mutualisée.

**C1.3 / C1.4 — Réactivation**
• Le schéma de stockage comporte les contraintes d'intégrité adaptées.
• Une requête de contrôle vérifie la cohérence après insertion (comptages, orphelins).

## Ressources

- Base Adresse Nationale — API : https://adresse.data.gouv.fr/api-doc/adresse
- API SIRENE — documentation : https://www.sirene.fr/sirene/public/static/api-sirene
- Open-Meteo — documentation API : https://open-meteo.com/en/docs
- Requests — documentation : https://requests.readthedocs.io/fr/latest/
- BeautifulSoup — documentation : https://beautiful-soup-4.readthedocs.io/en/latest/
- MDN — codes de statut HTTP : https://developer.mozilla.org/fr/docs/Web/HTTP/Status
