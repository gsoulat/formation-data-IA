# 02 — Dataviz interactive & dynamique en Python (Plotly & Bokeh)

| | |
|---|---|
| **Module** | 11 — Visualisations avancées |
| **Durée indicative** | ~14 h |
| **Objectif** | Réaliser des visualisations interactives et dynamiques à destination d'utilisateurs opérationnels |
| **Pré-requis** | [Pandas](../../01-Fondamentaux/Python/06-Data-Engineering/), dataviz descriptive ([module 04 EDA](../04-Analyse-Exploratoire-EDA/)) |
| **Posture** | **Réalisation** : on produit des graphiques manipulables (zoom, survol, filtres), pas des images figées. |

> Fil rouge : chez **NordRetail**, la direction veut pouvoir **explorer elle-même** les ventes :
> survoler un point pour voir le détail, zoomer sur une période, filtrer par magasin. Un
> `matplotlib` statique ne suffit plus — il faut de l'**interactif**.

---

## Objectifs pédagogiques

À la fin de ce module, tu seras capable de :

1. Expliquer **pourquoi et quand** choisir une visualisation interactive plutôt que statique.
2. Créer des graphiques interactifs avec **Plotly Express** (le plus rapide).
3. Ajouter des **infobulles** (`hover`), du zoom et des filtres.
4. Découvrir **Bokeh** et comprendre en quoi il diffère de Plotly.
5. **Exporter** une visualisation en HTML autonome, partageable sans Python.

---

## Pourquoi c'est utile au Data Analyst

Un graphique statique **répond** à une question. Un graphique interactif **laisse l'utilisateur
poser les siennes**. Pour une restitution à des opérationnels (managers de magasin, direction),
l'interactivité transforme un rapport qu'on subit en un outil qu'on explore — exactement ce
qu'on attend d'une viz « à destination d'utilisateurs opérationnels ».

| | Statique (matplotlib/seaborn) | Interactif (Plotly/Bokeh) |
|---|---|---|
| Sortie | Image PNG | HTML (zoom, survol, filtres) |
| Usage | Rapport PDF, article | Dashboard, exploration |
| Public | Lecteur passif | Utilisateur qui manipule |

---

## 1. Plotly Express : l'interactif en une ligne

`plotly.express` (importé `px`) est la porte d'entrée : une fonction = un graphique interactif.

```python
import plotly.express as px
import pandas as pd

ventes = pd.read_csv("ventes_nordretail.csv")   # colonnes : date, magasin, ca, categorie

# Courbe de CA par magasin — interactive par défaut (zoom, survol, légende cliquable)
fig = px.line(
    ventes,
    x="date", y="ca", color="magasin",
    title="Chiffre d'affaires par magasin",
    labels={"ca": "CA (€)", "date": "Date"},
)
fig.show()
```

Rien à configurer : le zoom, le déplacement, la légende cliquable (isoler un magasin) et
l'export PNG sont **inclus**. Les graphiques les plus utiles pour un DA :

```python
px.bar(ventes, x="magasin", y="ca", color="categorie", barmode="group")  # barres groupées
px.scatter(ventes, x="budget_pub", y="ca", size="ca", color="magasin")   # nuage de points
px.histogram(ventes, x="ca", nbins=30)                                   # distribution
px.box(ventes, x="magasin", y="ca")                                      # boîtes à moustache
```

---

## 2. Soigner les infobulles (`hover`)

L'infobulle est **le** superpouvoir de l'interactif : afficher au survol des infos qui
n'encombrent pas le graphique.

```python
fig = px.scatter(
    ventes,
    x="budget_pub", y="ca",
    color="magasin",
    hover_name="magasin",
    hover_data={"date": True, "categorie": True, "ca": ":.0f"},  # format : entier
)
fig.update_layout(hovermode="x unified")   # une seule infobulle regroupée par abscisse
fig.show()
```

---

## 3. Ajouter des filtres dynamiques

Plotly permet d'ajouter des **menus déroulants** ou des **curseurs de temps** sans dashboard.

```python
# Un curseur de plage temporelle (range slider) sous une courbe
fig = px.line(ventes, x="date", y="ca", title="CA total")
fig.update_xaxes(rangeslider_visible=True)
fig.show()
```

Pour de vrais filtres pilotés par l'utilisateur (menus par magasin, boutons), on combine
généralement Plotly avec **[Streamlit](../../12-Frontend-IA/02-Streamlit/)** — déjà au
programme du dépôt et compatible Plotly nativement.

---

## 4. Bokeh : l'alternative orientée « application »

**Bokeh** vise le même besoin (dataviz web interactive) avec une philosophie plus « briques à
assembler » : on construit la figure élément par élément, ce qui donne plus de contrôle pour
des outils complexes (widgets liés, tableaux de bord sur mesure).

```python
from bokeh.plotting import figure, show
from bokeh.models import HoverTool

p = figure(title="CA par jour", x_axis_type="datetime",
           width=800, height=400)
p.line(ventes["date"], ventes["ca"], line_width=2, legend_label="CA")
p.add_tools(HoverTool(tooltips=[("Date", "@x{%F}"), ("CA", "@y{0,0} €")],
                      formatters={"@x": "datetime"}))
show(p)
```

**Comment choisir ?**

| Critère | Plotly | Bokeh |
|---|---|---|
| Prise en main | ⚡ très rapide (`px`) | plus verbeux |
| Cas typique | graphiques prêts à l'emploi | applications data sur mesure |
| Écosystème | Streamlit, Dash | Panel, serveur Bokeh |

> 👉 **Pour un Data Analyst**, commence par **Plotly Express** (rapide, couvre 90 % des besoins).
> Bokeh est bon à connaître, à sortir quand tu construis une vraie application de données.

---

## 5. Partager : exporter en HTML autonome

Un graphique interactif se partage en **un seul fichier HTML** — ouvrable dans n'importe quel
navigateur, **sans Python installé**.

```python
fig.write_html("ca_par_magasin.html")   # Plotly : fichier autonome, prêt à envoyer
```

C'est idéal pour joindre une viz explorable à un mail ou l'héberger, sans exiger d'outil BI.

---

## À retenir

- Interactif = l'utilisateur **explore** (zoom, survol, filtres) au lieu de subir une image.
- **Plotly Express** : un graphique interactif par ligne — le réflexe du DA.
- L'**infobulle** (`hover_data`) enrichit sans surcharger.
- **Bokeh** : plus de contrôle pour des applications data sur mesure.
- **`write_html()`** produit un livrable autonome, partageable sans Python.

## Pour aller plus loin

- [Streamlit](../../12-Frontend-IA/02-Streamlit/) — transformer ces graphiques en dashboard filtrable.
- **Dash** (Plotly) — applications web analytiques complètes en Python.
- Prolongement naturel : la [cartographie interactive avec Folium](03-cartographie-folium.md).
