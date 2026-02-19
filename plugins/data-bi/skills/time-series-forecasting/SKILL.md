---
name: time-series-forecasting
version: 1.0.0
description: >
  Time series forecasting, Prophet, ARIMA SARIMA, seasonal decomposition, trend analysis,
  anomaly detection time series, demand forecasting, revenue forecasting, sales prediction,
  statsmodels, scikit-learn time series, cross-validation temporal, LSTM forecasting,
  business forecasting, capacity planning, inventory optimization
---

# Time Series Forecasting — Predictions Temporelles Business

## Quand Activer ce Skill

Ce skill est pertinent quand :
- Tu dois prevoir les ventes, le CA, le trafic, la demande pour les semaines/mois suivants
- Tu analyses des tendances et la saisonnalite dans tes donnees
- Tu detectes des anomalies dans des series temporelles (monitoring, fraude)
- Tu fais de la planification de capacite (serveurs, stocks, RH)
- Tu compares les performances actuelles avec une baseline prevue

---

## Decomposition des Series Temporelles

### Les 4 Composantes

```python
import pandas as pd
import numpy as np
from statsmodels.tsa.seasonal import STL
import matplotlib.pyplot as plt

def analyser_composantes(df: pd.DataFrame, colonne: str, periode: int = 7) -> None:
    """
    Decompose une serie temporelle en : tendance + saisonnalite + residus.

    Args:
        df: DataFrame avec index DatetimeIndex
        colonne: nom de la colonne a analyser
        periode: periodicite (7 = hebdomadaire, 12 = mensuel, 365 = annuel)
    """
    serie = df[colonne].dropna()

    # STL (Seasonal-Trend decomposition using LOESS) — robuste aux outliers
    stl = STL(serie, period=periode, robust=True)
    result = stl.fit()

    # Visualiser les composantes
    fig, axes = plt.subplots(4, 1, figsize=(12, 10), sharex=True)

    axes[0].plot(serie, label='Donnees brutes')
    axes[0].set_title('Serie originale')

    axes[1].plot(result.trend, color='red', label='Tendance')
    axes[1].set_title('Tendance')

    axes[2].plot(result.seasonal, color='green', label='Saisonnalite')
    axes[2].set_title('Saisonnalite')

    axes[3].plot(result.resid, color='purple', label='Residus')
    axes[3].axhline(0, linestyle='--', color='gray')
    axes[3].set_title('Residus')

    plt.tight_layout()
    plt.savefig('decomposition.png', dpi=150)

    # Mesurer la force de la saisonnalite (0 = aucune, 1 = forte)
    var_resid = result.resid.var()
    var_sais = (result.seasonal + result.resid).var()
    force_saisonnalite = max(0, 1 - var_resid / var_sais)
    print(f"Force de la saisonnalite : {force_saisonnalite:.2f}")
```

---

## Prophet — Forecasting Business

Prophet est developpe par Meta pour les donnees business avec saisonnalites multiples, jours feries et changements de tendance.

```python
from prophet import Prophet
from prophet.plot import plot_plotly, plot_components_plotly
import pandas as pd

def prevoir_avec_prophet(
    df: pd.DataFrame,
    periodes: int = 90,  # Nombre de jours a prevoir
    inclure_jours_feries: bool = True,
) -> tuple[pd.DataFrame, object]:
    """
    Prevision avec Prophet.
    df doit avoir des colonnes 'ds' (date) et 'y' (valeur).
    """
    modele = Prophet(
        # Saisonnalites
        yearly_seasonality=True,     # Saisonnalite annuelle automatique
        weekly_seasonality=True,     # Saisonnalite hebdomadaire
        daily_seasonality=False,     # Activez si donnees horaires

        # Flexibilite de la tendance
        changepoint_prior_scale=0.05,    # Plus petit = tendance plus lisse
        seasonality_prior_scale=10,      # Plus grand = saisonnalite plus flexible

        # Intervalles de confiance
        interval_width=0.95,

        # Gestion des valeurs aberrantes
        mcmc_samples=0,  # MAP estimation (rapide), utiliser >300 pour incertitude complete
    )

    # Ajouter les jours feries francais
    if inclure_jours_feries:
        modele.add_country_holidays(country_name='FR')

    # Ajouter une saisonnalite mensuelle personnalisee
    modele.add_seasonality(
        name='mensuelle',
        period=30.5,
        fourier_order=5,
    )

    modele.fit(df)

    # Generer le DataFrame futur
    futur = modele.make_future_dataframe(periods=periodes, freq='D')
    previsions = modele.predict(futur)

    return previsions, modele

# Exemple d'utilisation
df = pd.read_csv('ventes_quotidiennes.csv', parse_dates=['date'])
df = df.rename(columns={'date': 'ds', 'ventes': 'y'})

previsions, modele = prevoir_avec_prophet(df)

# Previsions pour les 90 prochains jours
df_futur = previsions[previsions['ds'] > df['ds'].max()][
    ['ds', 'yhat', 'yhat_lower', 'yhat_upper']
].copy()

print(df_futur.tail(10).to_string(index=False))
# ds           yhat    yhat_lower  yhat_upper
# 2025-04-01   1234.5  1050.2      1420.8
```

### Validation Croisee Temporelle

```python
from prophet.diagnostics import cross_validation, performance_metrics

def valider_prophet(modele, horizon='30 days', initial='365 days', period='90 days'):
    """
    Validation croisee specifique aux series temporelles.
    NE JAMAIS utiliser sklearn cross_val_score (ignore la temporalite).
    """
    df_cv = cross_validation(
        modele,
        initial=initial,    # Periode d'entrainement initiale
        period=period,       # Frequence de re-entrainement
        horizon=horizon,     # Horizon de prevision a evaluer
        parallel='processes',
    )

    metriques = performance_metrics(df_cv)

    print("\nMetriques de validation croisee :")
    print(f"MAE moyen  : {metriques['mae'].mean():.2f}")
    print(f"MAPE moyen : {metriques['mape'].mean():.1%}")
    print(f"RMSE moyen : {metriques['rmse'].mean():.2f}")

    return df_cv, metriques
```

---

## ARIMA / SARIMA — Approche Statistique

```python
from statsmodels.tsa.statespace.sarimax import SARIMAX
from statsmodels.tsa.stattools import adfuller, acf, pacf
import warnings

def ajuster_sarima(serie: pd.Series, order=(1,1,1), seasonal_order=(1,1,1,12)):
    """
    Ajuste un modele SARIMA.
    order = (p, d, q) : AR, differences, MA
    seasonal_order = (P, D, Q, s) : ordre saisonnier et periode
    """
    warnings.filterwarnings('ignore')

    modele = SARIMAX(
        serie,
        order=order,
        seasonal_order=seasonal_order,
        enforce_stationarity=False,
        enforce_invertibility=False,
    )
    result = modele.fit(disp=False)

    print(f"AIC : {result.aic:.2f}")
    print(f"BIC : {result.bic:.2f}")
    print(result.summary())

    return result

def tester_stationnarite(serie: pd.Series) -> bool:
    """Test de Dickey-Fuller augmente : la serie est-elle stationnaire ?"""
    result = adfuller(serie.dropna(), autolag='AIC')
    p_value = result[1]
    stationnaire = p_value < 0.05
    print(f"ADF p-value : {p_value:.4f} → {'Stationnaire' if stationnaire else 'Non stationnaire (differenciez)'}")
    return stationnaire

def selectionner_ordre_arima(serie: pd.Series, max_p=5, max_q=5) -> dict:
    """Selectionner automatiquement l'ordre ARIMA par AIC."""
    import itertools

    meilleur_aic = float('inf')
    meilleur_ordre = None

    for p, d, q in itertools.product(range(max_p), range(2), range(max_q)):
        try:
            modele = SARIMAX(serie, order=(p, d, q)).fit(disp=False)
            if modele.aic < meilleur_aic:
                meilleur_aic = modele.aic
                meilleur_ordre = (p, d, q)
        except:
            continue

    return {'ordre': meilleur_ordre, 'aic': meilleur_aic}
```

---

## Detection d'Anomalies

### Z-Score et IQR

```python
def detecter_anomalies(serie: pd.Series, methode='iqr', seuil=1.5) -> pd.Series:
    """
    Detecte les valeurs aberrantes dans une serie temporelle.

    Methodes :
    - 'iqr' : interquartile range (robuste aux distributions asymetriques)
    - 'zscore' : score z (pour distributions normales)
    - 'prophet' : intervalles de confiance Prophet
    """
    if methode == 'iqr':
        Q1 = serie.quantile(0.25)
        Q3 = serie.quantile(0.75)
        IQR = Q3 - Q1
        borne_inf = Q1 - seuil * IQR
        borne_sup = Q3 + seuil * IQR
        return (serie < borne_inf) | (serie > borne_sup)

    elif methode == 'zscore':
        z_scores = (serie - serie.mean()) / serie.std()
        return z_scores.abs() > seuil

def detecter_anomalies_prophet(df: pd.DataFrame, incertitude: float = 0.95) -> pd.DataFrame:
    """Deteceter les anomalies via les intervalles de confiance Prophet."""
    modele = Prophet(interval_width=incertitude)
    modele.fit(df)
    previsions = modele.predict(df)

    df_result = df.merge(
        previsions[['ds', 'yhat', 'yhat_lower', 'yhat_upper']],
        on='ds'
    )
    df_result['anomalie'] = (
        (df_result['y'] < df_result['yhat_lower']) |
        (df_result['y'] > df_result['yhat_upper'])
    )

    return df_result[df_result['anomalie']][['ds', 'y', 'yhat', 'yhat_lower', 'yhat_upper']]
```

### Isolation Forest pour les Series

```python
from sklearn.ensemble import IsolationForest

def detecter_anomalies_ml(serie: pd.Series, contamination=0.05) -> pd.Series:
    """
    Isolation Forest : efficace sur les series avec patterns complexes.
    contamination : proportion attendue d'anomalies (5% par defaut).
    """
    # Feature engineering temporel
    features = pd.DataFrame({
        'valeur': serie.values,
        'lag_1': serie.shift(1).values,
        'lag_7': serie.shift(7).values,
        'rolling_mean_7': serie.rolling(7).mean().values,
        'rolling_std_7': serie.rolling(7).std().values,
    }).dropna()

    modele = IsolationForest(contamination=contamination, random_state=42)
    labels = modele.fit_predict(features)  # -1 = anomalie, 1 = normal

    # Aligner avec la serie originale
    scores = pd.Series(labels, index=features.index)
    return serie[scores == -1]
```

---

## Metriques d'Evaluation

```python
import numpy as np

def evaluer_previsions(y_reel: np.ndarray, y_prevu: np.ndarray) -> dict:
    """Calcule les metriques standards de prevision."""
    mae = np.mean(np.abs(y_reel - y_prevu))
    mse = np.mean((y_reel - y_prevu) ** 2)
    rmse = np.sqrt(mse)

    # MAPE : attention si y_reel contient des zeros
    mape = np.mean(np.abs((y_reel - y_prevu) / np.maximum(np.abs(y_reel), 1e-8)))

    # SMAPE : symetrique, moins sensible aux extremes
    smape = np.mean(
        2 * np.abs(y_reel - y_prevu) /
        (np.abs(y_reel) + np.abs(y_prevu) + 1e-8)
    )

    return {
        'MAE': round(mae, 2),
        'RMSE': round(rmse, 2),
        'MAPE': f"{mape:.1%}",
        'SMAPE': f"{smape:.1%}",
    }
```

### Choisir la Bonne Metrique

| Metrique | Usage recommande | Limitation |
|---|---|---|
| **MAPE** | Business (% comprehensible) | Explose si valeurs proches de 0 |
| **MAE** | Outliers dans les donnees | Meme echelle que les donnees |
| **RMSE** | Penaliser les grandes erreurs | Sensible aux outliers |
| **SMAPE** | Valeurs pres de 0 | Peut etre biaise |

---

## Prevision Business — Applications

### Prevision du CA Mensuel

```python
def prevoir_ca_mensuel(historique: pd.DataFrame, mois_a_prevoir: int = 6) -> pd.DataFrame:
    """
    Prevision du CA avec Prophet + decomposition par composante.
    historique: DataFrame avec colonnes 'date' (mensuelle) et 'ca'
    """
    df = historique.rename(columns={'date': 'ds', 'ca': 'y'})
    df['ds'] = pd.to_datetime(df['ds'])

    # Modele avec saisonnalite annuelle renforcee (seulement sur donnees mensuelles)
    modele = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=False,   # Pas pertinent pour mensuel
        changepoint_prior_scale=0.1,
        interval_width=0.90,
    )
    modele.add_country_holidays(country_name='FR')
    modele.fit(df)

    futur = modele.make_future_dataframe(periods=mois_a_prevoir, freq='MS')
    previsions = modele.predict(futur)

    futur_uniquement = previsions[previsions['ds'] > df['ds'].max()][
        ['ds', 'yhat', 'yhat_lower', 'yhat_upper']
    ]
    futur_uniquement.columns = ['mois', 'ca_prevu', 'ca_min_90', 'ca_max_90']

    return futur_uniquement
```

---

## References

- `references/time-series-concepts.md` — Stationnarite, ACF/PACF, tests statistiques, decomposition
- `references/prophet-advanced.md` — Saisonnalites custom, regresseurs, changepoints, tuning
- `references/arima-sarima.md` — Methode Box-Jenkins, selection d'ordre, diagnostic des residus
- `references/case-studies.md` — 4 cas : prevision demande e-commerce, CA SaaS, capacity cloud, fraude
