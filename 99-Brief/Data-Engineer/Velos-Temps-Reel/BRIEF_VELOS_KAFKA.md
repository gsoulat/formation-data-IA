# Brief : Vélos en libre-service en temps réel — pipeline Kafka sur deux flux publics réels

## Informations

| Critère | Valeur |
|---------|--------|
| **Durée** | 5 jours (35 heures) |
| **Niveau** | Intermédiaire |
| **Modalité** | Individuel |
| **Technologies** | Apache Kafka (mode KRaft), Python (confluent-kafka, requests), Docker & Docker Compose, PostgreSQL, SQL, Git |
| **Prérequis** | [Cours Python](../../../01-Fondamentaux/Python/) + [Cours SQL](../../../01-Fondamentaux/SQL/) + [Cours Docker](../../../02-Containerisation/Docker/) + [Cours Kafka](../../../06-Data-Engineering/Kafka/) |
| **Données** | **100 % réelles** — deux flux publics en production, aucun générateur d'événements |

## Contexte

### L'entreprise

**Rebalance** est une jeune société de 15 personnes qui vend un service d'aide au **rééquilibrage** des flottes de vélos en libre-service : dire aux exploitants où envoyer leurs camions, et quand. Elle démarre avec deux réseaux pilotes, Paris (Vélib') et Lyon (Vélo'v). Vous êtes le premier data engineer de l'équipe.

### Le problème

Les exploitants réagissent aujourd'hui **après coup** : un usager signale une station vide, un agent y passe, souvent trop tard. Personne ne voit venir la station qui se vide.

Le vrai obstacle technique est là : les données publiques de ces réseaux sont des **instantanés**. À chaque instant, les flux disent combien de vélos sont disponibles *maintenant*, et rien d'autre. Aucun historique n'est publié, nulle part. Impossible donc de calculer une vitesse de vidage, de repérer une station figée depuis six heures, ou d'anticiper quoi que ce soit.

Autrement dit : **l'historique n'existe pas, il faut le fabriquer**. C'est tout l'objet de votre mission — construire la plateforme qui capte ces instantanés au fil de l'eau, en garde la trace, et en déduit les alertes que les exploitants attendent.

La directrice technique a tranché : ce sera une **architecture événementielle** autour d'Apache Kafka, pour que les futurs réseaux se branchent sans réécrire la plateforme.

### La question centrale

Chaque choix technique de la semaine devra pouvoir être justifié par sa contribution à cette question :

> **« Quelles stations vont tomber à sec dans l'heure, et lesquelles sont déjà hors service ? »**

### Les sources de données

Deux réseaux, **deux formats différents** — c'est volontaire, et c'est la réalité du métier.

- **Vélib' Métropole (Paris)** — API Opendatasoft Explore v2.1, publique, sans authentification :
  `https://opendata.paris.fr/api/explore/v2.1/catalog/datasets/velib-disponibilite-en-temps-reel/records`
  Environ **1 500 stations**. Une réponse mélange l'information statique et l'état courant : `stationcode`, `name`, `capacity`, `numbikesavailable`, `numdocksavailable`, `mechanical`, `ebike`, `is_installed`, `is_renting`, `is_returning`, `duedate`, `coordonnees_geo`, `code_insee_commune`.
- **Vélo'v (Lyon)** — flux **GBFS 2.3**, le standard international des vélos en libre-service, publié par la Métropole de Lyon :
  `https://download.data.grandlyon.com/files/rdata/jcd_jcdecaux.jcdvelov/gbfs.json`
  Ce fichier est un **index** : il pointe vers `station_information.json` (le statique : nom, capacité, position) et `station_status.json` (le dynamique : vélos et bornes disponibles, horodatage). Environ 430 stations.
- **Persistance** : PostgreSQL, conteneurisé avec Docker.
- **Bonus haut débit** : Wikimedia EventStreams (`https://stream.wikimedia.org/v2/stream/recentchange`), un vrai flux SSE mondial à plusieurs dizaines de messages par seconde.

### Ce qui rend ce brief différent d'un exercice

Aucun générateur d'événements ne vous est fourni. Vous branchez la plateforme sur **deux flux réellement en production**, avec leurs contraintes réelles :

- **Les deux réseaux ne parlent pas la même langue.** Chez Vélib', `is_renting` vaut la chaîne `"OUI"` ou `"NON"` ; en GBFS, c'est un entier `0`/`1`. Vélib' horodate en ISO 8601 (`duedate`), le GBFS en *epoch* Unix (`last_reported`, `last_updated`). Vélib' livre tout dans un seul enregistrement, le GBFS sépare statique et dynamique en deux fichiers à joindre. Votre plateforme doit absorber les deux sans que le métier ait à savoir lequel est lequel.
- **Le GBFS annonce sa propre fraîcheur.** Le champ `ttl` de `gbfs.json` indique au bout de combien de secondes les données sont considérées périmées. Interroger plus vite que le `ttl` ne rapporte rien de neuf et agresse un service public gratuit. À quelle fréquence sondez-vous, et comment le justifiez-vous ?
- **Les doublons sont inévitables, pas injectés.** Si vous sondez plus vite que le rafraîchissement de la source, vous recevrez deux fois le même état. Votre pipeline doit le supporter sans polluer les agrégats.
- **Une station morte ressemble à une station calme.** Une station dont l'horodatage ne bouge plus depuis des heures est probablement hors service — mais une station de quartier résidentiel à 3 h du matin ne bouge pas non plus. Où placez-vous la frontière ?

### Contraintes techniques

- **Kafka en local via Docker Compose, mode KRaft** (sans ZooKeeper), un seul broker suffit — la stack vous est fournie dans le kit, mais vous devez savoir l'expliquer.
- Producteur, consommateurs et traitements en **Python** ; persistance dans **PostgreSQL**.
- **Prérequis machine** : Docker et Docker Compose installés, environ 4 Go de RAM libres. Vérifiez ce point **dès la première heure** et signalez tout blocage au formateur.
- Le producteur doit rester **poli** : `User-Agent` explicite, fréquence de sondage cohérente avec le `ttl` annoncé, gestion propre des erreurs réseau. Ce sont des services publics gratuits.
- Tout le code est **versionné sur GitHub dès le premier jour**.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **Concevoir l'architecture d'une plateforme de flux** : adapter un pattern publish/subscribe à deux sources hétérogènes, et comparer Kafka à des alternatives au regard des 3V (volumétrie, vitesse, variété) ;
- **Intégrer les composants d'une infrastructure de flux** : comprendre et exploiter une stack Kafka (mode KRaft) + PostgreSQL sous Docker Compose, créer et paramétrer les topics, rédiger une procédure d'installation rejouable ;
- **Transformer un instantané en flux d'événements** : concevoir un producteur qui interroge périodiquement deux API réelles, normalise deux schémas en un format d'événement unique, et publie sur Kafka ;
- **Automatiser la consommation de données en continu** : concevoir seul des consommateurs Python en consumer group, avec gestion des erreurs, des offsets, de l'idempotence et journalisation — **aucun exemple de producteur ni de consommateur n'est fourni** ;
- **Développer des règles d'agrégation** fenêtrées et des règles de détection (station à sec, station hors service) sur un historique que vous avez vous-même constitué.

## Architecture cible

Un pipeline de streaming **publish/subscribe** : un producteur sonde les deux flux publics, normalise les états et les publie sur un broker Kafka ; des groupes de consommateurs lisent ces flux, persistent les états bruts et calculent des agrégats fenêtrés dans PostgreSQL, où une requête SQL rafraîchie fait office de mini-dashboard d'exploitation.

```
     +---------------------------+     +---------------------------+
     |  Vélib' Paris (API ODS)   |     |  Vélo'v Lyon (GBFS 2.3)   |
     |  ~1500 stations           |     |  ~430 stations            |
     |  is_renting = "OUI"/"NON" |     |  is_renting = 0/1         |
     |  duedate = ISO 8601       |     |  last_reported = epoch    |
     +-------------+-------------+     +-------------+-------------+
                   |                                 |
                   +----------------+----------------+
                                    |
              [ PRODUCTEUR PYTHON — sondage périodique ]
              [ normalisation des 2 schémas -> 1 format ]
                                    |
     +------------------------------v------------------------------+
     |              BROKER APACHE KAFKA (mode KRaft)                |
     |                 Docker Compose, mono-broker                  |
     |   +--------------------+      +--------------------------+   |
     |   | topic états station|      |  topic(s) de votre choix |   |
     |   | (partitions, clé)  |      |                          |   |
     |   +--------------------+      +--------------------------+   |
     +------------------------------+------------------------------+
                                    |
                       (consumer groups Python)
                                    |
     +------------------------------v------------------------------+
     |   CONSOMMATEURS PYTHON (erreurs / offsets / idempotence)     |
     |   - persistance des états bruts horodatés                    |
     |   - agrégats fenêtrés + détection (à sec, hors service)      |
     +------------------------------+------------------------------+
                                    |
     +------------------------------v------------------------------+
     |                      PostgreSQL (Docker)                     |
     |    table d'états historisés  +  tables d'agrégats/alertes    |
     +------------------------------+------------------------------+
                                    |
                        (requête SQL rafraîchie)
                                    |
     +------------------------------v------------------------------+
     |  MINI-DASHBOARD D'EXPLOITATION — où envoyer le camion ?      |
     +--------------------------------------------------------------+
```

> Vous produirez votre propre schéma d'architecture **au format image** (draw.io ou équivalent, pas d'ASCII art) à joindre au rendu.

## Données fournies

Le kit de démarrage se trouve dans le dossier [`starter-kit/`](starter-kit/). Il est volontairement minimal :

- `flux.md` — les URL exactes des deux flux et les premières commandes d'exploration ;
- `.env.example` — variables d'environnement d'exemple (aucun secret réel) ;
- `docker-compose.yml` — **une stack Kafka (mode KRaft, mono-broker) + PostgreSQL qui démarre**, avec les commandes de vérification.

Le `docker-compose.yml` est fourni pour une raison précise : monter un broker Kafka n'est pas une compétence évaluée par le référentiel, alors que la conception des topics, la gestion des offsets, l'idempotence et les agrégations le sont. Vous devez en revanche **savoir l'expliquer** — ce sera demandé en soutenance — et vous l'adapterez si vous tentez un bonus.

**Aucun code de producteur ni de consommateur n'est fourni**, et **aucun topic n'est créé** : c'est le sujet du brief.

## Travail demandé

Travail individuel sur 5 jours. L'entraide est encouragée : partagez blocages et astuces sur le canal de la promo, mais chacun conçoit, code et soutient son propre pipeline. Le brief distingue un **socle commun obligatoire** et des **pistes bonus** — un socle solide vaut mieux qu'un bonus bancal.

> **Règle des 2 heures.** Ces flux sont réels et l'infrastructure Kafka est capricieuse. **Bloqué plus de 2 heures sur le même point ? Demandez un indice au formateur.** Notez le blocage et sa résolution dans votre journal de bord, qui fait partie du rendu.

### Phase 1 — Cadrage et exploration des flux (J1)

Aucune ligne de code de pipeline. Interrogez les deux flux à la main, avec `curl` ou dans le navigateur.

Côté Vélib', combien de stations l'API annonce-t-elle, et que vaut `duedate` sur deux appels espacés de dix minutes ? Côté Lyon, ouvrez `gbfs.json` : que contient-il exactement, et où sont réellement les données ? Combien de fichiers devez-vous joindre pour reconstituer une station complète, et sur quelle clé ? Que vaut le `ttl`, et qu'en déduisez-vous pour votre fréquence de sondage ?

Confrontez ensuite les deux schémas champ par champ : quels champs disent la même chose sous des noms et des types différents ? Quel **format d'événement unique** allez-vous en tirer ? C'est la décision structurante de la semaine.

Tranchez aussi la conception des topics : combien, comment les nommer, combien de partitions, et quelle **clé de partitionnement** garantit que les états successifs d'une même station restent ordonnés ? Comparez Kafka à au moins **deux alternatives** (Redpanda, RabbitMQ, service cloud managé…) au regard des besoins de Rebalance.

Formalisez le tout dans un **Kanban public** avec des user stories, et posez un premier **schéma d'architecture**.

Terminez la journée par une **capture manuelle** : enregistrez deux instantanés des deux réseaux à une heure d'intervalle, dans des fichiers JSON. Comparez-les. Combien de stations ont bougé ? Combien n'ont pas bougé du tout ? C'est votre première mesure du rythme réel des flux, et elle vous servira à calibrer tout le reste.

**Résultat testable en fin de J1 (point de contrôle formateur) :** documentation des deux flux, format d'événement cible arbitré, conception des topics écrite, comparatif d'outils, Kanban rempli, deux instantanés capturés et comparés.

### Phase 2 — Infrastructure de flux (J2)

Un `docker-compose.yml` **fonctionnel vous est fourni** dans le kit (Kafka en mode KRaft mono-broker + PostgreSQL). Monter un broker n'est pas la compétence évaluée ici : la gestion des offsets, l'idempotence et les agrégations le sont. Ne perdez pas une journée sur de la configuration.

Cela ne vous dispense pas de le **comprendre**, et c'est le vrai travail de la journée. Ligne par ligne : à quoi sert chaque variable d'environnement du broker ? Pourquoi deux `listeners` déclarés, et lequel vos scripts Python utilisent-ils selon qu'ils tournent dans un conteneur ou sur votre machine ? Que se passe-t-il si vous supprimez le volume ? Vous devrez répondre à ces questions en soutenance.

Créez ensuite vos topics avec les paramètres décidés en Phase 1 — ça, c'est à vous — et rédigez au fil de l'eau la **procédure d'installation** : quelqu'un qui clone votre repo doit pouvoir tout relancer en moins de 10 minutes.

Comment vérifiez-vous que le broker est réellement **sain** avant d'y brancher quoi que ce soit ? Si vous détruisez puis recréez les conteneurs, vos topics et vos données survivent-ils — et est-ce un problème ?

Le temps dégagé par le `docker-compose` fourni, investissez-le dans un **banc d'essai** : produisez et consommez quelques messages de test à la main, en ligne de commande, avant d'écrire la moindre ligne de producteur. Vous saurez ainsi, le jour où votre code ne marchera pas, si le problème vient de Kafka ou de vous.

**Résultat testable en fin de J2 :** le démarrage de la stack puis la liste des topics fonctionnent sur une machine propre en suivant uniquement votre README ; vous savez expliquer chaque service du `docker-compose.yml` ; un message de test circule de bout en bout.

### Phase 3 — Producteur et premiers consommateurs (J3)

Le cœur du brief : transformer deux instantanés en un flux d'événements.

Développez le **producteur**. Il interroge les deux sources à la fréquence décidée, normalise les deux schémas vers votre format d'événement unique et publie sur Kafka. Que fait-il si Vélib' répond en 30 secondes, ou pas du tout — il attend, il abandonne, il réessaie, et Lyon en pâtit-il ? Que met-il exactement comme **clé de message**, et pourquoi ? Que fait-il d'une station dont l'API ne renvoie plus la moindre trace aujourd'hui ?

Développez ensuite vos premiers **consommateurs** en consumer group. Commencez simple : lire les états et les écrire, horodatés, dans PostgreSQL. C'est ici que se joue la robustesse. Que devient un message dont un champ attendu est absent — le pipeline s'arrête, l'ignore, le met de côté ? Quand validez-vous les **offsets**, et que se passe-t-il si le consommateur meurt entre la lecture d'un message et son écriture en base ? Si le même état est relu après un redémarrage, votre insertion crée-t-elle un doublon ? Et si la source elle-même vous renvoie deux fois le même état, parce que vous sondez plus vite qu'elle ne se rafraîchit ?

**Résultat testable en fin de J3 (point de contrôle formateur) :** le producteur tourne 20 minutes, vous arrêtez puis relancez un consommateur en cours de route, et vous démontrez qu'aucun état n'est perdu ni dupliqué en base.

> **Laissez tourner.** À partir de la fin de J3, faites tourner votre producteur en continu, y compris la nuit. Vos agrégations de J4 ont besoin d'un historique réel pour dire quoi que ce soit d'intéressant : une vitesse de vidage calculée sur vingt minutes de données ne prouve rien. C'est aussi le meilleur moyen de découvrir ce que fait votre pipeline au bout de douze heures.

### Phase 4 — Agrégations, détection et mini-dashboard (J4)

Vous disposez maintenant d'un historique — celui que vous avez fabriqué. Exploitez-le pour répondre à la question centrale. Trois calculs constituent le socle :

- le **taux de remplissage** par station sur une fenêtre glissante ;
- la **vitesse de vidage** : combien de vélos une station a-t-elle perdus par heure sur la dernière fenêtre, et donc dans combien de temps sera-t-elle à sec ?
- les **stations hors service** : horodatage figé au-delà d'un seuil, ou indicateurs de location/restitution au rouge.

Quel seuil retenez-vous pour déclarer une station « à sec imminente », et au nom de quel besoin d'exploitation ? Comment évitez-vous de crier au loup sur une station résidentielle endormie la nuit ? Qu'affiche votre fenêtre pour une station qui vient d'être installée et n'a que deux points de mesure ?

Persistez les résultats dans des tables dédiées et préparez la ou les **requêtes SQL** qui, rafraîchies, servent de mini-dashboard à l'exploitant : *où envoyer le camion maintenant ?*

Confrontez enfin vos alertes au réel : prenez les trois stations que votre dashboard déclare les plus urgentes et allez vérifier leur état sur le site public du réseau. Vos alertes disent-elles vrai ? Si non, est-ce le seuil, la fenêtre, ou le calcul ?

**Résultat testable en fin de J4 :** pendant que le producteur tourne, la requête dashboard classe les stations par urgence et la liste des stations hors service est cohérente avec ce qu'on observe sur le terrain.

### Phase 5 — Documentation et démonstration (J5)

Finalisez le README, vérifiez que la procédure d'installation est **rejouable de zéro** (effacez tout, reclonez votre propre repo, suivez votre README à la lettre), mettez à jour le schéma d'architecture et le Kanban, et rédigez votre **journal de bord**.

Répétez ensuite votre démonstration : scénario, ordre des terminaux, plan B si un flux public est indisponible le jour J — prévoyez des données déjà collectées en base, et sachez démontrer votre pipeline même sans réseau. C'est aussi la journée où tenter un bonus, si et seulement si votre socle est complet.

### Socle commun (obligatoire)

- Infrastructure **Kafka + PostgreSQL rejouable** via Docker Compose, topics conçus et justifiés.
- Un **producteur** branché sur les **deux** flux réels, normalisant les deux schémas en un format d'événement unique.
- Au moins **un consumer group robuste** (erreurs, offsets, idempotence, logs).
- Les **trois calculs du socle** (taux de remplissage, vitesse de vidage, stations hors service) persistés.
- Requête SQL de dashboard d'exploitation.
- Repo public documenté avec schéma d'architecture, comparatif d'outils et Kanban.

### Pour aller plus loin (bonus)

Dans l'ordre conseillé :

- Brancher un **troisième réseau** GBFS (les feeds français sont listés sur transport.data.gouv.fr) et vérifier que rien d'autre ne bouge dans votre plateforme — c'est le vrai test de votre normalisation.
- Consommer **Wikimedia EventStreams** pour éprouver l'architecture à haut débit.
- Exposer le dashboard dans une page **Streamlit** auto-rafraîchie.
- Introduire un **schema registry** et le format **Avro** sur un topic.

Les bonus ne compensent jamais un socle incomplet : **terminez d'abord le socle**.

## Livrables

À rendre au plus tard J5 à 17 h (lien du repo posté sur la plateforme) :

- Un **repo GitHub public** avec un README structuré : description du projet et de la question métier, technologies utilisées, instructions d'installation et de lancement pas à pas (prérequis Docker et RAM inclus), architecture, auteur.
- Le fichier **`docker-compose.yml`** effectivement utilisé (celui du kit, éventuellement adapté — signalez et justifiez toute modification) et les scripts ou commandes documentées de **création des topics**.
- Le **script du producteur** : sondage des deux sources, normalisation, publication, gestion des erreurs et journalisation.
- Les **scripts Python des consommateurs** (consumer groups) : persistance des états et calculs d'agrégats.
- Les **scripts SQL** : DDL des tables d'états et d'agrégats, et la ou les requêtes du mini-dashboard, commentées.
- Le **schéma d'architecture au format image** (PNG ou export draw.io) : sources, producteur, topics, consumer groups, base de persistance. Pas de schéma ASCII.
- La **documentation des flux et des topics** : pour chaque source, sa structure, son horodatage et son rafraîchissement ; pour chaque topic, son nom, ses partitions, sa clé et la structure des messages — avec la **table de correspondance des deux schémas** vers votre format unique.
- La **note de fréquence de sondage** : la fréquence retenue et sa justification au regard du `ttl` et du respect des services publics interrogés.
- Le **comparatif d'outils de streaming** — Kafka face à au moins 2 alternatives (une page maximum).
- Le lien vers le **Kanban public** avec les user stories et leur historique.
- Le **journal de bord** (`docs/journal.md`) : les blocages rencontrés sur les flux réels et sur Kafka, ce que vous avez essayé, ce qui a débloqué. Une ligne par blocage suffit ; c'est la qualité du diagnostic qui compte.
- Pour chaque **bonus** réalisé : code, configuration et preuve de fonctionnement dans un dossier `bonus/` séparé du socle.

## Démonstration finale

L'évaluation a lieu en fin de J5 et repose sur deux volets pondérés.

**Volet 1 — Démonstration technique individuelle : 70 %.** 15 minutes de démonstration en direct + 10 minutes de questions. Vous démarrez votre environnement, lancez le producteur, prouvez que les événements des **deux réseaux** circulent dans les topics sous un format unique, montrez les agrégats qui se mettent à jour dans PostgreSQL via la requête dashboard, et déclenchez au moins un **scénario de robustesse** : arrêt/relance d'un consommateur sans perte ni doublon, ou traitement d'une réponse dégradée d'une source.

Les questions portent sur les choix de conception : format d'événement unique, nombre de partitions, clé de partitionnement, gestion des offsets, idempotence, fréquence de sondage, seuils de détection.

**Volet 2 — Revue de code et d'architecture : 30 %.** Structure et lisibilité du repo, gestion des erreurs, logs, qualité du README, schéma d'architecture, table de correspondance des schémas, pertinence du comparatif d'outils (volumétrie, vitesse, variété, coût d'exploitation).

> **Validation partielle** : un pipeline qui ne fonctionne pas en démonstration mais dont le code est structuré, versionné et documenté peut valider partiellement les compétences concernées. À l'inverse, une démonstration réussie sans documentation ne valide pas les critères documentaires.

Sans repo GitHub public accessible et sans code versionné, le travail ne peut pas être évalué.

## Critères de validation

### Conception de l'architecture de flux

- Le schéma d'architecture représente les deux sources, le producteur, les topics, les consumer groups et la persistance, avec un formalisme lisible.
- Les choix techniques sont justifiés au regard de la **volumétrie, de la vitesse et de la variété** des deux flux.
- Un comparatif d'au moins 2 outils alternatifs à Kafka est documenté avec des critères explicites reliés au besoin de Rebalance.
- La conception des topics (nommage, partitions, clé de partitionnement) est documentée et argumentée.

### Intégration de l'infrastructure

- Kafka (mode KRaft) et PostgreSQL démarrent via Docker Compose sans erreur en environnement de test.
- La procédure d'installation du README se déroule sans erreur sur une machine propre.
- Les composants sont effectivement connectés : les états produits arrivent dans les topics et les données atterrissent dans PostgreSQL.
- La documentation couvre la configuration des composants (ports, volumes, variables d'environnement).

### Automatisation de la collecte et de la consommation

- Le producteur interroge effectivement les **deux** sources réelles et publie sans intervention manuelle ; sa fréquence de sondage est cohérente avec le `ttl` annoncé et justifiée.
- Les deux schémas sources sont normalisés en un format d'événement unique, documenté par une table de correspondance.
- Les consommateurs tournent en consumer group et lisent les topics en continu ; un message incomplet ou malformé ne stoppe pas le pipeline mais est traité selon une stratégie explicite.
- L'arrêt puis la relance d'un consommateur ne provoquent ni perte ni doublon en base (offsets et idempotence démontrés en direct) ; les logs permettent de diagnostiquer un incident.

### Règles d'agrégation et de détection

- Les trois calculs du socle (taux de remplissage, vitesse de vidage, stations hors service) sont calculés et persistés correctement.
- Les états dupliqués — qu'ils viennent d'un rejeu Kafka ou d'un sondage plus rapide que la source — sont écartés avant agrégation.
- Les seuils de détection sont explicites, justifiés au regard du besoin d'exploitation, et les cas limites sont traités (station récente, station endormie la nuit).
- La documentation explicite la règle de calcul de chaque agrégat : fenêtre, formule, cas limites.

## Ressources

- [Cours Python](../../../01-Fondamentaux/Python/)
- [Cours SQL](../../../01-Fondamentaux/SQL/)
- [Cours Docker](../../../02-Containerisation/Docker/)
- [Cours Kafka](../../../06-Data-Engineering/Kafka/)
- Vélib' Métropole — disponibilité en temps réel (jeu de données et API) : https://opendata.paris.fr/explore/dataset/velib-disponibilite-en-temps-reel/
- Documentation de l'API Opendatasoft Explore v2.1 : https://help.opendatasoft.com/apis/ods-explore-v2/
- Vélo'v Lyon — index GBFS : https://download.data.grandlyon.com/files/rdata/jcd_jcdecaux.jcdvelov/gbfs.json
- Spécification GBFS (standard officiel, champs et `ttl`) : https://gbfs.org/specification/reference/
- Liste des flux de vélos et trottinettes en France : https://transport.data.gouv.fr/datasets?type=vehicles-sharing
- Documentation officielle Apache Kafka (concepts, configuration, KRaft) : https://kafka.apache.org/documentation/
- Quickstart Apache Kafka : https://kafka.apache.org/quickstart
- Client Python confluent-kafka (producer, consumer, offsets) : https://docs.confluent.io/kafka-clients/python/current/overview.html
- PostgreSQL — `INSERT ... ON CONFLICT` (idempotence des écritures) : https://www.postgresql.org/docs/current/sql-insert.html
- Documentation Docker Compose : https://docs.docker.com/compose/
- Wikimedia EventStreams, flux temps réel public (bonus) : https://wikitech.wikimedia.org/wiki/Event_Platform/EventStreams
