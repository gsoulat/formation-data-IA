# Kit de démarrage — Référentiel TVA Meridian Distribution

## Le jeu de données

`data/numeros_tva.csv` et `data/numeros_tva.xlsx` contiennent **les mêmes 10 000 lignes**.
Les deux formats sont fournis volontairement : comparez-les avant de choisir.

| Colonne | Description |
|---|---|
| `id` | identifiant de ligne, 1 à 10 000 |
| `raison_sociale` | nom du client tel qu'enregistré |
| `pays_declare` | pays saisi dans le CRM — **pas toujours cohérent avec le numéro** |
| `numero_tva` | le numéro **tel qu'il a été saisi**, sans aucun nettoyage |
| `date_saisie` | date d'entrée dans le référentiel |
| `source_saisie` | canal d'origine : `crm`, `import_fournisseur`, `saisie_manuelle`, `portail_client`, `reprise_erp` |

Le jeu couvre dix États membres. Il mêle des numéros corrects, des numéros mal saisis mais
récupérables, et des numéros réellement fautifs. Les proportions ne vous sont pas données :
les établir fait partie du travail.

## Le module de validation structurelle

`validation_structure.py` vous est fourni. Il couvre les **dix pays présents dans le jeu** et
expose deux fonctions :

```python
from validation_structure import normaliser, valider

normaliser(" fr 27 552032534 ")   # -> "FR27552032534"
valider("FR27552032534")          # -> (True,  "ok")
valider("FR99552032534")          # -> (False, "cle_invalide")
valider("XX12345678")             # -> (False, "pays_non_couvert")
```

Motifs renvoyés : `ok`, `vide`, `trop_court`, `pays_non_couvert`, `cle_invalide`.

**Ils ne sont pas tous de même nature.** Décider quoi faire de chacun fait partie de votre
travail, et ces décisions se répercuteront sur vos chiffres finaux.

Lisez ce module avant de l'utiliser : vous devrez expliquer en soutenance ce que
« structurellement valide » recouvre exactement, et ce que cela permet — ou non — de garantir.

## La base de données

```bash
cp .env.example .env      # facultatif : les valeurs par défaut suffisent
docker compose up -d      # PostgreSQL 16 sur le port 5435
```

Connexion : `postgresql://meridian:meridian@localhost:5435/tva`

Le port 5435 évite les conflits avec les bases des autres briefs.

## Le service VIES

Public, gratuit, sans inscription :

```
https://ec.europa.eu/taxation_customs/vies/rest-api/ms/{PAYS}/vat/{NUMERO}
```

Exemple à essayer dans un navigateur avant d'écrire du code :
`https://ec.europa.eu/taxation_customs/vies/rest-api/ms/FR/vat/27552032534`

Lisez la réponse **en entier**. Tous les champs ne servent pas à la même chose, et l'un d'eux
vous dira des choses que `isValid` seul ne dit pas.

**Mesurez son temps de réponse avant de bâtir votre campagne dessus**, et faites le calcul
pour l'ensemble du référentiel. Le résultat conditionnera votre architecture.

> **Soyez raisonnable avec ce service.** Il est offert par la Commission européenne et partagé
> par toute l'Union. Temporisez vos appels, ne le sollicitez jamais pour un numéro dont vous
> savez déjà que la structure est fausse, et travaillez sur un échantillon tant que votre code
> n'est pas stabilisé.
