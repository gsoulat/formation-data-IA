# 01 — Tableur avancé : tableaux croisés dynamiques & recherches inter-fichiers

| | |
|---|---|
| **Module** | 19 — Tableur avancé |
| **Durée indicative** | ~8 h |
| **Objectif** | Utiliser les fonctions avancées du tableur pour croiser et rapprocher des données |
| **Pré-requis** | Bases du tableur (saisie, formules simples), notions d'EDA |
| **Posture** | **Réalisation** : on manipule un vrai tableur (Excel / Google Sheets), l'outil quotidien du métier. |

> Fil rouge : chez **NordRetail**, on te transmet deux exports : `ventes.xlsx` (une ligne par
> vente) et `magasins.xlsx` (la fiche de chaque magasin). Avant tout dashboard, le métier veut
> une **synthèse dans le tableur** — l'outil que tout le monde sait ouvrir.

---

## Objectifs pédagogiques

À la fin de ce module, tu seras capable de :

1. Construire un **tableau croisé dynamique** (TCD) pour synthétiser des milliers de lignes.
2. Rapprocher deux fichiers avec une **recherche** (`RECHERCHEV` / `RECHERCHEX`).
3. Nettoyer et compléter des colonnes avec les fonctions texte et logiques.
4. Savoir **quand rester au tableur** et quand passer à Python/BI.

> ℹ️ **Excel ou Google Sheets ?** Les deux partagent la même logique ; les noms de fonctions
> changent parfois (`RECHERCHEV` = `VLOOKUP`). Google Sheets est **multi-OS et gratuit**
> (confort sur Mac). Les captures d'écran sont à réaliser en formation ; ce cours décrit la
> **méthode**, transposable aux deux outils.

---

## Pourquoi c'est utile au Data Analyst

Le tableur reste **l'outil universel** du métier : le client t'envoie des `.xlsx`, te lit des
`.xlsx`, et raisonne en `.xlsx`. Un DA capable de sortir un **TCD propre** en cinq minutes
répond à 80 % des demandes ad hoc sans écrire une ligne de code. C'est aussi le pont naturel
vers Power BI, dont le moteur (Power Query, DAX) prolonge ces mêmes idées.

---

## 1. Le tableau croisé dynamique (TCD)

Un TCD **agrège** automatiquement un grand tableau selon des dimensions que tu choisis — c'est
le `groupby` de Pandas, mais en glisser-déposer.

**À partir de `ventes.xlsx`** (colonnes : `date`, `magasin`, `categorie`, `montant`) :

| Zone du TCD | Ce qu'on y glisse | Résultat |
|---|---|---|
| **Lignes** | `magasin` | une ligne par magasin |
| **Colonnes** | `categorie` | une colonne par catégorie |
| **Valeurs** | `montant` (Somme) | le CA à chaque croisement |
| **Filtres** | `date` (année) | filtrer sur une période |

Étapes (Excel : *Insertion → Tableau croisé dynamique* ; Sheets : *Insertion → Tableau croisé
dynamique*) :

1. Sélectionne toute la plage de données (en-têtes compris).
2. Glisse `magasin` en **Lignes**, `categorie` en **Colonnes**.
3. Glisse `montant` en **Valeurs**, réglé sur **Somme** (par défaut c'est parfois « Nombre » —
   à vérifier !).
4. Ajoute `date` en **Filtre** pour isoler une année.

> 💡 **Le piège classique** : la zone Valeurs affiche « Nombre de montant » au lieu de la
> **somme**. Clique sur le champ → *Paramètres de champ de valeurs* → **Somme**.

### Croiser deux variables = obtenir une information

Le croisement *magasin × catégorie* révèle, par exemple, que Lille écrase la concurrence sur le
textile mais pas sur l'électroménager — une information **invisible** dans la liste brute. C'est
tout l'intérêt : proposer des **croisements de variables** pour faire émerger l'information
recherchée.

---

## 2. Rapprocher deux fichiers : la recherche

Les données utiles sont souvent **éparpillées** : les ventes dans un fichier, les infos magasin
(région, surface, responsable) dans un autre. On les rapproche grâce à une **clé commune**
(ici `magasin`).

### `RECHERCHEV` (VLOOKUP) — la classique

```
=RECHERCHEV(B2 ; magasins!A:D ; 3 ; FAUX)
```

- `B2` : la valeur cherchée (le nom du magasin dans la ligne de vente).
- `magasins!A:D` : la table où chercher (autre feuille/fichier).
- `3` : renvoyer la valeur de la **3ᵉ colonne** de cette table (ex. la région).
- `FAUX` : correspondance **exacte** (à mettre quasi toujours).

### `RECHERCHEX` (XLOOKUP) — la moderne

Plus souple : pas de comptage de colonnes, cherche dans les deux sens.

```
=RECHERCHEX(B2 ; magasins!A:A ; magasins!C:C ; "Inconnu")
```

- cherche `B2` dans la colonne A de `magasins`, renvoie la valeur en face dans la colonne C ;
- `"Inconnu"` : valeur affichée si rien n'est trouvé (gère proprement les manquants).

> ⚠️ **Recherche inter-fichiers** : si les deux tables sont dans des **classeurs séparés**,
> la référence inclut le nom du fichier : `[magasins.xlsx]Feuil1!A:C`. Les deux fichiers
> doivent rester ouverts / accessibles pour que la liaison se mette à jour.

---

## 3. Nettoyer & compléter avec les fonctions

Quelques fonctions couvrent l'essentiel du nettoyage au tableur :

| Besoin | Fonction | Exemple |
|---|---|---|
| Supprimer les espaces parasites | `SUPPRESPACE` (`TRIM`) | `=SUPPRESPACE(A2)` |
| Uniformiser la casse | `MAJUSCULE` / `MINUSCULE` / `NOMPROPRE` | `=NOMPROPRE(A2)` |
| Concaténer | `&` ou `CONCAT` | `=B2&" - "&C2` |
| Condition | `SI` (`IF`) | `=SI(D2>1000;"Gros panier";"Standard")` |
| Compter selon un critère | `NB.SI` (`COUNTIF`) | `=NB.SI(B:B;"Lille")` |
| Sommer selon un critère | `SOMME.SI` (`SUMIF`) | `=SOMME.SI(B:B;"Lille";D:D)` |

---

## 4. Quand rester au tableur, quand en sortir

| Reste au tableur si… | Passe à Python / Power BI si… |
|---|---|
| Quelques milliers de lignes | Centaines de milliers de lignes (le tableur rame) |
| Analyse ponctuelle, jetable | Traitement à **reproduire** chaque semaine |
| Le client veut manipuler lui-même | Sources multiples, modèle en étoile, DAX |
| Partage rapide d'une synthèse | Automatisation, historisation, gouvernance |

> 👉 Le tableur est parfait pour **explorer vite** et **partager simple**. Dès qu'il faut
> **reproduire** ou **industrialiser**, on bascule vers [Pandas](../../01-Fondamentaux/Python/06-Data-Engineering/)
> (`pivot_table`, `merge`) ou vers [Power BI](../09-Modelisation-Etoile-PowerQuery/).

> 🔗 **Le pont Pandas** : un TCD = `df.pivot_table(index="magasin", columns="categorie",
> values="montant", aggfunc="sum")` ; une `RECHERCHEV` = `df.merge(magasins, on="magasin",
> how="left")`. Comprendre le tableur, c'est déjà comprendre Pandas.

---

## À retenir

- Le **TCD** synthétise des milliers de lignes en glisser-déposer (Lignes / Colonnes / Valeurs / Filtres).
- **`RECHERCHEV` / `RECHERCHEX`** rapprochent deux fichiers via une clé commune.
- Attention au piège « Nombre au lieu de Somme » et à la correspondance **exacte** (`FAUX`).
- Le tableur excelle pour l'**ad hoc** et le **partage** ; on en sort pour **reproduire / industrialiser**.
- TCD ↔ `pivot_table`, RECHERCHEV ↔ `merge` : mêmes idées, deux outils.
