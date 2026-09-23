# Vidéos récentes — Airflow 3 et Snowflake

Toutes les vidéos ci-dessous ont été publiées **entre septembre 2025 et septembre 2026**. Leur date
a été vérifiée sur la page de la vidéo (liste établie le 23/09/2026). Les vidéos sur Airflow
utilisent bien **Airflow 3** : beaucoup de tutoriels récents enseignent encore Airflow 2, ils ont
été écartés.

> ⚠️ Une vidéo n'est pas une documentation. Si une vidéo et ce cours se contredisent, vérifiez
> dans la documentation officielle — et signalez-le au formateur.

## Lundi — Airflow 3 : architecture et installation

| Vidéo | Chaîne | Date | Langue · durée | Pourquoi la regarder |
|---|---|---|---|---|
| [Apache Airflow 3 : La RÉVOLUTION qui Change TOUT](https://www.youtube.com/watch?v=54fMo6Epgb4) | NetSecDev | 20/10/2025 | FR · 17 min | vue d'ensemble d'Airflow 3 en français : architecture client-serveur, nouvelle interface |
| [Apache Airflow 3+ QuickStart Under 2 Minutes](https://www.youtube.com/watch?v=_DphEMwONMI) | Shantanu Khond | 19/06/2026 | EN · 3 min | le démarrage Docker Compose en accéléré : `.env`, `airflow-init`, `up -d` |
| [Introducing Apache Airflow® 3 – The Next Evolution in Orchestration](https://www.youtube.com/watch?v=nGklMyALNbQ) | Apache Airflow (Airflow Summit 2025) | 15/11/2025 | EN · 1 h 38 | la présentation par les mainteneurs : api-server, dag-processor, Task SDK, assets, backfill |
| [What's New in Apache Airflow® 3.3](https://www.youtube.com/watch?v=jXB4NFns--Q) | Astronomer | 09/07/2026 | EN · 27 min | les nouveautés de la version utilisée dans ce cours |

## Mardi — écrire et planifier des DAG

| Vidéo | Chaîne | Date | Langue · durée | Pourquoi la regarder |
|---|---|---|---|---|
| [Airflow Tutorial For Beginners (2026) — Full Course](https://www.youtube.com/watch?v=IiczxlbQb8s) | Ansh Lamba | 01/02/2026 | EN · 6 h 11 | cours complet en Airflow 3 ; chapitres sur la planification (cron, presets, delta), le chargement incrémental et les assets. Installation à 1:51:14 |
| [Data Engineering Best Practices: Idempotency](https://www.youtube.com/watch?v=SKtKoyVQHXs) | StartDataEngineering | 02/04/2026 | EN · 6 min | l'idempotence en six minutes : la propriété qui rend un pipeline rejouable |
| [Free Live Airflow Webinar](https://www.youtube.com/watch?v=38DHch4FxbU) | StartDataEngineering | 11/04/2026 | EN · 1 h 36 | chargement complet ou incrémental, assets, bonnes pratiques Airflow 3 sous Docker Compose |

## Mercredi — Snowflake

| Vidéo | Chaîne | Date | Langue · durée | Pourquoi la regarder |
|---|---|---|---|---|
| [Comment créer un compte Snowflake gratuit et exécuter sa première requête SQL](https://www.youtube.com/watch?v=rvy4NebtHHM) | J.A DATATECH CONSULTING | 16/03/2026 | FR · 9 min | la création du compte d'essai pas à pas. **Choisissez une région européenne**, pas celle du lien de la vidéo |
| [Learn Snowflake – Full 1-Hour Crash Course for Complete Beginners](https://www.youtube.com/watch?v=2t-ls6ekA8E) | Tom Bailey | 27/11/2025 | EN · 58 min | architecture, Snowsight, hiérarchie des objets, entrepôts virtuels |
| [Snowflake Data Loading Explained — Stages, COPY INTO, and Snowpipe](https://www.youtube.com/watch?v=hr8zTWDv_9U) | Agilityx | 02/06/2026 | EN · 10 min | stages, `COPY INTO`, `ON_ERROR`, et la mémoire des fichiers déjà chargés (utile pour comprendre notre `FORCE = TRUE`) |
| [Snowflake Pricing Explained (2026)](https://www.youtube.com/watch?v=fKU2vmIxMsc) | Professor M | 30/07/2026 | EN · 9 min | crédits, tailles d'entrepôt, stockage : pour ne pas brûler l'essai gratuit |
| [Stop Using Passwords in Snowflake — Here's the Modern Method](https://www.youtube.com/watch?v=fg7dnuAtsmI) | Timnology | 17/11/2025 | EN · 6 min | générer la paire de clés et créer l'utilisateur : exactement ce que fait notre script d'installation |
| [Production-Ready ELT Pipelines with Airflow 3 and Snowflake](https://www.astronomer.io/events/webinars/elt-pipelines-with-airflow-3-and-snowflake-video/) | Astronomer (webinaire) | 13/11/2025 | EN · 55 min | Airflow 3 + Snowflake de bout en bout : stages, contrôles qualité, assets, authentification par clé |
| [Du fichier CSV à la couche Gold avec Snowflake](https://www.youtube.com/watch?v=1tmbMNSLMMQ) | Martinien Adda | 17/07/2026 | FR · 1 h 12 | projet Snowflake complet en français, du chargement brut aux tables d'analyse |

## Jeudi — capteurs différés et assets

| Vidéo | Chaîne | Date | Langue · durée | Pourquoi la regarder |
|---|---|---|---|---|
| [Purple is the new green: harnessing deferrable operators](https://www.youtube.com/watch?v=vqH6dsPPlgw) | Apache Airflow (Airflow Summit 2025) | 20/11/2025 | EN · 20 min | comment fonctionnent les opérateurs différés et le triggerer, avec un retour d'expérience en production |
| [Assets: Past, Present, Future](https://www.youtube.com/watch?v=KA6iDX5MVi4) | Apache Airflow (Airflow Summit 2025) | 20/11/2025 | EN · 19 min | la planification pilotée par la donnée, des *datasets* d'Airflow 2 aux *assets* d'Airflow 3 |
| [Unlocking Event-Driven Scheduling in Airflow 3](https://www.youtube.com/watch?v=GT6BBdSwwt8) | Apache Airflow (Airflow Summit 2025) | 15/11/2025 | EN | aller plus loin : déclencher un DAG sur un événement externe |
| [Introducing Airflow 3.2: asset partitioning](https://www.youtube.com/watch?v=e1TVEIwNiCM) | Astronomer | 08/04/2026 | EN · 6 min | les assets partitionnés, pensés pour des fichiers périodiques comme nos fichiers mensuels |

## Vendredi — tests et bonnes pratiques

| Vidéo | Chaîne | Date | Langue · durée | Pourquoi la regarder |
|---|---|---|---|---|
| [The easiest way for testing Airflow DAGs](https://www.youtube.com/watch?v=Onm2vWy7SUM) | Data with Marc | 20/02/2026 | EN · 28 min | tester un DAG sans attendre l'interface, en Airflow 3 |
| [Apache Airflow 3.0 - Bad vs. Best Practices In Production](https://www.youtube.com/watch?v=6ZXQZnrU_fw) | Apache Airflow (Airflow Summit 2025) | 20/11/2025 | EN · 20 min | ce qu'Airflow 3 change dans les bonnes pratiques d'écriture et d'exploitation |
| [The Reddit Project (Airflow, Slack, Snowflake and OpenAI)](https://www.youtube.com/watch?v=9N0ZNFezfVw) | Data with Marc | 29/10/2025 | EN · 32 min | un projet complet Airflow 3 + Snowflake, avec alertes Slack : une bonne idée de ce que peut devenir votre brief |

## Ce qui manque (à la date de la liste)

- Aucune vidéo récente et vérifiée n'est consacrée au **backfill** d'Airflow 3 : il est traité dans
  la présentation de l'Airflow Summit et dans le cours d'Ansh Lamba.
- Aucune vidéo récente en français ne montre l'installation d'**Airflow 3 avec Docker Compose** :
  le cours du lundi est votre référence.
