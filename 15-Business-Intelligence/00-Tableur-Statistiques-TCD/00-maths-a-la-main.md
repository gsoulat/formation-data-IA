# 00 — Les maths à la main : moyenne, médiane, écart-type…

> 🧮 **À quoi sert ce cours ?** Google Sheets calcule tout pour toi. Mais pour savoir **si un chiffre
> a du sens**, il faut comprendre ce que la machine a fait. Ici, on refait chaque calcul **à la main,
> sur 7 nombres**, avant de le confier au tableur. Garde cette page ouverte pendant les deux semaines.

| | |
|---|---|
| **Quand** | à lire le lundi (sections 1 à 3) et le mardi (sections 4 à 6) ; la section 7 sert au brief B02-T |
| **Durée** | 30 min de lecture, 30 min d'exercices |
| **Niveau** | aucune connaissance en maths au-delà des 4 opérations |

---

## 1. Le vocabulaire

| Mot | Sens | Exemple Cyclo'Nord |
|---|---|---|
| **Individu** | ce qu'on observe, une ligne du tableau | une commande |
| **Variable** | ce qu'on mesure, une colonne | le montant, le magasin |
| **Effectif** (`n`) | le nombre d'individus | 613 commandes |
| **Valeur** | le contenu d'une case | 177 € |
| **Distribution** | la façon dont les valeurs se répartissent | beaucoup de petites commandes, peu de grosses |

Toute la suite utilise ces **7 commandes**, déjà rangées de la plus petite à la plus grande :

```
12 €   19 €   25 €   40 €   55 €   90 €   600 €
```

---

## 2. La moyenne

**On additionne tout, puis on divise par le nombre de valeurs.**

```
12 + 19 + 25 + 40 + 55 + 90 + 600 = 841
841 ÷ 7 = 120,14 €
```

En écriture mathématique, on la note **x̄** (« x barre ») :

$$\bar{x} = \frac{x_1 + x_2 + \dots + x_n}{n} = \frac{\sum x_i}{n}$$

Le signe **Σ** (sigma) veut simplement dire « additionne tout ».

Dans Sheets : `=AVERAGE(plage)` *(MOYENNE)*.

> ⚠️ **120 € ne ressemble à aucune des 7 commandes** : six font moins de 100 €. C'est la commande de
> 600 € qui tire la moyenne vers le haut. Sans elle, la moyenne des six autres tombe à **40,17 €**.

---

## 3. La médiane et le mode

**La médiane** : on range les valeurs dans l'ordre, et on prend **celle du milieu**.

- **Nombre impair** de valeurs (ici 7) : la valeur du milieu est la 4ᵉ → **40 €**.
  Trois commandes en dessous, trois au-dessus.
- **Nombre pair** : on fait la moyenne des deux du milieu. Sans la commande de 600 €, il reste
  6 valeurs : les deux du milieu sont 25 et 40 → (25 + 40) ÷ 2 = **32,50 €**.

Dans Sheets : `=MEDIAN(plage)` *(MEDIANE)*.

> 💡 La médiane de nos 7 commandes (40 €) ne bouge pas si la plus grosse vaut 600 € ou 600 000 € :
> on dit qu'elle est **robuste**. La moyenne, elle, s'envolerait.

**Le mode** : la valeur **la plus fréquente**. Dans `2, 4, 4, 4, 5, 5, 7, 9`, le mode est **4**
(présent trois fois). Dans nos 7 commandes, aucune valeur ne se répète : pas de mode.

Dans Sheets : `=MODE(plage)`.

### Moyenne ou médiane ?

| Si… | la distribution est… | on donne plutôt… |
|---|---|---|
| moyenne ≈ médiane | symétrique | la moyenne, ou les deux |
| moyenne > médiane | étalée à droite (quelques très grandes valeurs) | **la médiane** |
| moyenne < médiane | étalée à gauche (quelques très petites valeurs) | **la médiane** |

Nos 7 commandes : moyenne 120 € > médiane 40 € → étalées à droite → on donne la médiane.

---

## 4. L'étendue et les quartiles

**L'étendue** : la plus grande valeur moins la plus petite. `600 − 12 = 588 €`. Elle ne regarde
que deux valeurs, donc une seule valeur extrême la fausse.

**Les quartiles** coupent la liste rangée en **quatre parts égales** :

| Repère | Sens | Nos 7 commandes (calcul Sheets) |
|---|---|---|
| **Q1** | 25 % des valeurs en dessous | **22 €** |
| **Q2** = médiane | 50 % en dessous | **40 €** |
| **Q3** | 75 % en dessous | **72,50 €** |

La phrase à savoir dire : **« la moitié des commandes est entre Q1 et Q3 »**, ici entre 22 € et
72,50 €. L'écart **Q3 − Q1** (50,50 €) s'appelle l'**écart interquartile**.

> 🔎 **Pourquoi 22 € alors que 22 n'est pas dans la liste ?** Q1 tombe « entre » la 2ᵉ valeur (19) et
> la 3ᵉ (25). Sheets prend alors un point intermédiaire : 19 + (25 − 19) ÷ 2 = 22. Il existe d'autres
> façons de faire, qui donnent des résultats un peu différents (au lycée, on prend souvent la
> 2ᵉ valeur, 19). Ce n'est pas une erreur : c'est une **convention**. Dans ce module, on utilise
> toujours celle de Sheets : `=QUARTILE(plage; 1)` et `=QUARTILE(plage; 3)`.

---

## 5. L'écart-type, pas à pas

L'écart-type mesure **à quelle distance les valeurs sont, en général, de la moyenne**. On le calcule
sur une série simple : `2, 4, 4, 4, 5, 5, 7, 9` (8 valeurs, moyenne **5**).

| Valeur | Écart à la moyenne (valeur − 5) | Écart au carré |
|---|---|---|
| 2 | −3 | 9 |
| 4 | −1 | 1 |
| 4 | −1 | 1 |
| 4 | −1 | 1 |
| 5 | 0 | 0 |
| 5 | 0 | 0 |
| 7 | 2 | 4 |
| 9 | 4 | 16 |
| | **somme** | **32** |

1. **On mesure l'écart** de chaque valeur à la moyenne.
2. **On met au carré** : sinon les écarts négatifs et positifs s'annuleraient (leur somme fait 0).
3. **On fait la moyenne des carrés** : 32 ÷ 8 = **4**. C'est la **variance**.
4. **On prend la racine carrée** pour revenir dans l'unité de départ : √4 = **2**. C'est l'**écart-type**.

> ✅ **Lecture** : en général, les valeurs sont à **environ 2** de la moyenne 5.

**Une subtilité** : quand les données sont un **échantillon** (une partie seulement de ce qu'on veut
décrire), on divise par **n − 1** au lieu de n : 32 ÷ 7 = 4,57, puis √4,57 = **2,14**. C'est ce que
fait `=STDEV(plage)` *(ECARTYPE)* dans Sheets, et c'est celui qu'on utilise dans le module. Avec
beaucoup de valeurs (613 commandes), les deux calculs donnent presque le même résultat.

| Écart-type… | veut dire… |
|---|---|
| petit par rapport à la moyenne | les valeurs sont regroupées, la moyenne les résume bien |
| grand par rapport à la moyenne | les valeurs sont très dispersées, la moyenne résume mal |

Cyclo'Nord : moyenne 1 680 €, écart-type 15 505 € → neuf fois la moyenne : très dispersé.

---

## 6. Pourcentages et évolutions

**Une part** : `partie ÷ total`. 360 commandes livrées sur 613 → 360 ÷ 613 = 0,587 = **58,7 %**.

**Une évolution** : `(nouvelle valeur − ancienne) ÷ ancienne`. Les gares des Hauts-de-France sont
passées de 110,6 à 126,8 millions de voyageurs : (126,8 − 110,6) ÷ 110,6 = **+14,6 %**.

> ⚠️ **Points ou pourcentage ?** Un taux qui passe de 16,1 % à 19,1 % augmente de **3 points**, pas
> de 3 %. En pourcentage, c'est (19,1 − 16,1) ÷ 16,1 = +18,6 %. On parle en **points** quand on
> compare deux pourcentages.

---

## 7. La moyenne pondérée

Quand toutes les valeurs ne comptent pas pareil, on leur donne un **poids** (un coefficient).

**Exemple du bac** : 12 en maths (coefficient 2), 15 en français (coefficient 4), 10 en sport
(coefficient 1).

```
Moyenne simple   : (12 + 15 + 10) ÷ 3                   = 12,33
Moyenne pondérée : (12×2 + 15×4 + 10×1) ÷ (2 + 4 + 1)   = 94 ÷ 7 = 13,43
```

Le français pèse plus lourd : la moyenne pondérée se rapproche de 15.

$$\text{moyenne pondérée} = \frac{\sum (valeur_i \times poids_i)}{\sum poids_i}$$

Dans Sheets : `=SUMPRODUCT(valeurs; poids) / SUM(poids)` *(SOMMEPROD)*. Pour des territoires, le
poids est souvent la **population** : chaque habitant compte pour une voix (brief B02-T).

---

## Exercices (30 min)

Série : `3, 5, 5, 6, 8, 9, 20` (7 valeurs).

1. Calcule la moyenne.
2. Donne la médiane et le mode.
3. Quelle est l'étendue ?
4. Moyenne ou médiane : laquelle résume le mieux cette série, et pourquoi ?
5. Retire le 20 : que deviennent la moyenne et la médiane ?
6. Un magasin passe de 40 à 50 commandes par jour. Quelle évolution en % ?
7. Deux classes : 10 élèves avec 12 de moyenne, 30 élèves avec 8. Quelle est la moyenne de tous
   les élèves ? (Attention : ce n'est pas 10.)

<details>
<summary>Réponses</summary>

1. (3 + 5 + 5 + 6 + 8 + 9 + 20) ÷ 7 = 56 ÷ 7 = **8**.
2. Médiane : la 4ᵉ valeur, **6**. Mode : **5** (deux fois).
3. 20 − 3 = **17**.
4. **La médiane** : la moyenne (8) est tirée vers le haut par le 20 ; six valeurs sur sept sont en dessous de 10.
5. Reste `3, 5, 5, 6, 8, 9` : moyenne 36 ÷ 6 = **6** ; médiane (5 + 6) ÷ 2 = **5,5**. La moyenne perd 2, la médiane seulement 0,5.
6. (50 − 40) ÷ 40 = **+25 %**.
7. Moyenne pondérée par le nombre d'élèves : (10 × 12 + 30 × 8) ÷ 40 = 360 ÷ 40 = **9**. La moyenne simple des deux classes (10) donnerait autant de poids à 10 élèves qu'à 30.

</details>

---

## Mémo

| Notion | À la main | Dans Sheets |
|---|---|---|
| Moyenne | somme ÷ nombre | `AVERAGE` |
| Médiane | valeur du milieu (rangées) | `MEDIAN` |
| Mode | valeur la plus fréquente | `MODE` |
| Étendue | max − min | `MAX(…) - MIN(…)` |
| Quartiles | coupent en 4 parts égales | `QUARTILE(…; 1)`, `QUARTILE(…; 3)` |
| Écart-type | racine de la moyenne des écarts au carré | `STDEV` |
| Évolution | (nouveau − ancien) ÷ ancien | `=(B2-A2)/A2` |
| Moyenne pondérée | Σ(valeur × poids) ÷ Σ poids | `SUMPRODUCT(…; …) / SUM(…)` |

➡️ Retour à la [feuille de route du module](README.md) · cours suivant : [01 — Position](01-statistiques-descriptives.md)
