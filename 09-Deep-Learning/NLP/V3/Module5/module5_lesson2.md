---
title: 'Module 5 - Leçon 2 : Architecture LSTM'
description: 'Formation NLP - Module 5 - Leçon 2 : Architecture LSTM'
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# 🚀 Leçon 2 : LSTM - Long Short-Term Memory

Si les RNN sont comme une personne avec une mémoire à court terme, les LSTM sont comme une personne avec un **carnet de notes** ! Ils peuvent décider quoi écrire, quoi effacer et quoi lire.

## 🤔 Pourquoi les LSTM ?

### Le problème des RNN classiques

Rappelez-vous : les RNN simples ont du mal à se souvenir d'informations sur de longues séquences. C'est le problème du gradient qui disparaît.

#### Exemple du problème :

**Texte :** "Alice, qui habite à Paris et travaille comme médecin depuis 10 ans, *\[30 mots...\]* a décidé de déménager."

Un RNN simple pourrait oublier qu'on parle d'Alice et de Paris !

**RNN classique :** Comme essayer de retenir un numéro de téléphone en faisant autre chose - vous l'oubliez rapidement !

**LSTM :** Comme écrire le numéro sur un papier - vous pouvez le consulter quand vous en avez besoin !

## 🏗️ L'architecture LSTM expliquée simplement

### L'idée géniale des LSTM

Les LSTM utilisent un système de **portes** (gates) qui contrôlent le flux d'information. Imaginez un château avec plusieurs portes : certaines laissent entrer des informations, d'autres les laissent sortir, et d'autres décident ce qu'on garde en mémoire.

![Architecture complète LSTM](https://colah.github.io/posts/2015-08-Understanding-LSTMs/img/LSTM3-chain.png)

Architecture complète d'un LSTM - Regardons chaque élément en détail !

## 🔍 Décryptage complet du diagramme LSTM

### 🗺️ Guide de lecture du schéma

Le diagramme peut sembler complexe, mais chaque symbole a une signification précise :

**🟡 Couches neuronales**  
Les rectangles jaunes = opérations mathématiques (sigmoid, tanh)

**🔴 Opérations pointwise**  
Les cercles roses = multiplication ou addition élément par élément

**➡️ Flux de vecteurs**  
Les flèches = transfert d'information entre composants

**📋 Concaténation**  
Les jonctions = fusion de plusieurs vecteurs en un seul

### 🎯 Les deux "autoroutes" de l'information

**🛣️ Cell State (C\_t) - L'autoroute principale :**

Cette ligne horizontale en haut traverse tout le LSTM. C'est la mémoire à long terme. L'information peut circuler facilement avec très peu de modifications.

**🚗 Hidden State (h\_t) - La route locale :**

Cette ligne en bas contient l'information immédiatement utile. C'est ce qui est "sorti" à chaque étape.

![LSTM Forget Gate détaillé](https://colah.github.io/posts/2015-08-Understanding-LSTMs/img/LSTM3-focus-f.png)

Zoom sur la porte d'oubli - Elle regarde h\_{t-1} et x\_t pour décider quoi oublier

## 🔍 Analyse étape par étape du fonctionnement

1️⃣

### Étape 1 : Porte d'oubli (Forget Gate)

f\_t = σ(W\_f · \[h\_{t-1}, x\_t\] + b\_f)

**Ce qui se passe :**

*   📥 **Entrées :** État précédent h\_{t-1} + nouvelle entrée x\_t
*   🔄 **Processus :** Concaténation → Multiplication par poids W\_f → Fonction sigmoid
*   📤 **Sortie :** Valeurs entre 0 et 1 (0 = oublier complètement, 1 = garder complètement)
*   🎯 **Résultat :** Ces valeurs sont multipliées avec l'ancien Cell State

#### Exemple concret :

**Texte :** "Le chat était noir. Le chien..."

→ Quand on arrive à "chien", la porte d'oubli pourrait décider d'oublier partiellement les infos sur le chat (couleur, etc.)

![LSTM Input Gate détaillé](https://colah.github.io/posts/2015-08-Understanding-LSTMs/img/LSTM3-focus-i.png)

Porte d'entrée - Elle crée de nouvelles informations candidates et décide lesquelles ajouter

2️⃣

### Étape 2 : Porte d'entrée + Candidats (Input Gate)

**Décision d'ajout :**  
i\_t = σ(W\_i · \[h\_{t-1}, x\_t\] + b\_i)

**Nouvelles infos :**  
C̃\_t = tanh(W\_C · \[h\_{t-1}, x\_t\] + b\_C)

**Double processus :**

1.  **🚪 Input Gate (i\_t) :** Utilise sigmoid → décide *quelles* parties mettre à jour
2.  **📝 Candidats (C̃\_t) :** Utilise tanh → crée *les nouvelles valeurs* possibles
3.  **🤝 Combinaison :** i\_t × C̃\_t = les nouvelles infos qui seront vraiment ajoutées

#### Pourquoi deux fonctions ?

**Sigmoid (0 à 1) :** "À quel point cette info est-elle importante ?"

**Tanh (-1 à 1) :** "Quelle est la valeur de cette nouvelle information ?"

→ Séparation entre *l'importance* et *la valeur* !

![LSTM Cell State Update](https://colah.github.io/posts/2015-08-Understanding-LSTMs/img/LSTM3-focus-C.png)

Mise à jour du Cell State - L'ancien state est filtré puis enrichi de nouvelles informations

3️⃣

### Étape 3 : Mise à jour du Cell State

C\_t = f\_t × C\_{t-1} + i\_t × C̃\_t

**La formule magique :**

🧮 **Partie 1 :** f\_t × C\_{t-1} = "Ancien Cell State filtré par la porte d'oubli"

➕ **Plus :**

🧮 **Partie 2 :** i\_t × C̃\_t = "Nouvelles informations filtrées par la porte d'entrée"

\= Nouveau Cell State qui combine ancien (filtré) + nouveau (sélectionné)

**Analogie :** Imaginez votre bureau :

*   📄 f\_t × C\_{t-1} = Garder certains vieux documents (les importants)
*   📄 i\_t × C̃\_t = Ajouter de nouveaux documents (les pertinents)
*   🗂️ C\_t = Votre bureau mis à jour avec l'essentiel de l'ancien + le pertinent du nouveau

![LSTM Output Gate détaillé](https://colah.github.io/posts/2015-08-Understanding-LSTMs/img/LSTM3-focus-o.png)

Porte de sortie - Elle filtre le Cell State pour ne donner que l'information pertinente maintenant

4️⃣

### Étape 4 : Porte de sortie (Output Gate)

**Décision de sortie :**  
o\_t = σ(W\_o · \[h\_{t-1}, x\_t\] + b\_o)

**Hidden State :**  
h\_t = o\_t × tanh(C\_t)

**Processus final :**

1.  **🚪 Output Gate (o\_t) :** Regarde le contexte actuel, décide quoi montrer
2.  **🎭 tanh(C\_t) :** "Normalise" le Cell State entre -1 et 1
3.  **🎯 h\_t :** Le résultat final = Cell State filtré et adapté au contexte

#### Pourquoi tanh(C\_t) ?

Le Cell State peut contenir des valeurs très grandes ou très petites. tanh() les "normalise" pour que le résultat soit utilisable par les couches suivantes.

**Analogie :** C'est comme ajuster le volume de votre musique selon le contexte (bureau vs fête) !

## 🚪 Les 3 portes magiques du LSTM

🗑️

### Porte d'oubli (Forget Gate)

Décide quelles informations oublier

Cette porte regarde l'état précédent et l'entrée actuelle, puis décide quelles informations ne sont plus utiles.

#### Exemple :

**Texte :** "Le chat était sur le tapis. Le chien..."

→ On peut "oublier" certaines infos sur le chat car on parle maintenant du chien.

➕

### Porte d'entrée (Input Gate)

Décide quelles nouvelles informations stocker

Cette porte détermine quelles nouvelles informations sont importantes et doivent être ajoutées à la mémoire.

#### Exemple :

**Texte :** "Marie est **médecin**."

→ L'information "médecin" est importante et sera stockée pour comprendre la suite.

📤

### Porte de sortie (Output Gate)

Décide quelles informations utiliser maintenant

Cette porte filtre la mémoire pour ne donner que les informations pertinentes pour la tâche actuelle.

#### Exemple :

**Contexte mémorisé :** "Marie, médecin, Paris, 35 ans"

**Phrase actuelle :** "Elle soigne..."

→ La porte de sortie active l'info "médecin" car c'est pertinent ici.

## 🔄 Le flux d'information dans un LSTM

1

**État précédent**  
\+ Nouvelle entrée

→

2

**Forget Gate**  
Oublier l'inutile

→

3

**Input Gate**  
Ajouter le nouveau

→

4

**Output Gate**  
Filtrer la sortie

![LSTM Forget Gate](https://colah.github.io/posts/2015-08-Understanding-LSTMs/img/LSTM3-focus-f.png)

Zoom sur la porte d'oubli - Elle utilise une fonction sigmoïde (0 = tout oublier, 1 = tout garder)

## 💡 Comprendre avec une analogie complète

### L'LSTM comme un étudiant qui prend des notes

Imaginez un étudiant en cours :

*   **🗑️ Forget Gate :** Il efface les infos du tableau précédent qui ne sont plus utiles
*   **➕ Input Gate :** Il décide quelles nouvelles informations noter dans son cahier
*   **📤 Output Gate :** Il choisit quelles notes consulter pour répondre à une question
*   **📝 Cell State (État de cellule) :** Son cahier de notes complet
*   **👁️ Hidden State (État caché) :** Ce qu'il a actuellement en tête

## ⚖️ Avantages et inconvénients des LSTM

Avantages ✅

Inconvénients ❌

Excellente mémoire à long terme

Plus complexe et lent à entraîner

Résout le problème du gradient qui disparaît

Nécessite plus de mémoire (RAM)

Très efficace pour les longues séquences

Plus de paramètres à optimiser

Flexible et adaptatif

Peut être "overkill" pour des tâches simples

## 💻 Implémentation simplifiée

```
# Pseudo-code conceptuel d'un LSTM
class LSTM:
    def process_sequence(self, sequence):
        cell_state = 0  # Mémoire à long terme
        hidden_state = 0  # Mémoire à court terme
        
        for word in sequence:
            # 1. Forget Gate : décider quoi oublier
            forget = sigmoid(word + hidden_state)
            cell_state = cell_state * forget
            
            # 2. Input Gate : décider quoi ajouter
            input_gate = sigmoid(word + hidden_state)
            new_info = tanh(word + hidden_state)
            cell_state = cell_state + (input_gate * new_info)
            
            # 3. Output Gate : décider quoi sortir
            output_gate = sigmoid(word + hidden_state)
            hidden_state = output_gate * tanh(cell_state)
            
        return hidden_state
```

## 🎯 Applications pratiques des LSTM

### Où les LSTM excellent particulièrement

*   **🈂️ Traduction automatique :** Garder le contexte de phrases longues
*   **🎵 Génération de musique :** Se souvenir des motifs musicaux
*   **💬 Chatbots :** Maintenir le contexte d'une conversation
*   **📝 Résumé de texte :** Identifier les informations importantes sur de longs documents
*   **🗣️ Reconnaissance vocale :** Comprendre des phrases complètes

### Conseil pratique

Utilisez les LSTM quand :

*   ✓ Vos séquences sont longues (> 100 éléments)
*   ✓ Les dépendances à long terme sont importantes
*   ✓ La performance prime sur la vitesse

Préférez des architectures plus simples (RNN vanilla ou GRU) pour des tâches plus basiques.

## 📝 Résumé de la leçon

### Points clés à retenir :

*   ✅ Les LSTM résolvent le problème de mémoire à court terme des RNN
*   ✅ Ils utilisent 3 portes : Forget, Input et Output
*   ✅ Le Cell State agit comme une "autoroute" pour l'information
*   ✅ Parfaits pour les tâches nécessitant une mémoire à long terme
*   ✅ Plus complexes mais plus puissants que les RNN simples

[← Leçon 1 : Introduction RNN](module5_lesson1.md) [Leçon 3 : GRU →](module5_lesson3.md)
