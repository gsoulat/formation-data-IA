# Valider un référentiel de TVA intracommunautaire — API de vérification

## Informations

| Critère | Valeur |
|---------|--------|
| **Durée** | 2 jours (14 heures) — **J1 et J2** |
| **Niveau** | Intermédiaire |
| **Modalité** | Individuel |
| **Technologies** | Python, FastAPI, PostgreSQL, Docker, Git |
| **Prérequis** | [Cours Python](https://github.com/gsoulat/formation-data-IA/tree/main/01-Fondamentaux/Python) + [Cours FastAPI](https://github.com/gsoulat/formation-data-IA/tree/main/01-Fondamentaux/Python/08-FastAPI) + [Cours Docker](https://github.com/gsoulat/formation-data-IA/tree/main/02-Containerisation/Docker) |
| **Données** | **10 000 numéros**, fournis dans `starter-kit/data/` |
| **Service externe** | **VIES**, le registre officiel de la Commission européenne |

## Compétences visées

- **C8.** Automatiser l'extraction de données depuis un service web, une page web (scraping), un fichier de données, une base de données et un système big data en programmant le script adapté afin de pérenniser la collecte des données nécessaires au projet.
  → **Niveau 3 — TRANSPOSER.** La facette évaluée est l'appel d'un **service web tiers**, lent, soumis à quota et sujet à indisponibilités. Aucun client n'est fourni : c'est le cœur du brief.
- **C10.** Développer des règles d'agrégation de données issues de différentes sources en programmant, sous forme de script, la suppression des entrées corrompues et en programmant l'homogénéisation des formats des données afin de préparer le stockage du jeu de données final.
  → **Niveau 2 — ADAPTER.** Le module de validation structurelle vous est **fourni** : vous l'intégrez et décidez quoi faire de chaque motif de rejet, vous ne réécrivez pas les algorithmes.
- **C11.** Créer une base de données en définissant le schéma de données et en paramétrant le système de gestion choisi afin de stocker le jeu de données final et d'en permettre l'exploitation.
  → **Niveau 2 — ADAPTER.**
- **C12.** Partager le jeu de données en développant une API REST ou en configurant un accès direct afin de permettre l'exploitation du jeu de données par les autres composants du projet.
  → **Niveau 2 — ADAPTER.** L'enjeu est le **contrat de réponse**, pas la technique FastAPI.

## Contexte

**Meridian Distribution** vend des composants industriels à des entreprises de toute l'Union européenne. Quand le client est assujetti à la TVA dans un autre État membre, la facture part **hors taxe** : c'est le mécanisme d'autoliquidation, et il repose entièrement sur une condition — que le numéro de TVA du client soit **réellement valide au moment de la facturation**.

Le référentiel clients compte **10 000 numéros**, accumulés depuis huit ans par trois canaux qui ne se sont jamais parlé : le CRM, les imports de fournisseurs, et la saisie manuelle au comptoir. Personne ne les a jamais vérifiés.

Le contrôle fiscal de mars a coûté cher. Plusieurs factures avaient été émises hors taxe au bénéfice de numéros qui n'étaient pas valides : l'administration a réclamé la TVA non facturée, majorée. La direction financière veut deux choses. Savoir **où en est le référentiel**, et disposer d'un **service que la facturation appellera avant chaque émission** hors taxe.

> **La question centrale**, à laquelle tout votre travail doit permettre de répondre :
>
> **« Parmi nos 10 000 numéros, lesquels sont valides, lesquels ne le sont pas — et lesquels n'ont pas pu être tranchés ? »**

Le troisième terme n'est pas une facilité de langage. Il est le cœur du sujet.

### Ce qui rend ce brief différent d'un exercice de validation

Un module de **validation structurelle** vous est fourni : il connaît le format et la clé de contrôle des dix pays présents dans le jeu. Recopier dix spécifications nationales consommerait vos deux jours sans rien vous apprendre du métier, alors on vous les donne.

Ce module ne répond qu'à une partie de la question. **Déterminer laquelle, et ce qu'il reste à faire, est le premier travail attendu de vous.** Lisez-le, éprouvez-le, et demandez-vous ce qu'un verdict « valide » de sa part garantit réellement à la direction financière.

Le reste — comment obtenir la réponse qui manque, auprès de qui, et à quelles conditions — n'est décrit nulle part dans ce brief. C'est le sujet.

> **Le jeu n'a pas été nettoyé.** Il sort de huit ans de CRM, d'imports fournisseurs et de saisie au comptoir. Attendez-vous à y trouver ce qu'on trouve dans un référentiel réel, et prenez le temps de le regarder avant de bâtir quoi que ce soit dessus : plusieurs de vos chiffres finaux dépendront de décisions que vous aurez prises à cette étape, souvent sans vous en apercevoir.

## Ce qui vous est fourni

- `starter-kit/data/numeros_tva.csv` et `numeros_tva.xlsx` — **10 000 lignes**, mêmes données ;
- `starter-kit/validation_structure.py` — la **validation structurelle** des dix pays du jeu, avec `normaliser()` et `valider()`. Lisez-le : vous devrez expliquer en soutenance ce que « structurellement valide » recouvre, et pourquoi cela ne suffit pas ;
- `starter-kit/docker-compose.yml` — PostgreSQL, pour ne pas y passer la matinée.

Le service VIES est public et gratuit, sans inscription :
`https://ec.europa.eu/taxation_customs/vies/rest-api/ms/{PAYS}/vat/{NUMERO}`

Aucun client VIES, aucun schéma de base et aucune API ne sont fournis : c'est le sujet du brief.

## Travail demandé

Travail individuel sur 2 jours.

> **Règle des 2 heures.** Bloqué plus de deux heures sur le même point ? Demandez un indice. Notez le blocage et sa résolution dans votre journal de bord, c'est un livrable.

> **Ordre imposé.** Normaliser, dédupliquer, filtrer sur la structure, et **seulement ensuite** interroger VIES. Chaque étape réduit le volume que la suivante doit traiter — et ce raisonnement est précisément ce qu'on évalue.

### Phase 1 — Cadrage, réduction et chargement (J1)

Commencez sans écrire de code de production. Ouvrez le jeu et regardez-le : combien de pays distincts, combien de formats différents pour un même pays, quelle proportion de lignes portent des caractères qui n'ont rien à faire dans un numéro de TVA ? Combien de valeurs vides, et sous combien de formes différentes le vide se présente-t-il ?

Intégrez ensuite le module fourni. Il renvoie pour chaque numéro un verdict et un **motif**. Ces motifs ne sont pas tous de même nature : lisez le code pour comprendre ce que chacun signifie exactement, puis décidez du sort de chaque famille. Certaines décisions changeront vos chiffres finaux de plusieurs points — sachez lesquelles, et sachez les défendre.

Attaquez alors la préparation de la journée de demain. Vous devrez interroger un service distant, et vous n'aurez pas le loisir de le faire une fois par ligne de fichier : mesurez d'abord son temps de réponse sur quelques appels, faites le calcul pour l'ensemble du référentiel, et tirez-en les conséquences. Ce que vous ferez pour réduire ce volume, et de combien vous le réduisez, est un livrable.

Chargez enfin le référentiel dans **PostgreSQL**. Le schéma doit distinguer ce que vous avez reçu de ce que vous en avez déduit : la valeur brute telle que saisie, la valeur normalisée, le verdict structurel et son motif. Un rechargement ne doit pas dupliquer les lignes.

**Résultat testable en fin de J1 :** une commande unique charge les 10 000 lignes, la base porte le verdict structurel de chacune, une requête donne la répartition par motif, et vous savez dire combien d'appels VIES vous avez évités.

### Phase 2 — Vérification en ligne et API (J2)

Commencez par appeler VIES **à la main** sur trois numéros — un que vous savez bon, un dont la clé est fausse, un que vous avez inventé — et **lisez les réponses en entier** avant d'écrire la moindre boucle. Le service ne se contente pas de dire oui ou non ; regardez tous les champs qu'il renvoie et demandez-vous ce que chacun signifie.

Sollicitez-le ensuite sérieusement, sur quelques dizaines de numéros d'affilée, et **regardez tout ce qu'il vous répond** — pas seulement le cas passant. Confrontez chaque réponse à ce que vous savez du numéro envoyé. Si l'une d'elles vous paraît contredire ce que vous attendiez, ne la contournez pas : c'est probablement là que se joue le brief. Votre modèle de données devra rendre compte de tout ce que le service peut vous dire, et de tout ce qu'il peut ne pas vous dire.

Écrivez ensuite la campagne de vérification. Prévoyez un **mode échantillon** dès le départ : deux cents numéros suffisent à tout démontrer et coûtent quelques minutes, là où le référentiel entier demanderait des heures. Temporisez, journalisez, et faites en sorte qu'une campagne interrompue ne reparte pas de zéro. Une fois une réponse obtenue, combien de temps reste-t-elle vraie — un numéro vérifié il y a six mois doit-il être revérifié avant la prochaine facture ?

L'après-midi, exposez une **API REST** que la facturation appellera avant chaque émission hors taxe. Le contrat de réponse est le vrai sujet. Un appelant doit toujours savoir **trois choses** : le verdict, d'où il sort — une réponse fraîche de VIES ou une valeur déjà connue — et de quand il date. Une API qui renvoie `true` sans dire que l'information a huit mois expose son appelant au même redressement qu'avant. Et que répondez-vous quand VIES est injoignable et que vous n'avez rien en mémoire ?

Terminez par le rapport de réconciliation attendu par la direction financière, puis par le test qui compte : effacez votre dossier, reclonez votre dépôt, et déroulez votre README à la lettre.

**Résultat testable en fin de J2 :** une campagne s'exécute en mode échantillon, chaque ligne du référentiel porte un verdict que vous savez justifier, une relance ne refait pas les appels déjà faits, l'API renvoie verdict, origine et fraîcheur, et le rapport se régénère par une commande.

## Socle commun (obligatoire)

- Normalisation appliquée et motifs de rejet traités explicitement.
- Les 10 000 lignes en base PostgreSQL, avec verdict structurel et motif.
- Réduction chiffrée du nombre d'appels VIES avant toute vérification en ligne.
- Vérification en ligne aboutie, avec temporisation, journalisation et reprise après interruption.
- Un **mode échantillon** paramétrable.
- API REST exposant verdict, origine et fraîcheur.
- Rapport de réconciliation reproductible, README et journal de bord.

## Livrables

À rendre en fin de J2 (lien du repo posté sur la plateforme) :

- Un **repo GitHub public** avec README : description, technologies et justification, lancement depuis zéro, auteur.
- Le **code** du pipeline et de l'API, avec un historique de commits réparti sur les deux jours.
- Le **rapport de réconciliation** : valides, invalides, indéterminés, motifs de rejet, doublons — et la commande qui le produit.
- Une **note d'architecture** d'une page : comment vous avez réduit les appels à VIES et de combien, quelle durée de validité vous accordez à un verdict, et ce que vous faites des indéterminés.
- Le **journal de bord** : blocages rencontrés, tentatives, résolutions.

## Évaluation

**Démonstration technique (70 %).** 10 minutes de démonstration + 5 minutes de questions. Vous montrez la répartition des verdicts structurels, lancez une campagne VIES en mode échantillon, provoquez une interruption et la relancez pour prouver la reprise, appelez votre API sur un numéro valide et un invalide, et commentez la fraîcheur affichée.

**Revue de code et de conception (30 %).** Structure, gestion des erreurs, qualité des logs, modèle de données, README, régularité des commits.

> **Validation partielle** : un pipeline incomplet mais structuré, versionné et documenté peut valider partiellement. Une démonstration réussie sans documentation ne valide pas les critères documentaires.

## Critères de validation

### Automatiser l'extraction depuis un service web

- Le client VIES est fonctionnel et une campagne aboutit sur le volume annoncé.
- Le modèle de verdicts rend compte de **tous** les cas que le service renvoie, y compris ceux où il ne permet pas de conclure. **Aucune ligne n'est déclarée invalide sans preuve** : un défaut du service n'est pas un défaut du numéro, et confondre les deux fait facturer avec TVA un client qui avait droit à l'exonération.
- Temporisation, journalisation et reprise après interruption sont effectives et démontrées.
- Le nombre d'appels réseau est réduit par rapport à une approche naïve, et cette réduction est chiffrée et justifiée.

### Homogénéiser et fiabiliser le jeu

- La normalisation est appliquée : les numéros affectés d'un simple bruit de saisie ne sont pas comptés comme invalides.
- Chaque motif de rejet du module fourni reçoit un traitement explicite et documenté.
- Les doublons sont détectés et leur définition est justifiée.
- Le rapport de réconciliation est reproductible par une commande.

### Stocker et exposer

- La base se crée depuis un script versionné ; un rechargement ne produit aucun doublon.
- Le schéma distingue la valeur brute reçue, la valeur normalisée et les verdicts.
- Le verdict en ligne est stocké avec sa date.
- L'API expose pour chaque verdict son origine et sa fraîcheur, sa documentation OpenAPI est accessible, et toute la pile se lance par une commande unique.

## Ressources

- [Cours Python](https://github.com/gsoulat/formation-data-IA/tree/main/01-Fondamentaux/Python) · [Cours FastAPI](https://github.com/gsoulat/formation-data-IA/tree/main/01-Fondamentaux/Python/08-FastAPI) · [Cours Docker](https://github.com/gsoulat/formation-data-IA/tree/main/02-Containerisation/Docker)
- VIES — vérification en ligne : https://ec.europa.eu/taxation_customs/vies/
- VIES — exemple d'appel REST : https://ec.europa.eu/taxation_customs/vies/rest-api/ms/FR/vat/27552032534
- Commission européenne — TVA intracommunautaire : https://taxation-customs.ec.europa.eu/taxation/vat_en
- Formats nationaux des numéros de TVA : https://taxation-customs.ec.europa.eu/vat-identification-numbers_en
- Requests : https://requests.readthedocs.io/ · FastAPI : https://fastapi.tiangolo.com/
