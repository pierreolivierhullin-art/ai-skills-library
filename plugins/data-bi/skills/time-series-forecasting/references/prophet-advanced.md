# Prophet Avance — Tuning, Regresseurs et Production

## Vue d'ensemble

Prophet, developpe par Meta, est un modele additif decomposable concu pour les
series temporelles business. Sa force : gerer facilement les jours feries, les
donnees manquantes et les outliers, avec un tuning intuitif. Ce document couvre
l'architecture interne, le tuning avance et le deploiement en production.

---

## 1. Architecture Interne Prophet

### 1.1 Modele decomposable

Prophet decompose la serie en composantes additives :

y(t) = g(t) + s(t) + h(t) + epsilon(t)

- g(t) : tendance (lineaire ou logistique)
- s(t) : saisonnalite (series de Fourier)
- h(t) : effets des jours feries et evenements speciaux
- epsilon(t) : terme d'erreur (suppose i.i.d. Normal)

### 1.2 Tendance lineaire avec changepoints

Par defaut, Prophet utilise une tendance lineaire par morceaux :

g(t) = (k + a(t)^T * delta) * t + (m + a(t)^T * gamma)

Ou :
- k est le taux de croissance global
- delta est un vecteur de variations du taux aux changepoints
- a(t) vecteur indicateur de quel changepoint est actif

Prophet place automatiquement n_changepoints (defaut 25) dans les 80% premiers
points de la serie d'entrainement.

### 1.3 Tendance logistique (croissance bornee)

Pour les series avec plafond naturel (adoption produit, capacite physique) :

g(t) = L / (1 + exp(-k(t - m)))

L est la capacite maximale (cap). Prophet supporte aussi un plancher (floor).

```python
import pandas as pd
from prophet import Prophet
import matplotlib.pyplot as plt

# Tendance logistique — configuration du cap et floor
def preparer_donnees_logistique(df: pd.DataFrame,
                                 cap_value: float,
                                 floor_value: float = 0.0) -> pd.DataFrame:
    """
    Prophet logistique : requiert colonnes 'cap' et 'floor' dans le DataFrame.
    df doit avoir colonnes 'ds' (datetime) et 'y' (valeur).
    """
    df = df.copy()
    df['cap'] = cap_value
    df['floor'] = floor_value
    return df

# Modele logistique
def modele_logistique(df_train: pd.DataFrame,
                       cap: float,
                       floor: float = 0.0,
                       horizon_jours: int = 90) -> dict:
    df_train = preparer_donnees_logistique(df_train, cap, floor)

    modele = Prophet(
        growth='logistic',
        seasonality_mode='multiplicative',
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False
    )
    modele.fit(df_train)

    futur = modele.make_future_dataframe(periods=horizon_jours)
    futur['cap'] = cap
    futur['floor'] = floor

    forecast = modele.predict(futur)
    return {'modele': modele, 'forecast': forecast}
```

### 1.4 Saisonnalite par series de Fourier

Prophet approche la saisonnalite par une serie de Fourier d'ordre N :

s(t) = sum_{n=1}^{N} [ a_n * cos(2*pi*n*t/P) + b_n * sin(2*pi*n*t/P) ]

- P : periode (365.25 pour annuelle, 7 pour hebdo)
- N : ordre de Fourier (fourier_order) — plus N est grand, plus flexible

### 1.5 Estimation : MAP vs MCMC

- **MAP (Maximum A Posteriori)** : defaut, rapide, pas d'intervalles de confiance bayesiens
- **MCMC** : lent (~10-100x), genere des distributions posterieures completes

```python
# MAP (defaut) — rapide
modele_map = Prophet(uncertainty_samples=1000)

# MCMC — intervalles de confiance bayesiens complets
modele_mcmc = Prophet(
    mcmc_samples=300,          # iterations apres warm-up
    uncertainty_samples=0      # inutile avec MCMC
)
```

---

## 2. Changepoints — Detection et Tuning

### 2.1 Parametres cles

**changepoint_prior_scale** (defaut : 0.05)
- Controle la flexibilite de la tendance
- Trop faible → underfitting (tendance trop rigide)
- Trop fort → overfitting (tendance trop flexible, colle aux donnees)

**n_changepoints** (defaut : 25)
- Nombre de changepoints potentiels
- Augmenter pour series longues avec beaucoup de ruptures

**changepoint_range** (defaut : 0.8)
- Proportion de la serie ou les changepoints sont cherches
- Reduire si les ruptures de tendance recentes sont importantes

```python
def visualiser_changepoints(modele: Prophet,
                             forecast: pd.DataFrame,
                             df_train: pd.DataFrame) -> None:
    """
    Visualise la tendance avec les changepoints detectes et leur intensite.
    """
    fig = modele.plot(forecast, figsize=(14, 6))
    fig.suptitle('Previsions Prophet avec Changepoints', y=1.02)
    plt.tight_layout()

    # Graphique des composantes
    fig2 = modele.plot_components(forecast, figsize=(14, 10))
    plt.tight_layout()

    # Magnitude des changepoints
    changepoints_detectes = modele.changepoints
    deltas = modele.params['delta'].mean(axis=0)

    df_cp = pd.DataFrame({
        'date': changepoints_detectes,
        'delta': deltas,
        'magnitude': abs(deltas)
    }).sort_values('magnitude', ascending=False)

    print("Top 10 changepoints par magnitude:")
    print(df_cp.head(10).to_string(index=False))

    # Graphique magnitude
    plt.figure(figsize=(14, 4))
    plt.bar(changepoints_detectes, deltas,
            color=['red' if d < 0 else 'green' for d in deltas],
            alpha=0.7)
    plt.axhline(y=0, color='black', linestyle='-', linewidth=0.5)
    plt.title('Intensite des Changepoints (rouge = ralentissement, vert = acceleration)')
    plt.xlabel('Date')
    plt.ylabel('Variation du taux de croissance')
    plt.xticks(rotation=45)
    plt.tight_layout()
    plt.show()
```

### 2.2 Changepoints futurs

Prophet peut projeter des changepoints dans le futur via future_changepoints.
Utile pour incorporer des connaissances metier (ex : lancement produit prevu).

```python
def ajouter_changepoints_futurs(modele: Prophet,
                                  dates_rupture: list) -> Prophet:
    """
    Force des changepoints a des dates specifiques connues a l'avance.
    dates_rupture : liste de strings 'YYYY-MM-DD'
    """
    modele_ajuste = Prophet(
        changepoints=dates_rupture,
        n_changepoints=len(dates_rupture),
        changepoint_range=1.0  # autorise changepoints partout
    )
    return modele_ajuste
```

---

## 3. Saisonnalites Personnalisees

### 3.1 Saisonnalite sub-journaliere

```python
def modele_multi_saisonnalite(df_train: pd.DataFrame,
                               horizon: int = 30) -> dict:
    """
    Modele avec saisonnalites multiples : hebdo + mensuelle + annuelle.
    """
    modele = Prophet(
        yearly_seasonality=False,  # on desactive pour ajouter manuellement
        weekly_seasonality=False,
        daily_seasonality=False
    )

    # Saisonnalite annuelle — ordre eleve pour patterns complexes
    modele.add_seasonality(
        name='annuelle',
        period=365.25,
        fourier_order=10,
        prior_scale=10.0  # regularisation
    )

    # Saisonnalite hebdomadaire
    modele.add_seasonality(
        name='hebdomadaire',
        period=7,
        fourier_order=3,
        prior_scale=10.0
    )

    # Saisonnalite mensuelle (ex : effets debut/fin de mois)
    modele.add_seasonality(
        name='mensuelle',
        period=30.44,
        fourier_order=5,
        prior_scale=10.0
    )

    # Saisonnalite trimestrielle (budgets, reporting)
    modele.add_seasonality(
        name='trimestrielle',
        period=91.31,
        fourier_order=3
    )

    modele.fit(df_train)
    futur = modele.make_future_dataframe(periods=horizon)
    forecast = modele.predict(futur)

    return {'modele': modele, 'forecast': forecast}
```

### 3.2 Saisonnalite conditionnelle

Permet d'avoir des patterns saisonniers differents selon une condition (ex :
saisonnalite differente selon les jours promotionnels).

```python
def ajouter_saisonnalite_conditionnelle(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cree des indicateurs booleen pour la saisonnalite conditionnelle.
    Exemple : weekend vs semaine ont des patterns differents.
    """
    df = df.copy()
    df['is_weekend'] = df['ds'].dt.dayofweek.isin([5, 6])
    df['is_weekday'] = ~df['is_weekend']
    return df

def modele_saisonnalite_conditionnelle(df_train: pd.DataFrame,
                                        horizon: int = 30) -> dict:
    df_train = ajouter_saisonnalite_conditionnelle(df_train)

    modele = Prophet(weekly_seasonality=False)
    modele.add_seasonality(
        name='semaine_weekday',
        period=7,
        fourier_order=3,
        condition_name='is_weekday'
    )
    modele.add_seasonality(
        name='semaine_weekend',
        period=7,
        fourier_order=3,
        condition_name='is_weekend'
    )
    modele.fit(df_train)

    futur = modele.make_future_dataframe(periods=horizon)
    futur = ajouter_saisonnalite_conditionnelle(futur)
    forecast = modele.predict(futur)

    return {'modele': modele, 'forecast': forecast}
```

### 3.3 Multiplicative vs Additive seasonality

- **Additive** : amplitude saisonniere constante (defaut)
- **Multiplicative** : amplitude proportionnelle au niveau de la tendance
  Utiliser quand la variance augmente avec le niveau de la serie

```python
# Seasonality mode au niveau global
modele_mult = Prophet(seasonality_mode='multiplicative')

# Ou par saisonnalite individuelle
modele_mixte = Prophet(seasonality_mode='additive')
modele_mixte.add_seasonality(
    name='annuelle',
    period=365.25,
    fourier_order=10,
    mode='multiplicative'  # override le mode global
)
```

---

## 4. Regresseurs Externes

### 4.1 Ajouter des covariables

```python
import numpy as np
from sklearn.preprocessing import StandardScaler

def preparer_regresseurs(df_train: pd.DataFrame,
                          df_futur: pd.DataFrame,
                          colonnes_regresseurs: list,
                          standardiser: bool = True) -> tuple:
    """
    Prepare et standardise les regresseurs pour Prophet.

    IMPORTANT : les valeurs futures des regresseurs doivent etre connues
    au moment de la prevision. Sinon il faut les prevoir separement.

    Args:
        colonnes_regresseurs: liste des colonnes a inclure
        standardiser: recommande True pour la numerique stabilite
    """
    df_train = df_train.copy()
    df_futur = df_futur.copy()

    if standardiser:
        scaler = StandardScaler()
        df_train[colonnes_regresseurs] = scaler.fit_transform(
            df_train[colonnes_regresseurs]
        )
        df_futur[colonnes_regresseurs] = scaler.transform(
            df_futur[colonnes_regresseurs]
        )
        return df_train, df_futur, scaler
    return df_train, df_futur, None


def modele_avec_regresseurs(df_train: pd.DataFrame,
                             df_futur: pd.DataFrame,
                             regresseurs: list,
                             horizon: int = 30) -> dict:
    """
    Prophet avec regresseurs externes : temperature, promotions, etc.
    """
    # Standardisation
    df_train_prep, df_futur_prep, scaler = preparer_regresseurs(
        df_train, df_futur, regresseurs
    )

    modele = Prophet(
        yearly_seasonality=True,
        weekly_seasonality=True,
        daily_seasonality=False,
        seasonality_mode='multiplicative'
    )

    # Ajouter chaque regresseur
    for reg in regresseurs:
        # prior_scale controle l'influence du regresseur
        # standardised=False car on a deja standardise manuellement
        modele.add_regressor(reg, prior_scale=10.0, standardize=False)

    modele.fit(df_train_prep)

    # Futur avec les valeurs connues ou prevues des regresseurs
    futur = modele.make_future_dataframe(periods=horizon)
    # Merger les valeurs des regresseurs pour les dates futures
    futur = futur.merge(
        df_futur_prep[['ds'] + regresseurs],
        on='ds',
        how='left'
    )

    forecast = modele.predict(futur)
    return {
        'modele': modele,
        'forecast': forecast,
        'scaler': scaler,
        'contribution_regresseurs': extraire_contribution_regresseurs(
            modele, forecast, regresseurs
        )
    }

def extraire_contribution_regresseurs(modele: Prophet,
                                       forecast: pd.DataFrame,
                                       regresseurs: list) -> pd.DataFrame:
    """Extrait la contribution de chaque regresseur sur la prevision."""
    contributions = {}
    for reg in regresseurs:
        if reg in forecast.columns:
            contributions[reg] = forecast[reg].mean()

    df_contrib = pd.DataFrame([contributions]).T
    df_contrib.columns = ['contribution_moyenne']
    df_contrib = df_contrib.sort_values('contribution_moyenne', ascending=False)
    print("Contribution moyenne des regresseurs:")
    print(df_contrib)
    return df_contrib
```

### 4.2 Jours feries personnalises

```python
def creer_jours_feries_france() -> pd.DataFrame:
    """Cree un DataFrame des jours feries francais pour Prophet."""
    from pandas.tseries.holiday import AbstractHolidayCalendar
    import warnings

    jours_feries = pd.DataFrame({
        'holiday': [
            'Jour_An', 'Paques_Lundi', 'Fete_Travail', 'Victoire_1945',
            'Ascension', 'Pentecote_Lundi', 'Fete_Nationale', 'Assomption',
            'Toussaint', 'Armistice', 'Noel'
        ],
        'ds': pd.to_datetime([
            '2024-01-01', '2024-04-01', '2024-05-01', '2024-05-08',
            '2024-05-09', '2024-05-20', '2024-07-14', '2024-08-15',
            '2024-11-01', '2024-11-11', '2024-12-25'
        ]),
        'lower_window': [-1] * 11,  # impact commence 1 jour avant
        'upper_window': [1] * 11    # impact dure 1 jour apres
    })
    return jours_feries

def creer_evenements_marketing(df_evenements: pd.DataFrame) -> pd.DataFrame:
    """
    Ajoute des evenements promotionnels (Black Friday, soldes, etc.)
    df_evenements doit avoir : 'nom', 'date_debut', 'date_fin'
    """
    rows = []
    for _, evt in df_evenements.iterrows():
        dates = pd.date_range(evt['date_debut'], evt['date_fin'])
        for date in dates:
            rows.append({
                'holiday': evt['nom'],
                'ds': date,
                'lower_window': 0,
                'upper_window': 0
            })
    return pd.DataFrame(rows)
```

---

## 5. Gestion de l'Incertitude

### 5.1 Sources d'incertitude dans Prophet

Prophet quantifie 3 sources d'incertitude :
1. **Incertitude de la tendance** : futurs changepoints potentiels
2. **Incertitude d'observation** : variance sigma des donnees
3. **Incertitude des parametres** (MCMC uniquement)

### 5.2 Intervalles de prediction

```python
def modele_avec_intervalles(df_train: pd.DataFrame,
                              horizon: int = 90,
                              level: float = 0.95,
                              use_mcmc: bool = False) -> dict:
    """
    Prophet avec intervalles de prediction calibres.

    interval_width : largeur de l'intervalle (0.95 = 95% CI)
    uncertainty_samples : nombre de simulations pour les intervalles (defaut 1000)
    """
    params = {
        'interval_width': level,
        'uncertainty_samples': 1000,
        'yearly_seasonality': True,
        'weekly_seasonality': True
    }

    if use_mcmc:
        params['mcmc_samples'] = 500
        params.pop('uncertainty_samples')

    modele = Prophet(**params)
    modele.fit(df_train)

    futur = modele.make_future_dataframe(periods=horizon)
    forecast = modele.predict(futur)

    # Extraire les bornes
    previsions_horizon = forecast[forecast['ds'] > df_train['ds'].max()][[
        'ds', 'yhat', 'yhat_lower', 'yhat_upper'
    ]]

    print(f"\nPrevisions sur {horizon} jours (IC {level*100:.0f}%):")
    print(previsions_horizon.head(10).to_string(index=False))

    return {
        'modele': modele,
        'forecast': forecast,
        'previsions_horizon': previsions_horizon,
        'niveau_confiance': level
    }
```

---

## 6. Gestion des Outliers et Valeurs Manquantes

### 6.1 Outliers

Prophet est relativement robuste mais les gros outliers biaisent les changepoints.
Strategie : remplacer les outliers par NaN avant l'entrainement.

```python
def traiter_outliers_prophet(df: pd.DataFrame,
                              seuil_iqr: float = 3.0) -> pd.DataFrame:
    """
    Remplace les outliers par NaN. Prophet interpole automatiquement.
    """
    df = df.copy()
    Q1 = df['y'].quantile(0.25)
    Q3 = df['y'].quantile(0.75)
    IQR = Q3 - Q1

    borne_basse = Q1 - seuil_iqr * IQR
    borne_haute = Q3 + seuil_iqr * IQR

    nb_outliers = ((df['y'] < borne_basse) | (df['y'] > borne_haute)).sum()
    print(f"Outliers detectes et remplaces par NaN: {nb_outliers}")

    df.loc[(df['y'] < borne_basse) | (df['y'] > borne_haute), 'y'] = np.nan
    return df
```

### 6.2 Cap et Floor pour tendance logistique

```python
def calibrer_cap(serie: pd.Series, percentile: float = 99.5) -> float:
    """
    Calibre le cap de la tendance logistique.
    Ajoute une marge de 20% au-dessus du percentile observe.
    """
    max_observe = np.percentile(serie.dropna(), percentile)
    cap = max_observe * 1.20
    print(f"Max observe ({percentile}p): {max_observe:.2f}")
    print(f"Cap recommande (+20%): {cap:.2f}")
    return cap
```

---

## 7. Validation Croisee et Tuning Systematique

### 7.1 Cross-validation Prophet native

```python
from prophet.diagnostics import cross_validation, performance_metrics
from prophet.plot import plot_cross_validation_metric

def valider_prophet(modele: Prophet,
                     df_train: pd.DataFrame,
                     initial: str = '365 days',
                     period: str = '30 days',
                     horizon: str = '90 days') -> pd.DataFrame:
    """
    Validation croisee native de Prophet.

    initial : taille minimale du set d'entrainement
    period : pas entre chaque fenetre de validation
    horizon : horizon de prevision a evaluer
    """
    df_cv = cross_validation(
        modele,
        initial=initial,
        period=period,
        horizon=horizon,
        parallel='processes'  # utilise multiprocessing
    )

    df_perf = performance_metrics(df_cv, rolling_window=0.1)

    print("\nPerformances de validation croisee:")
    print(df_perf[['horizon', 'mae', 'mape', 'rmse', 'coverage']].to_string(index=False))

    # Graphique MAPE par horizon
    fig = plot_cross_validation_metric(df_cv, metric='mape')
    plt.title('MAPE par horizon de prevision')
    plt.tight_layout()

    return df_perf
```

### 7.2 Grid Search sur hyperparametres

```python
import itertools
from prophet.diagnostics import cross_validation, performance_metrics

def grid_search_prophet(df_train: pd.DataFrame,
                         param_grid: dict = None,
                         initial: str = '365 days',
                         period: str = '60 days',
                         horizon: str = '90 days') -> pd.DataFrame:
    """
    Grid search sur les hyperparametres Prophet.
    """
    if param_grid is None:
        param_grid = {
            'changepoint_prior_scale': [0.001, 0.01, 0.05, 0.1, 0.5],
            'seasonality_prior_scale': [0.01, 0.1, 1.0, 10.0],
            'seasonality_mode': ['additive', 'multiplicative'],
            'changepoint_range': [0.8, 0.9]
        }

    # Toutes les combinaisons
    all_params = [dict(zip(param_grid.keys(), v))
                  for v in itertools.product(*param_grid.values())]
    print(f"Evaluation de {len(all_params)} combinaisons...")

    resultats = []
    for params in all_params:
        try:
            modele = Prophet(**params)
            modele.fit(df_train)
            df_cv = cross_validation(
                modele,
                initial=initial,
                period=period,
                horizon=horizon,
                parallel='processes',
                disable_tqdm=True
            )
            df_perf = performance_metrics(df_cv, rolling_window=1)
            mape = df_perf['mape'].mean()
            resultats.append({**params, 'mape': mape})
            print(f"  {params} → MAPE: {mape:.4f}")
        except Exception as e:
            print(f"  Erreur pour {params}: {e}")

    df_resultats = pd.DataFrame(resultats).sort_values('mape')
    print("\n=== Meilleurs parametres ===")
    print(df_resultats.head(5).to_string(index=False))
    return df_resultats
```

---

## 8. Prophet en Production

### 8.1 Serialisation et chargement du modele

```python
import json
from prophet.serialize import model_to_json, model_from_json
import pickle
import os

def sauvegarder_modele_prophet(modele: Prophet,
                                 chemin: str,
                                 metadata: dict = None) -> None:
    """
    Serialise le modele Prophet en JSON (format recommande).
    Plus stable que pickle entre versions.
    """
    with open(chemin, 'w') as f:
        json.dump(model_to_json(modele), f)

    if metadata:
        meta_chemin = chemin.replace('.json', '_metadata.json')
        with open(meta_chemin, 'w') as f:
            json.dump({
                'date_entrainement': pd.Timestamp.now().isoformat(),
                'taille_train': metadata.get('n_rows'),
                'derniere_date': str(metadata.get('last_date')),
                'mape_validation': metadata.get('mape'),
                **metadata
            }, f, indent=2)

    print(f"Modele sauvegarde: {chemin}")

def charger_modele_prophet(chemin: str) -> Prophet:
    """Charge un modele Prophet depuis JSON."""
    with open(chemin, 'r') as f:
        modele = model_from_json(json.load(f))
    return modele
```

### 8.2 Pipeline batch scoring en production

```python
from dataclasses import dataclass
from typing import Optional
import logging

logger = logging.getLogger(__name__)

@dataclass
class ProphetPipelineConfig:
    model_path: str
    horizon_days: int = 30
    confidence_level: float = 0.95
    regressors: list = None
    cap: Optional[float] = None
    floor: float = 0.0

class ProphetProductionPipeline:
    """
    Pipeline production pour Prophet : scoring batch reproductible.
    """

    def __init__(self, config: ProphetPipelineConfig):
        self.config = config
        self.modele = None

    def charger(self) -> None:
        self.modele = charger_modele_prophet(self.config.model_path)
        logger.info(f"Modele charge depuis {self.config.model_path}")

    def preparer_futur(self, df_historique: pd.DataFrame,
                        df_regresseurs_futurs: Optional[pd.DataFrame] = None
                       ) -> pd.DataFrame:
        """Prepare le DataFrame futur pour la prevision."""
        futur = self.modele.make_future_dataframe(
            periods=self.config.horizon_days
        )

        if self.config.cap is not None:
            futur['cap'] = self.config.cap
            futur['floor'] = self.config.floor

        if df_regresseurs_futurs is not None and self.config.regressors:
            futur = futur.merge(
                df_regresseurs_futurs[['ds'] + self.config.regressors],
                on='ds', how='left'
            )

        return futur

    def predire(self, df_historique: pd.DataFrame,
                 df_regresseurs_futurs: Optional[pd.DataFrame] = None
                ) -> pd.DataFrame:
        """Execute la prevision et retourne les resultats structures."""
        if self.modele is None:
            self.charger()

        futur = self.preparer_futur(df_historique, df_regresseurs_futurs)
        forecast = self.modele.predict(futur)

        derniere_date_historique = df_historique['ds'].max()
        forecast_horizon = forecast[forecast['ds'] > derniere_date_historique].copy()

        forecast_horizon['date_generation'] = pd.Timestamp.now()
        forecast_horizon['horizon_jours'] = (
            forecast_horizon['ds'] - derniere_date_historique
        ).dt.days

        return forecast_horizon[[
            'ds', 'yhat', 'yhat_lower', 'yhat_upper',
            'horizon_jours', 'date_generation'
        ]]

    def scorer_batch(self, liste_series: list,
                      identifiant_col: str = 'serie_id') -> pd.DataFrame:
        """
        Score un batch de series (multi-series forecasting).
        liste_series : liste de dict avec {'id': str, 'df': pd.DataFrame}
        """
        tous_resultats = []
        for item in liste_series:
            try:
                resultats = self.predire(item['df'])
                resultats[identifiant_col] = item['id']
                tous_resultats.append(resultats)
                logger.info(f"Serie {item['id']} prevue avec succes")
            except Exception as e:
                logger.error(f"Erreur serie {item['id']}: {e}")

        return pd.concat(tous_resultats, ignore_index=True)
```

### 8.3 Monitoring de la derive (drift detection)

```python
def monitorer_derive_prophet(df_reel: pd.DataFrame,
                               df_prevu: pd.DataFrame,
                               seuil_mape: float = 0.10) -> dict:
    """
    Compare les previsions aux valeurs reelles pour detecter la derive.
    A executer a chaque nouveau batch de donnees reelles.

    Args:
        seuil_mape : alerte si MAPE depasse ce seuil (10% par defaut)
    """
    df_merge = df_reel.merge(
        df_prevu[['ds', 'yhat', 'yhat_lower', 'yhat_upper']],
        on='ds',
        how='inner'
    )

    if df_merge.empty:
        return {'statut': 'AUCUNE DONNEE DE COMPARAISON', 'reentainement': False}

    y_true = df_merge['y'].values
    y_pred = df_merge['yhat'].values

    mape = float(np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))))
    mae = float(np.mean(np.abs(y_true - y_pred)))
    coverage = float(np.mean(
        (y_true >= df_merge['yhat_lower']) &
        (y_true <= df_merge['yhat_upper'])
    ))

    alerte = mape > seuil_mape

    rapport = {
        'periode_evaluee': f"{df_merge['ds'].min()} → {df_merge['ds'].max()}",
        'n_observations': len(df_merge),
        'mape': round(mape, 4),
        'mae': round(mae, 4),
        'coverage_ic': round(coverage, 4),
        'seuil_mape': seuil_mape,
        'alerte_derive': alerte,
        'reentainement_recommande': alerte,
        'statut': 'ALERTE: Reentainer le modele' if alerte
                  else 'OK: Performance dans les normes'
    }

    if alerte:
        logger.warning(f"DERIVE DETECTEE: MAPE={mape:.2%} > seuil {seuil_mape:.2%}")
    else:
        logger.info(f"Monitoring OK: MAPE={mape:.2%}")

    return rapport
```

---

## Synthese Operationnelle

### Decision rapide : quand utiliser Prophet

**Utiliser Prophet quand :**
- Series business avec saisonnalite annuelle/hebdomadaire claire
- Jours feries et evenements speciaux importants
- Donnees manquantes frequentes
- Equipe non-experte en ARIMA — Prophet est plus accessible
- Besoin de previsions sur plusieurs series avec la meme structure

**Preferer un autre modele quand :**
- Serie tres courte (< 2 cycles complets) : Holt-Winters plus adapte
- Pas de saisonnalite : ARIMA suffisant et plus rapide
- Dependances entre series multiples : VAR ou modeles ML
- Haute frequence (minutes, secondes) : modeles ML (LightGBM) plus efficaces
- Relations non-lineaires complexes : LightGBM, XGBoost avec features temporelles

### Hyperparametres critiques — Guide de tuning

| Parametre | Defaut | Impact | Diagnostic |
|---|---|---|---|
| changepoint_prior_scale | 0.05 | Flexibilite tendance | Underfitting → augmenter |
| seasonality_prior_scale | 10.0 | Force saisonnalite | Saisonnalite trop marquee → reduire |
| holidays_prior_scale | 10.0 | Force jours feries | Idem seasonality |
| fourier_order | auto | Granularite saisonnalite | Wiggly → reduire |
| n_changepoints | 25 | Nombre ruptures potentielles | Adapter a la longueur |
| changepoint_range | 0.8 | Zone de recherche changepoints | Augmenter si ruptures recentes |
