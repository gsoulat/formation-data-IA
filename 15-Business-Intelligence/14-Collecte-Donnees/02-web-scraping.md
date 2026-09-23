# 02 — Collecter des données par web scraping

| | |
|---|---|
| **Module** | 14 — Collecte de données |
| **Durée indicative** | ~14 h |
| **Objectif** | Automatiser la récupération de données depuis des pages web, dans le respect de la réglementation |
| **Pré-requis** | Python ([01-Syntaxe](../../01-Fondamentaux/Python/01-Syntaxe/)), API & Requests ([Python/06 · 05-api-rest-requests](../../01-Fondamentaux/Python/06-Data-Engineering/)), notions de HTML |
| **Posture** | **Implémentation** : on écrit du code de collecte. Le *choix* d'une source de scraping a été vu en conception dans le [chapitre 01](01-processus-collecte.md). |

> Fil rouge : tu es Data Analyst chez **NordRetail**. Le service marketing veut suivre les
> **prix des concurrents** affichés sur leurs sites e-commerce. Aucune API n'est proposée :
> la seule source disponible est le **HTML des pages produit**. Tu dois automatiser cette
> collecte — proprement et **légalement**.

---

## Objectifs pédagogiques

À la fin de ce module, tu seras capable de :

1. Décider **quand** le scraping est justifié (et quand il ne l'est pas).
2. Vérifier la **légalité** d'une collecte : `robots.txt`, CGU, RGPD.
3. Récupérer une page avec **`requests`** et l'analyser avec **`BeautifulSoup`**.
4. **Extraire** des données structurées (sélecteurs CSS, navigation dans le DOM).
5. Gérer la **pagination** et scraper plusieurs pages sans se faire bloquer.
6. Produire un **DataFrame** propre, prêt pour l'analyse.

---

## Pourquoi c'est utile au Data Analyst

Beaucoup de données précieuses n'existent **que** sur le web, sans API : prix concurrents,
avis clients, annonces, données publiques mal exposées. Savoir scraper, c'est **débloquer des
sources que personne d'autre n'a**. Mais c'est aussi une compétence à **haut risque juridique** :
un DA responsable sait autant *scraper* que *refuser de scraper*.

---

## 1. Avant de coder : ai-je le droit ?

Le scraping n'est pas illégal en soi, mais il est **encadré**. Trois vérifications, dans l'ordre :

| Vérification | Où regarder | Ce qui bloque |
|---|---|---|
| **`robots.txt`** | `https://site.com/robots.txt` | Un `Disallow:` sur le chemin visé |
| **CGU du site** | Mentions légales / *Terms* | Une clause interdisant l'extraction automatisée |
| **RGPD** | Nature des données | Toute **donnée personnelle** (nom, avis signé, email…) |

> ⚖️ **Règles d'or** : ne scrape **jamais** de données personnelles sans base légale ; ne
> surcharge **jamais** un serveur (temporise tes requêtes) ; identifie-toi via un `User-Agent`
> honnête ; privilégie **toujours** une API ou de l'open data si elle existe.

Lire le `robots.txt` en Python avec le module standard `urllib.robotparser` :

```python
from urllib.robotparser import RobotFileParser

rp = RobotFileParser()
rp.set_url("https://www.concurrent-nordretail.example/robots.txt")
rp.read()

url_cible = "https://www.concurrent-nordretail.example/catalogue/chaussures"
mon_agent = "NordRetailBot/1.0 (contact: data@nordretail.example)"

if rp.can_fetch(mon_agent, url_cible):
    print("✅ Autorisé par robots.txt")
else:
    print("⛔ Interdit — on ne scrape pas cette page")
```

---

## 2. Récupérer une page : `requests`

```python
import requests

headers = {
    # Un User-Agent honnête et identifiable : on ne se cache pas.
    "User-Agent": "NordRetailBot/1.0 (contact: data@nordretail.example)"
}

reponse = requests.get(url_cible, headers=headers, timeout=10)
reponse.raise_for_status()   # lève une erreur si status != 200
html = reponse.text
```

Points de vigilance :

- **`timeout`** : sans lui, ton script peut se figer indéfiniment.
- **`raise_for_status()`** : ne travaille jamais sur une page 404 ou 500.
- **Encodage** : `reponse.encoding = "utf-8"` si les accents sont cassés.

---

## 3. Analyser le HTML : `BeautifulSoup`

`BeautifulSoup` transforme le texte HTML en un arbre navigable.

```python
from bs4 import BeautifulSoup

soup = BeautifulSoup(html, "html.parser")

# Un seul élément → .find()
titre = soup.find("h1", class_="product-title").get_text(strip=True)

# Tous les éléments correspondants → .find_all() ou .select() (sélecteurs CSS)
cartes = soup.select("div.product-card")
print(f"{len(cartes)} produits trouvés sur la page")
```

`.select()` accepte les **sélecteurs CSS** (comme en front) — souvent le plus lisible :

| Sélecteur | Cible |
|---|---|
| `div.product-card` | les `<div class="product-card">` |
| `span.price` | les prix |
| `a.product-link` | les liens produit (attribut via `["href"]`) |
| `div.card > h2` | les `<h2>` **enfants directs** d'une carte |

---

## 4. Extraire des données structurées

L'objectif : passer du HTML à une **liste de dictionnaires** (une ligne = un produit).

```python
produits = []

for carte in soup.select("div.product-card"):
    nom = carte.select_one("h2.product-title").get_text(strip=True)

    prix_brut = carte.select_one("span.price").get_text(strip=True)  # "24,90 €"
    prix = float(prix_brut.replace("€", "").replace(",", ".").strip())

    lien = carte.select_one("a.product-link")["href"]

    produits.append({"nom": nom, "prix_eur": prix, "url": lien})
```

> 💡 **Nettoyage à la source** : un prix web arrive **toujours** en texte (`"24,90 €"`).
> Le convertir en `float` tout de suite évite des heures de galère à l'analyse. Dès que le
> format se complique, on réutilise les
> [expressions régulières](../../01-Fondamentaux/Python/04-Bibliotheque-Standard/).

---

## 5. Gérer la pagination (plusieurs pages)

Un catalogue tient rarement sur une page. On boucle en **temporisant** entre chaque requête.

```python
import time

def scraper_catalogue(base_url, nb_pages, headers):
    tous_produits = []
    for page in range(1, nb_pages + 1):
        url = f"{base_url}?page={page}"
        reponse = requests.get(url, headers=headers, timeout=10)
        reponse.raise_for_status()

        soup = BeautifulSoup(reponse.text, "html.parser")
        for carte in soup.select("div.product-card"):
            nom = carte.select_one("h2.product-title").get_text(strip=True)
            prix = carte.select_one("span.price").get_text(strip=True)
            tous_produits.append({"page": page, "nom": nom, "prix": prix})

        time.sleep(2)   # ⏳ politesse : 2 s entre 2 requêtes pour ne pas surcharger le serveur
    return tous_produits
```

Le `time.sleep(2)` n'est pas une option : sans lui, tu envoies des centaines de requêtes par
seconde → tu ressembles à une attaque et tu te fais **bloquer** (voire poursuivre).

---

## 6. Vers l'analyse : produire un DataFrame propre

```python
import pandas as pd

df = pd.DataFrame(produits)
df["prix_eur"] = pd.to_numeric(df["prix_eur"], errors="coerce")
df = df.drop_duplicates(subset="url").dropna(subset=["prix_eur"])

df.to_csv("prix_concurrents.csv", index=False)
print(df.describe())
```

Le résultat rejoint directement le pipeline habituel :
[nettoyage](../16-Nettoyage-Donnees/) → [EDA](../04-Analyse-Exploratoire-EDA/) → dashboard.

---

## À retenir

- Le scraping est un **dernier recours** : API > open data > scraping.
- **Trois feux verts obligatoires** avant de coder : `robots.txt`, CGU, RGPD.
- `requests` récupère, `BeautifulSoup` analyse, Pandas structure.
- **Temporise** (`time.sleep`) et **identifie-toi** (`User-Agent`) : un scraper poli ne se fait pas bloquer.
- Nettoie **à l'extraction** (texte → nombre) pour livrer un DataFrame exploitable.

## Pour aller plus loin

- **`Scrapy`** : framework complet pour du scraping à grande échelle (spiders, pipelines).
- **Sites dynamiques** (JavaScript) : `Selenium` ou `Playwright` quand le contenu est chargé côté client.
- **Brief associé** : [API & Scraping](../../99-Brief/Data-Engineer/API-Scraping/BRIEF_API_SCRAPING.md).
