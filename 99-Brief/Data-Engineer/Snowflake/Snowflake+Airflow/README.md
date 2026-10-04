# Brief Data Engineer — Pipeline médaillon NYC Yellow Taxi : Snowflake et Airflow

> Apprenants : commencez par [`BRIEF.md`](BRIEF.md). Cette page s'adresse au formateur.

Brief guidé de 5 jours, en binôme. Les apprenants construisent un entrepôt Snowflake (rôles, droits, utilisateur de service, couche RAW) et un pipeline Airflow qui charge chaque mois les fichiers publics de la TLC, exécute des transformations SQL fournies et contrôle la qualité des données.

![Le parcours en cinq journées](starter-kit/docs/parcours.png)

## Contenu du dossier

| Fichier | Pour qui | Rôle |
|---|---|---|
| `BRIEF.md` | apprenants | le brief, champ par champ, au format Simplonline |
| `RESSOURCES.md` | apprenants | guides, documentation et vidéos, jour par jour |
| `starter-kit/` | apprenants | fichiers SQL fournis, contrat de la couche RAW, détail des étapes, schéma du pipeline, modèles de fiche et de réponse, configuration Airflow |

Ce dossier ne contient ni la solution ni la grille de notation : elles sont conservées hors de ce dépôt public.

## Compétences visées

C2 et C3 au niveau 1 (imiter) ; C8, C9, C14, C15 et C16 au niveau 2 (adapter).

## Prérequis des apprenants

Bases de Python et de SQL (SELECT, JOIN, GROUP BY), Git, terminal. Aucune connaissance de Snowflake ni d'Airflow. Postes macOS, Linux ou Windows (avec WSL).

## Publier le brief sur Simplonline

1. Copier chaque section de `BRIEF.md` dans le champ du même nom (titre, description rapide, compétences, contexte, modalités pédagogiques, modalités d'évaluation, livrables, critères de performance). Les limites de caractères de chaque champ sont respectées.
2. Copier le contenu de `RESSOURCES.md` dans le champ Ressources.
3. Les deux images du brief ont des chemins relatifs, qui s'affichent sur GitHub mais pas dans Simplonline. Y remplacer `starter-kit/docs/architecture.png` et `starter-kit/docs/parcours.png` par leurs adresses publiques, ou téléverser les images :
   - `https://raw.githubusercontent.com/gsoulat/formation-data-IA/main/99-Brief/Data-Engineer/Snowflake/Snowflake+Airflow/starter-kit/docs/architecture.png`
   - `https://raw.githubusercontent.com/gsoulat/formation-data-IA/main/99-Brief/Data-Engineer/Snowflake/Snowflake+Airflow/starter-kit/docs/parcours.png`

## Avant la première journée

Demander aux apprenants d'installer Python 3.12, Docker, Astro CLI et Git, de créer leur compte d'essai Snowflake, de récupérer le kit (commandes dans `RESSOURCES.md`) et d'y lancer `bash verifier_poste.sh`.

## Guides du cours utilisés par le brief

- Jour 1 : [Sécurité Snowflake : rôles, droits et utilisateurs de service](../../../../04-Cloud-Platforms/snowflake/10-securite.md)
- Jour 2 : [Charger des fichiers : format, stage, PUT, COPY INTO](../../../../04-Cloud-Platforms/snowflake/11-chargement-stage-copy.md)
- Jours 3 et 4 : [Airflow 3 avec Astro CLI](../../../../06-Data-Engineering/Airflow/06-Airflow3-Astro/01-airflow3-astro-snowflake.md)
