# Sources des jeux de données — Module 10 (Tableur : statistiques & TCD)

Chaque fichier porte en interne un onglet `Dictionnaire` et, selon le cas, un onglet
`Perimetre_et_source` ou `Journal_nettoyage`. Ce document récapitule l'origine, la licence et les
limites connues.

---

## 1. `cyclonord_ventes_2025_fiable.xlsx` · 613 lignes

**Nature** — Jeu **fictif** conçu pour la formation. Une enseigne de vente et réparation de vélos
dans les Hauts-de-France, huit magasins, exercice 2025.

**Généalogie** — Version **fiabilisée** de `cyclonord_commandes_2025_brut.xlsx` (627 lignes), le
fichier audité en semaine P1. Les corrections appliquées sont documentées ligne à ligne dans
l'onglet `Journal_nettoyage` : normalisation des libellés de magasin, complétion de `Departement`
et `Categorie`, suppression des doublons d'identifiant, retrait des dates hors 2025 et des
quantités impossibles, plafonnement des remises à 20 %, recalcul de `Montant_TTC`, effacement des
notes hors barème. **14 lignes écartées sur 627 (2,2 %).**

**Laissé exprès** — Trois commandes de quantité 100 sont **conservées telles quelles** et signalées
« en suspens » dans le journal. Ce n'est pas un oubli : décider quoi en faire est l'objet de
l'exercice du mardi.

**Usage** — Cours 01 à 04, exercice guidé (niveau 1).

**Licence** — Jeu pédagogique, réutilisable librement dans le cadre de la formation.

---

## 2. `cyclonord_commandes_2025_brut.xlsx` · 627 lignes

Le fichier **avant nettoyage**, celui de la semaine P1. Fourni pour permettre la comparaison
avant / après et pour rejouer l'audit si besoin. Ne pas l'utiliser pour les calculs de ce module.

---

## 3. `carburants_france_releve.xlsx` · 31 277 lignes · **données réelles**

| | |
|---|---|
| **Jeu** | Prix des carburants en France — flux instantané (v2) |
| **Producteur** | Ministère de l'Économie et des Finances |
| **Page** | https://data.economie.gouv.fr/explore/dataset/prix-des-carburants-en-france-flux-instantane-v2/ |
| **API utilisée** | `https://data.economie.gouv.fr/api/explore/v2.1/catalog/datasets/prix-des-carburants-en-france-flux-instantane-v2/exports/csv` |
| **Date d'extraction** | 18/09/2026 |
| **Licence** | **Licence Ouverte 2.0 (Etalab)** — réutilisation libre avec mention de la source |
| **Volume** | 9 800 stations · 31 277 couples station × carburant |

**Mise en forme appliquée** — Le fichier source est en format *large* (une colonne de prix par
carburant). Il a été **dépivoté en format long** (1 ligne = 1 station × 1 carburant), forme
directement exploitable par un TCD. Ajout de deux colonnes calculées : `Type_de_station`
(Route / Autoroute, depuis le champ `pop`) et `Energie` (regroupement Diesel / Essence /
Biocarburant / Gaz). Lignes sans prix retirées ; prix conservés entre 0,30 et 4,00 €/L.

**Limites à faire dire aux apprenants**
- C'est une **photographie** : chaque station affiche son dernier prix déclaré, et toutes ne
  déclarent pas au même moment. Un prix peut dater de plusieurs jours.
- Seules les stations **déclarantes** y figurent (obligation légale pour les stations ouvertes au
  public, mais la déclaration reste déclarative).
- Le fichier ne dit **rien des volumes vendus** : une station de village pèse autant qu'une station
  d'hypermarché. Toute moyenne est donc une moyenne *par station*, pas *par litre vendu*.
- Le champ `Ville` est en saisie libre : la casse et l'orthographe varient.

**Usage** — Brief B02-A (niveau 2 · adapter).

---

## 4. `portrait_territoire_hdf_socle.xlsx` · 3 782 communes · **données réelles**

Socle de départ du brief B02-T, complété par `insee_revenus_population_hdf.xlsx` (§ 5). Les deux
fichiers suffisent pour tout le brief. Les lignes « Facultatif (pour aller plus loin) » de l'onglet
`Sources` listent des sources supplémentaires pour le bonus du brief ; **rien n'est à télécharger**
pour les étapes obligatoires.

### Onglet `Communes_HDF` — 3 782 lignes

| | |
|---|---|
| **Source** | API Géo (Etalab), qui rediffuse le référentiel communal et les populations légales INSEE |
| **URL** | `https://geo.api.gouv.fr/departements/{02,59,60,62,80}/communes?fields=nom,code,population,surface,codeEpci` |
| **Licence** | Licence Ouverte 2.0 |
| **Colonnes calculées** | `Superficie_km2` (= surface ÷ 100), `Densite_hab_km2`, `Taille_commune` (5 tranches) |
| **Libellés EPCI** | `https://geo.api.gouv.fr/epcis?fields=nom,code` |

### Onglet `Marche_immobilier_2024` — 1 812 communes

| | |
|---|---|
| **Source** | Demandes de valeurs foncières géolocalisées (DVF), millésime 2024 — DGFiP / Etalab |
| **URL** | `https://files.data.gouv.fr/geo-dvf/latest/csv/2024/departements/{02,59,60,62,80}.csv.gz` |
| **Licence** | Licence Ouverte 2.0 |
| **Filtres** | `nature_mutation = Vente` · logements uniquement (maison / appartement) · une ligne par mutation (lots agrégés, ventes mixtes écartées) · prix 15 000 – 1 500 000 € · surface 15 – 400 m² · prix/m² 250 – 9 000 € |
| **Seuil** | Seules les communes comptant **au moins 5 ventes** en 2024 sont conservées, pour éviter les médianes calculées sur deux transactions |

**Limites à faire dire aux apprenants**
- DVF ne couvre **ni l'Alsace-Moselle ni Mayotte** (régime cadastral distinct).
- Une médiane calculée sur 5 ventes n'a pas la même fiabilité qu'une médiane sur 3 000 : la
  colonne `Nb_ventes_2024` doit **toujours** accompagner le prix.
- 1 970 communes sur 3 782 n'ont pas de marché mesurable en 2024 : leur absence est une
  information, pas un trou de données.

### Onglet `Sources`

Liste des pistes d'enrichissement (INSEE Dossier complet, Base permanente des équipements,
Data ES, Géo2France) avec les URL. Elles servent au « pour aller plus loin » du brief B02-T.
*(Le lien de la Base permanente des équipements indiqué dans cet onglet est mort ; adresse à jour :
https://www.insee.fr/fr/metadonnees/source/serie/s1161)*

## 5. `insee_revenus_population_hdf.xlsx` · 3 782 communes et 92 intercommunalités · **données réelles**

Source complémentaire **fournie** pour le brief B02-T (et la démo du cours 06).

| | |
|---|---|
| **Source** | INSEE, *Base du comparateur de territoires* — https://www.insee.fr/fr/statistiques/2521169 |
| **Millésimes** | niveau de vie et taux de pauvreté : Filosofi 2023 · population : recensements 2017 et 2023 · géographie au 1er janvier 2026 |
| **Licence** | Licence Ouverte 2.0 |
| **Extraction** | 24/09/2026. Le fichier complet compte 2,9 millions de lignes (trop pour un tableur) : extrait filtré sur les communes et intercommunalités des Hauts-de-France, mis en colonnes, sans autre modification |
| **Onglets** | `INSEE_Communes` (clé `Code_INSEE`, texte) · `INSEE_EPCI` (clé `Code_EPCI`, texte) · `INSEE_Source` |

**Limites à faire dire aux apprenants**
- Le niveau de vie et le taux de pauvreté sont couverts par le **secret statistique** pour les
  petites communes : les cases contiennent « non publié » (taux publié pour 520 communes sur 3 782,
  mais pour les 92 intercommunalités).
- Deux intercommunalités débordent sur la Normandie (CC des Villes Sœurs, CC Interrégionale Aumale –
  Blangy-sur-Bresle) : l'INSEE les mesure en entier, le socle n'en contient que les communes picardes.


---

## Règle commune

Tout livrable qui réutilise ces fichiers doit mentionner **la source, la date d'extraction, le
périmètre et la licence**. C'est une exigence de la Licence Ouverte, et c'est aussi le premier
réflexe professionnel d'un analyste.
