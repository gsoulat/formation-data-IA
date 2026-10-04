# 9. Monitoring et surveillance

[← Retour au sommaire](README.md) | [← Précédent](08-gestion-privileges.md) | [Suivant →](10-securite.md)

## Vue d'ensemble
Le monitoring dans Snowflake permet de surveiller les performances, l'utilisation des ressources et les coûts. Cette section couvre les outils de surveillance via l'interface graphique.

Les requêtes de ce chapitre lisent les vues `SNOWFLAKE.ACCOUNT_USAGE` : elles se lancent avec le rôle `ACCOUNTADMIN`, et leurs chiffres peuvent avoir jusqu'à trois heures de retard.

---

## Tableau de bord d'activité

### Étape 1 : Accéder aux métriques
1. Allez dans **Account** > **Usage**
2. Consultez les métriques :
   - **Compute Credits** : Utilisation des warehouses
   - **Storage** : Espace utilisé par les données
   - **Data Transfer** : Volume de données transférées

## Monitoring des Warehouses

### Vue d'ensemble des warehouses
1. **Warehouses** > Sélectionnez `SALES_WH`
2. Consultez les métriques :
   - État actuel (Running/Suspended)
   - Crédits consommés
   - Temps d'exécution moyen
   - File d'attente


### Graphiques de performance
- **Utilisation dans le temps** : Tendance sur 7/30 jours
- **Concurrent queries** : Requêtes simultanées
- **Queue time** : Temps d'attente moyen

## Historique des requêtes

### Étape 1 : Accéder à l'historique
1. Allez dans **Account** > **Query History**
2. Filtrez par :
   - **User** : Voir les requêtes par utilisateur
   - **Warehouse** : Analyser l'utilisation par warehouse
   - **Status** : Identifier les requêtes échouées


### Analyser une requête
Pour chaque requête, vous pouvez voir :
- **Query ID** : Identifiant unique
- **Query Text** : Le SQL exécuté
- **Duration** : Temps d'exécution
- **Rows** : Lignes produites
- **Bytes Scanned** : Volume de données lues

### Query Profile (Profil de requête)
1. Cliquez sur une requête
2. Sélectionnez **Query Profile**
3. Analysez :
   - Plan d'exécution
   - Opérateurs les plus coûteux
   - Distribution des données


## Resource Monitors

### Créer un monitor
1. Allez dans **Account** > **Resource Monitors**
2. Cliquez sur **+ Create Resource Monitor**
3. Configurez :
   - **Name** : `SALES_WH_MONITOR`
   - **Credit Quota** : `100` (limite mensuelle)
   - **Actions** : `Suspend warehouse at 90%`


### Actions disponibles
| Seuil | Action | Description |
|-------|--------|-------------|
| 50% | Notify | Email d'alerte |
| 75% | Notify & Suspend | Alerte et suspension future |
| 90% | Suspend | Suspension immédiate |
| 100% | Suspend Immediately | Arrêt forcé |

## Métriques de stockage

### Vue globale
1. **Account** > **Usage** > **Storage**
2. Consultez :
   - Stockage actif
   - Time Travel storage
   - Fail-safe storage
   - Tendance mensuelle

### Par base de données
```sql
SELECT
    DATABASE_NAME,
    AVG(DATABASE_BYTES) / POWER(1024, 3) as AVG_GB,
    MAX(DATABASE_BYTES) / POWER(1024, 3) as MAX_GB
FROM SNOWFLAKE.ACCOUNT_USAGE.DATABASE_STORAGE_USAGE_HISTORY
WHERE USAGE_DATE > DATEADD('day', -30, CURRENT_DATE())
GROUP BY DATABASE_NAME
ORDER BY AVG_GB DESC;
```

## Alertes et notifications

### Configuration des alertes
1. **Account** > **Notifications**
2. Configurez :
   - Email de destination
   - Types d'alertes (Credits, Failures, Security)
   - Seuils de déclenchement


### Types d'alertes
- **Credit Usage** : Dépassement de seuil
- **Query Failures** : Échecs répétés
- **Login Anomalies** : Connexions suspectes
- **Data Loading** : Erreurs d'import

## Dashboard personnalisé

### Créer un dashboard
1. **Worksheets** > Nouveau worksheet
2. Créez des requêtes de monitoring
3. **Save as Dashboard**
4. Organisez les widgets

### Requêtes utiles pour dashboard

#### Top 10 requêtes coûteuses
```sql
SELECT
    QUERY_TEXT,
    USER_NAME,
    TOTAL_ELAPSED_TIME/1000 as SECONDS,
    CREDITS_USED_CLOUD_SERVICES
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME > DATEADD('day', -7, CURRENT_TIMESTAMP())
ORDER BY CREDITS_USED_CLOUD_SERVICES DESC
LIMIT 10;
```

#### Utilisation par utilisateur
```sql
SELECT
    USER_NAME,
    COUNT(*) as QUERY_COUNT,
    SUM(TOTAL_ELAPSED_TIME)/1000 as TOTAL_SECONDS,
    AVG(TOTAL_ELAPSED_TIME)/1000 as AVG_SECONDS
FROM SNOWFLAKE.ACCOUNT_USAGE.QUERY_HISTORY
WHERE START_TIME > DATEADD('day', -7, CURRENT_TIMESTAMP())
GROUP BY USER_NAME
ORDER BY TOTAL_SECONDS DESC;
```

#### Tendance des crédits
```sql
SELECT
    DATE_TRUNC('day', START_TIME) as DAY,
    SUM(CREDITS_USED_COMPUTE) as DAILY_CREDITS
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
WHERE START_TIME > DATEADD('day', -30, CURRENT_TIMESTAMP())
GROUP BY DAY
ORDER BY DAY;
```

## Optimisation basée sur le monitoring

### Identifier les problèmes

| Métrique | Problème | Solution |
|----------|----------|----------|
| Queue time élevé | Warehouse sous-dimensionné | Augmenter la taille |
| Crédits élevés | Warehouse surdimensionné | Réduire la taille |
| Queries longues | Manque d'optimisation | Revoir les requêtes |
| Storage élevé | Données non nettoyées | Implémenter retention policy |

### Actions correctives
1. **Redimensionner warehouses** selon l'usage
2. **Optimiser les requêtes** fréquentes
3. **Créer des vues matérialisées** pour les agrégations
4. **Implémenter le clustering** sur grandes tables

## Coûts et budget

### Estimation des coûts
- **Compute** : $2-4 per credit (selon édition)
- **Storage** : $23-40 per TB/mois
- **Data Transfer** : Variable selon région

### Calculateur de coûts
```sql
WITH credit_price AS (
    SELECT 3.00 as price_per_credit -- Ajuster selon votre contrat
)
SELECT
    SUM(CREDITS_USED_COMPUTE) as TOTAL_CREDITS,
    SUM(CREDITS_USED_COMPUTE) * price_per_credit as ESTIMATED_COST_USD
FROM SNOWFLAKE.ACCOUNT_USAGE.WAREHOUSE_METERING_HISTORY
CROSS JOIN credit_price
WHERE START_TIME > DATE_TRUNC('month', CURRENT_DATE())
GROUP BY price_per_credit;
```

## Bonnes pratiques de monitoring

### ✅ À faire
1. **Vérifier quotidiennement** les métriques clés
2. **Configurer des alertes** proactives
3. **Documenter** les anomalies
4. **Optimiser** régulièrement
5. **Former** les utilisateurs

### 📊 KPIs à suivre
- Utilisation des crédits (daily/monthly)
- Top 10 requêtes coûteuses
- Taux d'échec des requêtes
- Croissance du stockage
- Temps de réponse moyen

## Export et rapports

### Génération de rapports
1. **Account** > **Usage** > **Download**
2. Formats disponibles :
   - CSV
   - JSON
   - PDF (certains rapports)

### Automatisation
- API REST pour extraction programmatique
- Intégration avec outils BI (Tableau, PowerBI)
- Scheduled tasks pour rapports réguliers

## ✅ Points de vérification
- [ ] Tableau de bord consulté
- [ ] Resource Monitor créé
- [ ] Historique des requêtes analysé
- [ ] Alertes configurées
- [ ] Dashboard personnalisé créé
- [ ] KPIs identifiés

---

[Suivant : Sécurité : rôles, droits et utilisateurs de service en SQL →](10-securite.md)