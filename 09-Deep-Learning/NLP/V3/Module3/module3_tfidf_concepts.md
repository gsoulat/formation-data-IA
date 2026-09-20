---
title: 'Module 3 - TF-IDF : Concepts'
description: 'Formation NLP - Module 3 - TF-IDF : Concepts'
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# ⚖️ TF-IDF : Concepts

Pondération Intelligente : Tous les mots ne se valent pas !

[🏠 Index Module 3](index.md) [← BoW Démo](module3_bow_demo.md) [Démonstrations →](module3_tfidf_demo.md)

## 🤔 Le Problème du Bag of Words

### ⚠️ Tous les Mots ont le Même Poids !

**🚨 Problème central de BoW :**  
Dans BoW, "le" = "Python" = "blockchain" = "révolutionnaire"  
Tous comptent pareil ! Mais certains mots sont plus informatifs que d'autres...

#### 🧪 Démonstration du Problème

Analysons ces 3 articles de presse :

##### 📰 Article 1 - Tech

"Le Python transforme le machine learning. Le langage Python révolutionne l'IA."

##### 📰 Article 2 - Cuisine

"Le chef prépare le plat. Le restaurant sert le meilleur plat de la région."

##### 📰 Article 3 - Sport

"Le joueur marque le but. Le stade acclame le joueur pour son but."

**💡 Observation :**  
Le mot "le" apparaît partout → pas discriminant  
Les mots "Python", "chef", "joueur" sont spécifiques → très informatifs  
**🎯 Solution : TF-IDF !**

## 🧮 Le Concept TF-IDF

### 📐 L'Idée Géniale

**TF-IDF** = **T**erm **F**requency × **I**nverse **D**ocument **F**requency

#### 🎯 Principe Central

Un mot est important s'il est :  
**FRÉQUENT** dans le document ET **RARE** dans la collection

#### 📈 Term Frequency (TF)

**Question :** À quel point ce mot est-il important dans CE document ?

TF(t,d) = count(t in d) / |d|

Fréquence du terme t dans le document d

#### 📉 Inverse Document Frequency (IDF)

**Question :** À quel point ce mot est-il rare dans TOUTE la collection ?

IDF(t) = log(N / df(t))

N = total docs, df(t) = docs contenant t

#### 🏆 Formule Finale TF-IDF

**TF-IDF(t,d) = TF(t,d) × IDF(t)**

*Score élevé = Mot fréquent localement ET rare globalement*

## 🔢 Calculs Détaillés

### ✏️ Exemple Étape par Étape

#### 📚 Corpus d'exemple :

*   Doc 1: "Python est un langage de programmation"
*   Doc 2: "Java est aussi un langage de programmation"
*   Doc 3: "Machine learning utilise Python"

1 **Calcul Term Frequency (TF)**

Pour chaque mot dans chaque document :

Doc 1: "Python"(1/6) = 0.167, "langage"(1/6) = 0.167  
Doc 2: "Java"(1/7) = 0.143, "langage"(1/7) = 0.143  
Doc 3: "Python"(1/3) = 0.333, "machine"(1/3) = 0.333

2 **Calcul Inverse Document Frequency (IDF)**

Pour chaque mot unique du vocabulaire :

"Python": log(3/2) = 0.176 (dans 2 docs sur 3)  
"Java": log(3/1) = 0.477 (dans 1 doc sur 3)  
"langage": log(3/2) = 0.176 (dans 2 docs sur 3)

3 **Calcul TF-IDF Final**

Multiplication TF × IDF :

Doc 1 "Python": 0.167 × 0.176 = 0.029  
Doc 2 "Java": 0.143 × 0.477 = 0.068  
Doc 3 "Python": 0.333 × 0.176 = 0.059

**🎯 Interprétation :**  
• "Java" a le score TF-IDF le plus élevé (0.068) car il est rare dans le corpus  
• "Python" a des scores différents selon le document (fréquence locale)  
• Les mots communs comme "un", "de" auront des scores faibles

## 📐 Variantes et Optimisations

### 🔧 Variantes de TF

Variant TF

Formule

Avantage

Usage

**Raw Count**

count(t, d)

Simple, direct

Documents similaires

**Term Frequency**

count(t, d) / |d|

Normalise par longueur

Documents variables

**Log Normalization**

1 + log(count(t, d))

Réduit l'impact extrême

Corpus très variables

**Boolean**

1 si t ∈ d, 0 sinon

Présence/absence

Classification binaire

### 🔧 Variantes d'IDF

Variant IDF

Formule

Avantage

Problème résolu

**Standard**

log(N / df(t))

Simple, efficace

\-

**Smooth**

log(N / (1 + df(t)))

Évite division par 0

Mots très rares

**Max**

log(max(df) / df(t))

Normalisation relative

Corpus déséquilibrés

**Probabilistic**

log((N - df(t)) / df(t))

Interprétation probabiliste

Modélisation formelle

## ⚔️ BoW vs TF-IDF : Le Duel

#### 🎒 Bag of Words

*   ✅ **Simple** : Facile à comprendre
*   ✅ **Rapide** : Calcul très efficace
*   ✅ **Baseline** : Bon point de départ
*   ❌ **Naïf** : Tous mots égaux
*   ❌ **Bruiteux** : Stopwords dominants
*   ❌ **Peu discriminant** : Mauvaise sélectivité

#### ⚖️ TF-IDF

*   ✅ **Intelligent** : Pondération adaptée
*   ✅ **Discriminant** : Mots rares valorisés
*   ✅ **Robuste** : Moins sensible au bruit
*   ❌ **Plus complexe** : Calculs supplémentaires
*   ❌ **Dépendant corpus** : IDF varie
*   ❌ **Mémoire** : Stockage des statistiques

### 📊 Quand Utiliser Chaque Méthode ?

Contexte

BoW

TF-IDF

Recommandation

**Corpus homogène**

🟢 Bon

🟡 Neutre

BoW suffisant

**Corpus hétérogène**

🔴 Faible

🟢 Excellent

TF-IDF obligatoire

**Classification**

🟡 Acceptable

🟢 Meilleur

TF-IDF recommandé

**Recherche**

🔴 Mauvais

🟢 Excellent

TF-IDF essentiel

**Temps réel**

🟢 Rapide

🟡 Moyen

BoW si contraintes

**Petit corpus**

🟢 Stable

🔴 Instable

BoW plus sûr

### Navigation

[🏠 Index Module 3](index.md) [← BoW Démo](module3_bow_demo.md) [TF-IDF Démo →](module3_tfidf_demo.md) [🏠 Accueil Formation](../index.html)
