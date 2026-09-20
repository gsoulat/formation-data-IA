# Brief B04 — Audit d'une base inconnue : exploration, diagnostic qualité et requêtage SQL

## Informations

| | |
|---|---|
| **Semaine** | S4 · 5–9 oct 2026 · 5 jours · Ayoub |
| **Modalité · Évaluation** | Individuel · Formatif |
| **Compétences visées** | C1.1 · C1.4 · C1.2 · C1.7 |

## Description

Une enseigne récupère la base de son ancien prestataire, sans documentation ni interlocuteur. Avant d'y brancher quoi que ce soit, il faut savoir ce qu'elle contient, ce qui y est faux, et quelles données personnelles s'y trouvent. Vous passez du tableur au SQL.

## Contexte

Maison Verlaine, enseigne régionale de 22 magasins d'ameublement, vient de rompre son contrat avec le prestataire qui hébergeait son système de caisse. Le prestataire a livré, comme l'y obligeait le contrat, une base de données complète. Puis il a cessé de répondre.

La base fonctionne, mais personne ne sait exactement ce qu'elle contient. Le schéma n'est pas documenté. Les noms de tables sont abrégés. Certaines colonnes portent des noms qui ne veulent plus rien dire pour personne (`flag_3`, `cd_typ`, `dt_maj2`). La direction financière veut y brancher un outil de pilotage ; la DSI refuse tant qu'on ne sait pas ce qu'il y a dedans ; et la déléguée à la protection des données a bloqué le projet en posant une question simple : « Y a-t-il des données personnelles là-dedans, et lesquelles ? »

Vous êtes missionné pour trois semaines — vous en avez une. Votre travail n'est pas de corriger la base mais de l'auditer : dire ce qu'elle contient, ce qui y est douteux, ce qu'on peut en tirer, et ce qui relève du RGPD.

Le tableur ne suffira plus. Plusieurs tables dépassent le million de lignes. C'est le moment où vous changez d'outil : le SQL n'est pas une nouvelle matière, c'est le même raisonnement que votre tableau croisé dynamique, écrit autrement.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C1.1** — Identifier les possibilités d'utilisation des données, être force de proposition dans l'exploration et l'évaluation de la qualité *(niveau 2 — adapter)*
- **C1.4** — Réaliser des requêtes avancées : agrégations, jointures, vues et sous-requêtes *(niveau 1 — imiter)*
- **C1.2** — Définir une stratégie de prise de décision par les données suivant les besoins métier *(niveau 1 — imiter)*
- **C1.7** — Contrôler les modalités de collecte et d'utilisation des données, mesurer les enjeux du RGPD *(niveau 1 — imiter)*

## Modalités pédagogiques

**Organisation** : individuel, dépôt personnel.

**Jour 1 — matin (lancement, 2 h)**. Le formateur joue le directeur financier. Vous recevez les accès à la base. Aucun schéma. Vous devez d'abord répondre à une question enfantine et redoutable : combien y a-t-il de tables, et à quoi servent-elles ?

**Jour 1 — après-midi**. Exploration libre. Vous essayez d'ouvrir la base avec vos réflexes de tableur. Vous mesurez pourquoi ça ne tient pas.

**Jour 2 — matin (apport flash, 2 h)**. SELECT, WHERE, ORDER BY, LIMIT. Fonctions d'agrégation et GROUP BY — présentés explicitement comme la traduction du TCD de la semaine précédente. Puis les jointures, présentées comme la traduction de la recherche inter-fichiers.

**Jour 3 — matin (apport flash, 1 h)**. Compter ce qui manque : COUNT, COUNT(colonne), IS NULL, DISTINCT. Détecter les doublons par GROUP BY … HAVING COUNT(*) > 1.

**Jours 2 à 4 — production**. Livrez un audit en quatre parties :
1. **Cartographie** — inventaire des tables : volumétrie, clés apparentes, relations que vous déduisez. Un schéma dessiné, même à la main.
2. **Qualité** — pour les cinq tables principales : taux de remplissage par colonne, doublons, valeurs impossibles, incohérences de type.
3. **Exploitation** — répondez à cinq questions métier réelles posées par la direction financière (chiffre d'affaires par magasin et par mois, panier moyen, produits jamais vendus, clients inactifs depuis 18 mois, saisonnalité).
4. **RGPD** — inventaire des colonnes contenant des données personnelles, avec pour chacune : la nature de la donnée, sa sensibilité, et une première appréciation du risque.

**Questions guidantes.** Comment savoir qu'une colonne est une clé étrangère quand rien ne le déclare ? Une colonne remplie à 3 % est-elle inutile, ou porte-t-elle l'information la plus précieuse de la base ? Un client qui apparaît deux fois avec deux orthographes est-il un doublon ? Une adresse e-mail est-elle une donnée personnelle ? Et un identifiant client interne ? Et un code postal seul ?

**Jour 4 — après-midi (revue croisée)**. Vous relisez l'audit d'un autre apprenant : ses conclusions sont-elles vérifiables à partir des requêtes qu'il fournit ?

**Jour 5**. Finalisation, publication, restitution de 8 minutes. Rétrospective.

## Modalités d'évaluation

Brief **formatif**. Auto-évaluation, revue croisée, retour collectif.

Le formateur portera une attention particulière à un point : les conclusions de l'audit doivent être **reproductibles**. Chaque affirmation du rapport doit renvoyer à une requête présente dans le dépôt, exécutable telle quelle. Un audit dont on ne peut pas refaire les calculs n'a aucune valeur professionnelle, quelle que soit la qualité de sa rédaction.

Le volet RGPD sera repris et approfondi en B08 puis évalué au palier 1 : cette semaine, l'inventaire suffit, l'analyse de risque viendra ensuite.

## Données fournies (source exacte)

> Le scénario (« Maison Verlaine ») et la base sont **synthétiques** : aucune donnée personnelle
> réelle. Une **base interne « sale » avec données personnelles** est indispensable à cet audit —
> l'open data n'en fournit jamais. La base est **fournie** et **reproductible**.

- **Base** : `base_verlaine.db` (SQLite) — 4 tables (`t_cli`, `t_art`, `t_mag`, `t_vte`), ~3 050 ventes.
- **Reproduction** : `python3 generer_base.py` régénère la base **à l'identique** (graine figée).
- Elle contient volontairement : schéma crypté sans contraintes, doublons de tickets, montants en
  **texte**, dates en **formats mixtes**, valeurs aberrantes, et données personnelles (nom, e-mail,
  téléphone) — c'est précisément l'objet de l'audit.

## Livrables attendus

**Un dépôt GitHub public** :

1. `README.md` — contexte, périmètre de l'audit, méthode, auteur.
2. `requetes/` — un fichier `.sql` par partie, requêtes commentées et exécutables.
3. `schema.md` (ou image) — le schéma de la base tel que vous le reconstituez, avec les relations déduites et votre degré de certitude.
4. `rapport-audit.md` — trois pages maximum : cartographie, qualité, exploitation, RGPD. Chaque chiffre renvoie à la requête qui le produit.
5. `inventaire-rgpd.md` — tableau : table, colonne, nature de la donnée, personnelle oui/non, sensibilité, remarque.

**Restitution** : 8 minutes devant le groupe.

## Critères de performance

**C1.1 — Exploration et qualité, niveau adapter**
• L'inventaire couvre toutes les tables, avec volumétrie.
• Le schéma reconstitué identifie au moins trois relations entre tables, avec justification.
• Le taux de remplissage est chiffré colonne par colonne sur les cinq tables principales.
• Au moins quatre anomalies distinctes sont documentées, chacune illustrée par une requête et un exemple.

**C1.4 — Requêtes, niveau imiter**
• Les cinq questions métier reçoivent une réponse produite par une requête fonctionnelle.
• Au moins une requête utilise GROUP BY avec une fonction d'agrégation.
• Au moins une requête utilise une jointure entre deux tables.
• Les requêtes sont commentées : une ligne indiquant ce qu'elles cherchent.

**C1.2 — Stratégie, niveau imiter**
• Le rapport propose au moins deux décisions que la direction financière pourrait prendre à partir de ces données.
• Pour chaque décision, l'indicateur qui la soutient est nommé.

**C1.7 — RGPD, niveau imiter**
• L'inventaire liste toutes les colonnes contenant des données personnelles.
• La nature de chaque donnée est qualifiée (identifiant direct, indirect, sensible).
• Au moins un risque concret est formulé.

## Ressources

- SQLZoo — exercices SQL progressifs : https://sqlzoo.net/
- Documentation PostgreSQL (français) : https://docs.postgresql.fr/
- SQL.sh — cours SQL en français : https://sql.sh/
- CNIL — qu'est-ce qu'une donnée personnelle ? : https://www.cnil.fr/fr/definition/donnee-personnelle
- dbdiagram.io — dessiner un schéma de base : https://dbdiagram.io/
