# GARP Analysis

Référence approfondie sur la méthodologie Growth At a Reasonable Price (GARP) pour la sélection de sous-jacents de qualité en trading d'options.

---

## Table of Contents

1. [GARP Methodology Origins](#garp-methodology-origins)
2. [PEG Ratio : la Métrique Centrale](#peg-ratio--la-métrique-centrale)
3. [Revenue Growth & Earnings Quality](#revenue-growth--earnings-quality)
4. [Balance Sheet Analysis](#balance-sheet-analysis)
5. [Free Cash Flow Analysis](#free-cash-flow-analysis)
6. [Sector Positioning & Competitive Moat](#sector-positioning--competitive-moat)
7. [Margin of Safety](#margin-of-safety)
8. [Catalyst Identification](#catalyst-identification)
9. [GARP Screening Process](#garp-screening-process)
10. [Integration with Options Strategies](#integration-with-options-strategies)

---

## GARP Methodology Origins

### Peter Lynch : le Pionnier du GARP

Peter Lynch, gérant du fonds Magellan chez Fidelity (1977-1990), a produit un rendement annualisé de 29.2% sur 13 ans, battant le S&P 500 dans 11 de ces 13 années. Sa philosophie GARP constitue une synthèse entre l'investissement value (Benjamin Graham) et l'investissement growth (Philip Fisher).

**Principes fondamentaux de Lynch** :
- **"Invest in what you know"** : comprendre le business model avant d'investir. Si l'on ne peut pas expliquer pourquoi l'entreprise gagne de l'argent en deux phrases, ne pas investir.
- **Le PEG ratio** : Lynch a popularisé le ratio Price/Earnings-to-Growth comme métrique de valorisation ajustée à la croissance. Un PEG < 1 signale une action sous-évaluée relativement à sa croissance.
- **Classification des actions** : Lynch catégorise les actions en 6 types -- slow growers, stalwarts, fast growers, cyclicals, turnarounds, asset plays -- chacun exigeant une approche d'analyse différente.
- **Les "tenbaggers"** : Lynch recherchait les actions pouvant multiplier par 10, trouvées principalement parmi les fast growers avec un PEG attractif.

### Jim Slater : le PEG Ratio Systématisé

Jim Slater, investisseur et auteur britannique (*The Zulu Principle*, 1992), a systématisé l'approche GARP en un framework de screening quantifiable.

**Les critères de Slater** :
- PEG ratio < 1.0 (critère strict, souvent assoupli à < 1.5 dans la pratique).
- Croissance des bénéfices par action (EPS) > 15% annualisé.
- Taux de croissance accélérant (ou au minimum stable) sur les 3 derniers exercices.
- Cash flow opérationnel supérieur aux bénéfices reportés (qualité des earnings).
- Ratio dette/fonds propres raisonnable (< 50%).
- Avantage compétitif identifiable.
- Management avec un track record de création de valeur.

**Le "Zulu Principle"** : se concentrer sur un nombre restreint d'entreprises et les connaître en profondeur plutôt que de diversifier superficiellement. L'expertise sectorielle crée un avantage informationnel.

### GARP vs Value vs Growth

| Critère | Value (Graham/Buffett) | Growth (Fisher/T. Rowe Price) | GARP (Lynch/Slater) |
|---|---|---|---|
| Focus principal | Prix bas vs valeur intrinsèque | Croissance future des bénéfices | Croissance à prix raisonnable |
| Métrique clé | P/E, P/B, FCF yield | Revenue growth, TAM | PEG ratio |
| Risque principal | Value trap (pas de croissance) | Surpaiement de la croissance | Ralentissement de la croissance |
| Horizon | Long terme (3-5 ans) | Long terme (5-10 ans) | Moyen terme (1-3 ans) |
| Catalyseur | Revalorisation du marché | Maintien/accélération de la croissance | Croissance + compression du PEG |
| Applicable aux options | Oui (CSP sur les supports) | Oui (LEAPS) | Oui (Wheel, CSP, CC, spreads) |

---

## PEG Ratio : la Métrique Centrale

### Calcul et Variantes

```
PEG Ratio = (P/E Ratio) / (Taux de croissance des bénéfices annualisé)

Où :
  P/E = Prix de l'action / Bénéfice par action (EPS)
  Taux de croissance = croissance attendue de l'EPS (%)

Variantes :
  PEG Forward = P/E forward (estimations) / croissance EPS estimée prochains 12 mois
  PEG Trailing = P/E trailing / croissance EPS réalisée sur les 12 derniers mois
  PEG 3-year  = P/E forward / CAGR EPS estimé sur 3 ans
```

### Interprétation du PEG

| PEG Ratio | Interprétation | Action |
|---|---|---|
| < 0.5 | Très sous-valorisé vs croissance | Investiguer pourquoi (piège potentiel ou opportunité) |
| 0.5 - 1.0 | Sous-valorisé -- sweet spot GARP | Candidat idéal pour la Wheel / CSP |
| 1.0 - 1.5 | Valorisation raisonnable | Acceptable pour la Wheel si autres critères forts |
| 1.5 - 2.0 | Valorisation tendue | Prudence, uniquement si croissance très visible |
| > 2.0 | Surévalué vs croissance | Éviter pour les stratégies income |

### Limites du PEG

**Pièges à éviter** :
- **PEG négatif** : quand les bénéfices ou la croissance sont négatifs, le PEG est non significatif. Filtrer les entreprises non profitables avant d'appliquer le PEG.
- **Croissance non durable** : un PEG bas basé sur un pic de croissance cyclique (ex : post-COVID) peut être trompeur. Vérifier la durabilité de la croissance.
- **Qualité des bénéfices** : un PEG attractif basé sur des bénéfices gonflés (one-time items, comptabilité agressive) est un piège. Croiser avec le FCF.
- **Secteurs différents** : les PEG ne sont pas comparables entre secteurs. Les secteurs à forte intensité capitalistique (utilities, industrials) ont structurellement des PEG plus élevés que les secteurs asset-light (software, services).
- **Taux d'intérêt** : en environnement de taux élevés, les multiples de valorisation se compriment, ce qui peut rendre un PEG apparemment bas en fait surévalué par rapport aux alternatives sans risque.

---

## Revenue Growth & Earnings Quality

### Analyse de la Croissance des Revenus

Évaluer la croissance du chiffre d'affaires (revenue) sur plusieurs dimensions :

**Métriques clés** :

```
Revenue Growth YoY = (Revenue_t - Revenue_{t-1}) / Revenue_{t-1}

Revenue CAGR 3Y = (Revenue_t / Revenue_{t-3})^(1/3) - 1

Organic Growth = Revenue growth excluant acquisitions et effets de change
```

**Framework d'évaluation** :

| Critère | Excellent | Bon | Médiocre | Red flag |
|---|---|---|---|---|
| Revenue CAGR 3Y | > 20% | 10-20% | 5-10% | < 5% ou négatif |
| Accélération récente | YoY accélérant | YoY stable | YoY décélérant | Décélération forte |
| Croissance organique | > 80% de la croissance totale | 50-80% | < 50% | Croissance uniquement par acquisitions |
| Diversification revenus | Multi-produits, multi-géographies | Concentration modérée | Dépendance à 1-2 clients/produits | Un seul client > 25% du CA |

### Qualité des Bénéfices (Earnings Quality)

Les bénéfices reportés (GAAP earnings) ne sont pas toujours un reflet fidèle de la performance économique réelle. Évaluer la qualité des earnings avec ces filtres :

**Accruals Quality** :

```
Accruals Ratio = (Net Income - Operating Cash Flow) / Total Assets

Interprétation :
  Ratio > 0 (élevé) : bénéfices "papier" non soutenus par du cash → méfiance
  Ratio ≈ 0 : bonne conversion des bénéfices en cash → qualité élevée
  Ratio < 0 : cash flow supérieur aux bénéfices → qualité très élevée
```

**Marge opérationnelle** :

```
Operating Margin = Operating Income / Revenue

Évaluer :
  - Le niveau absolu (comparé au secteur)
  - La tendance (stable, en expansion, en contraction)
  - La résistance en période de ralentissement économique
```

| Tendance de marge | Signal | Implication pour les options |
|---|---|---|
| En expansion régulière | Pouvoir de pricing, efficacité | Sous-jacent idéal pour la Wheel |
| Stable | Business mature, prévisible | Bon pour les stratégies income |
| En contraction | Pression concurrentielle, coûts | Prudence, éviter pour les CSP |
| Volatile | Cyclique ou compétitif | Risque élevé, pas de Wheel |

### Earnings Surprises et Momentum

Suivre le pattern des earnings surprises :
- **4+ trimestres consécutifs de beats** (EPS > consensus) : momentum positif, les analystes sous-estiment systématiquement.
- **Révisions à la hausse** : les analystes augmentent leurs estimations de bénéfices futurs -- signal très positif.
- **Post-Earnings Announcement Drift (PEAD)** : les actions qui battent les estimations tendent à surperformer dans les 60 jours suivants. Phénomène exploitable pour le timing des options.

---

## Balance Sheet Analysis

### Solidité Financière

Évaluer la capacité de l'entreprise à résister aux chocs et à maintenir sa croissance :

**Ratios d'endettement** :

```
Net Debt / EBITDA = (Total Debt - Cash) / EBITDA

Seuils GARP :
  < 1.0x : Excellent (bilan fortress)
  1.0-2.5x : Acceptable
  2.5-4.0x : Élevé (prudence, vérifier la stabilité du cash flow)
  > 4.0x : Red flag (risque de crédit, éviter pour la Wheel)
```

**Ratios de liquidité** :

```
Current Ratio = Current Assets / Current Liabilities
  Seuil minimum : 1.5x (capacité de faire face aux obligations court terme)

Quick Ratio = (Cash + Receivables + Short-term Investments) / Current Liabilities
  Seuil minimum : 1.0x

Interest Coverage = EBIT / Interest Expense
  Seuil minimum : 5.0x (capacité de servir la dette confortablement)
```

**Analyse du bilan -- checklist** :

| Élément | Ce qu'il faut vérifier | Red flag |
|---|---|---|
| Goodwill / Intangibles | Proportion par rapport aux actifs totaux | > 50% des actifs totaux |
| Inventaires | Rotation des stocks (Days Inventory Outstanding) | Augmentation significative du DIO |
| Créances clients | DSO (Days Sales Outstanding) | DSO en augmentation vs croissance du CA |
| Dette à court terme | Proportion de la dette totale due dans < 1 an | > 30% de la dette totale |
| Off-balance sheet | Leases opérationnels, guarantees, SPVs | Engagement hors bilan significatifs non provisionnés |

### Altman Z-Score (Risque de Faillite)

Pour les entreprises industrielles cotées, le Z-Score d'Altman évalue le risque de faillite :

```
Z = 1.2*A + 1.4*B + 3.3*C + 0.6*D + 1.0*E

Où :
  A = Working Capital / Total Assets
  B = Retained Earnings / Total Assets
  C = EBIT / Total Assets
  D = Market Cap / Total Liabilities
  E = Revenue / Total Assets

Interprétation :
  Z > 2.99 : Zone sûre (faible probabilité de faillite)
  1.81 < Z < 2.99 : Zone grise (risque modéré)
  Z < 1.81 : Zone de détresse (risque élevé)
```

**Application aux options** : ne jamais vendre des cash-secured puts ou exécuter la Wheel sur des entreprises en zone grise ou de détresse. Le risque d'assignation avec une perte permanente de capital est inacceptable.

---

## Free Cash Flow Analysis

### FCF : la Métrique Ultime de Qualité

Le Free Cash Flow est le cash généré par l'activité opérationnelle après les investissements nécessaires au maintien et à la croissance de l'activité. C'est la mesure la plus fiable de la capacité bénéficiaire réelle.

```
FCF = Operating Cash Flow - Capital Expenditures

FCF Margin = FCF / Revenue

FCF Yield = FCF per share / Stock Price   (ou FCF / Enterprise Value)

FCF Conversion = FCF / Net Income
  > 100% : excellent (le cash flow excède les bénéfices GAAP)
  80-100% : bon
  < 80% : qualité des bénéfices à investiguer
```

### FCF Growth et Durabilité

```
FCF CAGR 3Y = (FCF_t / FCF_{t-3})^(1/3) - 1

Évaluer la croissance du FCF par rapport à la croissance des revenus :
  FCF growth > Revenue growth : amélioration de la rentabilité et de l'efficacité
  FCF growth ≈ Revenue growth : profil de marge stable
  FCF growth < Revenue growth : investissements en hausse ou marges sous pression
```

### FCF Yield comme Alternative au P/E

Le FCF Yield est souvent plus pertinent que le P/E ratio pour évaluer la valorisation, car il n'est pas affecté par les choix comptables (amortissement, dépréciation, stock-based compensation).

```
FCF Yield = FCF per share / Stock Price

Comparaison :
  FCF Yield > Bond Yield (taux 10Y) + Equity Risk Premium : valorisation attractive
  FCF Yield < Bond Yield : valorisation tendue, le cash généré ne compense pas le risque
```

| FCF Yield | Interprétation | Application options |
|---|---|---|
| > 8% | Très attractif (sous-valorisé ou risqué) | Candidat Wheel si fondamentaux solides |
| 5-8% | Attractif | Sweet spot pour les CSP et Wheel |
| 3-5% | Raisonnable (growth justifie la valorisation) | Acceptable si PEG < 1.5 |
| < 3% | Cher (croissance exceptionnelle requise) | Éviter pour les stratégies income |

### Utilisation du FCF (Capital Allocation)

Évaluer comment le management alloue le FCF :

| Allocation | Signal positif | Signal négatif |
|---|---|---|
| Buyback (rachats d'actions) | À des valorisations attractives (PEG < 1.5) | À des prix élevés (destruction de valeur) |
| Dividendes | Payout ratio < 60%, croissance régulière | Payout ratio > 80%, endettement pour dividende |
| R&D / Capex de croissance | Investissement dans l'avantage compétitif | Capex non productif, diversification non-core |
| Réduction de dette | Quand le levier est élevé | Non nécessaire si bilan solide |
| Acquisitions | Bolt-on à prix raisonnable, synergies claires | Grosses acquisitions transformantes, surpaiement |

---

## Sector Positioning & Competitive Moat

### Avantage Compétitif (Economic Moat)

Identifier et évaluer le moat de l'entreprise selon le framework de Morningstar :

**Types de moat** :

| Type de moat | Description | Exemples | Durabilité |
|---|---|---|---|
| Network effects | La valeur augmente avec le nombre d'utilisateurs | Visa, Meta, marketplaces | Très élevée |
| Switching costs | Coût élevé pour le client de changer de fournisseur | SAP, Adobe, banques | Élevée |
| Cost advantage | Avantage structurel de coût (échelle, process, localisation) | Walmart, TSMC | Modérée à élevée |
| Intangible assets | Brevets, marques, licences réglementaires | Pfizer, Disney, Moody's | Variable |
| Efficient scale | Marché de taille limitée ne supportant qu'un petit nombre d'acteurs | Utilities, rail, pipelines | Élevée |

### Analyse Sectorielle

Positionner l'entreprise dans la dynamique sectorielle :

**Porter's Five Forces** (évaluation rapide) :
1. **Rivalité concurrentielle** : nombre de concurrents, différenciation, barrières de sortie.
2. **Pouvoir de négociation des fournisseurs** : concentration, dépendance, substituabilité.
3. **Pouvoir de négociation des clients** : concentration, sensibilité au prix, alternatives.
4. **Menace de nouveaux entrants** : barrières à l'entrée (capital, réglementation, technologie).
5. **Menace de substituts** : solutions alternatives résolvant le même problème.

**Positionnement dans le cycle sectoriel** :

| Phase | Caractéristique | Implication options |
|---|---|---|
| Early growth | Forte croissance, marges en expansion | LEAPS calls, long-dated CSP |
| Maturation | Croissance modérée, marges stables | Wheel strategy idéale |
| Decline | Croissance nulle ou négative, pression sur les marges | Éviter pour les stratégies income |
| Cyclique - expansion | Forte croissance temporaire, marges au-dessus de la moyenne | CSP prudents, durée courte |
| Cyclique - contraction | Décélération, marges sous pression | Éviter ou stratégies de protection |

---

## Margin of Safety

### Concept et Application

La marge de sécurité (margin of safety), concept central de Benjamin Graham, représente la différence entre la valeur intrinsèque estimée et le prix de marché. En GARP, la marge de sécurité est ajustée pour la croissance.

```
Margin of Safety = (Valeur intrinsèque estimée - Prix de marché) / Valeur intrinsèque

Seuil minimum : 20-30% pour les actions de qualité (GARP)
Seuil pour les situations plus risquées : 40-50%
```

### Estimation de la Valeur Intrinsèque (Simplified DCF)

```
Valeur intrinsèque = FCF_1 / (WACC - g)   (modèle de Gordon simplifié)

Où :
  FCF_1  = Free Cash Flow attendu la première année
  WACC   = Weighted Average Cost of Capital (typiquement 8-12%)
  g      = taux de croissance perpétuelle du FCF (typiquement 2-4%)

Variante à deux étapes :
  Phase 1 (5-10 ans) : croissance élevée (taux GARP, ex: 15%)
  Phase 2 (perpétuité) : croissance de maturité (2-4%)

  VI = SUM[FCF_t / (1+WACC)^t] + Terminal Value / (1+WACC)^n
  Terminal Value = FCF_n * (1+g) / (WACC - g)
```

### Application aux Options : le Strike comme Margin of Safety

Dans le contexte de la Wheel Strategy, le strike du cash-secured put constitue une marge de sécurité intégrée :

```
Marge effective = 1 - (Strike - Premium reçu) / Prix actuel

Exemple :
  Action à 100$, CSP au strike 90$ pour 2.50$ de premium
  Coût de base effectif si assigné = 90 - 2.50 = 87.50$
  Marge de sécurité = 1 - 87.50/100 = 12.5%

  Si la valeur intrinsèque estimée est 110$ :
  Marge de sécurité totale = 1 - 87.50/110 = 20.5% ← acceptable
```

---

## Catalyst Identification

### Types de Catalyseurs

Identifier les événements pouvant déclencher une réévaluation du cours :

**Catalyseurs fondamentaux** :
- **Lancement de nouveau produit** : expansion du TAM (Total Addressable Market), accélération de la croissance.
- **Expansion géographique** : entrée sur un nouveau marché significatif.
- **Amélioration des marges** : restructuration, économies d'échelle, mix favorable.
- **Programme de rachat d'actions** : soutien du cours, accroissement du BPA.
- **Déleveraging** : réduction de l'endettement, amélioration du profil de risque.
- **Acquisition transformante** : consolidation sectorielle, synergies.
- **Spin-off** : libération de valeur d'une division sous-évaluée.

**Catalyseurs de marché** :
- **Inclusion dans un indice** (S&P 500, MSCI) : flux d'achat passif.
- **Couverture analytique** : initiation de couverture par un broker majeur.
- **Upgrade sectoriel** : rotation sectorielle favorable.
- **Changement réglementaire** : nouvelle réglementation favorisant l'entreprise.

**Catalyseurs techniques** :
- **Breakout technique** : sortie d'une zone de consolidation avec volume.
- **Golden cross** : croisement de la MM50 au-dessus de la MM200.
- **Short squeeze potentiel** : short interest élevé (> 20% du float) + catalyseur positif.

### Timeline des Catalyseurs

Aligner l'expiration des options avec l'horizon du catalyseur :

| Horizon du catalyseur | Stratégie options adaptée |
|---|---|
| < 30 jours | CSP ou debit spreads à court terme |
| 1-3 mois | Vertical spreads, calendars |
| 3-12 mois | LEAPS, diagonales |
| > 12 mois | LEAPS, accumulation via Wheel |

---

## GARP Screening Process

### Étape par Étape

Appliquer ce processus de screening systématique :

```
ÉTAPE 1 : Filtre quantitatif initial (univers large → 50-100 candidats)
  ☐ PEG Forward < 1.5
  ☐ Revenue growth YoY > 10%
  ☐ EPS growth > 12% (estimé prochains 12 mois)
  ☐ FCF positif (trailing 12 mois)
  ☐ Market cap > 2 milliards $ (liquidité options)
  ☐ Options avec bid-ask spread < 5% du mid-price (ATM)

ÉTAPE 2 : Filtre qualité (50-100 → 20-30 candidats)
  ☐ FCF/Net Income > 80%
  ☐ Operating margin stable ou en expansion (3 ans)
  ☐ Net Debt/EBITDA < 2.5x
  ☐ Current ratio > 1.5x
  ☐ Interest coverage > 5.0x
  ☐ Altman Z-Score > 2.99
  ☐ Au moins 2 trimestres consécutifs de beats EPS

ÉTAPE 3 : Analyse qualitative (20-30 → 10-15 candidats)
  ☐ Moat identifiable et durable
  ☐ Management avec track record d'allocation de capital efficace
  ☐ Positionnement dans un secteur en croissance structurelle
  ☐ Au moins un catalyseur identifiable sur 6-12 mois
  ☐ Pas de risque réglementaire ou technologique majeur imminent

ÉTAPE 4 : Filtre options et timing (10-15 → 5-8 positions actives)
  ☐ IV Rank > 30% (premium suffisant pour la Wheel/CSP)
  ☐ Pas d'earnings dans les 30 prochains jours
  ☐ Niveaux techniques favorables (support identifiable pour le placement du strike)
  ☐ Put/Call ratio et options flow cohérents avec la thèse
  ☐ Diversification sectorielle du portefeuille maintenue
```

---

## Integration with Options Strategies

### GARP + Wheel Strategy

La combinaison GARP + Wheel est la plus naturelle et la plus robuste :
- GARP identifie les entreprises que l'on **accepte de détenir** à long terme.
- Le CSP au strike correspondant à la valorisation GARP attractive crée une **marge de sécurité**.
- Le covered call génère un revenu pendant la détention.
- Les fondamentaux GARP fournissent une **ancre de conviction** pour maintenir la position pendant les drawdowns temporaires.

### GARP + LEAPS

Pour les entreprises GARP avec un PEG < 0.8 et des catalyseurs à 6-12 mois :
- Acheter un LEAPS call deep ITM (delta 0.80+) comme substitut d'action.
- Le LEAPS bénéficie de l'expansion multiple (compression du PEG via la croissance des bénéfices) et de l'appréciation du cours.
- Coût en capital réduit par rapport à l'achat d'actions, levier contrôlé.

### GARP + Directional Spreads

Pour exprimer une conviction directionnelle sur une action GARP après un pullback :
- Bull call spread si IV Rank < 30% (acheter du premium bon marché).
- Bull put spread si IV Rank > 50% (vendre du premium cher).
- Aligner le strike inférieur avec un support technique et le strike supérieur avec un objectif de cours basé sur la valorisation GARP.

---

## Summary Checklist

### Screening GARP complet :

- [ ] PEG ratio < 1.5 (forward, vérifié sur au moins 2 sources)
- [ ] Revenue growth > 10% CAGR 3Y
- [ ] EPS growth > 12% estimé
- [ ] FCF positif et FCF/Net Income > 80%
- [ ] Operating margin stable ou en expansion
- [ ] Net Debt/EBITDA < 2.5x, Current ratio > 1.5x
- [ ] Altman Z-Score > 2.99
- [ ] Moat identifiable (network effects, switching costs, etc.)
- [ ] Au moins un catalyseur identifiable (6-12 mois)
- [ ] Management avec bonne allocation de capital
- [ ] Valorisation avec marge de sécurité > 20%
- [ ] Options liquides (bid-ask, volume, OI)
- [ ] Pas de concentration sectorielle excessive dans le portefeuille
