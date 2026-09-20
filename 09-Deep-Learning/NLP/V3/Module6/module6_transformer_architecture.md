---
title: Module 6 - Architecture Transformer
description: Formation NLP - Module 6 - Architecture Transformer
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# 🏗️ Architecture Transformer

Comprendre la structure révolutionnaire qui a transformé l'IA

### 🗺️ Navigation Module 6

Explorez les Transformers étape par étape

[🏠 Index Module 6](index.md) [👁️ Mécanismes d'Attention](module6_attention_mechanisms.md)

🏗️ Architecture (Actuel)

[🚀 Implémentation →](module6_implementation.md)

## 🏗️ Vue d'Ensemble de l'Architecture

🔍 Vue d'ensemble 🔄 Encodeur 📤 Décodeur 🎯 Architecture Complète

### 🎯 Structure Générale du Transformer

**Architecture Encoder-Decoder**

📥 Input

"Bonjour le monde"

Tokenisation + Embeddings

→

🔄 Encodeur

6 couches

Self-Attention + FFN

→

📤 Décodeur

6 couches

Masked Attention + Cross-Attention

→

📋 Output

"Hello world"

Probabilités des mots

**🔑 Innovations Clés :**  
• Parallélisation complète : Plus de traitement séquentiel  
• Self-Attention : Chaque mot "regarde" tous les autres  
• Multi-Head Attention : Plusieurs types d'attention en parallèle  
• Positional Encoding : Encodage de la position sans récurrence  
• Residual Connections : Évite la disparition du gradient

### 🔄 Bloc Encodeur Détaillé

#### Structure d'un Bloc Encodeur

**1\. Multi-Head Self-Attention**  
Chaque mot calcule son attention avec tous les autres mots

Input → Q, K, V → Attention(Q,K,V) → Concat → Linear

+

**2\. Add & Norm**  
Connexion résiduelle + normalisation de couche

LayerNorm(x + SelfAttention(x))

↓

**3\. Feed Forward Network**  
Réseau de neurones position-wise

Linear → ReLU → Linear (avec dimensions d\_model → d\_ff → d\_model)

+

**4\. Add & Norm**  
Deuxième connexion résiduelle + normalisation

LayerNorm(x + FFN(x))

**Formules Mathématiques :**

Attention(Q,K,V) = softmax(QK^T/√d\_k)V

MultiHead(Q,K,V) = Concat(head₁,...,head\_h)W^O

FFN(x) = max(0, xW₁ + b₁)W₂ + b₂

LayerNorm(x) = γ((x-μ)/σ) + β

### 📤 Bloc Décodeur Détaillé

#### Structure d'un Bloc Décodeur

**1\. Masked Multi-Head Self-Attention**  
Attention uniquement sur les positions précédentes (prévention du futur)

Mask pour éviter de voir les mots suivants

**2\. Add & Norm**  
Première connexion résiduelle

**3\. Cross-Attention (Encoder-Decoder)**  
Q vient du décodeur, K et V viennent de l'encodeur

Permet au décodeur de "regarder" l'entrée originale

**4\. Add & Norm**  
Deuxième connexion résiduelle

**5\. Feed Forward Network**  
Identique à l'encodeur

**6\. Add & Norm**  
Troisième connexion résiduelle

**🔍 Différences Clés Encodeur vs Décodeur :**  
• Masked Attention : Le décodeur ne peut pas voir le futur  
• Cross-Attention : Connexion avec l'output de l'encodeur  
• Génération Autoregressif : Production mot par mot  
• 3 couches d'attention : Masked Self + Cross + FFN

### 🎯 Architecture Complète

#### Transformer Complet : Traduction "Hello" → "Bonjour"

##### 🔄 ENCODEUR

**Input Embeddings**  
"Hello" → \[0.1, 0.8, 0.3, ...\]

**\+ Positional Encoding**  
Position 0: \[0.0, 1.0, 0.0, ...\]

**6 × Encoder Layers**  
Self-Attention + FFN

**Output Representations**  
Contexte enrichi de "Hello"

→

##### 📤 DÉCODEUR

**Output Embeddings**  
"" → génération progressive

**\+ Positional Encoding**  
Position de génération

**6 × Decoder Layers**  
Masked Attention + Cross-Attention + FFN

**Linear + Softmax**  
Probabilités : "Bonjour" (0.95)

#### 🎯 Flux Complet de Traduction

**1\. Tokenisation**  
"Hello" → \[101, 7592, 102\]

**2\. Embeddings**  
Tokens → Vecteurs denses

**3\. Encodage**  
Compréhension contextuelle

**4\. Décodage**  
Génération mot par mot

**5\. Output**  
"Bonjour" !

## ⚖️ Transformer vs RNN/LSTM

🔄 RNN/LSTM

**Traitement :** Séquentiel  
**Parallélisation :** ❌ Impossible  
**Mémoire :** Limitée (~1000 mots)  
**Vitesse :** Lente  
**Dépendances :** Difficiles long terme  
**Complexité :** O(n) en temps

🤖 Transformer

**Traitement :** Parallèle  
**Parallélisation :** ✅ Complète  
**Mémoire :** Illimitée théoriquement  
**Vitesse :** Très rapide  
**Dépendances :** Globales directes  
**Complexité :** O(1) en temps (parallèle)

📊 Performance

**BLEU Score Traduction :**  
• RNN/LSTM: ~28  
• Transformer: ~41  
  
**Vitesse d'entraînement :**  
• RNN: 1x (baseline)  
• Transformer: 10-100x

**🚀 Pourquoi les Transformers dominent :**  
• Parallélisation : Utilisation optimale des GPU modernes  
• Attention globale : Chaque mot peut "voir" tous les autres directement  
• Pas de goulot d'étranglement : Plus de limite par la mémoire séquentielle  
• Scalabilité : Performance améliore avec plus de données et de calcul  
• Transfert learning : Pré-entraînement efficace sur de vastes corpus

## 🔧 Détails Techniques Avancés

### 📐 Dimensions et Hyperparamètres

**Configuration Standard (Transformer Base) :**  
  

**Modèle :**  
• d\_model = 512 (dimension des embeddings)  
• d\_ff = 2048 (dimension FFN)  
• h = 8 (nombre de têtes d'attention)

**Architecture :**  
• N = 6 (couches encoder/decoder)  
• d\_k = d\_v = 64 (dimension par tête)  
• Dropout = 0.1

**Training :**  
• Paramètres totaux: ~65M  
• Adam optimizer  
• Warmup + decay learning rate

### 🧮 Complexité Computationnelle

**Self-Attention**  

Complexité: O(n² × d)  
Mémoire: O(n²)  
Parallélisation: O(1)

n = longueur séquence, d = dimension

**RNN**  

Complexité: O(n × d²)  
Mémoire: O(n × d)  
Parallélisation: O(n)

Séquentiel par nature

**⚠️ Trade-offs :**  
• Séquences courtes : Transformer plus efficace  
• Séquences très longues : Attention quadratique peut être limitante  
• Solutions : Sparse Attention, Linear Attention, Longformer  
• GPU vs CPU : Transformers excellent sur GPU, RNN acceptable sur CPU

## ➡️ Prochaine Étape

Vous comprenez maintenant l'architecture révolutionnaire des Transformers ! Passons à l'implémentation pratique.

**🎯 Ce que vous maîtrisez :**  
• Architecture Encoder-Decoder : Structure globale  
• Self-Attention : Mécanisme central  
• Multi-Head Attention : Parallélisation des perspectives  
• Avantages vs RNN : Parallélisation et performance

### 🚀 Continuez l'Exploration

Implémentez votre propre Transformer et découvrez ses applications

[🚀 Implémentation & Applications →](module6_implementation.md) [🤖 Module 7: BERT & GPT](../Module7/index.md)

// Animation de la barre de progression window.addEventListener('load', function() { setTimeout(() => { document.getElementById('progressBar').style.width = '75%'; }, 1000); }); // Gestion des onglets function showTab(tabName) { // Cacher tous les contenus d'onglets const contents = document.querySelectorAll('.tab-content'); contents.forEach(content => content.classList.remove('active')); // Désactiver tous les onglets const tabs = document.querySelectorAll('.tab'); tabs.forEach(tab => tab.classList.remove('active')); // Activer l'onglet et le contenu sélectionnés document.getElementById(tabName).classList.add('active'); event.target.classList.add('active'); } // Highlight des blocs transformer function highlightBlock(block, type) { // Reset all blocks document.querySelectorAll('.transformer-block').forEach(b => { b.style.transform = 'scale(1)'; b.style.boxShadow = ''; }); // Highlight clicked block block.style.transform = 'scale(1.1)'; block.style.boxShadow = '0 12px 30px rgba(255, 107, 107, 0.6)'; // Reset after 2 seconds setTimeout(() => { block.style.transform = 'scale(1)'; block.style.boxShadow = ''; }, 2000); }
