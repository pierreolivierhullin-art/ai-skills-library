# ARIMA et SARIMA — Methode Box-Jenkins

## Vue d'ensemble

La methode Box-Jenkins est le cadre canonique pour modeliser les series temporelles
univariees stationnaires. ARIMA (Autoregressive Integrated Moving Average) et son
extension saisonniere SARIMA restent les references incontournables pour comprendre
la structure des series et produire des previsions interpretables.

---

## 1. La Methode Box-Jenkins — 4 Etapes

### 1.1 Vue d'ensemble du processus iteratif

```
[1] IDENTIFICATION  →  [2] ESTIMATION  →  [3] DIAGNOSTIC  →  [4] PREVISION
     ACF / PACF            MLE / OLS          Residus              Intervalles
     Tests ADF/KPSS        AIC / BIC          Ljung-Box            de confiance
     Ordre (p,d,q)         Convergence        Normalite            Walk-forward
         ↑___________________________|
              (boucle jusqu'a residus adequats)
```

### 1.2 Notation ARIMA(p,d,q)

- **p** : ordre autoregressif — nombre de lags de la serie en entree
- **d** : ordre de differentiation pour atteindre la stationnarite
- **q** : ordre de moyenne mobile — nombre de lags des erreurs passes

Le modele ARIMA(p,d,q) :
phi(B)(1-B)^d * Xt = theta(B) * et

Ou B est l'operateur retard (BXt = Xt-1), phi et theta sont les polynomes AR et MA.

---

## 2. Etape 1 — Identification de l'ordre

### 2.1 Tests de stationnarite et determination de d

```python
import pandas as pd
import numpy as np
from statsmodels.tsa.stattools import adfuller, kpss
import matplotlib.pyplot as plt
from statsmodels.graphics.tsaplots import plot_acf, plot_pacf

def identifier_ordre_d(serie: pd.Series, max_d: int = 3,
                        alpha: float = 0.05) -> dict:
    """
    Determine l'ordre de differentiation d par tests iteratifs ADF + KPSS.
    """
    resultats = []

    for d in range(max_d + 1):
        if d == 0:
            s = serie.dropna()
        else:
            s = serie.diff(d).dropna()

        # Test ADF
        adf_stat, adf_pvalue = adfuller(s, autolag='AIC')[:2]
        # Test KPSS
        kpss_stat, kpss_pvalue = kpss(s, regression='c', nlags='auto')[:2]

        stationnaire = (adf_pvalue < alpha) and (kpss_pvalue > alpha)

        resultats.append({
            'd': d,
            'adf_pvalue': round(adf_pvalue, 4),
            'kpss_pvalue': round(kpss_pvalue, 4),
            'stationnaire': stationnaire
        })

        if stationnaire:
            d_optimal = d
            break
    else:
        d_optimal = max_d

    df_res = pd.DataFrame(resultats)
    print("Tests de stationnarite par ordre de differentiation:")
    print(df_res.to_string(index=False))
    print(f"\n→ Ordre d recommande : d = {d_optimal}")

    return {'d_optimal': d_optimal, 'detail': df_res}


def panel_diagnostic_stationnarite(serie: pd.Series, d: int,
                                    titre: str = "Serie") -> None:
    """
    Affiche la serie originale + serie differenciee avec ACF/PACF.
    """
    serie_diff = serie.diff(d).dropna() if d > 0 else serie.dropna()

    fig, axes = plt.subplots(2, 3, figsize=(16, 10))

    # Serie originale
    axes[0, 0].plot(serie)
    axes[0, 0].set_title(f'{titre} — Originale')
    plot_acf(serie.dropna(), lags=40, ax=axes[0, 1], zero=False)
    axes[0, 1].set_title('ACF Originale')
    plot_pacf(serie.dropna(), lags=40, ax=axes[0, 2],
              zero=False, method='ywm')
    axes[0, 2].set_title('PACF Originale')

    # Serie differenciee
    axes[1, 0].plot(serie_diff)
    axes[1, 0].set_title(f'{titre} — Differenciee (d={d})')
    plot_acf(serie_diff, lags=40, ax=axes[1, 1], zero=False)
    axes[1, 1].set_title(f'ACF (d={d})')
    plot_pacf(serie_diff, lags=40, ax=axes[1, 2],
              zero=False, method='ywm')
    axes[1, 2].set_title(f'PACF (d={d})')

    plt.tight_layout()
    plt.show()
```

### 2.2 Identification de p et q par ACF/PACF

```python
def regles_identification_arima(acf_vals: np.ndarray,
                                 pacf_vals: np.ndarray,
                                 intervalle_conf: float = 0.05) -> dict:
    """
    Applique les regles de decision Box-Jenkins pour suggerer p et q.

    Regles :
    - ACF coupe a q, PACF decline → MA(q)
    - PACF coupe a p, ACF decline → AR(p)
    - Deux declinent geometriquement → ARMA(p,q)
    """
    n = len(acf_vals)
    seuil = 1.96 / np.sqrt(n)  # intervalle de confiance 95%

    # Dernier lag significatif dans ACF et PACF
    acf_sig = [i for i, v in enumerate(acf_vals[1:], 1) if abs(v) > seuil]
    pacf_sig = [i for i, v in enumerate(pacf_vals[1:], 1) if abs(v) > seuil]

    q_suggestions = max(acf_sig) if acf_sig else 0
    p_suggestions = max(pacf_sig) if pacf_sig else 0

    print(f"Seuil de significativite : {seuil:.4f}")
    print(f"Lags ACF significatifs  : {acf_sig[:10]}")
    print(f"Lags PACF significatifs : {pacf_sig[:10]}")
    print(f"\nSuggestion initiale :")
    print(f"  p (AR) ≤ {p_suggestions} (dernier lag PACF significatif)")
    print(f"  q (MA) ≤ {q_suggestions} (dernier lag ACF significatif)")
    print(f"\nRecommandation : tester ARIMA({p_suggestions},d,{q_suggestions})")
    print(f"et valider par AIC/BIC avec auto_arima")

    return {
        'p_max': p_suggestions,
        'q_max': q_suggestions,
        'acf_lags_sig': acf_sig,
        'pacf_lags_sig': pacf_sig
    }
```

---

## 3. Etape 2 — Selection automatique et Estimation

### 3.1 auto_arima avec pmdarima

```python
import pmdarima as pm
from pmdarima import auto_arima

def selection_automatique_arima(serie: pd.Series,
                                  saisonnier: bool = False,
                                  periode: int = None,
                                  D_max: int = 1) -> dict:
    """
    Selection automatique de l'ordre ARIMA par AIC/BIC.

    auto_arima explore le "stepwise" : demarre d'un modele simple
    et explore les voisins (p±1, q±1) en retenant le meilleur AIC.

    Args:
        saisonnier: True pour SARIMA
        periode: periode saisonniere (12=mensuel, 7=journalier, 52=hebdo annuel)
        D_max: ordre max de differentiation saisonniere
    """
    params = {
        'information_criterion': 'aic',
        'stepwise': True,         # False pour grid complet (lent)
        'seasonal': saisonnier,
        'test': 'adf',            # test de stationnarite auto
        'max_p': 5,
        'max_q': 5,
        'max_d': 2,
        'd': None,                # auto-determination
        'trace': True,            # affiche les modeles testes
        'error_action': 'ignore',
        'suppress_warnings': True
    }

    if saisonnier and periode:
        params.update({
            'm': periode,
            'max_P': 2,
            'max_Q': 2,
            'max_D': D_max,
            'D': None             # auto-determination D
        })

    modele = auto_arima(serie.dropna(), **params)

    print(f"\n=== Meilleur modele selectionne ===")
    print(modele.summary())
    print(f"\nOrdre : {modele.order}")
    if saisonnier:
        print(f"Ordre saisonnier : {modele.seasonal_order}")
    print(f"AIC : {modele.aic():.2f}")
    print(f"BIC : {modele.bic():.2f}")

    return {
        'modele': modele,
        'ordre': modele.order,
        'ordre_saisonnier': modele.seasonal_order if saisonnier else None,
        'aic': modele.aic(),
        'bic': modele.bic()
    }
```

### 3.2 Estimation manuelle avec statsmodels

```python
from statsmodels.tsa.arima.model import ARIMA
from statsmodels.tsa.statespace.sarimax import SARIMAX

def estimer_arima(serie: pd.Series,
                   ordre: tuple = (1, 1, 1)) -> dict:
    """
    Estimation ARIMA avec statsmodels — controle total des parametres.

    ordre: (p, d, q)
    """
    modele = ARIMA(
        serie.dropna(),
        order=ordre,
        trend='c'  # constante
    )
    resultat = modele.fit(method='lbfgs')  # ou 'nm', 'bfgs'

    print(resultat.summary())
    return {
        'resultat': resultat,
        'aic': resultat.aic,
        'bic': resultat.bic,
        'residus': resultat.resid,
        'parametres': {
            'ar': resultat.arparams.tolist() if len(resultat.arparams) > 0 else [],
            'ma': resultat.maparams.tolist() if len(resultat.maparams) > 0 else [],
            'sigma2': float(resultat.params.get('sigma2', np.nan))
        }
    }


def estimer_sarima(serie: pd.Series,
                    ordre: tuple = (1, 1, 1),
                    ordre_saisonnier: tuple = (1, 1, 1, 12)) -> dict:
    """
    Estimation SARIMA(p,d,q)(P,D,Q)s avec statsmodels.

    ordre_saisonnier: (P, D, Q, s) ou s est la periode
    """
    modele = SARIMAX(
        serie.dropna(),
        order=ordre,
        seasonal_order=ordre_saisonnier,
        trend='c',
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    resultat = modele.fit(disp=False, maxiter=200)

    print(f"SARIMA{ordre}{ordre_saisonnier} — AIC: {resultat.aic:.2f}")
    print(resultat.summary())

    return {
        'resultat': resultat,
        'aic': resultat.aic,
        'bic': resultat.bic,
        'residus': resultat.resid
    }
```

---

## 4. Interpretation SARIMA(p,d,q)(P,D,Q)s

### 4.1 Signification des ordres saisonniers

**P** : ordre autoregressif saisonnier — correle Xt avec X_{t-s}, X_{t-2s}, ...
**D** : differentiation saisonniere — elimine la tendance saisonniere (delta_s)
**Q** : ordre MA saisonnier — erreurs retardees de s, 2s, ...
**s** : periode de la saisonnalite (7, 12, 52, 365)

Exemple SARIMA(1,1,1)(1,1,1)12 mensuel :
- AR(1) : depend de Xt-1
- MA(1) : depend de et-1
- SAR(1) : depend de Xt-12 (meme mois l'an passe)
- SMA(1) : depend de et-12

### 4.2 Table de correspondance frequence / periode

| Frequence donnees | Periode s | Modele typique |
|---|---|---|
| Journaliere | 7 (hebdo) | SARIMA(p,d,q)(P,D,Q)7 |
| Journaliere | 365 | Complexe — Prophet preferable |
| Hebdomadaire | 52 | SARIMA(p,d,q)(P,D,Q)52 |
| Mensuelle | 12 | SARIMA(p,d,q)(P,D,Q)12 |
| Trimestrielle | 4 | SARIMA(p,d,q)(P,D,Q)4 |

---

## 5. Etape 3 — Diagnostic des Residus

Le diagnostic est l'etape la plus critique. Des residus non-adequats indiquent
un modele mal specifie.

```python
from statsmodels.stats.diagnostic import acorr_ljungbox, het_arch
from scipy import stats
import matplotlib.pyplot as plt
import seaborn as sns

def diagnostic_complet_residus(resultat_modele,
                                titre: str = "ARIMA") -> dict:
    """
    Diagnostic exhaustif des residus d'un modele ARIMA/SARIMA.
    Reproduit le panel diagnostique de R (tsdiag).

    Verifie :
    1. Stationnarite des residus (pas de tendance visible)
    2. Autocorrelation (Ljung-Box)
    3. Normalite (Jarque-Bera + QQ plot)
    4. Heteroscedasticite (ARCH test)
    """
    residus = pd.Series(resultat_modele.resid).dropna()
    n = len(residus)

    # 1. Test de Ljung-Box (pas d'autocorrelation)
    lags_lb = [5, 10, 15, 20, min(50, n // 5)]
    lb_resultats = acorr_ljungbox(residus, lags=lags_lb, return_df=True)
    lb_ok = (lb_resultats['lb_pvalue'] > 0.05).all()

    # 2. Test de normalite Jarque-Bera
    jb_stat, jb_pvalue = stats.jarque_bera(residus)
    normalite_ok = jb_pvalue > 0.05

    # 3. Test ARCH (heteroscedasticite conditionnelle)
    arch_lm, arch_pvalue = het_arch(residus, nlags=12)[:2]
    homosc_ok = arch_pvalue > 0.05

    # 4. Statistiques descriptives des residus
    skewness = float(stats.skew(residus))
    kurtosis = float(stats.kurtosis(residus))

    # Panel graphique complet
    fig, axes = plt.subplots(2, 3, figsize=(16, 10))
    fig.suptitle(f'Diagnostic des Residus — {titre}', fontsize=14)

    # Residus dans le temps
    axes[0, 0].plot(residus.values)
    axes[0, 0].axhline(y=0, color='red', linestyle='--', alpha=0.5)
    axes[0, 0].set_title('Residus dans le temps')

    # ACF residus
    plot_acf(residus, lags=40, ax=axes[0, 1], zero=False)
    axes[0, 1].set_title('ACF des Residus (Ljung-Box)')

    # PACF residus
    plot_pacf(residus, lags=40, ax=axes[0, 2],
              zero=False, method='ywm')
    axes[0, 2].set_title('PACF des Residus')

    # Distribution des residus
    sns.histplot(residus, kde=True, ax=axes[1, 0])
    axes[1, 0].set_title(f'Distribution (Skew={skewness:.2f}, Kurt={kurtosis:.2f})')

    # QQ Plot
    stats.probplot(residus, dist='norm', plot=axes[1, 1])
    axes[1, 1].set_title('QQ Plot (Normalite)')

    # Residus^2 (heteroscedasticite)
    (residus**2).plot(ax=axes[1, 2])
    axes[1, 2].set_title('Residus^2 (Heteroscedasticite ARCH)')

    plt.tight_layout()
    plt.show()

    # Rapport
    rapport = {
        'ljung_box': {
            'resultats': lb_resultats.to_dict(),
            'ok': lb_ok,
            'interpretation': 'Residus white noise' if lb_ok
                              else 'ALERTE: Autocorrelation residuelle — augmenter p ou q'
        },
        'normalite_jarque_bera': {
            'statistique': round(jb_stat, 4),
            'pvalue': round(jb_pvalue, 4),
            'ok': normalite_ok,
            'interpretation': 'Distribution normale acceptable' if normalite_ok
                              else 'Non-normalite — intervalles de confiance biaies'
        },
        'arch_heteroscedasticite': {
            'statistique': round(arch_lm, 4),
            'pvalue': round(arch_pvalue, 4),
            'ok': homosc_ok,
            'interpretation': 'Variance constante' if homosc_ok
                              else 'Effets ARCH — envisager GARCH ou transformation'
        },
        'skewness': round(skewness, 4),
        'kurtosis': round(kurtosis, 4),
        'modele_adequat': lb_ok and homosc_ok
    }

    print("\n=== Rapport Diagnostic ===")
    for cle, val in rapport.items():
        if isinstance(val, dict) and 'interpretation' in val:
            statut = "OK" if val['ok'] else "ECHEC"
            print(f"  [{statut}] {cle}: {val['interpretation']}")

    print(f"\nConclusion: modele {'ADEQUAT' if rapport['modele_adequat'] else 'NON ADEQUAT — respecifier'}")
    return rapport
```

---

## 6. Etape 4 — Prevision avec Intervalles de Confiance

```python
def prevoir_arima(resultat_modele,
                   horizon: int = 12,
                   alpha: float = 0.05) -> pd.DataFrame:
    """
    Genere des previsions avec intervalles de confiance.

    alpha: niveau de signification (0.05 pour IC 95%)
    """
    forecast = resultat_modele.get_forecast(steps=horizon)
    forecast_summary = forecast.summary_frame(alpha=alpha)

    print(f"\nPrevisions sur {horizon} pas (IC {(1-alpha)*100:.0f}%):")
    print(forecast_summary[['mean', 'mean_ci_lower', 'mean_ci_upper']].round(4))

    # Graphique
    fig, ax = plt.subplots(figsize=(14, 6))

    # Historique (80 derniers points)
    n_historique = min(80, len(resultat_modele.fittedvalues))
    historique = resultat_modele.fittedvalues[-n_historique:]
    ax.plot(historique, label='Historique ajuste', color='steelblue')

    # Previsions
    ax.plot(forecast_summary.index, forecast_summary['mean'],
            color='red', label='Prevision')
    ax.fill_between(
        forecast_summary.index,
        forecast_summary['mean_ci_lower'],
        forecast_summary['mean_ci_upper'],
        alpha=0.3, color='red',
        label=f'IC {(1-alpha)*100:.0f}%'
    )
    ax.legend()
    ax.set_title(f'Previsions ARIMA — Horizon {horizon} pas')
    plt.tight_layout()
    plt.show()

    return forecast_summary


def prevoir_sarima_statsmodels(serie: pd.Series,
                                ordre: tuple,
                                ordre_saisonnier: tuple,
                                horizon: int = 12) -> pd.DataFrame:
    """
    Pipeline complet : estimation + prevision SARIMA en une fonction.
    """
    modele = SARIMAX(
        serie.dropna(),
        order=ordre,
        seasonal_order=ordre_saisonnier,
        trend='c',
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    resultat = modele.fit(disp=False)
    return prevoir_arima(resultat, horizon=horizon)
```

---

## 7. SARIMAX — Regresseurs Exogenes

```python
def sarimax_avec_regresseurs(serie: pd.Series,
                               regresseurs_train: pd.DataFrame,
                               regresseurs_test: pd.DataFrame,
                               ordre: tuple = None,
                               ordre_saisonnier: tuple = None) -> dict:
    """
    SARIMAX : SARIMA avec variables exogenes.
    Les regresseurs futurs doivent etre connus (variables de plan, jours feries).

    regresseurs_train: DataFrame avec les memes index que serie
    regresseurs_test: DataFrame pour la periode de prevision
    """
    # Selection auto si ordre non specifie
    if ordre is None:
        modele_auto = auto_arima(
            serie,
            exogenous=regresseurs_train,
            seasonal=ordre_saisonnier is not None,
            m=ordre_saisonnier[3] if ordre_saisonnier else 1,
            trace=False,
            suppress_warnings=True
        )
        ordre = modele_auto.order
        ordre_saisonnier = modele_auto.seasonal_order

    modele = SARIMAX(
        serie.dropna(),
        exog=regresseurs_train,
        order=ordre,
        seasonal_order=ordre_saisonnier or (0, 0, 0, 0),
        enforce_stationarity=False,
        enforce_invertibility=False
    )
    resultat = modele.fit(disp=False, maxiter=300)

    # Previsions avec regresseurs futurs
    forecast = resultat.get_forecast(
        steps=len(regresseurs_test),
        exog=regresseurs_test
    )
    forecast_df = forecast.summary_frame()

    print(f"SARIMAX{ordre}{ordre_saisonnier} — AIC: {resultat.aic:.2f}")
    print(f"Coefficients des regresseurs:")
    for col in regresseurs_train.columns:
        coef = resultat.params.get(col, None)
        pval = resultat.pvalues.get(col, None)
        if coef is not None:
            print(f"  {col}: {coef:.4f} (p={pval:.4f})")

    return {
        'resultat': resultat,
        'forecast': forecast_df,
        'ordre': ordre,
        'ordre_saisonnier': ordre_saisonnier,
        'aic': resultat.aic,
        'regresseurs': list(regresseurs_train.columns)
    }
```

---

## 8. VAR — Series Multivariees

```python
from statsmodels.tsa.vector_ar.var_model import VAR
from statsmodels.tsa.stattools import grangercausalitytests

def modele_var(df_series: pd.DataFrame,
               max_lags: int = 12,
               horizon: int = 12) -> dict:
    """
    VAR (Vector AutoRegression) pour series multivariees.
    Toutes les series doivent etre stationnaires.

    df_series: DataFrame avec une colonne par serie, index temporel.
    """
    # Verifier stationnarite de chaque serie
    for col in df_series.columns:
        pval = adfuller(df_series[col].dropna(), autolag='AIC')[1]
        print(f"ADF {col}: p={pval:.4f} {'OK' if pval < 0.05 else 'NON-STATIONNAIRE'}")

    # Ajustement VAR
    modele = VAR(df_series.dropna())

    # Selection de l'ordre par AIC
    resultats_selection = modele.select_order(maxlags=max_lags)
    print("\nSelection de l'ordre VAR:")
    print(resultats_selection.summary())

    p_optimal = resultats_selection.aic

    # Estimation
    resultat = modele.fit(p_optimal)
    print(resultat.summary())

    # Previsions
    y_last = df_series.dropna().values[-p_optimal:]
    forecast = resultat.forecast(y=y_last, steps=horizon)
    df_forecast = pd.DataFrame(
        forecast,
        columns=df_series.columns
    )

    return {
        'resultat': resultat,
        'p_optimal': p_optimal,
        'forecast': df_forecast,
        'aic': resultat.aic
    }


def tester_causalite_granger(df_series: pd.DataFrame,
                              max_lag: int = 12) -> pd.DataFrame:
    """
    Teste la causalite au sens de Granger entre paires de series.
    H0 : serie X ne cause pas serie Y (au sens Granger)
    p < 0.05 : X contient info predictive sur Y
    """
    colonnes = df_series.columns.tolist()
    resultats = []

    for y_col in colonnes:
        for x_col in colonnes:
            if x_col != y_col:
                test_data = df_series[[y_col, x_col]].dropna()
                try:
                    test_results = grangercausalitytests(
                        test_data, maxlag=max_lag, verbose=False
                    )
                    # Prendre le meilleur lag (pvalue min)
                    pvalues = [test_results[lag][0]['ssr_ftest'][1]
                               for lag in range(1, max_lag + 1)]
                    best_pvalue = min(pvalues)
                    best_lag = pvalues.index(best_pvalue) + 1

                    resultats.append({
                        'cause': x_col,
                        'effet': y_col,
                        'meilleur_lag': best_lag,
                        'pvalue': round(best_pvalue, 4),
                        'causalite_granger': best_pvalue < 0.05
                    })
                except Exception as e:
                    print(f"Erreur {x_col} → {y_col}: {e}")

    df_res = pd.DataFrame(resultats)
    print("\nTest de causalite de Granger:")
    print(df_res[df_res['causalite_granger']].to_string(index=False))
    return df_res
```

---

## 9. Comparaison ARIMA vs Prophet vs ML

### 9.1 Tableau de decision

| Critere | ARIMA/SARIMA | Prophet | ML (LightGBM) |
|---|---|---|---|
| Interpretabilite | Excellente | Bonne | Faible |
| Jours feries | Manuel (SARIMAX) | Natif | Feature engineering |
| Donnees manquantes | Problematique | Natif | Feature engineering |
| Changepoints | Manuel | Automatique | Pas de concept |
| Multiples saisonnalites | Difficile | Natif | Features |
| Tres longues series | Lent | Correct | Tres efficace |
| Multi-series (100+) | Impraticable | Batch OK | Global model ideal |
| Exogenes (futures connues) | SARIMAX | Regresseurs | Features directes |
| Intervalles de confiance | Analytiques | Simulation | Quantile regression |
| Setup / Tuning | Expert requis | Accessible | Expertise ML |
| Minimum de donnees | 30-50 obs | 1-2 cycles | 500+ obs |

### 9.2 Regles de selection pratiques

```
ARIMA/SARIMA : choisir quand
  → Serie unique, besoins d'interpretabilite elevee
  → Equipe avec expertise statistique
  → Moins de 200 observations
  → Relations lineaires clairement etablies
  → Publication academique ou reglementaire

Prophet : choisir quand
  → Series business avec jours feries importants
  → Donnees manquantes frequentes
  → Equipe non-experte en ARIMA
  → Entre 100 et 2 ans de donnees journalieres
  → Batch de plusieurs series independantes

ML (LightGBM/XGBoost) : choisir quand
  → Centaines de series similaires (global model)
  → Dependances non-lineaires complexes
  → Nombreuses covariables externes disponibles
  → Series tres longues (>2 ans de donnees horaires)
  → Precision prime sur interpretabilite
```

---

## 10. Limites d'ARIMA et Cas Difficiles

### 10.1 Non-linearite

ARIMA est fondamentalement lineaire. Si la relation entre les lags et la valeur
courante est non-lineaire, les residus auront de la structure.

Solutions :
- Transformer la serie (log, Box-Cox)
- Threshold ARIMA (TAR, SETAR) pour les regimes
- Transition vers modeles ML (LightGBM avec features lags)

### 10.2 Regime changes (ruptures structurelles)

Un changement de regime (crise, changement de politique) invalide les parametres
estimes avant la rupture.

```python
from statsmodels.tsa.statespace.structural import UnobservedComponents

def modele_structurel_local(serie: pd.Series,
                              niveau: str = 'local linear trend') -> dict:
    """
    Modele structurel par composantes non-observees (UCM).
    Plus robuste aux ruptures qu'ARIMA.
    Decompose explicitement niveau, tendance, saisonnalite.
    """
    modele = UnobservedComponents(
        serie.dropna(),
        level=niveau,
        seasonal=12 if len(serie) > 24 else None,
        autoregressive=1
    )
    resultat = modele.fit(disp=False, maxiter=200)
    print(resultat.summary())

    return {'resultat': resultat, 'aic': resultat.aic}
```

### 10.3 Stationnarite non-lineaire

La stationnarite peut etre locale mais pas globale. Solutions :
- Differencier par tranches
- Modeliser les ecarts par rapport a une tendance filtree (HP filter)
- Utiliser des modeles GARCH pour la variance

### 10.4 Walk-Forward Validation pour ARIMA

```python
from sklearn.metrics import mean_absolute_error, mean_squared_error

def walk_forward_arima(serie: pd.Series,
                        ordre: tuple,
                        ordre_saisonnier: tuple = None,
                        horizon: int = 12,
                        n_splits: int = 5) -> dict:
    """
    Walk-forward validation pour ARIMA.
    Re-estime le modele a chaque fenetre pour simuler la production.
    """
    n = len(serie)
    taille_min = n - n_splits * horizon
    resultats = []

    for i in range(n_splits):
        fin_train = taille_min + i * horizon
        train = serie.iloc[:fin_train]
        test = serie.iloc[fin_train:fin_train + horizon]

        if len(test) == 0:
            break

        try:
            if ordre_saisonnier:
                modele = SARIMAX(
                    train,
                    order=ordre,
                    seasonal_order=ordre_saisonnier,
                    enforce_stationarity=False,
                    enforce_invertibility=False
                )
            else:
                modele = ARIMA(train, order=ordre, trend='c')

            resultat = modele.fit(disp=False)
            forecast = resultat.get_forecast(steps=len(test))
            y_pred = forecast.predicted_mean.values
            y_true = test.values[:len(y_pred)]

            mae = mean_absolute_error(y_true, y_pred)
            rmse = np.sqrt(mean_squared_error(y_true, y_pred))
            mape = np.mean(np.abs((y_true - y_pred) / (y_true + 1e-8))) * 100

            resultats.append({
                'split': i + 1,
                'fin_train': train.index[-1],
                'n_train': len(train),
                'mae': round(mae, 4),
                'rmse': round(rmse, 4),
                'mape': round(mape, 2)
            })

        except Exception as e:
            print(f"Erreur split {i+1}: {e}")

    df_res = pd.DataFrame(resultats)
    print("\n=== Walk-Forward Validation ARIMA ===")
    print(df_res.to_string(index=False))
    print(f"\nMAPE moyen: {df_res['mape'].mean():.2f}%")
    print(f"RMSE moyen: {df_res['rmse'].mean():.4f}")

    return {
        'detail': df_res,
        'mape_moyen': df_res['mape'].mean(),
        'rmse_moyen': df_res['rmse'].mean()
    }
```

---

## Synthese Operationnelle

### Checklist Box-Jenkins Complete

```
ETAPE 1 - IDENTIFICATION
  [ ] Tracer la serie et identifier patterns visuels
  [ ] Tests ADF + KPSS → determiner d
  [ ] Appliquer differentiation (d fois)
  [ ] Tracer ACF + PACF de la serie stationnaire
  [ ] Appliquer regles de decision → bornes initiales p et q
  [ ] Detecter saisonnalite → determiner D et s

ETAPE 2 - ESTIMATION
  [ ] Lancer auto_arima pour exploration systematique
  [ ] Valider les candidats AIC/BIC
  [ ] Verifier convergence et significance des parametres
  [ ] Tester 2-3 modeles concurrents

ETAPE 3 - DIAGNOSTIC
  [ ] Ljung-Box sur les residus → p > 0.05 a tous les lags
  [ ] QQ Plot + Jarque-Bera → normalite des residus
  [ ] Test ARCH → homoscedasticite
  [ ] Aucune structure residuelle dans ACF/PACF des residus
  [ ] Si diagnostic echoue → retour etape 1

ETAPE 4 - PREVISION
  [ ] Walk-forward validation → MAPE base de reference
  [ ] Comparer au baseline naive saisonnier
  [ ] Generer previsions avec IC 95%
  [ ] Documenter les hypotheses et limites
```

### Codes d'erreur frequents et solutions

| Erreur | Cause probable | Solution |
|---|---|---|
| Non-convergence MLE | Ordre trop eleve ou donnees insuffisantes | Reduire p ou q |
| Residus autocorreles (LB p<0.05) | Ordre sous-specifie | Augmenter p et/ou q |
| Residus non-normaux (JB p<0.05) | Outliers ou non-linearite | Transformer serie ou traiter outliers |
| ARCH detecte dans residus | Heteroscedasticite | GARCH ou transformation log |
| AIC non ameliore | Modele deja optimal | Verifier si ARIMA est adapte |
| Erreur "not invertible" | Racines MA hors cercle unite | enforce_invertibility=True ou reduire q |
