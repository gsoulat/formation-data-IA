# Brief B02-I — Dites-moi ce qu'il y a dedans : les ventes Cyclo'Nord

## Informations

| | |
|---|---|
| **Semaine** | S2 · lundi 21 – mardi 22 sept 2026 · 2 après-midis (2 × 3 h) · Guillaume |
| **Modalité · Évaluation** | Individuel · Formatif, non noté (correction collective mardi 16 h) |
| **Compétences visées** | C3.1 · C4.2 · C4.5 — **niveau 1 · IMITER** |
| **Cours support** | [Module 00 — Tableur : statistiques & TCD](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/README.md) |
| **Support pas à pas** | [Exercice guidé 05 — Faire parler les ventes Cyclo'Nord](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/05-exercice-guide-cyclonord.md) |

> **Niveau 1 · IMITER** — tu reproduis, sur un jeu de données fourni, les gestes montrés en cours le
> matin même. La méthode est donnée étape par étape et **toutes les valeurs attendues sont fournies** :
> tu peux te corriger seul, au fur et à mesure. Ce qui t'appartient, ce sont les réponses aux questions.

## Description

La semaine dernière, tu as audité le fichier de commandes de Cyclo'Nord. Il a été corrigé. La
responsable commerciale te le rend avec une seule demande : « Dites-moi ce qu'il y a dedans. » Tu as
deux après-midis pour lui répondre avec des chiffres justes, et pour découvrir pourquoi « le chiffre
moyen » est rarement le bon chiffre à lui donner.

## Contexte

Tu es en stage chez **Cyclo'Nord**, une enseigne de vente et de réparation de vélos implantée dans
les Hauts-de-France : huit magasins, d'Arras à Dunkerque, et une boutique en ligne.

En semaine P1, ton audit du fichier des commandes 2025 avait relevé des doublons, des libellés de
magasin incohérents, des dates hors exercice et des quantités impossibles. Ces 14 lignes ont été
retirées, les villes normalisées, les montants recalculés. Il reste **613 commandes**, et l'onglet
`Journal_nettoyage` documente chaque correction.

Nadia Oumejjoud, responsable commerciale, prépare une présentation pour la direction. Elle n'a pas
besoin d'un tableau de bord ; elle a besoin de **savoir quoi dire** sans se tromper :

*« Quel est le montant d'une commande typique ? Nos clients sont-ils satisfaits ? Quel magasin
marche le mieux ? Je veux des chiffres que je peux défendre si quelqu'un me pose une question. »*

En reproduisant les calculs du cours, tu vas tomber sur trois pièges que Nadia n'a pas vus : une
moyenne qui ne ressemble à aucune commande réelle, un chiffre d'affaires qui compte des commandes
annulées, et un magasin premier du classement… grâce à une seule ligne.

## Objectifs pédagogiques

À l'issue de ce brief, tu seras capable de :

- **C3.1** — Utiliser les statistiques descriptives (position, dispersion, valeurs atypiques) pour
  faire émerger une information pertinente *(niveau 1 — imiter)*
- **C4.2** — Produire une visualisation descriptive (boîte à moustaches) titrée et légendée
  *(niveau 1 — imiter)*
- **C4.5** — Utiliser un tableur : tableau structuré, fonctions statistiques et conditionnelles,
  références structurées *(niveau 1 — imiter)*

Concrètement : calculer moyenne, médiane, mode, quartiles, écart-type et moyenne pondérée **par
formule**, et savoir dire lequel utiliser pour décrire quoi.

## Modalités pédagogiques

**Organisation** : individuel. L'entraide est encouragée, mais chacun produit son propre classeur.

**Lundi après-midi — Partie A · Position (3 h).**
Suis les étapes 0 et A1 à A7 de l'[exercice guidé](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/05-exercice-guide-cyclonord.md) :

| Étape | Geste | Durée indicative |
|---|---|---|
| 0 | Préparer le classeur, créer le tableau structuré `T_Ventes` | 10 min |
| A1 | Typer les 13 colonnes : sur lesquelles une moyenne a-t-elle un sens ? | 20 min |
| A2 | Moyenne, médiane, mode sur trois variables | 30 min |
| A3 | Compter les valeurs renseignées avant de commenter | 20 min |
| A4 | Délimiter le périmètre : toutes commandes ou commandes livrées ? | 30 min |
| A5 | Calculer par catégorie avec `NB.SI.ENS`, `SOMME.SI.ENS`, `MOYENNE.SI.ENS` | 45 min |
| A6 | Moyenne simple contre moyenne pondérée (`SOMMEPROD`) | 30 min |
| A7 | Écrire la phrase de restitution pour Nadia | 15 min |

**Mardi après-midi — Partie B · Dispersion (3 h).**

| Étape | Geste | Durée indicative |
|---|---|---|
| B1 | Étendue, écart-type, coefficient de variation | 30 min |
| B2 | Le résumé à cinq nombres et l'IQR | 30 min |
| B3 | Repérer les valeurs atypiques (règle de Tukey, `GRANDE.VALEUR`) | 40 min |
| B4 | Mesurer l'effet d'une seule ligne sur chaque indicateur | 30 min |
| B5 | Construire et habiller une boîte à moustaches par catégorie | 30 min |
| B6 | Le cas Arras : CA total, CA livré, panier médian par magasin | 30 min |

**Mardi 16 h — correction collective (1 h).** On confronte les réponses aux questions ; les valeurs
numériques, elles, sont déjà données.

**Mardi 17 h 30 — dépôt.**

**Questions guidantes.** Une moyenne de 1 680 € décrit-elle une commande Cyclo'Nord réelle ? Une
note moyenne calculée sur 560 notes peut-elle être présentée comme celle de 613 commandes ? Une
commande annulée fait-elle partie du chiffre d'affaires ? Si retirer **une seule ligne** fait
baisser un indicateur de 37 %, cet indicateur est-il fiable pour décrire l'activité ?

## Modalités d'évaluation

Brief **formatif, non noté**. Auto-évaluation avec la grille des critères ci-dessous, puis
correction collective mardi 16 h.

Au niveau 1, **retrouver les valeurs attendues ne suffit pas** — elles sont données. Ce qui montre
que le geste est acquis :

- les valeurs sont obtenues **par formule**, avec des références structurées (`T_Ventes[...]`),
  jamais saisies en dur ;
- chaque question reçoit une réponse **rédigée**, qui interprète le chiffre au lieu de le recopier ;
- chaque chiffre est accompagné de son **périmètre** (quelles commandes, combien de valeurs).

Un chiffre juste annoncé sans son périmètre sera compté comme faux.

## Données fournies

> L'entreprise Cyclo'Nord et ses données sont **fictives**, conçues pour la formation.

- **Fichier** : [`cyclonord_ventes_2025_fiable.xlsx`](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/donnees/cyclonord_ventes_2025_fiable.xlsx)
  — onglets `Ventes_2025` (613 lignes), `Dictionnaire`, `Journal_nettoyage`
- **Généalogie** : version fiabilisée de `cyclonord_commandes_2025_brut.xlsx` (627 lignes), le
  fichier audité en P1 — 14 lignes écartées (2,2 %), détail dans `Journal_nettoyage` et dans
  [`donnees/SOURCES.md`](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/donnees/SOURCES.md)
- **Périmètre** : 8 magasins des Hauts-de-France, 5 catégories, exercice 2025

**Structure du fichier** : `ID_commande`, `Date_commande`, `Magasin`, `Departement`, `Categorie`,
`Produit`, `Canal`, `Quantite`, `Prix_unitaire_TTC`, `Remise`, `Montant_TTC`, `Statut`,
`Note_client`.

> ⚠️ **Laissé exprès** : trois commandes de quantité 100 ont été **conservées** dans le fichier.
> Elles ne sont pas des erreurs de saisie évidentes. Les repérer et décider quoi en faire fait
> partie de l'exercice (étape B3).

## Livrables attendus

**Sur ton dépôt GitHub** (celui créé en semaine 1, qui te sert de portfolio), dans un dossier
`02-cyclonord-stats/`. Dernier push **mardi 22/09 avant 17 h 30**.

1. **`cyclonord_stats.xlsx`**

   | Onglet | Contenu |
   |---|---|
   | `Ventes_2025` | **intact** — aucune modification de la donnée source |
   | `Dictionnaire`, `Journal_nettoyage` | conservés tels quels |
   | `Position` | étapes A1 à A7, formules apparentes, réponses aux questions |
   | `Dispersion` | étapes B1 à B6, formules apparentes, réponses aux questions, boîte à moustaches |
   | `Conclusion` | **10 lignes maximum** : *« que faut-il retenir de ces 613 commandes, et quel chiffre unique donneriez-vous à la direction ? »* |

2. **`README.md`** — cinq lignes : de quoi parle le classeur, ce que tu as calculé, et ta phrase de
   restitution de l'étape A7.

> 🔧 Un classeur est un fichier binaire : Git ne montre pas ce qui a changé d'une version à l'autre.
> Committe au fur et à mesure (fin de partie A lundi, fin de partie B mardi) plutôt qu'en une fois.

## Critères de performance

**C3.1 — Statistiques descriptives (niveau 1)**
• Toutes les valeurs attendues de l'exercice guidé sont retrouvées.
• Chaque calcul indique son **périmètre** (toutes commandes / livrées, nombre de valeurs renseignées).
• L'écart entre moyenne et médiane est interprété en termes de **forme** de la distribution.
• Les valeurs atypiques sont identifiées **et** une décision (garder, écarter, analyser à part) est justifiée.
• La conclusion propose **un chiffre unique** pour la direction et le défend.

**C4.2 — Visualisations descriptives (niveau 1)**
• La boîte à moustaches par catégorie est produite.
• Elle porte un titre qui énonce un message, un axe nommé avec unité (« Montant TTC (€) ») et une
note de source.

**C4.5 — Tableur (niveau 1)**
• La donnée source est intacte.
• Le tableau structuré `T_Ventes` est créé et utilisé : les formules emploient des références
structurées, pas des plages `K2:K614`.
• Les indicateurs sont **calculés par formule**, jamais saisis en dur : un correcteur qui clique sur
une cellule voit la formule.
• La limite « pas de `MEDIANE.SI.ENS` » est contournée et la méthode est notée dans le classeur.

**Transversal**
• Les onglets sont nommés comme demandé, les cellules de résultat sont identifiables.
• Le `README.md` permet de comprendre le classeur sans l'ouvrir.

**Positionnement** : ● Acquis · ◐ En cours d'acquisition · ○ Non acquis

## Ressources

- [Exercice guidé 05 — pas à pas et valeurs attendues](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/05-exercice-guide-cyclonord.md)
- [Cours 01 — Statistiques descriptives : moyenne, médiane, mode](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/01-statistiques-descriptives.md)
- [Cours 02 — Dispersion : écart-type, quartiles et pièges de la moyenne](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/02-dispersion-et-pieges-de-la-moyenne.md)
- Microsoft — [utiliser des références structurées avec les tableaux Excel](https://support.microsoft.com/fr-fr/office/utilisation-de-r%C3%A9f%C3%A9rences-structur%C3%A9es-avec-des-tableaux-excel-f5ed2452-2337-4f71-bed3-c8ae6d2b276e)
- Microsoft — [fonctions statistiques Excel](https://support.microsoft.com/fr-fr/office/fonctions-statistiques-r%C3%A9f%C3%A9rence-624dac86-a375-4435-bc25-76d6df3c5b6f)
- Microsoft — [créer un graphique en boîte à moustaches](https://support.microsoft.com/fr-fr/office/cr%C3%A9er-un-graphique-en-bo%C3%AEte-%C3%A0-moustaches-62f4219f-db4b-4754-aca8-4743f6190f0d)

## Pour aller plus loin (facultatif)

- Refais la moyenne pondérée de l'étape A6 **par magasin**. Quel magasin voit sa note le plus
  dégradée par la pondération, et que cela dit-il de ses grosses commandes ?
- Calcule le coefficient de variation de `Montant_TTC` **par catégorie**. Dans quelle catégorie le
  panier moyen est-il un indicateur utilisable, et dans laquelle ne l'est-il pas ?
- Ouvre le fichier brut de P1 et recalcule la moyenne et la médiane de `Montant_TTC` avant
  nettoyage. Lequel des deux indicateurs le nettoyage a-t-il le plus changé ? Pourquoi ?
