# Brief B08 — Observatoire immobilier : scraping encadré, stratégie data-driven et registre RGPD

## Informations

| | |
|---|---|
| **Semaine** | S8 · 2–6 nov 2026 · 5 jours · Ayoub |
| **Modalité · Évaluation** | Groupe (3–4) · Sommatif |
| **Compétences visées** | C1.5 · C1.2 · C1.7 · C1.1 · C1.6 · C2.3 · C3.1 |

## Description

Une agence d'urbanisme veut suivre le marché locatif en temps réel. Les données n'existent que sur des sites d'annonces. Vous devez les collecter — et démontrer que vous avez le droit de le faire, ce qui est la moitié du travail.

## Contexte

L'Agence d'urbanisme de la métropole lilloise publie chaque année un observatoire du logement. Ses données sur le locatif privé proviennent d'une enquête déclarative annuelle : elles arrivent avec dix-huit mois de retard et reposent sur 400 réponses.

La directrice de l'observatoire veut un dispositif de suivi continu. Les annonces immobilières en ligne contiennent tout ce qui manque : loyers demandés, surfaces, localisation, délais de mise en location. Des milliers d'observations, actualisées chaque jour.

Elle sait aussi que le sujet est sensible. Une agence publique qui aspire les données d'acteurs privés s'expose. Elle a été claire lors du cadrage : « Je ne veux pas d'un script qui marche. Je veux un dispositif que je puisse défendre devant mon conseil d'administration, devant la CNIL si nécessaire, et devant les professionnels de l'immobilier qui vont râler. »

Trois questions doivent donc être traitées ensemble. Que dit le fichier `robots.txt` du site, et que disent ses conditions générales d'utilisation ? Les annonces contiennent-elles des données personnelles — le nom d'un particulier vendeur, un numéro de téléphone, une adresse précise ? Et à quelle fréquence peut-on interroger un serveur sans le perturber, ce qui relèverait d'un autre régime juridique ?

Vous travaillez en groupe, comme dans un vrai cabinet : quelqu'un code, quelqu'un instruit le volet juridique, quelqu'un construit la stratégie d'usage. Aucun de ces volets ne vaut sans les deux autres.

## Objectifs pédagogiques

À l'issue de ce brief, vous serez capable de :

- **C1.5** — Automatiser des collectes de données par web scraping en s'assurant du respect de la réglementation en vigueur *(niveau 2 — adapter)*
- **C1.2** — Définir une stratégie de prise de décision par les données suivant les besoins métier *(niveau 2 — adapter)*
- **C1.7** — Contrôler les modalités de collecte et d'utilisation de données et mesurer les enjeux du RGPD *(niveau 2 — adapter)*
- **C1.1** — Identifier les possibilités d'utilisation des données *(niveau 2 — adapter)*
- **C1.6** — Mettre en place une interface standard de partage automatique de données *(niveau 2 — adapter)*
- **C2.3** — Manipuler des structures de données et utiliser l'algorithmie *(niveau 2 — adapter)*
- **C3.1** — Utiliser les statistiques descriptives *(niveau 2 — adapter)*

## Modalités pédagogiques

**Organisation** : groupes de 3 à 4. Un dépôt commun. Les rôles tournent obligatoirement en milieu de semaine — personne ne doit finir la semaine sans avoir touché au code ni au volet juridique.

**Jour 1 — matin (lancement, 2 h)**. Le formateur joue la directrice. Vous recevez la cible : un site d'annonces réel. Avant tout code, vous ouvrez son `robots.txt` et ses CGU. Vous répondez par écrit : avons-nous le droit ?

**Jour 1 — après-midi**. Vous vous entraînez sur `books.toscrape.com`, bac à sable conçu pour l'apprentissage, pendant que le volet juridique s'instruit en parallèle.

**Jour 2 — matin (apport flash, 2 h)**. Scraping : sélecteurs CSS, pagination, temporisation, en-tête `User-Agent`, robustesse face aux changements de structure. Cadre légal : `robots.txt`, CGU, directive sur les bases de données, position de la CNIL sur la collecte de données publiques.

**Jour 3 — matin (apport flash, 1 h 30)**. RGPD opérationnel : base légale, minimisation, durée de conservation, registre des traitements, analyse d'impact. Ce qui distingue une donnée personnelle d'une donnée anonyme, et pourquoi le croisement change tout.

**Jours 2 à 4 — production**.
1. **Instruire** — note juridique : ce que permet le site, ce qu'il interdit, ce que vous décidez et pourquoi.
2. **Collecter** — scraper respectueux : temporisation, `User-Agent` identifiant l'agence, reprise après interruption, arrêt propre.
3. **Compléter** — enrichissez par l'API BAN (réactivation de B07) pour normaliser les localisations.
4. **Protéger** — registre RGPD : chaque champ collecté, sa nature, sa base légale, sa durée de conservation, la mesure appliquée.
5. **Valoriser** — note de stratégie : trois décisions d'urbanisme que ce dispositif permettrait d'éclairer, et l'indicateur associé à chacune.

**Questions guidantes.** Une annonce publiée par un particulier avec son prénom et son téléphone est-elle une donnée personnelle ? Le fait qu'elle soit publique change-t-il quelque chose ? Si vous conservez surface et loyer sans le nom, mais avec l'adresse exacte, la donnée est-elle anonyme ? Que se passe-t-il si le site modifie sa structure la semaine prochaine ? Combien de requêtes par minute constitueraient une perturbation de service ?

**Jour 4 — après-midi (revue croisée)**. Un autre groupe joue le rôle du juriste de l'agence et cherche la faille de votre note.

**Jour 5**. Finalisation, publication, restitution 12 minutes devant le formateur en directrice, qui posera les questions de son conseil d'administration.

## Modalités d'évaluation

Brief **sommatif**, checklist complète.

Trois volets pondérés. **Technique** (40 %) : le scraper collecte effectivement, proprement, de façon reprenable. **Juridique** (35 %) : la note et le registre résistent à la contradiction. **Stratégique** (25 %) : les usages proposés sont plausibles et outillés par un indicateur.

Un groupe qui livre un scraper parfait sans registre RGPD ne valide pas le brief. Un groupe qui, après instruction, conclut « ce site ne permet pas la collecte, voici la source alternative que nous proposons » et le démontre, valide pleinement — c'est une conclusion professionnelle légitime.

La restitution du jour 5 est contradictoire : préparez-vous à défendre vos choix.

## Données fournies (source exacte)

> Scraping réalisé sur un **bac à sable légal** ; enrichissement via une **API publique** réelle.

- **Cible de scraping** : `books.toscrape.com` (bac à sable conçu pour l'entraînement au scraping ;
  aucune donnée personnelle). Son **prix** sert de **proxy de loyer** ; une commune de la métropole
  lilloise est attribuée à chaque annonce (dimension géographique de l'observatoire).
- **Enrichissement** : Base Adresse Nationale (`api-adresse.data.gouv.fr`, sans clé).
- Sur un **vrai site d'annonces**, la collecte ne serait engagée **qu'après** analyse du `robots.txt`,
  des CGU et du droit des bases de données (c'est l'objet de la note juridique).

## Livrables attendus

**Un dépôt GitHub public** par groupe :

1. `README.md` — dispositif, cadre, installation, auteurs et répartition des rôles.
2. `note-juridique.md` — analyse du `robots.txt`, des CGU, du cadre applicable ; décision motivée ; mesures de limitation retenues.
3. `scraper/` — le code, avec temporisation, `User-Agent` explicite, journalisation et reprise sur interruption.
4. `enrichissement/ban.py` — normalisation des localisations par API.
5. `registre-rgpd.md` — tableau : champ collecté, nature, donnée personnelle oui/non, base légale, durée de conservation, mesure appliquée, risque résiduel.
6. `strategie-data-driven.md` — trois décisions d'urbanisme éclairées par le dispositif, l'indicateur associé, la fréquence de mise à jour nécessaire.
7. `rapport-collecte.md` — volumétrie, taux de succès, profil statistique des données obtenues (loyer médian, dispersion, valeurs aberrantes détectées).

## Critères de performance

**C1.5 — Scraping, niveau adapter**
• Le scraper collecte au minimum 300 annonces exploitables.
• Une temporisation explicite est en place et sa valeur est justifiée dans la note juridique.
• Le `User-Agent` identifie l'organisme collecteur.
• Le script reprend après interruption sans repartir de zéro.
• Le comportement face à une page manquante ou modifiée est géré et journalisé.

**C1.7 — RGPD, niveau adapter**
• Le registre couvre tous les champs collectés, sans exception.
• Chaque champ est qualifié : donnée personnelle ou non, avec justification.
• Une base légale est identifiée pour le traitement.
• Une durée de conservation est fixée pour chaque catégorie.
• Au moins une mesure de minimisation est appliquée et visible dans le code.

**C1.2 — Stratégie, niveau adapter**
• Trois décisions d'urbanisme sont formulées de façon opérationnelle.
• Chacune est reliée à un indicateur calculable à partir des données collectées.
• La fréquence d'actualisation nécessaire est précisée et justifiée.

**C1.1 / C1.6 / C2.3 / C3.1 — Réactivation**
• Les limites de qualité des données collectées sont identifiées et chiffrées.
• L'enrichissement par API fonctionne et son taux de succès est mesuré.
• Le code est modulaire et gère les erreurs.
• Le profil statistique comporte médiane, dispersion et détection de valeurs aberrantes.

## Ressources

- CNIL — la réutilisation des données publiquement accessibles : https://www.cnil.fr/fr/la-reutilisation-des-donnees-publiquement-accessibles-en-ligne-des-fins-de-demarchage-commercial
- CNIL — le registre des activités de traitement : https://www.cnil.fr/fr/RGPD-le-registre-des-activites-de-traitement
- Bac à sable d'entraînement au scraping : https://books.toscrape.com/
- BeautifulSoup — documentation : https://beautiful-soup-4.readthedocs.io/en/latest/
- Spécification robots.txt : https://www.rfc-editor.org/rfc/rfc9309.html
- Base Adresse Nationale — API : https://adresse.data.gouv.fr/api-doc/adresse
