# Brief B02-T — Portrait statistique d'un territoire : quels territoires aider en priorité ?

## Informations

| | |
|---|---|
| **Quand** | 2ᵉ semaine, **mardi → vendredi** · dépôt **vendredi 12 h 30** · restitutions vendredi 13 h 30 – 16 h 30 |
| **Organisation** | individuel ; entraide encouragée, chacun son classeur |
| **Outil** | Google Sheets |
| **Compétences visées** | C3.1 · C4.2 · C4.5 — **niveau 3 · TRANSPOSER, accompagné** |
| **Cours support** | [Module 00](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/README.md), dont le [cours 06 — Joindre deux tableaux avec XLOOKUP](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/06-joindre-deux-tableaux-xlookup.md) (mardi matin) |

> **Niveau 3 · TRANSPOSER, accompagné.** Pour la première fois, **c'est toi qui décides** : la
> maille, les indicateurs de décision, la règle de choix, les territoires retenus. Le brief te donne
> les étapes et des points de contrôle chaque jour, mais pas les réponses : deux apprenants peuvent
> rendre deux portraits différents, et tous les deux justes, s'ils savent les défendre.

## Description

Une agence de développement économique doit concentrer son aide sur quelques territoires des
Hauts-de-France. Elle ne sait pas lesquels choisir. Tu as quatre jours, deux fichiers de données
réelles, et une question : **« Qui aider en priorité, et pourquoi ? »**

## Contexte

Le cabinet **Orion Études** travaille pour une agence de développement économique des
Hauts-de-France. L'agence dispose d'une enveloppe d'accompagnement (ingénierie, subventions, mise en
réseau) et doit la concentrer sur **un nombre limité de territoires**. Sa directrice, Claire
Vandamme, te demande un portrait statistique qui l'aide à choisir :

> « Je ne vais pas te dire quels indicateurs regarder. Ce que je dois pouvoir faire après t'avoir lu :
> **désigner des territoires prioritaires et justifier ce choix devant des élus qui vont contester**. »

Elle ajoute :

> « Le dernier cabinet nous a rendu une moyenne où une commune de 200 habitants pesait autant que
> Lille. Un élu l'a remarqué. Je ne veux plus de ça. »

## Données fournies

> Le cabinet et l'agence sont **fictifs**. Les **données sont réelles**.

| Fichier | Contenu | Source |
|---|---|---|
| [`portrait_territoire_hdf_socle.xlsx`](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/donnees/portrait_territoire_hdf_socle.xlsx) | 3 782 communes : population, superficie, densité, intercommunalité (EPCI) ; marché immobilier 2024 | API Géo et DVF (Etalab), Licence Ouverte |
| [`insee_revenus_population_hdf.xlsx`](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/donnees/insee_revenus_population_hdf.xlsx) | Par commune (`INSEE_Communes`) et par intercommunalité (`INSEE_EPCI`) : population 2017 et 2023, niveau de vie médian et taux de pauvreté 2023 | INSEE, Base du comparateur de territoires, Licence Ouverte |

Lis les onglets `Sources` et `INSEE_Source` : ils disent d'où viennent les chiffres et ce qui manque.

## Déroulé, jour par jour

### Mardi — comprendre, réunir les données

- **9 h – 9 h 30 · lancement.** Le formateur joue Claire Vandamme. Pose-lui tes questions : c'est le
  seul moment où tu peux cadrer la commande.
- **9 h 45 – 10 h 30 · démo** du [cours 06](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/06-joindre-deux-tableaux-xlookup.md) : joindre deux tableaux, moyenne pondérée.
- **Étape 1 — Réunir** (1 h). Un classeur `NOM_Prenom_territoire` ; importe le socle, puis le
  fichier INSEE en **nouvelles feuilles**.
- **Étape 2 — Choisir la maille** (30 min). Onglet `Methode` : choisis entre
  **A. les 92 intercommunalités** (tous les indicateurs sont publiés) et **B. les communes** (plus fin,
  mais le taux de pauvreté manque pour 3 262 communes sur 3 782). Écris ton choix et **pourquoi**, en trois lignes.
- **Étape 3 — Le tableau d'analyse** (2 h 30). Onglet `Analyse`, une ligne par territoire. Pour la
  maille A : `Code_EPCI`, `Nom_EPCI` (repris de `INSEE_EPCI`), puis avec des formules :
  - le **nombre de communes** et la **superficie** : `COUNTIFS` et `SUMIFS` sur `Communes_HDF`, avec
    `Code_EPCI` comme clé ;
  - la **population 2023**, le **niveau de vie médian** et le **taux de pauvreté** : `XLOOKUP` dans `INSEE_EPCI` ;
  - l'**évolution de la population** 2017 → 2023, en % ;
  - le **nombre de personnes pauvres** : taux × population ÷ 100 ;
  - la **densité** : population ÷ superficie.

✅ **Point de contrôle mardi soir (maille A)** : 92 lignes ; total du nombre de communes **3 782** ;
Métropole Européenne de Lille : 95 communes, 1 195 234 habitants, taux de pauvreté 21,4 %.

### Mercredi — décrire

- **Étape 4 — Position et dispersion** (2 h 30). Onglet `Indicateurs` : pour le **taux de
  pauvreté** et le **niveau de vie**, calcule minimum, Q1, médiane, Q3, maximum, et la moyenne
  **simple** puis **pondérée par la population**. Écris une phrase par indicateur.
- **Étape 5 — Ce qui manque** (1 h). Combien de communes sans taux de pauvreté publié ? Combien
  d'habitants y vivent ? Deux intercommunalités débordent sur la Normandie : lesquelles, et
  qu'est-ce que ça change ? *(Indice : compare la population du socle et celle de l'INSEE.)*
- **Étape 6 — Choisir tes critères** (1 h). Dans `Methode`, choisis **deux** indicateurs de décision
  parmi : taux de pauvreté, nombre de personnes pauvres, évolution de la population, niveau de vie
  médian. Explique en trois lignes pourquoi ces deux-là **pour cette question**.

✅ **Point de contrôle mercredi soir** : taux de pauvreté des 92 EPCI, moyenne simple **16,1 %**,
pondérée **19,1 %** (le taux régional publié par l'INSEE est 19 %) ; médiane **14,5 %**.

### Jeudi — décider, montrer

- **Étape 7 — La règle** (2 h). Écris ta règle, par exemple *« taux de pauvreté ≥ 19 % et
  population en baisse »* ou *« parmi les 15 premiers en taux ET en nombre de personnes pauvres »*.
  Applique-la avec `FILTER` (ou `RANK` puis `FILTER`) dans un onglet `Decision`.
  Ta liste doit compter **entre 5 et 12 territoires** ; si elle est plus longue ou plus courte,
  resserre ou desserre ta règle, et note ce que tu as changé.
- **Étape 8 — Trois graphiques** (2 h 30), de trois familles différentes, par exemple :
  - des **barres triées** : tes territoires retenus sur ton premier critère ;
  - un **histogramme** : la distribution du taux de pauvreté des 92 EPCI ;
  - un **nuage de points** : tes deux critères, un point par territoire.
  Chacun a un titre qui dit le message, des axes avec unité, la source, et une **phrase de lecture**.

✅ **Point de contrôle jeudi soir** : une liste de 5 à 12 territoires, trois graphiques titrés.

### Vendredi — convaincre

- **9 h – 12 h 30 · la note et la diapositive.**
- **12 h 30 · dépôt.**
- **13 h 30 – 16 h 30 · restitutions** : 5 minutes chacun (3 minutes de présentation, 2 minutes de
  question), avec **une seule diapositive**. Elles se terminent par la phrase : *« J'accompagnerais en
  priorité ______, parce que ______. »* Le formateur, dans le rôle de Claire, te posera toujours la
  même question : *« Un élu me dit que votre critère est injuste. Je lui réponds quoi ? »*
- **16 h 30 – 17 h · retour collectif.**

## Livrables (vendredi 12 h 30)

1. **Le classeur Google Sheets**, partagé en **Lecteur** par lien, avec les onglets `Methode`,
   `Analyse`, `Indicateurs`, `Decision`, `Graphiques`. Les onglets importés ne sont pas modifiés.
2. Sur ton dépôt GitHub, le dossier **`P2-territoire/`** avec :
   - `README.md` : **la note pour Claire**, une page au plus :
     - ta maille et tes deux critères, et pourquoi ;
     - la moyenne simple et la moyenne pondérée de ton premier critère, et ce que l'écart change ;
     - **la réponse** : les territoires retenus, et la règle qui les désigne ;
     - **deux limites** de ton analyse ;
     - les sources, avec leur date, et le **lien** vers ton classeur ;
   - `diapositive.pdf` : ta diapositive de restitution ;
   - `territoire.xlsx` : *Fichier › Télécharger › Microsoft Excel*.

## Critères de performance

**C3.1 — Statistiques descriptives (niveau 3)**
- La maille et les deux critères sont choisis et justifiés au regard de la question.
- Position **et** dispersion sont calculées pour les deux indicateurs décrits.
- Les moyennes simple et pondérée sont calculées, l'écart est chiffré et sa conséquence est dite.
- Les données manquantes sont comptées et expliquées (secret statistique, EPCI interrégionaux).
- La note se termine par une **décision** : une liste de territoires et la règle qui la produit.

**C4.2 — Visualisations (niveau 3)**
- Trois graphiques de trois familles différentes, chacun au service d'une intention nommée.
- Titres porteurs de message, axes avec unité, source, phrase de lecture.

**C4.5 — Tableur (niveau 3)**
- La jointure se fait sur le code (INSEE ou EPCI), jamais sur le nom, et elle est vérifiée par un compte.
- Tout est calculé par formule ; la liste des territoires sort d'un `FILTER`, pas d'une recopie.
- Le classeur est lisible : onglets nommés, un tiers peut refaire le chemin.

**Transversal** : la restitution tient en 3 minutes et se termine par la phrase demandée ; les sources
et la licence sont citées.

## Ressources

- [Cours 06 — Joindre deux tableaux avec XLOOKUP](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/06-joindre-deux-tableaux-xlookup.md)
- [Cours 02 — Dispersion](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/02-dispersion-et-pieges-de-la-moyenne.md) · [Cours 04 — Graphiques](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/04-choisir-le-bon-graphique.md)
- INSEE — [définitions : taux de pauvreté, niveau de vie](https://www.insee.fr/fr/metadonnees/definitions)
- Aide Google Sheets — [XLOOKUP](https://support.google.com/docs/answer/12405947?hl=fr) · [FILTER](https://support.google.com/docs/answer/3093197?hl=fr)

## Pour aller plus loin (facultatif)

- Ajoute une **source que tu as trouvée toi-même** (emploi, équipements, santé…) sur
  [data.gouv.fr](https://www.data.gouv.fr/) ou [insee.fr](https://www.insee.fr/), et joins-la par le code.
- Ajoute le prix médian de l'immobilier par intercommunalité (onglet `Marche_immobilier_2024` du socle).
- Refais ta décision avec une autre règle : combien de territoires restent dans les deux listes ?
