# Brief B02-T — Quels territoires des Hauts-de-France aider en priorité ?

## Informations

| | |
|---|---|
| **Quand** | 2ᵉ semaine, **mardi → vendredi** · dépôt **vendredi 12 h 30** · restitutions vendredi 13 h 30 – 16 h 30 |
| **Organisation** | individuel ; entraide encouragée, chacun son classeur |
| **Outil** | Google Sheets |
| **Compétences visées** | C3.1 · C4.2 · C4.5 — **niveau 3 · TRANSPOSER, accompagné** |
| **Cours support** | [Module 00](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/README.md), dont le [cours 06 — Joindre deux tableaux avec XLOOKUP](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/06-joindre-deux-tableaux-xlookup.md) (démo mardi matin) |

## Ce que tu dois produire

À la fin de la semaine, tu remets **une liste de 5 à 12 intercommunalités à aider en priorité**, et
**la règle chiffrée** qui les a désignées (par exemple : « taux de pauvreté supérieur à 19 % et
population en baisse »). Tout le reste du brief sert à construire cette liste et à pouvoir la défendre.

> **Niveau 3 · TRANSPOSER, accompagné.** Les étapes et les formules sont données, et chaque soir un
> point de contrôle te dit si ton tableau est juste. Ce que **toi seul** décides : les **deux
> indicateurs** qui servent à choisir, la **règle** qui en découle, et les **limites** que tu
> signales. Deux apprenants peuvent rendre deux listes différentes et avoir tous les deux raison,
> s'ils savent expliquer pourquoi.

## Contexte

Le cabinet **Orion Études** travaille pour une agence de développement économique des
Hauts-de-France. L'agence a un budget d'aide (conseil, subventions) qu'elle ne peut pas répartir
sur toute la région : elle doit choisir **quelques territoires**. Sa directrice, Claire Vandamme,
te demande un portrait statistique qui l'aide à trancher :

> « Je ne vais pas te dire quels indicateurs regarder. Ce que je dois pouvoir faire après t'avoir
> lu : **désigner des territoires prioritaires et justifier ce choix devant des élus qui vont
> contester**. »

Elle ajoute une consigne :

> « Le dernier cabinet m'a donné une moyenne où une commune de 200 habitants comptait autant que
> Lille. Un élu l'a vu. Je ne veux plus de ça. »

Autrement dit : quand tu calcules une moyenne régionale, une intercommunalité d'un million
d'habitants doit peser plus qu'une intercommunalité de 10 000 habitants. C'est la **moyenne
pondérée** (cours 02), que tu compareras à la moyenne simple.

## Vocabulaire du brief

| Terme | Ce que ça veut dire ici |
|---|---|
| **Intercommunalité** (ou **EPCI**) | Un groupe de communes voisines qui gèrent ensemble certains services. Les Hauts-de-France comptent **3 782 communes** regroupées en **92 intercommunalités**. Chaque commune appartient à une seule intercommunalité. |
| **Code_EPCI** | Le numéro officiel d'une intercommunalité (9 chiffres). C'est la **clé** qui permet de relier les deux fichiers entre eux. On joint toujours sur le code, jamais sur le nom. |
| **Niveau de vie médian** | Le revenu annuel par personne tel que la moitié des habitants gagnent moins et l'autre moitié plus. En euros. |
| **Taux de pauvreté** | La part des habitants qui vivent sous le seuil de pauvreté. En %. |
| **Moyenne pondérée** | Une moyenne où chaque territoire compte proportionnellement à sa population, au lieu de compter pour 1. |
| **Secret statistique** | L'INSEE ne publie pas un chiffre quand la commune est trop petite : on pourrait deviner la situation d'une famille. C'est pour ça que le taux de pauvreté manque pour la plupart des communes, mais est publié pour toutes les intercommunalités. |

## Données fournies

> Le cabinet et l'agence sont **fictifs**. Les **données sont réelles** et publiques (Licence Ouverte).

**Fichier 1 — [`portrait_territoire_hdf_socle.xlsx`](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/donnees/portrait_territoire_hdf_socle.xlsx)** (source : API Géo et DVF, Etalab)

| Onglet | Une ligne = | Colonnes utiles pour ce brief |
|---|---|---|
| `Communes_HDF` | une commune (3 782 lignes) | `Code_EPCI`, `EPCI`, `Population`, `Superficie_km2` |
| `Marche_immobilier_2024` | une commune où il y a eu des ventes (1 812 lignes) | pas utilisé, sauf « pour aller plus loin » |
| `Dictionnaire` · `Sources` | la description des colonnes · l'origine des chiffres | à lire une fois. Les lignes « Facultatif » de `Sources` ne servent qu'au « pour aller plus loin » : **tu n'as rien à télécharger** pour faire le brief |

**Fichier 2 — [`insee_revenus_population_hdf-v.xlsx`](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/donnees/insee_revenus_population_hdf-v.xlsx)** (source : INSEE, comparateur de territoires)

| Onglet | Une ligne = | Colonnes utiles pour ce brief |
|---|---|---|
| `INSEE_EPCI` | une intercommunalité (92 lignes) | `Code_EPCI`, `Nom_EPCI`, `Population_2017`, `Population_2023`, `Niveau_vie_median_2023`, `Taux_pauvrete_2023` |
| `INSEE_Communes` | une commune (3 782 lignes) | pas utilisé, sauf à l'étape 5 (compter ce qui manque) |
| `INSEE_Source` | l'origine et les dates des chiffres | à lire une fois |

**On travaille à l'échelle des 92 intercommunalités**, parce que c'est le seul niveau où tous
les indicateurs sont publiés. Le tableau que tu construis a donc **92 lignes**, une par
intercommunalité.

## Déroulé, jour par jour

### Mardi — réunir les données dans un seul tableau

- **Démo du formateur** (cours 06) : relier deux tableaux avec `XLOOKUP`, calculer une moyenne pondérée.
- **Étape 1 — Importer** (1 h). Un classeur `NOM_Prenom_territoire`. Importe le fichier 1, puis le
  fichier 2, chacun dans de **nouvelles feuilles**. Ne modifie jamais ces feuilles importées.
- **Étape 2 — Construire le tableau `Analyse`** (3 h). Un onglet `Analyse`, **une ligne par
  intercommunalité**. Commence par copier les colonnes `Code_EPCI` et `Nom_EPCI` depuis
  `INSEE_EPCI` (92 lignes). Puis ajoute les colonnes suivantes, **toutes par formule** :

  | Colonne | Comment l'obtenir | Depuis |
  |---|---|---|
  | Nombre de communes | `COUNTIFS` sur `Code_EPCI` | `Communes_HDF` |
  | Superficie (km²) | `SUMIFS` de `Superficie_km2` sur `Code_EPCI` | `Communes_HDF` |
  | Population 2017 et 2023 | `XLOOKUP` sur `Code_EPCI` | `INSEE_EPCI` |
  | Niveau de vie médian 2023 | `XLOOKUP` sur `Code_EPCI` | `INSEE_EPCI` |
  | Taux de pauvreté 2023 | `XLOOKUP` sur `Code_EPCI` | `INSEE_EPCI` |
  | Évolution de la population (%) | (pop 2023 − pop 2017) ÷ pop 2017 × 100 | calcul |
  | Nombre de personnes pauvres | taux de pauvreté × pop 2023 ÷ 100 | calcul |
  | Densité (hab/km²) | pop 2023 ÷ superficie | calcul |

✅ **Point de contrôle mardi soir** : 92 lignes ; la somme de la colonne « nombre de communes »
fait **3 782** ; la ligne *Métropole Européenne de Lille* affiche 95 communes, 1 195 234 habitants
et un taux de pauvreté de 21,4 %. Si un chiffre ne colle pas, c'est la jointure : vérifie que tu as
bien utilisé `Code_EPCI` et pas le nom.

### Mercredi — décrire la région

- **Étape 3 — Position et dispersion** (2 h 30). Onglet `Indicateurs`. Pour le **taux de pauvreté**
  puis pour le **niveau de vie médian**, calcule sur les 92 lignes : minimum, Q1, médiane, Q3,
  maximum, **moyenne simple**, et **moyenne pondérée par la population 2023** (cours 02). Sous
  chaque bloc, écris une phrase : que dit l'écart entre moyenne simple et moyenne pondérée ?
- **Étape 4 — Ce qui manque** (1 h). Onglet `Manquants`, deux questions :
  1. Dans `INSEE_Communes`, combien de communes ont la mention `non publié` à la place du taux
     de pauvreté, et combien d'habitants vivent dans ces communes ? (`COUNTIF`, `SUMIFS`, avec
     `"non publié"` comme condition.)
  2. Additionne `Population_2023` des 92 lignes de `INSEE_EPCI`, puis `Population` des 3 782 lignes
     de `Communes_HDF`. Les deux totaux sont différents. Pourquoi ? *(Réponse à trouver : deux
     intercommunalités ont des communes en Normandie, que l'INSEE compte et que le socle
     Hauts-de-France ne compte pas. Trouve lesquelles.)*
- **Étape 5 — Choisir tes deux critères** (1 h). Onglet `Methode`. Parmi les quatre indicateurs
  suivants, choisis les **deux** qui serviront à désigner les territoires prioritaires :
  taux de pauvreté · nombre de personnes pauvres · évolution de la population · niveau de vie médian.
  Écris en trois lignes pourquoi ces deux-là **pour cette question** (aider des territoires), et
  pourquoi pas les deux autres.

✅ **Point de contrôle mercredi soir** : taux de pauvreté des 92 intercommunalités, moyenne
simple **16,1 %**, moyenne pondérée **19,1 %** (le taux régional publié par l'INSEE est 19 %),
médiane **14,5 %**, maximum **33,5 %**.

### Jeudi — décider, montrer

- **Étape 6 — La règle** (2 h). Onglet `Decision`. Écris ta règle avec tes deux critères, par
  exemple *« taux de pauvreté ≥ 19 % ET population en baisse »* ou *« dans les 15 premiers en taux
  de pauvreté ET dans les 15 premiers en nombre de personnes pauvres »*. Mets tes seuils dans des
  cellules à part, puis applique la règle avec `FILTER` (ou `RANK` puis `FILTER`) pour obtenir la
  liste. Elle doit compter **entre 5 et 12 territoires** : si elle est trop longue ou trop courte,
  change un seuil et note dans `Methode` ce que tu as changé et pourquoi.
- **Étape 7 — Trois graphiques** (2 h 30), onglet `Graphiques`, de trois familles différentes :
  - des **barres triées** : tes territoires retenus, sur ton premier critère ;
  - un **histogramme** : la répartition du taux de pauvreté des 92 intercommunalités ;
  - un **nuage de points** : tes deux critères, un point par intercommunalité, tes retenus visibles.
  Chacun a un titre qui dit le message, des axes avec unité, la source, et une **phrase de lecture**.

✅ **Point de contrôle jeudi soir** : une liste de 5 à 12 territoires produite par `FILTER`, trois
graphiques titrés.

### Vendredi — convaincre

- **9 h – 12 h 30** : la note pour Claire et ta diapositive.
- **12 h 30** : dépôt.
- **13 h 30 – 16 h 30 — restitutions** : 5 minutes chacun (3 minutes de présentation, 2 minutes de
  question), avec **une seule diapositive**. Tu termines par la phrase : *« J'accompagnerais en
  priorité ______, parce que ______. »* Claire pose toujours la même question : *« Un élu me dit que
  votre critère est injuste. Je lui réponds quoi ? »* Prépare ta réponse.
- **16 h 30 – 17 h** : retour collectif.

## Livrables (vendredi 12 h 30)

1. **Le classeur Google Sheets**, partagé en **Lecteur** par lien, avec les onglets `Analyse`,
   `Indicateurs`, `Manquants`, `Methode`, `Decision`, `Graphiques`. Les feuilles importées ne sont
   pas modifiées.
2. Sur ton dépôt GitHub, le dossier **`P2-territoire/`** avec :
   - `README.md` : **la note pour Claire**, une page au plus, en trois parties :
     1. **La réponse** : la liste des territoires retenus et la règle qui les désigne.
     2. **Pourquoi cette règle** : tes deux critères, l'écart entre moyenne simple et pondérée de
        ton premier critère, et ce que cet écart change.
     3. **Deux limites** de ton analyse, puis les sources avec leur date et le **lien** vers ton classeur.
   - `diapositive.pdf` : ta diapositive de restitution ;
   - `territoire.xlsx` : *Fichier › Télécharger › Microsoft Excel*.

## Critères de performance

**C3.1 — Statistiques descriptives (niveau 3)**
- Les deux critères sont choisis et justifiés au regard de la question, et les deux écartés sont nommés.
- Position **et** dispersion sont calculées pour les deux indicateurs décrits.
- Les moyennes simple et pondérée sont calculées, l'écart est chiffré et sa conséquence est dite.
- Les données manquantes sont comptées et expliquées (secret statistique, intercommunalités à cheval sur la Normandie).
- La note se termine par une **décision** : une liste de territoires et la règle qui la produit.

**C4.2 — Visualisations (niveau 3)**
- Trois graphiques de trois familles différentes, chacun au service d'une intention nommée.
- Titres porteurs de message, axes avec unité, source, phrase de lecture.

**C4.5 — Tableur (niveau 3)**
- La jointure se fait sur `Code_EPCI`, jamais sur le nom, et elle est vérifiée par le point de contrôle du mardi.
- Tout est calculé par formule ; la liste des territoires sort d'un `FILTER`, pas d'une recopie.
- Le classeur est lisible : onglets nommés, un tiers peut refaire le chemin.

**Transversal** : la restitution tient en 3 minutes et se termine par la phrase demandée ; les sources
et la licence sont citées.

## Ressources

- [Cours 06 — Joindre deux tableaux avec XLOOKUP](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/06-joindre-deux-tableaux-xlookup.md)
- [Cours 02 — Dispersion et pièges de la moyenne](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/02-dispersion-et-pieges-de-la-moyenne.md) · [Cours 04 — Choisir le bon graphique](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/04-choisir-le-bon-graphique.md)
- INSEE — [définitions : taux de pauvreté, niveau de vie](https://www.insee.fr/fr/metadonnees/definitions)
- Aide Google Sheets — [XLOOKUP](https://support.google.com/docs/answer/12405947?hl=fr) · [FILTER](https://support.google.com/docs/answer/3093197?hl=fr) · [COUNTIFS](https://support.google.com/docs/answer/3256550?hl=fr) · [SUMIFS](https://support.google.com/docs/answer/3238496?hl=fr)

## Pour aller plus loin (facultatif)

- **Descendre à la commune** : refais l'analyse sur `INSEE_Communes` pour les 520 communes où le
  taux de pauvreté est publié. Qu'est-ce que tu gagnes en finesse, qu'est-ce que tu perds ?
- **Ajouter l'immobilier** : le prix médian au m² par intercommunalité, à partir de l'onglet
  `Marche_immobilier_2024` du socle (joint par `Code_INSEE` puis agrégé par `Code_EPCI`).
- **Tester ta règle** : refais ta décision avec une autre règle. Combien de territoires sont dans
  les deux listes ?
- **Ajouter une source** trouvée par toi (emploi, équipements, santé…) sur
  [data.gouv.fr](https://www.data.gouv.fr/) ou [insee.fr](https://www.insee.fr/), jointe par le code.
