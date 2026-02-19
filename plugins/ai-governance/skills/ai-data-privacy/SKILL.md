---
name: ai-data-privacy
version: 1.0.0
description: >
  Use this skill when the user asks about "EU AI Act", "AI regulation", "AI compliance", "AI data governance", "model cards", "datasheets for datasets", "bias audit", "algorithmic audit", "AI transparency", "high-risk AI", "prohibited AI", "AI impact assessment", "FRIA", "AI Act conformity", "trustworthy AI certification", "ISO 42001", "NIST AI RMF", discusses AI governance frameworks, AI-specific data rights, or needs guidance on complying with AI regulations, documenting AI systems, and conducting bias audits.
---

# AI Data Privacy & Governance — EU AI Act, Model Cards & Bias Audits

## Overview

Le cadre reglementaire de l'IA est entre dans une phase d'applicabilite concrete. L'**EU AI Act** (Reglement (UE) 2024/1689), premier reglement mondial contraignant sur l'IA, s'applique progressivement depuis 2024 avec des obligations pleinement effectives en 2026. En parallele, la **gouvernance des donnees IA** — modeles de documentation, audits d'equite, droits sur les donnees d'entrainement — est devenue un imperatif operationnel.

**Pourquoi c'est distinct du RGPD** : Le RGPD protege les donnees personnelles ; l'EU AI Act reglemente les systemes d'IA eux-memes (leur developpement, leur deploiement, leur surveillance). Un meme projet peut etre soumis aux deux reglements simultanement.

**L'approche basee sur les risques** : L'EU AI Act classe les systemes IA selon leur niveau de risque — de l'IA interdite aux applications a risque minimal — et impose des obligations proportionnelles. Ne pas connaitre la classification de son IA est desormais un risque reglementaire.

**Perimetre** :
- EU AI Act : classification, obligations par risque, timeline de mise en conformite
- Model Cards et documentation IA : transparence sur les systemes deployes
- Audits de biais et d'equite : methodologies et metriques
- Gouvernance des donnees d'entrainement : origine, qualite, droits

## Core Principles

**1. Approche basee sur le risque.** Le niveau d'obligation est proportionnel au risque. Un filtre anti-spam IA n'a pas les memes contraintes qu'un systeme de selection d'embauche IA. Classifier ses systemes IA avant de concevoir la gouvernance.

**2. Transparence par defaut.** Les utilisateurs ont le droit de savoir quand ils interagissent avec un systeme IA, surtout pour les decisions qui les affectent. La transparence n'est pas optionnelle pour les IA a impact humain — c'est une obligation legale pour les systemes a risque eleve.

**3. Surveillance humaine (human oversight).** Pour les IA a risque eleve, un humain doit pouvoir comprendre les sorties, les contester et les neutraliser. L'autonomie totale de l'IA sur des decisions a impact humain est incompatible avec l'EU AI Act.

**4. Qualite et gouvernance des donnees d'entrainement.** Un modele n'est pas meilleur que ses donnees. Documenter l'origine, la composition, les biais connus et les mesures de mitigation des datasets d'entrainement. C'est une obligation pour les IA a risque eleve (Article 10).

**5. Robustesse, precision, cybersecurite.** Les systemes IA a risque eleve doivent etre precis, robustes aux perturbations et proteges contre les attaques adversariales. Tests de robustesse obligatoires avant deploiement.

**6. Accountability et documentation.** Tenir les registres de tests, les decisions de conception, les evaluations de conformite. Pour les IA a risque eleve : documentation technique complete obligatoire (Annexe IV de l'EU AI Act).

## EU AI Act — Classification et Obligations

### Les 4 niveaux de risque

**Risque inacceptable — INTERDIT (Article 5)** :
- Systemes de scoring social par les gouvernements
- Manipulation subliminale pour influencer le comportement
- Exploitation des vulnerabilites (age, handicap) pour influencer
- Identification biometrique en temps reel dans l'espace public (sauf exceptions securite nationale)
- IA pour predire des infractions sur base de profiling
- Reconnaissance des emotions au travail ou en education (sauf exceptions medicales)
- Bases de donnees de reconnaissance faciale par scraping non cible

**Risque eleve — OBLIGATIONS STRICTES (Annexes III et IV)** :

Categories de systemes IA a risque eleve :
- Infrastructure critique (transport, eau, energie, finance)
- Education et formation (acces, notation)
- Emploi et gestion RH (CV screening, promotion, licenciement)
- Acces aux services essentiels (credit scoring, assurance, services publics)
- Application de la loi
- Migration et asile
- Administration de la justice
- Dispositifs medicaux avec composante IA

Obligations pour les fournisseurs :
- Systeme de gestion de la qualite (Article 17)
- Documentation technique (Article 11, Annexe IV)
- Gestion des risques tout au long du cycle de vie (Article 9)
- Gouvernance des donnees (Article 10)
- Transparence et information des utilisateurs (Article 13)
- Surveillance humaine (Article 14)
- Precision, robustesse, cybersecurite (Article 15)
- Enregistrement dans la base de donnees EU (Article 71)
- Evaluation de la conformite (Article 43) — auto-evaluation ou tierce partie selon cas
- Declaration de conformite UE + marquage CE

**Risque limite — OBLIGATIONS DE TRANSPARENCE** :
- Chatbots : informer que l'utilisateur interagit avec une IA
- Deepfakes : labellisation obligatoire du contenu genere par IA
- IA d'emotion / biometrique a categorie limitee : obligations de notification

**Risque minimal — PAS D'OBLIGATION SPECIFIQUE** :
- Filtres spam, jeux video, recommandation de contenus, IA d'aide a la decision sans impact humain direct

### Timeline d'application (a partir de la date d'entree en vigueur — aout 2024)

| Periode | Obligations en vigueur |
|---|---|
| 6 mois (fev. 2025) | IA interdites — prohibitions applicables |
| 12 mois (aout 2025) | Modeles IA a usage general (GPAI) — regles applicables |
| 24 mois (aout 2026) | IA a risque eleve — toutes obligations applicables |
| 36 mois (aout 2027) | Systemes existants mis sur marche avant aout 2026 |

### Modeles IA a Usage General (GPAI — Article 51)

Systemes comme GPT-4, Claude, Gemini. Obligations :
- Documentation technique et politique de copyright
- Politique d'utilisation acceptable
- Acces aux parametres du modele pour les fournisseurs en aval
- Pour les modeles a "risque systemique" (puissance de calcul > 10^25 FLOPS) : obligations additionnelles (evaluation adversariale, reporting incidents, cybersecurite)

## Model Cards — Documentation des Systemes IA

Les model cards (Mitchell et al., 2019) sont des documents standardises accompagnant chaque modele. Ils deviennent une obligation de fait pour les IA a risque eleve (Article 11 EU AI Act).

### Structure d'une Model Card

```markdown
# Model Card — [Nom du Modele]

## Informations Generales
- **Version** : 1.2.0
- **Date** : 2025-03
- **Type** : Classification binaire (churn prediction)
- **Framework** : LightGBM 4.1
- **Fournisseur** : [Entreprise]

## Utilisation Prevue
- **Cas d'usage principal** : Prediction du risque de churn client B2B
- **Utilisateurs prevus** : Equipes Customer Success
- **Hors scope** : Ne pas utiliser pour des decisions de credit ou de scoring social

## Donnees d'Entrainement
- **Source** : CRM interne, 36 mois historique
- **Volume** : 145 000 observations
- **Periode** : Janvier 2022 - Decembre 2024
- **Biais connus** : Sur-representation des entreprises > 100 salaries (62%)
- **Donnees sensibles** : Aucune donnee personnelle directement identifiable

## Performances du Modele
| Metrique | Valeur | Population |
|---|---|---|
| AUC-ROC | 0.84 | Test set (out-of-time) |
| Precision @top20% | 68% | Decile de score le plus eleve |
| Recall @top20% | 62% | Decile de score le plus eleve |

## Performances par Sous-groupe
| Segment | AUC | Commentaire |
|---|---|---|
| PME (< 50 salaries) | 0.79 | Performance reduite, moins de donnees |
| ETI (50-500 sal.) | 0.87 | Performance nominale |
| Grandes entreprises (> 500) | 0.91 | Meilleure performance |

## Facteurs de Risque et Limitations
- Performance degradee sur les clients avec < 6 mois d'historique
- Sensible aux changements de comportement post-Covid (drift possible)
- Ne pas utiliser seul : doit etre combine avec l'expertise du CS manager

## Evaluation Ethique
- Pas de variables protegees directement utilisees
- Test de biais realise sur : taille entreprise, secteur, localisation — aucun ecart significatif > 5 points
- Revue humaine obligatoire pour les scores > 0.8

## Surveillance et Maintenance
- Monitoring mensuel de la distribution des scores (PSI)
- Retrainement trimestriel ou si AUC < 0.75 en production
- Responsable : [Nom, Contact]
- Prochaine revue : [Date]
```

## Audits de Biais — Methodologie

### Etape 1 — Definition des groupes proteges

Identifier les attributs susceptibles de creer des discriminations : age, genre, origine ethnique, handicap, localisation, niveau d'etude. Verifier que ces attributs (ou leurs proxies) ne sont pas dans les features ou ne creent pas d'ecart systematique de predictions.

### Etape 2 — Metriques d'equite (Fairness Metrics)

| Metrique | Definition | Quand l'utiliser |
|---|---|---|
| **Demographic Parity** | P(y=1 \| groupe A) = P(y=1 \| groupe B) | Decisions d'allocation (credit, emploi) |
| **Equal Opportunity** | TPR egal entre groupes | Quand le recall est critique (sante, justice) |
| **Equalized Odds** | TPR et FPR egaux entre groupes | Le plus strict — utiliser si les deux erreurs sont couteuses |
| **Predictive Parity** | Precision egale entre groupes | Quand on veut que le meme score signifie la meme chose |
| **Individual Fairness** | Individus similaires traites similairement | Cas ou comparaison individuelle possible |

**Attention** : Ces metriques ne peuvent pas toutes etre satisfaites simultanement (theoreme de Chouldechova). Choisir la metrique alignee avec l'objectif metier et ethical.

### Etape 3 — Outils d'audit

```python
# Exemple avec Fairlearn (Microsoft)
from fairlearn.metrics import MetricFrame, selection_rate, true_positive_rate

metric_frame = MetricFrame(
    metrics={
        'selection_rate': selection_rate,
        'true_positive_rate': true_positive_rate,
    },
    y_true=y_test,
    y_pred=y_pred,
    sensitive_features=X_test['gender']
)

# Visualisation des ecarts
metric_frame.by_group.plot.bar(
    subplots=True, layout=(2, 1), figsize=(12, 8)
)
```

Autres outils : IBM AI Fairness 360 (AIF360), Google What-If Tool, Aequitas (pour les systemes de justice predictive).

### Etape 4 — Mitigation

- **Pre-processing** : Reequilibrage du dataset, reweighting des exemples
- **In-processing** : Ajout d'une contrainte d'equite dans la fonction de perte
- **Post-processing** : Seuils de decision differencies par groupe (Equalized Odds Post-processing)

### Rapport d'Audit de Biais (structure)
```
1. Perimetre : modele audite, version, date, population concernee
2. Groupes proteges analyses
3. Metrique d'equite choisie et justification
4. Resultats par groupe
5. Ecarts identifies et significativite statistique
6. Mesures de mitigation recommandees
7. Residuels acceptes et justification ethique
8. Frequence de re-audit recommandee
```

## Gouvernance des Donnees d'Entrainement

### Datasheets for Datasets (Gebru et al.)

Complement aux model cards : documentation du dataset lui-meme.

**Sections cles** :
- **Motivation** : Pourquoi ce dataset existe ? Qui l'a financé ?
- **Composition** : Types de donnees, volume, representativite
- **Processus de collecte** : Sources, periode, methode d'echantillonnage
- **Preprocessing** : Nettoyage, transformations, filtres appliques
- **Utilisations recommandees** : Taches adaptees et inadaptees
- **Distribution** : Licence, restrictions d'usage
- **Maintenance** : Versioning, mises a jour, contacts

### Droits sur les donnees d'entrainement (enjeux 2024-2026)
- **Droit d'auteur** : le debat legal est ouvert (The New York Times vs OpenAI, Stability AI)
- **RGPD et donnees d'entrainement** : Si le modele a ete entraine sur des donnees personnelles, des droits s'appliquent (droit a l'effacement → droit au "machine unlearning")
- **Provenance et watermarking** : Frameworks emergents pour tracer l'origine des donnees (C2PA, Coalition for Content Provenance)

## Maturity Model — AI Data Governance

| Niveau | Caracteristique |
|---|---|
| **1 — Invisible** | Aucune documentation sur les modeles en production, pas d'audit |
| **2 — Ad hoc** | Model cards ponctuelles, pas de processus systematique |
| **3 — Structure** | Model cards standardisees, audit de biais sur les modeles a impact |
| **4 — Integre** | Gouvernance IA integree au MLOps, monitoring d'equite continu |
| **5 — Certifie** | Conformite EU AI Act documentee, ISO 42001, audits tiers periodiques |

## Frameworks Complementaires

**NIST AI Risk Management Framework (AI RMF 1.0)** : cadre volontaire americain en 4 fonctions — Govern, Map, Measure, Manage. Tres utilise par les organisations internationales.

**ISO/IEC 42001:2023** : premier standard de systeme de management de l'IA. Certifiable (comme ISO 27001 pour la securite). Couvre la gouvernance IA, la gestion des risques, la transparence.

**FRIA — Fundamental Rights Impact Assessment** : evaluation de l'impact sur les droits fondamentaux, recommandee par l'EU AI Act pour les deploiements publics.

## Limites et Points de Vigilance

- L'EU AI Act est jeune : les normes harmonisees (EN) sont encore en cours d'elaboration (CEN/CENELEC). Les obligations exactes de "conformite" pour les IA a risque eleve seront precisees par ces normes.
- La classification "risque eleve" n'est pas toujours evidente : consulter un juriste specialise avant de conclure a une classification
- Le machine unlearning est techniquement difficile : les obligations RGPD de droit a l'effacement appliquees aux modeles ML sont complexes a implementer en pratique
- Les metriques d'equite ne capturent pas tous les biais : le biais algorithmique peut exister meme si les metriques formelles sont satisfaites (biais contextuel, historique)
- Ne pas confondre transparence et explicabilite : un modele peut etre transparent (on sait ce qu'il fait) sans etre explicable (on ne comprend pas pourquoi il prend telle decision)
