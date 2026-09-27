# Squelette dbt — pour ne pas perdre de temps sur l'outillage

Vous avez vu dbt en cours sans le pratiquer. Ce squelette existe pour que votre
**première commande dbt réussisse**, pas pour vous mâcher le travail : il contient
un projet valide, une source déclarée et **un** modèle d'exemple qui ne fait presque rien.

Tout le reste — modèles sur les déclarations et les bénéficiaires, descriptions,
glossaire, tags PII, tests de fraîcheur / complétude / unicité, lignage — est le
sujet de la Phase 3 du brief.

## Mise en route

```bash
pip install dbt-postgres

set -a && source ../.env && set +a     # PGHOST, PGUSER, PGPASSWORD...
cp profiles.yml.example profiles.yml   # ne le commitez pas

# 1. La connexion fonctionne-t-elle ?
dbt debug --profiles-dir .

# 2. Le modèle d'exemple tourne-t-il ?
#    (nécessite d'avoir chargé la table raw.entreprises en Phase 2)
dbt run --select stg_entreprises --profiles-dir .

# 3. Les tests passent-ils ?
dbt test --profiles-dir .

# 4. La documentation s'ouvre-t-elle ?
dbt docs generate --profiles-dir .
dbt docs serve --profiles-dir .
```

Si `dbt debug` est vert, votre outillage est bon : tout ce qui suit est du travail
de data engineer, plus de la configuration.

## Structure

```
dbt/
├── dbt_project.yml              # projet (fourni)
├── profiles.yml.example         # connexion (fourni)
└── models/
    ├── staging/
    │   ├── _sources.yml         # 1 source déclarée + 2 tests (exemple fourni)
    │   └── stg_entreprises.sql  # 1 modèle minimal (exemple fourni)
    └── marts/                   # A VOUS
```

## Les trois commandes qui comptent pour le brief

- `dbt test` — vos règles de qualité. Un test qui échoue doit avoir une conduite à tenir écrite.
- `dbt docs generate && dbt docs serve` — votre catalogue navigable, avec le lignage.
- `dbt run` — la construction de vos modèles.

## Où mettre quoi

- **Description d'une table ou d'une colonne** → dans le `.yml`, clé `description`.
- **Tag PII** → dans le `.yml`, sous `meta:`, avec la **justification** du classement.
- **Terme de glossaire** → au choix : un `.md` versionné dans `models/` référencé
  via `{{ doc('...') }}`, ou un fichier de glossaire à part. Justifiez votre choix.

Documentation officielle : https://docs.getdbt.com/docs/build/documentation
