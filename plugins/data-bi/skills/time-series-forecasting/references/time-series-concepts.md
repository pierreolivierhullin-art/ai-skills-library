# Concepts des Series Temporelles — Theorie et Pratique

## Vue d'ensemble

Une serie temporelle est une suite d'observations indexees dans le temps. La maitrise
des concepts fondamentaux — stationnarite, autocorrelation, decomposition — est un
prerequis absolu avant tout choix de modele. Ce document couvre la theorie et son
application directe en Python.

---

## 1. Stationnarite

### 1.1 Definition formelle

Un processus stochastique Xt est dit strictement stationnaire si sa distribution jointe
est invariante par translation temporelle. En pratique, on utilise la stationnarite
faible (au second ordre) :

- E[Xt] = mu (moyenne constante)
- Var[Xt] = sigma^2 (variance constante)
- Cov[Xt, Xt+k] = gamma(k) depend uniquement du lag k, pas de t

### 1.2 Pourquoi c'est critique

Les modeles ARIMA et la plupart des methodes classiques supposent la stationnarite.
Une serie non-stationnaire genere des regressions fallacieuses et des previsions
divergentes. Identifier et corriger la non-stationnarite est la premiere etape
obligatoire.

### 1.3 Test ADF (Augmented Dickey-Fuller)

H0 : la serie contient une racine unitaire (non-stationnaire)
H1 : la serie est stationnaire

```python
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller, kpss

def test_stationnarite(serie: pd.Series, nom: str = "serie") -> dict:
    """
    Applique ADF et KPSS pour evaluer la stationnarite.
    Retourne un dict avec les resultats et la conclusion.
    """
    # Test ADF
    adf_result = adfuller(serie.dropna(), autolag='AIC')
    adf_stat, adf_pvalue, adf_lags, adf_nobs, adf_critvals, _ = adf_result

    # Test KPSS
    kpss_result = kpss(serie.dropna(), regression='c', nlags='auto')
    kpss_stat, kpss_pvalue, kpss_lags, kpss_critvals = kpss_result

    # Interpretation combinee
    adf_stationnaire = adf_pvalue < 0.05   # rejette H0 racine unitaire
    kpss_stationnaire = kpss_pvalue > 0.05  # ne rejette pas H0 stationnarite

    if adf_stationnaire and kpss_stationnaire:
        conclusion = "STATIONNAIRE (ADF + KPSS concordants)"
    elif not adf_stationnaire and not kpss_stationnaire:
        conclusion = "NON-STATIONNAIRE (ADF + KPSS concordants)"
    elif adf_stationnaire and not kpss_stationnaire:
        conclusion = "STATIONNARITE DES TENDANCES (trend-stationary)"
    else:
        conclusion = "STATIONNARITE DIFFERENTIELLE (diff-stationary)"

    return {
        "nom": nom,
        "adf_statistic": round(adf_stat, 4),
        "adf_pvalue": round(adf_pvalue, 4),
        "adf_critval_5pct": round(adf_critvals['5%'], 4),
        "kpss_statistic": round(kpss_stat, 4),
        "kpss_pvalue": round(kpss_pvalue, 4),
        "kpss_critval_5pct": round(kpss_critvals['5%'], 4),
        "conclusion": conclusion,
        "differentiation_recommandee": not (adf_stationnaire and kpss_stationnaire)
    }

# Usage
# resultats = test_stationnarite(df['ventes'], "Ventes quotidiennes")
# print(resultats)
```

### 1.4 Test KPSS (Kwiatkowski-Phillips-Schmidt-Shin)

H0 : la serie est stationnaire (autour d'une constante ou tendance)
H1 : la serie contient une racine unitaire

L'usage combine ADF + KPSS permet de distinguer 4 scenarios :
| ADF rejette H0 | KPSS rejette H0 | Conclusion |
|---|---|---|
| Oui | Non | Stationnaire |
| Non | Oui | Non-stationnaire |
| Oui | Oui | Trend-stationary |
| Non | Non | Diff-stationary |

### 1.5 Differentiation d'ordre d

La differentiation d'ordre 1 : delta_Xt = Xt - Xt-1
La differentiation d'ordre 2 : delta^2_Xt = delta_Xt - delta_Xt-1

```python
def differentier(serie: pd.Series, ordre: int = 1) -> pd.Series:
    """Differentie la serie d fois et reteste la stationnarite."""
    serie_diff = serie.copy()
    for i in range(ordre):
        serie_diff = serie_diff.diff()
    return serie_diff.dropna()

# Workflow automatique : differentier jusqu'a stationnarite
def ordre_differentiation(serie: pd.Series, max_d: int = 3) -> int:
    from statsmodels.tsa.stattools import adfuller
    for d in range(max_d + 1):
        s = serie.diff(d) if d > 0 else serie
        s = s.dropna()
        pvalue = adfuller(s, autolag='AIC')[1]
        if pvalue < 0.05:
            return d
    return max_d
```

---

## 2. Fonctions d'Autocorrelation (ACF et PACF)

### 2.1 ACF — Autocorrelation Function

L'ACF au lag k mesure la correlation entre Xt et Xt-k, incluant les effets
intermediaires. La formule :

rho(k) = Cov[Xt, Xt-k] / Var[Xt]

### 2.2 PACF — Partial Autocorrelation Function

La PACF au lag k mesure la correlation entre Xt et Xt-k apres avoir retire
l'influence des lags intermediaires 1 a k-1. Essentielle pour identifier p dans ARIMA.

### 2.3 Visualisation et interpretation

```python
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

def analyser_autocorrelations(serie: pd.Series, lags: int = 40,
                               titre: str = "Analyse ACF/PACF"):
    """
    Trace ACF et PACF avec annotations pour identification ARIMA.
    """
    fig, axes = plt.subplots(2, 1, figsize=(12, 8))

    # ACF
    plot_acf(serie.dropna(), lags=lags, ax=axes[0],
             alpha=0.05, zero=False)
    axes[0].set_title(f'{titre} — ACF\n'
                      f'Coupure abrupte a lag q → MA(q) | Declin geometrique → AR')
    axes[0].axhline(y=0, linestyle='--', color='black', alpha=0.3)

    # PACF
    plot_pacf(serie.dropna(), lags=lags, ax=axes[1],
              alpha=0.05, zero=False, method='ywm')
    axes[1].set_title(f'{titre} — PACF\n'
                      f'Coupure abrupte a lag p → AR(p) | Declin geometrique → MA')
    axes[1].axhline(y=0, linestyle='--', color='black', alpha=0.3)

    plt.tight_layout()
    plt.savefig(f'acf_pacf_{titre.lower().replace(" ", "_")}.png',
                dpi=150, bbox_inches='tight')
    plt.show()
    return fig
```

### 2.4 Regles de decision pour ARIMA

| Pattern ACF | Pattern PACF | Modele suggere |
|---|---|---|
| Declin exponentiel | Coupure a lag p | AR(p) |
| Coupure a lag q | Declin exponentiel | MA(q) |
| Declin exponentiel | Declin exponentiel | ARMA(p,q) |
| Tous non-significatifs | Tous non-significatifs | White noise |
| Persistence lente | — | Non-stationnaire, differencier |

---

## 3. White Noise et Bruit Structure

### 3.1 White noise pur

Un processus {et} est white noise si :
- E[et] = 0
- Var[et] = sigma^2 < inf
- Cov[et, es] = 0 pour t != s

Test de Ljung-Box pour verifier si les residus sont white noise :

```python
from statsmodels.stats.diagnostic import acorr_ljungbox

def tester_white_noise(residus: pd.Series, lags: list = None) -> pd.DataFrame:
    """
    Test de Ljung-Box sur les residus.
    H0 : les residus sont white noise (pas d'autocorrelation)
    p > 0.05 → on ne rejette pas H0 → residus adequats
    """
    if lags is None:
        lags = [5, 10, 15, 20]

    resultats = acorr_ljungbox(residus.dropna(), lags=lags, return_df=True)
    resultats['adequat'] = resultats['lb_pvalue'] > 0.05

    print("Test de Ljung-Box sur les residus:")
    print(resultats[['lb_stat', 'lb_pvalue', 'adequat']].to_string())
    print(f"\nConclusion: residus {'adequats' if resultats['adequat'].all() else 'NON adequats'}")
    return resultats
```

### 3.2 Bruit colore et structure residuelle

Si les residus montrent de l'autocorrelation, le modele n'a pas capture toute
l'information. Actions correctives :
- Augmenter l'ordre p ou q
- Ajouter une composante saisonniere
- Verifier les outliers qui biaisant les estimations

---

## 4. Decomposition des Series Temporelles

### 4.1 Modele additif vs multiplicatif

**Additif** : Xt = Tt + St + Rt
- Amplitude saisonniere constante independamment du niveau
- Adapte aux series avec croissance lente ou lineaire

**Multiplicatif** : Xt = Tt * St * Rt
- Amplitude saisonniere proportionnelle au niveau
- Adapte aux series avec croissance exponentielle
- Equivalence : log(Xt) transforme le multiplicatif en additif

```python
from statsmodels.tsa.seasonal import seasonal_decompose, STL
import matplotlib.pyplot as plt

def decomposer_serie(serie: pd.Series, periode: int,
                     modele: str = 'additive') -> dict:
    """
    Decompose la serie en tendance + saisonnalite + residus.

    Args:
        periode: 7 (hebdo), 12 (mensuel), 52 (annuel hebdo), 365 (annuel journalier)
        modele: 'additive' ou 'multiplicative'
    """
    decomp = seasonal_decompose(serie.dropna(), model=modele,
                                period=periode, extrapolate_trend='freq')

    fig, axes = plt.subplots(4, 1, figsize=(14, 10))
    decomp.observed.plot(ax=axes[0], title='Observee')
    decomp.trend.plot(ax=axes[1], title='Tendance')
    decomp.seasonal.plot(ax=axes[2], title=f'Saisonnalite ({modele})')
    decomp.resid.plot(ax=axes[3], title='Residus')
    plt.tight_layout()

    return {
        'tendance': decomp.trend,
        'saisonnalite': decomp.seasonal,
        'residus': decomp.resid,
        'force_saisonnalite': 1 - decomp.resid.var() /
                              (decomp.seasonal + decomp.resid).var()
    }
```

### 4.2 STL (Seasonal and Trend decomposition using Loess)

STL est superieur a seasonal_decompose car :
- Robuste aux outliers
- Permet une saisonnalite variable dans le temps
- Gere les valeurs manquantes
- Parametres ajustables (seasonal_smoother)

```python
def decomposer_stl(serie: pd.Series, periode: int,
                   seasonal: int = 7, robust: bool = True) -> dict:
    """
    Decomposition STL robuste.

    Args:
        seasonal: doit etre impair >= 7, controle le lissage de la saisonnalite
        robust: True pour utiliser des poids robustes (protege contre outliers)
    """
    stl = STL(serie.dropna(), period=periode,
              seasonal=seasonal, robust=robust)
    result = stl.fit()

    # Force de la tendance et de la saisonnalite (Wang et al. 2006)
    Ft = max(0, 1 - result.resid.var() /
             (result.trend + result.resid).var())
    Fs = max(0, 1 - result.resid.var() /
             (result.seasonal + result.resid).var())

    result.plot()
    plt.suptitle(f'STL — Force tendance: {Ft:.2f} | Force saisonnalite: {Fs:.2f}')
    plt.tight_layout()

    return {
        'tendance': result.trend,
        'saisonnalite': result.seasonal,
        'residus': result.resid,
        'force_tendance': round(Ft, 3),
        'force_saisonnalite': round(Fs, 3)
    }
```

---

## 5. Tests de Saisonnalite

### 5.1 Test de Kruskal-Wallis

Test non-parametrique pour detecter des differences entre periodes saisonnieres.
H0 : pas de differences entre les mois/jours/trimestres.

```python
from scipy.stats import kruskal, friedmanchisquare

def tester_saisonnalite_kruskal(serie: pd.Series, frequence: str = 'M') -> dict:
    """
    Test Kruskal-Wallis pour detecter la saisonnalite.
    frequence: 'M' (mensuel), 'W' (hebdo), 'Q' (trimestriel)
    """
    df = pd.DataFrame({'valeur': serie, 'periode': serie.index})

    if frequence == 'M':
        df['groupe'] = serie.index.month
    elif frequence == 'W':
        df['groupe'] = serie.index.dayofweek
    elif frequence == 'Q':
        df['groupe'] = serie.index.quarter

    groupes = [grp['valeur'].values for _, grp in df.groupby('groupe')]
    stat, pvalue = kruskal(*groupes)

    return {
        'statistique': round(stat, 4),
        'pvalue': round(pvalue, 4),
        'saisonnalite_detectee': pvalue < 0.05,
        'frequence': frequence
    }
```

### 5.2 Statistique de Ljung-Box pour saisonnalite

```python
def tester_saisonnalite_ljungbox(serie: pd.Series,
                                  periode: int = 12) -> dict:
    """
    Teste la saisonnalite via Ljung-Box aux lags saisonniers.
    """
    lags_saisonniers = [periode, 2*periode, 3*periode]
    lags_saisonniers = [l for l in lags_saisonniers if l < len(serie)]

    resultats = acorr_ljungbox(serie.dropna(),
                                lags=lags_saisonniers, return_df=True)
    return resultats
```

---

## 6. Heteroscedasticite et Effets ARCH

### 6.1 Detection des effets ARCH

L'heteroscedasticite conditionnelle (variance non constante) invalide les intervalles
de confiance des modeles lineaires.

```python
from statsmodels.stats.diagnostic import het_arch

def tester_arch(residus: pd.Series, lags: int = 12) -> dict:
    """
    Test ARCH de Engle sur les residus.
    H0 : pas d'effets ARCH (homoscedasticite)
    """
    lm_stat, lm_pvalue, f_stat, f_pvalue = het_arch(residus.dropna(), nlags=lags)
    return {
        'lm_statistic': round(lm_stat, 4),
        'lm_pvalue': round(lm_pvalue, 4),
        'arch_detecte': lm_pvalue < 0.05,
        'action': 'Utiliser GARCH ou transformer la serie' if lm_pvalue < 0.05
                  else 'Homoscedasticite satisfaisante'
    }
```

### 6.2 Introduction GARCH

Pour les series financieres avec clusters de volatilite, GARCH(p,q) modele
la variance conditionnelle :

sigma_t^2 = omega + sum_i(alpha_i * e_{t-i}^2) + sum_j(beta_j * sigma_{t-j}^2)

---

## 7. Detection et Traitement des Anomalies

### 7.1 Types d'outliers en series temporelles

**AO (Additive Outlier)** : choc ponctuel sur une seule observation
- Exemple : panne de systeme un jour, jeu de donnees manquant

**IO (Innovative Outlier)** : choc qui se propage via la dynamique AR
- Impact decroissant sur les observations suivantes
- Plus difficile a detecter et traiter

**LS (Level Shift)** : changement permanent du niveau
- Exemple : lancement d'un nouveau produit, changement de strategie
- Necessite une variable dummy permanente

**TC (Temporary Change)** : choc transitoire avec retour progressif au niveau

```python
def detecter_outliers_iqr(serie: pd.Series,
                           fenetre: int = 30,
                           seuil: float = 3.0) -> pd.DataFrame:
    """
    Detection d'outliers par IQR glissant (methode robuste).
    """
    rolling_median = serie.rolling(window=fenetre, center=True).median()
    rolling_iqr = (serie.rolling(window=fenetre, center=True).quantile(0.75) -
                   serie.rolling(window=fenetre, center=True).quantile(0.25))

    score = np.abs(serie - rolling_median) / (rolling_iqr + 1e-8)
    outliers = score > seuil

    return pd.DataFrame({
        'valeur': serie,
        'score_outlier': score,
        'est_outlier': outliers,
        'mediane_locale': rolling_median
    })

def traiter_outliers(serie: pd.Series,
                     outliers_mask: pd.Series,
                     methode: str = 'interpolation') -> pd.Series:
    """
    Methodes : 'interpolation', 'median', 'winsorize'
    """
    serie_corrigee = serie.copy()
    if methode == 'interpolation':
        serie_corrigee[outliers_mask] = np.nan
        serie_corrigee = serie_corrigee.interpolate(method='time')
    elif methode == 'median':
        fenetre_mediane = serie.rolling(window=7, center=True).median()
        serie_corrigee[outliers_mask] = fenetre_mediane[outliers_mask]
    return serie_corrigee
```

---

## 8. Transformations

### 8.1 Transformation Box-Cox

Stabilise la variance et peut rendre une serie multiplicative additive.
Lambda optimal par maximum de vraisemblance.

```python
from scipy.stats import boxcox
from scipy.special import inv_boxcox

def transformer_boxcox(serie: pd.Series) -> tuple:
    """
    Applique Box-Cox et retourne la serie transformee + lambda.
    Attention : necessite des valeurs strictement positives.
    """
    valeurs = serie.dropna().values
    if (valeurs <= 0).any():
        # Decaler pour valeurs positives
        shift = abs(valeurs.min()) + 1
        valeurs_positives = valeurs + shift
    else:
        shift = 0
        valeurs_positives = valeurs

    transformee, lambda_opt = boxcox(valeurs_positives)

    print(f"Lambda Box-Cox optimal : {lambda_opt:.4f}")
    print(f"  lambda ~ 0  → transformation log")
    print(f"  lambda ~ 0.5 → racine carree")
    print(f"  lambda ~ 1  → pas de transformation")

    return pd.Series(transformee, index=serie.dropna().index), lambda_opt, shift

def inverser_boxcox(serie_transformee: pd.Series,
                    lambda_opt: float, shift: float = 0) -> pd.Series:
    """Inverse la transformation Box-Cox."""
    valeurs_originales = inv_boxcox(serie_transformee.values, lambda_opt)
    return pd.Series(valeurs_originales - shift, index=serie_transformee.index)
```

### 8.2 Differentiation saisonniere

Pour eliminer la saisonnalite d'ordre s :
delta_s(Xt) = Xt - Xt-s

```python
def differencier_saisonnierment(serie: pd.Series, s: int) -> pd.Series:
    """
    Differentiation saisonniere d'ordre s.
    s=12 pour mensuelles, s=7 pour journalieres hebdomadaires.
    """
    return (serie - serie.shift(s)).dropna()
```

---

## 9. Methodes de Lissage Exponentiel (Holt-Winters)

### 9.1 Simple exponential smoothing (SES)

Adapte quand il n'y a pas de tendance ni saisonnalite.
St = alpha * Xt + (1 - alpha) * St-1

```python
from statsmodels.tsa.holtwinters import (
    SimpleExpSmoothing, Holt, ExponentialSmoothing
)

def lissage_simple(serie: pd.Series,
                   horizon: int = 12) -> pd.DataFrame:
    """Lissage exponentiel simple — optimise alpha automatiquement."""
    modele = SimpleExpSmoothing(serie, initialization_method='estimated')
    resultat = modele.fit(optimized=True)
    previsions = resultat.forecast(horizon)
    return pd.DataFrame({
        'ajuste': resultat.fittedvalues,
        'prevision': previsions
    })
```

### 9.2 Holt — Double exponential smoothing

Capture tendance lineaire en plus du niveau.

```python
def lissage_holt(serie: pd.Series, horizon: int = 12,
                 exponential: bool = False) -> pd.DataFrame:
    """
    Holt double smoothing.
    exponential=True : tendance multiplicative (croissance exponentielle)
    """
    modele = Holt(serie, exponential=exponential,
                  initialization_method='estimated')
    resultat = modele.fit(optimized=True, damped_trend=True)
    previsions = resultat.forecast(horizon)
    return pd.DataFrame({
        'ajuste': resultat.fittedvalues,
        'prevision': previsions,
        'alpha': resultat.params['smoothing_level'],
        'beta': resultat.params['smoothing_trend'],
        'phi': resultat.params.get('damping_trend', 1.0)
    })
```

### 9.3 Holt-Winters — Triple exponential smoothing

Capture niveau + tendance + saisonnalite.

```python
def holt_winters_complet(serie: pd.Series, periode: int,
                          horizon: int = 12,
                          modele_type: str = 'additive') -> dict:
    """
    Holt-Winters triple.
    modele_type : 'additive' ou 'multiplicative'
    """
    hw = ExponentialSmoothing(
        serie,
        trend='add',
        seasonal=modele_type,
        seasonal_periods=periode,
        initialization_method='estimated',
        damped_trend=True
    )
    resultat = hw.fit(optimized=True)
    previsions = resultat.forecast(horizon)

    aic = resultat.aic
    bic = resultat.bic

    return {
        'modele': resultat,
        'previsions': previsions,
        'ajuste': resultat.fittedvalues,
        'aic': round(aic, 2),
        'bic': round(bic, 2),
        'alpha': round(resultat.params['smoothing_level'], 4),
        'beta': round(resultat.params['smoothing_trend'], 4),
        'gamma': round(resultat.params['smoothing_seasonal'], 4),
        'phi': round(resultat.params.get('damping_trend', 1.0), 4)
    }
```

---

## 10. Metriques d'Evaluation Correctes pour Series Temporelles

### 10.1 Pourquoi le train/test split classique est insuffisant

Un split aleatoire viole l'ordre temporel et introduit du data leakage. Les series
temporelles exigent une validation qui respecte la causalite.

### 10.2 Walk-Forward Validation

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error
import numpy as np

def walk_forward_validation(serie: pd.Series,
                             modele_fn,
                             horizon: int = 12,
                             n_splits: int = 5) -> dict:
    """
    Walk-forward validation (expanding window).

    Args:
        modele_fn: fonction(train_serie, horizon) -> pd.Series de previsions
        horizon: nombre de pas a prevoir a chaque split
        n_splits: nombre de fenetres de validation
    """
    n = len(serie)
    taille_min_train = n - n_splits * horizon

    if taille_min_train < horizon * 2:
        raise ValueError("Serie trop courte pour le nombre de splits demande")

    resultats = []
    for i in range(n_splits):
        fin_train = taille_min_train + i * horizon
        train = serie.iloc[:fin_train]
        test = serie.iloc[fin_train:fin_train + horizon]

        if len(test) == 0:
            break

        previsions = modele_fn(train, horizon=len(test))

        # Alignement
        y_true = test.values
        y_pred = previsions.values[:len(y_true)]

        mae = mean_absolute_error(y_true, y_pred)
        rmse = np.sqrt(mean_squared_error(y_true, y_pred))
        mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100
        smape = np.mean(2 * np.abs(y_true - y_pred) /
                        (np.abs(y_true) + np.abs(y_pred) + 1e-8)) * 100

        resultats.append({
            'split': i + 1,
            'fin_train': train.index[-1],
            'debut_test': test.index[0],
            'mae': round(mae, 4),
            'rmse': round(rmse, 4),
            'mape': round(mape, 2),
            'smape': round(smape, 2)
        })

    df_resultats = pd.DataFrame(resultats)
    print("\n=== Walk-Forward Validation ===")
    print(df_resultats.to_string(index=False))
    print(f"\nMoyennes:")
    print(f"  MAE  : {df_resultats['mae'].mean():.4f} ± {df_resultats['mae'].std():.4f}")
    print(f"  RMSE : {df_resultats['rmse'].mean():.4f} ± {df_resultats['rmse'].std():.4f}")
    print(f"  MAPE : {df_resultats['mape'].mean():.2f}% ± {df_resultats['mape'].std():.2f}%")
    print(f"  sMAPE: {df_resultats['smape'].mean():.2f}% ± {df_resultats['smape'].std():.2f}%")

    return {
        'detail': df_resultats,
        'mae_moyen': df_resultats['mae'].mean(),
        'rmse_moyen': df_resultats['rmse'].mean(),
        'mape_moyen': df_resultats['mape'].mean(),
        'smape_moyen': df_resultats['smape'].mean()
    }
```

### 10.3 Choix de la metrique selon le contexte

| Metrique | Formule | Quand l'utiliser | Limite |
|---|---|---|---|
| MAE | mean(|y - yhat|) | Erreurs interpretables, robuste | Pas relatif |
| RMSE | sqrt(mean((y-yhat)^2)) | Penalise grosses erreurs | Sensible outliers |
| MAPE | mean(|y-yhat|/y)*100 | Comparaisons cross-series | Explose si y proche de 0 |
| sMAPE | mean(2*|y-yhat|/(|y|+|yhat|))*100 | MAPE symetrique | Biaise encore |
| MASE | MAE / MAE_naive | Reference vs naive, robuste | Moins intuitif |

### 10.4 Baseline Naive indispensable

Toujours comparer au modele naive :
- Naive simple : yhat_{t+1} = yt
- Naive saisonniere : yhat_{t+1} = y_{t-s}
- Drift : yhat_{t+h} = yt + h * (yt - y1) / (t - 1)

Un modele sophistique qui ne bat pas le naive saisonnier est inutile.

```python
def baseline_naive_saisonnier(train: pd.Series,
                               horizon: int,
                               periode: int = 12) -> pd.Series:
    """Prevision naive saisonniere : repete le dernier cycle."""
    n = len(train)
    previsions = []
    for h in range(1, horizon + 1):
        idx = n - periode + ((h - 1) % periode)
        if idx >= 0:
            previsions.append(train.iloc[idx])
        else:
            previsions.append(train.iloc[-1])

    last_date = train.index[-1]
    dates_prevision = pd.date_range(
        start=last_date + pd.tseries.frequencies.to_offset(train.index.freq or 'D'),
        periods=horizon,
        freq=train.index.freq or 'D'
    )
    return pd.Series(previsions, index=dates_prevision)
```

---

## Synthese Operationnelle

### Checklist d'analyse d'une nouvelle serie temporelle

1. **Visualisation initiale** : tracer la serie, identifier visuellement tendance/saisonnalite
2. **Tests de stationnarite** : ADF + KPSS, noter le resultat combine
3. **Decomposition** : STL avec periode appropriee, mesurer les forces
4. **Analyse ACF/PACF** : identifier structure AR/MA potentielle
5. **Detection outliers** : IQR glissant, documenter et traiter
6. **Test de saisonnalite** : Kruskal-Wallis ou Ljung-Box aux lags saisonniers
7. **Test ARCH** : si serie financiere ou variance potentiellement heteroscedastique
8. **Choix de transformation** : Box-Cox si variance non constante
9. **Definition baseline** : naive saisonnier comme reference minimale
10. **Setup walk-forward validation** : definir splits avant tout modelisation

### Selection du modele selon les caracteristiques

| Serie | Recommandation |
|---|---|
| Tendance + pas de saisonnalite | Holt double ou ARIMA(p,1,q) |
| Tendance + saisonnalite stable | Holt-Winters ou SARIMA |
| Saisonnalite variable dans le temps | STL + modele sur composantes |
| Multiples saisonnalites | Prophet ou TBATS |
| Regresseurs externes importants | SARIMAX ou Prophet avec regresseurs |
| Tres longue serie + non-linearite | ML : LightGBM, XGBoost |
| Multiples series correlees | VAR ou ML multi-output |
