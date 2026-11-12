# Auditer un référentiel de TVA intracommunautaire avec l'API VIES

## Informations

| Critère | Valeur |
|---------|--------|
| **Durée** | 2 jours (14 heures) — **J1 et J2** |
| **Niveau** | Intermédiaire |
| **Modalité** | Individuel |
| **Positionnement** | Brief autonome, à poser en Phase 3 (après [S20 — Extraction multi-sources](../briefs-hebdo/semaine-20-extraction-multisources.md)) |
| **Technologies** | Python 3, pandas, requests, Jupyter Notebook, matplotlib ou seaborn, Git/GitHub |
| **Prérequis** | [Modules et API en Python](../../../01-Fondamentaux/Python/Niveau-1/00-Parcours-Progressif/09-modules-api/) · [Collecte de données](../../../15-Business-Intelligence/14-Collecte-Donnees/) · [Nettoyage des données](../../../15-Business-Intelligence/16-Nettoyage-Donnees/) · [Analyse exploratoire](../../../15-Business-Intelligence/04-Analyse-Exploratoire-EDA/) |
| **Données** | **10 000 numéros de TVA**, fournis dans `starter-kit/data/` |
| **Service externe** | **VIES**, le registre officiel de la Commission européenne (API REST publique, gratuite, sans clé) |

## Compétences visées

Référentiel RNCP 38616 — Concepteur développeur en IA et analyse big data, option Data Analyse.

- **C2.** Créer un système automatisé de collecte de données en intégrant des solutions ETL et/ou en développant des scripts informatiques en Python ou SQL pour une agrégation rapide et exacte des données correspondant aux besoins métier.
  → **Niveau 2 — ADAPTER.** Vous adaptez ce que vous savez de `requests` à un **service web tiers** lent, soumis à quota et sujet à indisponibilités. Aucun script de collecte n'est fourni.
- **C3.** Développer des stratégies de nettoyage de données, en analysant le contexte spécifique des données pour assurer un traitement approprié et sécurisé des données qui réponde aux besoins métier de l'entreprise.
  → **Niveau 2 — ADAPTER.** Le module de validation structurelle vous est **fourni** : vous l'intégrez et décidez quoi faire de chaque motif de rejet, vous ne réécrivez pas les algorithmes.
- **C5.** Mener des analyses exploratoires en calculant des techniques statistiques descriptives pour comprendre la distribution des données et écarter les valeurs anormales.
  → **Niveau 3 — TRANSPOSER.** Aucun plan d'exploration n'est fourni : à vous de choisir quoi mesurer, sur le référentiel comme sur les réponses du service.
- **C6.** Identifier et interpréter des tendances en utilisant des langages de programmation et/ou des outils métiers adaptés pour comprendre finement le contexte et la nature des données analysées.
  → **Niveau 3 — TRANSPOSER.** Vous devez expliquer **d'où viennent** les erreurs du référentiel, pas seulement les compter.
- **C15.** Présenter les résultats de projets IA et Big Data en adaptant le contenu et la forme aux différentes parties prenantes, y compris les personnes en situation de handicap, en suivant les directives d'accessibilité du WCAG.
  → **Niveau 2 — ADAPTER.** Votre lecteur est une directrice financière, pas un data analyst.

## Contexte

**Meridian Distribution** vend des composants industriels à des entreprises de toute l'Union européenne. Quand le client est assujetti à la TVA dans un autre État membre, la facture part **hors taxe** : c'est le mécanisme d'autoliquidation. Il repose entièrement sur une condition : le numéro de TVA du client doit être **réellement valide au moment de la facturation**.

Le référentiel clients compte **10 000 numéros**, accumulés depuis huit ans par plusieurs canaux qui ne se sont jamais parlé : le CRM, les imports de fournisseurs, la saisie manuelle au comptoir, le portail client, une ancienne reprise d'ERP. Personne ne les a jamais vérifiés.

Le contrôle fiscal de mars a coûté cher. Plusieurs factures avaient été émises hors taxe au bénéfice de numéros qui n'étaient pas valides : l'administration a réclamé la TVA non facturée, majorée. La directrice financière ne vous demande pas un outil, elle vous demande un **état des lieux chiffré et argumenté**, qu'elle présentera au comité de direction. Elle veut savoir où en est le référentiel, d'où viennent les erreurs, et quoi faire maintenant.

> **La question centrale**, à laquelle tout votre travail doit permettre de répondre :
>
> **« Parmi nos 10 000 numéros, lesquels sont valides, lesquels ne le sont pas — et lesquels n'ont pas pu être tranchés ? »**

Le troisième terme n'est pas une facilité de langage. C'est le cœur du sujet.

### Ce qui rend ce brief différent d'un exercice de nettoyage

Un module de **validation structurelle** vous est fourni : il connaît le format et la clé de contrôle des dix pays présents dans le jeu. Recopier dix spécifications nationales consommerait vos deux jours sans rien vous apprendre du métier, alors on vous les donne.

Ce module ne répond qu'à une partie de la question. **Déterminer laquelle, et ce qu'il reste à faire, est le premier travail attendu de vous.** Lisez-le, éprouvez-le, et demandez-vous ce qu'un verdict « valide » de sa part garantit réellement à la direction financière.

L'autre partie de la réponse se trouve dans un registre tenu par la Commission européenne, accessible par une **API REST**. Comment l'interroger, à quel rythme, et que faire de ce qu'elle vous répond : c'est le sujet.

> **Le jeu n'a pas été nettoyé.** Il sort de huit ans de saisies diverses. Attendez-vous à y trouver ce qu'on trouve dans un référentiel réel, et prenez le temps de le regarder avant de bâtir quoi que ce soit dessus : plusieurs de vos chiffres finaux dépendront de décisions prises à cette étape, souvent sans que vous vous en aperceviez.

## Ce qui vous est fourni

- `starter-kit/data/numeros_tva.csv` et `numeros_tva.xlsx` — **10 000 lignes**, mêmes données, deux formats ;
- `starter-kit/validation_structure.py` — la **validation structurelle** des dix pays du jeu, avec `normaliser()` et `valider()`. Lisez-le : vous devrez expliquer en soutenance ce que « structurellement valide » recouvre, et pourquoi cela ne suffit pas ;
- `starter-kit/README.md` — la description des colonnes et l'adresse du service.

Le service VIES est public et gratuit, sans inscription :
`https://ec.europa.eu/taxation_customs/vies/rest-api/ms/{PAYS}/vat/{NUMERO}`

Aucun script d'appel n'est fourni.

## Travail demandé

Travail **individuel sur 2 jours**. L'entraide est encouragée, mais chacun produit ses propres notebooks, son propre script et sa propre note.

> **Règle des 2 heures.** Bloqué plus de deux heures sur le même point ? Demandez un indice. Notez le blocage et sa résolution dans votre journal de bord : c'est un livrable.

> **Ordre imposé.** Explorer, normaliser, dédoublonner, filtrer sur la structure, et **seulement ensuite** interroger l'API. Chaque étape réduit le volume que la suivante doit traiter, et ce raisonnement est précisément ce qu'on évalue.

> **Soyez raisonnable avec le service.** VIES est offert par la Commission européenne et partagé par toute l'Union. Ne l'interrogez jamais pour un numéro dont vous savez déjà qu'il est faux, temporisez vos appels, et travaillez sur un échantillon tant que votre code n'est pas stabilisé.

### Phase 1 — Explorer le référentiel, sans rien corriger (J1 matin)

Ouvrez le jeu et regardez-le avant d'écrire la moindre règle. Votre notebook d'exploration doit permettre de répondre à des questions comme :

- Combien de pays distincts ? Combien de formats différents pour un même pays ?
- Quelle proportion de lignes porte des caractères qui n'ont rien à faire dans un numéro de TVA ?
- Combien de valeurs vides, et sous combien de formes différentes le vide se présente-t-il ?
- Le pays déclaré dans le CRM correspond-il toujours au préfixe du numéro ?
- Le CSV et l'Excel contiennent-ils vraiment la même chose une fois chargés ? Lequel prenez-vous comme source de vérité, et pourquoi ?
- Les canaux de saisie et les périodes de saisie se ressemblent-ils, ou certains sortent-ils du lot ?

Notez ce que vous observez **avant** de décider quoi en faire.

### Phase 2 — Nettoyer, filtrer et chiffrer l'entonnoir (J1 après-midi)

Intégrez le module fourni. Il renvoie pour chaque numéro un verdict et un **motif**. Ces motifs ne sont pas tous de même nature : lisez le code pour comprendre ce que chacun signifie exactement, puis décidez du sort de chaque famille. Certaines décisions feront bouger vos chiffres finaux de plusieurs points : sachez lesquelles, et sachez les défendre.

Décidez ensuite de ce qu'est un **doublon** dans ce référentiel, et comptez-les. Votre définition doit pouvoir s'écrire en une phrase.

Préparez enfin la journée de demain. Appelez le service **à la main** sur une vingtaine de numéros de pays différents et **mesurez son temps de réponse**. Décrivez cette distribution comme vous décririez n'importe quelle variable : centre, dispersion, valeurs extrêmes, différences entre pays. Puis faites le calcul : combien de temps prendrait la vérification de tout le référentiel si l'on appelait le service une fois par ligne ? Combien d'appels votre nettoyage vous a-t-il fait économiser ?

**Résultat attendu en fin de J1 :** un tableau qui va de 10 000 lignes au nombre exact de numéros qui méritent un appel, étape par étape, avec la répartition par motif de rejet et une estimation chiffrée de la durée d'une campagne complète.

### Phase 3 — Interroger l'API VIES (J2 matin)

Commencez par trois appels **à la main** : un numéro que vous savez bon, un dont la clé est fausse, un que vous avez inventé de toutes pièces. **Lisez les réponses en entier** avant d'écrire la moindre boucle. Le service ne se contente pas de dire oui ou non : regardez tous les champs qu'il renvoie et demandez-vous ce que chacun signifie.

Sollicitez-le ensuite plus sérieusement, sur quelques dizaines de numéros d'affilée, et **regardez tout ce qu'il vous répond**, pas seulement le cas passant. Confrontez chaque réponse à ce que vous savez du numéro envoyé. Si l'une d'elles vous paraît contredire ce que vous attendiez, ne la contournez pas : c'est probablement là que se joue le brief.

Écrivez alors votre **script de collecte** :

- un **mode échantillon** paramétrable dès le départ (deux cents numéros suffisent à tout démontrer et coûtent quelques minutes) ;
- une **temporisation** entre les appels ;
- un **fichier de résultats** qui conserve, pour chaque numéro, la réponse obtenue **et sa date** ;
- une relance qui **ne refait pas** les appels déjà faits ;
- un **journal** qui permet de savoir après coup ce qui s'est passé pendant la collecte.

Questions à vous poser : votre échantillon de deux cents numéros représente-t-il le référentiel ? Comment l'avez-vous tiré ? Une fois une réponse obtenue, combien de temps reste-t-elle vraie : un numéro vérifié il y a six mois doit-il être revérifié avant la prochaine facture ?

### Phase 4 — Analyser et restituer (J2 après-midi)

Produisez le **rapport de réconciliation** attendu par la direction financière : valides, invalides, non tranchés, motifs de rejet, doublons. Il doit se régénérer en relançant votre notebook d'analyse, sans manipulation manuelle.

Allez ensuite au-delà du comptage. La direction veut comprendre :

- **D'où viennent les erreurs ?** Comparez les canaux de saisie, les pays, les périodes. Un écart observé est-il assez marqué pour qu'on en tire une conclusion ?
- **Que vaut un chiffre calculé sur un échantillon ?** Si vous n'avez interrogé VIES que sur une partie des numéros, dites ce que vous pouvez en conclure pour l'ensemble, et avec quelle marge.
- **Que faire des numéros non tranchés ?** Proposez une règle de conduite applicable par la facturation.

Restituez le tout dans une **note d'une page** à la directrice financière, illustrée de trois ou quatre graphiques lisibles par tous (pas d'information portée par la seule couleur, textes lisibles une fois agrandis).

Terminez par le test qui compte : effacez votre dossier, reclonez votre dépôt, et déroulez votre README à la lettre.

## Socle commun (obligatoire)

- Notebook d'exploration répondant aux questions de la Phase 1.
- Normalisation appliquée et chaque motif de rejet traité explicitement.
- Définition et comptage des doublons.
- Entonnoir chiffré : de 10 000 lignes au nombre d'appels réellement nécessaires.
- Script de collecte VIES abouti en mode échantillon, avec temporisation, journal, résultats datés et relance sans doublon d'appel.
- Rapport de réconciliation reproductible distinguant valides, invalides et non tranchés.
- Note d'une page à la direction financière, avec graphiques accessibles.
- README et journal de bord.

## Pistes bonus

- Une seconde campagne quelques heures plus tard : les verdicts ont-ils bougé ? Que cela vous apprend-il ?
- Un indicateur de **risque fiscal** : montant de TVA exposé si les numéros invalides étaient facturés hors taxe, à partir d'une hypothèse de chiffre d'affaires moyen par client que vous expliciterez.
- Un tableau de bord Power BI ou Looker Studio branché sur votre fichier de résultats.

## Livrables

À rendre en fin de J2 (lien du dépôt posté sur la plateforme) :

- Un **dépôt GitHub public** avec un README : description du projet, technologies utilisées et pourquoi, instructions de lancement depuis zéro, auteur.
- Le **notebook d'exploration** (Phase 1) et le **notebook d'analyse** (Phases 2 et 4), exécutés de haut en bas sans erreur.
- Le **script de collecte VIES**, avec son mode échantillon et la commande pour le lancer.
- Le **fichier de résultats VIES** issu de votre campagne échantillon, et le **journal** de collecte.
- Le **rapport de réconciliation** : valides, invalides, non tranchés, motifs de rejet, doublons — et la façon de le régénérer.
- La **note à la direction financière** (une page, PDF ou Markdown).
- Le **journal de bord** : blocages rencontrés, tentatives, résolutions.
- Un historique de commits réparti sur les deux jours.

## Évaluation

**Démonstration (70 %).** 10 minutes de présentation et 5 minutes de questions. Vous présentez votre entonnoir chiffré, lancez une campagne en mode échantillon, l'interrompez puis la relancez pour prouver qu'aucun appel n'est refait, montrez comment un numéro non tranché est classé dans vos résultats, puis présentez votre note comme vous le feriez devant la directrice financière.

**Revue des livrables (30 %).** Lisibilité et reproductibilité des notebooks, gestion des erreurs du script, qualité du journal, rigueur du rapport, accessibilité des graphiques, README, régularité des commits.

> **Validation partielle** : un travail incomplet mais structuré, versionné et documenté peut valider partiellement. Une démonstration réussie sans documentation ne valide pas les critères documentaires.

## Critères de performance

### C2 — Collecte automatisée depuis l'API

- Le script de collecte fonctionne et une campagne échantillon aboutit sur le volume annoncé.
- L'échantillon est paramétrable et son mode de tirage est justifié.
- Les erreurs du service sont détectées, journalisées et traitées. **Aucune ligne n'est déclarée invalide sans preuve** : un défaut du service n'est pas un défaut du numéro, et confondre les deux fait facturer avec TVA un client qui avait droit à l'exonération.
- Chaque résultat est stocké avec sa date ; une relance ne refait pas les appels déjà faits.
- Les appels sont temporisés.

### C3 — Nettoyage et fiabilisation

- La normalisation est appliquée : un numéro affecté d'un simple bruit de saisie n'est pas compté comme invalide.
- Chaque motif de rejet du module fourni reçoit un traitement explicite et documenté.
- La source de vérité (CSV ou Excel) est choisie et justifiée.
- Les doublons sont détectés et leur définition est justifiée.

### C5 — Analyse exploratoire

- Les caractéristiques du référentiel (pays, formats, vides, canaux) sont décrites chiffres à l'appui.
- Le temps de réponse du service est mesuré et décrit par des statistiques adaptées (centre, dispersion, valeurs extrêmes).
- L'entonnoir est chiffré étape par étape, et le gain en nombre d'appels est exprimé.

### C6 — Interprétation des tendances

- Le taux d'erreur est comparé selon au moins deux dimensions (canal, pays, période) et les écarts sont interprétés.
- Les limites des conclusions tirées d'un échantillon sont explicitées.
- Les graphiques respectent les critères WCAG 1.4.1 (la couleur n'est pas le seul vecteur d'information) et 1.4.4 (texte redimensionnable sans perte).

### C15 — Restitution

- La note tient sur une page et répond à la question centrale avec les trois catégories.
- Le vocabulaire est adapté à une lectrice non technique, sans perdre en exactitude.
- La note formule des recommandations actionnables, dont une règle de conduite pour les numéros non tranchés et une durée de validité d'un verdict.

## Ressources

- VIES — vérification en ligne : https://ec.europa.eu/taxation_customs/vies/
- VIES — exemple d'appel REST : https://ec.europa.eu/taxation_customs/vies/rest-api/ms/FR/vat/27552032534
- Commission européenne — TVA intracommunautaire : https://taxation-customs.ec.europa.eu/taxation/vat_en
- Formats nationaux des numéros de TVA : https://taxation-customs.ec.europa.eu/vat-identification-numbers_en
- Requests : https://requests.readthedocs.io/ · pandas : https://pandas.pydata.org/docs/
- WCAG 2.1 — usage de la couleur (1.4.1) : https://www.w3.org/WAI/WCAG21/Understanding/use-of-color.html
