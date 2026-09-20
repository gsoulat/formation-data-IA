# Brief B02 — Portrait statistique d'un territoire : indicateurs, dispersion et pièges de la moyenne

## Informations

| | |
|---|---|
| **Semaine** | S2 · 21–25 sept 2026 · 5 jours · Guillaume |
| **Modalité · Évaluation** | Binôme · Formatif |
| **Compétences visées** | C3.1 · C4.2 · C4.5 |

## Description

Un cabinet d'études doit livrer un portrait socio-économique des communes des Hauts-de-France. Le brouillon rendu par un stagiaire annonce « un revenu moyen de 22 400 € » et conclut que le territoire se porte bien. Votre travail : vérifier si cette phrase veut dire quelque chose.

## Contexte

Le cabinet Orion Études a été retenu par une agence de développement économique pour produire un portrait statistique des communes de la région. Le livrable doit servir à orienter des aides publiques : les communes les plus fragiles recevront un accompagnement renforcé.

Un stagiaire a produit un premier brouillon. Il tient en une phrase : « Le revenu médian moyen des communes de la région s'établit à 22 400 €, ce qui place le territoire dans la moyenne nationale. » Le directeur d'études est mal à l'aise sans savoir dire pourquoi. Il vous transmet le fichier source de l'INSEE et vous demande de reprendre le travail.

Vous découvrirez rapidement que cette phrase pose au moins trois problèmes. D'abord, elle fait une moyenne de médianes, ce qui n'a pas de sens statistique évident. Ensuite, elle traite de la même façon une commune de 300 habitants et une métropole de 230 000. Enfin et surtout, elle écrase toute l'information utile : si la moitié des communes est à 18 000 € et l'autre à 27 000 €, la moyenne est identique à celle d'un territoire parfaitement homogène — mais la politique publique à mener n'a rien à voir.

Votre mission n'est pas de refaire un tableau de chiffres. Elle est de montrer, avec des indicateurs et des graphiques, ce que la moyenne cache — et de proposer au directeur d'études la phrase qu'il aurait dû lire.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C3.1** — Utiliser les statistiques descriptives afin de modéliser les données et en faire émerger des informations pertinentes *(niveau 1 — imiter)*
- **C4.2** — Utiliser les visualisations descriptives : nuages de points, boîtes à moustache, histogrammes *(niveau 1 — imiter)*
- **C4.5** — Utiliser un tableur pour proposer des croisements de variables *(niveau 1 — imiter)*

## Modalités pédagogiques

**Organisation** : binôme. Un seul dépôt GitHub pour les deux, avec les contributions des deux membres visibles dans l'historique.

**Jour 1 — matin (lancement, 2 h)**. Le formateur joue le directeur d'études. Vous recevez le fichier INSEE et le brouillon du stagiaire. Vous devez d'abord dire, avec vos mots, pourquoi la phrase vous gêne — avant tout apport théorique.

**Jour 1 — après-midi**. Vous tentez de calculer ce que vous pouvez avec le tableur. Vous butez probablement sur la question : quel indicateur choisir ?

**Jour 2 — matin (apport flash, 1 h 30)**. Indicateurs de position (moyenne, médiane, mode) et de dispersion (écart-type, variance, quantiles, étendue), avec leurs fonctions tableur. Construction d'un histogramme et d'un nuage de points. Notion de moyenne pondérée.

**Jours 2 à 4 — production**. Produisez un portrait en quatre volets :
1. **Position** : où se situe le territoire ? Moyenne, médiane, et écart entre les deux — que signifie cet écart ?
2. **Dispersion** : quartiles, écart interquartile, communes extrêmes. Construisez une boîte à moustache.
3. **Pondération** : recalculez l'indicateur en tenant compte de la population. Le résultat change-t-il ? De combien ?
4. **Relation** : construisez un nuage de points entre deux variables de votre choix (par exemple population et revenu). Que voyez-vous ?

**Questions guidantes.** Quand la moyenne et la médiane s'écartent, dans quel sens la distribution est-elle déformée, et qu'est-ce que cela dit du territoire ? Une commune très riche de 200 habitants doit-elle peser autant qu'une ville pauvre de 50 000 dans le portrait ? Si l'écart-type double sans que la moyenne bouge, la politique publique doit-elle changer ? Un nuage de points qui monte prouve-t-il qu'une variable cause l'autre ?

**Jour 4 — après-midi (revue croisée)**. Chaque binôme relit le portrait d'un autre binôme et doit répondre à une seule question : « À la lecture de ce document, saurais-je quelles communes aider en priorité ? »

**Jour 5**. Finalisation, publication, restitution de 8 minutes par binôme. Rétrospective.

## Modalités d'évaluation

Brief **formatif**. Auto-évaluation sur grille, revue croisée entre binômes le jour 4, retour collectif du formateur le jour 5.

Le point d'attention de la semaine n'est pas la justesse des calculs — le tableur les fait — mais la **justesse de l'interprétation**. Un binôme qui calcule correctement dix indicateurs sans savoir dire lequel compte n'a pas atteint l'objectif ; un binôme qui en calcule quatre et explique précisément ce que chacun révèle l'a atteint.

La restitution du jour 5 se termine obligatoirement par la phrase corrigée : celle que le directeur d'études aurait dû lire à la place de celle du stagiaire.

## Données fournies (source exacte)

> Le scénario (cabinet « Orion Études ») est **fictif** ; les **données réelles** support — et sur
> lesquelles porte la correction — sont les revenus des communes du **département du Nord (59)**.

- **Jeu** : Filosofi 2021 — niveau de vie médian par commune (INSEE), rediffusé sur data.gouv.fr.
- **Page** : https://www.data.gouv.fr/datasets/revenu-des-francais-a-la-commune
- **Fichier** : `revenu_des_francais_a_la_commune_2021.csv` (toutes communes) → **filtrer les codes commune commençant par « 59 »** (648 communes).
- **Colonnes utiles** : code commune, libellé, nombre de personnes (≈ population), **médiane du niveau de vie (€)**.
- **Licence** : Licence Ouverte (Etalab).

## Livrables attendus

**Un dépôt GitHub public** par binôme, contenant :

1. `README.md` — description, source INSEE, méthode, les deux auteurs.
2. `portrait.xlsx` — un onglet par volet (position, dispersion, pondération, relation), formules apparentes.
3. `graphiques/` — au minimum un histogramme, une boîte à moustache et un nuage de points, exportés en image et commentés.
4. `note-critique.md` — deux pages maximum : ce que la phrase du stagiaire dissimulait, les indicateurs retenus et pourquoi, la phrase corrigée proposée au directeur d'études.

**Restitution orale** : 8 minutes par binôme.

## Critères de performance

**C3.1 — Statistiques descriptives**
• Moyenne, médiane, écart-type et quartiles sont calculés et présents dans le classeur.
• L'écart entre moyenne et médiane est explicitement commenté en termes de forme de distribution.
• Une moyenne pondérée par la population est calculée et comparée à la moyenne simple ; l'écart est chiffré.
• La note critique identifie au moins deux limites de l'indicateur retenu par le stagiaire.

**C4.2 — Visualisations descriptives**
• Un histogramme, une boîte à moustache et un nuage de points sont produits.
• Chaque graphique porte un titre, des axes légendés et une unité.
• Chaque graphique est accompagné d'une phrase disant ce qu'il faut y voir.

**C4.5 — Tableur**
• Les indicateurs sont obtenus par fonctions, non saisis.
• Les quartiles sont calculés par la fonction dédiée et non estimés visuellement.
• Le classeur est navigable : onglets nommés, cellules de résultat identifiables.

## Ressources

- INSEE — dossiers complets par commune : https://www.insee.fr/fr/statistiques
- INSEE — définitions : médiane, quantile, écart-type : https://www.insee.fr/fr/metadonnees/definitions
- Aide Google Sheets — liste des fonctions : https://support.google.com/docs/table/25273
- Microsoft — fonctions statistiques Excel : https://support.microsoft.com/fr-fr/office/fonctions-statistiques-r%C3%A9f%C3%A9rence-624dac86-a375-4435-bc25-76d6df3c5b6f
- Jeu de données (exact) — Revenu des Français à la commune (Filosofi 2021) : https://www.data.gouv.fr/datasets/revenu-des-francais-a-la-commune
