# Champs Simplonline — Mini-brief 1 : Scraper en profondeur

> Version de publication, adaptée aux contraintes de rendu Simplonline :
> aucun tableau markdown, aucun underscore hors backticks, aucun ASCII art.
> Le brief complet reste `BRIEF_SCRAPING.md` (rendu GitHub).

## Compétences et niveaux

— C8. Automatiser l'extraction de données depuis une page web (scraping) → Niveau 3, TRANSPOSER
— C11. Créer une base de données → Niveau 2, ADAPTER

## Titre  (76 / 100)

Mini-brief 1 : Scraper en profondeur — le catalogue détaillé d'un concurrent

## Description rapide  (624 / 900)

Bouquineo, libraire en ligne, surveille le catalogue d'un concurrent mais ne relève que ce qu'affichent ses pages de liste. Les informations qui manquent — stock réel, identifiant unique, nombre d'avis — ne vivent que sur les fiches produit, une par livre. Le catalogue en compte mille.

Vous écrivez le collecteur qui va les chercher, puis vous chargez le résultat dans PostgreSQL. La difficulté n'est pas le sélecteur CSS, elle est le volume : à mille requêtes, une interruption n'est plus hypothétique. Votre script doit reprendre où il s'est arrêté plutôt que repartir de zéro, et un rechargement ne doit rien dupliquer.

## Contexte  (3333 / 6000)

— Durée : 2 jours (14 heures), J1 et J2 d'une semaine de 5 jours
— Niveau : Débutant-Intermédiaire
— Modalité : Individuel
— Technologies : Python (Requests, BeautifulSoup), PostgreSQL, Docker, Git
— Prérequis : Cours Python et Cours Docker (liens en Ressources)
— Suite : Mini-brief 2, API de restitution, enchaîné sur J3 à J5 de la même semaine
— Données : 100 % réelles, collectées sur un bac à sable légal conçu pour l'entraînement

**Bouquineo** est un libraire en ligne français. Son équipe commerciale suit les prix d'un concurrent dont la vitrine est publique, et jusqu'ici elle se contente de relever ce qui s'affiche sur les pages de liste : titre, prix, note, disponibilité.

Ça ne suffit plus. En réunion, la responsable des achats a posé trois questions auxquelles personne n'a su répondre : **combien d'exemplaires** le concurrent a-t-il réellement en stock sur les titres où nous sommes en concurrence, quels titres sont **réellement commentés** par ses clients, et comment **rapprocher son catalogue du nôtre** de façon fiable quand deux livres portent le même titre ?

Ces trois informations existent, mais **aucune n'est sur les pages de liste**. Elles ne sont que sur les fiches produit, une par livre. Le catalogue en compte mille.

**La question centrale**, à laquelle tout votre travail doit permettre de répondre :

**« Sur quels titres le concurrent est-il en rupture ou en stock faible, et lesquels sont les mieux notés de son catalogue ? »**

**Ce qui rend ce mini-brief différent d'un exercice de scraping**

Vous avez peut-être déjà scrapé une page de liste. Le saut ici n'est pas dans la difficulté d'un sélecteur, il est dans le **volume et la durée** : une page de liste se récupère en une requête, mille fiches produit en demandent mille. Tout ce qui était négligeable à l'échelle de cinquante requêtes devient structurant à mille.

Le site est un bac à sable légal, conçu pour l'entraînement, sans authentification ni protection anti-robot. Cela ne vous dispense de rien : vous vous comporterez comme si le site appartenait à quelqu'un, parce que ce sera le cas la prochaine fois.

Quatre pièges sont posés dans les pages. Ils ne sont pas signalés davantage, à vous de les rencontrer :

— **La note n'est pas un texte.** Elle est encodée dans une classe CSS (`class="star-rating Three"`). Un scraper qui cherche un chiffre dans le texte ne trouvera jamais rien, et ne lèvera aucune erreur.
— **La page de liste ment par omission.** Elle affiche `In stock`, sans plus. La fiche produit, elle, indique `In stock (22 available)`. Si vous vous arrêtez à la liste, vous ne pourrez pas répondre à la question centrale.
— **Deux champs de prix, une taxe, et une surprise.** Les fiches exposent un prix hors taxe, un prix TTC et un montant de taxe. Regardez leurs valeurs sur une dizaine de livres avant de bâtir quoi que ce soit dessus, et dites dans votre documentation ce que vous en concluez.
— **Le titre n'est pas une clé.** Les fiches portent un identifiant `UPC`. Demandez-vous lequel des deux vous servira à reconnaître un livre déjà collecté.

**Ce qui vous est fourni**

Le point d'entrée, et rien d'autre : **https://books.toscrape.com**

1 000 livres, 50 catégories, 50 pages de liste de 20 livres, HTML statique, pas d'authentification. Aucun script n'est fourni : c'est le sujet du mini-brief.

## Modalités pédagogiques  (4069 / 6000)

Travail individuel sur 2 jours. L'entraide est encouragée, mais chacun rend son code et doit pouvoir l'expliquer.

**Règle des 2 heures.** Bloqué plus de deux heures sur le même point ? Demandez un indice. Notez le blocage et sa résolution dans votre journal de bord, c'est un livrable.

**Phase 1 — Reconnaissance et collecte des pages de liste (J1)**

Aucun script de production le matin. Ouvrez le site dans l'inspecteur du navigateur et cartographiez-le : comment passe-t-on d'une page de liste à la suivante, l'URL est-elle prévisible ou faut-il suivre un lien « next » ? Combien de pages au total, et le site annonce-t-il quelque part son nombre de résultats ? Où se trouve le lien vers la fiche d'un livre, et l'URL qu'il porte est-elle absolue ou relative — que se passe-t-il si vous la concaténez naïvement ?

Regardez aussi `https://books.toscrape.com/robots.txt` et dites dans votre documentation ce qu'il autorise. Puis ouvrez deux ou trois fiches produit et repérez où vivent les champs qui vous manquent.

L'après-midi, écrivez le **collecteur de pages de liste** : il parcourt les 50 pages et produit, pour chaque livre, au minimum son titre, son prix, sa note et **l'URL de sa fiche**. Cette dernière est le carburant de la Phase 2 — sans elle vous ne pourrez rien faire demain.

Envoyez un `User-Agent` explicite qui vous identifie, et temporisez entre deux requêtes. À quel rythme ? Justifiez votre choix : trop lent vous ne finirez pas, trop rapide vous vous comportez en nuisible.

**Résultat testable en fin de J1 :** une commande unique produit un fichier contenant les 1 000 livres avec l'URL de leur fiche, et les logs disent combien de pages ont été parcourues.

**Phase 2 — Collecte des fiches produit et robustesse (J2)**

Mille requêtes, une par fiche. C'est ici que se joue le mini-brief.

Commencez par enrichir un seul livre de bout en bout : UPC, prix hors taxe et TTC, taxe, **stock réel**, nombre d'avis, description, catégorie. Vérifiez la valeur obtenue contre la page affichée dans votre navigateur — pas une fois le script terminé, maintenant.

Passez ensuite à l'échelle, et posez-vous la question qui compte : **que se passe-t-il si votre script casse au 700e livre ?** Repart-il de zéro et refait-il 700 requêtes inutiles au site, ou reprend-il où il s'était arrêté ? Comment savez-vous ce qui est déjà collecté — un fichier de sortie relu au démarrage, un marqueur, une écriture au fil de l'eau plutôt qu'à la fin ? Cette reprise n'est pas un bonus : à mille requêtes, une interruption est probable, pas hypothétique.

Une fiche qui répond en erreur ou qui renvoie une structure inattendue doit être **journalisée et sautée**, jamais faire tomber le lot entier. Combien d'échecs tolérez-vous avant de considérer que le site a changé et qu'il faut s'arrêter ?

Prévoyez un **mode échantillon** (un paramètre limitant le nombre de fiches) : vous en aurez besoin pour la démonstration, et pour ne pas attendre une collecte complète à chaque test.

Chargez enfin le résultat dans **PostgreSQL** : un schéma simple suffit, une table de livres et ce qu'il faut pour les catégories. Choisissez votre clé en connaissance de cause, et faites en sorte qu'une seconde exécution du chargement ne crée pas de doublons.

Terminez par le test qui compte : effacez votre dossier, reclonez votre repo, et déroulez votre README à la lettre.

**Résultat testable en fin de J2 :** le scraper complet se relance par une commande unique ; une interruption en cours de route ne fait pas repartir de zéro ; la base contient les 1 000 livres avec leur stock réel ; deux exécutions successives ne dupliquent rien.

**Socle commun (obligatoire)**

— Le collecteur de pages de liste et le collecteur de fiches produit, fonctionnels et relançables.
— Les 1 000 livres en base PostgreSQL, avec UPC, stock réel, note numérique, nombre d'avis et catégorie.
— La reprise sur interruption, effective et démontrable.
— Temporisation et `User-Agent` explicite, avec le rythme choisi justifié.
— Un mode échantillon paramétrable.
— Un README et un journal de bord.

## Modalités d'évaluation  (610 / 3000)

**Démonstration technique (70 %).** 10 minutes de démonstration + 5 minutes de questions. Vous relancez le scraper en mode échantillon, montrez les logs, interrompez volontairement l'exécution et la relancez pour prouver la reprise, puis interrogez la base pour répondre à la question centrale.

**Revue de code (30 %).** Structure et lisibilité, gestion des erreurs, qualité des logs, README, régularité des commits.

**Validation partielle** : un scraper incomplet mais structuré, versionné et documenté peut valider partiellement les critères. Une démonstration réussie sans documentation ne les valide pas.

## Livrables attendus  (665 / 3000)

À rendre en fin de J2 (lien du repo posté sur la plateforme) :

— Un **repo GitHub public** avec README : description, technologies et justification, installation et lancement depuis zéro, auteur.
— Le **code du scraper**, avec un historique de commits réparti sur les deux jours.
— Le **script de création de la base** et le script de chargement.
— Le **jeu collecté** exporté en CSV ou JSON dans le repo.
— Une **note d'observation** (une demi-page) : ce que vous avez constaté sur les champs de prix et de taxe, et ce que vous en concluez sur la fiabilité de ces champs.
— Le **journal de bord** : blocages rencontrés, ce que vous avez essayé, ce qui a débloqué.

## Critères de performance  (1066 / 3000)

**C8 — Automatiser l'extraction de données (scraping) — Niveau 3, TRANSPOSER**

— Le scraper est fonctionnel : les 1 000 livres sont effectivement collectés, fiches produit comprises.
— Les champs absents des pages de liste — stock réel, UPC, nombre d'avis — sont bien récupérés depuis les fiches.
— La note est correctement convertie en valeur numérique depuis son encodage en classe CSS.
— Le script comporte un point de lancement, la gestion des erreurs et des exceptions, des logs exploitables, une temporisation justifiée et un `User-Agent` explicite.
— La reprise après interruption fonctionne et est démontrée en direct.
— Le code est versionné sur un dépôt public, avec un historique réparti sur la durée du mini-brief.

**C11 — Créer une base de données — Niveau 2, ADAPTER**

— La base se crée depuis un script versionné et le chargement insère effectivement le jeu collecté.
— La clé retenue est justifiée et documentée.
— Une seconde exécution du chargement ne produit aucun doublon.
— Le schéma permet de répondre à la question centrale par une requête.

## Ressources  (846 car.)

— Cours Python : https://github.com/gsoulat/formation-data-IA/tree/main/01-Fondamentaux/Python
— Cours Docker : https://github.com/gsoulat/formation-data-IA/tree/main/02-Containerisation/Docker
— [Mini-brief 2, la suite de celui-ci](https://github.com/gsoulat/formation-data-IA/blob/main/99-Brief/Data-Engineer/Bouquineo-API/BRIEF_API.md)
— Le site à scraper : https://books.toscrape.com
— Son fichier robots.txt : https://books.toscrape.com/robots.txt
— Requests (documentation officielle) : https://requests.readthedocs.io/
— Beautiful Soup 4 (documentation officielle) : https://www.crummy.com/software/BeautifulSoup/bs4/doc/
— Tutoriel français, scraping d'un site web (Python + BeautifulSoup), Realizing Tech, 22 min : https://www.youtube.com/watch?v=XiSFiqY0wIQ
— [Image Docker officielle PostgreSQL](https://hub.docker.com/_/postgres)
