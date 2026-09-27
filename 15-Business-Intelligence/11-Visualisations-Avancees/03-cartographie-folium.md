# 03 — Cartographie de données avec Folium

| | |
|---|---|
| **Module** | 11 — Visualisations avancées |
| **Durée indicative** | ~10 h |
| **Objectif** | Représenter des informations géographiques de manière agrégée et interactive |
| **Pré-requis** | [Pandas](../../01-Fondamentaux/Python/06-Data-Engineering/), dataviz descriptive ([module 04 EDA](../04-Analyse-Exploratoire-EDA/)) |
| **Posture** | **Réalisation** : on produit une carte interactive répondant à un besoin métier géolocalisé. |

> Fil rouge : **NordRetail** a 12 magasins dans les Hauts-de-France. La direction veut une
> **carte** : où sont les magasins, lesquels performent le mieux, et quel département génère le
> plus de CA ? Une carte vaut mille lignes de tableau pour une donnée **géographique**.

---

## Objectifs pédagogiques

À la fin de ce module, tu seras capable de :

1. Créer une carte interactive centrée sur une zone avec **Folium**.
2. Placer des **marqueurs** enrichis (popups, couleurs selon une valeur).
3. Construire une **carte choroplèthe** (départements colorés selon un indicateur).
4. Agréger des données par zone géographique avant de les cartographier.
5. Exporter la carte en **HTML autonome** pour la partager.

---

## Pourquoi c'est utile au Data Analyst

Dès qu'une donnée porte une **localisation** (magasin, client, région, incident), une carte
révèle des schémas invisibles dans un tableau : concentrations, zones blanches, disparités
régionales. Représenter des **données géographiques agrégées** de façon interactive fait partie
des attendus courants d'un tableau de bord orienté territoire.

---

## 1. Une première carte

**Folium** génère des cartes [Leaflet.js](https://leafletjs.com/) depuis Python. On centre la
carte sur des coordonnées (latitude, longitude) et un niveau de zoom.

```python
import folium

# Centre approximatif des Hauts-de-France
carte = folium.Map(location=[50.4, 2.8], zoom_start=8, tiles="OpenStreetMap")
carte.save("carte_nordretail.html")   # ouvrable dans un navigateur
```

> 💡 En notebook Jupyter, il suffit d'écrire `carte` sur la dernière ligne d'une cellule
> pour l'afficher directement.

---

## 2. Placer des marqueurs enrichis

Une ligne = un point géolocalisé. On ajoute un **popup** (au clic) et une **infobulle** (au survol).

```python
import pandas as pd

magasins = pd.DataFrame({
    "ville":   ["Lille", "Roubaix", "Dunkerque", "Valenciennes"],
    "lat":     [50.629, 50.691, 51.034, 50.358],
    "lon":     [3.057, 3.174, 2.377, 3.523],
    "ca_keur": [820, 410, 305, 260],
})

carte = folium.Map(location=[50.4, 2.8], zoom_start=8)

for _, row in magasins.iterrows():
    # Couleur selon la performance : vert si CA élevé, orange sinon
    couleur = "green" if row["ca_keur"] >= 400 else "orange"
    folium.Marker(
        location=[row["lat"], row["lon"]],
        popup=f"<b>{row['ville']}</b><br>CA : {row['ca_keur']} k€",
        tooltip=row["ville"],
        icon=folium.Icon(color=couleur, icon="shopping-cart", prefix="fa"),
    ).add_to(carte)

carte.save("magasins.html")
```

### Cercles proportionnels

Pour représenter une **grandeur** (le CA) par la **taille**, `CircleMarker` est plus lisible
qu'une icône :

```python
for _, row in magasins.iterrows():
    folium.CircleMarker(
        location=[row["lat"], row["lon"]],
        radius=row["ca_keur"] / 50,       # rayon proportionnel au CA
        popup=f"{row['ville']} : {row['ca_keur']} k€",
        color="crimson", fill=True, fill_opacity=0.6,
    ).add_to(carte)
```

---

## 3. La carte choroplèthe : colorer des zones

Une **choroplèthe** colore des zones (départements, régions) selon un indicateur agrégé. Il
faut deux ingrédients :

1. Un fichier **GeoJSON** décrivant les frontières des zones (téléchargeable en open data,
   ex. [france-geojson](https://github.com/gregoiredavid/france-geojson)).
2. Un **DataFrame** avec, par zone, la valeur à représenter.

```python
# CA agrégé par département (code INSEE)
ca_dept = pd.DataFrame({
    "code_dept": ["59", "62", "80", "02", "60"],
    "ca_keur":   [1230, 540, 210, 180, 150],
})

carte = folium.Map(location=[49.8, 2.8], zoom_start=7)

folium.Choropleth(
    geo_data="departements-hauts-de-france.geojson",
    data=ca_dept,
    columns=["code_dept", "ca_keur"],
    key_on="feature.properties.code",   # clé de jointure dans le GeoJSON
    fill_color="YlOrRd",                # palette : jaune → rouge
    fill_opacity=0.7, line_opacity=0.3,
    legend_name="CA par département (k€)",
).add_to(carte)

carte.save("choropleth_ca.html")
```

Le point délicat est **`key_on`** : il doit pointer vers la propriété du GeoJSON qui correspond
à ta colonne de jointure (ici le code département). Une erreur ici = une carte toute grise.

---

## 4. Agréger avant de cartographier

Une carte ne se dessine **jamais** sur des données brutes : on **agrège d'abord** avec Pandas.

```python
# De 50 000 lignes de ventes → 1 ligne par département
ca_dept = (ventes
           .groupby("code_dept", as_index=False)["ca"]
           .sum()
           .rename(columns={"ca": "ca_total"}))
```

C'est le sens de « représenter les données **de manière agrégée** » : la maille géographique
(département, ville) porte une **synthèse**, pas le détail transactionnel.

---

## À retenir

- Folium = cartes interactives Leaflet depuis Python, exportables en HTML autonome.
- **Marqueurs / CircleMarker** pour des points ; **Choropleth** pour colorer des zones.
- Une choroplèthe = **GeoJSON** (frontières) + **DataFrame** (valeurs), joints par `key_on`.
- On **agrège toujours** avec Pandas (`groupby`) avant de cartographier.
- Couleur et taille encodent une valeur : la carte doit **répondre à une question métier**.

## Pour aller plus loin

- **`HeatMap`** (plugin `folium.plugins`) — densité de points (clients, incidents).
- **`MarkerCluster`** — regrouper des milliers de marqueurs proches.
- **GeoPandas** — manipuler des données géographiques comme des DataFrames.
- S'intègre à un dashboard via [Streamlit](../../12-Frontend-IA/02-Streamlit/) (`st.components` ou `folium_static`).
