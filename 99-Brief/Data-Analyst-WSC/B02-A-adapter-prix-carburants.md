# Brief B02-A — Le carburant est-il vraiment plus cher chez nous ?

## Informations

| | |
|---|---|
| **Semaine** | S2 · mercredi 23 – jeudi 24 sept 2026 · 2 jours · Guillaume |
| **Modalité · Évaluation** | Binôme · Formatif (revue croisée jeudi 16 h) |
| **Compétences visées** | C3.1 · C4.2 · C4.5 — **niveau 2 · ADAPTER** |
| **Cours support** | [Module 00 — Tableur : statistiques & TCD](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/README.md) |

> **Niveau 2 · ADAPTER** — tu transposes à un contexte nouveau les gestes vus en cours et pratiqués
> lundi et mardi sur Cyclo'Nord. Les ressources sont fournies, la méthode ne l'est plus : c'est toi
> qui décides quels indicateurs calculer et quels graphiques produire.

## Description

Un lecteur écrit à la rédaction : « Chez nous, dans le Nord, on paye le carburant plus cher
qu'ailleurs. » Le rédacteur en chef veut publier. Avant, il veut savoir si c'est vrai. Vous avez
31 277 relevés de prix réels et deux jours.

## Contexte

Vous êtes en stage au **pôle données de *L'Écho des Hauts-de-France***, un quotidien régional de
Lille. La rédaction reçoit régulièrement des courriers de lecteurs sur le prix des carburants. Le
dernier en date est assez argumenté pour intéresser le rédacteur en chef, Malik Ferhaoui, qui
envisage un article : *« Carburant : les Hauts-de-France paient-ils plus cher ? »*

Il vient vous voir avec une consigne claire et un avertissement.

La consigne : *« Le ministère publie tous les prix de toutes les stations de France, en temps réel.
Prenez ce fichier et dites-moi si le lecteur a raison. »*

L'avertissement : *« Si on publie un chiffre faux, on passe pour des imbéciles pendant six mois. Je
ne veux pas d'un titre avant d'avoir vu vos calculs. Et je ne veux pas non plus d'un article qui
dit "c'est compliqué" — trouvez-moi ce qui est **vrai** et ce qui est **intéressant**. »*

Vous allez découvrir deux choses. La première, c'est que la réponse à la question du lecteur est
probablement non — mais que ce « non » dépend de l'indicateur que vous choisissez, et qu'il faut
savoir le dire. La seconde, plus intéressante pour l'article, c'est que la question n'était
peut-être pas la bonne : l'écart de prix entre deux stations **d'une même ville** est plus grand que
l'écart entre la région la moins chère et la plus chère de France. Ce n'est pas *où l'on habite* qui
compte, c'est *où l'on fait le plein*.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C3.1** — Utiliser les statistiques descriptives afin de modéliser les données et en faire
  émerger des informations pertinentes *(niveau 2 — adapter)*
- **C4.2** — Utiliser les visualisations descriptives : histogrammes, boîtes à moustaches, nuages de
  points *(niveau 2 — adapter)*
- **C4.5** — Utiliser un tableur et des tableaux croisés dynamiques pour proposer des croisements de
  variables *(niveau 2 — adapter)*

Concrètement, vous passerez du « je reproduis les formules du cours » au « je choisis les
indicateurs qui répondent à **cette** question-là ».

## Modalités pédagogiques

**Organisation** : binôme. Un seul classeur, mais les deux membres doivent savoir expliquer
n'importe quelle cellule.

**Mercredi après-midi — cadrage (3 h).**
Le formateur joue Malik Ferhaoui. Vous disposez d'une heure pour lui revenir avec **la question
reformulée** : « le carburant est-il plus cher chez nous ? » n'est pas une question analysable en
l'état. Plus cher que quoi ? Quel carburant ? Mesuré comment — moyenne, médiane, prix le plus
fréquent ? Sur quelles stations ? Vous lui soumettez votre formulation ; il valide ou renvoie.

Une fois la question cadrée, vous explorez le fichier et construisez vos premiers TCD.

**Jeudi matin — apport (1 h 30) puis production.**
Apport « choisir le bon graphique », puis production libre.

**Jeudi 16 h — revue croisée (45 min).**
Chaque binôme présente **un seul graphique** à un autre binôme, sans le commenter. Le binôme qui
reçoit doit dire à voix haute ce qu'il comprend. Si ce n'est pas ce que vous vouliez dire, le
graphique est à refaire.

**Jeudi 17 h 30 — dépôt.**

### Ce que vous devez traiter (le « quoi », pas le « comment »)

1. **Situer les Hauts-de-France.** La région est-elle plus chère, moins chère, dans la moyenne ?
   Votre réponse doit tenir compte du fait que le classement peut changer selon l'indicateur retenu.
2. **Mesurer la dispersion.** Un prix régional « moyen » a-t-il un sens ? De combien les stations
   s'écartent-elles les unes des autres, dans la région et à l'intérieur d'une même ville ?
3. **Croiser.** Au moins deux croisements non triviaux, justifiés. Type de station, carburant,
   département, énergie : qu'est-ce qui explique le mieux les écarts de prix ?
4. **Traiter les valeurs atypiques.** Le fichier en contient de vraies. Repérez-les, dites d'où
   elles viennent, et décidez — en le justifiant — ce que vous en faites.
5. **Produire trois graphiques** de trois familles différentes, titrés, légendés, sourcés.
6. **Proposer un titre d'article** et un chapô de cinq lignes, défendables devant le rédacteur en chef.

**Questions guidantes.** Une moyenne calculée sur des stations donne-t-elle le prix payé par les
automobilistes, ou le prix affiché par les stations ? Est-ce la même chose ? Si deux régions ont la
même médiane mais des écarts-types très différents, laquelle est « la plus chère » ? Une station
d'autoroute doit-elle entrer dans le calcul du prix régional ? Le prix le plus fréquent est-il le
prix moyen — et si non, pourquoi les deux diffèrent-ils autant sur le gazole ?

## Modalités d'évaluation

Brief **formatif**. Revue croisée le jeudi, retour collectif du formateur le vendredi matin.

Ce qui est évalué ici n'est pas le nombre de calculs, mais **l'adéquation entre la question et
l'indicateur**. Un binôme qui produit huit TCD sans savoir lequel répond à la question du rédacteur
en chef n'a pas atteint le niveau 2. Un binôme qui en produit trois, choisis et défendus, l'a
atteint.

Un chiffre publié sans son périmètre sera compté comme faux, même s'il est juste.

## Données fournies (source exacte)

> Le journal *L'Écho des Hauts-de-France* est **fictif**. Les **données sont réelles** et publiques.

- **Fichier** : [`carburants_france_releve.xlsx`](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/donnees/carburants_france_releve.xlsx)
  — onglets `Releve_prix` (31 277 lignes), `Stations`, `Dictionnaire`, `Perimetre_et_source`
- **Jeu** : Prix des carburants en France — flux instantané (v2)
- **Producteur** : Ministère de l'Économie et des Finances
- **Page** : https://data.economie.gouv.fr/explore/dataset/prix-des-carburants-en-france-flux-instantane-v2/
- **Licence** : **Licence Ouverte 2.0 (Etalab)** — la source doit être citée dans votre rendu
- **Périmètre** : 9 800 stations, 6 carburants, extraction du 18/09/2026
- **Format** : format *long* — 1 ligne = 1 station × 1 carburant. Directement exploitable en TCD.

**Structure du fichier** : `ID_station`, `Region`, `Departement`, `Code_departement`,
`Code_postal`, `Ville`, `Adresse`, `Type_de_station` (Route / Autoroute), `Energie`, `Carburant`,
`Prix_au_litre`.

> ⚠️ **Trois limites à lire avant de commencer** (onglet `Perimetre_et_source`) : c'est une
> photographie et toutes les stations ne déclarent pas au même moment ; seules les stations
> déclarantes figurent ; le fichier ne contient **aucun volume vendu**, donc toute moyenne est une
> moyenne *par station*, pas *par litre consommé*. Ces limites doivent apparaître dans votre note.

## Livrables attendus

**Un dépôt GitHub public** par binôme, contenant :

1. **`README.md`** — le nom des deux auteurs, la source des données et sa date d'extraction, la
   question telle que vous l'avez reformulée avec Malik, et où trouver quoi dans le dépôt.
2. **`analyse_carburants.xlsx`**
   - onglet `Releve_prix` **intact**
   - un onglet `Cadrage` : votre question reformulée, votre périmètre, vos hypothèses
   - un onglet par axe d'analyse, TCD **actualisés**, formules apparentes
   - un onglet `Graphiques` avec les trois visualisations finies
3. **`note-redaction.md`** — **deux pages maximum**, adressées à Malik Ferhaoui :
   - le titre d'article proposé et son chapô (5 lignes)
   - la réponse à la question du lecteur, avec le chiffre, son indicateur et son périmètre
   - ce que vous avez trouvé de plus intéressant, qui n'était pas dans la question initiale
   - les trois limites du jeu de données, formulées pour un lecteur non technicien
   - la source et la date d'extraction
4. **`graphiques/`** — les trois graphiques exportés en image, nommés explicitement.

> 🔧 **Travail en binôme, un seul dépôt.** L'un des deux le crée, ajoute l'autre en collaborateur
> dans *Settings › Collaborators*. Les deux doivent apparaître dans l'historique des commits : un
> dépôt où une seule personne a poussé sera lu comme un travail fait par une seule personne.

## Critères de performance

**C3.1 — Statistiques descriptives (niveau 2)**
• La question de départ est **reformulée** en question analysable, avec périmètre explicite.
• Position **et** dispersion sont calculées ; le choix de l'indicateur de position est justifié par
la forme de la distribution, pas par habitude.
• Le classement des Hauts-de-France est donné **et** la sensibilité de ce classement à l'indicateur
retenu est discutée.
• Les valeurs atypiques sont identifiées, expliquées, et une décision est prise et assumée.
• Aucun chiffre n'est publié sans son périmètre.

**C4.2 — Visualisations descriptives (niveau 2)**
• Trois graphiques de trois familles différentes, adaptés à l'intention annoncée.
• Titre porteur de message, axes nommés avec unité, source et date en note.
• Aucun mensonge graphique (axe tronqué sur des barres, 3D, camembert à plus de trois parts).
• Chaque graphique a passé l'épreuve de la revue croisée.

**C4.5 — Tableur et TCD (niveau 2)**
• Au moins deux croisements **non triviaux** et justifiés.
• Les TCD sont construits sur un tableau structuré et sont actualisés au moment du rendu.
• Le classeur est navigable : onglets nommés, cellules de résultat identifiables, pas de valeur
saisie en dur.
• La limite « le TCD ne calcule pas de médiane » est contournée explicitement, et la méthode de
contournement est documentée.

**Transversal**
• La source et la licence sont citées.
• La note est lisible par un journaliste : aucun jargon non expliqué.

## Ressources

- [Cours 01 — Statistiques descriptives](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/01-statistiques-descriptives.md)
- [Cours 02 — Dispersion et pièges de la moyenne](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/02-dispersion-et-pieges-de-la-moyenne.md)
- [Cours 03 — Tableaux croisés dynamiques](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/03-tableaux-croises-dynamiques.md)
- [Cours 04 — Choisir le bon graphique](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/04-choisir-le-bon-graphique.md)
- Microsoft — [créer un tableau croisé dynamique](https://support.microsoft.com/fr-fr/office/cr%C3%A9er-un-tableau-crois%C3%A9-dynamique-pour-analyser-des-donn%C3%A9es-de-feuille-de-calcul-a9a84538-bfe9-40a9-a8e9-f99134456576)
- Microsoft — [fonctions statistiques Excel](https://support.microsoft.com/fr-fr/office/fonctions-statistiques-r%C3%A9f%C3%A9rence-624dac86-a375-4435-bc25-76d6df3c5b6f)
- data.economie.gouv.fr — [jeu de données source](https://data.economie.gouv.fr/explore/dataset/prix-des-carburants-en-france-flux-instantane-v2/)
- Etalab — [Licence Ouverte 2.0](https://www.etalab.gouv.fr/licence-ouverte-open-licence/)

## Pour aller plus loin (facultatif)

- Le prix du gazole a un **mode** très marqué à 2,25 €/L alors que sa médiane est nettement
  au-dessus. Formulez une hypothèse sur ce qui produit ce pic, et cherchez de quel type
  d'enseignes proviennent ces stations.
- Le fichier ne contient pas de volumes. Cherchez sur data.gouv.fr une source qui permettrait de
  pondérer par la consommation, et dites en trois lignes ce que cela changerait à votre conclusion.
- Comparez votre résultat au prix moyen national publié par le ministère la même semaine. Si vous
  trouvez un écart, expliquez-le.
