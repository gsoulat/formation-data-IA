# Mini-brief 2 : Exposer un catalogue — API REST, rôles et quota d'appel

## Informations

| Critère | Valeur |
|---------|--------|
| **Durée** | 3 jours (21 heures) — **J3 à J5** d'une semaine de 5 jours |
| **Niveau** | Débutant-Intermédiaire |
| **Modalité** | Individuel |
| **Technologies** | Python, FastAPI, Pydantic, PostgreSQL, Docker, Git |
| **Prérequis** | [Cours FastAPI](../../../01-Fondamentaux/Python/08-FastAPI/) + [Cours Docker](../../../02-Containerisation/Docker/) |
| **Amont** | [Mini-brief 1 — Scraping](../Bouquineo-Scraping/BRIEF_SCRAPING.md), réalisé en J1-J2 : vous exposez le catalogue que vous avez collecté. |

## Compétences visées

- **C12.** Partager le jeu de données en développant une API REST ou en configurant un accès direct afin de permettre l'exploitation du jeu de données par les autres composants du projet.
  → **Niveau 3 — TRANSPOSER.** Aucun squelette d'API n'est fourni. Le cours FastAPI couvre l'authentification et les rôles, mais le **quota d'appel n'est traité nulle part dans le parcours** : cette partie est conçue en autonomie complète.
- **C21.** Implémenter les règles de gouvernance des données en configurant les contrôles d'accès, les politiques de rétention et les procédures de qualité afin d'assurer la conformité réglementaire et la fiabilité des données.
  → **Niveau 2 — ADAPTER.** Limité au volet « contrôles d'accès » : séparation public/protégé, rôles, habilitations. Rétention et qualité hors périmètre.

## Contexte

Le catalogue du concurrent est en base — vous l'y avez mis avant-hier. Trois personnes chez **Bouquineo** en ont besoin, et aucune ne sait écrire une requête SQL.

L'équipe commerciale veut consulter les prix et les stocks depuis son propre outil. La responsable des achats veut **corriger** les données : le scraper se trompe parfois de catégorie, et elle veut pouvoir ajouter à la main des titres repérés en salon que le concurrent ne référence pas encore. La direction, elle, veut ouvrir une partie du catalogue à un partenaire extérieur — sans lui donner accès aux informations commerciales internes, ni lui laisser la possibilité de saturer le service.

Vous exposez donc le catalogue derrière une **API REST**. Le sujet n'est pas d'écrire quatre routes : c'est de décider **qui a le droit de faire quoi**, et de tenir cette décision.

> **La question centrale** :
>
> **« Comment ouvrir le catalogue à des consommateurs aux droits différents, sans exposer ce qui doit rester interne ni laisser un appelant dégrader le service pour les autres ? »**

### Le renversement de perspective

Dans le mini-brief 1, vous avez envoyé mille requêtes à un serveur qui ne vous avait rien demandé. Vous étiez le client, et c'est vous qui deviez vous montrer raisonnable.

Vous passez maintenant de l'autre côté. C'est votre service qui encaisse, et c'est à vous de vous protéger d'un client qui ne se modérera pas. Gardez en tête, en concevant votre limite, ce que vous auriez voulu que le serveur vous dise quand vous étiez à sa porte.

## Ce qui vous est fourni

- Votre base issue du mini-brief 1, et un `docker-compose.yml` de départ dans [`starter-kit/`](starter-kit/).

**Si votre collecte est incomplète, ce n'est pas bloquant.** Ce mini-brief ne réévalue pas le scraping, et il ne réclame nulle part les 1 000 livres : quelques centaines de lignes correctement structurées suffisent à construire et démontrer l'API. Si vous n'avez vraiment rien en base, recollectez deux ou trois catégories avec votre scraper de J1-J2 — une demi-heure — et passez à la suite.

Aucun squelette d'API n'est fourni : c'est le sujet du mini-brief.

## Travail demandé

Travail individuel sur 3 jours, enchaînés au mini-brief 1 dans la même semaine.

> **Ordre imposé.** Traitez dans cet ordre : CRUD d'abord, puis public/protégé et authentification, puis rôles, puis quota. Chaque étape s'appuie sur la précédente. Une API dont le CRUD et l'authentification tiennent vaut mieux qu'une API complète sur le papier dont rien ne marche en démonstration.

### Phase 1 — CRUD complet et modèle d'accès (J3)

Commencez par les quatre opérations sur les livres, sans aucune protection : lecture en liste et en détail, création, modification, suppression. Validez les entrées avec des schémas Pydantic plutôt qu'à la main — un prix négatif, une note à 7 sur 5 ou un UPC absent doivent être refusés avant d'atteindre la base, avec un message qui dit quel champ est fautif.

La liste doit être **paginée** dès maintenant. Mille livres renvoyés d'un bloc, c'est le genre de route qui met un service à genoux tout seul. Quelle taille de page par défaut, et surtout quelle taille maximale acceptez-vous si l'appelant la réclame ?

Réfléchissez ensuite à ce que « supprimer » veut dire ici. Le catalogue est re-scrapé chaque semaine : un livre effacé physiquement reviendra au prochain passage. Suppression logique ou physique, et pourquoi ?

Terminez la journée en écrivant votre **modèle d'accès** dans `docs/api.md`, avant de l'implémenter. Trois profils : un appelant **anonyme**, un **gestionnaire**, un **administrateur**. Pour chaque route, qui y a droit ? Deux principes vous guident. Le catalogue provient d'un site public : rien ne justifie d'en protéger la lecture. En revanche les champs commerciaux que Bouquineo ajoute — prix d'achat, marge, fournisseur, stock interne — n'ont aucune raison de sortir, et **personne d'anonyme n'écrit dans votre base**.

**Résultat testable en fin de J3 :** les quatre opérations fonctionnent, la liste est paginée et bornée, les entrées invalides sont refusées avec un message exploitable, et le modèle d'accès est écrit.

### Phase 2 — Authentification, rôles et persistance des corrections (J4)

Implémentez le modèle décidé hier. Le mécanisme est votre choix — clé d'API dans un en-tête, ou jeton JWT — mais justifiez-le dans le README ; le [cours FastAPI](../../../01-Fondamentaux/Python/08-FastAPI/06-authentification.md) couvre les deux ainsi que les rôles.

Où posez-vous le contrôle : sur chaque fonction, ou au niveau du routeur ? La seconde option protège par construction les routes que vous ajouterez ensuite, et c'est exactement le genre d'oubli qui produit une fuite. Un appelant non identifié et un appelant identifié mais de rôle insuffisant reçoivent-ils la même réponse — et savez-vous dire pourquoi 401 et 403 ne sont pas interchangeables ? Vérifiez aussi qu'une route de lecture protégée ne laisse pas fuiter un champ interne dans sa version publique : c'est le schéma de réponse qui décide de ce qui sort, pas l'objet chargé depuis la base.

L'après-midi, attaquez le vrai problème d'ingénierie de ce mini-brief : **que devient une correction manuelle au prochain passage du scraper ?**

La responsable des achats corrige mardi la catégorie d'un livre via votre API. Le scraper tourne mercredi et recharge le catalogue. Si votre chargement écrase la table, la correction a disparu, et votre API est devenue un piège à confiance. Comment distinguez-vous une valeur venue du scraper d'une valeur saisie par un humain ? Marquez-vous la ligne ou le champ, tenez-vous les corrections dans une table à part réappliquée après chaque chargement, ou passez-vous en `upsert` préservant certains champs ? Et le livre ajouté à la main, que le concurrent ne référence pas : comment survit-il à un rechargement qui ne le contient pas ?

Quelle que soit votre réponse, elle est écrite, justifiée et **démontrable**.

**Résultat testable en fin de J4 :** un appel anonyme aboutit en lecture publique et est refusé en écriture ; un gestionnaire écrit ; les champs internes ne sortent jamais sans authentification ; une correction saisie via l'API survit à un rechargement du catalogue.

### Phase 3 — Quota d'appel, documentation et démonstration (J5)

Cette partie n'est couverte par aucun cours du parcours — vous la concevez seul.

Fixez une limite par appelant et par fenêtre de temps, différenciée selon le rôle : un anonyme n'a pas les mêmes droits de charge qu'un gestionnaire authentifié. Sur quoi comptez-vous, l'adresse IP ou la clé de l'appelant, et que faites-vous des anonymes derrière une même adresse ? Où logent vos compteurs, et survivent-ils au redémarrage du conteneur ?

Soignez surtout ce que voit celui qui dépasse, car c'est là que se joue la différence entre une API pénible et une API exploitable. Le bon comportement est connu : un code **429**, un en-tête `Retry-After` qui dit combien de temps patienter, et des en-têtes annonçant la limite et le solde restant, pour que le client se régule **avant** d'être bloqué. Beaucoup d'API publiques font l'inverse et renvoient un 200 avec l'échec enfoui dans le corps de la réponse ; un client naïf enregistre alors du vide sans qu'aucune alerte ne se déclenche. Vous avez été ce client il y a trois jours — ne reproduisez pas le piège.

Exposez enfin la **documentation OpenAPI** générée par FastAPI, et vérifiez qu'elle décrit les codes d'erreur et le schéma de sécurité. Le test est simple : un intégrateur extérieur doit pouvoir appeler votre API sans vous poser une seule question.

Finissez par le clone propre — effacez, reclonez, déroulez votre README — puis préparez la démonstration.

**Résultat testable en fin de J5 :** une rafale d'appels déclenche un 429 accompagné d'un `Retry-After` exploitable ; les quotas diffèrent selon le rôle ; la documentation OpenAPI est accessible et complète ; toute la pile se lance par une commande unique.

## Socle commun (obligatoire)

- CRUD complet sur les livres, avec validation des entrées et liste paginée bornée.
- Séparation explicite des routes et des champs publics et protégés.
- Authentification fonctionnelle et trois rôles effectifs.
- Quota d'appel différencié par rôle, renvoyant 429 et `Retry-After`.
- Mécanisme de persistance des corrections face à un rechargement, documenté et démontrable.
- Documentation OpenAPI accessible, README, `docs/api.md`.

## Livrables

À rendre en fin de J5 (lien du repo posté sur la plateforme) :

- Un **repo GitHub public** avec README : description, technologies et justification, lancement de la pile depuis zéro, obtention d'un accès de test, auteur.
- Le **code de l'API** : routes, schémas de validation, dépendances d'authentification et de contrôle de rôle, mécanisme de quota — avec un historique de commits réparti sur les trois jours (J3 à J5).
- **`docs/api.md`** : le tableau des routes avec, pour chacune, sa méthode, le rôle minimal requis et son quota ; le mécanisme d'authentification retenu et sa justification ; et la **note sur la persistance des corrections**, avec la solution retenue et pourquoi.
- La **spécification OpenAPI** exportée (`openapi.json`) ou l'URL de la documentation interactive dans le README.
- Le **fichier de composition** permettant de lancer base et API ensemble, et un `.env.example` sans aucun secret réel.

## Évaluation

**Démonstration technique (70 %).** 15 minutes de démonstration + 10 minutes de questions. Vous appelez une route publique en anonyme, puis une route protégée qui vous refuse, puis la même en gestionnaire. Vous déroulez le CRUD. Vous corrigez un livre, relancez le chargement du catalogue, et montrez que la correction a survécu. Vous terminez par une rafale d'appels jusqu'au 429, en commentant les en-têtes renvoyés.

**Revue de code et de conception (30 %).** Structure du code, placement du contrôle d'accès, qualité de `docs/api.md` et de la documentation OpenAPI, pertinence du modèle d'accès, régularité des commits.

> **Validation partielle** : une API dont le CRUD et l'authentification fonctionnent, structurée et documentée, valide partiellement même si le quota est incomplet. Une démonstration réussie sans documentation ne valide pas les critères documentaires.

## Critères de validation

### Partage du jeu de données via une API REST

- L'API est fonctionnelle et toute la pile se lance par une commande unique documentée.
- Les quatre opérations CRUD aboutissent effectivement ; les entrées invalides sont rejetées avant la base, avec le champ fautif identifié.
- La liste est paginée et sa taille de page est bornée côté serveur.
- La documentation OpenAPI est accessible et décrit les routes, les codes d'erreur et le schéma de sécurité.

### Contrôle d'accès

- La séparation entre routes publiques et protégées est explicite et documentée dans `docs/api.md`.
- Aucun champ commercial interne n'est accessible sans authentification, y compris via une route de lecture publique.
- L'authentification fonctionne et le contrôle de rôle est effectif : appel anonyme sur route protégée refusé, rôle insuffisant refusé, et les codes 401 et 403 sont distingués à bon escient.
- Le contrôle est posé de façon à couvrir par construction les routes ajoutées ultérieurement.

### Quota d'appel

- Le quota est effectif et différencié selon le rôle.
- Un dépassement renvoie un code 429 accompagné d'un en-tête `Retry-After` exploitable par le client.
- L'assiette du comptage (adresse ou clé d'appelant) et le lieu de stockage des compteurs sont justifiés dans la documentation.

### Persistance des corrections

- Le mécanisme est implémenté, documenté et démontré en direct : une correction saisie via l'API survit à un rechargement du catalogue.
- Le sort d'un livre ajouté manuellement, absent du jeu rechargé, est traité et justifié.

## Ressources

- [Cours FastAPI](../../../01-Fondamentaux/Python/08-FastAPI/) — dont [authentification, JWT et rôles](../../../01-Fondamentaux/Python/08-FastAPI/06-authentification.md)
- [Cours Docker](../../../02-Containerisation/Docker/)
- FastAPI — Sécurité et dépendances : https://fastapi.tiangolo.com/tutorial/security/
- MDN — Code de statut HTTP 429 Too Many Requests : https://developer.mozilla.org/fr/docs/Web/HTTP/Status/429
- MDN — En-tête HTTP `Retry-After` : https://developer.mozilla.org/fr/docs/Web/HTTP/Headers/Retry-After
- SlowAPI — limitation de débit pour FastAPI (une piste parmi d'autres) : https://slowapi.readthedocs.io/
- Spécification OpenAPI : https://swagger.io/specification/
