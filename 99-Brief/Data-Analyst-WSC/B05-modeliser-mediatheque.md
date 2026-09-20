# Brief B05 — Concevoir la base d'une médiathèque : modélisation, intégrité et performance

## Informations

| | |
|---|---|
| **Semaine** | S5 · 12–16 oct 2026 · 5 jours · Ayoub |
| **Modalité · Évaluation** | Binôme · Sommatif |
| **Compétences visées** | C1.3 · C1.4 |

## Description

La médiathèque intercommunale gère ses prêts sur un tableur de 40 000 lignes devenu ingérable. Vous concevez la base relationnelle qui le remplacera, vous y injectez l'historique, et vous prouvez que vos requêtes tiennent la charge.

## Contexte

La médiathèque intercommunale des Weppes gère 18 000 documents et 4 200 adhérents. Depuis 2019, tout passe par un unique classeur partagé : une ligne par prêt, avec le nom de l'adhérent, son adresse, le titre du document, l'auteur, la date de sortie et la date de retour.

Le classeur atteint 40 000 lignes et pose désormais trois problèmes quotidiens. Il est lent à ouvrir. Il contient des incohérences — le même adhérent apparaît sous quatre orthographes, le même livre sous trois titres légèrement différents. Et il ne permet pas de répondre aux questions que pose la directrice : quels documents ne sortent jamais ? quels adhérents ont cessé de venir ? combien de retards par mois ?

La collectivité a budgété un vrai logiciel de gestion, livrable dans dix-huit mois. En attendant, la directrice veut une base propre : « Je veux qu'on arrête de saisir trois fois la même personne, et je veux pouvoir poser des questions sans attendre trois minutes. »

Votre mission comporte deux volets indissociables. Concevoir le modèle — c'est-à-dire décider quelles tables existent, comment elles se lient, et quelles règles empêchent la saisie d'une incohérence. Puis démontrer que ce modèle tient : injecter les 40 000 prêts historiques, écrire les requêtes de la directrice, et mesurer leur temps d'exécution avant et après optimisation.

Un modèle qu'on ne peut pas interroger vite n'est pas un bon modèle. C'est le critère du référentiel : la modélisation doit être « optimisée pour des besoins professionnels ».

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C1.3** — Modéliser des bases de données relationnelles (notamment SQL) afin de répondre avec rigueur aux besoins des utilisateurs *(niveau 1 — imiter)*
- **C1.4** — Réaliser des requêtes avancées : agrégations, jointures, vues et sous-requêtes, en s'assurant de l'intégrité des données *(niveau 2 — adapter)*

## Modalités pédagogiques

**Organisation** : binôme, dépôt commun.

**Jour 1 — matin (lancement, 2 h)**. Le formateur joue la directrice. Vous recevez le classeur historique et la liste de ses questions. Avant tout apport : dessinez au tableau, en binôme, les « choses » qui existent dans cette médiathèque. Un prêt est-il une chose ? Un exemplaire et une œuvre sont-ils la même chose ?

**Jour 1 — après-midi**. Vous confrontez vos schémas entre binômes. Les désaccords sont le vrai matériau du brief.

**Jour 2 — matin (apport flash, 2 h)**. Modélisation relationnelle : entités, attributs, cardinalités, clés primaires et étrangères. Formes normales jusqu'à la 3NF. CREATE TABLE, contraintes NOT NULL, UNIQUE, FOREIGN KEY, CHECK.

**Jour 3 — matin (apport flash, 1 h 30)**. Vues, sous-requêtes, CTE. Puis : index, plan d'exécution (EXPLAIN), mesure du temps de réponse.

**Jours 2 à 4 — production**.
1. **Modéliser** — schéma relationnel complet, cardinalités justifiées. Décidez explicitement du sort de la distinction œuvre / exemplaire et défendez votre choix.
2. **Créer** — scripts DDL avec contraintes d'intégrité. Chaque contrainte doit empêcher une erreur réelle observée dans le classeur.
3. **Injecter** — chargez l'historique. Vous rencontrerez des lignes que vos contraintes refusent : c'est normal et c'est le plus instructif. Documentez-les.
4. **Interroger** — écrivez les requêtes de la directrice, dont au moins une vue et une sous-requête.
5. **Optimiser** — mesurez le temps de la requête la plus lente, ajoutez un index, remesurez, expliquez.

**Questions guidantes.** Si deux adhérents portent le même nom, votre modèle les distingue-t-il ? Que se passe-t-il quand un document est perdu — le supprimez-vous, et qu'advient-il de son historique de prêts ? Une contrainte qui refuse 8 % de l'historique est-elle trop stricte, ou l'historique est-il faux ? Un index accélère la lecture : que coûte-t-il ?

**Jour 4 — après-midi (revue croisée)**. Chaque binôme tente de faire échouer le modèle d'un autre : trouvez une saisie absurde que ses contraintes laissent passer.

**Jour 5**. Finalisation, publication, restitution 8 minutes.

## Modalités d'évaluation

Brief **sommatif**, checklist complète.

Deux volets. Le **modèle** (60 %) : justesse des cardinalités, pertinence des contraintes, capacité à absorber l'historique. La **performance** (40 %) : les requêtes répondent aux questions posées, et la démonstration d'optimisation est chiffrée — un avant, un après, un écart mesuré.

La revue croisée du jour 4 compte : si un autre binôme parvient à insérer une donnée absurde dans votre base, la contrainte manquante est signalée et vous avez le jour 5 pour la corriger. Corriger après signalement ne pénalise pas ; laisser la faille pénalise.

## Données fournies (source exacte)

> Le scénario (« médiathèque des Weppes ») et le classeur sont **synthétiques** : aucune personne
> réelle. Une base interne avec des identités d'adhérents est nécessaire — l'open data ne la fournit pas.
> Le classeur est **fourni** et **reproductible**.

- **Classeur** : `classeur_prets.csv` — **40 000 prêts** (1 ligne = 1 prêt : nom/prénom/adresse de
  l'adhérent, titre/auteur du document, date de sortie, date de retour).
- **Reproduction** : `python3 generer_classeur.py` régénère le fichier **à l'identique**.
- Il contient volontairement : mêmes adhérents/œuvres sous **plusieurs orthographes**, **dates
  incohérentes** (retour avant sortie), prêts en cours (retour vide) et lignes sans nom — c'est la
  matière du modèle et de l'assainissement.

## Livrables attendus

**Un dépôt GitHub public** par binôme :

1. `README.md` — projet, choix de modélisation majeurs, auteurs.
2. `modele/schema.png` — le schéma relationnel avec cardinalités.
3. `modele/justification.md` — pour chaque décision structurante : l'option retenue, l'option écartée, pourquoi.
4. `sql/01-creation.sql` — DDL complet avec contraintes commentées.
5. `sql/02-chargement.sql` — script d'injection de l'historique.
6. `sql/03-requetes.sql` — les requêtes de la directrice, dont une vue et une sous-requête.
7. `rapport-integrite.md` — les lignes refusées par les contraintes : combien, pourquoi, que faire.
8. `rapport-performance.md` — requête testée, temps avant, index ajouté, temps après, plan d'exécution.

## Critères de performance

**C1.3 — Modélisation, niveau imiter**
• Le schéma comporte au minimum quatre tables reliées, avec cardinalités explicites.
• Les clés primaires et étrangères sont déclarées dans le DDL.
• Au moins trois contraintes d'intégrité (NOT NULL, UNIQUE, CHECK, FOREIGN KEY) sont posées, et chacune est justifiée par une erreur réelle du classeur d'origine.
• La distinction œuvre / exemplaire est tranchée et argumentée, quelle que soit l'option retenue.
• Le modèle absorbe l'historique : le nombre de lignes chargées et rejetées est chiffré.

**C1.4 — Requêtes, niveau adapter**
• Les quatre questions de la directrice reçoivent une réponse par requête fonctionnelle.
• Au moins une vue est créée et utilisée.
• Au moins une sous-requête ou CTE est présente.
• Au moins une jointure porte sur trois tables.
• Le rapport de performance présente un temps avant, un index, un temps après, et un écart chiffré.
• Le plan d'exécution (EXPLAIN) est joint et commenté en une phrase.

## Ressources

- PostgreSQL — documentation française : https://docs.postgresql.fr/
- PostgreSQL — comprendre EXPLAIN : https://www.postgresql.org/docs/current/using-explain.html
- SQL.sh — création de tables et contraintes : https://sql.sh/cours/create-table
- dbdiagram.io — schéma relationnel : https://dbdiagram.io/
- SQLite — documentation (alternative légère) : https://www.sqlite.org/docs.html
