---
title: 'Module 2 : Nettoyage et Normalisation'
description: 'Formation NLP - Module 2 : Nettoyage et Normalisation'
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

[🏠 Introduction](module2_intro.md) → 🧹 Nettoyage et Normalisation

# 🧹 Nettoyage et Normalisation

Maîtriser les techniques fondamentales de préparation du texte

1

2

3

4

5

## 🎯 Les 5 Techniques Essentielles

#### 🔤 1. Gestion de la Casse

**Objectif :** Unifier "SUPER", "Super", "super" → "super"

**Avant :**  
"GÉNIAL !", "Génial", "génial"  
→ 3 mots différents

**Après :**  
"génial", "génial", "génial"  
→ 1 seul mot

#### 📝 2. Suppression Ponctuation

**Objectif :** Retirer "!", "?", "..." qui n'apportent pas de sens

**Avant :**  
"Bonjour!!!", "Bonjour.", "Bonjour"  
→ 3 mots différents

**Après :**  
"bonjour", "bonjour", "bonjour"  
→ 1 seul mot

#### 🌐 3. Suppression URLs/Emails

**Objectif :** Éliminer le bruit qui pollue l'analyse

**Avant :**  
"Super article https://bit.ly/xyz"  
→ pollution par l'URL

**Après :**  
"super article"  
→ focus sur le contenu

#### 😊 4. Gestion des Emojis

**Objectif :** Traiter les emojis selon le contexte

**Avant :**  
"Super ! 😍😍😍"  
→ emojis parasites

**Après :**  
"super" OU "super positif"  
→ selon la stratégie

#### 🔧 5. Normalisation Espaces

**Objectif :** Uniformiser les espaces multiples

**Avant :**  
"Bonjour comment allez-vous"  
→ espaces irréguliers

**Après :**  
"bonjour comment allez-vous"  
→ espaces normalisés

#### 🔡 6. Normalisation Accents

**Objectif :** Gérer les variantes avec/sans accents

**Avant :**  
"été", "ete", "été"  
→ variantes accents

**Après :**  
"ete", "ete", "ete"  
→ forme normalisée

## 💻 Notebooks Jupyter Interactifs

#### 🔧 Nettoyage Basique avec Python Standard

📓 Notebook : **nettoyage\_basique.ipynb**

📝 Notebook interactif avec exemples pratiques et explications détaillées

[📓 Ouvrir le Notebook](notebook/nettoyage_basique.ipynb)

**🎯 Contenu du notebook :**  
• Techniques de base avec Python standard  
• Exemples interactifs étape par étape  
• Exercices pratiques avec solutions  
• Tests sur vos propres données

#### ⚙️ Nettoyage Avancé avec Gestion des Accents

📓 Notebook : **nettoyage\_avance.ipynb**

[📓 Ouvrir le Notebook](notebook/nettoyage_avance.ipynb)

**🎯 Ce notebook contient :**  
• Classe NettoyeurFrancais personnalisée  
• Gestion des accents et caractères spéciaux  
• Options configurables pour emojis  
• Comparaisons et analyses de performance

#### 🧪 Pipeline de Nettoyage Personnalisable

📓 Notebook : **pipeline\_nettoyage.ipynb**

[📓 Ouvrir le Notebook](notebook/pipeline_nettoyage.ipynb)

**🚀 Fonctionnalités avancées :**  
• Pipeline modulaire et configurable  
• Traitement par batch de plusieurs textes  
• Métriques de qualité du nettoyage  
• Visualisations et analyses comparatives

## 🧪 Démo Interactive : Nettoyeur Multi-Options

### 🔬 Testez Différentes Stratégies de Nettoyage

🧹 Basique ⚙️ Avancé 🎯 Personnalisé

#### Nettoyage Basique

🧹 Nettoyer

Le résultat apparaîtra ici...

#### Nettoyage Avancé avec Options

 Garder les accents français  
 Supprimer emojis  Convertir emojis en mots  Garder emojis

⚙️ Nettoyer Avancé

Le résultat apparaîtra ici...

#### Pipeline Personnalisé

 Minuscules  Supprimer ponctuation  Supprimer URLs  Supprimer mentions (@)  Supprimer hashtags (#)  Normaliser espaces

🎯 Nettoyer Personnalisé

Le résultat apparaîtra ici...

## ⚠️ Pièges et Bonnes Pratiques

#### 🚨 Attention aux Pièges Courants

*   **Ordre des opérations :** Toujours nettoyer AVANT de tokeniser
*   **Sur-nettoyage :** Ne pas supprimer trop d'informations utiles
*   **Contexte :** Un emoji peut être informatif pour l'analyse de sentiment
*   **Langue :** Les règles changent selon la langue (français vs anglais)
*   **Domaine :** Traiter différemment tweets vs articles académiques

#### ✅ Bonnes Pratiques

*   **Testez sur des échantillons :** Vérifiez que le nettoyage garde le sens
*   **Documentez vos choix :** Pourquoi garder/supprimer tel élément ?
*   **Gardez l'original :** Toujours conserver une copie du texte brut
*   **Adaptez au contexte :** Pas de solution universelle
*   **Mesurez l'impact :** Évaluez l'effet sur les performances finales

[⬅️ Retour Introduction](module2_intro.md) [✂️ Tokenisation](module2_tokenisation.md)

### ✂️ Prochaine Étape

Maintenant que votre texte est propre, apprenons à le découper intelligemment en tokens (mots) !

[Maîtriser la Tokenisation 🔍](module2_tokenisation.md)

function switchTab(tabName) { // Masquer tous les contenus const contents = document.querySelectorAll('.demo-content'); contents.forEach(content => content.classList.remove('active')); // Désactiver tous les onglets const tabs = document.querySelectorAll('.demo-tab'); tabs.forEach(tab => tab.classList.remove('active')); // Activer l'onglet et le contenu sélectionnés document.getElementById(tabName).classList.add('active'); event.target.classList.add('active'); } function nettoyageBasique() { const texte = document.getElementById('texteBasique').value.trim(); if (!texte) { document.getElementById('resultatBasique').textContent = 'Veuillez entrer du texte à nettoyer'; return; } let resultat = texte; let etapes = \[\]; // Étape 1: Minuscules resultat = resultat.toLowerCase(); etapes.push(\`1. Minuscules: "${resultat}"\`); // Étape 2: URLs resultat = resultat.replace(/https?:\\/\\/\[^\\s\]+/g, '\[URL\]'); etapes.push(\`2. Sans URLs: "${resultat}"\`); // Étape 3: Mentions resultat = resultat.replace(/@\\w+/g, '\[MENTION\]'); etapes.push(\`3. Sans mentions: "${resultat}"\`); // Étape 4: Hashtags resultat = resultat.replace(/#\\w+/g, '\[HASHTAG\]'); etapes.push(\`4. Sans hashtags: "${resultat}"\`); // Étape 5: Ponctuation resultat = resultat.replace(/\[^\\w\\s\]/g, ' '); etapes.push(\`5. Sans ponctuation: "${resultat}"\`); // Étape 6: Espaces resultat = resultat.replace(/\\s+/g, ' ').trim(); etapes.push(\`6. Espaces normalisés: "${resultat}"\`); document.getElementById('resultatBasique').textContent = etapes.join('\\n') + \`\\n\\nRésultat final: "${resultat}"\`; } function nettoyageAvance() { const texte = document.getElementById('texteAvance').value.trim(); if (!texte) { document.getElementById('resultatAvance').textContent = 'Veuillez entrer du texte à nettoyer'; return; } let resultat = texte; const garderAccents = document.getElementById('garderAccents').checked; const traitementEmojis = document.querySelector('input\[name="emojis"\]:checked').value; // Gestion des accents if (!garderAccents) { resultat = resultat.normalize('NFD').replace(/\[\\u0300-\\u036f\]/g, ''); } // Minuscules resultat = resultat.toLowerCase(); // Gestion des emojis if (traitementEmojis === 'convertir') { const emojiDict = { '😍': ' très positif ', '😊': ' positif ', '🙂': ' positif ', '😞': ' négatif ', '😡': ' très négatif ', '❤️': ' amour ', '👍': ' bien ', '👎': ' mal ', '☕': ' café ', '🍕': ' pizza ' }; for (const \[emoji, remplacement\] of Object.entries(emojiDict)) { resultat = resultat.replace(new RegExp(emoji, 'g'), remplacement); } } else if (traitementEmojis === 'supprimer') { resultat = resultat.replace(/\[\\u{1F600}-\\u{1F64F}\]|\[\\u{1F300}-\\u{1F5FF}\]|\[\\u{1F680}-\\u{1F6FF}\]|\[\\u{1F1E0}-\\u{1F1FF}\]|\[\\u{2600}-\\u{26FF}\]|\[\\u{2700}-\\u{27BF}\]/gu, ''); } // Suppression des éléments web resultat = resultat.replace(/https?:\\/\\/\[^\\s\]+/g, ' '); resultat = resultat.replace(/www\\.\[^\\s\]+/g, ' '); resultat = resultat.replace(/\\S+@\\S+/g, ' '); resultat = resultat.replace(/@\\w+/g, ' '); resultat = resultat.replace(/#\\w+/g, ' '); resultat = resultat.replace(/rt\\s+/g, ' '); // Suppression caractères spéciaux resultat = resultat.replace(/\[^\\w\\sàâäéèêëïîôöùûüÿç\]/g, ' '); // Normalisation espaces resultat = resultat.replace(/\\s+/g, ' ').trim(); document.getElementById('resultatAvance').innerHTML = \` <strong>Configuration:</strong> • Accents: ${garderAccents ? 'Gardés' : 'Supprimés'} • Emojis: ${traitementEmojis} <strong>Résultat:</strong> "${resultat}" <strong>Statistiques:</strong> • Longueur originale: ${texte.length} caractères • Longueur finale: ${resultat.length} caractères • Réduction: ${Math.round((1 - resultat.length / texte.length) \* 100)}% \`; } function nettoyagePersonnalise() { const texte = document.getElementById('textePersonnalise').value.trim(); if (!texte) { document.getElementById('resultatPersonnalise').textContent = 'Veuillez entrer du texte à nettoyer'; return; } let resultat = texte; let etapes = \[\`Original: "${texte}"\`\]; // Options sélectionnées const opts = { minuscules: document.getElementById('opt1').checked, ponctuation: document.getElementById('opt2').checked, urls: document.getElementById('opt3').checked, mentions: document.getElementById('opt4').checked, hashtags: document.getElementById('opt5').checked, espaces: document.getElementById('opt6').checked }; // Application conditionnelle des transformations if (opts.minuscules) { resultat = resultat.toLowerCase(); etapes.push(\`Minuscules: "${resultat}"\`); } if (opts.urls) { resultat = resultat.replace(/https?:\\/\\/\[^\\s\]+/g, '\[URL\]'); etapes.push(\`Sans URLs: "${resultat}"\`); } if (opts.mentions) { resultat = resultat.replace(/@\\w+/g, '\[MENTION\]'); etapes.push(\`Sans mentions: "${resultat}"\`); } if (opts.hashtags) { resultat = resultat.replace(/#\\w+/g, '\[HASHTAG\]'); etapes.push(\`Sans hashtags: "${resultat}"\`); } if (opts.ponctuation) { resultat = resultat.replace(/\[^\\w\\s\]/g, ' '); etapes.push(\`Sans ponctuation: "${resultat}"\`); } if (opts.espaces) { resultat = resultat.replace(/\\s+/g, ' ').trim(); etapes.push(\`Espaces normalisés: "${resultat}"\`); } document.getElementById('resultatPersonnalise').textContent = etapes.join('\\n\\n'); } // Exemples automatiques au clic document.addEventListener('DOMContentLoaded', function() { const examples = { 'texteBasique': "RT @user: SUPER article!!! https://bit.ly/xyz #génial 😍", 'texteAvance': "J'adore ce café ☕😍 contact@cafe.fr #délicieux", 'textePersonnalise': "Salut!!! Comment ça va??? J'espère que tout va BIEN 🙂 @marie #bonnejournée" }; Object.entries(examples).forEach((\[id, example\]) => { const element = document.getElementById(id); if (element) { element.addEventListener('click', function() { if (!this.value) { this.value = example; } }); } }); });
