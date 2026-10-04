# 03 — Opérateurs Fichiers

## Vue d'ensemble

Les opérateurs fichiers permettent d'interagir avec le système de fichiers local, S3 (AWS), GCS (Google Cloud Storage), Azure Blob Storage, et bien d'autres.

```bash
# Installation des providers nécessaires
pip install apache-airflow-providers-amazon    # S3
pip install apache-airflow-providers-google    # GCS
pip install apache-airflow-providers-sftp      # SFTP
pip install apache-airflow-providers-ftp       # FTP
```

---

## FileSensor — attendre qu'un fichier soit présent

Le `FileSensor` attend qu'un fichier ou un répertoire apparaisse sur le système de fichiers. C'est utile pour déclencher un pipeline dès qu'un fichier de données arrive.

En Airflow 3, il s'importe depuis le provider standard (l'ancien chemin `airflow.sensors.filesystem` des tutoriels Airflow 2 est à remplacer).

```python
from airflow.providers.standard.sensors.filesystem import FileSensor

attendre_fichier = FileSensor(
    task_id='attendre_fichier_source',
    filepath='/data/incoming/ventes_{{ ds_nodash }}.csv',
    # Vérifier toutes les 30 secondes
    poke_interval=30,
    # Échouer après 1 heure d'attente
    timeout=3600,
    # soft_fail=True : passer en "skipped" au lieu d'"echec" en cas de timeout
    soft_fail=False,
    # mode='reschedule' : libère le worker entre les vérifications (recommandé)
    mode='reschedule',
)
```

### mode='poke' vs mode='reschedule'

```
mode='poke' :
  Worker occupé tout le temps de l'attente
  ┌─────────────────────────────────────────┐
  │ Worker 1 : [poke][wait 30s][poke][wait] │ ← bloque un worker
  └─────────────────────────────────────────┘

mode='reschedule' (recommandé) :
  Worker libéré entre chaque vérification
  ┌─────────┐     ┌─────────┐     ┌─────────┐
  │ poke    │ ... │ poke    │ ... │ poke    │ ← worker libre entre les pokes
  └─────────┘     └─────────┘     └─────────┘
```

### FileSensor avec connexion

Le paramètre `fs_conn_id` désigne une connexion de type **File (path)** : elle fournit un répertoire de base (champ Extra `{"path": "/data"}`) auquel `filepath` est ajouté. Le `FileSensor` ne surveille que le système de fichiers vu par le worker (disque local ou volume monté).

```python
from airflow.providers.standard.sensors.filesystem import FileSensor

attendre_rapport = FileSensor(
    task_id='attendre_rapport',
    filepath='incoming/rapport_{{ ds_nodash }}.xlsx',  # Relatif au chemin de la connexion
    fs_conn_id='fs_data',   # Connexion File (path) configurée dans Airflow
    poke_interval=60,   # Vérifier toutes les minutes
    timeout=7200,       # Timeout après 2 heures
    mode='reschedule',
)
```

Pour surveiller un fichier sur un serveur distant, on utilise le capteur du provider concerné, par exemple `SFTPSensor` (`apache-airflow-providers-sftp`) :

```python
from airflow.providers.sftp.sensors.sftp import SFTPSensor

attendre_rapport_sftp = SFTPSensor(
    task_id='attendre_rapport_sftp',
    path='/remote/data/rapport_{{ ds_nodash }}.xlsx',
    sftp_conn_id='sftp_serveur_production',  # Connexion SFTP configurée dans Airflow
    poke_interval=60,
    timeout=7200,
    mode='reschedule',
)
```

---

## Opérateurs de manipulation de fichiers locaux

```python
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.standard.operators.python import PythonOperator
import shutil, os

# Copier un fichier
copier_fichier = BashOperator(
    task_id='copier_fichier',
    bash_command='cp /data/source/{{ ds_nodash }}.csv /data/archive/{{ ds_nodash }}.csv',
)

# Déplacer avec vérification Python
def deplacer_fichier(**context):
    date = context['ds_nodash']
    source = f'/data/incoming/ventes_{date}.csv'
    destination = f'/data/processed/ventes_{date}.csv'

    if not os.path.exists(source):
        raise FileNotFoundError(f"Fichier source introuvable : {source}")

    # Créer le répertoire destination si nécessaire
    os.makedirs(os.path.dirname(destination), exist_ok=True)

    shutil.move(source, destination)
    print(f"Fichier déplacé : {source} → {destination}")
    return destination

deplacer = PythonOperator(
    task_id='deplacer_fichier',
    python_callable=deplacer_fichier,
)

# Archiver (compresser)
archiver = BashOperator(
    task_id='archiver_fichiers',
    bash_command="""
        cd /data/processed
        tar -czf archive_{{ ds_nodash }}.tar.gz *.csv
        echo "Archive créée : archive_{{ ds_nodash }}.tar.gz"
    """,
)
```

---

## S3 — Opérateurs AWS

### Configurer la connexion AWS

```bash
# Via CLI
airflow connections add 'aws_default' \
    --conn-type 'aws' \
    --conn-extra '{"aws_access_key_id": "AKIAIOSFODNN7EXAMPLE",
                   "aws_secret_access_key": "wJalrXUtnFEMI/K7MDENG",
                   "region_name": "eu-west-1"}'

# Via variable d'environnement (recommandé pour les secrets)
# AIRFLOW_CONN_AWS_DEFAULT=aws://AKIAIOSFODNN7EXAMPLE:wJalrXUtnFEMI%2FK7MDENG@?region_name=eu-west-1
```

### S3CreateObjectOperator — créer un objet à partir d'un contenu

`data` est le **contenu** de l'objet (chaîne ou octets), pas un chemin de fichier. Pour envoyer un fichier local, utiliser `LocalFilesystemToS3Operator` ci-dessous.

```python
from airflow.providers.amazon.aws.operators.s3 import S3CreateObjectOperator

# Créer un petit objet S3 (marqueur de fin de traitement)
creer_marqueur_s3 = S3CreateObjectOperator(
    task_id='creer_marqueur_s3',
    s3_bucket='mon-bucket-production',
    s3_key='rapports/{{ ds }}/_SUCCESS',
    data='Rapport du {{ ds }} généré par {{ dag.dag_id }}',  # Contenu de l'objet
    aws_conn_id='aws_default',
    replace=True,   # Écraser si existe déjà
)
```

### LocalFilesystemToS3Operator — transfert local vers S3

```python
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator

transferer_vers_s3 = LocalFilesystemToS3Operator(
    task_id='transferer_vers_s3',
    filename='/data/export/{{ ds_nodash }}_ventes.csv',
    dest_key='data/ventes/{{ ds }}/ventes.csv',
    dest_bucket='mon-data-lake',
    aws_conn_id='aws_default',
    replace=True,
)
```

### Téléchargement depuis S3

Le provider Amazon ne fournit pas d'opérateur de transfert S3 → disque local : on passe par le `S3Hook` dans une tâche Python.

```python
from airflow.sdk import task
from airflow.providers.amazon.aws.hooks.s3 import S3Hook

@task
def telecharger_donnees_s3(ds=None):
    hook = S3Hook(aws_conn_id='aws_default')
    chemin_local = hook.download_file(
        key=f'data/sources/{ds}/commandes.json',
        bucket_name='mon-data-lake',
        local_path='/data/incoming',
        preserve_file_name=True,          # Garder le nom « commandes.json »
        use_autogenerated_subdir=False,   # Écrire directement dans local_path
    )
    return chemin_local   # Chemin du fichier téléchargé, poussé en XCom
```

### S3KeySensor — attendre qu'un objet S3 apparaisse

```python
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

attendre_fichier_s3 = S3KeySensor(
    task_id='attendre_export_s3',
    bucket_name='mon-data-lake',
    bucket_key='exports/partenaire/{{ ds }}/data.parquet',
    aws_conn_id='aws_default',
    poke_interval=300,    # Vérifier toutes les 5 minutes
    timeout=14400,        # Timeout après 4 heures
    mode='reschedule',
)
```

### Lister et supprimer des objets S3

```python
from airflow.providers.amazon.aws.operators.s3 import (
    S3ListOperator,
    S3DeleteObjectsOperator,
)

# Lister les objets d'un préfixe
lister_fichiers = S3ListOperator(
    task_id='lister_fichiers_s3',
    bucket='mon-data-lake',
    prefix='data/staging/{{ ds }}/',
    aws_conn_id='aws_default',
    # Résultat disponible en XCom : liste des clés
)

# Supprimer des objets (nettoyage du staging)
nettoyer_staging = S3DeleteObjectsOperator(
    task_id='nettoyer_staging_s3',
    bucket='mon-data-lake',
    keys=['data/staging/{{ ds }}/file1.csv', 'data/staging/{{ ds }}/file2.csv'],
    aws_conn_id='aws_default',
)
```

---

## Utiliser le S3Hook directement

```python
from airflow.providers.amazon.aws.hooks.s3 import S3Hook
from airflow.providers.standard.operators.python import PythonOperator

def traiter_fichiers_s3(**context):
    """
    Utiliser le Hook S3 directement pour plus de flexibilité.
    """
    hook = S3Hook(aws_conn_id='aws_default')
    date = context['ds']

    # Lister tous les fichiers d'un préfixe
    keys = hook.list_keys(
        bucket_name='mon-data-lake',
        prefix=f'data/incoming/{date}/',
    )
    print(f"Fichiers trouvés : {len(keys or [])}")

    if not keys:
        raise ValueError(f"Aucun fichier trouvé pour la date {date}")

    # Télécharger et traiter chaque fichier
    import pandas as pd
    dfs = []
    for key in keys:
        # Télécharger vers un fichier local temporaire
        local_path = hook.download_file(
            key=key,
            bucket_name='mon-data-lake',
            local_path='/tmp/',
            preserve_file_name=True,
        )
        df = pd.read_csv(local_path)
        dfs.append(df)
        print(f"  Traité : {key} ({len(df)} lignes)")

    # Consolider
    df_final = pd.concat(dfs, ignore_index=True)
    output_path = f'/tmp/consolidated_{date}.parquet'
    df_final.to_parquet(output_path, index=False)

    # Uploader le résultat
    hook.load_file(
        filename=output_path,
        key=f'data/processed/{date}/consolidated.parquet',
        bucket_name='mon-data-lake',
        replace=True,
    )

    print(f"Consolidé : {len(df_final)} lignes au total")
    return f'data/processed/{date}/consolidated.parquet'

traiter_s3 = PythonOperator(
    task_id='traiter_fichiers_s3',
    python_callable=traiter_fichiers_s3,
)
```

---

## DAG complet : pipeline de fichiers

```python
# dags/pipeline_fichiers_s3.py

from datetime import datetime, timedelta
from airflow.sdk import DAG
from airflow.providers.standard.sensors.filesystem import FileSensor
from airflow.providers.standard.operators.python import PythonOperator
from airflow.providers.standard.operators.bash import BashOperator
from airflow.providers.amazon.aws.transfers.local_to_s3 import LocalFilesystemToS3Operator
from airflow.providers.amazon.aws.sensors.s3 import S3KeySensor

default_args = {
    'owner': 'data-team',
    'retries': 2,
    'retry_delay': timedelta(minutes=5),
}

with DAG(
    dag_id='pipeline_fichiers_s3',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    # Airflow 3 : ds est la date de déclenchement. Le run du 2 janvier à 6h
    # attend ventes_20240102.csv (en Airflow 2, c'était ventes_20240101.csv).
    schedule='0 6 * * *',
    catchup=False,
    tags=['fichiers', 's3', 'etl'],
) as dag:

    # 1. Attendre le fichier source
    attendre_source = FileSensor(
        task_id='attendre_fichier_source',
        filepath='/data/incoming/ventes_{{ ds_nodash }}.csv',
        poke_interval=60,
        timeout=7200,
        mode='reschedule',
    )

    # 2. Valider et transformer
    def valider_et_transformer(**context):
        import pandas as pd

        date = context['ds_nodash']
        input_path = f'/data/incoming/ventes_{date}.csv'

        df = pd.read_csv(input_path)
        print(f"Fichier lu : {len(df)} lignes, {len(df.columns)} colonnes")

        # Validation basique
        assert len(df) > 0, "Le fichier est vide !"
        assert 'montant' in df.columns, "Colonne 'montant' manquante !"

        # Transformation
        df['montant'] = pd.to_numeric(df['montant'], errors='coerce')
        df = df.dropna(subset=['montant'])
        df['date_traitement'] = context['ds']

        output_path = f'/data/processed/ventes_{date}.parquet'
        df.to_parquet(output_path, index=False)

        print(f"Transformation OK : {len(df)} lignes → {output_path}")
        return output_path

    transformer = PythonOperator(
        task_id='valider_et_transformer',
        python_callable=valider_et_transformer,
    )

    # 3. Upload vers S3
    upload_s3 = LocalFilesystemToS3Operator(
        task_id='upload_vers_s3',
        filename='/data/processed/ventes_{{ ds_nodash }}.parquet',
        dest_key='ventes/processed/{{ ds }}/ventes.parquet',
        dest_bucket='mon-data-lake',
        aws_conn_id='aws_default',
        replace=True,
    )

    # 4. Vérifier l'upload
    verifier_s3 = S3KeySensor(
        task_id='verifier_fichier_s3',
        bucket_name='mon-data-lake',
        bucket_key='ventes/processed/{{ ds }}/ventes.parquet',
        aws_conn_id='aws_default',
        poke_interval=10,
        timeout=120,
    )

    # 5. Archiver et nettoyer le local
    archiver_et_nettoyer = BashOperator(
        task_id='archiver_et_nettoyer',
        bash_command="""
            mv /data/incoming/ventes_{{ ds_nodash }}.csv \
               /data/archive/ventes_{{ ds_nodash }}.csv
            echo "Fichier archivé."
        """,
    )

    # Dépendances
    attendre_source >> transformer >> upload_s3 >> verifier_s3 >> archiver_et_nettoyer
```

---

> 🔴 **ACTION FORMATEUR — CAPTURE REQUISE**
> **Capturer :** Le terminal + l'interface Airflow montrant une tâche `FileSensor` qui attend (état "up_for_reschedule" entre deux vérifications en mode reschedule), avec les logs indiquant les tentatives "Poking for file..."
> **Expliquer :** Montrer dans les logs le message "Poking for file /data/incoming/ventes_xxx.csv" — fichier absent. Puis simuler l'arrivée du fichier (`touch /data/incoming/ventes_xxx.csv`) et voir la tâche passer en "success". Expliquer la différence entre `mode='poke'` et `mode='reschedule'` en termes de consommation de workers.

---

## GCSToLocalFilesystemOperator — Google Cloud Storage

```python
from airflow.providers.google.cloud.transfers.gcs_to_local import GCSToLocalFilesystemOperator

telecharger_gcs = GCSToLocalFilesystemOperator(
    task_id='telecharger_depuis_gcs',
    bucket='mon-gcs-bucket',
    object_name='data/{{ ds }}/fichier.csv',
    filename='/data/local/fichier_{{ ds_nodash }}.csv',
    gcp_conn_id='google_cloud_default',
)
```

## LocalFilesystemToGCSOperator — upload vers GCS

```python
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator

upload_gcs = LocalFilesystemToGCSOperator(
    task_id='upload_vers_gcs',
    src='/data/processed/rapport_{{ ds_nodash }}.csv',
    dst='rapports/{{ ds }}/rapport.csv',
    bucket='mon-gcs-bucket',
    gcp_conn_id='google_cloud_default',
)
```

---

## Points clés à retenir

1. `FileSensor` avec `mode='reschedule'` pour éviter de bloquer les workers
2. `S3KeySensor` pour attendre qu'un fichier apparaisse dans S3
3. `LocalFilesystemToS3Operator` pour les uploads vers S3
4. Pour télécharger depuis S3 ou pour des opérations complexes (parcourir, filtrer, transformer), utiliser le `S3Hook` directement dans un `PythonOperator` ou un `@task`
5. Toujours configurer les **Connections** Airflow avant d'utiliser les opérateurs cloud
6. Les templates Jinja `{{ ds_nodash }}` donnent la date au format `YYYYMMDD` — pratique pour les noms de fichiers (en Airflow 3, par défaut, c'est la date de déclenchement du run)
