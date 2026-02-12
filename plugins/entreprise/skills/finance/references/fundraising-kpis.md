# Fundraising & KPIs — Levees de Fonds, Relations Investisseurs, Unit Economics & Metriques SaaS

## Overview

Ce document de reference couvre le processus de levee de fonds (du pre-seed a l'IPO), les relations investisseurs, l'analyse financiere par les ratios, les unit economics (CAC, LTV, payback) et les metriques SaaS (MRR, ARR, NDR, churn). Utiliser ce guide comme fondation pour structurer une strategie de financement, communiquer avec les investisseurs et piloter la performance par les metriques cles.

---

## Fundraising — Processus et Structuration

### Typologie des Financements

| Source | Stade | Montant typique | Dilution | Avantages | Inconvenients |
|---|---|---|---|---|---|
| **Love money** | Pre-seed | 10-100K EUR | Variable | Rapidite, souplesse | Montants limites, risque relationnel |
| **Business Angels (BA)** | Pre-seed / Seed | 50-500K EUR | 10-25% | Smart money, reseau, rapidite | Montants limites, gouvernance legere |
| **Venture Capital (VC)** | Seed a Serie C+ | 500K-100M+ EUR | 15-30% par tour | Montants importants, accompagnement, credibilite | Dilution, pression de sortie, reporting |
| **Corporate Venture (CVC)** | Serie A+ | 1-20M EUR | 5-15% | Acces marche, synergies industrielles | Risque de conflit d'interet, lenteur |
| **Growth Equity / PE** | Serie C+ | 20-200M+ EUR | 10-30% | Expertise operationnelle, moins dilutif que VC | Exigences de gouvernance, focus rentabilite |
| **Dette (venture debt)** | Post-Seed / Post-Serie A | 1-10M EUR | 0% (+ warrants 0.5-2%) | Non dilutif, complement de la levee | Remboursement obligatoire, covenants |
| **Subventions / aides publiques** | Tous stades | Variable | 0% | Non dilutif, gratuit | Processus long, contraintes administratives, remboursement conditionnel (avances) |
| **Revenue-Based Financing (RBF)** | Post-revenue | 100K-5M EUR | 0% | Non dilutif, rembourse sur le CA | Cout effectif 15-25%, pas adapte aux modeles a marge faible |
| **IPO** | Maturite | Variable | 10-25% (flottant) | Liquidite, notoriete, monnaie d'echange (M&A) | Couts eleves, obligations reglementaires, pression trimestrielle |

### Processus de Levee de Fonds — Timeline

```
Phase 1 — Preparation (2-3 mois avant le lancement)
  |-- Structurer le data room (financiers, juridique, IP, metriques)
  |-- Construire le modele financier integre (P&L, bilan, cash flow, 3-5 ans)
  |-- Preparer le pitch deck (15-20 slides)
  |-- Definir la thèse d'investissement (pourquoi maintenant, pourquoi nous)
  |-- Identifier 30-50 investisseurs cibles (fit de stade, secteur, geographie, taille de ticket)
  |-- Obtenir des warm intros (2-3 intros qualifiees par investisseur cible)

Phase 2 — Lancement et premiers rendez-vous (4-6 semaines)
  |-- Premiere vague de meetings (10-15 investisseurs par semaine les 2 premieres semaines)
  |-- Pitch de 30-45 minutes + Q&A
  |-- Tracking dans un CRM dedie (Notion, Affinity, Streak)
  |-- Ajuster le pitch sur la base des retours

Phase 3 — Due Diligence et term sheet (4-8 semaines)
  |-- Reception des term sheets (objectif : 2-3 pour creer une tension competitive)
  |-- Negociation des termes cles (valorisation, liquidation preference, anti-dilution, board seats)
  |-- Due diligence approfondie (financiere, juridique, technique, commerciale)
  |-- Selection du lead investor

Phase 4 — Closing (4-6 semaines)
  |-- Redaction des documents juridiques (pacte d'actionnaires, contrat d'investissement, statuts)
  |-- Conditions suspensives (GAP, due diligence finale)
  +-- Signature et versement des fonds
      Duree totale typique : 4-6 mois
```

### Pitch Deck — Structure Standard (15-20 Slides)

| Slide | Contenu | Temps (pour un pitch de 20 min) |
|---|---|---|
| **1. Cover** | Nom, tagline, logo | 10 sec |
| **2. Problem** | Le probleme adresse, sa gravite, qui le subit | 1-2 min |
| **3. Solution** | Comment on resout le probleme (valeur, pas features) | 1-2 min |
| **4. Demo / Product** | Capture d'ecran ou demo rapide du produit | 2 min |
| **5. Market** | TAM, SAM, SOM avec methodologie bottom-up | 1 min |
| **6. Business Model** | Comment on gagne de l'argent (pricing, monetisation) | 1 min |
| **7. Traction** | Metriques cles (CA, MRR, croissance, users, NPS) | 2 min |
| **8. Unit Economics** | CAC, LTV, LTV/CAC, payback period | 1-2 min |
| **9. Go-to-Market** | Strategie de vente, canaux, cycle de vente | 1 min |
| **10. Competition** | Positionnement differentiant (matrice, pas liste) | 1 min |
| **11. Team** | Fondateurs, experience cle, complementarite | 1-2 min |
| **12. Financial Projections** | P&L 3-5 ans, hypotheses cles, path to profitability | 2 min |
| **13. Fundraising Ask** | Montant cherche, valorisation cible, utilisation des fonds | 1 min |
| **14. Vision** | Ou on sera dans 5-10 ans | 30 sec |

### Term Sheet — Termes Cles a Negocier

| Terme | Description | Point d'attention |
|---|---|---|
| **Pre-money valuation** | Valorisation de l'entreprise avant l'injection de capital | Determiner la dilution. Eviter les valorisations excessives ("flat round" ou "down round" au tour suivant) |
| **Liquidation Preference** | Priorite de remboursement en cas de liquidation/exit | 1x non-participating est le standard. Eviter les multiples (2x, 3x) et le participating preferred |
| **Anti-dilution** | Protection de l'investisseur en cas de down round | Weighted average broad-based est le standard. Eviter le full ratchet (tres dilutif pour les fondateurs) |
| **Board composition** | Composition du conseil d'administration | Garder le controle (majorite fondateurs + independants). Standard : 2 fondateurs, 1 investisseur, 1-2 independants |
| **Vesting / Founders** | Calendrier d'acquisition des actions des fondateurs | 4 ans avec cliff de 1 an est le standard. Assure l'engagement des fondateurs |
| **Drag-along** | Droit d'obliger les minoritaires a vendre en cas d'offre | Standard. Seuils typiques : 66-75% du capital |
| **Tag-along** | Droit des minoritaires de participer a une vente | Standard. Protege les investisseurs minoritaires |
| **ESOP pool** | Reserve d'options pour les employes | 10-15% post-money est typique. Negocier si constitue avant ou apres le tour (impact sur la dilution) |

### Cap Table Management

La cap table (tableau de capitalisation) recapitule la repartition du capital entre les actionnaires, les detenteurs de BSA/BSPCE et les convertibles.

#### Instruments d'equity en France

| Instrument | Nature | Fiscalite (beneficiaire) | Usage |
|---|---|---|---|
| **Actions ordinaires** | Titre de propriete | PFU 30% ou option bareme IR | Fondateurs, investisseurs |
| **Actions de preference** | Droits specifiques (liquidation pref, anti-dilution) | PFU 30% | Investisseurs VC/PE |
| **BSPCE** | Option d'achat d'actions a prix fixe | PFU 12.8% + PS 17.2% si detenue >3 ans dans la societe | Employes de startups (<15 ans, non cotees ou <150M EUR capi) |
| **BSA** | Bon de souscription d'actions | Plus-value au regime des plus-values mobilieres | Advisors, consultants, administrateurs |
| **AGA (Actions Gratuites)** | Attribution gratuite d'actions | Gain d'acquisition : 30% CSG + IR (abattement 50% si >2 ans). Plus-value : PFU 30% | Cadres dirigeants, retention |
| **Obligations convertibles (OC)** | Dette convertible en actions | Interets : PFU 30%. Conversion : regime des plus-values | Bridge financing entre deux tours |

#### Bonnes pratiques de gestion de cap table

- **Outil dedie** : utiliser un outil specialise (Carta, Ledgy, Capdesk, Ownr) plutot qu'un tableur Excel des le premier tour. La complexite croit exponentiellement avec les tours.
- **Fully diluted** : toujours raisonner en "fully diluted" (incluant tous les BSPCE, BSA, OC et ESOP pool) pour connaitre la dilution reelle.
- **Waterfall analysis** : simuler les scenarios de sortie (exit) a differentes valorisations pour comprendre la repartition effective entre les actionnaires (impact des liquidation preferences, participation, anti-dilution).
- **409A / valorisation independante** : pour les BSPCE et les AGA, le prix d'exercice doit refleter la juste valeur de l'entreprise. Obtenir une valorisation independante (rapport d'expert) pour securiser la fiscalite.

---

## Relations Investisseurs (Investor Relations)

### Communication Post-Levee

Apres la levee, maintenir une communication reguliere et transparente avec les investisseurs :

| Frequence | Format | Contenu |
|---|---|---|
| **Mensuel** | Update email (1-2 pages) | KPIs cles, cash position, highlights/lowlights, asks |
| **Trimestriel** | Board meeting + deck | P&L vs budget, cash flow, KPIs detailles, strategie, risques |
| **Annuel** | Board offsite + plan strategique | Bilan de l'annee, plan N+1, budget, objectifs de recrutement |
| **Ad hoc** | Appel / email | Evenements significatifs (perte client majeur, pivot, opportunite M&A) |

### Investor Update — Template

```
[Nom de l'entreprise] — Monthly Update [Mois/Annee]

HEADLINE (1 phrase)
"Meilleur mois de l'histoire avec 250K EUR d'ARR et 3 nouveaux logos enterprise."

KPIs
- MRR : xxx EUR (+xx% MoM)
- ARR : xxx EUR
- Cash in bank : xxx EUR (runway : xx mois)
- Headcount : xx
- [KPI specifique : NDR, NPS, pipeline, etc.]

HIGHLIGHTS
- [Point positif 1]
- [Point positif 2]

LOWLIGHTS
- [Defi 1 + ce qu'on fait pour y remedier]
- [Defi 2 + plan d'action]

ASKS
- [Intro demandee : nom, societe, raison]
- [Aide recherchee : recrutement, partenariat, conseil]

NEXT MILESTONES
- [Objectif 1 + date cible]
- [Objectif 2 + date cible]
```

---

## Unit Economics — CAC, LTV, Payback

### Customer Acquisition Cost (CAC)

```
CAC = Total des depenses d'acquisition / Nombre de nouveaux clients acquis

Depenses d'acquisition incluent :
- Marketing (paid + organic : salaires marketing, ads, content, events)
- Sales (salaires commerciaux, commissions, outils CRM)
- Exclure : brand marketing general, PR, R&D produit

Variantes :
- Blended CAC : inclut tous les canaux (inbound + outbound + viral)
- Paid CAC : uniquement les canaux payants
- Fully loaded CAC : inclut les frais generaux alloues au GTM (overhead)
```

#### CAC par canal

| Canal | CAC typique (SaaS B2B) | Scalabilite | Cycle |
|---|---|---|---|
| **Inbound (content / SEO)** | 200-800 EUR | Elevee (long terme) | 6-18 mois pour ROI |
| **Paid Search (Google Ads)** | 500-2000 EUR | Moyenne (CPC en hausse) | Immediat |
| **Paid Social (LinkedIn, Meta)** | 300-1500 EUR | Moyenne | 1-3 mois |
| **Outbound (SDR/BDR)** | 1000-5000 EUR | Lineaire (headcount) | 3-6 mois |
| **Partnerships / Channel** | 500-2000 EUR | Elevee | 6-12 mois setup |
| **Product-led growth (PLG)** | 50-300 EUR | Tres elevee | Variable |
| **Referral / viral** | 50-200 EUR | Tres elevee si product-market fit | Long terme |

### Lifetime Value (LTV)

```
LTV = ARPA x Gross Margin % x Average Customer Lifetime

ou :
- ARPA (Average Revenue Per Account) = MRR moyen par client x 12
- Gross Margin % = (CA - COGS) / CA
- Average Customer Lifetime = 1 / Churn Rate (mensuel ou annuel)

Formules alternatives :
- LTV simple = ARPA mensuel x Gross Margin % / Monthly Churn Rate
- LTV avec expansion = ARPA x Gross Margin % x (1 / (Churn Rate - Net Expansion Rate))
  (uniquement si Churn Rate > Net Expansion Rate)
```

#### Exemple numerique

```
Donnees :
- MRR moyen par client : 500 EUR
- Marge brute : 80%
- Taux de churn mensuel : 2%

LTV = 500 x 0.80 / 0.02 = 20 000 EUR
ARPA annuel = 500 x 12 = 6 000 EUR
Duree de vie moyenne = 1 / 0.02 = 50 mois ≈ 4.2 ans
```

### LTV / CAC Ratio

Le ratio LTV/CAC est le KPI roi de l'unit economics :

| LTV / CAC | Interpretation | Action |
|---|---|---|
| **< 1.0** | Destructeur de valeur : chaque client coute plus qu'il ne rapporte | Urgence : ameliorer la retention ou reduire le CAC. Revoir le modele. |
| **1.0 - 3.0** | Insuffisant pour couvrir les frais generaux et generer du profit | Ameliorer la monetisation (upsell), reduire le churn, optimiser les canaux d'acquisition |
| **3.0 - 5.0** | Zone saine. L'entreprise cree de la valeur sur chaque client | Investir pour scaler l'acquisition tout en surveillant l'evolution du ratio |
| **> 5.0** | Excellent, mais potentiellement sous-investissement en acquisition | Accelerer les depenses d'acquisition (growth), tester de nouveaux canaux |

### CAC Payback Period

```
CAC Payback = CAC / (ARPA mensuel x Gross Margin %)

Benchmarks :
- SaaS SMB : 6-12 mois (acceptable), < 6 mois (excellent)
- SaaS Mid-Market : 12-18 mois (acceptable), < 12 mois (bon)
- SaaS Enterprise : 18-24 mois (acceptable), < 18 mois (bon)

Regle generale : payback < 12 mois est un signal de sante.
Un payback > 24 mois signale un probleme de monetisation ou de CAC trop eleve.
```

---

## Metriques SaaS — MRR, ARR, NDR, Churn

### Monthly Recurring Revenue (MRR)

```
MRR = Somme des abonnements mensuels recurrents de tous les clients actifs

Decomposition du MRR :
- New MRR : revenu des nouveaux clients du mois
- Expansion MRR : augmentation du revenu des clients existants (upsell, cross-sell)
- Contraction MRR : diminution du revenu des clients existants (downgrade)
- Churned MRR : revenu perdu des clients partis

MRR net movement = New MRR + Expansion MRR - Contraction MRR - Churned MRR
```

### Annual Recurring Revenue (ARR)

```
ARR = MRR x 12

L'ARR est la metrique de reference pour la valorisation des entreprises SaaS.
Multiples de valorisation ARR typiques (2024-2026) :
- Early-stage (pre-profit, croissance >50%) : 8-15x ARR
- Growth-stage (croissance 30-50%) : 6-12x ARR
- Late-stage / profitable : 5-10x ARR
- Public SaaS median : 6-8x ARR (varie significativement avec la croissance et la rentabilite)
```

### Net Dollar Retention (NDR) / Net Revenue Retention (NRR)

```
NDR = (MRR debut de periode + Expansion - Contraction - Churn) / MRR debut de periode x 100

Exemple :
- MRR debut : 100K EUR
- Expansion : +15K EUR
- Contraction : -3K EUR
- Churn : -5K EUR
- NDR = (100 + 15 - 3 - 5) / 100 = 107%

Benchmarks :
- NDR < 90% : probleme de retention, modele fragile
- NDR 90-100% : retention correcte mais pas d'expansion
- NDR 100-110% : bon, l'expansion compense le churn
- NDR 110-130% : excellent (Slack: 143%, Snowflake: 131%, Datadog: 130%)
- NDR > 130% : exceptionnel, forte expansion/upsell
```

Le NDR est la metrique la plus scrutee par les investisseurs SaaS car un NDR > 100% signifie que l'entreprise croit meme sans ajouter un seul nouveau client.

### Churn — Types et Calcul

```
Logo Churn Rate (mensuel) = Nombre de clients perdus / Nombre de clients debut de mois
Revenue Churn Rate (mensuel) = MRR perdu / MRR debut de mois
Gross Revenue Churn = (Churned MRR + Contraction MRR) / MRR debut de mois

Benchmarks mensuels :
- SaaS SMB/self-serve : 3-7% logo churn / mois (soit 31-58% annuel)
- SaaS Mid-Market : 1-2% logo churn / mois (soit 11-22% annuel)
- SaaS Enterprise : 0.5-1% logo churn / mois (soit 6-11% annuel)

Net Revenue Churn (negatif = bon) = Gross Revenue Churn - Expansion Rate
Un net revenue churn negatif signifie que l'expansion depasse le churn : croissance organique du revenu existant.
```

### Autres Metriques SaaS Cles

| Metrique | Formule | Benchmark |
|---|---|---|
| **Gross Margin** | (Revenue - COGS) / Revenue | >70% (SaaS typique : 75-85%) |
| **Rule of 40** | Revenue Growth Rate % + EBITDA Margin % | >40% = sain |
| **Magic Number** | Net New ARR (QoQ) / S&M Spend (Q-1) | >0.75 = efficient, >1.0 = excellent |
| **Burn Multiple** | Net Burn / Net New ARR | <1.5x = efficient, >2x = danger |
| **Quick Ratio (SaaS)** | (New MRR + Expansion MRR) / (Churned MRR + Contraction MRR) | >4 = excellent |
| **Revenue per Employee** | ARR / FTE | >100K EUR (early), >200K EUR (scale) |
| **ARPU / ARPA** | MRR / Nombre de clients | Varie par segment |
| **Months to Recover CAC** | CAC / (ARPA x Gross Margin %) | <12 mois |

---

## Analyse Financiere — Ratios Cles

### Ratios de Rentabilite

| Ratio | Formule | Interpretation |
|---|---|---|
| **Marge brute** | (CA - COGS) / CA | Capacite a generer de la valeur sur le produit/service |
| **Marge EBITDA** | EBITDA / CA | Rentabilite operationnelle avant amortissements et provisions |
| **Marge nette** | Resultat net / CA | Rentabilite finale apres toutes les charges |
| **ROE (Return on Equity)** | Resultat net / Capitaux propres | Rentabilite pour les actionnaires |
| **ROCE (Return on Capital Employed)** | EBIT x (1-IS) / (CP + Dette nette) | Rentabilite du capital investi |
| **ROA (Return on Assets)** | Resultat net / Total actif | Efficacite de l'utilisation des actifs |

### Decomposition de Dupont (ROE)

```
ROE = Marge nette x Rotation des actifs x Levier financier
    = (Resultat net / CA) x (CA / Total actif) x (Total actif / Capitaux propres)

Cette decomposition permet d'identifier les leviers de la rentabilite :
- Marge nette : pilotage des couts et du pricing
- Rotation des actifs : efficacite operationnelle (BFR, utilisation des actifs)
- Levier financier : structure de financement (endettement)
```

### Ratios de Solvabilite et d'Endettement

| Ratio | Formule | Cible indicative |
|---|---|---|
| **Gearing (Debt/Equity)** | Dette nette / Capitaux propres | < 1.0 (varie par secteur) |
| **Leverage (Dette nette / EBITDA)** | Dette financiere nette / EBITDA | < 3.0x (< 2.0x pour les PME) |
| **Interest Coverage** | EBITDA / Charges d'interets nettes | > 4.0x |
| **Equity Ratio** | Capitaux propres / Total bilan | > 30% |

### Ratios de BFR et Cycle de Tresorerie

| Ratio | Formule | Objectif |
|---|---|---|
| **DSO** | (Creances clients / CA TTC) x 365 | Reduire (30-60 jours selon le secteur) |
| **DPO** | (Dettes fournisseurs / Achats TTC) x 365 | Maximiser (dans le respect de la loi) |
| **DIO** | (Stocks / COGS) x 365 | Reduire (optimiser sans rupture) |
| **CCC** | DSO + DIO - DPO | Minimiser (negatif = ideal) |
| **BFR / CA** | BFR / CA annuel | Reduire (benchmark sectoriel) |

---

## State of the Art (2024-2026)

### Evolution du Paysage VC et Fundraising

Le marche du venture capital a subi des transformations profondes depuis 2022 :

- **Retour a la discipline** : apres l'euphorie 2020-2021 (valorisations record, levees rapides), le marche est revenu a des fondamentaux plus stricts. Les investisseurs exigent une "path to profitability" claire des la Serie A. Le "growth at all costs" est revolu.
- **Compression des multiples** : les multiples de valorisation ARR des SaaS publics ont baisse de 15-25x (pic 2021) a 6-10x (2024-2026). Les valorisations des entreprises privees s'ajustent progressivement.
- **Metriques de qualite** : les investisseurs privilegient la qualite du revenu (NDR, gross margin, revenue quality score) a la croissance brute. Un NDR de 120% avec une croissance de 40% est prefere a une croissance de 80% avec un NDR de 90%.
- **Efficience du capital** : le burn multiple (net burn / net new ARR) est devenu une metrique de reference. Un burn multiple < 1.5x est considere efficient. Les entreprises "capital efficient" levent plus facilement et a de meilleures conditions.
- **Bridge rounds et extensions** : augmentation des tours de financement intermediaires (bridge, extension) pour les entreprises qui n'atteignent pas les milestones de leur prochain tour.

### Revenue-Based Financing (RBF) et Alternatives Non-Dilutives

L'ecosysteme de financement non-dilutif s'est enrichi :

- **RBF** : financement rembourse sur un pourcentage du CA (5-10% du CA mensuel jusqu'a remboursement de 1.3-1.8x le montant avance). Acteurs : Silvr, Capchase, Pipe, Clearco. Adapte aux entreprises SaaS avec des revenus recurrents previsibles.
- **ARR-based lending** : prets adosses a l'ARR (50-100% de l'ARR comme plafond de pret). Moins dilutif que l'equity, avec des taux de 8-15%.
- **Government-backed loans** : en France, les prets BPI (Bpifrance) restent un pilier du financement des PME et startups (pret d'amorcage, pret innovation, garanties).
- **Crowdfunding equity** : les plateformes de crowdfunding (Crowdcube, Seedrs, WeFundPeople) permettent de lever 100K-5M EUR aupres d'investisseurs individuels. Complement aux tours VC pour diversifier la base d'investisseurs.

### Metriques AI-Native et Nouveaux Modeles SaaS

L'emergence des modeles AI-native cree de nouvelles metriques :

- **Usage-based pricing** : la tarification a l'usage (API calls, tokens, compute credits) se generalise pour les produits AI. Les metriques traditionnelles (MRR, ARR) doivent etre adaptees pour capturer la volatilite inherente aux modeles usage-based.
- **Cost of Revenue en hausse** : les couts d'inference AI (GPU, API LLM) augmentent le COGS des entreprises AI-native, compressant les marges brutes. La marge brute des SaaS AI-native est souvent de 50-65% vs 75-85% pour les SaaS traditionnels.
- **Net Dollar Retention booste par l'expansion AI** : les clients qui adoptent des fonctionnalites AI augmentent naturellement leur consommation, boostant le NDR.
- **Metriques specifiques** : tokens consumed per user, AI feature adoption rate, cost per inference, AI gross margin (marge apres couts d'inference).

### PLG (Product-Led Growth) et Hybrid Go-to-Market

Les modeles de distribution evoluent :

- **PLG + Sales-assist** : le modele purement PLG (adoption virale, self-serve) s'hybride avec une couche commerciale (sales-assisted PLG). L'utilisateur decouvre le produit seul, la vente intervient pour le passage en offre enterprise. Exemples : Notion, Figma, Slack.
- **Metriques PLG** : Product Qualified Leads (PQL), Time-to-Value (TTV), activation rate, PQL-to-paid conversion rate.
- **Community-Led Growth (CLG)** : construction de communautes de pratique comme canal d'acquisition (dbt, Airbyte). Metriques : community size, engagement rate, community-sourced ARR.

### Real-Time Financial Intelligence

Les outils d'analyse financiere en temps reel se democratisent :

- **Automated KPI dashboards** : les plateformes (ChartMogul, Baremetrics, ProfitWell/Paddle) calculent automatiquement les metriques SaaS a partir des donnees de facturation. Plus besoin de tableurs manuels.
- **Predictive churn** : les modeles de ML predisent le risque de churn par client en analysant les patterns d'usage, les tickets support, les indicateurs d'engagement. Le customer success intervient avant le churn, pas apres.
- **Dynamic pricing** : les outils d'optimisation de pricing (Corrily, Pricefx) testent dynamiquement les niveaux de prix pour maximiser le revenu tout en maintenant la conversion.
- **Investor reporting automation** : les plateformes (Visible, Carta, Ownr) automatisent la production des investor updates et des reportings board a partir des donnees financieres et operationnelles integrees.

### ELTIF 2.0 et Democratisation du Private Equity

Le nouveau reglement ELTIF 2.0 (European Long-Term Investment Fund, applicable depuis 2024) facilite l'acces des investisseurs non-professionnels au capital-investissement :

- **Seuil d'investissement abaisse** : suppression du ticket minimum de 10 000 EUR.
- **Classe d'actifs elargie** : inclusion de FinTechs, immobilier, infrastructure, real assets.
- **Impact pour les startups et ETI** : potentiel d'elargissement de la base d'investisseurs, acces a des capitaux plus patients et plus diversifies.
- **Liquidite amelioree** : possibilite de rachats periodiques (sous conditions), rendant les fonds de PE plus accessibles aux investisseurs individuels.
