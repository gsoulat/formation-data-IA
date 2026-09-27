# Situation professionnelle — Collecter et exploiter le catalogue d'un libraire concurrent

> Situation de rattachement des mini-briefs Bouquineo (semaine de 5 jours) :
> **Mini-brief 1 — Scraper en profondeur** (J1-J2, active C8 et C11) et
> **Mini-brief 2 — API de restitution** (J3-J5, active C12).
> Champs prêts à coller dans Simplonline.

## Nom

Collecter et exploiter le catalogue d'un libraire concurrent

## Langue

FR

## Métier visé

Data Engineer

## Besoin visé / Problème rencontré  (1973 / 3000)

**Bouquineo** est un libraire en ligne français d'une trentaine de salariés. Son équipe commerciale surveille depuis deux ans les prix d'un concurrent dont la vitrine est publique. La méthode n'a jamais changé : chaque lundi, un assistant ouvre le site, parcourt les pages de résultats et recopie à la main dans un tableur ce qui s'y affiche — titre, prix, note, mention de disponibilité.

Ce relevé ne suffit plus. En comité, la responsable des achats a posé trois questions auxquelles personne n'a su répondre : combien d'exemplaires le concurrent détient-il réellement sur les titres où nous sommes en concurrence, quels titres ses clients commentent-ils vraiment, et comment rapprocher son catalogue du nôtre de façon fiable quand deux livres portent le même titre ?

Le problème n'est pas la bonne volonté de l'assistant, il est structurel. Les informations qui permettraient de répondre n'apparaissent nulle part sur les pages de résultats : elles ne vivent que sur les fiches produit, une par livre, et le catalogue du concurrent en compte un millier. À raison d'une minute par fiche, le relevé manuel demanderait plus de deux jours de travail pour une photographie déjà périmée le lendemain.

S'y ajoute un problème de confiance. Le tableur actuel ne porte aucune date de collecte : personne ne sait dire si un prix a été relevé hier ou le mois dernier, ni ce qui a changé entre deux relevés. Les décisions d'achat se prennent donc sur une donnée dont on ignore l'âge.

L'équipe a besoin d'une collecte **automatisée, datée et reproductible**, qui descende jusqu'aux fiches produit et dépose le résultat dans une base interrogeable. L'enjeu est commercial : identifier les titres sur lesquels le concurrent est en tension pour y positionner une offre, et repérer ceux que ses clients plébiscitent afin d'arbitrer les réassorts. Ce que la direction attend n'est pas un fichier de plus, mais un dispositif que l'on relance quand on veut et dont on sait ce qu'il vaut.

## Description du geste professionnel  (2544 / 3000)

Le Data Engineer commence par cartographier la source avant d'écrire la moindre ligne de production. Il ouvre le site dans l'inspecteur du navigateur, identifie le mécanisme de pagination, repère où vivent les champs manquants et vérifie ce que le fichier `robots.txt` déclare. Il documente ses observations et les contraintes qu'il s'impose.

Il développe ensuite un premier collecteur en **Python**, avec **Requests** et **BeautifulSoup**, qui parcourt les pages de résultats et produit l'inventaire des références ainsi que l'adresse de chaque fiche produit. Il envoie un `User-Agent` explicite qui identifie son organisation, temporise entre deux requêtes et justifie le rythme retenu.

Il écrit alors le collecteur de fiches, qui constitue le cœur de la mission : un millier de requêtes successives. Il extrait de chaque page les champs absents des listes — identifiant unique, stock réel, nombre d'avis, description, catégorie — en tenant compte de leur encodage réel, certaines valeurs n'étant pas du texte mais des classes CSS. Il vérifie ses premières extractions contre la page affichée dans le navigateur avant de passer à l'échelle.

Il conçoit la reprise sur incident, car à cette volumétrie une interruption est probable : il écrit les résultats au fil de l'eau, relit son propre fichier de sortie au démarrage et saute sans nouvelle requête ce qui est déjà collecté. Il journalise et écarte les fiches en erreur sans faire tomber le lot, et fixe un seuil au-delà duquel il considère que la source a changé.

Il modélise ensuite le schéma cible et crée la base **PostgreSQL** conteneurisée avec **Docker**, en retenant comme clé l'identifiant stable de la source plutôt que le titre. Il écrit le script de chargement de sorte qu'une seconde exécution mette à jour les lignes existantes sans jamais en dupliquer.

Il rédige enfin les requêtes **SQL** qui répondent aux questions de l'équipe commerciale, contrôle la cohérence de ce qu'il a collecté, et signale les champs dont les valeurs se révèlent redondantes ou constantes plutôt que de les présenter comme exploitables. Il versionne l'ensemble sous **Git** et documente le lancement du dispositif depuis zéro.

Il rend enfin le jeu exploitable par le reste de l'organisation : il expose les données collectées via une **API REST** documentée, en contrôlant les accès et en cadrant ce que chaque consommateur peut interroger, afin que l'équipe commerciale et les autres composants du système d'information s'appuient sur une source unique plutôt que sur des copies de fichiers.

## Compétences visées (5)

- **C8.** Automatiser l'extraction de données depuis un service web, une page web (scraping), un fichier de données, une base de données et un système big data en programmant le script adapté afin de pérenniser la collecte des données nécessaires au projet.
- **C9.** Développer des requêtes de type SQL d'extraction des données depuis un système de gestion de base de données et un système big data en appliquant le langage de requête propre au système afin de préparer la collecte des données nécessaires au projet.
- **C10.** Développer des règles d'agrégation de données issues de différentes sources en programmant, sous forme de script, la suppression des entrées corrompues et en programmant l'homogénéisation des formats des données afin de préparer le stockage du jeu de données final.
- **C11.** Créer une base de données en définissant le schéma de données et en paramétrant le système de gestion choisi afin de stocker le jeu de données final et d'en permettre l'exploitation.
- **C12.** Partager le jeu de données en développant une API REST ou en configurant un accès direct afin de permettre l'exploitation du jeu de données par les autres composants du projet.

## Niveaux activés par mini-brief

— Mini-brief 1, Scraper en profondeur (J1-J2) : C8 niveau 3 TRANSPOSER, C11 niveau 2 ADAPTER
— Mini-brief 2, API de restitution (J3-J5) : C12, niveau à fixer dans ce brief

C9 et C10 sont portées par la situation et exercées en J2 (requêtes de restitution, décodage
et homogénéisation des champs). Elles ne sont pas évaluées par le mini-brief 1, dont le
périmètre est volontairement resserré sur deux compétences.
