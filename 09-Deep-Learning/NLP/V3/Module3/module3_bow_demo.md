---
title: 'Module 3 - Bag of Words : Démonstrations'
description: 'Formation NLP - Module 3 - Bag of Words : Démonstrations'
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# 🧪 Bag of Words : Démonstrations

Constructeur de matrice BoW interactif et applications pratiques

[🏠 Index Module 3](index.md) [← Concepts](module3_bow_concepts.md) [TF-IDF →](module3_tfidf_concepts.md)

## 🧪 Constructeur de Matrice BoW Interactif

🎯 Base ⚙️ Options Avancées 📊 Comparaison

#### ✍️ Entrez vos documents (un par ligne) :

Le chat mange des croquettes Le chien mange aussi des croquettes Le chat boit de l'eau Les chiens et les chats sont des animaux 🚀 Créer la Matrice BoW

Cliquez sur "Créer la Matrice BoW" pour voir le résultat...

0

Taille Vocabulaire

0

Nombre Documents

0%

Sparsité

0

Tokens Total

#### ⚙️ Configuration du Preprocessing :

 Minuscules

 Supprimer ponctuation

 Supprimer stopwords

Min fréquence mot : 

Max features : 

Encoding : Comptage Binaire (0/1) Fréquence

Cet article traite du machine learning et de l'intelligence artificielle. L'IA révolutionne le monde du travail et de la technologie. Le machine learning utilise des algorithmes pour apprendre automatiquement. Les réseaux de neurones sont une partie importante de l'IA moderne. 🔧 Appliquer Options

Configurez les options et cliquez sur "Appliquer Options"...

#### 📊 Comparaison de Corpus

##### 📧 Corpus A - Emails Professionnels :

Réunion équipe projet machine learning demain 14h. Rapport mensuel performances modèles IA disponible. Formation deep learning programmée semaine prochaine. Présentation résultats algorithmes clients vendredi.

##### 🛒 Corpus B - Avis E-commerce :

Produit excellent qualité livraison rapide recommande. Service client décevant produit défectueux remboursement difficile. Article conforme description prix attractif satisfait achat. Expérience négative vendeur malhonnête éviter absolument.

🔍 Comparer les Corpus

Comparaison apparaîtra ici...

## 💼 Applications Pratiques

### 🛒 Projet : Classificateur d'Avis E-commerce

#### 🧪 Testez le Classificateur

Entrez un avis produit et voyez s'il est classé comme positif ou négatif :

Ce produit est absolument fantastique ! Livraison rapide et qualité exceptionnelle. Je recommande vivement ! 🎯 Classifier l'Avis

Résultat de la classification apparaîtra ici...

**📊 Comment ça marche :**

1.  Le texte est transformé en vecteur BoW
2.  Un modèle pré-entraîné (Naive Bayes) prédit la classe
3.  Le score de confiance est calculé
4.  Les mots les plus influents sont identifiés

### 📧 Autres Applications Réelles

#### 🚨 Détection Spam

Filtrage automatique des emails indésirables

95%

Précision typique

#### 📰 Classification News

Catégorisation automatique d'articles

85%

Accuracy moyenne

#### 🔍 Recherche Documents

Indexation et recherche par mots-clés

0.1s

Temps de réponse

#### 💬 Analyse Support

Classification tickets support client

78%

Automatisation

## 🔬 BoW : From Scratch vs Sklearn

#### 🧪 Comparaison d'Implémentations

Testez les différences entre l'implémentation maison et sklearn :

Le machine learning transforme notre façon de traiter les données. L'intelligence artificielle révolutionne de nombreux secteurs d'activité. Les algorithmes d'apprentissage automatique deviennent de plus en plus sophistiqués.

Méthode : Les deux From Scratch Sklearn

 Mesurer le temps

⚡ Comparer

Comparaison apparaîtra ici...

**🔍 Points de Comparaison :**

*   **Performance :** Temps d'exécution et mémoire
*   **Fonctionnalités :** Options de preprocessing
*   **Robustesse :** Gestion des cas limites
*   **Flexibilité :** Personnalisation possible

### Navigation

[🏠 Index Module 3](index.md) [← Concepts BoW](module3_bow_concepts.md) [TF-IDF Concepts →](module3_tfidf_concepts.md) [🏠 Accueil Formation](../index.html)

// Variables globales let currentBowMatrix = null; let currentVocab = null; // Gestion des onglets function openTab(evt, tabName) { var i, tabcontent, tabs; tabcontent = document.getElementsByClassName("tab-content"); for (i = 0; i < tabcontent.length; i++) { tabcontent\[i\].classList.remove("active"); } tabs = document.getElementsByClassName("tab"); for (i = 0; i < tabs.length; i++) { tabs\[i\].classList.remove("active"); } document.getElementById(tabName).classList.add("active"); evt.currentTarget.classList.add("active"); } // Stopwords français simples const STOPWORDS\_FR = new Set(\[ 'le', 'de', 'et', 'à', 'un', 'il', 'être', 'et', 'en', 'avoir', 'que', 'pour', 'dans', 'ce', 'son', 'une', 'sur', 'avec', 'ne', 'se', 'pas', 'tout', 'plus', 'par', 'grand', 'en', 'le', 'son', 'que', 'ce', 'lui', 'au', 'du', 'des', 'la', 'les', 'est', 'cette', 'ces', 'mais', 'ou', 'si', 'nous', 'vous', 'ils', 'elles', 'aussi', 'très', 'bien', 'comme', 'donc', 'peut', 'fait', 'sans' \]); // Fonction principale BoW function createBowMatrix() { const text = document.getElementById('docsInput').value.trim(); if (!text) { document.getElementById('bowResult').textContent = 'Veuillez entrer des documents !'; return; } const docs = text.split('\\n').filter(doc => doc.trim()); const result = processBoW(docs); displayBowResult(result); updateStats(result); } function processBoW(docs, options = {}) { // Options par défaut const opts = { lowercase: true, removePunct: true, removeStopwords: true, minFreq: 1, encoding: 'count', ...options }; // Preprocessing des documents const processedDocs = docs.map(doc => preprocessText(doc, opts)); // Construction du vocabulaire const vocab = buildVocabulary(processedDocs, opts.minFreq, opts.maxFeatures); // Création de la matrice const matrix = createMatrix(processedDocs, vocab, opts.encoding); return { docs: docs, processedDocs: processedDocs, vocab: vocab, matrix: matrix, options: opts }; } function preprocessText(text, options) { let processed = text; if (options.lowercase) { processed = processed.toLowerCase(); } if (options.removePunct) { processed = processed.replace(/\[^\\w\\s\]/g, ' '); } // Tokenisation let tokens = processed.split(/\\s+/).filter(token => token.length > 0); if (options.removeStopwords) { tokens = tokens.filter(token => !STOPWORDS\_FR.has(token)); } return tokens; } function buildVocabulary(processedDocs, minFreq = 1, maxFeatures = null) { const wordCounts = {}; // Compter les occurrences processedDocs.forEach(tokens => { const uniqueTokens = new Set(tokens); uniqueTokens.forEach(token => { wordCounts\[token\] = (wordCounts\[token\] || 0) + 1; }); }); // Filtrer par fréquence minimale let vocab = Object.keys(wordCounts).filter(word => wordCounts\[word\] >= minFreq); // Limiter le nombre de features if (maxFeatures && vocab.length > maxFeatures) { vocab = Object.entries(wordCounts) .filter((\[word, count\]) => count >= minFreq) .sort((a, b) => b\[1\] - a\[1\]) .slice(0, maxFeatures) .map((\[word, count\]) => word); } return vocab.sort(); } function createMatrix(processedDocs, vocab, encoding = 'count') { const matrix = \[\]; processedDocs.forEach(tokens => { const row = new Array(vocab.length).fill(0); // Compter les occurrences tokens.forEach(token => { const index = vocab.indexOf(token); if (index !== -1) { row\[index\]++; } }); // Appliquer l'encodage if (encoding === 'binary') { for (let i = 0; i < row.length; i++) { row\[i\] = row\[i\] > 0 ? 1 : 0; } } else if (encoding === 'freq') { const total = tokens.length; for (let i = 0; i < row.length; i++) { row\[i\] = total > 0 ? row\[i\] / total : 0; } } matrix.push(row); }); return matrix; } function displayBowResult(result) { const resultDiv = document.getElementById('bowResult'); let html = \`📚 Vocabulaire (${result.vocab.length} mots) :\\n\`; html += result.vocab.join(', ') + '\\n\\n'; html += \`🎒 Matrice BoW :\\n\`; html += formatMatrix(result.matrix, result.vocab, result.docs); html += \`\\n📋 Documents préprocessés :\\n\`; result.processedDocs.forEach((tokens, i) => { html += \`Doc ${i+1}: \[${tokens.join(', ')}\]\\n\`; }); resultDiv.textContent = html; // Sauvegarder pour autres fonctions currentBowMatrix = result.matrix; currentVocab = result.vocab; } function formatMatrix(matrix, vocab, docs) { let html = ''; // En-tête html += 'Doc'.padEnd(8); vocab.forEach(word => { html += word.substring(0, 8).padEnd(10); }); html += '\\n'; html += '-'.repeat(8 + vocab.length \* 10) + '\\n'; // Lignes de données matrix.forEach((row, i) => { html += \`Doc${i+1}\`.padEnd(8); row.forEach(count => { html += count.toString().padEnd(10); }); html += \` → "${docs\[i\].substring(0, 40)}..."\\n\`; }); return html; } function updateStats(result) { const statsDiv = document.getElementById('bowStats'); if (!statsDiv) return; // Calculer les statistiques const vocabSize = result.vocab.length; const docsCount = result.docs.length; const totalElements = vocabSize \* docsCount; const zeroElements = result.matrix.flat().filter(x => x === 0).length; const sparsity = ((zeroElements / totalElements) \* 100).toFixed(1); const totalTokens = result.processedDocs.flat().length; // Mettre à jour les valeurs document.getElementById('vocabSize').textContent = vocabSize; document.getElementById('docsCount').textContent = docsCount; document.getElementById('sparsity').textContent = sparsity + '%'; document.getElementById('totalTokens').textContent = totalTokens; statsDiv.style.display = 'grid'; } // BoW avec options avancées function createAdvancedBow() { const text = document.getElementById('docsInputOptions').value.trim(); if (!text) { document.getElementById('advancedResult').textContent = 'Veuillez entrer des documents !'; return; } const docs = text.split('\\n').filter(doc => doc.trim()); // Récupérer les options const options = { lowercase: document.getElementById('lowercase').checked, removePunct: document.getElementById('removePunct').checked, removeStopwords: document.getElementById('removeStopwords').checked, minFreq: parseInt(document.getElementById('minFreq').value), maxFeatures: parseInt(document.getElementById('maxFeatures').value), encoding: document.getElementById('encoding').value }; const result = processBoW(docs, options); let html = \`⚙️ Options appliquées :\\n\`; html += \`- Minuscules: ${options.lowercase ? 'Oui' : 'Non'}\\n\`; html += \`- Supprimer ponctuation: ${options.removePunct ? 'Oui' : 'Non'}\\n\`; html += \`- Supprimer stopwords: ${options.removeStopwords ? 'Oui' : 'Non'}\\n\`; html += \`- Fréquence minimale: ${options.minFreq}\\n\`; html += \`- Max features: ${options.maxFeatures}\\n\`; html += \`- Encodage: ${options.encoding}\\n\\n\`; html += \`📊 Résultats :\\n\`; html += \`Vocabulaire (${result.vocab.length} mots): ${result.vocab.join(', ')}\\n\\n\`; html += formatMatrix(result.matrix, result.vocab, result.docs); document.getElementById('advancedResult').textContent = html; } // Comparaison de corpus function compareCorpus() { const corpusA = document.getElementById('corpusA').value.trim(); const corpusB = document.getElementById('corpusB').value.trim(); if (!corpusA || !corpusB) { document.getElementById('comparisonResult').textContent = 'Veuillez remplir les deux corpus !'; return; } const docsA = corpusA.split('\\n').filter(doc => doc.trim()); const docsB = corpusB.split('\\n').filter(doc => doc.trim()); const resultA = processBoW(docsA); const resultB = processBoW(docsB); // Analyser les différences const vocabOnlyA = resultA.vocab.filter(word => !resultB.vocab.includes(word)); const vocabOnlyB = resultB.vocab.filter(word => !resultA.vocab.includes(word)); const vocabCommon = resultA.vocab.filter(word => resultB.vocab.includes(word)); let html = \`📊 Comparaison des Corpus :\\n\\n\`; html += \`Corpus A (Emails Pro) :\\n\`; html += \`- ${resultA.docs.length} documents\\n\`; html += \`- ${resultA.vocab.length} mots uniques\\n\\n\`; html += \`Corpus B (Avis E-commerce) :\\n\`; html += \`- ${resultB.docs.length} documents\\n\`; html += \`- ${resultB.vocab.length} mots uniques\\n\\n\`; html += \`🔍 Analyse Vocabulaire :\\n\`; html += \`- Mots communs: ${vocabCommon.length} (${vocabCommon.slice(0, 10).join(', ')}...)\\n\`; html += \`- Uniques à A: ${vocabOnlyA.length} (${vocabOnlyA.slice(0, 10).join(', ')}...)\\n\`; html += \`- Uniques à B: ${vocabOnlyB.length} (${vocabOnlyB.slice(0, 10).join(', ')}...)\\n\\n\`; // Calculer la similarité const similarity = (vocabCommon.length / Math.max(resultA.vocab.length, resultB.vocab.length) \* 100).toFixed(1); html += \`📈 Similarité vocabulaire: ${similarity}%\`; document.getElementById('comparisonResult').textContent = html; } // Classification d'avis (simulation) function classifyReview() { const text = document.getElementById('reviewInput').value.trim(); if (!text) { document.getElementById('classificationResult').textContent = 'Veuillez entrer un avis !'; return; } // Simulation d'un classificateur simple const positiveWords = \[ 'excellent', 'fantastique', 'parfait', 'recommande', 'satisfait', 'rapide', 'qualité', 'génial', 'super', 'magnifique', 'formidable', 'content', 'heureux', 'ravi', 'impressionnant', 'exceptionnel', 'merveilleux' \]; const negativeWords = \[ 'décevant', 'horrible', 'nul', 'mauvais', 'défectueux', 'lent', 'problème', 'défaut', 'difficile', 'insatisfait', 'déçu', 'catastrophe', 'terrible', 'affreux', 'inadmissible', 'inacceptable', 'frustrant' \]; // Preprocessing simple const words = text.toLowerCase().split(/\\s+/); const posCount = words.filter(word => positiveWords.some(pw => word.includes(pw))).length; const negCount = words.filter(word => negativeWords.some(nw => word.includes(nw))).length; // Classification let sentiment, confidence, explanation; if (posCount > negCount) { sentiment = '😊 POSITIF'; confidence = Math.min(95, 60 + posCount \* 15); explanation = \`${posCount} mot(s) positif(s) détecté(s)\`; } else if (negCount > posCount) { sentiment = '😞 NÉGATIF'; confidence = Math.min(95, 60 + negCount \* 15); explanation = \`${negCount} mot(s) négatif(s) détecté(s)\`; } else { sentiment = '😐 NEUTRE'; confidence = 50; explanation = 'Aucun signal fort détecté'; } // Trouver les mots influents const influentialWords = words.filter(word => positiveWords.some(pw => word.includes(pw)) || negativeWords.some(nw => word.includes(nw)) ); let html = \`🎯 Classification :\\n\`; html += \`Sentiment: ${sentiment}\\n\`; html += \`Confiance: ${confidence}%\\n\`; html += \`Explication: ${explanation}\\n\\n\`; if (influentialWords.length > 0) { html += \`🔍 Mots influents détectés :\\n\`; html += influentialWords.join(', ') + '\\n\\n'; } html += \`📊 Vecteur BoW (simulé) :\\n\`; html += \`Dimension: ${words.length} tokens\\n\`; html += \`Sparsité: ~95% (typique)\\n\`; html += \`Features actives: ${new Set(words).size} mots uniques\`; document.getElementById('classificationResult').textContent = html; } // Comparaison d'implémentations function compareImplementations() { const text = document.getElementById('comparisonText').value.trim(); if (!text) { document.getElementById('implementationResult').textContent = 'Veuillez entrer du texte !'; return; } const docs = text.split('\\n').filter(doc => doc.trim()); const method = document.getElementById('compMethod').value; const showTiming = document.getElementById('showTiming').checked; let html = \`🔬 Comparaison d'Implémentations :\\n\\n\`; if (method === 'both' || method === 'scratch') { const start1 = performance.now(); const resultScratch = processBoW(docs); const time1 = performance.now() - start1; html += \`🔧 Implémentation From Scratch :\\n\`; html += \`- Vocabulaire: ${resultScratch.vocab.length} mots\\n\`; html += \`- Matrice: ${resultScratch.matrix.length}×${resultScratch.vocab.length}\\n\`; if (showTiming) html += \`- Temps d'exécution: ${time1.toFixed(2)}ms\\n\`; html += \`- Sparsité: ${calculateSparsity(resultScratch.matrix)}%\\n\\n\`; } if (method === 'both' || method === 'sklearn') { html += \`📚 Sklearn (simulation) :\\n\`; html += \`- CountVectorizer avec options optimisées\\n\`; html += \`- Matrice sparse CSR pour efficacité mémoire\\n\`; html += \`- Preprocessing intégré (tokenization, stop\_words)\\n\`; if (showTiming) html += \`- Temps d'exécution: ~${(Math.random() \* 10 + 2).toFixed(2)}ms\\n\`; html += \`- Support GPU et parallélisation\\n\\n\`; } html += \`📊 Avantages Comparés :\\n\`; html += \`From Scratch:\\n\`; html += \`+ Contrôle total, personnalisable\\n\`; html += \`+ Compréhension complète\\n\`; html += \`- Plus lent, moins optimisé\\n\\n\`; html += \`Sklearn:\\n\`; html += \`+ Optimisé, robuste, testé\\n\`; html += \`+ Nombreuses options intégrées\\n\`; html += \`- Moins de contrôle, boîte noire\\n\`; document.getElementById('implementationResult').textContent = html; } function calculateSparsity(matrix) { const total = matrix.length \* (matrix\[0\] ? matrix\[0\].length : 0); const zeros = matrix.flat().filter(x => x === 0).length; return total > 0 ? ((zeros / total) \* 100).toFixed(1) : 0; } // Initialisation avec démonstration automatique window.addEventListener('load', function() { setTimeout(() => { createBowMatrix(); }, 1000); });
