# Brief B14 — Premier modèle prédictif : le process ML de bout en bout

## Informations

| | |
|---|---|
| **Semaine** | S18 · 25–29 janv 2027 · 5 jours · Ayoub |
| **Modalité · Évaluation** | Individuel · Formatif |
| **Compétences visées** | C3.2 · C3.1 · C2.6 |

## Description

Une compagnie d'assurance perd des clients sans savoir lesquels vont partir. Vous construisez votre premier modèle prédictif complet — non pour obtenir le meilleur score, mais pour maîtriser chaque étape : séparer, entraîner, prédire, mesurer, et comprendre ce que le score veut dire.

## Contexte

Une compagnie d'assurance auto voit partir environ 15 % de ses clients chaque année. Reconquérir un client coûte cinq fois plus cher que d'en retenir un, mais l'entreprise agit à l'aveugle : elle découvre les départs quand ils sont consommés.

Le directeur commercial voudrait anticiper : « Si je savais, en début d'année, quels clients risquent de partir, je concentrerais mes efforts de fidélisation sur eux. » C'est exactement ce que le machine learning permet — apprendre, à partir des clients partis les années précédentes, à reconnaître ceux qui s'apprêtent à faire de même.

Vous disposez d'un historique : pour chaque ancien client, ses caractéristiques et le fait qu'il soit parti ou resté. C'est la matière première de l'apprentissage supervisé.

Cette semaine, l'objectif n'est pas la performance. Un modèle médiocre dont vous maîtrisez chaque étape vaut mieux qu'un modèle brillant que vous ne comprenez pas. Vous allez installer le geste fondamental du machine learning, celui que vous répéterez ensuite en régression, en classification, en NLP : séparer les données en entraînement et test, entraîner sur les premières, prédire sur les secondes, mesurer l'écart entre prédiction et réalité.

Le piège que vous devez comprendre cette semaine porte un nom : la fuite de données. Si vous mesurez votre modèle sur les données qui ont servi à l'entraîner, vous vous mentez. Comprendre pourquoi est le vrai enjeu.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C3.2** — Maîtriser le process d'apprentissage automatique : syntaxe, découpage jeu d'entraînement et de validation, entraînement, prédiction, mesure *(niveau 1 — imiter)*
- **C3.1** — Utiliser les statistiques descriptives *(niveau 3 — transposer)*
- **C2.6** — Nettoyer les données *(niveau 3 — transposer)*

## Modalités pédagogiques

**Organisation** : individuel.

**Jour 1 — matin (lancement, 2 h)**. Le formateur joue le directeur commercial. Vous recevez l'historique. Vous le profilez avec vos réflexes statistiques (réactivation B13) : qui sont les partis, en quoi diffèrent-ils des restés ?

**Jour 1 — après-midi**. Vous formulez des hypothèses : quelles variables semblent liées au départ ?

**Jour 2 — matin (apport flash, 2 h 30)**. Le process ML : la notion d'apprentissage supervisé, la séparation entraînement / test et pourquoi elle est vitale, la syntaxe scikit-learn (`fit`, `predict`), un premier modèle simple. La mesure : justesse, et pourquoi elle ne suffit pas.

**Jours 2 à 4 — production**.
1. **Préparer** — nettoyez et mettez en forme les données pour scikit-learn.
2. **Séparer** — jeu d'entraînement et jeu de test. Justifiez la proportion.
3. **Entraîner** — un modèle simple sur le jeu d'entraînement.
4. **Prédire** — sur le jeu de test, jamais vu à l'entraînement.
5. **Mesurer** — confrontez prédictions et réalité. Interprétez le score.
6. **Comparer** — confrontez ce que le modèle a « appris » à la segmentation descriptive de B13. Se rejoignent-ils ?

**Questions guidantes.** Pourquoi ne peut-on pas mesurer un modèle sur ses données d'entraînement ? Si votre modèle annonce 85 % de justesse mais que 85 % des clients restent, qu'a-t-il vraiment appris ? Que se passe-t-il si une variable de votre jeu contient déjà, indirectement, la réponse ? Un modèle qui se trompe est-il inutile, ou son erreur est-elle instructive ?

**Jour 4 — après-midi (revue croisée)**. Un autre apprenant vérifie que votre mesure est honnête : cherche-t-il une fuite de données dans votre démarche ?

**Jour 5**. Finalisation, publication, restitution 6 minutes.

## Modalités d'évaluation

Brief **formatif**. Auto-évaluation, revue croisée, retour collectif.

Le critère décisif n'est pas le score obtenu mais l'**honnêteté de la démarche** : séparation correcte, absence de fuite, interprétation lucide du résultat. Un apprenant qui obtient 70 % en comprenant exactement ce que ce chiffre signifie a mieux réussi qu'un apprenant qui affiche 95 % grâce à une fuite qu'il n'a pas vue.

C3.2 est au niveau imiter : reproduire le process complet sur un cas guidé suffit. La régression et la classification approfondiront aux semaines suivantes.

## Données fournies (source exacte)

> Jeu **réel** de télécom, sans donnée personnelle directe.

- **Jeu** : **Telco Customer Churn** (IBM) — 7 043 clients, 21 variables (ancienneté, contrat,
  services, facturation, `Churn`). Miroir public :
  `https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv`
- ⚠️ `TotalCharges` contient 11 valeurs vides (à convertir puis traiter).

## Livrables attendus

**Un dépôt GitHub public** :

1. `README.md` — problème, démarche, résultat, auteur.
2. `01-exploration.ipynb` — profil des partis vs restés, hypothèses.
3. `02-modele.ipynb` — préparation, séparation, entraînement, prédiction, mesure, chaque étape commentée.
4. `interpretation.md` — ce que signifie le score, les limites du modèle, la comparaison avec la segmentation B13.

## Critères de performance

**C3.2 — Process ML, niveau imiter**
• Les données sont séparées en jeu d'entraînement et jeu de test avant tout entraînement.
• La proportion de séparation est choisie et justifiée.
• Un modèle est entraîné avec la syntaxe scikit-learn (`fit`).
• La prédiction est faite sur le jeu de test uniquement (`predict`).
• Au moins une métrique est calculée et interprétée en langage métier.
• Aucune fuite de données : la mesure porte sur des données non vues à l'entraînement (vérifié en revue croisée).

**C3.1 — Réactivation, niveau transposer**
• Le profil comparé partis / restés est produit et exploité pour formuler des hypothèses.

**C2.6 — Réactivation, niveau transposer**
• Les données sont nettoyées et mises en forme pour scikit-learn de façon autonome.

**Interprétation**
• Le score est confronté à la répartition des classes (un modèle naïf est-il battu ?).
• La comparaison avec la segmentation descriptive B13 est menée.

## Ressources

- scikit-learn — mise en route : https://scikit-learn.org/stable/getting_started.html
- scikit-learn — train_test_split : https://scikit-learn.org/stable/modules/generated/sklearn.model_selection.train_test_split.html
- Telco Customer Churn (jeu de données) : https://www.kaggle.com/datasets/blastchar/telco-customer-churn
- scikit-learn — validation et évaluation : https://scikit-learn.org/stable/modules/cross_validation.html
- Comprendre la fuite de données (data leakage) : https://scikit-learn.org/stable/common_pitfalls.html
