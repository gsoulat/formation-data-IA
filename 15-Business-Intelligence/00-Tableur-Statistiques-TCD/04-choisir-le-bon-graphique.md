# 04 — Choisir le bon graphique

> 🎬 **Fin du fil rouge.**
> Nadia présente tes chiffres au comité de direction vendredi. Elle t'envoie sa diapositive : un
> **camembert en 3D à douze parts** intitulé « Répartition ». Personne autour de la table ne saura
> dire si Lille fait mieux que Roubaix.
> Ton travail aujourd'hui : savoir **quel graphique répond à quelle question**, et pourquoi celui-là
> ne répond à aucune.

| | |
|---|---|
| **Jour** | Jeudi 24/09/2026 · matin (apport) + après-midi (production brief Adapter) |
| **Durée** | ≈ 7 h |
| **Compétences** | **C4.2** (niveau 1 → 2) |
| **Données** | [`donnees/cyclonord_ventes_2025_fiable.xlsx`](donnees/cyclonord_ventes_2025_fiable.xlsx) |
| **Pré-requis** | Cours [01](01-statistiques-descriptives.md), [02](02-dispersion-et-pieges-de-la-moyenne.md), [03](03-tableaux-croises-dynamiques.md) |

---

## Objectifs pédagogiques

À la fin de la journée, tu sauras :

1. Partir de l'**intention** (comparer, répartir, distribuer, relier, évoluer) pour choisir la forme.
2. Distinguer un **histogramme** d'un diagramme en barres — et savoir que ce n'est pas un détail.
3. Construire au tableur : histogramme, boîte à moustaches, nuage de points, courbe, barres.
4. Repérer et refuser les **cinq mensonges graphiques** les plus courants.
5. Écrire un **titre qui dit le message**, pas le contenu.
6. Rendre un graphique lisible par une personne **daltonienne** ou en noir et blanc.

---

## 1. La seule question qui compte : quelle est mon intention ?

On ne choisit pas un graphique parce qu'il est joli. On le choisit parce qu'il rend visible une
**relation précise** entre des données.

| Mon intention | Graphique | Exemple Cyclo'Nord |
|---|---|---|
| **Comparer** des catégories entre elles | **barres** (horizontales si les libellés sont longs) | CA livré par magasin |
| **Décomposer** un tout en parties | barres **empilées** ou barres 100 % | part de chaque canal, magasin par magasin |
| **Montrer la distribution** d'une variable | **histogramme** | comment se répartissent les montants |
| **Comparer des distributions** | **boîtes à moustaches** côte à côte | dispersion des montants par catégorie |
| **Relier deux variables quantitatives** | **nuage de points** | surface vs prix, quantité vs montant |
| **Suivre une évolution** dans le temps | **courbe** | CA livré mois par mois |
| **Situer sur un territoire** | **carte** (vu en P27) | CA par département |

> 🧭 **La règle d'or** : formule ta question **avant** d'ouvrir le menu Insertion.
> « Est-ce que le VAE se vend mieux en ligne qu'en magasin ? » est une question de **comparaison** →
> barres. « Est-ce que nos prix sont homogènes ? » est une question de **distribution** → histogramme.
> Si tu n'arrives pas à écrire ta question, aucun graphique ne te sauvera.

---

## 2. Histogramme ≠ diagramme en barres

C'est la confusion la plus répandue, et elle change tout.

| | **Diagramme en barres** | **Histogramme** |
|---|---|---|
| Variable en abscisse | **qualitative** (Lille, Arras…) | **quantitative découpée en tranches** (0-50 €, 50-100 €…) |
| Ordre des barres | libre — on trie par valeur | **imposé** — l'axe est numérique |
| Espace entre les barres | oui | **non** (les tranches se touchent) |
| Ce qu'on lit | une comparaison | une **forme** |

**Construire un histogramme dans Excel :** sélectionne la colonne → *Insertion › Graphiques
statistiques › Histogramme* → clic droit sur l'axe horizontal › *Mettre en forme l'axe* → fixe la
**largeur d'intervalle** (le nombre de tranches change complètement la lecture — essaie-en trois).

Alternative parfaitement valable : construire soi-même la table des effectifs avec `FREQUENCE`
(`FREQUENCY`) ou un **TCD avec regroupement par tranches** (vu hier), puis insérer un graphique en
barres sans espacement.

**Ce que raconte l'histogramme des montants Cyclo'Nord :**

| Tranche | Nb commandes |
|---|---|
| 0 – 50 € | 151 |
| 50 – 100 € | 108 |
| 100 – 250 € | 60 |
| 250 – 500 € | 12 |
| 500 – 1 000 € | 79 |
| 1 000 – 2 000 € | 83 |
| 2 000 – 3 000 € | 64 |
| 3 000 – 5 000 € | 50 |
| > 5 000 € | 6 |

La forme n'est pas une cloche : elle a **deux bosses** (autour de 50 € et autour de 1 500 €), avec
un creux net entre 250 et 500 €. On appelle ça une distribution **bimodale**, et elle a un sens
métier immédiat : Cyclo'Nord a en réalité **deux activités** — l'atelier et les accessoires d'un
côté, la vente de vélos de l'autre. Les résumer par une seule moyenne n'avait aucun sens.

> 💡 **Voilà pourquoi on fait un histogramme avant de commenter une moyenne.** Une distribution
> bimodale invalide à elle seule la phrase « la commande moyenne est de 1 680 € ».

---

## 3. La boîte à moustaches : comparer des distributions

Un histogramme montre **une** distribution en détail. Une série de boîtes à moustaches en compare
**plusieurs** d'un coup d'œil.

*Insertion › Graphiques statistiques › Boîte à moustaches.* Mets `Categorie` en abscisse et
`Montant_TTC` en valeurs : cinq boîtes apparaissent côte à côte.

**Ce qu'on y lit sur Cyclo'Nord** — les boîtes Accessoires et Atelier sont écrasées près de zéro,
celle du VTT est franchement plus haute et compacte, celle du VAE est haute **et** longue avec des
points très au-dessus. Trois régimes de prix différents, une seule image.

> 🎯 Une boîte à moustaches est le graphique le plus dense en information par centimètre carré :
> médiane, dispersion, asymétrie, valeurs atypiques. C'est aussi celui qu'il faut **apprendre à
> lire** à son public : prévois toujours une phrase de légende.

---

## 4. Le nuage de points : relier deux variables

Un point par observation, une variable en X, une en Y. C'est le graphique de la **relation**.

*Insertion › Nuage de points (XY)* — **jamais** « Courbe », qui relierait les points dans l'ordre du
tableau et produirait un plat de spaghettis.

**Ce qu'on y cherche :**

| Ce que tu vois | Ce que ça veut dire |
|---|---|
| Nuage orienté vers le haut | relation positive |
| Nuage orienté vers le bas | relation négative |
| Nuage rond, sans direction | pas de relation linéaire |
| Nuage en entonnoir | la dispersion augmente avec la valeur |
| Points isolés loin du nuage | valeurs atypiques — à examiner |
| Deux paquets distincts | deux **populations** mélangées |

On peut ajouter une **courbe de tendance** (clic droit sur les points › *Ajouter une courbe de
tendance* › cocher *Afficher l'équation* et *Afficher le coefficient R²*). Le R² sera étudié en
détail la semaine prochaine ; retiens seulement qu'il mesure la part de variation expliquée.

> 🚩 **Corrélation n'est pas causalité.** Deux variables qui montent ensemble peuvent dépendre d'une
> troisième (la saison, la taille de la ville, l'inflation), ou se rencontrer par hasard. Un nuage de
> points **montre** une association ; il ne **démontre** rien. Écris « on observe que », jamais
> « donc X cause Y ».

---

## 5. Les cinq mensonges graphiques

### 5.1 L'axe tronqué

Un axe des ordonnées qui démarre à 60 % au lieu de 0 % transforme un écart de 2 points en falaise.

- **Barres** : l'axe **doit** partir de zéro. La longueur de la barre *est* la valeur.
- **Courbes** : on peut cadrer sur la plage utile — mais on le **signale** et on ne l'utilise pas
  pour dramatiser.

### 5.2 La 3D

Elle ne transporte aucune information et fausse la perception des volumes. **Aucune exception.**

### 5.3 Le camembert à douze parts

L'œil humain compare mal des angles. Un camembert reste acceptable à **2 ou 3 parts**, pour dire
« la moitié / un tiers ». Au-delà : barres triées.

Sur Cyclo'Nord, « Répartition du CA par catégorie » en camembert donne Accessoires 1,5 %, Atelier
0,8 % — deux filets invisibles. En barres triées, on lit instantanément : VAE 65,3 %, Vélo urbain
17,1 %, VTT 15,3 %, Accessoires 1,5 %, Atelier 0,8 %.

### 5.4 Le double axe vertical

Deux échelles différentes dans un même graphique : en décalant les axes, on peut faire raconter à peu
près n'importe quoi. Préfère deux graphiques empilés partageant le même axe des temps.

### 5.5 Le titre qui ne dit rien

« Répartition », « Analyse », « Graphique 1 » : ces titres font porter tout le travail
d'interprétation au lecteur.

> ✍️ **Écris ton titre comme une phrase de conclusion.**
> ❌ « CA par magasin »
> ✅ « Lens et Dunkerque réalisent 40 % du CA livré, Arras en réalise 8,5 % »

---

## 6. L'anatomie d'un graphique fini

Avant de livrer, vérifie les huit points suivants :

- [ ] **Titre** = le message, en une phrase
- [ ] **Axes nommés**, avec l'**unité** (€, %, nombre de commandes)
- [ ] **Source et périmètre** en note de bas de graphique (« DVF 2024, 613 commandes livrées »)
- [ ] **Ordre** volontaire (trié par valeur si l'axe est qualitatif)
- [ ] **Étiquettes de données** si elles sont peu nombreuses — sinon une grille discrète
- [ ] Pas de fioriture : ni 3D, ni dégradé, ni ombre, ni arrière-plan coloré
- [ ] **Légende** utile, ou mieux : les libellés directement à côté des séries
- [ ] Une **phrase de lecture** sous le graphique (« ce qu'il faut voir : … »)

> 🧹 **La règle du rapport données / encre** : chaque élément visuel qui ne porte pas d'information
> doit disparaître. Quadrillages lourds, bordures, effets : supprime.

---

## 7. Couleur et accessibilité

Environ **8 % des hommes** sont daltoniens, très majoritairement sur l'axe rouge / vert. Une
diapositive projetée, une impression noir et blanc, un vidéoprojecteur délavé ajoutent leurs propres
contraintes.

| Principe | Mise en œuvre |
|---|---|
| Ne jamais coder une information **uniquement** par la couleur | ajoute un motif, un libellé, une épaisseur, une icône |
| Éviter le couple rouge / vert comme seule opposition | bleu / orange se distingue dans tous les cas |
| Une couleur = une signification, sur tout le document | ne recycle pas le même bleu pour deux séries différentes |
| Mettre en avant **une** série, griser les autres | l'œil va là où tu veux |
| Contraste suffisant texte / fond | vise un ratio d'au moins 4,5:1 |

Test rapide : imprime ton graphique en noir et blanc. S'il reste lisible, il est accessible.

> 📎 La compétence **C4.7 — prendre en compte les handicaps visuels** sera travaillée à fond en P28.
> Les réflexes se prennent maintenant.

---

## 8. Exercice express (30 min, en groupe)

Pour chacune des questions de Nadia, indique le graphique, ce que tu mets en X et en Y, et le titre
que tu écrirais. Défends ton choix à l'oral.

| # | Question de la responsable commerciale |
|---|---|
| 1 | « Quel magasin réalise le plus gros chiffre d'affaires livré ? » |
| 2 | « Comment nos ventes se répartissent-elles dans l'année ? » |
| 3 | « Est-ce que nos commandes sont plutôt petites ou plutôt grosses ? » |
| 4 | « Le panier est-il plus dispersé sur le site web qu'en magasin ? » |
| 5 | « Les clients qui commandent cher mettent-ils de meilleures notes ? » |
| 6 | « Quelle part du CA chaque catégorie représente-t-elle ? » |
| 7 | « Le taux d'annulation est-il le même partout ? » |

<details>
<summary>Réponses attendues</summary>

1. **Barres horizontales triées**, X = CA livré (€), Y = magasin. Titre : « Lens et Dunkerque
   réalisent à eux deux 32 % du CA livré ».
2. **Courbe**, X = mois, Y = CA livré (€). Une courbe parce que le temps est continu et ordonné.
3. **Histogramme** de `Montant_TTC`. La réponse est « les deux » — la distribution est bimodale,
   et c'est justement l'information.
4. **Boîtes à moustaches** par canal (une boîte par canal). On compare des dispersions, pas des
   totaux.
5. **Nuage de points**, X = `Montant_TTC`, Y = `Note_client`. Attention : `Note_client` n'a que
   5 valeurs, les points se superposent — on le dit, et on complète par une moyenne de note par
   tranche de montant.
6. **Barres triées** (pas un camembert : 5 parts dont deux sous 2 %). Titre : « Le VAE pèse 65 % du
   chiffre d'affaires pour 16 % des commandes ».
7. **Barres empilées 100 %** par magasin, ou barres simples du seul taux « annulée + retournée »,
   triées. Le second est plus lisible si c'est le seul message.

</details>

---

## 9. À toi de jouer

➡️ **Production du [brief B02-A — Adapter](../../99-Brief/Data-Analyst-WSC/B02-A-adapter-prix-carburants.md)**, revue croisée à 16 h, dépôt à 17 h 30.
➡️ **Demain (FOAD) : [brief B02-T — Transposer](../../99-Brief/Data-Analyst-WSC/B02-T-transposer-portrait-territoire.md)**.

---

## 10. Auto-évaluation

- [ ] Je formule ma question avant de choisir un graphique.
- [ ] Je sais expliquer la différence entre histogramme et diagramme en barres.
- [ ] Je sais construire les cinq formes au tableur : barres, courbe, histogramme, boîte à
      moustaches, nuage de points.
- [ ] Je sais lire une distribution bimodale et en tirer une conséquence métier.
- [ ] Je n'utilise jamais la 3D, ni un camembert au-delà de trois parts.
- [ ] Je fais partir un axe de barres de zéro.
- [ ] Mes titres énoncent un message, pas un contenu.
- [ ] Mes graphiques restent lisibles en noir et blanc.
- [ ] J'écris « on observe une association », pas « X cause Y ».

---

## 11. Pour aller plus loin

- [Étude data viz — Nord de la France](../02-Panorama-Outils-BI/etude-dataviz-nord-france.md) *(dans ce dépôt)*
- Microsoft — [types de graphiques disponibles dans Office](https://support.microsoft.com/fr-fr/office/types-de-graphiques-disponibles-dans-office-a6187218-807e-4103-9e0a-27cdb19afb90)
- Microsoft — [créer un histogramme](https://support.microsoft.com/fr-fr/office/cr%C3%A9er-un-histogramme-85680173-064b-4024-b39d-80f17ff2f4e8)
- Financial Times — [Visual Vocabulary](https://github.com/Financial-Times/chart-doctor/tree/main/visual-vocabulary) *(la meilleure antisèche « quelle intention → quel graphique »)*
- [Datawrapper Blog — what to consider when choosing colors](https://blog.datawrapper.de/colors/)

⬅️ **Retour au [sommaire du module](README.md)**
