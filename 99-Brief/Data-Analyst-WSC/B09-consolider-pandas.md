# Brief B09 — Consolider quatre sources hétérogènes avec pandas

## Informations

| | |
|---|---|
| **Semaine** | S11 · 23–27 nov 2026 · 5 jours · Guillaume |
| **Modalité · Évaluation** | Binôme · Formatif |
| **Compétences visées** | C2.5 · C4.5 · C2.3 · C3.1 · C1.4 |

## Description

Une centrale d'achat reçoit chaque mois les ventes de ses quatre enseignes, dans quatre formats qui ne se ressemblent pas. Aujourd'hui, une personne les recopie à la main dans un classeur. Vous automatisez cette fusion avec pandas.

## Contexte

Le groupement Saveurs de France fédère quatre enseignes de distribution alimentaire, rachetées à des moments différents et jamais vraiment intégrées. Chaque enseigne a conservé son système de caisse.

Chaque début de mois, la contrôleuse de gestion du groupement, Nadia, reçoit quatre exports de ventes. Le premier est un CSV en UTF-8 séparé par des virgules. Le deuxième, un CSV en Latin-1 séparé par des points-virgules, avec les montants à la française (virgule décimale). Le troisième, un fichier Excel à trois onglets. Le quatrième, un export texte à largeur fixe hérité d'un logiciel des années 2000.

Les colonnes ne portent pas les mêmes noms. « Référence produit » ici, « code_article » là, « SKU » ailleurs. Les dates sont tantôt au format JJ/MM/AAAA, tantôt AAAA-MM-JJ, tantôt en numéro de série Excel. Une enseigne compte les remises en positif, une autre en négatif.

Nadia passe deux jours par mois à recopier tout cela dans un classeur maître, à la main, avec les erreurs que cela suppose. Elle vous le dit sans détour : « Je fais un travail de photocopieuse. Je veux lancer quelque chose qui me sorte le fichier consolidé, propre, tous les mois. »

Le tableur a montré ses limites en B03 sur trois fichiers. Ici il y en a quatre, plus lourds, à refaire chaque mois. C'est exactement ce pour quoi pandas existe : importer des formats hétérogènes, les aligner, les fusionner, et rejouer l'opération d'un mois sur l'autre sans effort.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C2.5** — Utiliser les tableaux de données (DataFrames avec Python et Pandas) afin de faciliter l'import, la manipulation et la fusion de données *(niveau 1 — imiter)*
- **C4.5** — Utiliser un tableur, notamment les TCD *(niveau 2 — adapter)*
- **C2.3** — Manipuler des structures de données et utiliser l'algorithmie *(niveau 2 — adapter)*
- **C3.1** — Utiliser les statistiques descriptives *(niveau 2 — adapter)*
- **C1.4** — Réaliser des requêtes avancées *(niveau 2 — adapter)*

## Modalités pédagogiques

**Organisation** : binôme, dépôt commun.

**Jour 1 — matin (lancement, 2 h)**. Le formateur joue Nadia. Vous recevez les quatre fichiers d'un mois réel. Première tâche sans code : dressez la carte des différences. Combien de formats de date ? Combien de noms pour désigner le produit ? Quelles colonnes n'existent que dans certains fichiers ?

**Jour 1 — après-midi**. Vous tentez la fusion au tableur, comme en B03. Vous mesurez pourquoi cela ne passe pas à l'échelle.

**Jour 2 — matin (apport flash, 2 h 30)**. pandas : `read_csv`, `read_excel`, gestion des encodages et séparateurs. Le DataFrame : sélection, filtrage, création de colonnes. `rename`, conversion de types, `to_datetime`. `concat` et `merge` — présenté comme la version programmée de la recherche inter-fichiers.

**Jours 2 à 4 — production**. Construisez un pipeline qui :
1. importe les quatre fichiers malgré leurs formats ;
2. harmonise les noms de colonnes vers un schéma commun que vous définissez ;
3. uniformise les types : dates, montants, signe des remises ;
4. concatène en un jeu unique, avec une colonne indiquant l'enseigne d'origine ;
5. produit un rapport de fusion : lignes par source, lignes finales, écarts inexpliqués.

**Questions guidantes.** Si une colonne existe dans trois fichiers sur quatre, que mettez-vous pour le quatrième — zéro, vide, une valeur signalant l'absence, et quelle différence pour Nadia ? Comment vérifiez-vous qu'aucune ligne n'a été perdue ni dupliquée pendant la fusion ? Le total des ventes du fichier consolidé doit-il égaler la somme des quatre totaux d'origine, et comment le prouvez-vous ? Si le mois prochain une enseigne change son format, combien de votre code faut-il réécrire ?

**Jour 4 — après-midi (revue croisée)**. Chaque binôme relance le pipeline d'un autre sur un cinquième fichier fourni au dernier moment. Un pipeline qui ne survit pas à un nouveau fichier n'est pas terminé.

**Jour 5**. Finalisation, publication, restitution 8 minutes.

## Modalités d'évaluation

Brief **formatif**. Auto-évaluation, revue croisée, retour collectif.

Le test décisif est celui de la réconciliation : le total consolidé doit être traçable jusqu'aux totaux d'origine, et tout écart doit être expliqué. Un pipeline qui produit un beau fichier dont on ne peut pas garantir qu'il n'a rien perdu est inutilisable en contrôle de gestion.

Le formateur insistera en retour collectif sur la différence entre un code qui marche sur les quatre fichiers de démonstration et un code qui résiste à un cinquième fichier inconnu — c'est la définition de la réutilisabilité.

## Données fournies (source exacte)

> Produits **réels** (OpenFoodFacts) ; 4 exports de ventes **synthétiques** aux formats divergents.

- **Référentiel produits** : `data/produits_reference.csv` — 60 produits réels via l'API
  **OpenFoodFacts** (code-barres + nom).
- **4 exports de ventes** dans `sources/` : `enseigne_A.csv` (UTF-8, virgule) · `enseigne_B.csv`
  (Latin-1, `;`, décimales FR, remise négative) · `enseigne_C.xlsx` (Excel 3 onglets) ·
  `enseigne_D.txt` (largeur fixe, sans en-tête, sans colonne remise).
- **Reproductibles** : `python3 generer_sources.py`.

## Livrables attendus

**Un dépôt GitHub public** par binôme :

1. `README.md` — projet, formats gérés, installation, lancement, auteurs.
2. `carte-des-differences.md` — l'inventaire des écarts entre sources, produit le jour 1.
3. `pipeline/consolidation.py` — le pipeline, découpé en fonctions (une par étape).
4. `schema-cible.md` — le schéma commun choisi : noms de colonnes, types, conventions.
5. `rapport-fusion.md` — lignes par source, lignes finales, réconciliation des totaux, écarts expliqués.
6. `sortie/consolide.csv` — le fichier produit.

## Critères de performance

**C2.5 — DataFrames, niveau imiter**
• Les quatre formats sont importés par le script, sans conversion manuelle préalable.
• Les encodages et séparateurs différents sont gérés dans le code.
• Une fusion (`concat` ou `merge`) produit un jeu unique.
• Les types sont uniformisés : dates converties, montants numériques, signe des remises homogène.

**C4.5 — Tableur, niveau adapter (réactivation)**
• Le fichier consolidé est vérifié par un TCD croisant enseigne et mois.
• La réconciliation des totaux est présentée dans un tableau lisible.

**C2.3 — Algorithmie, niveau adapter**
• Le pipeline est découpé en fonctions à responsabilité unique.
• L'ajout d'une source suppose de modifier une seule fonction, ce qui est démontré lors de la revue croisée.

**C3.1 — Statistiques, niveau adapter**
• Le rapport présente un profil du jeu consolidé : nombre de lignes, période couverte, chiffre d'affaires total, panier moyen.

**C1.4 — Requêtes, niveau adapter (réactivation)**
• Au moins un contrôle de cohérence est exprimé sous forme de requête ou d'équivalent pandas (détection de doublons, de lignes orphelines).

## Ressources

- pandas — guide de démarrage (10 minutes) : https://pandas.pydata.org/docs/user_guide/10min.html
- pandas — read_csv (encodages, séparateurs) : https://pandas.pydata.org/docs/reference/api/pandas.read_csv.html
- pandas — merge, join, concatenate : https://pandas.pydata.org/docs/user_guide/merging.html
- pandas — travailler avec les dates : https://pandas.pydata.org/docs/user_guide/timeseries.html
- OpenFoodFacts — données ouvertes : https://world.openfoodfacts.org/data
