# 04 — Choisir et construire un graphique dans Google Sheets

> 🎬 **Fin du fil rouge.** Nadia présente tes chiffres au comité de direction vendredi. Sa diapositive
> actuelle : un camembert en 3D à douze parts, titré « Répartition ». Personne ne saura dire si Lille
> fait mieux que Roubaix. Aujourd'hui, tu apprends à choisir le graphique qui répond à **une** question,
> puis à le construire proprement dans Sheets.

| | |
|---|---|
| **Jour** | Jeudi · matin |
| **Durée démo** | 45 min |
| **Données** | [`donnees/cyclonord_ventes_2025_fiable.xlsx`](donnees/cyclonord_ventes_2025_fiable.xlsx) |
| **Mise en pratique** | Jeudi matin : [exercice guidé, partie D](05-exercice-guide-cyclonord.md) (rendu 12 h 30) · jeudi après-midi : lancement du [brief B02-A](../../99-Brief/Data-Analyst-WSC/B02-A-adapter-prix-carburants.md), dépôt **lundi 16 h 30** |

---

## Ce que tu sauras faire

- Partir d'une **intention** (comparer, évoluer, distribuer, relier, décomposer) pour choisir le graphique.
- Repérer et refuser les **quatre mensonges graphiques** les plus courants.
- Livrer un **graphique fini** : titre qui dit le message, axes nommés avec unité, source.
- Choisir des **couleurs lisibles** par tout le monde.
- Utiliser l'**éditeur de graphique** de Sheets (onglets *Configurer* et *Personnaliser*).

---

## 1. Une intention → un graphique

On ne choisit pas un graphique parce qu'il est joli. On le choisit parce qu'il montre **une** chose
précise. Écris ta question **avant** d'ouvrir *Insertion › Graphique*.

| Mon intention | Graphique Sheets | Exemple Cyclo'Nord |
|---|---|---|
| **Comparer** des catégories | **barres triées** (de la plus grande à la plus petite) | CA livré par magasin |
| **Suivre une évolution** dans le temps | **courbe** | CA livré mois par mois |
| **Voir la distribution** (comment se répartissent les valeurs) | **histogramme** | les montants de commande |
| **Relier** deux nombres | **nuage de points** | montant et note client |
| **Décomposer** un tout en parts | **barres empilées à 100 %** ; camembert seulement si 2 ou 3 parts | part de chaque canal, par magasin |

Un **histogramme** n'est pas un graphique en barres. Les barres comparent des **catégories** (Lille,
Arras…). L'histogramme découpe un **nombre** en tranches (0-250 €, 250-500 €…) et compte combien de
lignes tombent dans chaque tranche : on y lit une **forme**.

**Et pour comparer plusieurs distributions ?** Sheets n'a pas de boîte à moustaches. Fais deux ou
trois histogrammes côte à côte **avec les mêmes tranches**, ou plus simple, un tableau des quartiles
(`QUARTILE`, vu mardi). Exemple : les montants par canal.

| Canal | Q1 | Médiane | Q3 |
|---|---|---|---|
| Magasin | 33,25 € | 89,00 € | 1 483,50 € |
| Site web | 69,50 € | 664,05 € | 1 795,50 € |
| Click & Collect | 81,38 € | 611,62 € | 2 052,75 € |

Lecture : la commande « du milieu » en magasin est bien plus petite qu'en ligne.

---

## 2. Les quatre mensonges à éviter

1. **L'axe tronqué sur des barres.** Si l'axe vertical démarre à 25 000 € au lieu de 0, un écart de
   10 % devient une falaise. La longueur d'une barre *est* la valeur : l'axe part de **zéro**.
   Dans Sheets : *Personnaliser › Axe vertical › Min.* = 0.
2. **La 3D.** Elle n'apporte aucune information et déforme les tailles. Jamais.
3. **Le camembert à 8 parts.** L'œil compare mal les angles. Au-delà de 3 parts : barres triées.
   Exemple : la part du CA commandé par catégorie. En camembert, Accessoires (1,5 %) et Atelier (0,8 %)
   deviennent deux filets invisibles. En barres triées, tout se lit : VAE 65,3 %, Vélo urbain 17,1 %,
   VTT 15,3 %, Accessoires 1,5 %, Atelier 0,8 %.
4. **Le double axe.** Deux échelles verticales dans un même graphique : en réglant chaque axe, on fait
   se croiser les courbes où l'on veut. Fais plutôt deux graphiques l'un sous l'autre.

---

## 3. Un graphique fini

Avant de livrer, vérifie trois choses.

- **Un titre qui dit le message**, pas le contenu.
  ❌ « CA par magasin »
  ✅ « Lens et Dunkerque font 32 % du CA livré »
- **Des axes nommés avec leur unité** : « CA livré (€) », « Nombre de commandes ».
- **La source et le périmètre**, en sous-titre : « Cyclo'Nord, commandes 2025, 360 commandes livrées ».

Et un bon réflexe : **supprime tout ce qui ne porte pas d'information** (quadrillage lourd, ombre,
fond coloré, légende inutile quand il n'y a qu'une série).

---

## 4. Des couleurs lisibles

Environ 8 % des hommes sont daltoniens, le plus souvent sur le couple rouge / vert. Un vidéoprojecteur
délavé ou une impression noir et blanc posent le même problème.

- Ne code **jamais** une information par la couleur seule : ajoute une étiquette ou un libellé.
- Évite rouge / vert comme seule opposition : **bleu / orange** marche pour tout le monde.
- Mets **une** série en couleur et les autres en gris : l'œil va où tu veux.
- Test rapide : imprime en noir et blanc. Si ça reste lisible, c'est bon.

---

## 5. La démo : l'éditeur de graphique de Sheets

**Exemple : CA livré par magasin, en barres triées.**

1. Pars d'un **TCD** (cours 03) : Lignes = `Magasin`, Valeurs = `Montant_TTC` résumé par SUM,
   Filtre = `Statut` = *Livrée*. Trie le TCD par la somme, ordre **décroissant** (le graphique suit
   l'ordre du tableau).
2. Clique dans le TCD, puis *Insertion › Graphique*. Le panneau **Éditeur de graphique** s'ouvre à droite.
3. Onglet **Configurer** (le *quoi*) :
   - **Type de graphique** : *Graphique à barres* (barres horizontales, pratiques pour les libellés).
   - **Plage de données** : vérifie qu'elle ne contient pas la ligne *Total général*, sinon elle
     écrase toutes les autres barres.
   - **Axe X / Série** : Sheets les devine ; corrige-les si besoin.
4. Onglet **Personnaliser** (le *comment*) :
   - *Titres du graphique et des axes* : titre = le message, sous-titre = la source, titres des axes avec unité.
   - *Séries* : couleur, et **Étiquettes de données** pour afficher les valeurs.
   - *Légende* : **Aucune** (une seule série).
   - *Axe horizontal* : minimum à 0.

**Résultat attendu** (CA livré, total 343 877,45 €) :

| Magasin | CA livré | Part |
|---|---|---|
| Lens | 56 878,50 € | 16,5 % |
| Dunkerque | 53 362,40 € | 15,5 % |
| Amiens | 47 930,05 € | 13,9 % |
| Lille | 47 768,75 € | 13,9 % |
| Beauvais | 42 822,10 € | 12,5 % |
| Valenciennes | 36 357,35 € | 10,6 % |
| Roubaix | 29 543,50 € | 8,6 % |
| Arras | 29 214,80 € | 8,5 % |

**Variante : l'histogramme des montants.** Sélectionne la colonne `Montant_TTC`, *Insertion ›
Graphique*, type *Histogramme*. Premier réflexe : le graphique est inutilisable, une seule barre
géante. La faute à la commande de 379 050 € : elle étire l'axe. Dans *Personnaliser › Histogramme*,
règle la **taille des segments** (la largeur des tranches : essaie 250). Et pour que la commande de
379 050 € n'écrase plus tout, fais l'histogramme sur `=FILTER(Montant; Montant<=5000)` (cours 02). Change la taille des tranches deux ou trois fois : la
lecture change avec elle.

Ce que tu dois voir : **331 commandes sur 613 font moins de 500 €**, puis les montants s'étalent
jusqu'à 5 000 €, et 6 commandes seulement dépassent ce seuil. Une distribution étalée à droite, comme
annoncé lundi.

---

## 6. Exercice express (20 min, en binôme)

Pour chaque question de Nadia : quel graphique, quoi en X et en Y, quel titre ?

| # | Question de la responsable commerciale |
|---|---|
| 1 | « Quel magasin réalise le plus gros chiffre d'affaires livré ? » |
| 2 | « Comment nos ventes livrées évoluent-elles dans l'année ? » |
| 3 | « Nos commandes sont-elles plutôt petites ou plutôt grosses ? » |
| 4 | « Les clients qui commandent cher mettent-ils de meilleures notes ? » |
| 5 | « Quelle part du CA chaque catégorie représente-t-elle ? » |

<details>
<summary>Réponses attendues</summary>

1. **Barres horizontales triées**, X = CA livré (€), Y = magasin. Titre : « Lens et Dunkerque font
   32 % du CA livré » (16,5 % + 15,5 %). C'est le graphique de la démo.
2. **Courbe**, X = mois, Y = CA livré (€), à partir d'un TCD groupé par mois (cours 03). Le CA livré
   va de 17 145,30 € (mai) à 37 249,55 € (novembre). Titre possible : « Le CA livré varie du simple au double
   selon les mois, creux en mai, pic en novembre ».
3. **Histogramme** de `Montant_TTC`, tranches de 250 €. Réponse : surtout petites (331 commandes sur
   613 sous 500 €), avec quelques très grosses qui tirent la moyenne vers le haut.
4. **Nuage de points**, X = `Montant_TTC` (€), Y = `Note_client`. Attention : la note n'a que
   5 valeurs, les points se superposent. Complète avec la note moyenne par tranche de montant : entre
   4,00 et 4,26 selon la tranche. Réponse honnête : on ne voit **pas de relation**.
5. **Barres triées**, pas un camembert (5 parts, dont deux sous 2 %). Titre : « Le VAE pèse 65 % du CA
   commandé pour 16 % des commandes » (65,3 % du CA, 97 commandes sur 613).

</details>

---

## Mémo

| Geste | Où dans Sheets |
|---|---|
| Créer un graphique | *Insertion › Graphique* |
| Changer de type, de plage, de séries | Éditeur › **Configurer** |
| Titre, sous-titre (source), titres des axes | Éditeur › **Personnaliser › Titres du graphique et des axes** |
| Couleurs, étiquettes de données | Éditeur › **Personnaliser › Séries** |
| Axe qui part de zéro | Éditeur › **Personnaliser › Axe vertical** (ou horizontal) › Min. |
| Tranches d'un histogramme | Éditeur › **Personnaliser › Histogramme** |

---

## Auto-évaluation

- [ ] J'écris ma question avant de choisir le graphique.
- [ ] Je sais dire pourquoi un histogramme n'est pas un graphique en barres.
- [ ] Je refuse l'axe tronqué sur des barres, la 3D, le camembert à plus de 3 parts et le double axe.
- [ ] Mes graphiques ont un titre-message, des axes avec unité et une source.
- [ ] Je sais passer de *Configurer* à *Personnaliser* pour finir un graphique.

---

⬅️ Cours précédent : [03 — Tableaux croisés dynamiques](03-tableaux-croises-dynamiques.md)
➡️ Mise en pratique : [brief B02-A — Adapter (prix des carburants)](../../99-Brief/Data-Analyst-WSC/B02-A-adapter-prix-carburants.md)
⬆️ [Retour au sommaire du module](README.md)
