# Brief B15 — Prévoir les charges d'un parc immobilier : régression et séries temporelles

## Informations

| | |
|---|---|
| **Semaine** | S19 · 1–5 fév 2027 · 5 jours · Guillaume |
| **Modalité · Évaluation** | Binôme · Sommatif |
| **Compétences visées** | C3.3 · C3.2 · C1.6 |

## Description

Un bailleur social doit budgéter les charges énergétiques de 1 200 logements pour l'an prochain. Vous construisez le modèle de régression qui prévoit la consommation — en y intégrant la météo réelle récupérée par API, et en disant honnêtement la marge d'erreur de votre prévision.

## Contexte

Un bailleur social gère 1 200 logements répartis sur la métropole. Chaque automne, il doit voter un budget prévisionnel des charges, dont la part énergétique — chauffage collectif surtout — est la plus lourde et la plus incertaine. Une sous-estimation creuse le déficit ; une surestimation gonfle les charges appelées aux locataires, déjà en difficulté.

Jusqu'ici, le directeur financier reconduit le budget de l'année passée en ajoutant un pourcentage forfaitaire. Les écarts en fin d'exercice sont importants et il le sait : « Mon "plus 3 %" n'a aucun fondement. L'an dernier l'hiver a été doux et j'avais surbudgété de 200 000 €. Je veux une prévision qui tienne compte de la réalité, à commencer par la météo. »

Vous disposez de l'historique de consommation mensuelle des résidences sur plusieurs années. La consommation dépend de facteurs que vous devez modéliser : la saison évidemment, mais aussi la rigueur réelle de l'hiver, la surface chauffée, le nombre de logements occupés. La météo n'est pas dans vos données : vous irez la chercher par API (réactivation de B07), aux coordonnées des résidences.

C'est votre premier modèle de régression : prédire une valeur numérique continue, et pas seulement une catégorie. Vous interpréterez ses métriques — de combien votre prévision se trompe-t-elle en moyenne ? — et vous dégagerez une tendance sur les douze mois à venir. Le directeur financier votera un budget sur la foi de votre chiffre : la marge d'erreur que vous annoncez fait partie du livrable autant que le chiffre lui-même.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C3.3** — Modéliser des régressions et interpréter les métriques associées afin de définir des modèles de prévisions et trouver des tendances futures pour des valeurs numériques *(niveau 2 — adapter)*
- **C3.2** — Maîtriser le process d'apprentissage automatique *(niveau 2 — adapter)*
- **C1.6** — Mettre en place une interface standard de partage automatique de données (API) *(niveau 3 — transposer)*

## Modalités pédagogiques

**Organisation** : binôme, dépôt commun.

**Jour 1 — matin (lancement, 2 h)**. Le formateur joue le directeur financier. Vous recevez l'historique de consommation. Vous identifiez les facteurs explicatifs plausibles et constatez que la météo manque.

**Jour 1 — après-midi**. Vous récupérez les données météo historiques par API (réactivation B07) et les rapprochez de la consommation.

**Jour 2 — matin (apport flash, 2 h 30)**. La régression linéaire : principe, ajustement, coefficients et leur interprétation. Les métriques : RMSE, MAE, R² — ce que chacune dit. La différence entre corréler et prédire. Notion de saisonnalité et de tendance dans une série temporelle.

**Jours 2 à 4 — production**.
1. **Assembler** — croisez consommation et météo en un jeu prêt pour la modélisation.
2. **Modéliser** — une régression prédisant la consommation à partir des facteurs retenus. Séparez entraînement et test (réactivation B14).
3. **Mesurer** — RMSE, MAE, R². Traduisez la RMSE en euros : de combien votre budget peut-il se tromper ?
4. **Interpréter** — quels facteurs pèsent le plus ? Le signe des coefficients est-il cohérent avec le bon sens ?
5. **Projeter** — prévoyez les douze prochains mois, avec la saisonnalité. Encadrez la prévision d'une marge.

**Questions guidantes.** Un R² de 0,8 signifie-t-il que votre prévision budgétaire est fiable à 80 % ? Que vaut une RMSE de 15 000 kWh si vous ne savez pas à quoi la comparer ? Si le coefficient de la température est positif, votre modèle a-t-il un sens physique ? Peut-on prévoir décembre prochain sans connaître la météo de décembre prochain — et comment gérez-vous cette incertitude ? Quelle marge annoncez-vous au directeur financier pour qu'il vote sans être trompé ?

**Jour 4 — après-midi (revue croisée)**. Un autre binôme reçoit votre prévision et doit dire s'il voterait un budget dessus, et avec quelle réserve.

**Jour 5**. Finalisation, publication, restitution 8 minutes devant le formateur en directeur financier, qui demandera « et si je me trompe de combien ? ».

## Modalités d'évaluation

Brief **sommatif**, checklist complète.

L'évaluation valorise l'**interprétation honnête** autant que la construction du modèle. Un binôme qui annonce « nous prévoyons 1,2 M€ ± 180 000 € et voici pourquoi cette marge » réussit mieux qu'un binôme qui annonce « 1,2 M€ » sans marge, même si le modèle sous-jacent est identique.

C1.6 est ici au niveau transposer : la récupération météo par API doit être autonome et robuste, c'est sa troisième mise en œuvre.

## Données fournies (source exacte)

> Météo **réelle** (API) ; consommation du parc **synthétique** (données internes du bailleur →
> hors open data), pilotée par la vraie météo.

- **Météo** : **Open-Meteo** API historique — température mensuelle 2019-2024, métropole lilloise
  (récupérée par `collecte-meteo.py`).
- **Consommation** : `data/consommation.csv` — historique mensuel des 1 200 logements, généré par
  `generer_consommation.py` (chauffage ∝ degrés-jours + occupation + bruit). La consommation
  régionale **RTE éCO2mix** serait la source réelle équivalente.

## Livrables attendus

**Un dépôt GitHub public** par binôme :

1. `README.md` — problème, démarche, prévision, marge, auteurs.
2. `collecte-meteo.py` — récupération API des données climatiques.
3. `modele.ipynb` — assemblage, régression, séparation, métriques, projection.
4. `interpretation.md` — lecture des coefficients, RMSE traduite en euros, facteurs dominants.
5. `prevision-budget.md` — le chiffre pour le directeur financier, sa marge, ses hypothèses, ses limites.
6. `graphiques/` — consommation historique et projetée, avec intervalle.

## Critères de performance

**C3.3 — Régression, niveau adapter**
• Une régression est construite pour prédire la consommation.
• RMSE, MAE et R² sont calculés et chacun est interprété.
• La RMSE est traduite en unité métier (euros ou kWh comparés à une référence).
• Les coefficients sont interprétés et leur cohérence physique discutée.
• Une projection à douze mois est produite, avec saisonnalité et marge d'erreur.

**C3.2 — Process ML, niveau adapter**
• La séparation entraînement / test est correcte, sans fuite.
• Le choix des variables explicatives est justifié.

**C1.6 — API, niveau transposer**
• Les données météo sont récupérées par API de façon autonome.
• La collecte est robuste (gestion des erreurs, des coordonnées, des périodes).

**Restitution**
• La prévision est accompagnée d'une marge explicite et défendable.
• Au moins une limite du modèle est énoncée spontanément.

## Ressources

- Open-Meteo — API historique : https://open-meteo.com/en/docs/historical-weather-api
- scikit-learn — régression linéaire : https://scikit-learn.org/stable/modules/linear_model.html
- scikit-learn — métriques de régression : https://scikit-learn.org/stable/modules/model_evaluation.html#regression-metrics
- RTE éCO2mix — données de consommation : https://www.rte-france.com/eco2mix
- Comprendre R², RMSE et MAE : https://scikit-learn.org/stable/modules/model_evaluation.html
