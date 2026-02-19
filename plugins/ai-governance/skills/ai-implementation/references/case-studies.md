# Etudes de Cas — Implementation IA en Production

## Vue d'Ensemble

Ces etudes de cas illustrent des implementations IA reelles couvrant le cycle complet : definition du probleme, qualification du PoC, deploiement en production, et mesure du ROI. Chaque cas presente les decisions cles, les obstacles rencontres, et les lecons apprises.

---

## Cas 1 — Churn Prediction pour un SaaS B2B (Taux PoC-to-Prod reussi)

### Contexte

Plateforme SaaS B2B avec 15 000 clients PME, revenu annuel de 45 M EUR, taux de churn mensuel de 4.2% (50.4% annualisé — tres eleve pour le SaaS). L'equipe de Customer Success avait 12 personnes mais contactait les clients de maniere reactive (apres resiliation) plutot que proactive.

### Definition du Probleme

**Variable cible** : Churn dans les 30 prochains jours (definition stricte : non-renouvellement de l'abonnement mensuel ou annuel dans les 30 jours).

**KPI metier** : Reduire le taux de churn mensuel de 4.2% a 3.5% en 6 mois = 0.7 point de reduction = 105 clients retenus/mois = 105 x LTV moyen 3 000 EUR = 315 000 EUR de revenus sauvegardes/mois.

**Seuil de reussite du PoC** : AUC-PR > 0.65 et Recall@top20% > 55% (detecter plus de 55% des churners en contactant les 20% de clients avec le score le plus eleve).

### Construction du PoC (4 semaines)

**Donnees disponibles** :
- Historique de connexions (3 ans) : date, duree, features utilisees
- Historique de facturation : paiements, retards, litiges
- Tickets support : volume, nature, CSAT
- Profil entreprise : taille, secteur, anciennete, tier d'abonnement

**Features les plus predictives** (via SHAP) :
1. Tendance d'utilisation sur 4 semaines (ratio semaine4/semaine1)
2. Nb de tickets support ouverts dans les 30 derniers jours
3. Jours depuis la derniere connexion
4. Score CSAT moyen sur les 90 derniers jours
5. Pourcentage de features cles utilisees (activation score)

**Modele final** : LightGBM avec validation out-of-time (4 mois de test)
- AUC-ROC : 0.84
- AUC-PR : 0.71 (> seuil 0.65)
- Recall@top20% : 62% (> seuil 55%)

**Decision Go/No-Go** : GO — tous les criteres passes, latence batch < 2 minutes pour 15 000 clients.

### Deploiement (6 semaines)

**Architecture choisie** : Batch inference hebdomadaire (pas de need temps reel), scores pousses vers le CRM Salesforce via API.

**Pipeline MLOps** :
- Entrainement mensuel via pipeline Airflow (trigger: premier lundi du mois)
- Feature engineering en dbt (partage entre entrainement et scoring)
- Tracking MLflow avec model registry
- Scoring batch le lundi matin, import Salesforce le lundi apres-midi

**Monitoring configure** :
- Distribution hebdomadaire des scores (alerte si distribution shift > 15%)
- Volume de predictions (alerte si < 13 000 ou > 16 000)
- Performance mensuelle sur echantillon labelle (alerte si AUC-PR < 0.60)

### Mesure du ROI (A/B Test sur 90 jours)

**Design** : 50% des clients a risque eleve (score > 0.65) contactes par le CS (groupe traitement), 50% non contactes (groupe controle).

**Resultats** :
- Churn dans le groupe traitement : 2.9% (vs 4.1% dans le controle)
- Reduction absolue : 1.2 points
- Clients retenus additionnels : 90/mois
- Valeur mensuelle generee : 90 x 3 000 EUR LTV = 270 000 EUR
- Couts mensuels du modele : 8 000 EUR (compute + maintenance)
- ROI mensuel : (270 000 - 8 000) / 8 000 = 32x

**Lecons apprises** :
- La feature "tendance d'utilisation" etait beaucoup plus predictive que l'utilisation absolue
- Le taux de contact optimal est 20% des clients (au-dela, le signal se dilue)
- L'equipe CS avait besoin d'un guide d'action par niveau de risque pour maximiser l'impact

---

## Cas 2 — Demand Forecasting pour un Retailer Alimentaire (Complexite Operationnelle)

### Contexte

Chaine de distribution alimentaire avec 150 magasins, 8 000 SKUs actifs, gestion des stocks critique (produits perissables, marges faibles). Avant le ML, les previsonistes manuels avaient un MAPE de 28% sur les previsions J+7, generant des surstocks de 12% et des ruptures sur 6% du CA.

### Choix d'Architecture Multi-Modeles

**Segmentation par type de produit** :

| Segment | Caracteristiques | Modele retenu | MAPE cible |
|---|---|---|---|
| Produits stables | Faible variabilite, pas de saisonnalite forte | SARIMA | < 12% |
| Produits saisonniers | Saisonnalite hebdo/annuelle, promotions | Prophet | < 18% |
| Nouveaux produits | Historique < 6 mois | Media des ventes similaires + XGBoost | < 25% |
| Produits promo | Spike lors des promotions, difficult a prevoir | XGBoost + calendar features | < 30% |

**Challenge technique principal** : Hierarchie multi-niveaux (national -> regional -> magasin -> SKU). La somme des previsions par SKU et par magasin doit etre coherente avec les previsions agregees.

**Solution** : Reconciliation hierarchique bottom-up pour la prevision operationnelle, top-down pour la planification strategique. Implementation avec la librairie `hierarchicalforecast`.

### Pipeline de Production

**Frequence** : Previsions quotidiennes J+1 a J+14, recalcul a 4h00.

**Donnees** :
- Historique de ventes par SKU/magasin (3 ans, 8M lignes)
- Calendrier des promotions (3 mois d'avance)
- Meteo (API externe, 7 jours d'avance)
- Jours feries et evenements locaux

**Infrastructure** :
- Spark sur EMR pour l'entrainement (8 000 SKUs x 150 magasins en parallele)
- DynamoDB pour les previsions en production (acces rapide par le systeme de commandes)
- Airflow pour l'orchestration, MLflow pour le tracking par SKU

### Resultats et Impact

- MAPE J+7 passe de 28% a 14% (-50% d'erreur)
- Surstock reduit de 12% a 7% (-42%)
- Ruptures reduites de 6% a 3.5% du CA (-42%)
- Impact financier : 2.3 M EUR d'economie annuelle (reduction surstock + ventes recuperees)
- ROI sur investissement de 380 000 EUR : 6x en an 1

**Obstacles rencontres** :
- Data leakage initial : les features de promotions etaient calculees sur toute la periode, pas en "point in time" — correction necessaire qui a pris 2 semaines.
- Certains magasins avaient des distributions tres differentes (clientele touristique vs. residentielle) — segmentation supplementaire requise.

---

## Cas 3 — Fraude Detection en Temps Reel (Contraintes de Latence)

### Contexte

Plateforme de paiement en ligne traitant 2 millions de transactions/jour. Taux de fraude initial : 0.08% (1 600 transactions frauduleuses/jour), montant moyen fraude : 180 EUR, perte mensuelle : 8.6 M EUR. Systeme existant : regles metier avec 70% de recall et 12% de precision (88% de faux positifs generant de la friction client).

### Contraintes Techniques Non-Negociables

- **Latence** : decision en < 30ms pour 99% des transactions (P99 < 30ms)
- **Disponibilite** : 99.99% uptime (SLA du processeur de paiement)
- **Volume** : 2M transactions/jour = 23 transactions/seconde en moyenne, pic a 200/seconde

### Architecture Retenue

**Ensemble a 3 couches** :

**Couche 1 — Regles deterministiques** (< 1ms) :
- Pays blacklistes, IP suspectes, patterns connus (IBAN frauduleux)
- Bloquage immediat si score de regle > seuil critique
- 15% des transactions bloquees ici, precision = 95%

**Couche 2 — Modele ML leger** (< 5ms) :
- LightGBM avec 50 features numeriques (pre-calculees dans un feature store Redis)
- Features : velocite (nb transactions/1min/5min/15min), montant vs. historique, distance geographique, appareil
- Inference sur CPU, modele quantifie pour reduire la latence

**Couche 3 — Modele ML lourd** (< 25ms) :
- XGBoost avec 200+ features incluant des agregats historiques complexes
- Declenche uniquement sur les transactions avec score couche 2 entre 0.3 et 0.8 (zone ambigue)
- 35% des transactions passent par cette couche

**Feature Store Redis** :
- Pre-calcul des features par customer_id a chaque transaction
- TTL de 24h, acces en < 1ms
- Mise a jour en temps reel via consumer Kafka

### Resultats Techniques

| Metrique | Avant | Apres |
|---|---|---|
| **Recall** | 70% | 87% |
| **Precision** | 12% | 58% |
| **Latence P99** | N/A (regles) | 22ms |
| **Taux de faux positifs** | 88% | 42% |
| **Fraude detectee/mois** | 4.3 M EUR | 7.5 M EUR |
| **Friction client reduite** | - | -53% de transactions bloquees a tort |

**ROI** : Fraude additionnelle detectee (3.2 M EUR/mois) - Couts du systeme (180k EUR/mois) = 18x ROI.

---

## Cas 4 — NLP pour l'Automatisation du Triage Support (MLOps sur LLM)

### Contexte

Entreprise e-commerce avec 50 000 tickets support/mois. Avant le ML : 3 agents pour le triage manuel, delai de triage moyen 45 minutes, 15% d'erreurs de classification (mauvaise equipe assignee).

### Architecture LLM pour le Triage

**Approche** : Fine-tuning d'un modele de classification (DistilBERT) sur l'historique de tickets labelles par les agents humains.

**Classes** : 12 categories (retour produit, probleme livraison, facturation, probleme technique, question produit, etc.)

**Pipeline** :
1. Extraction du ticket (sujet + corps)
2. Preprocessing (suppression des PII, nettoyage)
3. Inference DistilBERT → classe + score de confiance
4. Si confiance > 0.85 : routage automatique vers l'equipe
5. Si confiance < 0.85 : soumis a un agent humain pour validation

**LLMOps specifiques** :
- Suivi du score de confiance moyen (alerte si < 0.75)
- Taux de validation humaine (alerte si > 30%)
- Matrice de confusion mensuelle par categorie
- Retraining trimestriel sur les 3 000 tickets les plus recents

### Resultats

- Taux de triage automatique : 78% des tickets (seuil confiance > 0.85)
- Precision du triage automatique : 94%
- Delai de triage reduit : 45 min → 30 secondes (en moyenne)
- Economies : 2.2 agents ETP liberes pour des taches a valeur ajoutee
- ROI : 8x sur cout annuel du systeme
