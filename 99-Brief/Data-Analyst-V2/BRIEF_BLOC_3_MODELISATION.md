# Brief Bloc 3 — Modéliser les données et prévoir avec le Machine Learning

## Informations

| Critère | Valeur |
|---------|--------|
| **Bloc** | Bloc 3 — Modélisation des données structurées : corrélations & Machine Learning |
| **Durée** | ~2 semaines (10 jours) |
| **Niveau** | Intermédiaire → avancé |
| **Modalité** | Binôme |
| **Technologies** | Python, pandas, scikit-learn, matplotlib/seaborn, Jupyter |
| **Prérequis** | [Statistiques descriptives](../../01-Fondamentaux/Mathematiques/03-Statistiques-Descriptives/) · [Machine Learning](../../08-Machine-Learning/) · [NLP](../../09-Deep-Learning/NLP/) |

## Description rapide

En binôme, vous passez de la description à la **prévision**. À partir des données propres de
NordRetail, vous identifiez les **corrélations** (statistiques descriptives), puis vous entraînez
des modèles de **Machine Learning** : une **régression** pour prévoir une valeur numérique
(le CA), une **classification** pour catégoriser (clients ou paniers), et une analyse de
**sentiments** (NLP) sur des avis clients. Vous interprétez les métriques, documentez les
**biais** et **vulgarisez** vos modèles pour éviter l'effet « boîte noire ».

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- Utiliser les **statistiques descriptives** (variance, quantiles, corrélation) pour faire émerger des informations.
- Maîtriser le **process ML** : découpage entraînement/validation, entraînement, prédiction, mesure.
- Modéliser une **régression** et interpréter ses métriques (prévision numérique).
- Modéliser une **classification** et interpréter ses métriques (catégorisation).
- Réaliser une **analyse de sentiments** (NLP) à partir de texte brut.
- **Contrôler les biais** d'un modèle et **vulgariser** son fonctionnement.

## Contexte

**L'entreprise et son problème**

NordRetail dispose maintenant de données fiables et sait décrire son passé. Mais la direction
veut **anticiper** : peut-on prévoir le chiffre d'affaires du mois prochain ? repérer les
clients à fort potentiel ? comprendre ce que disent les avis en ligne ? Et surtout : peut-on
faire confiance à ces modèles, ou reproduisent-ils des biais ?

**La question centrale**

> « Que peut-on prévoir à partir des données de NordRetail, avec quelle fiabilité, et quels biais
> faut-il surveiller ? »

**Les données fournies**

Le jeu propre [`../Data-Analyst/data/`](../Data-Analyst/data/) (ventes, produits, clients,
schéma en étoile `Faits_Ventes.csv` + `Dim_*`). Pour l'analyse de sentiments, vous constituez
un petit corpus d'avis clients (fourni ou simulé) à classer en positif/négatif.

## Modalités pédagogiques

Projet en BINÔME sur ~10 jours, dépôt GitHub public. **Périmètre Data Analyst** : on **utilise**
le ML pour analyser et prévoir, on n'industrialise pas (pas de MLOps).

### Phase 1 — Statistiques & corrélations (J1-J2)

Décrivez les relations dans les données : matrice de **corrélation**, variance, quantiles.
Quelles variables sont liées au CA (surface magasin, catégorie, remise, saison) ? Ces
corrélations orientent le choix des variables explicatives (features). Attention : corrélation
n'est pas causalité.

### Phase 2 — Régression : prévoir le CA (J3-J5)

Modélisez une **régression** (linéaire, puis éventuellement arbre/forêt) pour prévoir une valeur
numérique (CA mensuel ou par magasin). Appliquez le **process ML** : split train/validation,
entraînement, prédiction, **mesure** (MAE, RMSE, R²). Interprétez : le modèle prévoit-il mieux
qu'une moyenne naïve ? Quelles variables pèsent le plus ?

### Phase 3 — Classification : catégoriser (J5-J7)

Modélisez une **classification** : par exemple prédire si un panier est « à forte marge », ou
segmenter les clients. Interprétez les métriques adaptées (**accuracy, précision, rappel, F1**,
matrice de confusion). Pourquoi l'accuracy seule peut-elle tromper sur des classes déséquilibrées ?

### Phase 4 — Analyse de sentiments (NLP) (J7-J8)

Sur un corpus d'avis clients, réalisez une **analyse de sentiments** : nettoyage du texte,
vectorisation simple (BoW / TF-IDF), classifieur (régression logistique ou Naive Bayes),
évaluation. Quels mots pèsent dans un avis négatif ?

### Phase 5 — Biais, vulgarisation & restitution (J9-J10)

Documentez les **biais** possibles (données d'entraînement non représentatives, variables
sensibles) et les limites de vos modèles. Rédigez une **explication vulgarisée** de chaque
modèle destinée à un décideur non technique (éviter la « boîte noire »). Présentez vos prévisions
et vos réserves.

## Modalités d'évaluation

- **Notebook & analyse (60 %)** : justesse du process ML, interprétation correcte des métriques,
  pertinence des features, qualité de l'analyse de sentiments, lucidité sur les biais.
- **Restitution orale (40 %)** : 12 min de présentation vulgarisée des modèles et prévisions +
  8 min de questions.

**Validation partielle** : un binôme qui livre une régression et une classification correctement
évaluées et interprétées, même sans NLP abouti, valide les acquis de modélisation.

## Livrables attendus

- Un **dépôt GitHub public** contenant :
  - un **notebook** régression (process complet + métriques + interprétation) ;
  - un **notebook** classification (métriques adaptées + matrice de confusion) ;
  - un **notebook** analyse de sentiments (NLP) ;
  - une analyse des **corrélations** (matrice + commentaires) ;
  - un **`README.md`** complet.
- Une **note « biais & limites »** + une **fiche de vulgarisation** d'un modèle pour un décideur.

## Critères de performance

**Statistiques & corrélations**
- Variance, quantiles et coefficients de corrélation sont utilisés pour expliquer les données.

**Process de Machine Learning**
- Le découpage entraînement/validation, l'entraînement, la prédiction et la mesure sont corrects.

**Régression & classification**
- La régression est modélisée et ses métriques (MAE/RMSE/R²) sont interprétées.
- La classification est modélisée et ses métriques (précision/rappel/F1, confusion) sont interprétées.

**NLP & éthique**
- Un corpus de texte est traité et catégorisé automatiquement (analyse de sentiments).
- Les biais du modèle et des données sont documentés ; le fonctionnement est vulgarisé (pas de boîte noire).

## Ressources

- Cours — [Machine Learning](../../08-Machine-Learning/) (cibler 01, 02, 06, 07, 09, 12, 13) · [Interprétabilité & éthique](../../08-Machine-Learning/cours/14-interpretabilite-ethique.md)
- Cours — [NLP](../../09-Deep-Learning/NLP/) (Modules 2-3 : nettoyage, BoW/TF-IDF)
- Cours — [Statistiques descriptives](../../01-Fondamentaux/Mathematiques/03-Statistiques-Descriptives/)
- Brief connexe — [Analyse de sentiments](../Dev-IA/Deep-Learning-NLP/BRIEF_ANALYSE_SENTIMENTS.md)
- Données NordRetail : [`../Data-Analyst/data/`](../Data-Analyst/data/)
- Étape précédente : [Bloc 2 — Traitement](BRIEF_BLOC_2_TRAITEMENT.md) · Suivante : [Bloc 4 — Visualisation](BRIEF_BLOC_4_VISUALISATION.md)
