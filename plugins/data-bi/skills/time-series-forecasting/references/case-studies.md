# Etudes de Cas — Forecasting en Production

## Vue d'ensemble

Quatre etudes de cas reelles illustrent le cycle complet du forecasting : contexte
metier, preparation des donnees, choix et justification du modele, validation,
deploiement et mesure d'impact. Chaque cas inclut les erreurs commises et les
lecons apprises.

---

## Cas 1 — E-commerce Demand Forecasting : 500 SKUs avec Prophet

### 1.1 Contexte

**Industrie** : Retailer e-commerce mode et accessoires, 3 pays europeens
**Probleme** : Ruptures de stock frequentes (-23% objectif) et surstocks (-18% objectif)
menant a des promotions forcees. Previsions manuelles dans Excel par les acheteurs :
horizon 8 semaines, MAPE ~28%.
**Objectif** : Pipeline automatise de previsions 12 semaines pour 500 SKUs actifs,
integration avec systeme de reapprovisionnement (ERP SAP).
**Contrainte** : Budget data science limite, equipe de 2 personnes. Modeles doivent
etre re-entraines chaque semaine automatiquement.

### 1.2 Donnees et Preparation

```python
import pandas as pd
import numpy as np
from prophet import Prophet
from prophet.diagnostics import cross_validation, performance_metrics
import logging
from concurrent.futures import ProcessPoolExecutor, as_completed
from tqdm import tqdm

logger = logging.getLogger(__name__)

# Structure des donnees source (entrepot SQL)
# TABLE: ventes_quotidiennes (sku_id, date, quantite_vendue, prix_vente, pays)
# TABLE: calendrier_marketing (date, type_evenement, pays, intensite_promo)
# TABLE: historique_stock (sku_id, date, stock_disponible)

def charger_donnees_sku(conn, sku_id: str,
                         date_debut: str = '2021-01-01') -> pd.DataFrame:
    """
    Charge et prepare les donnees pour un SKU specifique.
    Gere : jours sans ventes (stock = 0), doublons, outliers saisonniers.
    """
    query = f"""
    SELECT
        v.date                          AS ds,
        SUM(v.quantite_vendue)          AS y_brut,
        AVG(v.prix_vente)               AS prix_moyen,
        MAX(COALESCE(s.stock_disponible, 1)) AS stock_dispo,
        MAX(m.intensite_promo)          AS promo_intensite
    FROM ventes_quotidiennes v
    LEFT JOIN historique_stock s ON s.sku_id = v.sku_id AND s.date = v.date
    LEFT JOIN calendrier_marketing m ON m.date = v.date AND m.pays = v.pays
    WHERE v.sku_id = '{sku_id}'
      AND v.date >= '{date_debut}'
    GROUP BY v.date
    ORDER BY v.date
    """
    df = pd.read_sql(query, conn)
    df['ds'] = pd.to_datetime(df['ds'])

    # Reindexer pour inclure tous les jours (meme sans ventes)
    date_range = pd.date_range(df['ds'].min(), df['ds'].max(), freq='D')
    df = df.set_index('ds').reindex(date_range).reset_index()
    df.columns = ['ds'] + list(df.columns[1:])

    # Ventes = 0 si stock absent (rupture) → NaN pour Prophet
    df['y'] = df['y_brut'].fillna(0)
    df.loc[df['stock_dispo'] == 0, 'y'] = np.nan  # rupture stock = donnee manquante

    # Outliers : promotions flash => conserver mais marquer
    df['promo_intensite'] = df['promo_intensite'].fillna(0)
    df['prix_moyen'] = df['prix_moyen'].ffill().bfill()

    # Normaliser le prix (variation par rapport au prix habituel)
    prix_median = df['prix_moyen'].median()
    df['remise_relative'] = (prix_median - df['prix_moyen']) / prix_median
    df['remise_relative'] = df['remise_relative'].clip(0, 0.8)

    return df


def detecter_outliers_ventes(df: pd.DataFrame,
                              fenetre: int = 21,
                              seuil: float = 4.0) -> pd.DataFrame:
    """
    Detecte et remplace les outliers non promotionnels par NaN.
    Les pics promotionnels (promo_intensite > 0) sont preserves.
    """
    df = df.copy()
    rolling_med = df['y'].rolling(fenetre, center=True, min_periods=5).median()
    rolling_std = df['y'].rolling(fenetre, center=True, min_periods=5).std()

    score = (df['y'] - rolling_med) / (rolling_std + 1e-4)
    outlier_mask = (np.abs(score) > seuil) & (df['promo_intensite'] == 0)

    n_outliers = outlier_mask.sum()
    if n_outliers > 0:
        logger.info(f"  {n_outliers} outliers non-promotionnels remplace par NaN")
        df.loc[outlier_mask, 'y'] = np.nan

    return df
```

### 1.3 Modele Prophet Multi-SKU

```python
def creer_jours_feries_multi_pays(pays: list) -> pd.DataFrame:
    """Jours feries combines pour FR, DE, GB."""
    rows = []
    # Simplifie — en production : utiliser la lib `holidays`
    import holidays as hd
    for annee in [2021, 2022, 2023, 2024, 2025]:
        for pays_code in pays:
            try:
                feries = hd.country_holidays(pays_code, years=annee)
                for date, nom in feries.items():
                    rows.append({
                        'holiday': f"{nom}_{pays_code}",
                        'ds': pd.Timestamp(date),
                        'lower_window': -1,
                        'upper_window': 1
                    })
            except Exception:
                pass
    return pd.DataFrame(rows).drop_duplicates(subset=['holiday', 'ds'])


def entrainer_prophet_sku(df: pd.DataFrame,
                           jours_feries: pd.DataFrame,
                           sku_id: str) -> dict:
    """
    Entraine Prophet pour un SKU. Gere la logistique si la serie
    semble avoir un plafond naturel (produit en fin de vie).
    """
    # Verifier si la serie est trop courte
    n_points_valides = df['y'].notna().sum()
    if n_points_valides < 60:
        logger.warning(f"SKU {sku_id}: seulement {n_points_valides} points valides")
        return None

    modele = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        holidays=jours_feries,
        seasonality_mode='multiplicative',
        changepoint_prior_scale=0.05,    # conservateur pour eviter overfitting
        seasonality_prior_scale=10.0,
        holidays_prior_scale=10.0,
        interval_width=0.80,             # IC 80% pour systeme reappro
        uncertainty_samples=500
    )

    # Regresseur : remise/promotion
    modele.add_regressor('remise_relative', prior_scale=5.0, standardize=True)

    modele.fit(df[['ds', 'y', 'remise_relative']].dropna(subset=['ds']))
    return modele


def pipeline_previsions_batch(conn,
                               liste_skus: list,
                               horizon_semaines: int = 12,
                               n_workers: int = 4) -> pd.DataFrame:
    """
    Pipeline complet : charge, entraine et predit pour tous les SKUs.
    Utilise multiprocessing pour paralleliser.
    """
    jours_feries = creer_jours_feries_multi_pays(['FR', 'DE', 'GB'])
    horizon_jours = horizon_semaines * 7
    tous_resultats = []

    # Preparation des futures promotions (depuis le calendrier marketing)
    # En production : charger depuis la BDD
    dates_futures = pd.date_range(
        pd.Timestamp.today(), periods=horizon_jours, freq='D'
    )
    df_promo_futur = pd.DataFrame({
        'ds': dates_futures,
        'remise_relative': 0.0  # par defaut : pas de promo
    })

    for sku_id in tqdm(liste_skus, desc="Entrainement SKUs"):
        try:
            df_sku = charger_donnees_sku(conn, sku_id)
            df_sku = detecter_outliers_ventes(df_sku)

            modele = entrainer_prophet_sku(df_sku, jours_feries, sku_id)
            if modele is None:
                continue

            futur = modele.make_future_dataframe(periods=horizon_jours)
            futur = futur.merge(df_promo_futur, on='ds', how='left')
            futur['remise_relative'] = futur['remise_relative'].fillna(0)

            forecast = modele.predict(futur)
            forecast_horizon = forecast[
                forecast['ds'] > df_sku['ds'].max()
            ].copy()

            # Formater pour le systeme de reappro SAP
            forecast_horizon['sku_id'] = sku_id
            forecast_horizon['semaine'] = forecast_horizon['ds'].dt.isocalendar().week
            forecast_horizon['annee'] = forecast_horizon['ds'].dt.year
            forecast_horizon['quantite_prevue'] = np.maximum(
                0, forecast_horizon['yhat'].round()
            ).astype(int)
            forecast_horizon['quantite_min'] = np.maximum(
                0, forecast_horizon['yhat_lower'].round()
            ).astype(int)
            forecast_horizon['quantite_max'] = np.maximum(
                0, forecast_horizon['yhat_upper'].round()
            ).astype(int)

            tous_resultats.append(forecast_horizon[[
                'sku_id', 'ds', 'semaine', 'annee',
                'quantite_prevue', 'quantite_min', 'quantite_max'
            ]])

        except Exception as e:
            logger.error(f"Erreur SKU {sku_id}: {e}")

    return pd.concat(tous_resultats, ignore_index=True)
```

### 1.4 Validation et Resultats

Walk-forward validation sur 6 mois, horizon 8 semaines :
- **MAPE median** : 14.2% (vs 28% manuel Excel)
- **MAPE 90e percentile** : 34.1% (SKUs a faible volume)
- **Coverage IC 80%** : 81.3% (bien calibre)
- **Baseline naive saisonnier** : MAPE 19.7% → modele bat le baseline de 28%

**Impact metier mesure sur 6 mois post-deploiement :**
- Ruptures de stock : -23% (objectif atteint)
- Surstocks : -18% (objectif atteint)
- Reductions pour ecoulement : -12% du chiffre promos forcees
- Temps acheteur sur previsions : -70% (de 3h/semaine a 30 min)

### 1.5 Lecons Apprises

1. **Donnees de stock manquantes = biais majeur** : sans correction des jours
   de rupture (ventes = 0 mais demande reelle > 0), le modele sous-estime
   systematiquement. Solution : utiliser le stock disponible comme masque.

2. **SKUs a faible volume** : MAPE instable pour SKUs <5 unites/jour.
   Solution : clustering des SKUs similaires et modele groupe.

3. **Saisonnalite multiplicative obligatoire** : les pics du Black Friday et des
   soldes etaient 8-15x le volume normal. Mode additif sous-estimait les pics.

4. **Re-entrainement hebdomadaire critique** : sans re-entrainement, la MAPE
   degradait de +4% par mois. Airflow DAG configure pour samedi minuit.

---

## Cas 2 — SaaS Revenue Forecasting : MRR sur 6 Mois

### 2.1 Contexte

**Industrie** : SaaS B2B, 3,200 comptes clients, ACV moyen 18K EUR/an
**Probleme** : Budget annuel base sur des previsions MRR (Monthly Recurring Revenue)
avec ecart moyen de 12% vs reel. Le CFO exige une precision < 5% MAPE.
**Objectif** : Modele de prevision du MRR total a 6 mois, avec decomposition par
type de mouvement (nouveau, expansion, churn, reactivation).
**Donnees** : Evenements d'abonnement depuis le CRM (Salesforce), 3 ans d'historique.

### 2.2 Architecture — Modelisation Separee par Cohorte

La cle de ce projet : ne pas modeliser le MRR agregee directement.
Decomposer en 4 composantes independantes avec des drivers differents.

```python
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX
import pmdarima as pm

# Composantes du MRR
# MRR_total(t) = MRR_new(t) + MRR_expansion(t) - MRR_churn(t) + MRR_reactivation(t)

def charger_mouvements_mrr(conn, date_debut: str = '2021-01-01') -> pd.DataFrame:
    """
    Extrait les mouvements MRR depuis Salesforce/BDD CRM.
    Chaque ligne = un evenement d'abonnement.
    """
    query = """
    SELECT
        DATE_TRUNC('month', evenement_date)  AS mois,
        SUM(CASE WHEN type_mouvement = 'new'         THEN mrr_delta ELSE 0 END) AS mrr_new,
        SUM(CASE WHEN type_mouvement = 'expansion'   THEN mrr_delta ELSE 0 END) AS mrr_expansion,
        SUM(CASE WHEN type_mouvement = 'churn'       THEN ABS(mrr_delta) ELSE 0 END) AS mrr_churn,
        SUM(CASE WHEN type_mouvement = 'reactivation' THEN mrr_delta ELSE 0 END) AS mrr_reactiv,
        SUM(mrr_delta) AS mrr_net_change,
        MAX(mrr_cumule) AS mrr_total_eom  -- end of month
    FROM abonnements_evenements
    WHERE evenement_date >= '{date_debut}'
    GROUP BY DATE_TRUNC('month', evenement_date)
    ORDER BY mois
    """
    df = pd.read_sql(query, conn)
    df['mois'] = pd.to_datetime(df['mois'])
    return df.set_index('mois')


def prevoir_composante_sarima(serie: pd.Series,
                               nom: str,
                               horizon: int = 6,
                               regresseurs_train: pd.DataFrame = None,
                               regresseurs_futur: pd.DataFrame = None) -> dict:
    """
    Prevision d'une composante MRR par SARIMA automatique.
    """
    print(f"\n--- Modelisation {nom} ---")

    if regresseurs_train is not None:
        modele = pm.auto_arima(
            serie,
            exogenous=regresseurs_train,
            seasonal=True, m=12,
            max_p=3, max_q=3, max_P=2, max_Q=2,
            information_criterion='aic',
            stepwise=True, trace=True,
            suppress_warnings=True
        )
    else:
        modele = pm.auto_arima(
            serie,
            seasonal=True, m=12,
            max_p=3, max_q=3, max_P=2, max_Q=2,
            information_criterion='aic',
            stepwise=True, trace=True,
            suppress_warnings=True
        )

    print(f"Ordre selectionne: {modele.order} x {modele.seasonal_order}")
    print(f"AIC: {modele.aic():.2f}")

    if regresseurs_futur is not None:
        previsions, conf_int = modele.predict(
            n_periods=horizon,
            exogenous=regresseurs_futur,
            return_conf_int=True,
            alpha=0.10  # IC 90%
        )
    else:
        previsions, conf_int = modele.predict(
            n_periods=horizon,
            return_conf_int=True,
            alpha=0.10
        )

    return {
        'nom': nom,
        'modele': modele,
        'previsions': previsions,
        'ci_lower': conf_int[:, 0],
        'ci_upper': conf_int[:, 1]
    }


def pipeline_mrr_forecast(df_mrr: pd.DataFrame,
                           df_pipeline_commercial: pd.DataFrame,
                           horizon: int = 6) -> pd.DataFrame:
    """
    Pipeline complet de prevision MRR decompose.

    df_pipeline_commercial : signaux leading (nb deals en phase finale,
    taux de conversion 90j) disponibles pour les futurs mois.
    """
    composantes = {}

    # 1. MRR New : correlate avec le pipeline commercial (leading indicator)
    regresseurs_new = df_pipeline_commercial[['deals_phase4', 'taux_conv_90j']]
    composantes['new'] = prevoir_composante_sarima(
        df_mrr['mrr_new'],
        nom='MRR New',
        horizon=horizon,
        regresseurs_train=regresseurs_new.loc[df_mrr.index],
        regresseurs_futur=regresseurs_new.tail(horizon)
    )

    # 2. MRR Expansion : depend du MRR base installee (lagged)
    composantes['expansion'] = prevoir_composante_sarima(
        df_mrr['mrr_expansion'],
        nom='MRR Expansion',
        horizon=horizon
    )

    # 3. MRR Churn : trend seculaire + saisonnalite (pic T4)
    composantes['churn'] = prevoir_composante_sarima(
        df_mrr['mrr_churn'],
        nom='MRR Churn',
        horizon=horizon
    )

    # 4. MRR Reactivation : faible volume, simple lissage exponentiel
    from statsmodels.tsa.holtwinters import SimpleExpSmoothing
    ses = SimpleExpSmoothing(df_mrr['mrr_reactiv'],
                             initialization_method='estimated')
    ses_fit = ses.fit(optimized=True)
    composantes['reactivation'] = {
        'nom': 'MRR Reactivation',
        'previsions': ses_fit.forecast(horizon)
    }

    # 5. Agregation
    mois_futurs = pd.date_range(
        df_mrr.index[-1] + pd.offsets.MonthBegin(1),
        periods=horizon, freq='MS'
    )

    df_prevision = pd.DataFrame(index=mois_futurs)
    df_prevision.index.name = 'mois'
    df_prevision['mrr_new_prevu'] = composantes['new']['previsions']
    df_prevision['mrr_expansion_prevu'] = composantes['expansion']['previsions']
    df_prevision['mrr_churn_prevu'] = composantes['churn']['previsions']
    df_prevision['mrr_reactiv_prevu'] = composantes['reactivation']['previsions'].values

    # MRR total = dernier MRR connu + mouvements nets prevus
    dernier_mrr = float(df_mrr['mrr_total_eom'].iloc[-1])
    mrr_variation_nette = (
        df_prevision['mrr_new_prevu'] +
        df_prevision['mrr_expansion_prevu'] -
        df_prevision['mrr_churn_prevu'] +
        df_prevision['mrr_reactiv_prevu']
    )
    df_prevision['mrr_total_prevu'] = dernier_mrr + mrr_variation_nette.cumsum()

    # Intervalles de confiance (propagation des IC composantes)
    df_prevision['mrr_total_ci_low'] = dernier_mrr + (
        composantes['new']['ci_lower'] +
        composantes['expansion']['ci_lower'] -
        composantes['churn']['ci_upper'] +
        df_prevision['mrr_reactiv_prevu'] * 0.8
    ).cumsum()
    df_prevision['mrr_total_ci_high'] = dernier_mrr + (
        composantes['new']['ci_upper'] +
        composantes['expansion']['ci_upper'] -
        composantes['churn']['ci_lower'] +
        df_prevision['mrr_reactiv_prevu'] * 1.2
    ).cumsum()

    print("\n=== Previsions MRR (EUR) ===")
    print(df_prevision[['mrr_total_prevu', 'mrr_total_ci_low',
                          'mrr_total_ci_high']].round(0).to_string())

    return df_prevision
```

### 2.3 Validation et Resultats

**Walk-forward sur 12 mois, horizon 6 mois :**
- **MAPE MRR total** : 4.2% (objectif < 5% atteint)
- **MAPE MRR New** : 8.1% (plus volatile, depend du pipeline)
- **MAPE MRR Churn** : 5.8%
- **Coverage IC 90%** : 87.9%
- **Baseline budget manuel** : MAPE 12.1% → amelioration de 65%

### 2.4 Lecons Apprises

1. **Modelisation decomposee > agregee** : modeliser le MRR total directement
   donnait MAPE 9.3%. La decomposition par composante et la reaggregation
   ont reduit la MAPE de moitie.

2. **Leading indicators critiques** : le pipeline commercial (deals en phase 4)
   est un regresseur avec lag de 2-3 mois. Sans ce regresseur, la MAPE du
   MRR New etait de 13.2% vs 8.1% avec.

3. **IC trop larges sans decomposition** : propager les IC composante par
   composante permet des IC plus serres qu'un IC sur le total.

4. **T4 Churn toujours sous-estime** : les entreprises resiliient a la
   rencontre annuelle (budget Q4). Ajouter une dummy T4 a reduit le biais.

---

## Cas 3 — Capacity Planning Cloud : Prediction CPU/RAM pour 340K EUR/an

### 3.1 Contexte

**Industrie** : Fintech, infrastructure AWS (EC2 + RDS), 180 microservices
**Probleme** : Surprovisionnement systematique des instances EC2 et RDS.
Les equipes infra provisionnent au "peak + 40% marge" sans modelisation.
**Objectif** : Predire l'utilisation CPU/RAM a 2 semaines pour permettre
le scaling automatique proactif (avant les pics, pas pendant).
**Metrique de succes** : Reduction des couts AWS de 20% sans SLA degrade.

### 3.2 Structure des Donnees

```python
import pandas as pd
import numpy as np
from statsmodels.tsa.statespace.sarimax import SARIMAX

# Donnees : metriques CloudWatch agregees toutes les 5 minutes
# → re-echantillonnage horaire pour la modelisation

def charger_metriques_cloudwatch(service_name: str,
                                  date_debut: str,
                                  resolution_minutes: int = 60) -> pd.DataFrame:
    """
    Charge les metriques depuis S3 (export CloudWatch) et reagrege.
    """
    # Simulation structure reelle
    df = pd.read_parquet(
        f"s3://monitoring-data/cloudwatch/{service_name}/",
        filters=[('timestamp', '>=', date_debut)]
    )

    df['timestamp'] = pd.to_datetime(df['timestamp'])
    df = df.set_index('timestamp').resample(f'{resolution_minutes}T').agg({
        'cpu_percent': 'mean',
        'memory_percent': 'max',   # max pour capture pics memoire
        'request_count': 'sum',
        'p99_latency_ms': 'max'
    })

    return df


def enrichir_avec_calendrier(df: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute les features temporelles et evenements metier.
    Ces variables servent de regresseurs exogenes dans SARIMA.
    """
    df = df.copy()

    # Features temporelles (stationnarisees)
    df['heure_jour'] = df.index.hour
    df['jour_semaine'] = df.index.dayofweek
    df['est_weekend'] = (df['jour_semaine'] >= 5).astype(int)
    df['est_heure_pic'] = df['heure_jour'].isin([9, 10, 11, 14, 15, 16]).astype(int)

    # Evenements metier connus : dates de paiement (pic de charge)
    # 1 et 15 de chaque mois = vagues de batch payments
    df['est_date_paiement'] = (
        (df.index.day == 1) | (df.index.day == 15)
    ).astype(int)

    # Campagnes marketing (depuis calendrier externe)
    # En production : merger avec table calendrier_marketing
    df['est_campagne_active'] = 0  # placeholder

    return df
```

### 3.3 Modele SARIMA avec Regresseurs

```python
def construire_modele_capacite(df: pd.DataFrame,
                                metrique: str = 'cpu_percent',
                                periode_saisonniere: int = 24,
                                horizon_heures: int = 336) -> dict:
    """
    SARIMA(p,d,q)(P,D,Q)24 pour prediction horaire.
    periode=24 : saisonnalite journaliere pour donnees horaires.

    horizon_heures=336 : 2 semaines * 7 jours * 24 heures
    """
    regresseurs = ['est_weekend', 'est_heure_pic', 'est_date_paiement']

    serie = df[metrique].dropna()
    exog = df[regresseurs].loc[serie.index]

    # Selection automatique de l'ordre
    import pmdarima as pm
    modele_auto = pm.auto_arima(
        serie,
        exogenous=exog,
        seasonal=True,
        m=periode_saisonniere,
        max_p=3, max_q=3,
        max_P=2, max_Q=2,
        d=None, D=None,
        information_criterion='aic',
        stepwise=True,
        suppress_warnings=True,
        error_action='ignore',
        trace=True
    )

    print(f"Modele selectionne: {modele_auto.order} x {modele_auto.seasonal_order}")
    print(f"AIC: {modele_auto.aic():.2f}")

    # Construire les regresseurs futurs pour l'horizon
    dates_futures = pd.date_range(
        serie.index[-1] + pd.Timedelta(hours=1),
        periods=horizon_heures, freq='H'
    )
    df_futur = pd.DataFrame(index=dates_futures)
    df_futur['est_weekend'] = (df_futur.index.dayofweek >= 5).astype(int)
    df_futur['est_heure_pic'] = df_futur.index.hour.isin(
        [9, 10, 11, 14, 15, 16]
    ).astype(int)
    df_futur['est_date_paiement'] = (
        (df_futur.index.day == 1) | (df_futur.index.day == 15)
    ).astype(int)

    previsions, conf_int = modele_auto.predict(
        n_periods=horizon_heures,
        exogenous=df_futur[regresseurs].values,
        return_conf_int=True,
        alpha=0.05  # IC 95%
    )

    df_previsions = pd.DataFrame({
        'ds': dates_futures,
        'prevu': np.clip(previsions, 0, 100),
        'ci_lower': np.clip(conf_int[:, 0], 0, 100),
        'ci_upper': np.clip(conf_int[:, 1], 0, 100)
    })

    return {
        'modele': modele_auto,
        'previsions': df_previsions,
        'metrique': metrique
    }


def generer_alertes_capacite(df_previsions: pd.DataFrame,
                              seuil_cpu: float = 75.0,
                              seuil_memoire: float = 85.0) -> pd.DataFrame:
    """
    Genere des alertes si la prevision depasse les seuils.
    Alerte declenchee si ci_upper > seuil pour anticiper avant le pic.
    """
    alertes = []

    for _, row in df_previsions.iterrows():
        if row['ci_upper'] > seuil_cpu and row['metrique'] == 'cpu':
            alertes.append({
                'timestamp': row['ds'],
                'type': 'CPU_THRESHOLD',
                'valeur_prevue': round(row['prevu'], 1),
                'valeur_pire_cas': round(row['ci_upper'], 1),
                'seuil': seuil_cpu,
                'recommandation': 'Scale-out preemptif recommande',
                'horizon_heures': int((row['ds'] - pd.Timestamp.now()).total_seconds() / 3600)
            })

    df_alertes = pd.DataFrame(alertes)
    if not df_alertes.empty:
        print(f"ALERTES CAPACITE ({len(df_alertes)} evenements prevus):")
        print(df_alertes[['timestamp', 'type', 'valeur_pire_cas',
                           'seuil', 'horizon_heures']].to_string(index=False))
    return df_alertes
```

### 3.4 Resultats et Impact

**Validation (walk-forward 4 semaines, horizon 2 semaines) :**
- **MAPE CPU** : 8.3% (horaire)
- **MAPE RAM** : 6.7%
- **False alarms** (alertes injustifiees) : 4.2% des alertes
- **Miss rate** (pics non detectes) : 1.8%

**Impact financier mesure sur 12 mois :**
- Reduction des instances over-provisionnees : -31% du parc EC2 reserved
- Economies AWS annuelles : **340K EUR** (objectif 20% atteint a 27%)
- SLA P99 latence : inchange (99.97% vs 99.98% avant)
- Incidents de saturation evites : 14 events dont 3 critiques

### 3.5 Lecons Apprises

1. **Saisonnalite hebdomadaire cachee** : la saisonnalite majeure etait
   hebdomadaire (7*24=168), pas journaliere. SARIMA avec m=24 manquait
   les creux du weekend. Solution : STL decomposition d'abord pour identifier.

2. **Les dates de paiement sont le regresseur le plus puissant** : coeff
   standardise +18.3% de CPU. Sans ce regresseur, les pics du 1er et 15
   etaient systematiquement sous-estimes.

3. **Alerte sur ci_upper pas yhat** : declencher l'alerte sur la prevision
   centrale (yhat) generait 23% de faux positifs. Utiliser le 95e percentile
   (ci_upper) a reduit les faux positifs a 4.2%.

4. **Re-entrainement bimensuel suffit** : les patterns de charge sont
   stables. Re-entrainement mensuel = bon compromis stabilite/fraicheur.

---

## Cas 4 — Detection d'Anomalies Fraude Bancaire : STL + Isolation Forest

### 4.1 Contexte

**Industrie** : Banque regionale, 2.3M de transactions/jour
**Probleme** : La fraude survient en jours atypiques (volumes anormaux,
repartition horaire inhabituelle). Les regles statiques (seuils fixes) generaient
trop de faux positifs (800/jour) et rataient les fraudes sophistiquees.
**Objectif** : Detecter les jours anormaux au niveau macro (pas transaction
individuelle) pour declencher une surveillance renforcee.
**Contrainte** : Pipeline doit tourner a J+1 (donnees du jour J disponibles
a 6h00 le lendemain).

### 4.2 Architecture — STL + Isolation Forest

```python
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import STL
from sklearn.ensemble import IsolationForest
from sklearn.preprocessing import StandardScaler
import matplotlib.pyplot as plt
from typing import Optional

def charger_agregats_journaliers(conn, date_debut: str) -> pd.DataFrame:
    """
    Agregats de transactions journaliers pour la detection macro-anomalies.
    Plusieurs dimensions aggregees = plus robuste que le volume seul.
    """
    query = f"""
    SELECT
        DATE(transaction_datetime)              AS date_jour,
        COUNT(*)                                AS nb_transactions,
        SUM(montant_eur)                        AS volume_eur,
        AVG(montant_eur)                        AS ticket_moyen,
        COUNT(DISTINCT compte_id)               AS comptes_actifs,
        COUNT(DISTINCT pays_marchand)           AS pays_differents,
        SUM(CASE WHEN heure < 6 OR heure > 22
                 THEN 1 ELSE 0 END)             AS transactions_hors_heures,
        SUM(CASE WHEN montant_eur > 5000
                 THEN 1 ELSE 0 END)             AS gros_montants,
        AVG(CASE WHEN rejet_code IS NOT NULL
                 THEN 1.0 ELSE 0.0 END)         AS taux_rejet
    FROM transactions
    WHERE transaction_datetime >= '{date_debut}'
      AND statut IN ('COMPLETED', 'REJECTED')
    GROUP BY DATE(transaction_datetime)
    ORDER BY date_jour
    """
    df = pd.read_sql(query, conn)
    df['date_jour'] = pd.to_datetime(df['date_jour'])
    return df.set_index('date_jour')


def decomposer_features_stl(df: pd.DataFrame,
                              periode: int = 7) -> pd.DataFrame:
    """
    Applique STL a chaque feature numerique.
    Extrait les residus : ce qui reste apres avoir retire tendance + saisonnalite.
    Les residus anormalement grands signalent des anomalies.
    """
    features_numeriques = [
        'nb_transactions', 'volume_eur', 'ticket_moyen',
        'comptes_actifs', 'transactions_hors_heures',
        'gros_montants', 'taux_rejet'
    ]

    df_residus = pd.DataFrame(index=df.index)

    for feature in features_numeriques:
        serie = df[feature].dropna()

        if len(serie) < 2 * periode:
            # Pas assez de donnees pour STL → utiliser la differentiation simple
            df_residus[f'{feature}_resid'] = serie.diff().fillna(0)
            continue

        try:
            stl = STL(serie, period=periode, seasonal=7, robust=True)
            result = stl.fit()
            df_residus[f'{feature}_resid'] = result.resid
            df_residus[f'{feature}_trend'] = result.trend
            df_residus[f'{feature}_seasonal'] = result.seasonal
        except Exception as e:
            print(f"Erreur STL {feature}: {e}")
            df_residus[f'{feature}_resid'] = serie.diff().fillna(0)

    return df_residus


def detecter_anomalies_isolation_forest(df_residus: pd.DataFrame,
                                         contamination: float = 0.02,
                                         n_estimators: int = 200,
                                         random_state: int = 42) -> pd.DataFrame:
    """
    Isolation Forest sur les residus STL multi-dimensionnels.

    contamination : proportion de points consideres comme anomalies
    (2% = environ 7 jours sur une annee, calibrer selon risque acceptable)
    """
    # Selectionner uniquement les colonnes residus
    cols_residus = [c for c in df_residus.columns if c.endswith('_resid')]
    X = df_residus[cols_residus].fillna(0)

    # Standardisation (Isolation Forest sensible a l'echelle)
    scaler = StandardScaler()
    X_scaled = scaler.fit_transform(X)

    # Entrainement
    clf = IsolationForest(
        contamination=contamination,
        n_estimators=n_estimators,
        max_samples='auto',
        random_state=random_state,
        n_jobs=-1
    )
    clf.fit(X_scaled)

    # Scores : plus negatif = plus anormal
    scores = clf.score_samples(X_scaled)  # log-likelihood, negatif = anormal
    predictions = clf.predict(X_scaled)   # 1 = normal, -1 = anomalie

    df_resultats = df_residus.copy()
    df_resultats['anomalie_score'] = scores
    df_resultats['est_anomalie'] = predictions == -1
    df_resultats['rang_anomalie'] = (-scores).argsort().argsort() + 1  # rang 1 = plus anormal

    n_anomalies = df_resultats['est_anomalie'].sum()
    print(f"Anomalies detectees: {n_anomalies} jours "
          f"({n_anomalies/len(df_resultats)*100:.1f}%)")

    return df_resultats, clf, scaler


def expliquer_anomalie(date_anomalie: pd.Timestamp,
                        df_original: pd.DataFrame,
                        df_residus: pd.DataFrame,
                        top_n: int = 3) -> dict:
    """
    Explique quelles features contribuent le plus a l'anomalie.
    Calcule la contribution de chaque feature au score d'anomalie.
    """
    cols_residus = [c for c in df_residus.columns if c.endswith('_resid')]

    if date_anomalie not in df_residus.index:
        return {'erreur': f'Date {date_anomalie} non trouvee'}

    residus_jour = df_residus.loc[date_anomalie, cols_residus]

    # Score de contribution : residu normalise par la std historique
    contributions = {}
    for col in cols_residus:
        std_col = df_residus[col].std()
        feature_nom = col.replace('_resid', '')
        contributions[feature_nom] = {
            'residu': round(float(residus_jour[col]), 4),
            'z_score': round(float(residus_jour[col] / (std_col + 1e-8)), 2),
            'valeur_reelle': round(float(df_original.loc[date_anomalie, feature_nom])
                                   if feature_nom in df_original.columns else np.nan, 2)
        }

    # Trier par z_score absolu
    top_features = sorted(
        contributions.items(),
        key=lambda x: abs(x[1]['z_score']),
        reverse=True
    )[:top_n]

    explication = {
        'date': str(date_anomalie.date()),
        'top_features_anomales': {k: v for k, v in top_features},
        'interpretation': f"Anomalie principalement due a: "
                          f"{', '.join([f[0] for f in top_features])}"
    }
    return explication
```

### 4.3 Pipeline de Production et Alerting

```python
import json
from datetime import datetime, timedelta

class PipelineDetectionFraude:
    """
    Pipeline journalier J+1 de detection d'anomalies.
    Tourne a 6h00 chaque matin via Airflow.
    """

    def __init__(self, conn, seuil_alerte_rang: int = 10,
                 lookback_jours: int = 365):
        self.conn = conn
        self.seuil_alerte_rang = seuil_alerte_rang
        self.lookback_jours = lookback_jours
        self.clf = None
        self.scaler = None

    def executer(self, date_analyse: Optional[str] = None) -> dict:
        """Execution quotidienne complete."""
        if date_analyse is None:
            date_analyse = (datetime.today() - timedelta(days=1)).strftime('%Y-%m-%d')

        date_debut = (
            pd.Timestamp(date_analyse) - pd.Timedelta(days=self.lookback_jours)
        ).strftime('%Y-%m-%d')

        print(f"\n=== Pipeline Detection Fraude — {date_analyse} ===")

        # 1. Charger donnees
        df_raw = charger_agregats_journaliers(self.conn, date_debut)
        print(f"Donnees chargees: {len(df_raw)} jours")

        # 2. Decomposition STL
        df_residus = decomposer_features_stl(df_raw, periode=7)

        # 3. Detection anomalies
        df_resultats, self.clf, self.scaler = detecter_anomalies_isolation_forest(
            df_residus, contamination=0.02
        )

        # 4. Analyser le jour sous analyse
        date_ts = pd.Timestamp(date_analyse)
        if date_ts in df_resultats.index:
            score = df_resultats.loc[date_ts, 'anomalie_score']
            rang = df_resultats.loc[date_ts, 'rang_anomalie']
            est_anomalie = df_resultats.loc[date_ts, 'est_anomalie']

            rapport = {
                'date': date_analyse,
                'score': round(float(score), 4),
                'rang': int(rang),
                'est_anomalie': bool(est_anomalie),
                'alerte_declenchee': rang <= self.seuil_alerte_rang
            }

            if rapport['alerte_declenchee']:
                explication = expliquer_anomalie(date_ts, df_raw, df_residus)
                rapport['explication'] = explication
                self.envoyer_alerte(rapport)
            else:
                print(f"Jour {date_analyse}: NORMAL (rang {rang}/{len(df_resultats)})")

        else:
            rapport = {'erreur': f'Date {date_analyse} absente des donnees'}

        return rapport

    def envoyer_alerte(self, rapport: dict) -> None:
        """Envoie l'alerte via webhook (Slack, PagerDuty, etc.)"""
        import requests
        webhook_url = "https://hooks.slack.com/services/EXAMPLE_TOKEN"

        features_top = rapport.get('explication', {}).get(
            'top_features_anomales', {}
        )
        features_str = "\n".join([
            f"  - {k}: z-score={v['z_score']}"
            for k, v in features_top.items()
        ])

        message = {
            "text": f":rotating_light: *ALERTE ANOMALIE FRAUDE*",
            "blocks": [{
                "type": "section",
                "text": {
                    "type": "mrkdwn",
                    "text": (
                        f"*Date:* {rapport['date']}\n"
                        f"*Score:* {rapport['score']:.4f}\n"
                        f"*Rang anomalie:* {rapport['rang']}\n"
                        f"*Features anomales:*\n{features_str}"
                    )
                }
            }]
        }

        try:
            requests.post(webhook_url, json=message, timeout=5)
            print(f"Alerte envoyee pour {rapport['date']}")
        except Exception as e:
            print(f"Erreur envoi alerte: {e}")
```

### 4.4 Resultats sur 6 Mois

**Statistiques de detection (6 mois) :**
- Jours analyses : 183
- Anomalies detectees : **47 jours**
- Dont vrais positifs (incidents confirmes) : 31 jours (66%)
- Dont faux positifs (alerte injustifiee) : 16 jours (34%)
- **Incidents fraude reels detectes** : 3 (dont 2 non identifies par les regles existantes)
- Miss rate (fraudes non detectees) : 1 incident connu non detecte

**Comparaison avec regles statiques precedentes :**
- Regles statiques : 800 alertes/jour (niveau transaction), 97% faux positifs
- Nouveau systeme : 8 alertes/mois (niveau jour), 34% faux positifs
- Reduction charge equipe fraude : -89%

**Economies estimees :**
- 3 fraudes detectees : montants evites = 247K EUR
- Cout operationnel evite (faux positifs geres) : 180K EUR/an estime

### 4.5 Lecons Apprises

1. **STL residus >> valeurs brutes** : Isolation Forest sur les valeurs brutes
   detectait principalement les weekends et les jours feries (saisonnalite normale),
   pas les vraies anomalies. Les residus STL eliminent la saisonnalite et focalisent
   sur les deviations genuines.

2. **Calibration contamination iterative** : contamination=0.02 (2%) fixe a priori.
   En pratique, affiner selon la capacite de traitement de l'equipe fraude.
   Trop eleve → alerte fatigue. Trop faible → faux sentiment de securite.

3. **Multi-dimensionnel obligatoire** : le volume de transactions seul ne detectait
   qu'1 fraude sur 3. Combiner volume + taux de rejet + transactions hors heures
   + gros montants = signal beaucoup plus discriminant.

4. **Explication essentielle pour adoption** : les analystes fraude refusaient
   d'utiliser la boite noire sans explication. La fonction expliquer_anomalie()
   avec les z-scores par feature a ete le facteur decisif d'adoption.

5. **Lookback 365 jours optimal** : avec 90 jours, les anomalies de l'annee
   precedente biaisant la STL. Au-dela de 18 mois, les anciennes fraudes
   structurelles polluaient le baseline. 365 jours = bon equilibre.

---

## Synthese Comparative des 4 Cas

| Critere | Cas 1 E-commerce | Cas 2 SaaS MRR | Cas 3 Cloud Capacity | Cas 4 Fraude |
|---|---|---|---|---|
| Modele principal | Prophet batch | SARIMA decompose | SARIMA + regresseurs | STL + Isolation Forest |
| Horizon | 12 semaines | 6 mois | 2 semaines | Temps reel J+1 |
| Volume series | 500 SKUs | 4 composantes | 180 services | 9 features |
| MAPE obtenu | 14.2% | 4.2% | 8.3% | N/A (classification) |
| Impact mesure | -23% ruptures | -65% vs budget | 340K EUR economies | 247K EUR fraudes evitees |
| Facteur de succes | Correction ruptures stock | Leading indicators | Seuil sur ci_upper | Residus STL multi-dim |
| Piege evite | Mode additif / multiplicatif | Modeliser agregat | Seuil sur yhat | Isolation Forest brut |
| Re-entrainement | Hebdomadaire | Mensuel | Bimensuel | Quotidien |

### Patterns transversaux appliques dans les 4 cas

1. **Ne jamais modeliser l'agregat directement** : decomposer en composantes
   independantes ameliore systematiquement la precision (Cas 1, 2, 4).

2. **Les regresseurs externes font la difference** : pipeline commercial (Cas 2),
   dates de paiement (Cas 3), promotions (Cas 1). Identifier les leading
   indicators metier est plus impactant que l'optimisation des hyperparametres.

3. **Walk-forward validation obligatoire** : dans les 4 cas, le split classique
   train/test avait sous-estime l'erreur reelle de 30 a 60%.

4. **Production != notebook** : la serialisation, le monitoring et l'alerting
   ont requis autant de travail que la modelisation elle-meme.

5. **Interpretabilite comme facteur d'adoption** : dans les cas 2 et 4,
   l'explication des previsions (contribution des composantes, z-scores) a
   ete decisive pour que les metiers fassent confiance et utilisent le systeme.
