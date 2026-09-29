# 06 — Joindre deux tableaux avec XLOOKUP, et la moyenne pondérée

> 🎬 **Nouveau commanditaire.** Une agence de développement économique veut savoir où concentrer
> son aide. Tu as deux fichiers : les communes des Hauts-de-France (population, superficie,
> intercommunalité) d'un côté, les revenus et la pauvreté publiés par l'INSEE de l'autre. Aucun ne
> suffit seul. Aujourd'hui, tu apprends à les **réunir**.

| Jour | Durée démo | Mise en pratique |
|---|---|---|
| Mardi de la 2ᵉ semaine, matin | 45 min | [Brief B02-T — Portrait d'un territoire](../../99-Brief/Data-Analyst-WSC/B02-T-transposer-portrait-territoire.md) (mardi → vendredi) |

Données : [`donnees/portrait_territoire_hdf_socle.xlsx`](donnees/portrait_territoire_hdf_socle.xlsx)
et [`donnees/insee_revenus_population_hdf-v.xlsx`](donnees/insee_revenus_population_hdf-v.xlsx).

---

## Ce que tu sauras faire

- Réunir deux fichiers dans un même classeur Google Sheets.
- Aller chercher une valeur dans un autre tableau avec `XLOOKUP`, grâce à une **clé**.
- Vérifier qu'une jointure a marché.
- Calculer une moyenne **pondérée** par la population, et dire pourquoi elle change le résultat.

---

## 1. Deux fichiers, une clé

Le socle dit, pour chaque commune, sa population et son intercommunalité. Le fichier de l'INSEE
dit, pour chaque commune, son taux de pauvreté. Pour mettre les deux côte à côte, il faut une
colonne présente **dans les deux** et qui désigne **une seule** commune : c'est la **clé**.

| Clé possible | Bonne clé ? |
|---|---|
| Le nom de la commune | ❌ **54 noms** sont portés par plusieurs communes des Hauts-de-France : il y a quatre *Fleury* (Aisne, Oise, Pas-de-Calais, Somme) et trois *Dury*. |
| Le **code INSEE** (`02001`, `59350`…) | ✅ unique pour chaque commune de France, et présent dans les deux fichiers |

> ⚠️ Le code INSEE est un **texte** de 5 caractères, pas un nombre : `02001` n'est pas `2001`. Les
> deux fichiers fournis le stockent correctement. Si tu importes un autre fichier (un CSV de
> l'INSEE, par exemple), **décoche** la conversion automatique en nombres dans la fenêtre
> d'importation, sinon les communes de l'Aisne perdent leur zéro et ne se joignent plus.

---

## 2. Réunir les deux fichiers dans un classeur

1. Importe le socle : *Fichier › Importer* › **Remplacer la feuille de calcul**.
2. Importe le fichier INSEE : *Fichier › Importer* › cette fois **Insérer de nouvelles feuilles**.

Tu obtiens six onglets : `Communes_HDF`, `Marche_immobilier_2024`, `Dictionnaire`, `Sources` (le
socle) et `INSEE_Communes`, `INSEE_EPCI`, `INSEE_Source`. Lis `INSEE_Source` : il explique chaque
colonne et ses limites.

---

## 3. XLOOKUP : aller chercher une valeur ailleurs

`XLOOKUP` (RECHERCHEX) cherche une valeur dans une colonne, et renvoie ce qui se trouve **sur la
même ligne** dans une autre colonne.

```
XLOOKUP( ce que je cherche ; où je le cherche ; ce que je veux en retour ; si je ne trouve pas )
```

**Démo.** Crée un onglet `Jointure`.

1. En **A1:C1** : `Code_INSEE`, `Commune`, `Taux_pauvrete`.
2. En **A2** : `=Communes_HDF!A2` ; en **B2** : `=Communes_HDF!B2`.
3. En **C2** :

```
=XLOOKUP(A2; INSEE_Communes!$A$2:$A$3783; INSEE_Communes!$F$2:$F$3783; "code introuvable")
```

4. Sélectionne **A2:C2**, puis **double-clique** sur le petit carré bleu en bas à droite : Sheets
   recopie jusqu'à la dernière commune (ligne 3783).

✅ **Résultat attendu** : pour `02001` (Abbécourt), « non publié » ; pour `59350` (Lille), **28,6**.

| Morceau | Rôle |
|---|---|
| `A2` | la clé de la commune de cette ligne |
| `INSEE_Communes!$A$2:$A$3783` | la colonne des codes dans le fichier INSEE (avec des `$` pour qu'elle ne glisse pas quand on recopie) |
| `INSEE_Communes!$F$2:$F$3783` | la colonne à rapporter : le taux de pauvreté |
| `"code introuvable"` | ce qu'on affiche si le code n'existe pas dans le fichier INSEE (le signe d'une jointure ratée) |

---

## 4. Vérifier une jointure

Une jointure ne prévient jamais quand elle échoue. On vérifie toujours avec trois comptes :

```
=COUNTA(Jointure!A2:A3783)                         → 3 782 communes
=COUNTIF(Jointure!C2:C3783; "code introuvable")    → 0     (sinon, la jointure a raté)
=COUNTIF(Jointure!C2:C3783; "non publié")          → 3 262 sans taux publié
```

« non publié » est écrit **dans le fichier de l'INSEE** : 3 262 communes sur 3 782 n'ont pas de taux
de pauvreté. Ce n'est **pas** une erreur de jointure.
L'INSEE ne publie pas ce chiffre pour les petites communes (**secret statistique** : on pourrait
reconnaître les foyers). Les 520 communes publiées regroupent pourtant 72 % des habitants.

> 🧭 **Conséquence pour le brief** : à l'échelle de la commune, le taux de pauvreté manque pour
> 86 % des communes. À l'échelle de l'**intercommunalité** (onglet `INSEE_EPCI`), il est publié pour
> les 92. C'est pour ça que le brief B02-T travaille sur les 92 intercommunalités : l'échelle
> choisie décide de ce qu'on peut mesurer. Le même `XLOOKUP` s'écrit alors avec `Code_EPCI` comme
> clé et `INSEE_EPCI` comme table où chercher.

---

## 5. La moyenne pondérée

Dans `INSEE_EPCI`, les 92 intercommunalités ont chacune un taux de pauvreté. Quel est le taux
« des Hauts-de-France » ?

```
=AVERAGE(INSEE_EPCI!F2:F93)                                           → 16,1
=SUMPRODUCT(INSEE_EPCI!F2:F93; INSEE_EPCI!D2:D93) / SUM(INSEE_EPCI!D2:D93)   → 19,1
```

*(`SUMPRODUCT` = SOMMEPROD : multiplie les deux colonnes ligne à ligne, puis additionne.)*

- La **moyenne simple** (16,1 %) donne **le même poids** à chaque intercommunalité : une
  communauté de communes de 5 500 habitants pèse autant que la Métropole de Lille (1,2 million).
- La **moyenne pondérée** (19,1 %) donne à chaque intercommunalité un poids égal à **sa
  population** : chaque habitant compte pour une voix.

Le taux officiel publié par l'INSEE pour la région est **19 %** : c'est la moyenne pondérée qui le
retrouve. La moyenne simple sous-estime la pauvreté de 3 points, parce que les intercommunalités
rurales, nombreuses et peu peuplées, sont moins pauvres que les grandes agglomérations, où vivent la
plupart des habitants.

> 📌 **Règle** : quand les lignes n'ont pas la même taille (des territoires, des magasins…) et que
> ta question porte sur les **personnes**, pondère. Et donne toujours les deux chiffres.

---

## Mémo

| Besoin | Fonction ou geste |
|---|---|
| Importer un 2ᵉ fichier | *Fichier › Importer* › **Insérer de nouvelles feuilles** |
| Rapporter une valeur d'un autre tableau | `XLOOKUP(clé; colonne des clés; colonne à rapporter; "si absent")` (RECHERCHEX) |
| Recopier jusqu'en bas | double-clic sur le petit carré bleu |
| Vérifier une jointure | `COUNTA`, puis `COUNTIF(…; "code introuvable")` = 0 (NB.SI) |
| Moyenne pondérée | `SUMPRODUCT(valeurs; poids) / SUM(poids)` (SOMMEPROD) |

## Auto-évaluation

- [ ] Je sais dire pourquoi on joint sur le code INSEE et jamais sur le nom.
- [ ] Je sais écrire un `XLOOKUP` avec une valeur « si introuvable ».
- [ ] Je vérifie une jointure par deux comptes avant de m'en servir.
- [ ] Je sais expliquer pourquoi la moyenne pondérée (19,1 %) diffère de la moyenne simple (16,1 %).

⬅️ Cours précédent : [04 — Graphiques](04-choisir-le-bon-graphique.md) · ➡️ Brief : [B02-T](../../99-Brief/Data-Analyst-WSC/B02-T-transposer-portrait-territoire.md)
