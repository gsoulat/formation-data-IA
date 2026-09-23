# A/B testing — décider entre deux versions, sans se faire piéger par le hasard

> 🎯 **Ça te servira pour…** trancher une vraie question business : « la nouvelle page produit
> fait-elle **vraiment** vendre plus, ou c'est juste de la chance ? ». L'A/B test est l'outil du
> Data Analyst pour transformer une intuition (« je crois que le bouton vert convertit mieux »)
> en **décision fondée sur les données**.

Un A/B test, c'est simplement un **test d'hypothèse appliqué à une expérience** : on montre la
version **A** (l'existante) à une moitié des visiteurs, la version **B** (la nouvelle) à l'autre
moitié, et on compare une métrique. C'est le prolongement direct du chapitre précédent
([tests d'hypothèses](02-tests-hypotheses-avances.md)) — ici sur une **différence de taux**.

---

## 1. L'idée, avec NordRetail

Le site e-commerce de NordRetail affiche un bouton « Ajouter au panier » gris. Le service
marketing pense qu'un bouton **vert** inciterait plus à l'achat. Plutôt que de trancher au
feeling (ou au « chef a décidé »), on **teste** :

- **Version A** (contrôle) : bouton gris → montrée à 5 000 visiteurs.
- **Version B** (variante) : bouton vert → montrée à 5 000 autres visiteurs, **tirés au hasard**.
- **Métrique observée** : le **taux de conversion** (part des visiteurs qui achètent).

Résultat observé :

| Version | Visiteurs | Achats | Taux de conversion |
|---|---|---|---|
| A (gris) | 5 000 | 300 | 6,0 % |
| B (vert) | 5 000 | 345 | 6,9 % |

B semble meilleure (+0,9 point, soit +15 % relatif). **Mais est-ce réel, ou du bruit ?** Si tu
relançais l'expérience demain, l'écart pourrait s'inverser. C'est exactement la question à
laquelle le test répond.

---

## 2. Le raisonnement (rappel, version A/B)

Comme tout test d'hypothèse :

- **H₀ (hypothèse nulle)** : les deux versions convertissent pareil. L'écart observé = hasard de l'échantillon.
- **H₁ (hypothèse alternative)** : les taux diffèrent (B convertit différemment de A).

On calcule la **p-value** : la probabilité d'observer un écart **au moins aussi grand** que
+0,9 point **si H₀ était vraie** (si en réalité les deux boutons étaient équivalents).

- **p-value < 0,05** → l'écart est **statistiquement significatif** : on adopte B.
- **p-value ≥ 0,05** → on ne peut pas conclure : l'écart est peut-être du bruit, on garde A.

> **Analogie** — Tu lances deux pièces 10 fois : l'une fait 6 piles, l'autre 5. Vas-tu déclarer
> la première « plus chanceuse » ? Non : sur si peu de lancers, l'écart est banal. L'A/B test
> mesure précisément à partir de quand un écart cesse d'être « banal » compte tenu du **volume**.

---

## 3. Le calcul en Python

On compare **deux proportions**. Le test adapté est le **test z de proportions** (ou un χ² sur
le tableau de contingence — ils sont équivalents ici).

```python
from statsmodels.stats.proportion import proportions_ztest

achats   = [345, 300]     # succès : B puis A
visiteurs = [5000, 5000]  # tailles des groupes

stat, p_value = proportions_ztest(count=achats, nobs=visiteurs, alternative="two-sided")
print(f"p-value = {p_value:.4f}")

if p_value < 0.05:
    print("✅ Écart significatif : on adopte la version B")
else:
    print("⛔ Écart non significatif : on ne change rien pour l'instant")
```

Sur cet exemple, `p-value ≈ 0,07` → **au-dessus de 5 %** : malgré un +15 % relatif alléchant,
on **ne peut pas** conclure que le bouton vert est meilleur. Il faudrait **plus de données**.

> 💡 Ce résultat contre-intuitif est le cœur du métier : un joli chiffre relatif (« +15 % ! »)
> peut n'être **que du bruit**. Le DA est là pour le dire avant qu'on refonde tout le site.

---

## 4. La taille d'échantillon : le piège n°1

Pourquoi +0,9 point n'est pas significatif ici, alors qu'il le serait sur 50 000 visiteurs ? Parce
que la **précision d'un taux dépend du volume**. Deux réflexes de DA :

- **Estimer la taille nécessaire AVANT de lancer** le test (analyse de puissance), en fonction de
  l'effet minimal qu'on veut détecter. Détecter +0,5 point demande beaucoup plus de trafic que
  détecter +3 points.
- **Ne jamais « regarder en continu » et s'arrêter dès que ça passe sous 5 %** (le *peeking*) :
  en scrutant les résultats en temps réel, on finit toujours par tomber sur un faux positif. On
  fixe la durée / la taille **à l'avance**, et on regarde **à la fin**.

```python
from statsmodels.stats.proportion import proportion_effectsize
from statsmodels.stats.power import NormalIndPower

# Taille nécessaire pour détecter un passage de 6,0 % à 6,9 %, à 80 % de puissance
effet = proportion_effectsize(0.069, 0.060)
n = NormalIndPower().solve_power(effect_size=effet, alpha=0.05, power=0.80, alternative="two-sided")
print(f"≈ {round(n)} visiteurs PAR groupe nécessaires")   # ≈ 11 000 → nos 5 000 étaient trop justes
```

---

## 5. Les autres pièges à connaître

| Piège | Ce qui se passe | La parade |
|---|---|---|
| **Peeking** | On s'arrête dès que p < 0,05 → faux positifs | Fixer la durée/taille à l'avance |
| **Trop de variantes** | Tester A/B/C/D/E multiplie les faux positifs | Corriger le seuil (Bonferroni) ou limiter |
| **Effet nouveauté** | B « marche » juste parce que c'est nouveau | Laisser tourner assez longtemps |
| **Groupes non comparables** | A et B diffèrent déjà avant le test | **Randomiser** l'affectation des visiteurs |
| **Métrique mal choisie** | On optimise les clics… au détriment des ventes | Choisir une métrique alignée sur le business |

---

## 6. La démarche complète (mémo)

1. **Une hypothèse claire** : « le bouton vert augmentera la conversion ».
2. **Une métrique unique** décidée à l'avance (taux de conversion).
3. **Calculer la taille** d'échantillon nécessaire.
4. **Randomiser** : chaque visiteur voit A ou B au hasard.
5. **Laisser tourner** jusqu'à la taille prévue (pas de peeking).
6. **Tester** (p-value) et **décider** — puis mesurer l'impact réel après déploiement.

---

## À retenir

- Un A/B test = un **test d'hypothèse sur une différence de taux** : même raisonnement (H₀, p-value, seuil 5 %).
- Un écart **relatif** impressionnant peut être **non significatif** : tout dépend du **volume**.
- Les deux tueurs de tests : le **peeking** (regarder en continu) et une **taille d'échantillon** insuffisante.
- **Randomiser** est non négociable, sinon on compare des groupes qui diffèrent déjà.
- Le DA ne « prouve » jamais qu'il n'y a pas d'effet : il dit « on n'a pas assez de preuves pour conclure ».

## Pour aller plus loin

- Chapitre précédent — [Tests d'hypothèses : t de Student & χ²](02-tests-hypotheses-avances.md)
- Application décision par la donnée — [Métier & besoin (BI)](../../../15-Business-Intelligence/03-Analyse-Besoin-Metier/)
- `statsmodels` — documentation des tests de proportions : https://www.statsmodels.org/stable/stats.html
