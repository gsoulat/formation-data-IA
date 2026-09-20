---
title: Module 6 - Mécanismes d'Attention
description: Formation NLP - Module 6 - Mécanismes d'Attention
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# 🧠 Mécanismes d'Attention

Le cœur révolutionnaire des Transformers

**🎯 Question centrale :**  
"Comment permettre à un modèle de se concentrer sur les parties importantes d'une séquence ?"

[← Introduction](module6_introduction.md)

**Mécanismes d'Attention**  
Le cœur des Transformers

[Architecture Transformer →](module6_transformer_architecture.md)

## 1\. 🔍 Qu'est-ce que l'Attention ?

#### 🎭 Analogie : Une Soirée Cocktail

Imaginez-vous dans une soirée bruyante. Votre ami vous parle, mais il y a de la musique, d'autres conversations, des bruits de verres...

**Question :** Comment votre cerveau fait-il pour se concentrer sur la voix de votre ami ?

**Réponse :** Il utilise un mécanisme d'*attention sélective* qui amplifie les signaux importants et atténue le bruit.

**💡 C'est exactement ce que fait l'attention dans les Transformers !**

#### 🧠 L'Attention en NLP

Dans une phrase, tous les mots ne sont pas également importants pour comprendre chaque mot individuel. L'attention permet au modèle de décider quels mots regarder quand il traite un mot donné.

🎯 Démonstration Interactive : Attention en Action

Cliquez sur un mot pour voir sur quoi il "porte son attention" :

Le

chat

noir

mange

la

souris

Cliquez sur un mot pour voir son pattern d'attention

### 🔬 Les Types d'Attention

#### 🔄 Attention Croisée

Un mot porte attention à d'autres mots de la séquence. Utile pour la traduction.

**Exemple :** "chat" en français porte attention à "cat" en anglais.

#### 🪞 Self-Attention

Chaque mot porte attention à tous les mots de la même séquence, y compris lui-même.

**Révolution :** C'est la clé des Transformers !

## 2\. 🔑 Les Concepts Query, Key, Value

#### 🏛️ Analogie : Une Bibliothèque

Imaginez que vous cherchez des informations dans une bibliothèque immense :

*   **Query (Requête) :** "Je cherche des livres sur l'IA"
*   **Key (Clé) :** L'étiquette sur chaque étagère : "Informatique", "Histoire", "Sciences"...
*   **Value (Valeur) :** Le contenu réel des livres sur l'étagère

**Processus :** Votre requête compare avec chaque étiquette, trouve les plus pertinentes, et récupère le contenu correspondant.

🔍

#### Query (Q)

**"Qu'est-ce que je cherche ?"**

La représentation de ce que le mot actuel veut savoir sur les autres mots.

**Exemple :**  
Pour "mange", la query pourrait être : "Qui fait l'action ?" et "Quoi est mangé ?"

🗝️

#### Key (K)

**"Qu'est-ce que je peux offrir ?"**

La représentation de l'information que chaque mot peut fournir aux autres.

**Exemple :**  
"chat" pourrait avoir une key : "Je suis un sujet qui peut faire des actions"

💎

#### Value (V)

**"Quelle information je fournis ?"**

Le contenu réel de l'information à transmettre.

**Exemple :**  
La value de "chat" contient toute l'information sémantique sur ce qu'est un chat

#### 🔄 Le Processus d'Attention

1\. **Comparaison :** La Query de chaque mot compare avec toutes les Keys  
2\. **Score :** Plus la Query et la Key sont similaires, plus le score est élevé  
3\. **Pondération :** Les scores deviennent des poids d'attention (softmax)  
4\. **Agrégation :** Les Values sont combinées selon ces poids

## 3\. 📐 Les Mathématiques de l'Attention

#### 💡 Ne Paniquez Pas !

Les maths peuvent sembler intimidantes, mais le concept est simple : **calculer des similarités et faire des moyennes pondérées**.

**Formule de base de l'Attention :**  
  
Attention(Q,K,V) = softmax(QKT/√dk)V

### 🔢 Décomposition Étape par Étape

#### Étape 1 : Calcul des Scores

**Formule :** Scores = QKT

On multiplie chaque Query par toutes les Keys pour obtenir des scores de compatibilité.

Si Q = \[q₁, q₂, ...\] et K = \[k₁, k₂, ...\]  
Alors Score(i,j) = qᵢ · kⱼ

#### Étape 2 : Normalisation

**Formule :** Scores = Scores / √dk

On divise par la racine de la dimension pour stabiliser les gradients.

**Pourquoi ?** Sans cela, les scores deviennent trop grands et le softmax sature.

#### Étape 3 : Softmax

**Formule :** Weights = softmax(Scores)

Conversion des scores en probabilités qui somment à 1.

softmax(xᵢ) = exᵢ / Σⱼ exⱼ

#### Étape 4 : Agrégation Pondérée

**Formule :** Output = Weights × V

On combine les Values selon les poids d'attention calculés.

Résultat : une représentation enrichie qui capture les informations pertinentes.

#### 🎮 Démonstration Interactive

Matrice d'attention pour : "Le chat mange"

Le

chat

mange

Le

0.1

0.3

0.6

chat

0.2

0.5

0.3

mange

0.1

0.7

0.2

Passez la souris sur les cellules pour voir l'interprétation

Cliquez sur une cellule pour voir ce que signifie ce score d'attention

## 4\. 🧩 Multi-Head Attention

#### 👥 Analogie : Un Conseil d'Experts

Imaginez que vous demandez conseil pour acheter une voiture. Vous consultez :

*   **Expert 1 :** Se concentre sur la sécurité
*   **Expert 2 :** Se concentre sur l'économie
*   **Expert 3 :** Se concentre sur le design
*   **Expert 4 :** Se concentre sur la performance

**Résultat :** Vous obtenez une vision complète en combinant tous ces points de vue spécialisés.

#### 🎯 Pourquoi Plusieurs "Têtes" ?

Une seule tête d'attention ne peut capturer qu'un type de relation. Le Multi-Head Attention permet de capturer différents types de relations simultanément :

*   Relations syntaxiques (sujet-verbe)
*   Relations sémantiques (synonymes)
*   Relations de position (proche/loin)
*   Relations contextuelles (anaphore)

#### 👥 8 Têtes d'Attention Spécialisées

Phrase : "Le chat noir mange la souris grise"

Tête 1: Syntaxe

Se concentre sur sujet-verbe  
"chat" ↔ "mange"

Tête 2: Objets

Se concentre sur verbe-objet  
"mange" ↔ "souris"

Tête 3: Adjectifs

Se concentre sur nom-adjectif  
"chat" ↔ "noir"

Tête 4: Déterminants

Se concentre sur articles  
"Le" ↔ "chat"

Tête 5: Distance

Mots adjacents  
Relations de proximité

Tête 6: Sémantique

Concepts liés  
"chat" ↔ "souris" (prédateur-proie)

Tête 7: Position

Début/fin de phrase  
Structure globale

Tête 8: Contexte

Informations globales  
Thème général

**💡 Résultat :** Chaque tête capture un aspect différent, puis toutes les informations sont combinées pour une compréhension complète et nuancée.

**Formule Multi-Head Attention :**  
  
MultiHead(Q,K,V) = Concat(head₁, head₂, ..., head₈)WO  
  
où head₍ᵢ₎ = Attention(QW₍ᵢ₎Q, KW₍ᵢ₎K, VW₍ᵢ₎V)

### 🔧 Avantages du Multi-Head

#### 🎯 Spécialisation

Chaque tête peut se spécialiser dans un type de relation différent.

#### 🔄 Parallélisation

Toutes les têtes sont calculées en parallèle, pas de ralentissement.

#### 🧠 Richesse

Représentation plus riche et nuancée du contexte.

## 5\. 🪞 Self-Attention : La Révolution

#### 🔄 Self-Attention Expliquée

Dans la Self-Attention, chaque mot de la séquence porte attention à tous les mots de la même séquence, y compris lui-même. C'est comme si chaque mot "discutait" avec tous les autres pour enrichir sa propre compréhension.

🔍 Self-Attention en Action

Regardez comment "mange" enrichit sa représentation :

**"Le chat noir mange la souris grise"**

**🎯 "mange" demande :**

*   "Qui fait l'action ?" → **Attention forte sur "chat"**
*   "Quoi est mangé ?" → **Attention forte sur "souris"**
*   "Quelles propriétés ?" → **Attention moyenne sur "noir", "grise"**
*   "Contexte grammatical ?" → **Attention faible sur "le", "la"**

**📊 Résultat :** La représentation de "mange" est enrichie avec toutes ces informations contextuelles.

### 🚀 Pourquoi Self-Attention Révolutionne Tout

#### ✅ Connexions Directes

Chaque mot peut directement accéder à tout autre mot, quelle que soit la distance.

**Impact :** Dépendances à long terme parfaitement capturées.

#### ⚡ Parallélisation

Tous les calculs d'attention peuvent être faits simultanément.

**Impact :** Vitesse d'entraînement drastiquement améliorée.

#### 🎯 Flexibilité

Le modèle apprend automatiquement quelles connexions sont importantes.

**Impact :** Adaptation automatique à différents types de tâches.

[← Introduction](module6_introduction.md)

**Prêt pour l'architecture complète ?**  
Découvrez le Transformer au complet

[Architecture Transformer →](module6_transformer_architecture.md)

// Démonstration interactive d'attention const attentionPatterns = { '0': { weights: \[0.8, 0.1, 0.05, 0.02, 0.02, 0.01\], explanation: "Le déterminant 'Le' porte surtout attention à lui-même et un peu au nom qu'il détermine." }, '1': { weights: \[0.2, 0.4, 0.15, 0.2, 0.03, 0.02\], explanation: "Le nom 'chat' porte attention au déterminant, à son adjectif 'noir', et au verbe 'mange'." }, '2': { weights: \[0.05, 0.6, 0.3, 0.03, 0.01, 0.01\], explanation: "L'adjectif 'noir' porte principalement attention au nom qu'il qualifie : 'chat'." }, '3': { weights: \[0.02, 0.5, 0.05, 0.3, 0.08, 0.05\], explanation: "Le verbe 'mange' porte attention au sujet 'chat' et à l'objet 'souris'." }, '4': { weights: \[0.1, 0.02, 0.01, 0.05, 0.7, 0.12\], explanation: "Le déterminant 'la' porte surtout attention à lui-même et au nom qu'il détermine." }, '5': { weights: \[0.01, 0.02, 0.01, 0.3, 0.15, 0.51\], explanation: "Le nom 'souris' porte attention au verbe qui l'affecte et à son déterminant." } }; document.getElementById('attentionDemo').addEventListener('click', function(e) { if (e.target.classList.contains('word-token')) { // Reset all tokens document.querySelectorAll('.word-token').forEach(token => { token.classList.remove('active'); const existing = token.querySelector('.attention-weight'); if (existing) existing.remove(); }); // Activate clicked token e.target.classList.add('active'); // Get attention pattern const wordIndex = e.target.dataset.word; const pattern = attentionPatterns\[wordIndex\]; // Add attention weights document.querySelectorAll('.word-token').forEach((token, i) => { const weight = pattern.weights\[i\]; if (weight > 0.1) { const weightElement = document.createElement('div'); weightElement.className = 'attention-weight'; weightElement.textContent = weight.toFixed(1); token.appendChild(weightElement); } }); // Update explanation document.getElementById('attentionExplanation').textContent = pattern.explanation; } }); // Matrice d'attention interactive const matrixExplanations = { '0.1': "Attention faible - relation grammaticale basique", '0.2': "Attention faible-moyenne - lien contextuel", '0.3': "Attention moyenne - relation syntaxique", '0.5': "Attention forte - auto-attention (le mot se regarde lui-même)", '0.6': "Attention forte - relation grammaticale importante", '0.7': "Attention très forte - dépendance syntaxique directe" }; document.getElementById('attentionMatrix').addEventListener('click', function(e) { if (e.target.classList.contains('matrix-value')) { const score = e.target.dataset.score; const explanation = matrixExplanations\[score\] || "Score d'attention"; document.getElementById('matrixExplanation').innerHTML = \`<strong>Score ${score} :</strong> ${explanation}\`; } }); // Animation au scroll function animateOnScroll() { const elements = document.querySelectorAll('.content-section'); elements.forEach(element => { const elementTop = element.getBoundingClientRect().top; const elementVisible = 150; if (elementTop < window.innerHeight - elementVisible) { element.style.opacity = '1'; element.style.transform = 'translateY(0)'; } }); } window.addEventListener('scroll', animateOnScroll); document.addEventListener('DOMContentLoaded', animateOnScroll);
