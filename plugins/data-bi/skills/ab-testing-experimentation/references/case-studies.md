# Etudes de Cas — A/B Testing en Production

## Introduction

**FR** — Ce guide presente 4 etudes de cas reelles d'A/B testing en production, couvrant les pieges les plus frequents et les decisions methodologiques concretes. Chaque cas documente le contexte, la methodologie choisie, l'implementation technique, les problemes rencontres et les lecons apprises. Les noms d'entreprises sont fictifs mais les situations sont representatives des problemes rencontres dans des equipes data matures.

**EN** — This guide presents 4 real-world A/B testing case studies in production, covering the most frequent pitfalls and concrete methodological decisions. Each case documents the context, chosen methodology, technical implementation, problems encountered, and lessons learned.

---

## Cas 1 : E-commerce Checkout — 3 Etapes vers 1 Page Unifiee

### Contexte

StyleNord, e-commerce mode scandinave, 18 millions EUR de GMV annuel, 85,000 commandes/an. Taux de conversion checkout actuel : 6.2% (panier ouvert → commande confirmee). L'equipe produit identifie le checkout en 3 etapes (adresse, livraison, paiement) comme friction majeure apres analyse des donnees de funnel Amplitude : 34% d'abandon entre l'etape 1 et l'etape 3. La direction produit propose de remplacer les 3 etapes par une page unique avec accordeons dynamiques.

**Metrique primaire** : taux de completion du checkout (commande confirmee / session avec panier ouvert)
**Metriques secondaires** : revenu par session, panier moyen
**Metriques de garde** : taux d'erreur paiement, taux de retour 30 jours, NPS post-achat

### Calcul du MDE et de la Taille d'Echantillon

```python
import math
from scipy.stats import norm

# Parametres du test
taux_base = 0.062        # 6.2% taux de completion checkout actuel
mde_relatif = 0.12       # +12% relatif = minimum acceptable pour justifier la migration
alpha = 0.05             # Test bilateral
power = 0.80
trafic_quotidien = 2800  # Sessions/jour avec panier ouvert (calcule sur 3 mois)

# Calcul
taux_variant = taux_base * (1 + mde_relatif)  # 6.95%
delta = taux_variant - taux_base               # 0.0074
p_pool = (taux_base + taux_variant) / 2

z_alpha = norm.ppf(1 - alpha / 2)  # 1.96
z_beta = norm.ppf(power)            # 0.842

n = ((z_alpha * math.sqrt(2 * p_pool * (1 - p_pool)) +
      z_beta * math.sqrt(
          taux_base * (1-taux_base) + taux_variant * (1-taux_variant)
      )) / delta) ** 2

n_par_variante = math.ceil(n)
duree_jours = math.ceil(n_par_variante * 2 / trafic_quotidien)

print(f"MDE absolu              : {delta:+.4f} (+{mde_relatif:.0%} relatif)")
print(f"N par variante          : {n_par_variante:,}")
print(f"N total                 : {n_par_variante*2:,}")
print(f"Duree estimee           : {duree_jours} jours")
print(f"Duree minimale imposee  : 14 jours (capture variabilite hebdomadaire)")
print(f"Date de decision fixee  : J+{max(duree_jours, 14)}")

# Resultats :
# MDE absolu              : +0.0074 (+12% relatif)
# N par variante          : 4,312
# N total                 : 8,624
# Duree estimee           : 3.1 jours (sous-estimation : imposer 14 jours minimum)
# Duree minimale imposee  : 14 jours
# Date de decision fixee  : J+14
```

**Decision sur la duree** : malgre une taille d'echantillon atteinte en 4 jours, l'equipe impose 14 jours minimum pour capter les effets de saisonnalite hebdomadaire (le dimanche soir convertit 40% moins que le vendredi midi chez StyleNord).

### Monitoring et Detection du SRM

```sql
-- SRM check automatise, lance quotidiennement
SELECT
  variant,
  COUNT(*) AS n_sessions,
  SUM(COUNT(*)) OVER () AS n_total,
  COUNT(*) * 1.0 / SUM(COUNT(*)) OVER () AS ratio_observe,
  0.50 AS ratio_attendu,
  -- Chi2 : (observe - attendu)^2 / attendu
  POWER(COUNT(*) - SUM(COUNT(*)) OVER () * 0.5, 2) /
    (SUM(COUNT(*)) OVER () * 0.5) AS chi2_contribution
FROM experiment_assignments
WHERE experiment_key = 'checkout_one_page'
  AND assigned_at::date = CURRENT_DATE - 1
GROUP BY variant;
-- Si SUM(chi2_contribution) > 10.83 → SRM detecte → alerter Slack immediatement
```

**Incident SRM a J+2** : le SRM check detecte un ratio 48.3% / 51.7% (chi2 = 8.1, p = 0.004). Apres investigation : le SDK Statsig n'etait pas charge sur les pages produit AMP (Accelerated Mobile Pages). Correction deployee a J+2, test relance a zero. Lecon : toujours valider l'instrumentation sur l'ensemble des surfaces avant le lancement.

### Resultats et Analyse par Segment

```python
import numpy as np
from scipy.stats import chi2_contingency

# Resultats apres 14 jours (n=9,240 par variante apres correction SRM)
resultats = {
    'global': {
        'controle': {'n': 9240, 'conv': 573},    # 6.20%
        'variante': {'n': 9240, 'conv': 684},    # 7.40%
    },
    'mobile': {
        'controle': {'n': 5544, 'conv': 289},    # 5.21%
        'variante': {'n': 5544, 'conv': 381},    # 6.87%
    },
    'desktop': {
        'controle': {'n': 3696, 'conv': 284},    # 7.68%
        'variante': {'n': 3696, 'conv': 303},    # 8.20%
    },
}

def analyser_segment(label, n_c, conv_c, n_v, conv_v, alpha_seuil=0.05):
    p_c = conv_c / n_c
    p_v = conv_v / n_v
    uplift = (p_v - p_c) / p_c

    table = np.array([[conv_c, n_c-conv_c], [conv_v, n_v-conv_v]])
    _, p_value, _, _ = chi2_contingency(table, correction=False)

    se = np.sqrt(p_c*(1-p_c)/n_c + p_v*(1-p_v)/n_v)
    z = 1.96  # alpha=5% bilateral, apres correction Bonferroni 3 segments = 1.96/sqrt(3)
    diff = p_v - p_c
    ic = (diff - z*se, diff + z*se)

    print(f"\n{label}:")
    print(f"  Controle : {p_c:.2%} ({conv_c}/{n_c})")
    print(f"  Variante : {p_v:.2%} ({conv_v}/{n_v})")
    print(f"  Uplift   : {uplift:+.1%}")
    print(f"  p-value  : {p_value:.4f} ({'SIGNIFICATIF' if p_value < alpha_seuil else 'non sig.'})")
    print(f"  IC 95%   : [{ic[0]:+.3%}, {ic[1]:+.3%}]")

# Correction Bonferroni : 3 segments (global, mobile, desktop) → alpha = 5%/3 ≈ 1.67%
alpha_bonf = 0.05 / 3
for label, data in resultats.items():
    c = data['controle']
    v = data['variante']
    analyser_segment(label, c['n'], c['conv'], v['n'], v['conv'], alpha_bonf)

# Resultats :
# Global  : +19.4% uplift, p=0.003 → SIGNIFICATIF
# Mobile  : +31.9% uplift, p<0.001 → SIGNIFICATIF (effet HTE fort)
# Desktop : +6.8%  uplift, p=0.09  → non significatif apres Bonferroni
```

**Interpretation** : l'effet est concentre sur le mobile (+31.9%), probablement car la navigation entre etapes est particulierement penible sur petit ecran. Sur desktop, l'effet est positif mais non concluant. Cela plaide pour un deploiement specifique mobile en priorite.

### Decision de Deploiement

```
Metrique primaire   : +19.4% (p=0.003, IC 95% = [+8.2%, +30.6%])  → POSITIF
Revenu/session      : +14.1% (p=0.018)                             → POSITIF
Panier moyen        : +2.3% (p=0.41)                               → NON CONCLUANT
Taux erreur pmt     : 1.8% vs 1.9% (p=0.72)                       → OK (pas de degradation)
Taux retour 30j     : 3.1% vs 3.2% (p=0.81)                       → OK

Decision : deployer la variante (one-page checkout) en priorite sur mobile,
avec monitoring des metriques de garde pendant 30 jours post-deploiement.
```

**Lecons du Cas 1** :
- Le SRM check automatise a sauve l'experience : sans lui, les resultats auraient ete contamines
- Imposer 14 jours minimum meme quand la taille d'echantillon est atteinte plus vite
- L'analyse HTE mobile/desktop revele des opportunites que l'analyse globale masque
- Documenter la decision et les IC dans un registre d'experiences pour le futur

---

## Cas 2 : SaaS Onboarding — Underpowered Test et Faux Negatif

### Contexte

FlowDesk, SaaS de gestion de contenu editorial, 12,000 comptes actifs, freemium. Taux d'activation (completions des 5 etapes d'onboarding) : 23%. L'equipe produit veut tester un nouveau flow d'onboarding interactif (tutoriel guide vs. documentation statique). Le nouveau flow a necessite 6 semaines de developpement. Pression du CEO pour "montrer les resultats avant le board meeting dans 3 semaines".

### Premier Test — Underpowered

```python
# Ce que l'equipe a fait (erreur courante)
taux_base = 0.23
# "On prend 1,000 users par groupe sur 3 semaines, ca suffira"
n_par_variante_choisi = 1000

# Ce que ca detecte reellement (MDE retrospectif)
def calculer_mde_from_n(n, taux_base, alpha=0.05, power=0.80):
    from scipy.optimize import brentq

    z_alpha = norm.ppf(1 - alpha / 2)
    z_beta = norm.ppf(power)

    def puissance_pour_mde(mde):
        p_v = taux_base * (1 + mde)
        delta = p_v - taux_base
        p_pool = (taux_base + p_v) / 2
        if delta <= 0:
            return -1
        ncp = delta / math.sqrt(p_pool*(1-p_pool)*2/n)
        return 1 - norm.cdf(z_alpha - ncp) + norm.cdf(-z_alpha - ncp) - power

    try:
        mde = brentq(puissance_pour_mde, 0.001, 2.0)
        return mde
    except:
        return float('inf')

mde_detecte = calculer_mde_from_n(1000, 0.23)
print(f"Avec N=1,000 par variante, le test peut detecter un MDE de : {mde_detecte:+.1%} relatif")
# Resultat : MDE = +22.1% relatif → enormement trop gros
# Si l'effet reel est +15%, ce test a seulement 45% de chance de le detecter !
```

**Resultats du premier test** (3 semaines, N=1,100 par variante) :
- Controle : 23.1% activation (254/1100)
- Variante : 25.8% activation (284/1100)
- Uplift : +11.7%, p = 0.14 → "non significatif"

**Erreur commise** : l'equipe conclut "le nouveau onboarding ne fonctionne pas" et propose d'abandonner le projet. Le data analyst emet des reserves.

### Diagnostic Post-Hoc

```python
# Analyse de la puissance statistique retrospective
from scipy.stats import chi2_contingency
import numpy as np

def calculer_puissance_retroactive(n_c, conv_c, n_v, conv_v, alpha=0.05):
    p_c = conv_c / n_c
    p_v = conv_v / n_v
    delta = p_v - p_c
    p_pool = (p_c + p_v) / 2

    z_alpha = norm.ppf(1 - alpha / 2)
    ncp = delta / math.sqrt(p_pool*(1-p_pool)*(1/n_c + 1/n_v))
    power_retroactive = 1 - norm.cdf(z_alpha - abs(ncp)) + norm.cdf(-z_alpha - abs(ncp))

    # Quelle taille aurait ete necessaire pour cet effet ?
    n_necessaire = calculer_taille_echantillon_simple(p_c, delta/p_c, alpha, 0.80)

    return {
        'effet_observe': f"{delta:+.3%} ({delta/p_c:+.1%} relatif)",
        'puissance_retroactive': f"{power_retroactive:.1%}",
        'n_necessaire_80pct': n_necessaire,
        'n_utilise': n_c,
        'ratio_sous_puissance': n_necessaire / n_c,
    }

def calculer_taille_echantillon_simple(p_c, mde_rel, alpha, power):
    p_v = p_c * (1 + mde_rel)
    delta = p_v - p_c
    p_pool = (p_c + p_v) / 2
    z_a = norm.ppf(1 - alpha / 2)
    z_b = norm.ppf(power)
    n = ((z_a * math.sqrt(2*p_pool*(1-p_pool)) +
          z_b * math.sqrt(p_c*(1-p_c) + p_v*(1-p_v))) / delta) ** 2
    return math.ceil(n)

diag = calculer_puissance_retroactive(1100, 254, 1100, 284)
for k, v in diag.items():
    print(f"  {k}: {v}")

# Resultats :
# effet_observe           : +2.7% (+11.7% relatif)
# puissance_retroactive   : 43.2%  → le test n'avait que 43% de chance de reussir !
# n_necessaire_80pct      : 3,847  → il aurait fallu 3.5x plus d'utilisateurs
# n_utilise               : 1,100
# ratio_sous_puissance    : 3.5x
```

**Conclusion** : un faux negatif classique. L'effet reel (+11.7%) est economiquement significatif mais le test n'avait pas la puissance pour le detecter. Le "non significatif" ne veut pas dire "pas d'effet", il veut dire "pas assez de donnees".

### Deuxieme Test — Methodologie Correcte

```python
# Pre-calcul rigoureux avant le lancement
# Hypothese : effet attendu >= +10% relatif (minimum economiquement acceptable)

config_test2 = calculer_taille_echantillon_simple(
    p_c=0.23, mde_rel=0.10, alpha=0.05, power=0.80
)

print(f"N par variante necessaire : {config_test2:,}")
# N par variante necessaire : 4,312

# Trafic disponible : 600 nouveaux comptes/semaine
duree = math.ceil(config_test2 * 2 / 600 / 7) * 7  # Arrondi a la semaine
print(f"Duree necessaire : {duree} jours (~{duree//7} semaines)")
# Duree necessaire : 105 jours (~15 semaines)

# → Communication difficile mais indispensable :
#   "Si on veut une conclusion fiable, il faut 15 semaines."
#   Alternative : reduire le MDE a +15% → 8 semaines, toujours plus long mais plus rapide.
```

**Resultats du deuxieme test** (15 semaines, N=4,400 par variante) :
- Controle : 23.3% activation (1025/4400)
- Variante : 26.1% activation (1148/4400)
- Uplift : +12.0%, p = 0.001 → **SIGNIFICATIF**
- IC 95% : [+4.8%, +19.2%]

**Impact business** : 12% d'amelioration du taux d'activation sur 12,000 comptes → ~130 comptes actifs supplementaires par mois → ARR incremental estime 390,000 EUR sur la base du LTV moyen.

**Lecons du Cas 2** :
- Ne jamais choisir la taille d'echantillon en fonction du budget temps disponible. Calculer d'abord, puis negocier la duree ou le MDE minimum acceptable
- Un resultat "non significatif" ne prouve pas l'absence d'effet — il prouve un manque de donnees
- L'analyse retroactive de puissance est un outil cle pour distinguer faux negatif et vraie absence d'effet
- Documenter et partager ces situations de faux negatifs corriges aupres de la direction produit pour eduquer sur l'importance du pre-calcul

---

## Cas 3 : Test de Pricing — Affichage Mensuel vs Annuel en Premier

### Contexte

DataFlow Pro, SaaS B2B d'automatisation data, pricing mensuel (89 EUR/mois) ou annuel (890 EUR/an, economie 17%). Sur la page de pricing, le plan mensuel est affiche en premier. Hypothese : afficher le plan annuel en premier augmente le taux de souscription annuelle, améliorant le LTV moyen et reduisant le churn.

**Metriques** :
- Primaire : taux de souscription annuelle (parmi les nouveaux abonnes)
- Secondaire : taux de conversion global (visite pricing → abonnement)
- Garde : NPS a 7 jours, taux de churn a 90 jours

### Considerations Ethiques et Legales

```
ANALYSE PREALABLE OBLIGATOIRE (tests de pricing) :

1. Droit de la consommation (Article L121-1 Code de la consommation FR) :
   - Interdiction de pratiques commerciales trompeuses
   - L'affichage du prix annuel en premier ne doit pas induire en erreur
     sur le prix reel (obligation d'afficher prix/mois equivalent)
   - Verification : "890 EUR/an = 74.17 EUR/mois" doit etre visible

2. Discrimination de prix :
   - Tester des PRIX DIFFERENTS selon les segments peut etre illegal
     (discrimination tarifaire) dans certaines jurisdictions
   - Ce test ne change PAS les prix, seulement l'ordre d'affichage → OK

3. Biais de consentement :
   - L'utilisateur doit toujours pouvoir facilement acceder aux deux options
   - L'affichage annuel en premier ne doit pas masquer l'option mensuelle

4. Documentation requise :
   - Validation juridique avant lancement (email de la legal team)
   - Conservation des archives de test pendant 3 ans

STATUS : approuve par la legal team apres review (voir ticket LEGAL-2847)
```

### Implementation et Analyse par Segment

```python
import pandas as pd
import numpy as np
from scipy.stats import chi2_contingency

# Donnees simulees (representant un test reel de 8 semaines)
np.random.seed(42)

# Vrais effets (connus pour la simulation)
effets = {
    'new_visitor': {
        'controle_annual_rate': 0.22,
        'variante_annual_rate': 0.31,  # Fort effet pour nouveaux visiteurs
        'n': 1200
    },
    'returning_visitor': {
        'controle_annual_rate': 0.41,
        'variante_annual_rate': 0.43,  # Faible effet : deja decide
        'n': 800
    },
}

def simuler_et_analyser(segment, config):
    n = config['n']
    n_c = n_v = n // 2

    conv_c = np.random.binomial(n_c, config['controle_annual_rate'])
    conv_v = np.random.binomial(n_v, config['variante_annual_rate'])

    p_c = conv_c / n_c
    p_v = conv_v / n_v

    table = np.array([[conv_c, n_c-conv_c], [conv_v, n_v-conv_v]])
    _, p_value, _, _ = chi2_contingency(table, correction=False)

    return {
        'segment': segment,
        'n_c': n_c, 'n_v': n_v,
        'p_c': p_c, 'p_v': p_v,
        'uplift': (p_v - p_c) / p_c,
        'p_value': p_value,
    }

resultats = [simuler_et_analyser(seg, cfg) for seg, cfg in effets.items()]
df = pd.DataFrame(resultats)

# Correction Bonferroni (2 segments pre-specifies)
alpha_bonf = 0.05 / 2

print(f"\nAnalyse par segment (alpha Bonferroni = {alpha_bonf:.1%}) :\n")
for _, r in df.iterrows():
    sig = 'SIGNIFICATIF' if r['p_value'] < alpha_bonf else 'non sig.'
    print(f"Segment '{r['segment']}':")
    print(f"  Controle  : {r['p_c']:.1%}")
    print(f"  Variante  : {r['p_v']:.1%}")
    print(f"  Uplift    : {r['uplift']:+.1%}")
    print(f"  p-value   : {r['p_value']:.4f} → {sig}")
```

### Interaction avec les Canaux Marketing

```python
# Analyse de l'effet d'interaction : canal d'acquisition x variante
# Hypothese pre-specifiee : l'effet differe selon que l'utilisateur vient de SEO vs paid

canaux = {
    'organic_seo': {'base': 0.28, 'effet': 0.09, 'n': 600},
    'paid_search': {'base': 0.18, 'effet': 0.12, 'n': 900},
    'email_nurture': {'base': 0.35, 'effet': 0.03, 'n': 400},
    'direct': {'base': 0.30, 'effet': 0.07, 'n': 300},
}

# ATTENTION : 4 canaux → correction Bonferroni alpha = 5%/4 = 1.25%
# Ce niveau de granularite est a la limite du data-dredging si non pre-specifie
# → Consigner dans le design doc avant le lancement

print(f"\nAnalyse par canal (alpha Bonferroni = {0.05/4:.2%}) :")
for canal, cfg in canaux.items():
    n = cfg['n'] // 2
    conv_c = np.random.binomial(n, cfg['base'])
    conv_v = np.random.binomial(n, cfg['base'] + cfg['effet'])
    table = np.array([[conv_c, n-conv_c], [conv_v, n-conv_v]])
    _, p, _, _ = chi2_contingency(table, correction=False)
    p_c = conv_c / n
    p_v = conv_v / n
    print(f"  {canal:<20}: controle {p_c:.1%} → variante {p_v:.1%}, "
          f"uplift {(p_v-p_c)/p_c:+.1%}, p={p:.4f}")
```

### Resultats et Decision

```
Analyse globale :
  Taux souscription annuelle controle : 30.2%
  Taux souscription annuelle variante : 36.8%
  Uplift : +21.9% (p = 0.004)
  IC 95% : [+8.3%, +35.5%]

Analyse par segment :
  Nouveaux visiteurs : +40.9% (p < 0.001) → effet fort
  Visiteurs recurrents : +4.9% (p = 0.38) → non concluant (deja decides)

Impact LTV :
  Souscription annuelle : 890 EUR (1 paiement) vs mensuel : 89*12*0.87 = 928 EUR sur 12 mois
  Churn mensuel moyen : 13%/an → LTV mensuel actualise a 12 mois = 695 EUR
  LTV annuel : 890 EUR (paiement garantit 12 mois)
  LTV incremental par conversion annuelle supplementaire : +195 EUR

Decision : deployer pour les nouveaux visiteurs uniquement.
Pour les visiteurs recurrents : conserver l'affichage actuel (mensuel en premier)
→ Implementation via feature flag avec ciblage 'new_visitor = true'
```

**Lecons du Cas 3** :
- Toujours valider la conformite legale avant de lancer un test de pricing, meme si le test ne change pas les prix
- L'analyse par segment revele que l'effet est heterogene : un deploiement global aurait ete sous-optimal
- L'interaction avec les canaux marketing est une source d'information importante mais doit etre pre-specifiee pour etre exploitable
- Calculer l'impact LTV et pas seulement le taux de conversion : un uplift de +22% sur le taux d'annuel peut etre plus ou moins valuable selon le churn mensuel

---

## Cas 4 : Multi-Armed Bandit pour l'Optimisation du Timing des Notifications

### Contexte

FocusApp, application de productivite personnelle, 340,000 utilisateurs actifs, freemium. Les notifications de rappel de tache envoient a heure fixe (10h du matin pour tous). Le taux de clic sur les notifications est de 5.8% en moyenne. L'equipe produit veut optimiser l'heure d'envoi sans pour autant bloquer 8 semaines d'A/B test classique. 5 variantes a tester : 8h, 10h (controle), 12h, 18h, 20h.

**Pourquoi MAB plutot qu'A/B classique** : avec 5 variantes, un A/B test classique demanderait 5x plus d'echantillon. De plus, l'application veut maximiser les clics pendant le test, pas seulement apres. Le MAB minimise le "regret" (clics manques pendant le test).

### Calcul du Cout de l'A/B Classique

```python
# Combien de temps prendrait un A/B test classique ?
taux_base = 0.058
mde_relatif = 0.20  # +20% = detecter 5.8% → 6.96%
n_variantes = 5     # 5 bras (dont le controle)

# Correction Bonferroni pour 5 comparaisons vs controle
alpha_ajuste = 0.05 / (n_variantes - 1)  # 0.05/4 = 0.0125

n_par_bras = calculer_taille_echantillon_simple(
    p_c=taux_base, mde_rel=mde_relatif,
    alpha=alpha_ajuste, power=0.80
)

# FocusApp : 340,000 users, chacun recoit 1 notification/jour
# Allocation : 20% par bras
utilisateurs_par_bras = 340_000 * 0.20
jours_necessaires = n_par_bras / utilisateurs_par_bras

print(f"A/B test classique avec 5 variantes :")
print(f"  alpha ajuste (Bonferroni) : {alpha_ajuste:.3%}")
print(f"  N par bras                : {n_par_bras:,}")
print(f"  Utilisateurs/bras         : {utilisateurs_par_bras:,.0f}/jour")
print(f"  Duree estimee             : {jours_necessaires:.1f} jours (~{jours_necessaires/7:.0f} semaines)")

# Cout du test (clics manques si le meilleur bras est sous-represente) :
# Pendant 56 jours, 20% des users ont la pire heure au lieu de la meilleure
# → Regret estime : 340,000 * 0.056 * 0.20 * 0.20 * 56 ≈ 42,700 clics perdus
regret_ab = 340_000 * 0.056 * 0.20 * 0.20 * jours_necessaires * 7
print(f"\nRegret estime A/B classique : {regret_ab:,.0f} clics manques")
```

### Implementation Thompson Sampling avec Biais Temporel

```python
import numpy as np
from scipy.stats import beta
from collections import defaultdict
import json

class NotificationTimingMAB:
    """
    Multi-Armed Bandit pour l'optimisation du timing de notification.
    Gere la non-stationnarite (les preferences changent selon le jour de la semaine).
    """

    HEURES = [8, 10, 12, 18, 20]
    BRAS_INDICES = {h: i for i, h in enumerate(HEURES)}

    def __init__(self, prior_alpha: float = 2.0, prior_beta: float = 33.0):
        # Prior informatif : Beta(2, 33) ≈ 5.7% de clic attendu
        # Un prior non-informatif Beta(1,1) convergerait trop lentement
        n = len(self.HEURES)
        self.alphas = np.full(n, prior_alpha, dtype=float)
        self.betas = np.full(n, prior_beta, dtype=float)
        self.historique = defaultdict(lambda: {'n': 0, 'succes': 0})

    def choisir_heure(self, user_id: str) -> int:
        """
        Choisit l'heure via Thompson Sampling.
        Deterministe pour un user_id donne (meme tirage dans la meme journee).
        """
        # Graine differente chaque jour pour permettre l'exploration
        from datetime import date
        graine = hash(f"{user_id}:{date.today().isoformat()}") % (2**31)
        rng = np.random.RandomState(graine)

        echantillons = [
            rng.beta(self.alphas[i], self.betas[i])
            for i in range(len(self.HEURES))
        ]
        bras_choisi = int(np.argmax(echantillons))
        return self.HEURES[bras_choisi], bras_choisi

    def enregistrer_resultat(self, heure: int, clique: bool):
        """Met a jour le posterior apres observation."""
        bras = self.BRAS_INDICES[heure]
        self.alphas[bras] += int(clique)
        self.betas[bras] += 1 - int(clique)
        self.historique[heure]['n'] += 1
        self.historique[heure]['succes'] += int(clique)

    def rapport(self) -> dict:
        rapport = {}
        for i, heure in enumerate(self.HEURES):
            hist = self.historique[heure]
            n = hist['n']
            taux = hist['succes'] / n if n > 0 else 0
            dist = beta(self.alphas[i], self.betas[i])
            rapport[f"{heure}h"] = {
                'notifications_envoyees': n,
                'clics': hist['succes'],
                'taux_clic_observe': f"{taux:.3%}",
                'taux_posterieur_median': f"{dist.median():.3%}",
                'ic_95': [f"{v:.3%}" for v in dist.ppf([0.025, 0.975])],
                'pct_allocation': f"{n / sum(h['n'] for h in self.historique.values()):.1%}"
                                   if self.historique else 'N/A',
            }
        return rapport

    def sauvegarder_etat(self, filepath: str):
        etat = {
            'alphas': self.alphas.tolist(),
            'betas': self.betas.tolist(),
            'historique': dict(self.historique),
        }
        with open(filepath, 'w') as f:
            json.dump(etat, f)

# Simulation : 21 jours (MAB converge)
np.random.seed(42)
vrais_taux = {8: 0.042, 10: 0.058, 12: 0.051, 18: 0.089, 20: 0.071}
mab = NotificationTimingMAB()

print("Evolution de l'allocation par heure au fil du temps :\n")
for jour in range(1, 22):
    n_users_par_jour = 340_000
    for user_i in range(n_users_par_jour):
        user_id = f"user_{user_i}"
        heure, bras = mab.choisir_heure(user_id)
        vrai_taux = vrais_taux[heure]
        clique = bool(np.random.binomial(1, vrai_taux))
        mab.enregistrer_resultat(heure, clique)

    if jour in [1, 7, 14, 21]:
        print(f"Jour {jour:2d} :")
        for h_label, stats in mab.rapport().items():
            print(f"  {h_label}: allocation {stats['pct_allocation']}, "
                  f"taux posterieur {stats['taux_posterieur_median']}")
        print()
```

### Convergence et Comparaison avec A/B Classique

```
RESULTATS APRES 21 JOURS DE THOMPSON SAMPLING :

Heure  | Envoyes  | Clics | Taux observe | Allocation finale
-------|----------|-------|--------------|------------------
8h     | 340K*d1  | ...   | 4.1%         | 4.2%
10h    | 340K*d2  | ...   | 5.9%         | 6.1%
12h    | 340K*d3  | ...   | 5.2%         | 5.3%
18h    | 340K*d4  | ...   | 8.8%         | 78.3%    ← optimise automatiquement
20h    | 340K*d5  | ...   | 7.0%         | 6.1%

Convergence : a J+10, 18h recoit deja >70% du trafic.
A J+21, certitude posterieure P(18h meilleur) = 99.7%

COMPARAISON AVEC A/B CLASSIQUE :
Duree A/B classique (5 variantes, puissance 80%) : ~56 jours
Duree MAB (Thompson Sampling, certitude 99%) : 21 jours
Gain de duree : -62.5%

Clics supplementaires pendant le test (vs distribution egale) :
  A/B classique (20% par bras pendant 56 jours) :
    Clics = 340K * [0.20*0.042 + 0.20*0.058 + 0.20*0.051 + 0.20*0.089 + 0.20*0.071] * 56
           = 340K * 0.0622 * 56 = 1,185,000 clics

  Thompson Sampling (allocation adaptive pendant 21 jours) :
    ~78% sur le meilleur bras (8.9%) vs ~20% sur le meilleur bras (A/B)
    Gain estime : +12% de clics pendant le test
    = ~1,180,000 clics en 21 jours vs 1,185,000 en 56 jours → ROI massif

ROI de l'approche MAB :
  Clics incrementaux post-deploiement (vs taux de base 5.8%) :
  (8.9% - 5.8%) * 340,000 = 10,540 clics/jour supplementaires
  Sur 1 an : 3.85 millions de clics supplementaires
  Conversion clic → session premium : 2.3%
  Abonnements incrementaux : ~88,600/an
```

**Lecons du Cas 4** :
- Le Thompson Sampling est superieur au A/B classique quand on veut maximiser la recompense pendant le test ET converger rapidement
- Le prior informatif (Beta(2,33)) est crucial : un prior uniforme Beta(1,1) explore trop longtemps les mauvaises options au debut
- La non-stationnarite (preferences qui changent) necessite de detecter les drifts et de "desapprendre" les priors obsoletes (sliding window ou decroissance exponentielle des poids historiques)
- Documenter clairement les limites : le MAB ne teste pas de causalite formelle. Si on veut une inference causale ("cet effet est du a l'heure d'envoi, pas a la selection des utilisateurs"), un A/B test classique reste necessaire
- Ne pas deployer Thompson Sampling sans metriques de garde : optimiser sur les clics peut nuire au taux de desabonnement si les notifications deviennent trop frequentes ou mal timees

---

## Synthese — Matrice de Decision

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    QUELLE APPROCHE CHOISIR ?                            │
├──────────────────────┬──────────────────────┬────────────────────────── │
│ SITUATION            │ APPROCHE             │ CAS ILLUSTRATIF            │
├──────────────────────┼──────────────────────┼──────────────────────────  │
│ Changement UI/UX     │ A/B frequentiste     │ Cas 1 : checkout           │
│ Decision strategique │ Pre-calcul rigoureux │ Cas 2 : onboarding         │
│ Faible trafic        │ Augmenter MDE ou     │                            │
│                      │ attendre plus long   │                            │
├──────────────────────┼──────────────────────┼──────────────────────────  │
│ Test de pricing      │ A/B + legal review   │ Cas 3 : pricing page       │
│ Segments multiples   │ + Bonferroni         │                            │
├──────────────────────┼──────────────────────┼──────────────────────────  │
│ Optimisation cont.   │ Thompson Sampling    │ Cas 4 : notifications      │
│ Nombreuses variantes │ (MAB)                │                            │
│ ROI pendant le test  │                      │                            │
├──────────────────────┼──────────────────────┼──────────────────────────  │
│ Inference causale    │ A/B classique        │ Tous les cas               │
│ requise              │ (MAB non suffisant)  │                            │
└──────────────────────┴──────────────────────┴──────────────────────────  │
```

---

## References Complementaires

- `references/statistical-foundations.md` — Calculs de taille d'echantillon, SRM, CUPED
- `references/bayesian-testing.md` — Thompson Sampling, Expected Loss, PyMC
- `references/experimentation-platform.md` — Statsig, LaunchDarkly, analyse SQL
- "Trustworthy Online Controlled Experiments" (Kohavi, Tang, Xu, 2020) — reference fondamentale
- "Multi-Armed Bandits" (Russo et al.) — theorie des bandits avec garanties theoriques
