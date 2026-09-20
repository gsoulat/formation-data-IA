# Brief B11 — Registre patients : fiabiliser un jeu de données et argumenter sa méthode

## Informations

| | |
|---|---|
| **Semaine** | S13 · 7–11 déc 2026 · 5 jours · Ayoub |
| **Modalité · Évaluation** | Individuel · Sommatif |
| **Compétences visées** | C2.6 · C2.7 · C2.1 · C2.5 · C2.4 · C3.1 · C1.7 |

## Description

Un service d'épidémiologie ne peut pas exploiter son registre : 12 % de valeurs manquantes, des poids de 700 kg, des dates de naissance au format libre. Vous le fiabilisez — mais chaque décision de nettoyage doit être justifiée, car en santé, effacer une donnée n'est jamais neutre.

## Contexte

Le service d'épidémiologie d'un centre hospitalier régional tient un registre des patients admis pour une pathologie chronique. Ce registre doit alimenter une étude sur les facteurs de risque, mais la responsable de recherche a suspendu l'analyse : les données sont trop sales pour être exploitées telles quelles.

Le fichier cumule les problèmes. Environ 12 % des valeurs sont manquantes, réparties de façon inégale — certaines colonnes sont presque complètes, d'autres à moitié vides. On trouve des poids de 700 kg et des tailles de 3 mètres, manifestement des erreurs de saisie ou d'unité. Les dates de naissance ont été saisies sans contrôle : « 12/03/1958 », « 12 mars 58 », « 1958-03-12 » coexistent. Des numéros de téléphone et des adresses e-mail traînent dans un champ « commentaires » censé être anonyme.

La responsable de recherche vous confie le nettoyage avec un avertissement : « En épidémiologie, supprimer une ligne parce qu'elle vous dérange, c'est potentiellement effacer un cas qui compte. Chaque fois que vous jetez ou modifiez une donnée, je veux savoir pourquoi, et je veux pouvoir ne pas être d'accord. »

C'est le cœur du métier de traitement : nettoyer n'est pas embellir, c'est décider — et documenter ses décisions pour qu'un tiers puisse les contester. Un poids de 700 kg est faux, mais faut-il le supprimer, le corriger, ou le marquer comme manquant ? La réponse n'est pas technique, elle est méthodologique.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C2.6** — Nettoyer les données, retraiter les valeurs aberrantes (outliers) et les valeurs manquantes afin d'éviter les impacts sur l'exploitation *(niveau 1 — imiter)*
- **C2.7** — Utiliser les expressions régulières (RegEx) pour traiter les valeurs textuelles *(niveau 1 — imiter)*
- **C2.1** — Effectuer des choix méthodologiques et les documenter *(niveau 2 — adapter)*
- **C2.5** — Utiliser les DataFrames avec pandas *(niveau 2 — adapter)*
- **C2.4** — Appliquer les bonnes pratiques de la programmation *(niveau 2 — adapter)*
- **C3.1** — Utiliser les statistiques descriptives *(niveau 2 — adapter)*
- **C1.7** — Contrôler les enjeux du RGPD *(niveau 3 — transposer)*

## Modalités pédagogiques

**Organisation** : individuel.

**Jour 1 — matin (lancement, 2 h)**. Le formateur joue la responsable de recherche. Vous recevez le registre. Première tâche sans code : établissez le diagnostic. Quelles colonnes sont touchées, par quel type de problème, dans quelle proportion ?

**Jour 1 — après-midi**. Exploration du fichier avec pandas. Vous quantifiez ce que vous avez repéré à l'œil.

**Jour 2 — matin (apport flash, 2 h)**. Valeurs manquantes : détection, typologie (manquant aléatoire ou non), stratégies (suppression, imputation par moyenne/médiane, marquage). Valeurs aberrantes : détection par écart interquartile et par écart-type, distinction erreur / valeur extrême légitime.

**Jour 3 — matin (apport flash, 1 h 30)**. Expressions régulières : syntaxe, classes de caractères, groupes. Application à l'uniformisation des dates et à la détection des données personnelles (e-mails, téléphones) dans le champ commentaires.

**Jours 2 à 4 — production**. Produisez un outil de nettoyage qui, pour chaque problème :
1. le détecte et le chiffre ;
2. applique une stratégie de traitement que vous avez choisie ;
3. conserve une trace de ce qui a été modifié (jamais d'écrasement silencieux) ;
4. produit un registre nettoyé et un rapport de nettoyage.

Traitez au minimum : valeurs manquantes (stratégie différenciée selon les colonnes), aberrations physiologiques, uniformisation des dates par RegEx, repérage et neutralisation des données personnelles dans les commentaires.

**Questions guidantes.** Un poids manquant et un poids à zéro sont-ils la même chose ? Imputer la médiane sur 40 % de valeurs manquantes, est-ce encore de la donnée ou de l'invention ? Comment distinguer un patient réellement très âgé d'une erreur de date ? Quand vous corrigez « 700 kg » en « 70 kg », qu'est-ce qui vous autorise à supposer que c'est une erreur de virgule plutôt qu'autre chose ? Faut-il tracer la valeur d'origine, et pourquoi ?

**Jour 4 — après-midi (revue croisée)**. Un autre apprenant joue la responsable de recherche et conteste trois de vos décisions de nettoyage. Vous devez les défendre ou les réviser.

**Jour 5**. Finalisation, publication, restitution 8 minutes centrée sur la méthode.

## Modalités d'évaluation

Brief **sommatif**, checklist complète.

L'évaluation pèse plus lourd sur la **justification** que sur la technique. Détecter les aberrations est à la portée d'une fonction ; décider quoi en faire et le défendre devant une chercheuse qui conteste, c'est le niveau attendu. Un apprenant qui nettoie parfaitement sans documenter ses choix ne valide pas C2.1.

C1.7 est ici évalué au **niveau 3** : c'est la troisième rencontre avec le RGPD (après B04 et B08), sur des données de santé, les plus sensibles. La neutralisation des données personnelles dans les commentaires n'est pas optionnelle.

## Données fournies (source exacte)

> Registre patients **100 % synthétique** (les données de santé ne se prennent pas en open data),
> reproductible.

- **Fichier** : `data/registre_brut.csv` — 800 patients avec ~12 % de valeurs manquantes (inégales
  selon les colonnes), des aberrations physiologiques (poids de 700 kg, tailles de 3 m), des dates
  de naissance au **format libre** (3 variantes), et des e-mails/téléphones dans le champ commentaire.
- **Reproduction** : `python3 generer_registre.py` (graine figée).

## Livrables attendus

**Un dépôt GitHub public** :

1. `README.md` — projet, méthode générale, installation, auteur.
2. `diagnostic.md` — l'état des lieux du jour 1 : problèmes par colonne, quantifiés.
3. `nettoyage/outil.py` — l'outil, découpé par type de traitement.
4. `choix-methodologiques.md` — **le livrable central** : pour chaque décision (stratégie de manquants par colonne, seuils d'aberration, règle de correction, traitement des données personnelles), la décision, l'alternative écartée, la justification.
5. `sortie/registre-nettoye.csv` — le registre fiabilisé.
6. `sortie/journal-modifications.csv` — la trace : ligne, colonne, valeur d'origine, valeur après, raison.
7. `rapport-nettoyage.md` — synthèse chiffrée : combien de valeurs traitées, par quelle méthode, avec quel impact sur les distributions.

## Critères de performance

**C2.6 — Nettoyage, niveau imiter**
• Les valeurs manquantes sont détectées et chiffrées par colonne.
• Une stratégie différenciée est appliquée selon les colonnes, et non un traitement uniforme.
• Les valeurs aberrantes sont détectées par une méthode statistique (IQR ou écart-type) et non à l'œil.
• Aucune modification n'écrase silencieusement une valeur : le journal conserve l'origine.

**C2.7 — RegEx, niveau imiter**
• Les dates de naissance sont uniformisées par expression régulière vers un format unique.
• Les e-mails et téléphones du champ commentaires sont détectés par RegEx.
• Au moins une expression régulière est commentée pour expliquer ce qu'elle capture.

**C2.1 — Choix méthodologiques, niveau adapter**
• Chaque décision majeure figure dans `choix-methodologiques.md` avec son alternative écartée.
• Les seuils (aberration, taux de manquants au-delà duquel on ne remplit plus) sont chiffrés et argumentés.
• Les trois décisions contestées en revue croisée ont été défendues ou révisées, avec trace.

**C2.5 / C2.4 / C3.1 — Réactivation**
• Le traitement est réalisé avec pandas, en fonctions réutilisables.
• Le rapport montre l'effet du nettoyage sur les distributions (avant/après : moyenne, médiane, dispersion).

**C1.7 — RGPD, niveau transposer**
• Toutes les données personnelles présentes dans les commentaires sont neutralisées.
• La méthode de neutralisation est justifiée au regard de l'usage épidémiologique.
• Le caractère sensible des données de santé est explicitement pris en compte.

## Ressources

- pandas — données manquantes : https://pandas.pydata.org/docs/user_guide/missing_data.html
- scikit-learn — imputation des valeurs manquantes : https://scikit-learn.org/stable/modules/impute.html
- Python — module re (expressions régulières) : https://docs.python.org/fr/3/library/re.html
- regex101 — testeur d'expressions régulières : https://regex101.com/
- Comprendre l'écart interquartile pour les outliers : https://fr.wikipedia.org/wiki/%C3%89cart_interquartile
- CNIL — données de santé : https://www.cnil.fr/fr/donnees-de-sante
