---
title: 'Module 5 - Leçon 1 : Introduction aux RNN'
description: 'Formation NLP - Module 5 - Leçon 1 : Introduction aux RNN'
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# 🧠 Leçon 1 : Introduction aux Réseaux de Neurones Récurrents (RNN)

Imaginez que vous lisez un livre. Pour comprendre chaque phrase, vous vous souvenez de ce qui s'est passé avant. C'est exactement ce que font les RNN : ils possèdent une **mémoire** qui leur permet de comprendre les séquences !

## 📚 Pourquoi avons-nous besoin des RNN ?

### Le problème des réseaux de neurones classiques

Les réseaux de neurones traditionnels (comme ceux que vous avez vus dans les modules précédents) traitent chaque entrée indépendamment. Ils n'ont aucune notion de ce qui s'est passé avant.

#### Exemple concret :

**Phrase 1 :** "Le chat est sur le..."

**Phrase 2 :** "J'ai oublié mes clés sur le..."

Un humain devine facilement : "tapis" pour la première, "bureau" pour la seconde. Mais un réseau classique ne peut pas utiliser le contexte précédent pour prédire !

![Architecture RNN enroulée](https://colah.github.io/posts/2015-08-Understanding-LSTMs/img/RNN-rolled.png)

Vue simplifiée d'un RNN - La boucle représente la connexion récurrente

## 🔄 Comment fonctionnent les RNN ?

### L'idée clé : La mémoire

Un RNN est comme un réseau de neurones avec une **mémoire à court terme**. À chaque étape, il :

*   🔸 Reçoit une nouvelle entrée (ex: un mot)
*   🔸 Combine cette entrée avec sa mémoire précédente
*   🔸 Produit une sortie
*   🔸 Met à jour sa mémoire pour l'étape suivante

![Architecture RNN déroulée](https://colah.github.io/posts/2015-08-Understanding-LSTMs/img/RNN-unrolled.png)

RNN "déroulé" dans le temps - Chaque étape utilise la mémoire de l'étape précédente

### Point clé à retenir

Un RNN est le **même réseau** utilisé plusieurs fois de suite. C'est comme si vous aviez un seul cerveau qui traite les mots un par un, en gardant en mémoire ce qu'il a vu avant.

## 🎯 Applications concrètes des RNN

Application

Description

Exemple concret

**Traduction automatique**

Traduire une phrase en gardant le contexte

"I love you" → "Je t'aime" (pas "J'aime tu")

**Analyse de sentiment**

Comprendre l'émotion d'un texte complet

"Le film était long mais finalement génial !" → Positif

**Génération de texte**

Écrire du texte cohérent mot par mot

Compléter "Il était une fois..." → "...un prince dans un château"

**Reconnaissance vocale**

Transcrire la parole en tenant compte du contexte

Distinguer "verre" de "vers" selon le contexte

## 💻 Architecture technique simplifiée

```
# Pseudo-code simplifié d'un RNN
pour chaque mot dans la phrase:
    état_caché = fonction(mot_actuel, état_caché_précédent)
    sortie = fonction(état_caché)
    
# état_caché = la "mémoire" du réseau
# Il contient les informations importantes des mots précédents
```

### Les composants essentiels

*   **Input (Entrée) :** Le mot actuel (souvent sous forme de vecteur)
*   **Hidden State (État caché) :** La mémoire du réseau
*   **Output (Sortie) :** La prédiction ou représentation actuelle
*   **Poids partagés :** Les mêmes paramètres sont utilisés à chaque étape

## ⚠️ Les limitations des RNN simples

### Le problème de la mémoire à court terme

Les RNN "vanilla" (basiques) ont tendance à oublier les informations anciennes. C'est comme essayer de se souvenir du début d'un livre en arrivant à la fin !

#### Exemple du problème :

**Phrase longue :** "Le chat *\[50 mots au milieu\]* était noir."

Un RNN simple pourrait oublier que nous parlons d'un chat !

![Problème du gradient qui disparaît](https://miro.medium.com/max/1400/1*AKpT7aXLCCNSB5nqTqFfmg.png)

Le problème du "vanishing gradient" - Les informations anciennes s'estompent

## 🚀 Vers des architectures plus avancées

### La solution : LSTM et GRU

Pour résoudre ces problèmes, des chercheurs ont inventé des architectures plus sophistiquées :

*   **LSTM (Long Short-Term Memory) :** Comme un RNN avec une mémoire à long terme
*   **GRU (Gated Recurrent Unit) :** Une version simplifiée mais efficace du LSTM

Nous les étudierons en détail dans la prochaine leçon !

#### 🎯 Quiz rapide - Testez votre compréhension

**Question 1 :** Quelle est la principale différence entre un réseau de neurones classique et un RNN ? Voir la réponse

Un RNN possède une **mémoire** qui lui permet de se souvenir des entrées précédentes, contrairement à un réseau classique qui traite chaque entrée indépendamment.

**Question 2 :** Pourquoi dit-on que les RNN partagent leurs poids ? Voir la réponse

Parce que c'est le **même réseau** (avec les mêmes paramètres) qui est utilisé à chaque étape temporelle. Il n'y a pas un réseau différent pour chaque mot !

## 📝 Résumé de la leçon

### Ce qu'il faut retenir :

*   ✅ Les RNN sont conçus pour traiter des **séquences** (texte, audio, etc.)
*   ✅ Ils possèdent une **mémoire** qui conserve les informations passées
*   ✅ Le même réseau est utilisé à chaque étape (poids partagés)
*   ✅ Ils sont parfaits pour les tâches nécessitant du contexte
*   ✅ Les RNN simples ont des limitations (mémoire courte)

[← Retour au Module 5](index.md) [Leçon 2 : LSTM →](module5_lesson2.md)
