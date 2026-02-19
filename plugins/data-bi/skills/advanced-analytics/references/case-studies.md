# Etudes de Cas — ML Avance Applique au Metier

## Vue d'Ensemble

Ces etudes de cas illustrent l'application du machine learning predictif, de la segmentation et de l'experimentation a des problemes metier reels dans differents secteurs.

---

## Cas 1 — Segmentation Client pour une Banque de Detail (RFM + Clustering)

### Contexte

Banque de detail europeenne avec 2.3 millions de clients particuliers. L'equipe marketing utilisait une segmentation basique (Premium / Standard / Basic) basee uniquement sur le solde moyen, ignorant le comportement transactionnel. Taux d'engagement moyen aux campagnes : 2.1%.

### Approche de Segmentation

**Etape 1 — Analyse RFM transactionnelle** (sur les 12 derniers mois) :
- **Recency** : nombre de jours depuis la derniere transaction
- **Frequency** : nombre de transactions par mois
- **Monetary** : montant moyen depense par mois (hors virements)

**Etape 2 — Enrichissement des features** :
- Diversite des produits detenus (compte courant, epargne, credit, assurance)
- Utilisation digitale (app mobile, web banking)
- Saisonnalite des depenses (loisirs vs. necessites)
- Propension aux produits additionnels (score base sur les achats similaires)

**Etape 3 — Clustering hierarchique Ward** :
- 7 clusters identifies (silhouette score : 0.52)
- Validation avec l'equipe marketing sur la coherence metier

**Segments identifies** :

| Segment | Taille | Profil | Revenus annuels/client |
|---|---|---|---|
| **Hyper-Actifs Premium** | 8% | Tout digital, nombreuses transactions, hauts revenus | 680 EUR |
| **Affinite Investissement** | 12% | Epargne et placements prioritaires, faible consommation | 520 EUR |
| **Familles Equilibrees** | 22% | Depenses courantes elevees, multi-produits | 320 EUR |
| **Actifs Moderés** | 25% | Profil standard, peu d'engagement digital | 180 EUR |
| **Jeunes Entrants** | 15% | Anciennete < 3 ans, premiers produits | 120 EUR |
| **Dormants a Potentiel** | 11% | Anciens clients avec solde eleve mais peu d'activite | 95 EUR |
| **Risque Depart** | 7% | Recency elevee, tendance de diminution | 60 EUR |

**Actions par segment** :
- Hyper-Actifs Premium : programme ambassadeur, acces privileges, offres avant-premiere
- Affinite Investissement : campagne fonds d'investissement, advisory digital
- Dormants a Potentiel : programme de reactiver avec offres adaptes

**Resultats** :
- Taux d'engagement campagnes passe de 2.1% a 5.8% (+176%)
- Revenue par campagne augmente de 340% (ciblage plus precis)

---

## Cas 2 — A/B Testing pour une Fintech (Rigueur Statistique)

### Contexte

Application fintech de paiement entre particuliers. 4.2 millions d'utilisateurs actifs. Equipe produit voulant tester si l'ajout d'une animation de confirmation de virement augmenterait le taux d'adoption des virements recurrents (feature peu utilisee : 3.2% des utilisateurs actifs).

### Design de l'Experience

**Hypothese** : L'animation de confirmation (groupe B) augmentera le taux d'activation des virements recurrents de 3.2% a 3.7% (lift de +0.5 point, +15.6% relatif) dans les 14 jours suivant l'exposition.

**Calcul de la taille d'echantillon** :
- Taux baseline : 3.2%
- MDE : +0.5 point absolu
- Alpha : 5%, Puissance : 80%
- Taille requise par groupe : 42 800 utilisateurs
- Taille totale : 85 600 utilisateurs
- Avec 50 000 nouvelles sessions/jour eligibles → duree = 2 jours d'exposition minimale + 14 jours de suivi

**Randomisation** : Par user_id (hash mod 2), stable entre sessions.

### Analyse des Resultats

**Verification SRM** :
- Groupe A : 42 916 utilisateurs
- Groupe B : 42 684 utilisateurs
- Ratio observe : 50.1% vs 49.9% — pas de SRM (chi2 = 0.42, p = 0.52)

**Resultats primaires (14 jours)** :
- Groupe A : 1 381 activations (3.22%)
- Groupe B : 1 704 activations (3.99%)
- Lift absolu : +0.77 point
- Lift relatif : +23.9%
- p-value : 0.0003 (tres significatif)
- IC 95% : [+0.39% ; +1.15%]

**Resultats secondaires** :
- Nombre de virements recurrents crees/utilisateur : +18% en groupe B
- Montant moyen par virement : non significativement different (bonne nouvelle : pas de dilution)

**Decision** : Deploiement complet. Impact annuel estime : 280 000 utilisateurs supplementaires avec virements recurrents actives = +1.4 M EUR de revenus nets (commissions sur les virements).

**Lecon cle** : La taille d'echantillon avait ete calculee pour un MDE de 0.5 point, mais l'effet reel etait de 0.77 point — le test etait deja sur-puissant. Prochaine etape : calibrer les MDE sur les effets historiquement observes plutot que sur des hypotheses trop conservatives.

---

## Cas 3 — LTV Prediction pour un Service de Streaming (Modele BG/NBD)

### Contexte

Service de streaming musical avec 8 millions d'abonnes en Europe. Business model : abonnement mensuel (9.99 EUR) et annuel (89.99 EUR). Taux de churn mensuel : 5.8%. Objectif : calculer le LTV previsionnel de chaque utilisateur pour optimiser le budget d'acquisition et de retention.

### Implementation du Modele BG/NBD

**Donnees pre-parees** :
- Recency : nombre de mois depuis le dernier paiement
- Frequency : nombre de paiements (hors premier)
- T : anciennete du compte en mois
- Monetary : MRR moyen

**Calibration sur 24 mois de donnees historiques** :

```
Modele BG/NBD :
- r = 0.243 (heterogeneite de la frequence d'achat)
- alpha = 4.414 (echelle du temps entre achats)
- a = 0.793 (heterogeneite du taux de churn)
- b = 2.426 (echelle du processus geometrique de churn)

Modele Gamma-Gamma (valeur monetaire) :
- p = 6.25
- q = 3.74
- v = 15.45
```

**Validation** :
- Sur les 6 mois de holdout : MAPE du LTV cumule a 12 mois = 18%
- Accuracy de la prediction "actif ou non dans 6 mois" : 81% AUC

**LTV projete par segment** :

| Segment | LTV 12 mois | LTV 36 mois | Action |
|---|---|---|---|
| Abonnes annuels fidelises (>2 ans) | 180 EUR | 420 EUR | Retention premium |
| Abonnes mensuels actifs | 95 EUR | 190 EUR | Conversion annuel |
| Abonnes recents (<3 mois) | 45 EUR | 110 EUR | Onboarding optimise |
| Abonnes a risque | 25 EUR | 40 EUR | Offre de retention ciblee |

**Impact business** :
- Budget d'acquisition ajuste selon le LTV prevu (CPA max = LTV/3)
- 2.2 M EUR d'economies sur les campagnes d'acquisition mal ciblees
- Taux de conversion annuel augmente de 11% a 17% grace au ciblage sur les utilisateurs avec LTV prevu > 120 EUR

---

## Cas 4 — Uplift Modeling pour une Campagne de Retention Telecom

### Contexte

Operateur telecom avec 3.5 millions d'abonnes mobiles. Budget de retention : 8 M EUR/an pour des offres de fidelisation (reduction tarifaire, mise a niveau de forfait). Probleme : 60% du budget etait depense sur des "Sure Things" (clients qui restent de toute facon) ou des "Sleeping Dogs" (clients qui partent quand on les contacte).

### Mise en Oeuvre de l'Uplift Modeling

**Donnees disponibles** (historique de 18 mois de campagnes A/B) :
- Features clients (anciennete, forfait, usage data, appels, satisfaction)
- Indicateur de traitement : contacte ou non lors de la campagne
- Variable cible : churn dans les 60 jours

**Modele T-Learner** (deux modeles independants) :
- Modele mu1 : P(churn | traite, X) — sur le groupe traitement
- Modele mu0 : P(churn | non traite, X) — sur le groupe controle
- Uplift individual = mu0(x) - mu1(x) (reduction de churn due a l'action)

**Distribution des 4 types d'individus** :

| Type | Definition | % de la base | Action |
|---|---|---|---|
| **Persuadables** | Uplift > +5% | 18% | CIBLER en priorite |
| **Sure Things** | P(churn sans action) < 5% | 45% | NE PAS cibler |
| **Lost Causes** | P(churn) > 70%, uplift faible | 22% | NE PAS cibler |
| **Sleeping Dogs** | Uplift negatif (action augmente le churn) | 15% | EVITER ABSOLUMENT |

**Courbe de gains d'uplift** : En ciblant les 20% de clients avec le plus fort uplift positif, on capturait 68% de tout l'effet de retention atteignable (vs. 20% avec un ciblage aleatoire).

**Resultats de la campagne optimisee** :
- Budget cible sur les 18% de Persuadables (vs. 40% avant)
- Reduction du churn dans la population ciblee : -8.3 points
- ROI de la campagne : 4.2x (vs. 1.8x avant l'uplift modeling)
- Economies sur le budget : 3.1 M EUR (moins de Sure Things traites inutilement)

**Lecon principale** : L'uplift modeling n'est utile que si les actions ont des effets heterogenes (certains clients repondent, d'autres non). Si tous les clients repondent pareil, un modele de churn classique suffit. L'uplift est particulierement valoreux dans les campagnes d'incitation ou de retention.
