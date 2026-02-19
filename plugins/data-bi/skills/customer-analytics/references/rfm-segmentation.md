# Segmentation RFM — Recence, Frequence, Valeur Monetaire

## Definition et Logique Business

La segmentation RFM est une methode d'analyse comportementale qui classe les clients selon trois dimensions issues de leur historique d'achat :

- **Recence (R)** : combien de jours se sont ecoules depuis la derniere commande. Un client qui a achete recemment est plus susceptible de repondre a une sollicitation marketing.
- **Frequence (F)** : combien de commandes le client a passe sur une periode donnee (typiquement 12 mois). La frequence mesure la fidelite comportementale.
- **Valeur Monetaire (M)** : le chiffre d'affaires total genere par le client sur la periode. Permet d'identifier les clients a forte valeur independamment de leur frequence.

La logique business est simple : les clients qui ont achete recemment, souvent et pour des montants eleves ont la plus forte probabilite de repondre positivement aux prochaines actions marketing. L'objectif est de traiter differemment des clients fondamentalement differents, plutot que d'envoyer le meme message a toute la base.

**Pourquoi le RFM fonctionne :** il repose sur des comportements observes, pas sur des intentions declarees. Il est calculable depuis n'importe quelle base de transactions. Il est actionnable immediatement : chaque segment correspond a une action CRM specifique.

---

## Calcul RFM Complet en SQL (PostgreSQL / BigQuery Compatible)

### Etape 1 — Calcul de la Recence

```sql
-- Date de reference : aujourd'hui ou date de snapshot
WITH reference_date AS (
  SELECT DATE('2024-01-01') AS ref_date
),

-- Derniere commande par client
last_order AS (
  SELECT
    customer_id,
    MAX(order_date) AS last_order_date
  FROM orders
  WHERE order_status NOT IN ('cancelled', 'refunded')
  GROUP BY customer_id
),

-- Recence en jours
recency_calc AS (
  SELECT
    l.customer_id,
    l.last_order_date,
    DATE_DIFF(r.ref_date, l.last_order_date, DAY) AS recency_days
  FROM last_order l
  CROSS JOIN reference_date r
)

SELECT * FROM recency_calc;
```

### Etape 2 — Calcul de la Frequence

```sql
-- Frequence : nombre de commandes sur les 12 derniers mois
frequency_calc AS (
  SELECT
    customer_id,
    COUNT(DISTINCT order_id) AS order_count
  FROM orders
  WHERE
    order_status NOT IN ('cancelled', 'refunded')
    AND order_date >= DATE_SUB(DATE('2024-01-01'), INTERVAL 12 MONTH)
  GROUP BY customer_id
)
```

### Etape 3 — Calcul de la Valeur Monetaire

```sql
-- Valeur monetaire : CA total net sur 12 mois
monetary_calc AS (
  SELECT
    customer_id,
    SUM(order_amount_net) AS total_revenue
  FROM orders
  WHERE
    order_status NOT IN ('cancelled', 'refunded')
    AND order_date >= DATE_SUB(DATE('2024-01-01'), INTERVAL 12 MONTH)
  GROUP BY customer_id
)
```

### Etape 4 — Scoring 1-5 par Quintile avec NTILE()

```sql
-- Assemblage et scoring RFM
rfm_raw AS (
  SELECT
    rc.customer_id,
    rc.recency_days,
    COALESCE(fc.order_count, 0)     AS frequency,
    COALESCE(mc.total_revenue, 0)   AS monetary
  FROM recency_calc rc
  LEFT JOIN frequency_calc fc USING (customer_id)
  LEFT JOIN monetary_calc  mc USING (customer_id)
),

rfm_scored AS (
  SELECT
    customer_id,
    recency_days,
    frequency,
    monetary,
    -- Recence : score inverse (moins de jours = meilleur score)
    NTILE(5) OVER (ORDER BY recency_days DESC) AS r_score,
    -- Frequence : score direct (plus de commandes = meilleur score)
    NTILE(5) OVER (ORDER BY frequency ASC)     AS f_score,
    -- Monetaire : score direct (plus de CA = meilleur score)
    NTILE(5) OVER (ORDER BY monetary ASC)      AS m_score
  FROM rfm_raw
  WHERE monetary > 0  -- Exclure les clients sans achat sur la periode
)
```

### Etape 5 — Score RFM Composite et Segments

```sql
rfm_final AS (
  SELECT
    customer_id,
    recency_days,
    frequency,
    monetary,
    r_score,
    f_score,
    m_score,
    -- Score composite : concatenation RFM (ex: "5-4-3")
    CONCAT(r_score, '-', f_score, '-', m_score) AS rfm_code,
    -- Score numerique pour tri (pondere : R x 0.4, F x 0.35, M x 0.25)
    ROUND(r_score * 0.4 + f_score * 0.35 + m_score * 0.25, 2) AS rfm_score,
    -- Segmentation par regles metier
    CASE
      WHEN r_score >= 5 AND f_score >= 4 AND m_score >= 4 THEN 'Champions'
      WHEN r_score >= 4 AND f_score >= 4 AND m_score >= 3 THEN 'Loyal Customers'
      WHEN r_score >= 4 AND f_score <= 2 AND m_score >= 3 THEN 'Potential Loyalists'
      WHEN r_score >= 4 AND f_score <= 1                  THEN 'New Customers'
      WHEN r_score BETWEEN 3 AND 4 AND f_score <= 2      THEN 'Promising'
      WHEN r_score BETWEEN 3 AND 4 AND f_score BETWEEN 3 AND 4 THEN 'Need Attention'
      WHEN r_score BETWEEN 2 AND 3 AND f_score >= 3      THEN 'At Risk'
      WHEN r_score BETWEEN 2 AND 3 AND f_score BETWEEN 1 AND 2 THEN 'About to Sleep'
      WHEN r_score <= 2 AND f_score >= 4 AND m_score >= 4 THEN "Can't Lose Them"
      WHEN r_score <= 2 AND f_score BETWEEN 2 AND 3      THEN 'Hibernating'
      ELSE 'Lost'
    END AS rfm_segment
  FROM rfm_scored
)

SELECT * FROM rfm_final
ORDER BY rfm_score DESC;
```

---

## Les 11 Segments RFM Classiques

### Champions (R:5, F:4-5, M:4-5)
**Profil :** acheteurs recents, frequents, fort CA. Les meilleurs clients de la base.
**Taille typique :** 5-10% de la base, 30-40% du CA.
**Actions CRM :**
- Progamme VIP exclusif (acces avant-vente, invitation evenements)
- Demander des avis et temoignages
- Programme ambassadeur / referral
- Ne pas surexposer aux promotions — ils achetent deja au plein prix

### Loyal Customers (R:3-5, F:3-5, M:3-5)
**Profil :** acheteurs reguliers et fideles, pas forcement les plus recents.
**Taille typique :** 10-15% de la base, 20-30% du CA.
**Actions CRM :**
- Programme de fidelite avec points / avantages progressifs
- Vente croisee (cross-sell) sur categories adjacentes
- Communication privilegiee (newsletter premium)
- Offres anniversaire et personnalisation poussee

### Potential Loyalists (R:4-5, F:1-2, M:3-5)
**Profil :** clients recents avec un ou deux achats de valeur. Potentiel fort a confirmer.
**Taille typique :** 8-12%.
**Actions CRM :**
- Onboarding renforce apres premier achat
- Programme de fidelite avec incentive a rejoindre
- Recommandations personnalisees basees sur le premier achat
- Email de nurturing : contenu educatif, guide d'utilisation produit

### New Customers (R:4-5, F:1, M:variable)
**Profil :** acheteurs tres recents, premiere commande seulement.
**Taille typique :** 5-8%.
**Actions CRM :**
- Sequence de bienvenue (5-7 emails sur 30 jours)
- Premier achat : encourage la decouverte du catalogue complet
- Offre de deuxieme achat avec deadline (urgence)
- Collecte de preference pour personnalisation future

### Promising (R:3-4, F:1-2, M:1-2)
**Profil :** clients recents mais peu engages, faible valeur monetaire pour l'instant.
**Taille typique :** 8-12%.
**Actions CRM :**
- Email de re-engagement avec offre de decouverte
- Mise en avant des best-sellers et produits tendance
- Programme parrainage pour ajouter de la valeur perçue

### Need Attention (R:3-4, F:3-4, M:3-4)
**Profil :** clients reguliers mais dont la recence commence a baisser. Signal d'alerte precoce.
**Taille typique :** 10-15%.
**Actions CRM :**
- Offres personnalisees basees sur l'historique d'achat
- Enquete satisfaction rapide (NPS ou CSAT)
- Reactiver via canal prefere (email, SMS, push selon historique)

### At Risk (R:2-3, F:3-5, M:3-5)
**Profil :** anciens bons clients qui n'ont pas achete depuis plusieurs mois. Priorite de retention.
**Taille typique :** 8-12%.
**Actions CRM :**
- Campagne de retention urgente : "Vous nous manquez"
- Offre de win-back avec remise significative (15-25%)
- Appel telephonique pour les plus gros comptes
- Comprendre le motif de l'arret (enquete courte)

### About to Sleep (R:2-3, F:1-2, M:variable)
**Profil :** clients sporadiques qui s'eloignent progressivement.
**Taille typique :** 8-10%.
**Actions CRM :**
- Campagne de re-engagement avec nouvelle offre
- Mise en avant des nouveautes depuis leur dernier achat
- Si pas de reaction : diminuer la pression marketing pour eviter la desinscription

### Can't Lose Them (R:1-2, F:4-5, M:4-5)
**Profil :** anciens tres bons clients inactifs depuis longtemps. Valeur historique elevee.
**Taille typique :** 2-5%, mais CA potentiel tres eleve.
**Actions CRM :**
- Contact direct et personnalise (appel, email VIP one-to-one)
- Offre de win-back premium, sans aspect generique
- Proposition de feedback : pourquoi ont-ils arrete ?
- Investir jusqu'a 2-3x le CAC initial pour les recuperer

### Hibernating (R:1-2, F:2-3, M:1-3)
**Profil :** clients inactifs, valeur moderee. Effort de recuperation marginal.
**Taille typique :** 10-15%.
**Actions CRM :**
- Email de re-engagement automatise (faible cout)
- Si pas de reaction sur 2 campagnes : retirer de la pression marketing active
- Conserver dans la base pour les grandes occasions (soldes, Black Friday)

### Lost (R:1, F:1, M:1)
**Profil :** clients totalement inactifs et a faible valeur historique.
**Taille typique :** 10-20% de la base.
**Actions CRM :**
- Ne pas investir de budget marketing significatif
- Email de desabonnement propre si inactif email depuis 12+ mois (RGPD)
- Analyser pour comprendre les patterns de churn evitable

---

## Implementation Python avec Pandas

```python
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from datetime import datetime, timedelta

# --- Chargement des donnees ---
df = pd.read_csv('transactions.csv', parse_dates=['order_date'])
df = df[df['order_status'].isin(['completed', 'shipped'])]

# --- Date de reference ---
reference_date = df['order_date'].max() + timedelta(days=1)

# --- Calcul RFM ---
rfm = df.groupby('customer_id').agg(
    recency_days   = ('order_date',   lambda x: (reference_date - x.max()).days),
    frequency      = ('order_id',     'nunique'),
    monetary       = ('order_amount', 'sum')
).reset_index()

# --- Scoring 1-5 par quintile ---
rfm['r_score'] = pd.qcut(rfm['recency_days'], q=5, labels=[5, 4, 3, 2, 1]).astype(int)
rfm['f_score'] = pd.qcut(rfm['frequency'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5]).astype(int)
rfm['m_score'] = pd.qcut(rfm['monetary'].rank(method='first'), q=5, labels=[1, 2, 3, 4, 5]).astype(int)

# --- Score composite pondere ---
rfm['rfm_score'] = (rfm['r_score'] * 0.4 +
                    rfm['f_score'] * 0.35 +
                    rfm['m_score'] * 0.25).round(2)

# --- Segmentation ---
def assign_segment(row):
    r, f, m = row['r_score'], row['f_score'], row['m_score']
    if r >= 5 and f >= 4 and m >= 4:      return 'Champions'
    elif r >= 4 and f >= 4 and m >= 3:    return 'Loyal Customers'
    elif r >= 4 and f <= 2 and m >= 3:    return 'Potential Loyalists'
    elif r >= 4 and f <= 1:               return 'New Customers'
    elif r >= 3 and f <= 2:               return 'Promising'
    elif r >= 3 and f >= 3:               return 'Need Attention'
    elif r >= 2 and f >= 3:               return 'At Risk'
    elif r >= 2 and f <= 2:               return 'About to Sleep'
    elif r <= 2 and f >= 4 and m >= 4:    return "Can't Lose Them"
    elif r <= 2 and f >= 2:               return 'Hibernating'
    else:                                  return 'Lost'

rfm['segment'] = rfm.apply(assign_segment, axis=1)

# --- Rapport par segment ---
segment_summary = rfm.groupby('segment').agg(
    nb_clients     = ('customer_id', 'count'),
    revenue_total  = ('monetary',    'sum'),
    recence_moy    = ('recency_days', 'mean'),
    frequence_moy  = ('frequency',   'mean')
).sort_values('revenue_total', ascending=False)

print(segment_summary.round(1))
```

### Visualisation Radar Chart par Segment

```python
from matplotlib.patches import FancyArrowPatch
import matplotlib.pyplot as plt
import numpy as np

def radar_chart(rfm, segments_to_plot=None):
    if segments_to_plot is None:
        segments_to_plot = ['Champions', 'Loyal Customers', 'At Risk', 'Hibernating']

    categories = ['Recence', 'Frequence', 'Monetaire']
    N = len(categories)
    angles = [n / float(N) * 2 * np.pi for n in range(N)]
    angles += angles[:1]

    fig, ax = plt.subplots(figsize=(8, 8), subplot_kw=dict(polar=True))

    for segment in segments_to_plot:
        seg_data = rfm[rfm['segment'] == segment]
        values = [
            seg_data['r_score'].mean(),
            seg_data['f_score'].mean(),
            seg_data['m_score'].mean()
        ]
        values += values[:1]
        ax.plot(angles, values, linewidth=2, linestyle='solid', label=segment)
        ax.fill(angles, values, alpha=0.1)

    ax.set_xticks(angles[:-1])
    ax.set_xticklabels(categories, size=12)
    ax.set_ylim(0, 5)
    ax.set_title('Profil RFM par Segment', size=16, pad=20)
    ax.legend(loc='upper right', bbox_to_anchor=(1.3, 1.1))
    plt.tight_layout()
    plt.savefig('rfm_radar.png', dpi=150)
    plt.show()

radar_chart(rfm)
```

---

## Adaptation RFM pour le SaaS

Dans un contexte SaaS, il n'y a pas de "commande" au sens e-commerce. Adapter les trois dimensions :

| Dimension | E-commerce | SaaS B2B | SaaS B2C |
|-----------|-----------|----------|----------|
| Recence | Jours depuis derniere commande | Jours depuis derniere connexion | Jours depuis derniere session |
| Frequence | Nombre de commandes / 12 mois | Nombre de logins / 30 jours | Sessions actives / 30 jours |
| Monetaire | CA total net | MRR ou ARR | Revenue mensuel / plan |

```sql
-- Exemple SaaS : RFM sur base d'usage produit
WITH saas_rfm AS (
  SELECT
    account_id,
    -- Recence : jours depuis derniere connexion
    DATE_DIFF(CURRENT_DATE(), MAX(session_date), DAY) AS recency_days,
    -- Frequence : sessions actives sur 30 jours
    COUNT(DISTINCT session_date)                       AS monthly_logins,
    -- Monetaire : MRR du compte
    MAX(mrr_usd)                                       AS mrr
  FROM product_sessions
  WHERE session_date >= DATE_SUB(CURRENT_DATE(), INTERVAL 30 DAY)
  GROUP BY account_id
)
SELECT
  account_id,
  recency_days,
  monthly_logins,
  mrr,
  NTILE(5) OVER (ORDER BY recency_days DESC)     AS r_score,
  NTILE(5) OVER (ORDER BY monthly_logins ASC)    AS f_score,
  NTILE(5) OVER (ORDER BY mrr ASC)               AS m_score
FROM saas_rfm;
```

---

## Limites du RFM et Solutions

**Limite 1 — Ne capture pas la valeur future.** Un client Champion peut avoir atteint son pic d'achat. Combiner avec le CLV predictif pour identifier les clients a potentiel croissant.

**Limite 2 — Biais temporel.** Un client saisonnier (achat uniquement en decembre) sera penalise par sa recence en juillet. Adapter la periode de reference ou utiliser des fenetres glissantes.

**Limite 3 — Insensible aux changements de comportement recents.** Un client qui passe de 10 commandes/an a 2 peut rester dans "Loyal Customers" plusieurs mois. Implementer une detection de variation (delta RFM).

**Limite 4 — Absence de contexte produit.** Deux clients avec le meme score RFM peuvent avoir des comportements d'achat totalement differents (categorie, recurrence, saisonnalite). Completer avec une segmentation par categorie.

**Solution recommandee :** utiliser le RFM comme base de segmentation, et enrichir avec :
- CLV predictif (modele BG/NBD) pour la valeur future
- Segmentation produit pour la personalisation du contenu
- Score de propension pour actions specifiques (cross-sell, upgrade)

---

## Benchmarks Distribution Typique — E-commerce

| Segment | % Base clients | % CA total | Recence moy. | Freq. moy. |
|---------|---------------|-----------|--------------|------------|
| Champions | 5-10% | 30-40% | 15 j | 8.2 cmd |
| Loyal Customers | 10-15% | 20-30% | 35 j | 5.1 cmd |
| Potential Loyalists | 8-12% | 8-12% | 20 j | 1.8 cmd |
| New Customers | 5-8% | 3-6% | 12 j | 1.0 cmd |
| At Risk | 8-12% | 8-15% | 120 j | 4.3 cmd |
| Hibernating | 10-15% | 4-8% | 280 j | 2.1 cmd |
| Lost | 10-20% | 2-5% | 400+ j | 1.2 cmd |

Recalculer la segmentation au minimum mensuellement. Un client ne reste pas dans le meme segment indefiniment : la migration de segment est l'indicateur cle de sante du programme CRM.
