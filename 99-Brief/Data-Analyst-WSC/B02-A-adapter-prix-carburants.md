# Brief B02-A — Le carburant est-il vraiment plus cher chez nous ?

## Informations

| | |
|---|---|
| **Quand** | jeudi après-midi (lancement), vendredi, lundi · **dépôt lundi 16 h 30** |
| **Organisation** | individuel ; entraide encouragée, chacun son classeur |
| **Outil** | Google Sheets |
| **Compétences visées** | C3.1 · C4.2 · C4.5 — **niveau 2 · ADAPTER** |
| **Cours support** | [Module 00 — Tableur : statistiques & TCD](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/README.md) |

> **Niveau 2 · ADAPTER** — tu refais sur des données nouvelles les gestes pratiqués de lundi à
> mercredi sur Cyclo'Nord : médiane, dispersion, TCD, graphiques. Les étapes sont données ; les
> formules et les réglages, c'est à toi de les retrouver dans ton classeur Cyclo'Nord et dans les cours.

## Description

Un lecteur écrit au journal : « Chez nous, dans le Nord, on paye le gazole plus cher qu'ailleurs. »
Le rédacteur en chef veut savoir si c'est vrai avant de publier. Tu as les prix réels de toutes les
stations de France et deux jours et demi.

## Contexte

Tu es en stage au **pôle données de *L'Écho des Hauts-de-France***, un quotidien régional de Lille.
Le rédacteur en chef, Malik Ferhaoui, t'apporte la lettre du lecteur :

*« Le ministère publie les prix de toutes les stations de France. Prends ce fichier et dis-moi si le
lecteur a raison. Si on publie un chiffre faux, on passe pour des imbéciles. Mais je ne veux pas non
plus d'un article qui dit "c'est compliqué" : trouve-moi ce qui est **vrai** et ce qui est
**intéressant**. »*

Pour rester dans le temps, on s'intéresse à **un seul carburant, le gazole**, le plus vendu en France.

## Données fournies

> Le journal est **fictif**. Les **données sont réelles** et publiques.

- **Fichier** : [`carburants_france_releve.xlsx`](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/donnees/carburants_france_releve.xlsx)
  — onglet `Releve_prix` : **31 277 lignes**, une ligne = un carburant dans une station
- **Source** : Ministère de l'Économie et des Finances, *Prix des carburants en France — flux
  instantané (v2)*, https://data.economie.gouv.fr/explore/dataset/prix-des-carburants-en-france-flux-instantane-v2/
- **Licence** : Licence Ouverte 2.0 (Etalab) — la source doit être citée dans ton rendu
- **Périmètre** : France métropolitaine, prix relevés le **18/09/2026**
- **Colonnes utiles** : `Region`, `Departement`, `Ville`, `Type_de_station` (Route / Autoroute),
  `Carburant`, `Prix_au_litre`

> ⚠️ **Trois limites** (onglet `Perimetre_et_source`) : c'est une photo prise un jour donné ; seules
> les stations qui déclarent leurs prix y figurent ; et le fichier ne dit **pas combien de litres**
> chaque station vend. Un prix « médian » est donc celui **d'une station type**, pas le prix payé en
> moyenne par les automobilistes. Ces limites doivent apparaître dans ta note.

## Déroulé

**Jeudi 13 h 30 — lancement (30 min, tous ensemble).** Réunion avec Malik : ensemble, on
transforme la phrase du lecteur en question qu'on peut vérifier avec les données.

**Jeudi 14 h – 17 h, vendredi toute la journée, lundi 9 h – 14 h 30 — production.**

1. **Importer et préparer** (30 min). Nouveau classeur `NOM_Prenom_carburants`, paramètres
   régionaux France, import du fichier. Crée un onglet `Cadrage` et écris-y la question, en
   complétant : *« Le 18/09/2026, le prix du gazole affiché par une station type des Hauts-de-France
   est-il plus élevé que dans les autres régions de France métropolitaine ? »* Puis explique en
   deux lignes pourquoi on compare des **médianes** et pas des moyennes.
2. **Axe 1 — Les régions** (1 h 30). Un TCD : les régions en lignes, le prix du gazole en valeurs,
   résumé par **médiane** puis, dans une deuxième colonne, par **moyenne**. Trie par médiane.
   À quel rang arrivent les Hauts-de-France ? Le rang change-t-il entre médiane et moyenne ?
3. **Axe 2 — Route ou autoroute** (45 min). Un TCD : le type de station en lignes, la médiane du
   prix du gazole en valeurs, pour toute la France. Quel écart ?
4. **Axe 3 — Dans une même ville** (1 h 30). Un TCD sur le gazole des **Hauts-de-France**
   seulement (filtres sur la région et le carburant) : les villes en lignes, le prix résumé par
   **MIN**, puis par **MAX**. Dans ce TCD, retrouve **Lille, Amiens, Calais, Arras et Dunkerque**.
   À côté du TCD, construis un petit tableau de ces cinq villes avec leur prix minimum, maximum, et
   l'écart (maximum − minimum, en centimes). Pas de recopie à la main : tape `=` puis clique sur la
   case du TCD qui contient le prix. Compare le plus gros de ces écarts à l'écart entre la
   médiane de la région la moins chère et celle de la plus chère (axe 1).
5. **Les valeurs anormales** (30 min). Filtre le carburant **E85** et trie les prix de Z à A :
   quelques prix sont plus du double des autres. Erreur de saisie probable ? Écris ta décision.
6. **Deux graphiques** (1 h 30), à partir de tes TCD :
   - des **barres triées** : la médiane du gazole par région, axe qui part de **0** ;
   - un **histogramme** des prix du gazole (toute la France).
   Chacun a un titre qui dit le message, des axes avec l'unité (€/L) et la source.

**Lundi 14 h 30 – 15 h 15 — revue croisée.** Par deux : tu montres **un** graphique à ton
voisin **sans rien dire**. Il dit à voix haute ce qu'il comprend. Si ce n'est pas ton message, tu
corriges le titre ou le graphique.

**Lundi 15 h 15 – 16 h 30 — finitions et dépôt.** Retour collectif de 16 h 30 à 17 h.

**Questions pour avancer.** Plus cher que quoi : que la moyenne nationale, ou que les autres
régions ? Si deux régions ont la même médiane, laquelle est la plus chère ? Une station
d'autoroute doit-elle compter dans le prix d'une région ? Qu'est-ce qui fait le plus varier le prix :
la région, le type de station, ou la station elle-même ?

## Livrables (lundi 16 h 30)

1. **Le classeur Google Sheets**, partagé en **Lecteur** par lien, avec les onglets `Cadrage`, un
   onglet par axe (TCD visibles), et `Graphiques`. L'onglet `Releve_prix` n'est pas modifié.
2. Sur ton dépôt GitHub, le dossier **`P2-carburants/`** avec :
   - `README.md` : **la note pour Malik**, une demi-page au plus :
     - un **titre d'article** et un **chapô** de 3 lignes ;
     - **la réponse**, avec le chiffre, l'indicateur et le périmètre (ex. « prix médian du gazole
       affiché par les stations, le 18/09/2026 ») ;
     - **ce qui est intéressant** et que le lecteur n'avait pas demandé ;
     - **deux limites** des données, dites simplement ;
     - la **source** et le **lien** vers ton classeur ;
   - `carburants.xlsx` : *Fichier › Télécharger › Microsoft Excel*.

## Critères de performance

**C3.1 — Statistiques descriptives (niveau 2)**
- La question est reformulée avec un carburant, un indicateur et un périmètre.
- Le choix de la médiane est justifié en une ou deux phrases.
- Le rang des Hauts-de-France est donné, et le changement éventuel de rang entre médiane et moyenne
  est signalé.
- Les prix anormaux de l'E85 sont repérés et une décision est écrite.
- Aucun chiffre de la note n'est donné sans son périmètre.

**C4.2 — Visualisations (niveau 2)**
- Les deux graphiques demandés sont présents : barres triées partant de 0, histogramme.
- Titres porteurs de message, axes avec unité, source indiquée.
- Le graphique montré en revue croisée a été compris par le voisin, ou corrigé.

**C4.5 — Tableur et TCD (niveau 2)**
- Les trois axes sont traités par TCD, et la médiane est obtenue dans le TCD.
- Le TCD des villes est filtré sur les Hauts-de-France et le gazole ; l'écart est calculé pour les cinq villes demandées.
- Le classeur est lisible : onglets nommés, pas de valeur recopiée à la main.

**Transversal** : la source et la licence sont citées ; le classeur est partagé et son lien est dans
le README.

## Ressources

- [Cours 02 — Dispersion](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/02-dispersion-et-pieges-de-la-moyenne.md)
- [Cours 03 — TCD dans Google Sheets](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/03-tableaux-croises-dynamiques.md)
- [Cours 04 — Choisir et construire un graphique](../../15-Business-Intelligence/00-Tableur-Statistiques-TCD/04-choisir-le-bon-graphique.md)
- Aide Google Sheets — créer et utiliser des tableaux croisés dynamiques : https://support.google.com/docs/answer/1272900?hl=fr
- Etalab — [Licence Ouverte 2.0](https://www.etalab.gouv.fr/licence-ouverte-open-licence/)

## Pour aller plus loin (facultatif)

- Fais la même analyse pour le **SP95-E10**. La conclusion change-t-elle ?
- Près d'une station sur cinq affiche le gazole à **exactement 2,25 €**. Comment le vois-tu sur ton
  histogramme ? Quelle hypothèse ferais-tu ?
