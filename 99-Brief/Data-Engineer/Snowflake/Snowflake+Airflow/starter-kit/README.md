# Kit de démarrage — Pipeline médaillon NYC Yellow Taxi (Snowflake et Airflow)

Point de départ du brief. Ce kit contient ce qui est fourni ; tout le reste est à construire.

## Dans quel ordre lire

1. **Le brief** : la situation, ce qui est attendu, comment vous serez évalués.
2. **Ce README** : ce que contient le kit.
3. **`ETAPES.md`**, chaque matin : le détail de la journée, les pièges, le résultat à obtenir.
4. **`CONTRAT_RAW.md`**, au jour 2 : les noms que votre entrepôt doit respecter.

Avant le premier jour, lancez `bash verifier_poste.sh` : tout doit afficher `OK`.

## Ce que vous allez construire

![Schéma du pipeline](docs/architecture.png)

## Contenu du kit

```
.
├── README.md                      ce fichier
├── ETAPES.md                      le détail de chaque journée
├── CONTRAT_RAW.md                 noms et colonnes que votre entrepôt doit contenir
├── verifier_poste.sh              vérifie Python, Git, Docker, Astro CLI, OpenSSL
├── .gitignore                     exclut les clés, le .env et les fichiers téléchargés
├── snowflake/                     À ÉCRIRE : scripts d'infrastructure et de couche RAW
├── ingestion/                     À ÉCRIRE : script Python de chargement d'un mois
├── docs/
│   ├── architecture.png           le schéma du pipeline
│   ├── parcours.png               les cinq journées en un coup d'œil
│   ├── FICHE_SOURCE_MODELE.md     modèle de fiche source (jour 1)
│   └── REPONSE_MODELE.md          modèle de réponse à la direction (jour 5)
└── airflow/
    ├── requirements.txt           dépendances Python du projet Airflow
    ├── .env.example               format de la connexion Snowflake
    ├── dags/                      À ÉCRIRE : votre DAG
    └── include/sql/               FOURNI : les fichiers SQL, à ne pas modifier
        ├── 00_tables.sql          crée les trois tables alimentées mois par mois
        ├── staging/               2 vues de renommage + les tables de codes
        ├── intermediate/          trajets étiquetés, puis trajets valides enrichis
        ├── marts/                 5 dimensions, la table de faits, 3 tables d'analyse
        └── controles/             1 contrôle fourni comme modèle, les autres À ÉCRIRE
```

Les fichiers `.gitkeep` ne servent qu'à conserver les dossiers vides dans Git : vous pouvez les supprimer dès que vous y ajoutez un fichier.

## Selon votre système

| Système | Terminal à utiliser | Installation d'Astro CLI | À savoir |
|---|---|---|---|
| macOS | Terminal | `brew install astro` | Docker Desktop ou OrbStack |
| Linux | terminal habituel | `curl -sSL install.astronomer.io \| sudo bash -s` | Docker Engine suffit |
| Windows | **WSL avec Ubuntu**, pas PowerShell | la commande Linux, dans Ubuntu | activer l'intégration WSL dans Docker Desktop ; placer le projet dans le dossier personnel d'Ubuntu (`~`), pas sous `/mnt/c` : les droits du fichier de clé n'y fonctionnent pas |

Les commandes du brief et des guides (`openssl`, `awk`, `bash`, `python3`) sont celles d'un terminal macOS ou Linux. Sous Windows, elles s'exécutent telles quelles dans Ubuntu (WSL). Les consignes Windows n'ont pas été testées sur un poste réel.

## Lire les fichiers SQL fournis

Chaque fichier crée une vue ou une table, ou alimente une table pour le mois traité.

- **Les noms sont complets** (`NYC_TAXI.MARTS.FCT_TRIPS`) : la base, les schémas et les tables portent des noms imposés. Le nom du warehouse, du rôle et de l'utilisateur de service est libre.
- **Pour trouver l'ordre d'exécution** : chaque fichier lit des tables (`FROM`, `JOIN`) et en crée une. Un fichier s'exécute après ceux qui créent les tables qu'il lit. `00_tables.sql` passe avant tout le reste.
- **Ce qui est entre doubles accolades** est remplacé par Airflow avant l'exécution :

| Dans le fichier | Remplacé par | Exemple pour janvier 2025 |
|---|---|---|
| `{{ ds }}` | le premier jour du mois traité | `2025-01-01` |
| `{{ logical_date.strftime("%Y-%m") }}` | le mois traité | `2025-01` |
| `{{ params.xxx }}` | un paramètre à déclarer dans votre DAG | voir ci-dessous |

Exécuté tel quel dans Snowsight, un fichier qui contient des accolades échoue : remplacez-les d'abord à la main pour le tester.

Les quatre paramètres attendus par les fichiers fournis :

| Paramètre | Valeur | Utilisé par |
|---|---|---|
| `max_trip_distance_miles` | `100` | `intermediate/int_trips__flagged.sql` |
| `max_trip_duration_min` | `180` | `intermediate/int_trips__flagged.sql` |
| `start_month` | `"2025-01-01"` | `marts/dim_date.sql` |
| `end_month` | `"2025-04-01"` | `marts/dim_date.sql` |

## Le contrôle fourni

`controles/raw_mois_charge.sql` vérifie que le mois traité est bien présent dans RAW. Une requête de contrôle renvoie une seule ligne : si une de ses valeurs est fausse, la tâche échoue et la suite ne s'exécute pas. Écrivez les vôtres sur ce modèle.

## Mettre en place le projet Airflow (jour 3)

```bash
cd airflow
astro dev init                    # le dossier n'est pas vide : répondre y
```

`astro dev init` génère le `Dockerfile` et les fichiers du projet, sans toucher à `requirements.txt` ni à `include/`. Ensuite :

1. Supprimer `dags/exampledag.py`.
2. Créer le fichier `airflow/.env` à partir de `airflow/.env.example`. La clé privée y tient sur une seule ligne : voir la section 3 du guide Airflow.
3. Démarrer :

```bash
astro dev start
```

L'adresse de l'interface est affichée à la fin de la commande.

- L'identifiant de connexion à utiliser dans votre code est `snowflake_nyc_taxi`.
- Un DAG est en pause à sa création : activez-le avec son interrupteur. N'utilisez pas le bouton Trigger pour le DAG de chargement : il lance une exécution datée d'aujourd'hui.
- Quand vous ajoutez des tâches à un DAG dont les exécutions sont déjà terminées, elles ne tournent pas toutes seules : ouvrez chaque exécution et relancez-la avec Clear.

## Résultats attendus

| Table | Lignes après les trois mois |
|---|---|
| `RAW.YELLOW_TRIPDATA` | 11 198 026 (3 475 226 en janvier) |
| `RAW.TAXI_ZONE_LOOKUP` | 265 |
| `INTERMEDIATE.INT_TRIPS__FLAGGED` | 11 198 026 |
| `MARTS.FCT_TRIPS` | 10 382 378 |
| `MARTS.MART_ZONE_HOURLY_DEMAND` | 11 524 |
| `MARTS.MART_DATA_QUALITY` | 18 |
