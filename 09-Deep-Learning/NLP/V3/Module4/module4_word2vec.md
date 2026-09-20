---
title: 'Module 4 - Word2Vec : Comprendre les Embeddings de Mots'
description: 'Formation NLP - Module 4 - Word2Vec : Comprendre les Embeddings de Mots'
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# 🧠 Word2Vec : Comprendre les Embeddings de Mots

La révolution qui a transformé le traitement du langage naturel

**🎯 L'idée géniale de Word2Vec :**  
"Les mots qui apparaissent dans des contextes similaires ont des significations similaires"

[← Index Module 4](index.md)

**Word2Vec - De débutant à expert**  
Google Research, 2013

[Notebook Pratique →](notebook/module4_word2vec_demo.ipynb)

## 1\. 🌟 Qu'est-ce que Word2Vec ?

#### 💡 Le problème avant Word2Vec

Imaginez que vous devez expliquer à un ordinateur ce qu'est un "chat". Avant Word2Vec, on représentait chaque mot par un numéro unique :

*   chat = \[0, 0, 1, 0, 0, ...\] (un seul 1 parmi des milliers de 0)
*   chien = \[0, 0, 0, 1, 0, ...\] (un 1 à une position différente)

**Problème :** L'ordinateur ne sait pas que "chat" et "chien" sont similaires !

#### ✨ La solution Word2Vec

**Word2Vec** transforme chaque mot en un petit vecteur dense qui capture sa signification :

*   chat = \[0.2, -0.5, 0.8, 0.1, ...\] (100 dimensions par exemple)
*   chien = \[0.3, -0.4, 0.7, 0.2, ...\] (vecteur similaire car sens proche)

**Révolution :** Maintenant l'ordinateur "comprend" que chat et chien sont proches !

#### 🔍 Exemple concret

**Phrase 1 :** "Le chat dort sur le canapé"

**Phrase 2 :** "Le chien dort sur le canapé"

**Résultat :** Word2Vec remarque que "chat" et "chien" apparaissent dans le même contexte, donc leurs vecteurs deviennent similaires !

### 🎯 Pourquoi c'est révolutionnaire ?

*   **Capture la sémantique :** Les mots similaires ont des vecteurs proches
*   **Relations mathématiques :** roi - homme + femme ≈ reine
*   **Efficace :** Vecteurs compacts (100-300 dimensions)
*   **Non supervisé :** Apprend tout seul à partir de texte brut

## 2\. 🏗️ Les Deux Architectures

Word2Vec propose deux méthodes pour apprendre ces vecteurs magiques :

#### 📖 CBOW (Continuous Bag of Words)

**Mission :** "Devine le mot manquant"

**Exemple :**  
Contexte : \["Le", "\_\_\_", "mange", "des", "croquettes"\]  
Prédiction : "chat"

Plus rapide

Bon pour mots fréquents

**Architecture :** Plusieurs mots en entrée → Un mot en sortie

#### 🎯 Skip-gram

**Mission :** "Devine le contexte"

**Exemple :**  
Mot central : "chat"  
Prédiction : \["Le", "mange", "des", "croquettes"\]

Meilleur qualité

Excellent pour mots rares

**Architecture :** Un mot en entrée → Plusieurs mots en sortie

## 3\. 🎬 Comment ça fonctionne ?

### 📚 Le processus d'apprentissage étape par étape

**Étape 1 - Préparation :** Transforme "Le chat mange" en \["le", "chat", "mange"\]

**Étape 2 - Fenêtre glissante :** Regarde 2 mots avant et après chaque mot central

#### 🪟 Exemple avec fenêtre de taille 2

```
[le, chat, mange, des, croquettes]
     ↑
   mot central

Contexte de "chat" : [le, mange]
```

**Étape 3 - Apprentissage :** Le modèle ajuste les vecteurs pour que les mots qui apparaissent ensemble aient des vecteurs proches

**Étape 4 - Répétition :** Fait cela pour des millions de phrases jusqu'à capturer tous les patterns

#### ✨ La magie des vecteurs

Après l'entraînement, on obtient des propriétés étonnantes :

*   **Similarités :** distance(chat, chien) < distance(chat, voiture)
*   **Analogies :** roi - homme + femme ≈ reine
*   **Clustering :** Les mots du même domaine se regroupent

## 4\. 🔧 Les Paramètres Clés

Pour configurer Word2Vec, voici les paramètres importants à comprendre :

#### 📏 vector\_size

Dimension des vecteurs de mots

Recommandé : 100-300

**Impact :** Plus grand = plus précis mais plus lent

#### 🪟 window

Taille de la fenêtre de contexte

Recommandé : 5-10

**Impact :** Plus grand = relations plus larges

#### 🎯 sg (Skip-gram)

Choix de l'architecture

0 = CBOW, 1 = Skip-gram

**Impact :** Skip-gram généralement meilleur

#### 📊 min\_count

Fréquence minimale des mots

Recommandé : 5-10

**Impact :** Ignore les mots trop rares

#### 🔄 epochs

Nombre d'itérations d'entraînement

Recommandé : 50-200

**Impact :** Plus = meilleur apprentissage

#### 👥 workers

Nombre de processeurs utilisés

Recommandé : 4-8

**Impact :** Accélère l'entraînement

**\# Configuration recommandée :**  
model = Word2Vec(  
    vector\_size=100,    # Dimension des vecteurs  
    window=5,           # Taille du contexte  
    min\_count=5,        # Ignorer les mots rares  
    sg=1,               # Skip-gram  
    epochs=100          # Nombre d'itérations  
)

## 5\. 🚀 Applications Pratiques

Word2Vec n'est pas juste théorique - voici comment on l'utilise dans la vraie vie :

#### 🔍 Recherche Sémantique

**Usage :** Trouver des documents similaires même s'ils n'utilisent pas les mêmes mots

**Exemple :** Chercher "voiture" trouve aussi "automobile", "véhicule", "auto"

#### 💡 Système de Recommandation

**Usage :** Suggérer des produits ou contenus similaires

**Exemple :** Si vous aimez "iPhone", proposer "Samsung", "smartphone", "mobile"

#### 🎯 Analyse de Sentiment

**Usage :** Comprendre les émotions dans les textes

**Exemple :** Détecter que "génial", "fantastique", "super" sont positifs

#### 🌍 Traduction Automatique

**Usage :** Aligner les mots entre langues

**Exemple :** "chat" en français correspond à "cat" en anglais

#### 📊 Classification de Texte

**Usage :** Catégoriser automatiquement des documents

**Exemple :** Trier des emails en "important", "spam", "personnel"

#### 🤖 Chatbots

**Usage :** Comprendre les intentions des utilisateurs

**Exemple :** "Réserver", "Commander", "Acheter" = même intention

#### 🧮 Les analogies magiques

Voici les exemples les plus impressionnants de Word2Vec :

*   **roi - homme + femme ≈ reine** (relations de genre)
*   **Paris - France + Italie ≈ Rome** (capitales)
*   **marcher - marche + cours ≈ courir** (conjugaisons)
*   **grand - plus grand + plus petit ≈ petit** (comparatifs)

## 6\. ⚖️ Avantages et Limitations

#### ✅ Avantages

*   **Capture la sémantique :** Comprend le sens des mots
*   **Efficace :** Vecteurs compacts et rapides
*   **Relations mathématiques :** Analogies fonctionnent
*   **Pré-entraîné disponible :** Modèles prêts à utiliser
*   **Non supervisé :** Apprend sans annotations
*   **Polyvalent :** Fonctionne sur tous domaines

#### ❌ Limitations

*   **Polysémie :** "avocat" (fruit) = "avocat" (métier)
*   **Mots nouveaux :** Ne gère pas les mots non vus
*   **Besoin de données :** Millions de mots nécessaires
*   **Contexte fixe :** Fenêtre limitée
*   **Pas de composition :** Difficile pour phrases complètes
*   **Biais :** Reproduit les stéréotypes du texte

#### 💡 Exemple de limitation : la polysémie

Word2Vec donne **un seul vecteur** par mot, donc :

*   "J'ai mangé un avocat" (fruit) 🥑
*   "Mon avocat défend mon dossier" (métier) ⚖️

→ Le même vecteur pour les deux sens ! C'est pourquoi on a créé des modèles plus récents.

## 7\. 🚀 Évolution vers les Modèles Modernes

Word2Vec a ouvert la voie à une révolution en NLP. Voici l'évolution :

2013

**Word2Vec** - Le pionnier des embeddings denses

2014

**GloVe** - Combine approche locale et globale

2016

**FastText** - Gère les mots hors vocabulaire

2018

**ELMo** - Premiers embeddings contextuels

2018

**BERT** - Révolution des Transformers bidirectionnels

2019+

**GPT, T5, etc.** - Modèles de langage géants

#### 🎯 Pourquoi Word2Vec reste important ?

*   **Fondamental :** Base pour comprendre les embeddings modernes
*   **Efficace :** Parfait pour applications simples et rapides
*   **Ressources limitées :** Fonctionne sur un ordinateur portable
*   **Pédagogique :** Excellent pour apprendre les concepts
*   **Toujours utilisé :** Dans beaucoup d'applications industrielles

[← Index Module 4](index.md)

**Prêt pour la pratique ?**  
Essayez le notebook interactif

[Notebook Pratique →](notebook/module4_word2vec_demo.ipynb)
