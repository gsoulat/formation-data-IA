---
title: 'Module 1 : Tâches Principales du NLP'
description: 'Formation NLP - Module 1 : Tâches Principales du NLP'
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

[🏠 Introduction](module1_intro.md) → [🚧 Défis](module1_defis.md) → 🎯 Tâches Principales

# 🎯 Principales Tâches du NLP

Découvrez ce que les systèmes NLP savent faire concrètement

## 🧠 1. Tâches de Compréhension

Ces tâches consistent à analyser et comprendre du texte existant :

### 📂 Classification de Texte

Catégoriser un document selon des critères prédéfinis

**Exemple :**  
📧 Email : "Félicitations ! Vous avez gagné 1M€ !"  
➡️ **Catégorie :** SPAM

### 😊 Analyse de Sentiment

Détecter l'émotion ou l'opinion exprimée dans un texte

**Exemple :**  
💬 Avis : "Ce restaurant est fantastique !"  
➡️ **Sentiment :** POSITIF (95%)

### 🏷️ Reconnaissance d'Entités (NER)

Extraire et identifier des informations spécifiques

**Exemple :**  
📝 "Apple recrute à Paris en 2024"  
➡️ **Entités :** Apple (ORG), Paris (LOC), 2024 (DATE)

### ❓ Question-Réponse

Répondre automatiquement à des questions sur un texte

**Exemple :**  
📄 Contexte : "Einstein a développé la relativité en 1915"  
❓ Question : "Qui a créé la relativité ?"  
➡️ **Réponse :** Einstein

## ✨ 2. Tâches de Génération

Ces tâches créent du nouveau contenu textuel :

### 🌍 Traduction Automatique

Convertir un texte d'une langue vers une autre

**Exemple :**  
🇫🇷 "Bonjour le monde"  
➡️ 🇬🇧 "Hello world"

### 📄 Résumé Automatique

Condenser un long texte en gardant les informations clés

**Exemple :**  
📰 Article de 500 mots  
➡️ 📝 Résumé en 50 mots

### 🎨 Génération de Texte

Créer du contenu original à partir d'un début

**Exemple :**  
✏️ Début : "Il était une fois..."  
➡️ 📖 Histoire complète générée

### 💬 Dialogue/Chatbot

Converser naturellement avec les utilisateurs

**Exemple :**  
👤 "Quel temps fait-il ?"  
🤖 "Il fait beau aujourd'hui à Paris, 22°C avec du soleil !"

### 🧪 Démo Interactive : Testez les Tâches NLP

Expérimentez avec différentes tâches de traitement du langage :

😊 Sentiment 🏷️ Entités 🌍 Traduction ✨ Génération

#### Analyse de Sentiment

 Analyser

Entrez un texte pour analyser son sentiment...

#### Reconnaissance d'Entités

 Extraire

Entrez un texte pour extraire les entités...

#### Traduction FR → EN

 Traduire

Entrez un texte français à traduire...

#### Génération de Texte

 Générer

Entrez un début de phrase à compléter...

## 🏢 3. Applications Concrètes par Secteur

#### 💰 Secteur Financier

*   • Analyse de sentiment sur actualités financières
*   • Extraction d'infos des rapports annuels
*   • Détection de fraude dans communications
*   • Chatbots service client bancaire

#### 🛒 E-commerce

*   • Recommandations basées sur descriptions
*   • Analyse d'avis clients automatisée
*   • Recherche sémantique ("chaussures confortables")
*   • Génération de descriptions produits

#### 🏥 Santé

*   • Analyse de dossiers médicaux
*   • Extraction d'infos publications scientifiques
*   • Chatbots médicaux pour triage
*   • Traduction de documents médicaux

#### 📰 Médias

*   • Génération automatique d'articles sportifs
*   • Détection de fake news
*   • Résumé automatique d'événements
*   • Traduction en temps réel

## 📊 4. Tableau Récapitulatif

Catégorie

Tâche

Input

Output

Difficulté

🧠 Compréhension

Classification

Texte

Catégorie

⭐⭐

🧠 Compréhension

Sentiment

Texte

Émotion

⭐⭐

🧠 Compréhension

NER

Texte

Entités

⭐⭐⭐

✨ Génération

Traduction

Texte (langue A)

Texte (langue B)

⭐⭐⭐⭐

✨ Génération

Résumé

Texte long

Texte court

⭐⭐⭐⭐

✨ Génération

Dialogue

Question

Réponse

⭐⭐⭐⭐⭐

[⬅️ Retour Défis](module1_defis.md) [📈 Voir l'Évolution Historique](module1_evolution.md)

### 📈 Prochaine Étape

Maintenant que vous connaissez les principales tâches du NLP, découvrons comment cette technologie a évolué au fil du temps et quelles sont les innovations qui ont marqué son développement.

// Fonction pour changer d'onglet dans la démo function switchTab(tabName) { // Cacher tous les contenus const contents = document.querySelectorAll('.demo-content'); contents.forEach(content => { content.classList.remove('active'); }); // Désactiver tous les boutons const tabs = document.querySelectorAll('.demo-tab'); tabs.forEach(tab => { tab.classList.remove('active'); }); // Activer le contenu sélectionné document.getElementById(tabName).classList.add('active'); // Activer le bouton correspondant event.target.classList.add('active'); } // Fonction d'analyse de sentiment (démo simulée) function analyzeSentiment() { const input = document.getElementById('sentimentInput').value.trim(); const output = document.getElementById('sentimentOutput'); if (!input) { output.innerHTML = '<span style="color: #e74c3c;">⚠️ Veuillez entrer un texte à analyser</span>'; return; } // Simulation du traitement output.innerHTML = '<span class="processing">🔄 Analyse en cours...</span>'; setTimeout(() => { // Logique simplifiée de détection de sentiment const positiveWords = \['super', 'génial', 'fantastique', 'excellent', 'parfait', 'magnifique', 'merveilleux', 'passionnant', 'incroyable', 'formidable', 'bien', 'bon', 'beau', 'top'\]; const negativeWords = \['mauvais', 'nul', 'horrible', 'terrible', 'affreux', 'décevant', 'ennuyeux', 'pire', 'catastrophique', 'mal'\]; const lowerInput = input.toLowerCase(); let sentiment = 'NEUTRE'; let confidence = 60; let emoji = '😐'; const positiveCount = positiveWords.filter(word => lowerInput.includes(word)).length; const negativeCount = negativeWords.filter(word => lowerInput.includes(word)).length; if (positiveCount > negativeCount) { sentiment = 'POSITIF'; confidence = Math.min(90, 70 + positiveCount \* 10); emoji = '😊'; } else if (negativeCount > positiveCount) { sentiment = 'NÉGATIF'; confidence = Math.min(90, 70 + negativeCount \* 10); emoji = '😞'; } output.innerHTML = \` <strong>${emoji} Sentiment détecté :</strong> <span style="color: ${sentiment === 'POSITIF' ? '#27ae60' : sentiment === 'NÉGATIF' ? '#e74c3c' : '#f39c12'}">${sentiment}</span><br> <strong>Confiance :</strong> ${confidence}% \`; }, 1500); } // Fonction d'extraction d'entités (démo simulée) function extractEntities() { const input = document.getElementById('entitiesInput').value.trim(); const output = document.getElementById('entitiesOutput'); if (!input) { output.innerHTML = '<span style="color: #e74c3c;">⚠️ Veuillez entrer un texte pour extraire les entités</span>'; return; } output.innerHTML = '<span class="processing">🔄 Extraction en cours...</span>'; setTimeout(() => { // Règles simplifiées pour détecter des entités const entities = \[\]; // Noms de personnes (commencent par une majuscule, pas de mots-outils) const personPattern = /\\b\[A-Z\]\[a-z\]+(?:\\s+\[A-Z\]\[a-z\]+)?\\b/g; const persons = input.match(personPattern); if (persons) { persons.forEach(person => { if (!\['Le', 'La', 'Les', 'Un', 'Une', 'Des', 'Ce', 'Cette', 'Ces', 'Mon', 'Ma', 'Mes', 'Son', 'Sa', 'Ses'\].includes(person)) { entities.push(\`<span style="background: #ffebee; padding: 2px 5px; border-radius: 3px;">${person}</span> <small>(PERSONNE)</small>\`); } }); } // Organisations connues const organizations = \['Google', 'Apple', 'Microsoft', 'Amazon', 'Facebook', 'Netflix', 'Tesla', 'IBM', 'Oracle'\]; organizations.forEach(org => { if (input.includes(org)) { entities.push(\`<span style="background: #e3f2fd; padding: 2px 5px; border-radius: 3px;">${org}</span> <small>(ORGANISATION)</small>\`); } }); // Lieux const places = \['Paris', 'Londres', 'New York', 'Tokyo', 'Berlin', 'Madrid', 'Rome', 'Lyon', 'Marseille', 'France', 'Angleterre', 'Japon', 'Allemagne', 'Espagne', 'Italie'\]; places.forEach(place => { if (input.includes(place)) { entities.push(\`<span style="background: #e8f5e8; padding: 2px 5px; border-radius: 3px;">${place}</span> <small>(LIEU)</small>\`); } }); // Dates const datePattern = /\\b(janvier|février|mars|avril|mai|juin|juillet|août|septembre|octobre|novembre|décembre|\\d{4}|\\d{1,2}\\/\\d{1,2}\\/\\d{4})\\b/gi; const dates = input.match(datePattern); if (dates) { dates.forEach(date => { entities.push(\`<span style="background: #fff3e0; padding: 2px 5px; border-radius: 3px;">${date}</span> <small>(DATE)</small>\`); }); } if (entities.length === 0) { output.innerHTML = '🤔 Aucune entité détectée. Essayez avec des noms, des lieux ou des dates !'; } else { output.innerHTML = \`<strong>🏷️ Entités trouvées :</strong><br><br>${entities.join('<br>')}\`; } }, 1500); } // Fonction de traduction (démo simulée) function translateText() { const input = document.getElementById('translationInput').value.trim(); const output = document.getElementById('translationOutput'); if (!input) { output.innerHTML = '<span style="color: #e74c3c;">⚠️ Veuillez entrer un texte français à traduire</span>'; return; } output.innerHTML = '<span class="processing">🔄 Traduction en cours...</span>'; setTimeout(() => { // Dictionnaire de traductions simples const translations = { 'bonjour': 'hello', 'au revoir': 'goodbye', 'merci': 'thank you', 'comment allez-vous': 'how are you', 'comment ça va': 'how are you', 'bonne nuit': 'good night', 'bon matin': 'good morning', 'bon après-midi': 'good afternoon', 'je vous en prie': 'you\\'re welcome', 'excusez-moi': 'excuse me', 'pardon': 'sorry', 'oui': 'yes', 'non': 'no', 'peut-être': 'maybe', 'très bien': 'very good', 'intelligence artificielle': 'artificial intelligence', 'traitement du langage': 'language processing', 'ordinateur': 'computer', 'technologie': 'technology', 'apprentissage': 'learning' }; let translatedText = input.toLowerCase(); // Remplacer les expressions connues for (const \[french, english\] of Object.entries(translations)) { translatedText = translatedText.replace(new RegExp(french, 'gi'), english); } // Si aucune traduction trouvée, traduction générique if (translatedText === input.toLowerCase()) { translatedText = \`\[Traduction approximative\] ${input}\`; } output.innerHTML = \` <strong>🇫🇷 Français :</strong> ${input}<br> <strong>🇬🇧 Anglais :</strong> ${translatedText} \`; }, 1500); } // Fonction de génération de texte (démo simulée) function generateText() { const input = document.getElementById('generationInput').value.trim(); const output = document.getElementById('generationOutput'); if (!input) { output.innerHTML = '<span style="color: #e74c3c;">⚠️ Veuillez entrer un début de phrase</span>'; return; } output.innerHTML = '<span class="processing">🔄 Génération en cours...</span>'; setTimeout(() => { // Continuations prédéfinies selon le contexte const continuations = { 'intelligence artificielle': 'va transformer notre façon de travailler et d\\'interagir avec la technologie dans les prochaines décennies.', 'le futur': 'sera probablement façonné par les avancées technologiques et les défis environnementaux que nous devons relever ensemble.', 'il était une fois': 'dans un royaume lointain, une princesse qui possédait le don de comprendre le langage des animaux.', 'la technologie': 'évolue rapidement et continue de repousser les limites de ce que nous pensions possible.', 'les données': 'sont devenues l\\'or noir du 21ème siècle, alimentant l\\'innovation et la prise de décision.', 'machine learning': 'permet aux ordinateurs d\\'apprendre à partir de données sans être explicitement programmés pour chaque tâche.', 'chatbot': 'utilise des algorithmes sophistiqués pour comprendre les questions et fournir des réponses pertinentes.', 'demain': 'apportera son lot de surprises et d\\'opportunités pour ceux qui sauront s\\'adapter.' }; let generatedText = input; // Trouver une continuation appropriée for (const \[keyword, continuation\] of Object.entries(continuations)) { if (input.toLowerCase().includes(keyword)) { generatedText += ' ' + continuation; break; } } // Si aucune continuation spécifique, générer une continuation générique if (generatedText === input) { const genericContinuations = \[ 'ouvre de nouvelles perspectives fascinantes pour l\\'avenir.', 'représente un défi passionnant à relever.', 'mérite qu\\'on s\\'y intéresse de plus près.', 'pourrait bien révolutionner notre approche habituelle.', 'soulève des questions importantes qu\\'il faut considérer.' \]; const randomContinuation = genericContinuations\[Math.floor(Math.random() \* genericContinuations.length)\]; generatedText += ' ' + randomContinuation; } output.innerHTML = \` <strong>✨ Texte généré :</strong><br> "${generatedText}" \`; }, 2000); } // Permettre l'exécution avec la touche Entrée document.addEventListener('DOMContentLoaded', function() { const inputs = document.querySelectorAll('.demo-input'); inputs.forEach(input => { input.addEventListener('keypress', function(e) { if (e.key === 'Enter') { const tabId = this.closest('.demo-content').id; switch(tabId) { case 'sentiment': analyzeSentiment(); break; case 'entities': extractEntities(); break; case 'translation': translateText(); break; case 'generation': generateText(); break; } } }); }); });
