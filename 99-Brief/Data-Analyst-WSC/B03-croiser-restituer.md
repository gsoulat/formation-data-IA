# Brief B03 — Croiser pour décider : TCD, corrélations et première restitution client

## Informations

| | |
|---|---|
| **Semaine** | S3 · 28 sept–2 oct 2026 · 5 jours · Guillaume |
| **Modalité · Évaluation** | Binôme · Sommatif (checklist complète) |
| **Compétences visées** | C4.5 · C3.1 · C4.2 · C3.3 · C4.8 |

## Description

Une agence immobilière veut savoir où acheter dans les deux ans. Vous disposez des transactions réelles enregistrées par l'État (DVF), réparties sur trois fichiers qui ne se parlent pas. Vous devez les rapprocher, dégager une tendance et la défendre devant le gérant.

## Contexte

L'agence Habitat Nord, huit collaborateurs, réalise l'essentiel de son chiffre d'affaires sur une dizaine de communes de la métropole lilloise. Le gérant, Karim Belkacem, envisage d'ouvrir une seconde agence. Il hésite entre trois secteurs et raisonne aujourd'hui « au feeling » : ce que lui disent ses négociateurs, ce qu'il lit dans la presse locale.

Un de ses négociateurs lui a signalé que l'État publie l'intégralité des transactions immobilières réelles — le fichier DVF, Demandes de Valeurs Foncières. Prix effectivement payés, surfaces, dates, localisation. Karim y voit une occasion de décider sur des faits plutôt que sur des impressions, mais personne dans l'agence ne sait exploiter un fichier de plusieurs centaines de milliers de lignes.

Il vous transmet trois extractions annuelles distinctes, qui n'ont ni exactement les mêmes colonnes ni les mêmes codes de commune. Sa question est directe : « Dans quel secteur les prix montent-ils le plus vite, et est-ce que ça va continuer ? »

C'est votre première vraie chaîne complète : vous allez collecter des fichiers séparés, les rapprocher, les nettoyer un minimum, les analyser, puis défendre une recommandation devant un décideur qui engagera de l'argent. Le gérant ne veut pas de tableaux : il veut savoir où acheter.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C4.5** — Utiliser un tableur, notamment les TCD, pour proposer des croisements de variables *(niveau 2 — adapter)*
- **C3.1** — Utiliser les statistiques descriptives pour faire émerger des informations pertinentes *(niveau 2 — adapter)*
- **C4.2** — Utiliser les visualisations descriptives *(niveau 2 — adapter)*
- **C3.3** — Modéliser des régressions et interpréter les métriques pour trouver des tendances *(niveau 1 — imiter)*
- **C4.8** — Présenter à l'oral et à l'écrit de manière claire et sans ambiguïté *(niveau 1 — imiter)*

## Modalités pédagogiques

**Organisation** : binôme, dépôt GitHub commun.

**Jour 1 — matin (lancement, 2 h)**. Le formateur joue Karim Belkacem. Vous récupérez les trois fichiers DVF. Vous constatez l'ampleur du problème : volumétrie, colonnes divergentes, valeurs manquantes, transactions atypiques (ventes à 1 €, garages comptés comme logements).

**Jour 1 — après-midi**. Vous tentez de rapprocher les fichiers avec ce que vous savez. Vous butez sur la question du rapprochement et sur la volumétrie.

**Jour 2 — matin (apport flash, 1 h 30)**. Tableaux croisés dynamiques : le TCD comme calcul statistique par groupe. Recherches inter-fichiers (RECHERCHEV / XLOOKUP, INDEX-EQUIV). Complétion de données. Graphiques croisés.

**Jour 3 — matin (apport flash, 1 h)**. Coefficient de corrélation, nuage de points, droite de tendance et R². Ce que le R² dit — et ce qu'il ne dit pas.

**Jours 2 à 4 — production**. Quatre étapes :
1. **Rapprocher** — consolidez les trois années dans un jeu unique. Documentez les correspondances de colonnes que vous établissez.
2. **Assainir** — écartez ce qui fausserait l'analyse. Toute exclusion doit être justifiée par écrit et chiffrée : combien de lignes retirées, pourquoi.
3. **Croiser** — prix au m² par commune et par année, par TCD. Évolution sur trois ans. Identifiez les trois secteurs les plus dynamiques.
4. **Projeter** — droite de tendance sur les secteurs retenus. Quelle progression annoncez-vous à 24 mois, et avec quelle confiance ?

**Questions guidantes.** Un prix moyen au m² a-t-il un sens si vous mélangez maisons et appartements ? Une commune où trois ventes ont eu lieu est-elle comparable à une commune où il y en a eu quatre cents ? Une hausse de 12 % sur trois ans permet-elle d'annoncer 8 % sur les deux suivantes — et qu'est-ce qui pourrait invalider cette projection ? Que signifie un R² de 0,4 pour votre recommandation ?

**Jour 4 — après-midi (revue croisée)**. Chaque binôme relit le travail d'un autre en se demandant : « Si j'étais le gérant, engagerais-je 300 000 € sur cette recommandation ? »

**Jour 5**. Finalisation, publication, restitution de 10 minutes devant le formateur en posture de gérant — qui posera des questions et contestera. Rétrospective.

## Modalités d'évaluation

Brief **sommatif**, corrigé à la checklist par le formateur qui l'a rédigé.

L'évaluation porte sur deux volets. Le **volet technique** (70 %) vérifie la consolidation, les croisements, l'assainissement documenté et la tendance. Le **volet restitution** (30 %) est évalué pendant les 10 minutes du jour 5 : le gérant contestera au moins une de vos conclusions, et votre capacité à répondre sans vous réfugier derrière la technique fait partie de la note.

Une recommandation prudente et argumentée vaut mieux qu'une recommandation ambitieuse et fragile. Un binôme qui conclut « les données ne permettent pas de trancher entre A et B, voici ce qu'il faudrait de plus » peut valider toutes les compétences.

## Données fournies (source exacte)

> Le scénario (agence « Habitat Nord », gérant Karim Belkacem) est **fictif** ; les **données réelles**
> support — et sur lesquelles porte la correction — sont les transactions DVF de trois communes de la
> métropole lilloise.

- **Jeu** : DVF géolocalisées (Etalab) — https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/
- **Les 3 fichiers** (un par année) : Roubaix (59512), Tourcoing (59599), Marcq-en-Barœul (59378), pour **2021, 2022 et 2023**.
- **Récupération** (par commune et année — suivre les redirections avec `-L`) :

```bash
curl -sL "https://files.data.gouv.fr/geo-dvf/latest/csv/2023/communes/59/59599.csv" -o tourcoing_2023.csv
# idem pour 59512 (Roubaix) et 59378 (Marcq), et pour les années 2021 et 2022
```

- **Licence** : Licence Ouverte (Etalab).

## Livrables attendus

**Un dépôt GitHub public** par binôme :

1. `README.md` — projet, source DVF, méthode, auteurs, mode d'emploi du classeur.
2. `analyse-dvf.xlsx` — onglets : données consolidées, journal d'assainissement, TCD par commune et par année, graphiques.
3. `journal-assainissement.md` — chaque règle d'exclusion appliquée, le nombre de lignes concernées, la justification.
4. `recommandation.md` — deux pages : les trois secteurs analysés, celui que vous recommandez, la tendance projetée, et les limites de votre analyse.
5. `graphiques/` — évolution des prix par secteur, nuage de points avec droite de tendance.

**Restitution** : 10 minutes devant le formateur en posture de gérant, sans diapositives (vous montrez le classeur).

## Critères de performance

**C4.5 — Tableur, niveau adapter**
• Les trois fichiers sont consolidés en un jeu unique et la correspondance des colonnes est documentée.
• Au moins un TCD croise deux dimensions (commune × année) avec un indicateur calculé.
• Au moins une recherche inter-fichiers est utilisée et fonctionnelle.
• Un graphique croisé est produit à partir d'un TCD.

**C3.1 — Statistiques, niveau adapter**
• Le prix au m² est calculé et non le prix brut ; le choix est justifié.
• Les effectifs par groupe sont affichés à côté des moyennes, permettant d'écarter les groupes non significatifs.
• Un coefficient de corrélation est calculé et interprété en toutes lettres.

**C4.2 — Visualisations, niveau adapter**
• L'évolution par secteur est représentée graphiquement, avec axes et unités.
• Un nuage de points avec droite de tendance est produit.

**C3.3 — Tendance, niveau imiter**
• Une droite de tendance est ajoutée avec son R² affiché.
• Une projection chiffrée à 24 mois est formulée, assortie d'au moins une réserve explicite.

**C4.8 — Restitution, niveau imiter**
• La recommandation tient en deux pages et se conclut par un choix, pas par une liste.
• Au moins une limite de l'analyse est énoncée spontanément à l'oral.

## Ressources

- DVF — demandes de valeurs foncières : https://www.data.gouv.fr/fr/datasets/demandes-de-valeurs-foncieres/
- Explorateur DVF (visualisation officielle) : https://app.dvf.etalab.gouv.fr/
- Microsoft — créer un tableau croisé dynamique : https://support.microsoft.com/fr-fr/office/cr%C3%A9er-un-tableau-crois%C3%A9-dynamique-pour-analyser-des-donn%C3%A9es-de-feuille-de-calcul-a9a84538-bfe9-40a9-a8e9-f99134456576
- Google Sheets — tableaux croisés dynamiques : https://support.google.com/docs/answer/1272900
- INSEE — population communale (pondération) : https://www.insee.fr/fr/statistiques
