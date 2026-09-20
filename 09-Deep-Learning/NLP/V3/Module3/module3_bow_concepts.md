---
title: 'Module 3 - Bag of Words : Concepts'
description: 'Formation NLP - Module 3 - Bag of Words : Concepts'
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# 🎒 Bag of Words : Concepts

Transformer le texte en nombres : la méthode fondamentale

[🏠 Index Module 3](index.md) [← Introduction](module3_intro.md) [Démonstrations →](module3_bow_demo.md)

## 🧠 Le Concept Fondamental

### 🎯 L'Idée Simple mais Puissante

Le **Bag of Words** (sac de mots) est la technique la plus intuitive pour vectoriser du texte :

#### **Principe Central :**

Compter combien de fois chaque mot apparaît dans chaque document

Document → Vecteur de comptages

**🏠 Analogie simple :**  
Imaginez que vous triez vos courses dans des paniers étiquetés.  
• Chaque panier = un mot du vocabulaire  
• Chaque produit dans le panier = une occurrence du mot  
→ Votre liste de courses devient un vecteur de comptages !

### 📊 Transformation Mathématique

#### Exemple Concret

**Documents :**

*   Doc 1: "Le chat mange des croquettes"
*   Doc 2: "Le chien mange aussi des croquettes"
*   Doc 3: "Le chat boit de l'eau"

**Vocabulaire créé :**

le chat mange des croquettes chien aussi boit de l'eau

**Matrice Bag of Words :**

Document

le

chat

mange

des

croquettes

chien

aussi

boit

de

l'eau

**Doc 1**

1

1

1

1

1

0

0

0

0

0

**Doc 2**

1

0

1

1

1

1

1

0

0

0

**Doc 3**

1

1

0

0

0

0

0

1

1

1

## 🔢 Formalisation Mathématique

### 📐 Algorithme Détaillé

**Étape 1 : Construction du Vocabulaire**  
V = {w₁, w₂, ..., wₙ} où n = |vocabulaire|

**Explication :** On collecte tous les mots uniques de tous les documents. Chaque mot distinct devient une dimension dans notre espace vectoriel. Si nous avons 10 000 mots uniques, nous travaillons dans un espace à 10 000 dimensions !

**Exemple concret :**  
Corpus : \["Le chat dort", "Le chien mange", "Le chat mange"\]  
→ V = {le, chat, dort, chien, mange} → n = 5 dimensions

**Étape 2 : Matrice de Comptage**  
BoW\[i,j\] = count(wⱼ in dᵢ)  
où dᵢ = document i, wⱼ = mot j du vocabulaire

**Explication :** Pour chaque document (ligne i) et chaque mot du vocabulaire (colonne j), on compte combien de fois ce mot apparaît. Cela crée une matrice documents × mots.

**Matrice résultante :**

Doc\\Mot

le

chat

dort

chien

mange

Doc 1

1

1

1

0

0

Doc 2

1

0

0

1

1

Doc 3

1

1

0

0

1

### 📊 Propriétés Mathématiques

#### Dimension de l'Espace

dim(BoW) = |V| = nombre de mots uniques

**Implications :**  
• Corpus anglais typique : 10 000 - 50 000 dimensions  
• Wikipedia : > 1 000 000 dimensions  
• Espace très sparse (creux) : 95-99% de zéros

#### Distance et Similarité

**Distance Euclidienne :**  
d(d₁, d₂) = ||BoW\[d₁\] - BoW\[d₂\]||₂  
  
**Similarité Cosinus :**  
sim(d₁, d₂) = (BoW\[d₁\] · BoW\[d₂\]) / (||BoW\[d₁\]||₂ × ||BoW\[d₂\]||₂)

La similarité cosinus mesure l'angle entre deux vecteurs (0 = orthogonaux, 1 = identiques). Plus adaptée que la distance euclidienne pour des documents de longueurs différentes.

## ⚖️ Avantages vs Limitations

#### ✅ Avantages

*   **Simplicité :** Facile à comprendre et implémenter
*   **Rapidité :** Calcul très rapide
*   **Interprétabilité :** Résultats explicables
*   **Baseline solide :** Point de départ efficace
*   **Peu de paramètres :** Pas d'hyperparamètres complexes
*   **Robustesse :** Fonctionne sur tout type de texte

#### ❌ Limitations

*   **Perte d'ordre :** Ignore la séquence des mots
*   **Sparsité :** Beaucoup de zéros dans la matrice
*   **Dimension élevée :** Vocabulaire peut être très grand
*   **Pas de sémantique :** "bon" ≠ "excellent"
*   **Sensible au bruit :** Fautes de frappe problématiques
*   **Mots fréquents :** "le", "de" dominent

### 🎯 Quand Utiliser BoW ?

**✅ Cas d'usage recommandés :**

*   **Classification de documents :** Spam/Ham, thématiques
*   **Analyse de sentiment basique :** Positif/Négatif
*   **Recherche par mots-clés :** Moteurs de recherche simples
*   **Baseline pour comparaison :** Avant modèles complexes
*   **Datasets petits/moyens :** < 100k documents
*   **Applications temps réel :** Rapidité prioritaire

**❌ Éviter BoW pour :**

*   **Traduction automatique :** Ordre crucial
*   **Génération de texte :** Séquence nécessaire
*   **Analyse syntaxique :** Structure grammaticale
*   **Similarité sémantique :** Sens des mots important
*   **Textes longs :** Livres, articles complets

### Navigation

[🏠 Index Module 3](index.md) [← Introduction](module3_intro.md) [Démonstrations →](module3_bow_demo.md) [🏠 Accueil Formation](../index.html)
