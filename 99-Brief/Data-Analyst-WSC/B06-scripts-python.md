# Brief B06 — Automatiser un contrôle qualité : premiers scripts Python documentés

## Informations

| | |
|---|---|
| **Semaine** | S6 · 19–23 oct 2026 · 5 jours · Ayoub |
| **Modalité · Évaluation** | Individuel · Formatif |
| **Compétences visées** | C2.3 · C2.1 · C2.4 · C1.4 · C4.5 |

## Description

Chaque matin, un opérateur vérifie à la main 900 lignes de bons de commande. Il y passe deux heures et rate des erreurs. Vous écrivez le script qui le remplace — et vous documentez chacun de vos choix, car c'est lui qui devra le comprendre.

## Contexte

Nord Logistique exploite une plateforme de 12 000 m² près de Lesquin. Chaque nuit, ses clients déposent leurs bons de commande sur un serveur : un fichier CSV par client, une trentaine de fichiers, 900 lignes au total.

Chaque matin à 6 h, Damien, préparateur référent, ouvre ces fichiers un par un et vérifie. Les quantités négatives, les codes produits inexistants, les dates de livraison passées, les lignes tronquées, les séparateurs qui changent d'un client à l'autre. Il y passe environ deux heures. Il en rate — la semaine dernière, une commande de 1 200 unités saisie au lieu de 12 a bloqué une allée entière.

Damien n'est pas informaticien et ne le sera pas. Il a formulé sa demande simplement : « Je veux arriver le matin, lancer un truc, et avoir la liste de ce qui cloche. » Le responsable d'exploitation ajoute une condition : « Et je veux qu'on puisse le modifier quand un client change son format, sans rappeler celui qui l'a écrit. »

C'est votre première semaine de programmation. Le SQL des deux semaines précédentes vous a appris à interroger des données qui existent déjà, proprement rangées. Python répond à un autre besoin : agir sur des fichiers en désordre, répéter un traitement, décider selon des conditions.

Le piège de cette semaine n'est pas technique : c'est d'écrire un script que vous êtes seul à comprendre. La demande du responsable d'exploitation fait partie du cahier des charges, au même titre que la détection des anomalies.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C2.3** — Manipuler des structures de données et utiliser l'algorithmie afin de traduire en script des besoins de traitement *(niveau 1 — imiter)*
- **C2.1** — Effectuer des choix méthodologiques pour l'automatisation des traitements et les documenter *(niveau 1 — imiter)*
- **C2.4** — Appliquer les bonnes pratiques de la programmation : code organisé, réutilisable, partageable *(niveau 1 — imiter)*
- **C1.4** — Réaliser des requêtes avancées *(niveau 2 — adapter)*
- **C4.5** — Utiliser un tableur, notamment les TCD *(niveau 2 — adapter)*

## Modalités pédagogiques

**Organisation** : individuel.

**Jour 1 — matin (lancement, 2 h)**. Le formateur joue Damien et décrit son geste quotidien. Vous recevez les fichiers d'une journée réelle. Première tâche, sans code : listez par écrit toutes les vérifications que Damien fait sans y penser. Cette liste est votre spécification.

**Jour 1 — après-midi**. Vous tentez d'automatiser avec le tableur. Vous mesurez la limite : trente fichiers, formats différents, tous les matins.

**Jour 2 — matin (apport flash, 2 h 30)**. Python : variables, types, listes, dictionnaires, tuples. Conditions, boucles, itérateurs. Lecture et écriture de fichiers CSV.

**Jour 3 — matin (apport flash, 1 h 30)**. Fonctions : paramètres, valeurs de retour, une fonction = une responsabilité. Compréhensions de liste. Nommage, PEP 8, docstrings. Notion de complexité : pourquoi une boucle dans une boucle devient lente.

**Jours 2 à 4 — production**. Écrivez un script qui parcourt le dossier, lit chaque fichier, applique les contrôles et produit un rapport d'anomalies exploitable par Damien.

Contrôles minimaux attendus : quantité négative ou nulle, quantité aberrante au regard de l'historique, code produit absent du référentiel, date de livraison antérieure à aujourd'hui, ligne incomplète, doublon exact.

**Questions guidantes.** Si un fichier utilise le point-virgule et un autre la virgule, faut-il deux scripts ou un script qui s'adapte ? Que doit faire votre programme quand il rencontre une ligne illisible : s'arrêter, l'ignorer, la signaler ? Quelle différence pour Damien ? Comment savoir qu'une quantité est « aberrante » — quel seuil, et d'où le tirez-vous ? Si un client ajoute une colonne demain, combien de lignes de votre code faut-il modifier ?

**Jour 4 — après-midi (revue croisée)**. Vous recevez le script d'un autre apprenant, sans son auteur. Vous devez ajouter un contrôle supplémentaire. Le temps qu'il vous faut pour comprendre son code est la vraie note de sa lisibilité.

**Jour 5**. Finalisation, README rédigé pour Damien, publication. Restitution 6 minutes : vous lancez le script en direct.

## Modalités d'évaluation

Brief **formatif**. Auto-évaluation, revue croisée, retour collectif.

L'épreuve réelle de la semaine est celle du jour 4 : un autre apprenant doit pouvoir étendre votre script sans vous. C'est la traduction concrète du critère du référentiel — « code organisé, réutilisable et partageable dans un cadre professionnel ».

Le formateur signalera en retour collectif les trois travers les plus fréquents en première semaine de code : le script d'un seul bloc sans fonction, les variables nommées `a`, `b`, `tmp`, et l'absence de gestion des cas d'erreur.

## Données fournies (source exacte)

> Le scénario (« Nord Logistique ») et les fichiers sont **synthétiques** et **reproductibles** :
> une journée de bons de commande sales, avec un référentiel produits en base.

- **Fichiers du jour** : `donnees/client_01.csv` … `client_30.csv` (~30 fichiers, ~900-1000 lignes),
  aux **séparateurs hétérogènes** (`;` ou `,`) et avec des lignes corrompues.
- **Référentiel produits** : `referentiel.db` (SQLite, table `produit` : codes valides +
  quantité max historique) — à **extraire par requête SQL**, pas à ressaisir.
- **Reproduction** : `python3 generer_donnees.py` régénère fichiers + référentiel (les dates sont
  relatives au jour de génération, pour que le contrôle « date passée » ait du sens).

## Livrables attendus

**Un dépôt GitHub public** :

1. `README.md` — **rédigé pour Damien**, pas pour un développeur : à quoi sert le script, comment le lancer, comment lire le rapport, qui appeler si ça casse.
2. `specification.md` — la liste des contrôles issue du jour 1, avec pour chacun la règle appliquée et le seuil retenu.
3. `controle_qualite.py` — le script, découpé en fonctions, conforme PEP 8, avec docstrings.
4. `rapport_exemple.csv` — un rapport d'anomalies produit sur les données du jour.
5. `choix-methodologiques.md` — une page : trois décisions que vous avez prises (traitement des lignes illisibles, choix du seuil d'aberration, gestion des séparateurs), l'option écartée et pourquoi.
6. `donnees/` — les fichiers d'exemple.

## Critères de performance

**C2.3 — Algorithmie, niveau imiter**
• Le script lit l'ensemble des fichiers du dossier sans que leur nombre soit codé en dur.
• Au moins une liste, un dictionnaire et une boucle sont utilisés à bon escient.
• Les six contrôles minimaux sont implémentés et détectent effectivement les anomalies présentes.
• Le script ne s'interrompt pas sur une ligne illisible : le comportement choisi est appliqué et documenté.

**C2.1 — Choix méthodologiques, niveau imiter**
• Le document `choix-methodologiques.md` présente trois décisions, chacune avec l'option écartée.
• Le seuil d'aberration est chiffré et son origine est expliquée.
• La spécification du jour 1 est présente et correspond aux contrôles implémentés.

**C2.4 — Bonnes pratiques, niveau imiter**
• Le code est découpé en au moins quatre fonctions, chacune avec une responsabilité unique.
• Les noms de variables et de fonctions sont explicites (aucun `a`, `tmp`, `data2`).
• Chaque fonction porte une docstring d'une ligne minimum.
• L'indentation et l'espacement respectent PEP 8.
• Le README permet à un non-technicien de lancer le script.

**C1.4 / C4.5 — Réactivation**
• Le référentiel produits est extrait de la base SQL par une requête, non ressaisi.
• Le rapport d'anomalies est ouvert dans un tableur et synthétisé par un TCD (anomalies par client et par type).

## Ressources

- Documentation Python — tutoriel officiel (français) : https://docs.python.org/fr/3/tutorial/
- Python — module csv : https://docs.python.org/fr/3/library/csv.html
- PEP 8 — guide de style Python : https://peps.python.org/pep-0008/
- Real Python — écrire des fonctions propres : https://realpython.com/defining-your-own-python-function/
- Python — gestion des exceptions : https://docs.python.org/fr/3/tutorial/errors.html
