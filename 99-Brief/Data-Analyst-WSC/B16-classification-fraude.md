# Brief B16 — Détecter la fraude : classification déséquilibrée et premiers biais du modèle

## Informations

| | |
|---|---|
| **Semaine** | S20 · 8–12 fév 2027 · 5 jours · Ayoub |
| **Modalité · Évaluation** | Individuel · Sommatif |
| **Compétences visées** | C3.4 · C3.6 · C3.7 · C3.3 · C3.2 · C3.1 · C1.7 |

## Description

Sur 285 000 transactions, 0,17 % sont frauduleuses. Un modèle qui prédit « jamais de fraude » a 99,8 % de justesse et ne sert à rien. Vous apprenez à classer l'introuvable, à lire les vraies métriques, et à regarder qui votre modèle accuse à tort.

## Contexte

Un établissement de paiement traite des millions de transactions par carte. Une infime fraction est frauduleuse — de l'ordre de deux pour mille — mais chacune coûte cher et entame la confiance. L'établissement veut un système d'alerte qui signale les transactions suspectes pour contrôle humain.

Le responsable lutte anti-fraude pose le problème avec lucidité : « Si je vous demande un modèle précis, vous allez me sortir un truc qui dit "pas de fraude" à tous les coups et qui a raison 99,8 % du temps. Ça ne m'intéresse pas. Ce qui m'intéresse, c'est : combien de fraudes réelles vous rattrapez, et combien de clients honnêtes vous embêtez pour y arriver. »

Il vient de formuler, dans ses mots, tout l'enjeu de la classification sur classes déséquilibrées. La justesse ne veut rien dire ici. Ce qui compte, c'est le rappel — quelle proportion des fraudes le modèle attrape — et la précision — quelle proportion de ses alertes sont justes. Les deux s'opposent : plus vous rattrapez de fraudes, plus vous générez de fausses alertes.

Et il y a une seconde question, éthique celle-là, que vous rencontrez pour la première fois. Un modèle qui signale des transactions « suspectes » signale en réalité des personnes. Qui votre modèle accuse-t-il à tort ? Ces faux positifs se répartissent-ils au hasard, ou frappent-ils davantage certains profils ? C'est le début du contrôle des biais — une compétence que le référentiel exige et que la détection de fraude illustre mieux que tout autre cas, parce que l'erreur y a un coût humain visible.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C3.4** — Modéliser des classifications et interpréter les métriques associées afin de catégoriser automatiquement des informations *(niveau 1 — imiter)*
- **C3.6** — Contrôler et documenter les biais d'un modèle et des données d'entraînement afin d'estimer les risques éthiques *(niveau 1 — imiter)*
- **C3.7** — Communiquer et vulgariser le fonctionnement interne d'un algorithme afin d'éviter le phénomène de boîte noire *(niveau 1 — imiter)*
- **C3.3** — Modéliser des régressions *(niveau 2 — adapter)*
- **C3.2** — Maîtriser le process ML *(niveau 2 — adapter)*
- **C3.1** — Utiliser les statistiques descriptives *(niveau 3 — transposer)*
- **C1.7** — Contrôler les enjeux du RGPD *(niveau 3 — transposer)*

## Modalités pédagogiques

**Organisation** : individuel.

**Jour 1 — matin (lancement, 2 h)**. Le formateur joue le responsable anti-fraude. Vous recevez le jeu de transactions. Vous mesurez le déséquilibre et comprenez pourquoi la justesse est un piège.

**Jour 1 — après-midi**. Vous entraînez un premier modèle naïf et constatez qu'il « réussit » en ne détectant rien.

**Jour 2 — matin (apport flash, 2 h 30)**. Classification : arbres de décision, forêts aléatoires. La matrice de confusion. Précision, rappel, F1, AUC — ce que chacun mesure et pourquoi l'accuracy trompe sur classes déséquilibrées. Le compromis précision / rappel et le réglage du seuil.

**Jour 3 — matin (apport flash, 1 h 30)**. Premiers biais : lire l'importance des variables, examiner la répartition des faux positifs selon les profils, formuler un risque éthique. Vulgariser une décision de modèle en langage clair.

**Jours 2 à 4 — production**.
1. **Mesurer le déséquilibre** et écarter d'emblée l'accuracy comme métrique principale.
2. **Classer** — un modèle de classification. Séparez, entraînez, prédisez (réactivation B14).
3. **Évaluer vraiment** — matrice de confusion, précision, rappel, F1, AUC. Traduisez : combien de fraudes attrapées, combien d'honnêtes dérangés ?
4. **Régler** — ajustez le seuil selon la priorité du métier. Documentez l'arbitrage.
5. **Auditer** — quelles variables pèsent ? Les faux positifs frappent-ils certains profils ? Formulez un risque éthique.
6. **Vulgariser** — expliquez en quelques phrases, sans jargon, comment le modèle décide.

**Questions guidantes.** Pourquoi un modèle à 99,8 % de justesse peut-il être inutile ? Vaut-il mieux rattraper 90 % des fraudes en dérangeant 5 % des clients, ou 60 % en n'en dérangeant que 0,5 % — et qui doit trancher, vous ou le métier ? Si votre modèle signale plus souvent certaines tranches de montants ou d'horaires, est-ce un biais problématique ou une réalité de la fraude ? Comment expliqueriez-vous une alerte à un client mécontent ?

**Jour 4 — après-midi (revue croisée)**. Un autre apprenant conteste votre choix de seuil et votre analyse de biais.

**Jour 5**. Finalisation, publication, restitution 8 minutes : les métriques réelles et l'audit de biais.

## Modalités d'évaluation

Brief **sommatif**, checklist complète.

Le cœur de l'évaluation est le **refus de l'accuracy** et la lecture juste des métriques adaptées. Un modèle même modeste, évalué au rappel et à la précision avec un arbitrage de seuil documenté, valide C3.4 ; un modèle brillant évalué à la seule justesse ne le valide pas.

Ce brief introduit C3.6 et C3.7 au niveau imiter, précisément là où le biais se voit — les faux positifs de la fraude sont des personnes. Cette amorce sera portée au niveau adapter en B17 puis au niveau transposer au palier 3.

## Données fournies (source exacte)

> Jeu **réel**, déjà **pseudonymisé à la source** (idéal pour aborder le RGPD sans donnée
> identifiante à manipuler).

- **Credit Card Fraud Detection** — Machine Learning Group, ULB (Bruxelles), diffusé sur Kaggle :
  https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- **284 807 transactions** (sept. 2013), dont **492 fraudes = 0,173 %**. Variables `V1`…`V28` =
  **composantes ACP** publiées à la place des données brutes ; seuls `Time` et `Amount` sont en clair.
- Le corrigé travaille sur un **échantillon** (`data/creditcard_sample.csv`, 60 492 lignes, **toutes les
  fraudes conservées** → 0,81 %) pour rester léger tout en gardant un **fort déséquilibre**. Le jeu
  intégral se télécharge via le lien ci-dessus.

## Livrables attendus

**Un dépôt GitHub public** :

1. `README.md` — problème, démarche, métriques clés, auteur.
2. `modele.ipynb` — déséquilibre, classification, matrice de confusion, métriques, réglage du seuil.
3. `audit-biais.md` — importance des variables, répartition des faux positifs, risque éthique formulé.
4. `vulgarisation.md` — une demi-page expliquant à un non-technicien comment le modèle décide.

## Critères de performance

**C3.4 — Classification, niveau imiter**
• Un modèle de classification est entraîné et évalué.
• La matrice de confusion est produite et lue.
• Précision, rappel, F1 et AUC sont calculés ; l'accuracy est explicitement écartée comme métrique principale.
• Le seuil de décision est ajusté selon une priorité métier, et l'arbitrage est documenté.
• Les métriques sont traduites en langage métier (fraudes attrapées / clients dérangés).

**C3.6 — Biais, niveau imiter**
• L'importance des variables est examinée.
• La répartition des faux positifs est analysée selon au moins un profil.
• Au moins un risque éthique concret est formulé.

**C3.7 — Vulgarisation, niveau imiter**
• Le fonctionnement du modèle est expliqué en langage clair, sans jargon, sur une demi-page.

**C3.2 / C3.3 / C3.1 — Réactivation**
• La séparation entraînement / test est correcte.
• Le profil statistique des fraudes vs transactions normales est produit.

**C1.7 — Réactivation, niveau transposer**
• La nature personnelle des données de transaction est prise en compte dans l'analyse de risque.

## Ressources

- Credit Card Fraud Detection (jeu de données) : https://www.kaggle.com/datasets/mlg-ulb/creditcardfraud
- scikit-learn — arbres et forêts : https://scikit-learn.org/stable/modules/ensemble.html#forest
- scikit-learn — métriques de classification : https://scikit-learn.org/stable/modules/model_evaluation.html#classification-metrics
- scikit-learn — matrice de confusion : https://scikit-learn.org/stable/modules/generated/sklearn.metrics.confusion_matrix.html
- scikit-learn — données déséquilibrées : https://imbalanced-learn.org/stable/
- scikit-learn — importance des variables : https://scikit-learn.org/stable/modules/permutation_importance.html
