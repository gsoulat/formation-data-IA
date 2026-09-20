---
title: 'Module 2 : Tokenisation'
description: 'Formation NLP - Module 2 : Tokenisation'
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

[📚 Module 2](index.md) → [🏠 Introduction](module2_intro.md) → [🧹 Nettoyage](module2_nettoyage.md) → ✂️ Tokenisation

# ✂️ Tokenisation

Découper intelligemment le texte en unités exploitables

1

2

3

4

5

## 🎯 Qu'est-ce que la Tokenisation ?

### 📋 Définition

**Tokenisation** = Découper un texte en **unités** plus petites appelées **tokens**

#### Exemple Simple :

**Texte :** "Bonjour, comment allez-vous ?"

**Tokens :** Bonjour , comment allez-vous ?

#### Exemple Complexe (Français) :

**Texte :** "J'adore les self-services, n'est-ce pas ?"

**Tokens :** J' adore les self-services , n' est \-ce pas ?

## 🔧 Les 4 Stratégies Principales

#### 📝 1. Tokenisation par Espaces

**Méthode :** `text.split()`

**Input :** "Bonjour comment allez-vous"  
**Output :** \["Bonjour", "comment", "allez-vous"\]

**✅ Avantages**

*   Très simple
*   Rapide
*   Intuitive

**❌ Inconvénients**

*   Garde la ponctuation
*   Ignore les contractions
*   Problème avec mots composés

#### 🔍 2. Tokenisation par Regex

**Méthode :** `re.findall(r'\w+', text)`

**Input :** "Bonjour, comment allez-vous ?"  
**Output :** \["Bonjour", "comment", "allez", "vous"\]

**✅ Avantages**

*   Flexible
*   Supprime ponctuation
*   Personnalisable

**❌ Inconvénients**

*   Casse les mots composés
*   Perd les contractions
*   Moins intuitif

#### 🐍 3. NLTK Word Tokenize

**Méthode :** `nltk.word_tokenize()`

**Input :** "J'adore les self-services."  
**Output :** \["J'", "adore", "les", "self-services", "."\]

**✅ Avantages**

*   Gère les contractions
*   Garde mots composés
*   Bien testé

**❌ Inconvénients**

*   Plus lent
*   Optimisé pour l'anglais
*   Dépendance externe

#### ⚡ 4. spaCy Tokenizer

**Méthode :** `spacy_nlp(text)`

**Input :** "N'est-ce pas formidable ?"  
**Output :** \["N'", "est", "-ce", "pas", "formidable", "?"\]

**✅ Avantages**

*   Très performant
*   Modèles spécialisés
*   Production-ready

**❌ Inconvénients**

*   Plus lourd
*   Courbe d'apprentissage
*   Modèles à télécharger

## 🇫🇷 Spécificités du Français

### 📚 Défis Particuliers du Français

Le français pose des défis uniques pour la tokenisation :

#### 1\. Contractions et Élisions

Forme Contractée

Forme Développée

Tokenisation Idéale

j'adore

je adore

\["j'", "adore"\] OU \["je", "adore"\]

n'est-ce pas

ne est-ce pas

\["n'", "est", "-ce", "pas"\]

qu'est-ce que

que est-ce que

\["qu'", "est", "-ce", "que"\]

c'est

ce est

\["c'", "est"\] OU \["ce", "est"\]

aujourd'hui

\-

\["aujourd'hui"\] (mot unique)

#### 2\. Mots Composés et Traits d'Union

**Exemples :**

• "self-service" → Garder ensemble ou séparer ?

• "c'est-à-dire" → 4 tokens distincts

• "merry-go-round" → Mot anglais composé

• "rendez-vous" → Souvent gardé ensemble

#### 3\. Accents et Caractères Spéciaux

**Défis :**

• Accents : "café" vs "cafe"

• Cédille : "français" vs "francais"

• Ligatures : "œuf" vs "oeuf"

• Majuscules accentuées : "ÉLÉPHANT" vs "ELEPHANT"

## 💻 Notebooks Jupyter Interactifs

#### 🔬 Comparaison des Méthodes de Tokenisation

📓 Notebook : **tokenisation\_comparaison.ipynb**

🔬 Notebook interactif pour comparer toutes les méthodes de tokenisation

[📓 Ouvrir le Notebook](notebook/tokenisation_comparaison.ipynb)

**🔧 Contenu du notebook :**  
• Implémentation des 4 méthodes principales  
• Tests sur textes français complexes  
• Benchmarks de performance  
• Visualisations comparatives

#### 🇫🇷 Tokeniseur Personnalisé pour le Français

📓 Notebook : **tokeniseur\_francais.ipynb**

[📓 Ouvrir le Notebook](notebook/tokeniseur_francais.ipynb)

**🎯 Ce notebook contient :**  
• Classe TokeniseurFrancais personnalisée  
• Gestion des contractions françaises  
• Traitement des mots composés  
• Exemples d'utilisation pratiques

#### ⚡ Optimisation et Performance

📓 Notebook : **tokenisation\_performance.ipynb**

[📓 Ouvrir le Notebook](notebook/tokenisation_performance.ipynb)

**🚀 Fonctionnalités avancées :**  
• Benchmarks de vitesse détaillés  
• Optimisation des algorithmes  
• Gestion de gros volumes de données  
• Recommandations par cas d'usage

## 🧪 Démo Interactive : Comparaison des Méthodes

### 🔬 Testez les Différentes Approches

Comparez les résultats des 4 méthodes de tokenisation :

J'adore les self-services, n'est-ce pas ? ⚔️ Comparer les Méthodes

Entrez du texte et cliquez sur "Comparer" pour voir les différences...

## 💡 Recommandations par Cas d'Usage

#### ⚡ Prototypage Rapide

**Recommandation :** `text.split()`

**Avantages :**

*   Très simple à implémenter
*   Pas de dépendances
*   Rapide pour tester des idées

#### 🎯 Projets de Production

**Recommandation :** spaCy

**Avantages :**

*   Performance optimisée
*   Modèles pré-entraînés
*   Support français excellent

#### 🔬 Recherche Académique

**Recommandation :** NLTK

**Avantages :**

*   Très flexible
*   Bien documenté
*   Communauté active

#### 🛠️ Besoins Spécifiques

**Recommandation :** Regex personnalisées

**Avantages :**

*   Contrôle total
*   Adaptable au domaine
*   Performance prévisible

[⬅️ Retour Nettoyage](module2_nettoyage.md) [⚙️ Techniques Avancées](module2_avance.md)

### ⚙️ Prochaine Étape

Excellent ! Vous maîtrisez maintenant la tokenisation. Passons aux techniques avancées : stopwords, lemmatisation et stemming !

[Découvrir les Techniques Avancées 🚀](module2_avance.md)

// Gestion des onglets function showTab(tabId) { // Cacher tous les contenus const contents = document.querySelectorAll('.tab-content'); contents.forEach(content => content.classList.remove('active')); // Désactiver tous les onglets const tabs = document.querySelectorAll('.tab'); tabs.forEach(tab => tab.classList.remove('active')); // Activer l'onglet et contenu sélectionnés document.getElementById(tabId).classList.add('active'); event.target.classList.add('active'); } // Démonstration comparative de tokenisation function compareTokenization() { const input = document.getElementById('tokenInput').value.trim(); const resultDiv = document.getElementById('tokenResults'); if (!input) { resultDiv.textContent = 'Veuillez entrer du texte à tokeniser'; return; } // Méthode 1: Split par espaces const method1 = input.split(/\\s+/); // Méthode 2: Regex simple const method2 = input.match(/\\w+/g) || \[\]; // Méthode 3: Simulation NLTK (gestion contractions) let method3 = input; // Simulation de la gestion des contractions method3 = method3.replace(/n'(\\w)/g, "n' $1"); method3 = method3.replace(/j'(\\w)/g, "j' $1"); method3 = method3.replace(/c'(\\w)/g, "c' $1"); method3 = method3.replace(/qu'(\\w)/g, "qu' $1"); const nltkTokens = method3.split(/\\s+/).filter(t => t.trim().length > 0); // Méthode 4: Simulation spaCy (plus sophistiquée) let method4 = input; method4 = method4.replace(/(\[.!?\])/g, ' $1'); method4 = method4.replace(/(\[,;:\])/g, ' $1'); method4 = method4.replace(/-/g, ' - '); method4 = method4.replace(/'/g, "' "); const spacyTokens = method4.split(/\\s+/).filter(t => t.trim().length > 0); resultDiv.innerHTML = \` <strong>🔬 Comparaison des méthodes de tokenisation :</strong> 📝 <strong>Texte original :</strong> "${input}" 📊 <strong>Résultats :</strong> 1️⃣ <strong>Split simple (${method1.length} tokens) :</strong> \[${method1.map(t => \`"${t}"\`).join(', ')}\] 2️⃣ <strong>Regex \\\\w+ (${method2.length} tokens) :</strong> \[${method2.map(t => \`"${t}"\`).join(', ')}\] 3️⃣ <strong>Style NLTK (${nltkTokens.length} tokens) :</strong> \[${nltkTokens.map(t => \`"${t}"\`).join(', ')}\] 4️⃣ <strong>Style spaCy (${spacyTokens.length} tokens) :</strong> \[${spacyTokens.map(t => \`"${t}"\`).join(', ')}\] 💡 <strong>Observations :</strong> • Split simple : ${method1.some(t => t.includes(',') || t.includes('.')) ? 'Garde la ponctuation attachée' : 'Sépare bien les mots'} • Regex : ${method2.length < method1.length ? 'Supprime la ponctuation' : 'Préserve les mots'} • NLTK : ${nltkTokens.some(t => t.includes("'")) ? 'Gère bien les contractions françaises' : 'Tokenisation standard'} • spaCy : ${spacyTokens.length > method1.length ? 'Sépare finement (ponctuation isolée)' : 'Tokenisation conservative'} 🎯 <strong>Recommandation pour ce texte :</strong> ${getBestMethod(input, method1, method2, nltkTokens, spacyTokens)} \`; } function getBestMethod(input, method1, method2, nltk, spacy) { if (input.includes("'") && (input.includes("n'") || input.includes("j'"))) { return "spaCy ou NLTK pour gérer les contractions françaises"; } else if (input.includes(",") || input.includes(".")) { return "spaCy pour séparer proprement la ponctuation"; } else { return "Split simple suffit pour ce cas basique"; } } // Exemples automatiques au clic document.addEventListener('DOMContentLoaded', function() { const examples = \[ "J'adore les self-services, n'est-ce pas ?", "C'est vraiment génial ! Qu'est-ce que tu en penses ?", "Rendez-vous à 14h30 pour discuter du e-commerce.", "L'anti-inflammatoire coûte vingt-trois euros.", "Marie-Claire habite à Saint-Étienne depuis l'année dernière." \]; const input = document.getElementById('tokenInput'); if (input) { input.addEventListener('click', function() { if (!this.value) { const randomExample = examples\[Math.floor(Math.random() \* examples.length)\]; this.value = randomExample; } }); } });
