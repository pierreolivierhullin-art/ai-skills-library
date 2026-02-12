# Supply Chain Management — Planification, Stocks, Logistique et Resilience

## Overview

Ce document de reference couvre l'ensemble des disciplines de la gestion de la chaine d'approvisionnement : demand planning, gestion des stocks, logistique, procurement, S&OP et visibilite supply chain. Il fournit les modeles de decision, les formules cles et les architectures organisationnelles necessaires pour concevoir et piloter une supply chain performante, agile et resiliente. Utiliser ce guide pour structurer toute decision liee a la planification, a l'approvisionnement, a la production et a la distribution.

---

## Demand Planning & Forecasting

### Fondamentaux de la prevision

La prevision de la demande est le point de depart de toute planification supply chain. Accepter d'emblee que toute prevision est fausse — l'objectif est de minimiser l'erreur et de concevoir des systemes capables d'absorber l'erreur residuelle.

#### Methodes de prevision

| Methode | Type | Quand l'utiliser | Precision typique |
|---|---|---|---|
| **Moyenne mobile** | Quantitative / Time series | Demande stable sans tendance ni saisonnalite | Faible a moyenne |
| **Lissage exponentiel (SES)** | Quantitative / Time series | Demande stable, reaction rapide aux changements recents | Moyenne |
| **Holt-Winters** | Quantitative / Time series | Demande avec tendance et saisonnalite | Bonne |
| **ARIMA/SARIMA** | Quantitative / Time series | Demande complexe, series longues | Bonne a tres bonne |
| **Regression lineaire/multiple** | Quantitative / Causale | Quand des facteurs explicatifs sont identifies | Variable (depend des facteurs) |
| **Machine Learning (XGBoost, LSTM)** | Quantitative / AI | Grands volumes de donnees, patterns non lineaires | Tres bonne si donnees suffisantes |
| **Jugement d'expert / Delphi** | Qualitative | Nouveau produit, absence de donnees historiques | Variable (depend des experts) |
| **Analogie** | Qualitative | Nouveau produit similaire a un produit existant | Moyenne |

#### Mesures de l'erreur de prevision

- **MAD (Mean Absolute Deviation)** = moyenne(|reel - prevu|). Simple mais ne permet pas la comparaison entre produits.
- **MAPE (Mean Absolute Percentage Error)** = moyenne(|reel - prevu| / reel) x 100. Permet la comparaison mais pose probleme quand la demande est proche de zero.
- **WMAPE (Weighted MAPE)** = somme(|reel - prevu|) / somme(reel) x 100. Plus robuste que le MAPE pour les portefeuilles de produits.
- **Forecast Bias** = somme(prevu - reel) / n. Detecte le biais systematique (sur-prevision ou sous-prevision).
- **Tracking Signal** = somme cumulative des erreurs / MAD. Si > 4, le modele est probablement biaise.

#### Demand Sensing vs Demand Planning

- **Demand Planning** : prevision a moyen/long terme (3-18 mois), base sur les historiques et les hypotheses commerciales. Utiliser pour la planification de capacite et les achats strategiques.
- **Demand Sensing** : ajustement a court terme (0-12 semaines) base sur les signaux de demande recents (POS data, commandes en cours, donnees meteo, evenements). Utiliser pour l'ajustement des approvisionnements et la logistique.

---

## Inventory Management — Gestion des Stocks

### Couts de stock

Comprendre les quatre composantes du cout de stock pour optimiser les decisions :

1. **Cout de possession (Holding Cost)** : typiquement 15-30% de la valeur annuelle du stock. Inclut le cout du capital immobilise, l'entreposage, l'assurance, l'obsolescence et la deterioration.
2. **Cout de commande (Ordering Cost)** : cout fixe par commande (administratif, transport fixe, reception, controle qualite). Pousser a augmenter les tailles de lot.
3. **Cout de rupture (Stockout Cost)** : ventes perdues, penalites contractuelles, perte de reputation, cout de production d'urgence. Souvent sous-estime.
4. **Cout unitaire** : peut varier avec la quantite (remises volume), le fournisseur et les conditions de marche.

### Economic Order Quantity (EOQ)

La formule classique de Wilson pour determiner la quantite optimale de commande :

```
EOQ = sqrt(2 * D * S / H)

Ou :
  D = demande annuelle (unites)
  S = cout fixe par commande (euros)
  H = cout de possession annuel par unite (euros)
```

**Limites de l'EOQ** : suppose une demande constante, un lead time fixe, pas de remise volume, pas de contrainte de capacite. Utiliser comme point de depart puis ajuster selon les contraintes reelles.

**Variantes** :
- **EOQ avec remise volume** : comparer le cout total (achat + commande + possession) pour chaque palier de prix.
- **EOQ avec contrainte de capacite** : ajuster la quantite de commande pour respecter les limites de stockage ou de tresorerie.
- **POQ (Periodic Order Quantity)** : commander a intervalles fixes plutot qu'a quantite fixe, plus adapte aux systemes de revue periodique.

### Safety Stock (Stock de Securite)

Le stock de securite absorbe la variabilite de la demande et du lead time. Formule standard :

```
Safety Stock = Z * sqrt(LT * sigma_D^2 + D_avg^2 * sigma_LT^2)

Ou :
  Z = facteur de service (z-score correspondant au taux de service cible)
  LT = lead time moyen
  sigma_D = ecart-type de la demande par periode
  D_avg = demande moyenne par periode
  sigma_LT = ecart-type du lead time
```

**Niveaux de service typiques** :

| Taux de service | Z-score | Usage |
|---|---|---|
| 90% | 1.28 | Produits de commodite, faible impact de rupture |
| 95% | 1.65 | Standard pour la plupart des SKU |
| 97.5% | 1.96 | Produits importants, clients exigeants |
| 99% | 2.33 | Produits critiques, risque de perte de client |
| 99.9% | 3.09 | Pieces de rechange critiques, securite |

### Classification ABC/XYZ

#### Classification ABC (par valeur)

Segmenter les references (SKU) par leur contribution a la valeur totale (Pareto) :
- **A** : 20% des SKU representant 80% de la valeur. Gestion fine, revue frequente, haute priorite.
- **B** : 30% des SKU representant 15% de la valeur. Gestion intermediaire.
- **C** : 50% des SKU representant 5% de la valeur. Gestion simplifiee, automatisation maximale.

#### Classification XYZ (par variabilite)

Segmenter par la previsibilite de la demande (coefficient de variation CV = ecart-type / moyenne) :
- **X** : CV < 0.5. Demande reguliere, prevision fiable. Approvisionnement MRP classique.
- **Y** : 0.5 <= CV < 1.0. Demande moderement variable. Buffer de securite et demand sensing.
- **Z** : CV >= 1.0. Demande tres erratique. Make-to-order ou stock de securite eleve.

#### Matrice ABC-XYZ croisee

| | X (Regulier) | Y (Variable) | Z (Erratique) |
|---|---|---|---|
| **A (Valeur haute)** | Kanban / JIT. Optimisation fine. | Safety stock + demand sensing. Revue hebdo. | Contrats cadre + stock de securite eleve. Alert management. |
| **B (Valeur moyenne)** | Reorder point automatique. | Revue periodique. | Make-to-order si possible. |
| **C (Valeur basse)** | Commande automatique en gros. | Commande groupee. | Eliminer ou consolider les SKU. |

### Reorder Point (Point de Commande)

```
Reorder Point = D_avg * LT + Safety Stock

Ou :
  D_avg = demande moyenne quotidienne
  LT = lead time de reapprovisionnement (jours)
```

### Demand-Driven MRP (DDMRP)

Le DDMRP (Demand-Driven Institute, Ptak & Smith) est une evolution du MRP classique qui positionne des buffers strategiques de decouplage pour absorber la variabilite :

1. **Positionner les buffers** : identifier les points strategiques de la supply chain ou positionner des buffers (matiere premiere cle, sous-ensemble critique, produit fini a forte demande).
2. **Dimensionner les buffers** : chaque buffer a trois zones (vert, jaune, rouge) basees sur le lead time decouple, la variabilite et le profil de demande.
3. **Ajuster dynamiquement** : les buffers sont recalcules regulierement selon les changements de demande et de lead time (Demand Adjustment Factors, Lead Time Adjustment Factors).
4. **Planifier par la demande reelle** : le Net Flow Position (on-hand + on-order - qualified demand) determine les ordres de reapprovisionnement. Pas de prevision detaillee au niveau SKU.
5. **Executer visiblement** : des alertes visuelles (rouge/jaune/vert) prioritisent l'execution.

---

## Logistics — 3PL, Last Mile, Reverse Logistics

### Architecture logistique

#### Modeles de sous-traitance logistique

| Modele | Description | Quand l'utiliser |
|---|---|---|
| **1PL** | Logistique en interne (flotte propre, entrepots propres) | Volume tres eleve, competence cle, controle maximal |
| **2PL** | Transport sous-traite uniquement | Volume moyen, besoin de flexibilite transport |
| **3PL** | Externalisation entreposage + transport | Besoin de scalabilite, expertise logistique, couverture geographique |
| **4PL** | Orchestrateur logistique global (Lead Logistics Provider) | Supply chain complexe, multi-3PL, besoin d'optimisation globale |
| **5PL** | Agregateur de chaines logistiques (plateforme) | E-commerce marketplace, supply chain en reseau |

#### Selection d'un 3PL — Criteres cles

1. **Couverture geographique** : zones couvertes, capillarite du reseau.
2. **Capacite et scalabilite** : capacite a absorber les pics (Black Friday, soldes).
3. **Technologie** : WMS (Warehouse Management System), TMS (Transport Management System), EDI/API, visibilite temps reel.
4. **SLA et performance** : taux de service, taux d'erreur, lead time, gestion des retours.
5. **Couts** : structure de prix (fixe vs variable), couts caches (surcharges carburant, frais de manipulation).
6. **Conformite** : certifications (ISO, GDP pour le pharma), assurances, RSE.

### Last Mile Delivery

Le "dernier kilometre" represente 40-50% du cout logistique total et est le moment de verite pour l'experience client.

#### Strategies de livraison last mile

- **Hub and Spoke** : entrepot central -> hubs regionaux -> livraison. Modele classique, economies d'echelle.
- **Dark Stores / Micro-Fulfillment Centers** : petits entrepots urbains proches du client final. Permettent le quick commerce (livraison < 2h).
- **Point relais / Consignes** : reduction du cout de livraison (pas de probleme d'absence) et de l'empreinte carbone. Modele dominant en Europe.
- **Ship-from-Store** : utiliser les stocks en magasin pour livrer les commandes e-commerce locales. Optimise le stock et accelere la livraison.
- **Crowdsourced Delivery** : utiliser un reseau de livreurs independants pour la flexibilite. Adapte aux pics de demande.

### Reverse Logistics

La logistique inversee (retours, recyclage, reconditionnement) est un levier strategique sous-estime :

- **Gatekeeping** : filtrer les retours a la source pour eviter les retours injustifies. Politique de retour claire, photos/diagnostics avant acceptation.
- **Grading et disposition** : classifier les retours (revendable en l'etat, reconditionnable, recyclable, dechet) pour optimiser la valeur recuperee.
- **Reconditionnement (Refurbishment)** : remettre en etat les produits retournes pour les revendre a un prix reduit. Marche en forte croissance (economie circulaire).
- **Closed-Loop Supply Chain** : concevoir la supply chain pour recuperer et reutiliser les materiaux en fin de vie (DfD — Design for Disassembly).

---

## Procurement & Strategic Sourcing

### Matrice de Kraljic

Classer les achats selon leur impact sur le profit et le risque d'approvisionnement :

| | Risque faible | Risque eleve |
|---|---|---|
| **Impact profit eleve** | **Leverage** : maximiser le pouvoir de negociation, mise en concurrence, encheres inversees. | **Strategic** : partenariats long terme, co-developpement, risk sharing, dual sourcing. |
| **Impact profit faible** | **Non-critical** : simplifier, automatiser, P2P digitale, catalogues. | **Bottleneck** : securiser l'approvisionnement, developper des alternatives, stock de securite. |

### Total Cost of Ownership (TCO)

Ne jamais selectionner un fournisseur sur le prix unitaire seul. Le TCO integre :

- Prix unitaire + transport + droits de douane + assurance.
- Cout de la qualite : taux de defauts, couts de controle, retouches.
- Cout logistique : lead time, variabilite, taille de lot minimale.
- Couts administratifs : complexite des commandes, facturation, litiges.
- Risques : dependance fournisseur unique, risque pays, stabilite financiere.
- Innovation : capacite du fournisseur a co-innover, roadmap technologique.

### Supplier Relationship Management (SRM)

#### Segmentation des fournisseurs

| Segment | Strategie | KPI |
|---|---|---|
| **Strategique** | Partenariat long terme, innovation conjointe, partage de risques | Score qualite, innovation, reduction TCO, resilience |
| **Prefere** | Contrats cadres, collaboration reguliere | OTD (On-Time Delivery), qualite, reactivite |
| **Approuve** | Mise en concurrence periodique, suivi standard | Prix, OTD, conformite |
| **Transactionnel** | Catalogues, P2P automatise, spot buying | Prix, disponibilite |

---

## S&OP (Sales & Operations Planning)

### Processus S&OP standard (cycle mensuel)

Le S&OP aligne la demande commerciale, la capacite operationnelle et les objectifs financiers sur un horizon de 3-18 mois :

| Semaine | Etape | Participants | Livrables |
|---|---|---|---|
| **S1** | Data Gathering & Statistical Forecast | Demand Planning | Forecast statistique de base, donnees marche |
| **S2** | Demand Review | Commercial, Marketing, Demand Planning | Consensus demand plan (integrant promos, lancements, evenements) |
| **S3** | Supply Review | Operations, Supply Chain, Procurement | Supply plan, identification des contraintes, scenarios |
| **S4** | Pre-S&OP Alignment | Finance, Demand, Supply | Scenarios chiffres (optimiste, nominal, pessimiste), recommandations |
| **S5** | Executive S&OP | Direction Generale | Decisions arbitrees, plan valide, allocation des ressources |

### KPI du S&OP

- **Forecast Accuracy** (WMAPE) : cible < 20% au niveau famille de produits.
- **Demand Plan Value Added (FVA)** : mesurer si chaque etape d'enrichissement ameliore la prevision. Supprimer les etapes qui degradent la prevision.
- **S&OP Adherence** : ecart entre le plan S&OP valide et l'execution reelle.
- **Inventory vs Plan** : ecart de stock reel vs plan.
- **Service Level** : taux de service reel vs objectif.

### IBP (Integrated Business Planning)

L'IBP est l'evolution du S&OP vers une planification integree couvrant strategie, finance, demande, supply et portefeuille produits. Principales differences avec le S&OP classique :

- Horizon etendu (24-36 mois vs 3-18 mois pour le S&OP).
- Integration financiere native (P&L par scenario).
- Gestion du portefeuille produits (lancements, phase-outs).
- Scenario planning avance (what-if analysis).
- Alignement direct avec le plan strategique.

---

## Supply Chain Visibility & Control Tower

### Niveaux de maturite de la visibilite

| Niveau | Capacite | Technologie |
|---|---|---|
| **1. Reactive** | Visibilite apres coup (rapports periodiques) | ERP, tableurs |
| **2. Tracking** | Suivi en temps reel des flux physiques | TMS, GPS, RFID |
| **3. Predictive** | Anticipation des disruptions et des retards | AI/ML, IoT, donnees externes |
| **4. Prescriptive** | Recommandations d'actions automatiques | Digital twin, optimization engines |
| **5. Autonomous** | Execution autonome des ajustements | AI autonome, autonomous planning |

### Architecture d'une Control Tower

Une supply chain control tower centralise la visibilite et la capacite de decision :

- **Data Integration Layer** : connecteurs vers ERP, WMS, TMS, fournisseurs, transporteurs, IoT. Utiliser des APIs et de l'EDI. Les plateformes comme project44, FourKites, o9 Solutions fournissent des connecteurs pre-integres.
- **Analytics Layer** : tableaux de bord temps reel, alertes, analyses predictives. KPI : OTD, inventory levels, forecast accuracy, lead time performance.
- **Decision Layer** : simulation de scenarios, recommandations d'action, workflows d'escalade.
- **Collaboration Layer** : communication avec les fournisseurs, transporteurs et clients. Portail collaboratif.

---

## State of the Art (2024-2026)

### Digital Supply Chain Twin

Le jumeau numerique de la supply chain est l'avancee la plus transformatrice de 2024-2026 :

- **Definition** : reproduction virtuelle de l'ensemble de la chaine d'approvisionnement (reseaux, flux, stocks, capacites, contraintes) mise a jour en temps reel.
- **Usages** : simulation de scenarios (que se passe-t-il si ce fournisseur est en rupture pendant 3 semaines ?), optimisation du network design, test de strategies d'inventaire avant implementation.
- **Plateformes** : o9 Solutions, Coupa Supply Chain Design, anyLogistix, LLamasoft (Coupa), GAINS, Kinaxis (RapidResponse).
- **Maturite** : les leaders du Gartner Supply Chain Top 25 (Schneider Electric, Cisco, Johnson & Johnson, L'Oreal, Nestle) ont deploye des digital twins operationnels. L'adoption s'accelere dans les mid-market grace aux solutions cloud.

### AI-Native Supply Chain Planning

L'IA transforme fondamentalement la planification supply chain :

- **Demand Sensing avec ML** : les modeles de machine learning (gradient boosting, deep learning) integrent des signaux externes (meteo, evenements, reseaux sociaux, POS data, Google Trends) pour ajuster les previsions a court terme avec une precision de 20-40% superieure aux methodes statistiques classiques.
- **Autonomous Planning** : des systemes d'IA prennent des decisions de reapprovisionnement automatiquement pour les SKU stables (categories A-X et B-X de la matrice ABC-XYZ), liberant les planificateurs pour se concentrer sur les exceptions.
- **Probabilistic Forecasting** : au lieu d'un chiffre unique de prevision, generer des distributions de probabilite (quantile forecasting) pour dimensionner les safety stocks de maniere plus fine.
- **Generative AI pour le S&OP** : utiliser les LLM pour generer des syntheses de donnees, des analyses de scenarios et des narratifs pour les reunions S&OP. Prototypage de plans d'action bases sur les contraintes identifiees.

### Resilience et Risk Management

Les crises recentes (COVID-19, crise du canal de Suez, semi-conducteurs, tensions geopolitiques) ont renforce la priorite donnee a la resilience :

- **Multi-sourcing et nearshoring** : diversifier les sources d'approvisionnement geographiquement. Le "China+1" devient "China+2+nearshore". Le nearshoring vers l'Europe de l'Est, le Maghreb, le Mexique ou le Vietnam s'accelere.
- **Stress Testing supply chain** : simuler regulierement des scenarios de disruption (perte d'un fournisseur critique, blocage d'un corridor logistique, hausse brutale de la demande) pour identifier les vulnerabilites.
- **Real-Time Risk Monitoring** : plateformes de surveillance des risques en temps reel (Resilinc, Everstream Analytics, Interos, riskmethods) integrant donnees geopolitiques, meteo, financieres et sanitaires.
- **Inventory Repositioning** : passer de la minimisation absolue des stocks (JIT) a une strategic inventory positioning ou des buffers de decouplage protegent le flux aux points critiques (approche DDMRP).

### Sustainable Supply Chain

La durabilite devient un critere de performance au meme titre que le cout et le delai :

- **Scope 3 Emissions Tracking** : mesurer et reduire les emissions de gaz a effet de serre sur toute la chaine (scope 3 represente 70-90% des emissions totales pour la plupart des entreprises). Plateformes : Watershed, Persefoni, Carbonfact.
- **Circular Supply Chain** : concevoir des chaines d'approvisionnement circulaires (reconditionnement, remanufacturing, recyclage). Les modeles Product-as-a-Service (PaaS) facilitent la recuperation des produits en fin de vie.
- **Deforestation-Free Supply Chains** : la reglementation EU (EUDR — European Union Deforestation Regulation) impose la tracabilite des chaines d'approvisionnement pour 7 commodites (soja, huile de palme, cacao, bois, cafe, caoutchouc, betail).
- **Green Logistics** : vehicules electriques, optimisation des chargements (fill rate), consolidation des envois, choix modal (report modal route vers rail ou maritime).

### Supply Chain as a Service (SCaaS)

- **Fulfillment-as-a-Service** : des prestataires (Amazon MCF, ShipBob, Flexport) offrent des capacites logistiques completes en mode plateforme, permettant aux entreprises de scaler leur logistique sans investissement en actifs.
- **API-First Supply Chain** : les systemes supply chain s'integrent via des APIs standardisees, permettant de composer des chaines d'approvisionnement flexibles a partir de services specialises.
- **Marketplace Logistics** : les marketplaces (Amazon, Zalando, Cdiscount) proposent des services logistiques integres (FBA, ZFS) qui redefinissent les normes de livraison (J+1, creneaux de livraison).

### Exemples de KPI supply chain modernes

```
Planification :
- Forecast Accuracy (WMAPE) : cible < 15% (famille) / < 25% (SKU)
- Forecast Bias : cible entre -2% et +2%
- S&OP Adherence : cible > 90%

Stock :
- Inventory Turns : cible selon industrie (retail > 8, industrie > 4)
- Days of Supply : adapte a la strategie
- Obsolete/Slow-Moving Stock : cible < 5% de la valeur stock
- Stock Accuracy : cible > 99%

Service :
- OTIF (On Time In Full) : cible > 95%
- Perfect Order Rate : cible > 90%
- Order-to-Delivery Lead Time : benchmark marche
- Backorder Rate : cible < 2%

Logistique :
- Cost-to-Serve : tracking par canal, client, produit
- Transport Cost / Revenue : cible < 5%
- Warehouse Productivity : lignes/heure/operateur
- Vehicle Fill Rate : cible > 85%

Resilience et Durabilite :
- Time-to-Recover (TTR) : temps pour retrouver le service apres disruption
- Supplier Risk Score : surveillance continue
- Scope 3 Emissions / Revenue : reduction YoY
- Circular Material Rate : % de materiaux recycles ou reutilises
```
