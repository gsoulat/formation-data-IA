---
title: Module 8 - Optimisation des Modèles
description: Formation NLP - Module 8 - Optimisation des Modèles
tags:
  - NLP
  - 09-Deep-Learning
category: 09-Deep-Learning
---

# ⚡ Optimisation des Modèles

Réduire la latence et l'empreinte mémoire pour la production

## 🎯 Défis de Performance en Production

### ⚡ Problématiques de Latence

Les modèles Transformer comme BERT et GPT, bien que très performants, posent des défis majeurs en production :

BERT-Base Original

340M

Paramètres

1.3GB RAM

Latence Inférence

200ms

Par prédiction

Trop lent

Coût GPU

$500

Par mois

Instance V100

Objectif Production

<50ms

P95 Latence

🎯 Cible

**💡 Objectifs d'Optimisation :**  
• Latence : <50ms P95 pour classification  
• Mémoire : <500MB par instance  
• Throughput : >1000 req/sec par GPU  
• Qualité : Maintenir >95% des performances originales

#### 🧪 Comparateur d'Optimisations

BERT Original DistilBERT Quantization Combiné

Sélectionnez une technique pour voir l'impact...

## 🎓 Distillation de Modèles

### 👨‍🏫 Principe Teacher-Student

La distillation crée un modèle "étudiant" plus petit qui imite un modèle "professeur" plus large.

🧠

DistilBERT

Version distillée de BERT avec 6 couches au lieu de 12. Conserve 97% des performances.

66M

paramètres

2x

plus rapide

60%

moins de RAM

97%

performance

📱

TinyBERT

Encore plus compact avec distillation en deux phases : pré-entraînement + task-specific.

14M

paramètres

9x

plus rapide

85%

moins de RAM

96%

performance

🔄

Distillation Custom

Distiller votre modèle fine-tuné pour conserver les spécialisations métier.

Variable

taille

3-5x

plus rapide

Optimisé

pour votre tâche

98%

performance métier

\# Implémentation de distillation avec TensorFlow import tensorflow as tf from transformers import TFBertModel, TFDistilBertModel class DistillationTrainer: def \_\_init\_\_(self, teacher\_model, student\_model, temperature=3.0, alpha=0.7): self.teacher = teacher\_model self.student = student\_model self.temperature = temperature self.alpha = alpha # Balance entre loss distillation et task loss def distillation\_loss(self, y\_true, y\_pred\_student, y\_pred\_teacher): """Combine task loss et knowledge distillation loss""" # Task loss (classification standard) task\_loss = tf.keras.losses.sparse\_categorical\_crossentropy( y\_true, y\_pred\_student, from\_logits=True ) # Knowledge distillation loss (soft targets) teacher\_probs = tf.nn.softmax(y\_pred\_teacher / self.temperature) student\_log\_probs = tf.nn.log\_softmax(y\_pred\_student / self.temperature) kd\_loss = tf.keras.losses.KLDivergence()( teacher\_probs, student\_log\_probs ) # Loss combinée total\_loss = (self.alpha \* kd\_loss \* self.temperature \*\* 2 + (1 - self.alpha) \* task\_loss) return total\_loss def train\_step(self, batch\_data): """Step d'entraînement avec distillation""" inputs, labels = batch\_data with tf.GradientTape() as tape: # Prédictions teacher (frozen) teacher\_logits = self.teacher(inputs, training=False) # Prédictions student student\_logits = self.student(inputs, training=True) # Loss de distillation loss = self.distillation\_loss(labels, student\_logits, teacher\_logits) # Mise à jour uniquement du student gradients = tape.gradient(loss, self.student.trainable\_variables) self.optimizer.apply\_gradients(zip(gradients, self.student.trainable\_variables)) return loss

**⚠️ Considérations pour la Distillation :**  
• Données d'entraînement : Besoin du même dataset que le teacher  
• Temps de calcul : Teacher doit faire l'inférence pendant l'entraînement  
• Task-specific : Redistiller après fine-tuning pour maintenir performance  
• Hyperparamètres : Température et alpha critiques pour réussir

## 🗜️ Quantization et Compression

### 📊 Réduction de Précision

La quantization réduit la précision des poids de FP32 vers FP16 ou INT8, diminuant drastiquement la taille et accélérant l'inférence.

Technique Précision Taille Modèle Speedup Perte Qualité Hardware **FP32 Original** 32-bit float 1.3GB 1x 0% CPU/GPU **FP16 Half-Precision** 16-bit float 650MB 1.5-2x <1% GPU moderne **INT8 Dynamic** 8-bit integer 325MB 2-4x 1-3% CPU optimisé **INT8 Static** 8-bit integer 325MB 3-5x 2-5% CPU/Edge

💨

Post-Training Quantization

Quantization après entraînement sans données supplémentaires. Rapide mais moins précis.

🎯

Quantization-Aware Training

Entraînement avec simulation de quantization. Plus long mais meilleure qualité.

🔧

Dynamic Quantization

Quantization à la volée des activations. Bon compromis performance/simplicité.

\# Quantization avec TensorFlow Lite import tensorflow as tf def quantize\_model(saved\_model\_path, calibration\_dataset=None): """ Quantize un modèle BERT avec TensorFlow Lite """ # Converter setup converter = tf.lite.TFLiteConverter.from\_saved\_model(saved\_model\_path) # Configuration de base converter.optimizations = \[tf.lite.Optimize.DEFAULT\] if calibration\_dataset: # INT8 Quantization avec dataset de calibration converter.target\_spec.supported\_ops = \[tf.lite.OpsSet.TFLITE\_BUILTINS\_INT8\] converter.target\_spec.supported\_types = \[tf.int8\] def representative\_dataset(): for batch in calibration\_dataset.take(100): # Prendre seulement les input\_ids pour calibration yield \[batch\['input\_ids'\].numpy().astype(np.float32)\] converter.representative\_dataset = representative\_dataset converter.inference\_input\_type = tf.int8 converter.inference\_output\_type = tf.int8 else: # FP16 Quantization (plus simple) converter.target\_spec.supported\_types = \[tf.float16\] # Conversion quantized\_model = converter.convert() return quantized\_model def benchmark\_quantized\_model(original\_model, quantized\_model\_path, test\_data): """ Compare les performances original vs quantized """ import time # Load quantized model interpreter = tf.lite.Interpreter(model\_path=quantized\_model\_path) interpreter.allocate\_tensors() input\_details = interpreter.get\_input\_details() output\_details = interpreter.get\_output\_details() # Benchmark original start\_time = time.time() original\_predictions = original\_model.predict(test\_data) original\_time = time.time() - start\_time # Benchmark quantized start\_time = time.time() quantized\_predictions = \[\] for sample in test\_data: interpreter.set\_tensor(input\_details\[0\]\['index'\], sample) interpreter.invoke() output = interpreter.get\_tensor(output\_details\[0\]\['index'\]) quantized\_predictions.append(output) quantized\_time = time.time() - start\_time # Calcul métriques speedup = original\_time / quantized\_time accuracy\_loss = calculate\_accuracy\_difference(original\_predictions, quantized\_predictions) return { 'speedup': speedup, 'accuracy\_loss': accuracy\_loss, 'original\_time': original\_time, 'quantized\_time': quantized\_time }

## 🚀 ONNX Runtime et Optimisations Hardware

### ⚡ Optimisations au niveau du Graph

ONNX Runtime applique des optimisations automatiques au niveau du graphe computationnel pour maximiser les performances.

🔗

Graph Optimization

Fusion d'opérations, élimination de nœuds inutiles, réorganisation pour optimiser le cache.

15-30%

speedup CPU

Auto

optimisation

🎮

TensorRT Integration

Utilise TensorRT NVIDIA pour optimisations GPU avancées avec précision mixte.

2-5x

speedup GPU

FP16

précision mixte

📱

Edge Optimization

Optimisations spécifiques pour déploiement mobile et edge computing.

<100MB

taille modèle

CPU

uniquement

\# Optimisation ONNX Runtime pour production import onnxruntime as ort import numpy as np class OptimizedBERTInference: def \_\_init\_\_(self, onnx\_model\_path, use\_gpu=True): # Configuration des providers providers = \[\] if use\_gpu and ort.get\_device() == 'GPU': providers.append(('TensorrtExecutionProvider', { 'trt\_fp16\_enable': True, 'trt\_max\_workspace\_size': 2147483648, # 2GB 'trt\_max\_partition\_iterations': 1000, })) providers.append('CUDAExecutionProvider') providers.append('CPUExecutionProvider') # Optimisations du graphe sess\_options = ort.SessionOptions() sess\_options.graph\_optimization\_level = ort.GraphOptimizationLevel.ORT\_ENABLE\_ALL sess\_options.optimized\_model\_filepath = "optimized\_model.onnx" # Parallel execution sess\_options.intra\_op\_num\_threads = 4 sess\_options.inter\_op\_num\_threads = 4 # Création de la session self.session = ort.InferenceSession( onnx\_model\_path, sess\_options=sess\_options, providers=providers ) self.input\_names = \[inp.name for inp in self.session.get\_inputs()\] self.output\_names = \[out.name for out in self.session.get\_outputs()\] def predict\_batch(self, input\_ids, attention\_mask, token\_type\_ids=None): """ Prédiction optimisée avec support batch """ # Préparation inputs ort\_inputs = { 'input\_ids': input\_ids.astype(np.int64), 'attention\_mask': attention\_mask.astype(np.int64) } if token\_type\_ids is not None: ort\_inputs\['token\_type\_ids'\] = token\_type\_ids.astype(np.int64) # Inférence outputs = self.session.run(self.output\_names, ort\_inputs) return outputs\[0\] # logits def benchmark\_performance(self, test\_inputs, num\_runs=100): """ Benchmark des performances """ import time # Warmup for \_ in range(10): self.predict\_batch(\*\*test\_inputs) # Mesure start\_time = time.time() for \_ in range(num\_runs): self.predict\_batch(\*\*test\_inputs) avg\_time = (time.time() - start\_time) / num\_runs throughput = test\_inputs\['input\_ids'\].shape\[0\] / avg\_time return { 'avg\_latency\_ms': avg\_time \* 1000, 'throughput\_samples\_per\_sec': throughput, 'memory\_usage': self.get\_memory\_usage() }

**📊 Gains de Performance Typiques :**  
• ONNX CPU : 20-40% plus rapide que TensorFlow  
• ONNX + TensorRT : 3-5x plus rapide sur GPU  
• Optimisations automatiques : Aucun code supplémentaire  
• Compatibilité : Support multi-plateforme

## 🎪 Stratégies Combinées et Best Practices

### 🚀 Pipeline d'Optimisation Complète

#### 🎯 Simulateur de Pipeline d'Optimisation

Conservative Équilibré Agressif

Sélectionnez une approche pour voir le pipeline...

**🎯 Recommandations par Use Case :**  
• Latence critique (<10ms) : DistilBERT + INT8 + ONNX  
• Qualité prioritaire : FP16 + Graph optimization  
• Edge deployment : TinyBERT + Quantization + Pruning  
• Cost-sensitive : CPU-only avec optimisations maximales

**⚠️ Validation et Tests :**  
• A/B Testing : Comparer avec modèle original en production  
• Regression Testing : Suite de tests automatisés  
• Performance Monitoring : Métriques continues  
• Rollback Strategy : Plan de retour arrière rapide

[← Architecture](module8_architecture_production.md)

**Optimisation des Modèles**  
Distillation, Quantization, ONNX

[Déploiement →](module8_deploiement_production.md)

// Animation de la barre de progression window.addEventListener('load', function() { setTimeout(() => { document.getElementById('progressBar').style.width = '100%'; }, 1000); }); // Comparateur d'optimisations function compareOptimizations(technique) { let comparison = ''; switch(technique) { case 'original': comparison = \`🤖 BERT-Base Original 📊 Caractéristiques : • Paramètres : 340M • Taille mémoire : 1.3GB • Latence CPU : 200ms • Latence GPU : 50ms • Qualité : 100% (référence) 💰 Coût mensuel estimé : • GPU V100 : $500/mois • Instances : 4x pour 1000 req/sec • Total infrastructure : $2000/mois ⚠️ Limitations : • Trop lent pour temps réel • Coût élevé pour scaling • Empreinte mémoire importante\`; break; case 'distillation': comparison = \`🎓 DistilBERT (Distillation) 📊 Caractéristiques : • Paramètres : 66M (-80%) • Taille mémoire : 500MB (-62%) • Latence CPU : 100ms (-50%) • Latence GPU : 25ms (-50%) • Qualité : 97% (-3%) 💰 Coût mensuel estimé : • GPU T4 : $200/mois • Instances : 2x pour 1000 req/sec • Total infrastructure : $400/mois ✅ Avantages : • Excellent rapport qualité/performance • Peu de perte de précision • Compatible production temps réel\`; break; case 'quantization': comparison = \`🗜️ BERT + INT8 Quantization 📊 Caractéristiques : • Paramètres : 340M (même) • Taille mémoire : 325MB (-75%) • Latence CPU : 50ms (-75%) • Latence GPU : 20ms (-60%) • Qualité : 96% (-4%) 💰 Coût mensuel estimé : • CPU instances : $100/mois • Instances : 2x pour 1000 req/sec • Total infrastructure : $200/mois ✅ Avantages : • Déploiement CPU viable • Très économique • Bonne pour edge computing\`; break; case 'combined': comparison = \`🚀 DistilBERT + INT8 + ONNX 📊 Caractéristiques : • Paramètres : 66M (-80%) • Taille mémoire : 165MB (-87%) • Latence CPU : 25ms (-87%) • Latence GPU : 10ms (-80%) • Qualité : 95% (-5%) 💰 Coût mensuel estimé : • CPU instances : $50/mois • Instances : 1x pour 1000 req/sec • Total infrastructure : $50/mois 🎯 Performance Production : • <10ms latence P95 • >10,000 req/sec single instance • Déploiement edge possible • ROI optimal\`; break; } document.getElementById('optimizationOutput').innerHTML = \`<div style="text-align: left; font-size: 0.9em; line-height: 1.4; white-space: pre-line;">${comparison}</div>\`; } // Simulateur de pipeline d'optimisation function simulateOptimizationPipeline(approach) { let pipeline = ''; switch(approach) { case 'conservative': pipeline = \`🛡️ Approche Conservative 🎯 Objectif : Minimiser les risques 📊 Perte qualité acceptée : <2% 📋 Pipeline : 1. 🧪 Tests baseline exhaustifs 2. 💨 FP16 quantization uniquement 3. 🔧 ONNX graph optimization 4. 📊 Benchmarks approfondis 5. 🚀 Déploiement progressif ⏱️ Timeline : 3-4 semaines 🎯 Gains attendus : • Latence : -30% • Mémoire : -50% • Qualité : -1% ✅ Recommandé pour : • Applications critiques • Environnements réglementés • Première optimisation\`; break; case 'balanced': pipeline = \`⚖️ Approche Équilibrée 🎯 Objectif : Bon compromis perf/qualité 📊 Perte qualité acceptée : <5% 📋 Pipeline : 1. 🎓 Distillation vers DistilBERT 2. 🗜️ INT8 quantization post-training 3. 🚀 ONNX Runtime optimization 4. 📊 A/B testing en production 5. 🔄 Monitoring continu ⏱️ Timeline : 6-8 semaines 🎯 Gains attendus : • Latence : -70% • Mémoire : -75% • Qualité : -3% ✅ Recommandé pour : • Applications grand public • Besoins de scalabilité • Budget infrastructure limité\`; break; case 'aggressive': pipeline = \`🚀 Approche Agressive 🎯 Objectif : Performance maximale 📊 Perte qualité acceptée : <10% 📋 Pipeline : 1. 🎓 TinyBERT distillation 2. 🗜️ INT8 quantization + pruning 3. ✂️ Architecture search optimization 4. 🚀 Custom ONNX operators 5. 📱 Edge deployment ready ⏱️ Timeline : 10-12 semaines 🎯 Gains attendus : • Latence : -90% • Mémoire : -95% • Qualité : -8% ✅ Recommandé pour : • Applications mobile/edge • Contraintes hardware extrêmes • Use cases tolérants aux erreurs\`; break; } document.getElementById('pipelineOutput').innerHTML = \`<div style="text-align: left; font-size: 0.9em; line-height: 1.4; white-space: pre-line;">${pipeline}</div>\`; }
