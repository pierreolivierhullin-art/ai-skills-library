---
name: risk-management
description: This skill should be used when the user asks about "enterprise risk management", "business continuity planning", "compliance program", "crisis management", "risk assessment", "gestion des risques", "ERM", "plan de continuité d'activité", "PCA", "PRA", "plan de reprise", "gestion de crise", "évaluation des risques", "cartographie des risques", "risk mapping", "COSO", "ISO 31000", "risk governance", "gouvernance des risques", "anti-corruption", "Sapin II", "FCPA", "UK Bribery Act", "disaster recovery", "BIA", "business impact analysis", "risk appetite", "appétit au risque", "risk register", "matrice de risques", "contrôle interne", "internal control", "audit des risques", discusses COSO, ISO 31000, or needs guidance on risk governance, anti-corruption compliance, or disaster recovery planning.
version: 1.0.0
---

# Enterprise Risk Management

## Overview

Ce skill couvre l'ensemble de la gestion des risques d'entreprise (ERM) : gouvernance du risque, identification et evaluation des risques, conformite reglementaire, continuite d'activite et transfert de risques. Il synthetise les meilleures pratiques 2024-2026 incluant les cadres COSO ERM et ISO 31000:2018, les exigences Sapin II, FCPA, RGPD, la directive europeenne sur les lanceurs d'alerte, et les approches modernes de BCP/DRP integrant la cyber-resilience. Utiliser ce skill comme reference systematique pour toute decision touchant a la maitrise des risques dans une organisation.

Note : ce skill couvre la gouvernance du risque d'entreprise. L'implementation technique de la securite applicative (authentification, chiffrement, OWASP) releve du skill "Auth & Security" dans Code Development.

## When This Skill Applies

Activer ce skill dans les situations suivantes :

- Mise en place ou amelioration d'un cadre ERM (COSO, ISO 31000)
- Definition de l'appetence au risque (risk appetite) et des tolerances
- Creation ou mise a jour d'un registre des risques
- Conduite d'evaluations de risques (qualitatives, quantitatives, semi-quantitatives)
- Elaboration de cartographies de risques et heat maps
- Definition de KRIs (Key Risk Indicators) et tableaux de bord de risque
- Mise en conformite reglementaire (Sapin II, FCPA, UK Bribery Act, RGPD, CCPA)
- Deploiement d'un dispositif d'alerte professionnelle (whistleblowing)
- Elaboration ou test d'un Plan de Continuite d'Activite (PCA/BCP)
- Conception d'un Plan de Reprise d'Activite (PRA/DRP)
- Gestion de crise et communication de crise
- Structuration d'un programme d'assurance et transfert de risques
- Analyse de scenarios et stress testing
- Identification et suivi des risques emergents

## Core Principles

### 1. Tone at the Top (Culture du risque)

La gestion des risques commence au plus haut niveau de l'organisation. Le conseil d'administration et la direction generale doivent porter la culture du risque, definir l'appetence au risque et demontrer par l'exemple que la gestion proactive des risques est une priorite strategique. Sans engagement visible de la direction, aucun dispositif ERM ne produit de resultats durables.

### 2. Integration dans la strategie

Ne jamais traiter la gestion des risques comme une activite isolee ou un exercice de conformite. Integrer l'analyse des risques dans chaque decision strategique : lancement de produit, expansion geographique, fusion-acquisition, transformation digitale. Le risque n'est pas un frein a la strategie mais un accelerateur de decisions eclairees.

### 3. Approche holistique et transversale

Adopter une vision a 360 degres couvrant toutes les categories de risques : strategiques, operationnels, financiers, de conformite, reputationnels, cyber, climatiques. Briser les silos entre les fonctions (finance, juridique, IT, operations) pour assurer une comprehension globale du profil de risque.

### 4. Proportionnalite et pragmatisme

Calibrer le dispositif ERM a la taille, la complexite et le profil de risque de l'organisation. Une ETI n'a pas besoin du meme appareil qu'un groupe du CAC 40. Privilegier l'efficacite operationnelle : un registre de risques vivant et exploite vaut mieux qu'un referentiel exhaustif mais ignore.

### 5. Amelioration continue

Le profil de risque evolue en permanence. Revoir le dispositif ERM au minimum annuellement, et apres chaque incident majeur, changement strategique ou evolution reglementaire significative. Tirer les lecons de chaque crise et les integrer dans les processus.

## Key Frameworks & Methods

### Cadres de reference ERM

| Cadre | Portee | Forces | Cas d'usage |
|-------|--------|--------|-------------|
| **COSO ERM (2017)** | Strategie et performance | Integration strategie-risque, 5 composantes, 20 principes | Grandes entreprises, reporting integre |
| **ISO 31000:2018** | Management du risque universel | Principes, cadre, processus, toute organisation | Universel, certification possible |
| **ISO 22301:2019** | Continuite d'activite | SMCA structure, certification | BCP/DRP formalise |
| **FERMA Risk Management Standard** | Gouvernance du risque europeenne | Approche pragmatique, taille intermediaire | ETI europeennes |
| **IIA Three Lines Model (2020)** | Roles et responsabilites | Clarte des lignes de defense | Audit interne, gouvernance |

### Methodologies d'evaluation des risques

| Methode | Type | Complexite | Utilisation |
|---------|------|-----------|-------------|
| Matrice probabilite-impact | Qualitative | Faible | Screening initial, communication |
| AMDEC/FMEA | Semi-quantitative | Moyenne | Processus industriels, IT |
| Bow-tie analysis | Semi-quantitative | Moyenne | Risques complexes, barriere de prevention/mitigation |
| Monte Carlo simulation | Quantitative | Haute | Risques financiers, planning |
| Value at Risk (VaR) | Quantitative | Haute | Risques financiers, portefeuilles |
| Scenario analysis | Qualitative/Quantitative | Moyenne-Haute | Risques strategiques, stress testing |

### Reglementation cle

| Regulation | Juridiction | Perimetre | Sanction maximale |
|-----------|------------|-----------|-------------------|
| **Sapin II** | France | Anti-corruption, trafic d'influence | 1M EUR personne physique, 5M EUR personne morale |
| **FCPA** | USA (extraterritorial) | Anti-corruption internationale | Illimite (amendes, prison) |
| **UK Bribery Act** | UK (extraterritorial) | Anti-corruption | Illimite |
| **RGPD/GDPR** | UE | Protection des donnees | 4% CA mondial ou 20M EUR |
| **CCPA/CPRA** | Californie | Protection des donnees | $7,500/violation intentionnelle |
| **Directive 2019/1937** | UE | Protection des lanceurs d'alerte | Transposition nationale variable |
| **DORA** | UE | Resilience operationnelle numerique (finance) | Sanctions administratives |
| **NIS2** | UE | Cybersecurite des entites essentielles | 10M EUR ou 2% CA mondial |

## Decision Guide

### Choisir un cadre ERM

```
Organisation > 5 000 salaries, cotee en bourse ?
  -> COSO ERM comme cadre principal
  -> ISO 31000 comme complement methodologique
  -> Three Lines Model pour la gouvernance

ETI (250-5 000 salaries) ?
  -> ISO 31000 comme cadre principal (plus souple)
  -> FERMA comme guide pratique
  -> Adapter la complexite au profil de risque

PME (< 250 salaries) ?
  -> ISO 31000 simplifie (principes + processus)
  -> Focus sur les 5-10 risques critiques
  -> Registre de risques leger et operationnel

Secteur financier ?
  -> COSO ERM + Bale III/IV (risques bancaires)
  -> Solvabilite II (assurance)
  -> DORA pour la resilience operationnelle numerique

Secteur industriel ?
  -> ISO 31000 + ISO 45001 (sante-securite)
  -> AMDEC/FMEA pour les risques processus
  -> ISO 14001 pour les risques environnementaux
```

### Structurer un programme de conformite

```
Obligations anti-corruption ?
  -> Cartographie des risques de corruption (Sapin II art. 17)
  -> Code de conduite et formation
  -> Dispositif d'alerte interne (whistleblowing)
  -> Due diligence tiers (KYC, sanctions screening)
  -> Controles comptables et audit interne

Obligations donnees personnelles ?
  -> Registre des traitements (RGPD art. 30)
  -> AIPD/DPIA pour les traitements a risque
  -> DPO designe (si obligatoire)
  -> Procedures droits des personnes
  -> Gestion des violations de donnees (72h)

Obligations de continuite d'activite ?
  -> BIA (Business Impact Analysis) prealable
  -> PCA/BCP formalise et documente
  -> PRA/DRP pour les systemes critiques
  -> Tests reguliers (tabletop, simulation, full-scale)
  -> RTO/RPO definis par processus critique
```

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **Risk Appetite Framework** : Formaliser l'appetence au risque a trois niveaux : strategique (conseil d'administration), tactique (direction), operationnel (management). Decliner en tolerances mesurables par categorie de risque. Reviser annuellement et apres chaque evenement significatif.

- **Three Lines Model** : Structurer la gouvernance du risque selon les trois lignes de defense : 1re ligne (management operationnel, proprietaires du risque), 2e ligne (fonctions risk management et compliance), 3e ligne (audit interne, assurance independante). Chaque ligne a des responsabilites claires et complementaires.

- **Living Risk Register** : Maintenir un registre de risques vivant, mis a jour en continu, avec des proprietaires designes et des revues trimestrielles. Utiliser des KRIs automatises pour alimenter le registre en temps reel. Un registre mis a jour une fois par an est obsolete des sa publication.

- **Crisis Management Framework** : Deployer une structure de gestion de crise a trois niveaux : cellule de crise strategique (direction), cellule de crise operationnelle (experts metiers), equipes d'intervention (terrain). Definir les criteres d'activation, les canaux de communication et les delegations de pouvoir a l'avance.

- **Integrated GRC** : Integrer Governance, Risk et Compliance dans une plateforme unique pour eliminer les doublons, assurer la coherence et permettre un reporting consolide. Les silos GRC sont un anti-pattern majeur.

### Anti-patterns a eviter

- **Risk Theatre** : Produire une cartographie de risques elaboree pour satisfaire le regulateur ou le conseil d'administration sans la traduire en actions concretes. Si les risques identifies ne generent pas de plans d'action suivis, l'exercice est un theatre.

- **Compliance-Only Mindset** : Reduire l'ERM a la conformite reglementaire. La conformite est un minimum legal, pas une gestion du risque. Les risques strategiques, operationnels et reputationnels ne sont couverts par aucune reglementation specifique.

- **Risques figees** : Publier un registre de risques annuel et ne pas le reviser entre deux exercices. Le profil de risque change en permanence. Un risque emergent (pandemie, conflit geopolitique, disruption technologique) peut bouleverser le classement en quelques jours.

- **Over-Insurance / Under-Insurance** : Souscrire des assurances sans BIA prealable conduit a des couvertures inadaptees. Realiser d'abord le BIA, quantifier les impacts potentiels, puis structurer le programme d'assurance en consequence.

- **BCP non teste** : Un PCA qui n'a jamais ete teste est un document, pas un plan. Tester au minimum annuellement par tabletop exercise. Simuler au moins une crise majeure tous les deux ans. Documenter les retours d'experience et mettre a jour le plan.

## Implementation Workflow

### Phase 1 : Fondations ERM

1. Obtenir le sponsorship de la direction generale et du conseil d'administration
2. Definir l'appetence au risque et les tolerances par categorie
3. Adopter un cadre de reference (COSO ERM ou ISO 31000)
4. Nommer un Chief Risk Officer ou un responsable ERM
5. Constituer le comite des risques avec representation pluridisciplinaire
6. Former les equipes aux principes de la gestion des risques

### Phase 2 : Identification et evaluation

1. Realiser l'inventaire exhaustif des risques (ateliers, interviews, historique)
2. Structurer la taxonomie de risques adaptee a l'organisation
3. Evaluer chaque risque (probabilite, impact, vitesse de survenance)
4. Construire la heat map et identifier les risques prioritaires
5. Definir les KRIs et leurs seuils d'alerte
6. Lancer les premieres analyses de scenarios sur les risques majeurs

### Phase 3 : Conformite et gouvernance

1. Cartographier les obligations reglementaires applicables
2. Deployer le programme anti-corruption (si applicable : Sapin II, FCPA)
3. Verifier la conformite RGPD (registre, AIPD, DPO)
4. Mettre en place le dispositif d'alerte professionnelle
5. Structurer les controles internes et le monitoring de conformite
6. Planifier les audits internes et externes

### Phase 4 : Continuite d'activite et transfert

1. Conduire le BIA sur les processus critiques
2. Definir les RTO/RPO par processus et systeme critique
3. Elaborer le PCA/BCP et le PRA/DRP
4. Structurer le programme d'assurance (base sur le BIA)
5. Tester les plans (tabletop, simulation, full-scale)
6. Former les equipes de gestion de crise

### Phase 5 : Amelioration continue

1. Mettre en place le reporting periodique au comite des risques
2. Automatiser les KRIs et le tableau de bord de risque
3. Conduire des revues post-incident systematiques
4. Integrer les risques emergents dans la veille continue
5. Benchmarker le dispositif ERM avec les pairs sectoriels
6. Evoluer vers une plateforme GRC integree


## Skills connexes

| Skill | Lien |
|---|---|
| Juridique | `entreprise:juridique` — Conformité réglementaire et compliance |
| Finance | `entreprise:finance` — Risques financiers et audit |
| IT Systèmes | `entreprise:it-systemes` — PCA/PRA et résilience IT |
| RSE-ESG | `entreprise:rse-esg` — Risques ESG et climatiques |
| AI Risk | `ai-governance:ai-risk` — Risques spécifiques à l'intelligence artificielle |

## Additional Resources

Consulter les fichiers de reference pour un approfondissement detaille :

- **[ERM Frameworks](./references/erm-frameworks.md)** : COSO ERM 2017 (composantes et principes detailles), ISO 31000:2018 (principes, cadre, processus), risk appetite framework, gouvernance du risque, Three Lines Model, comite des risques, culture du risque, maturite ERM.

- **[Risk Assessment](./references/risk-assessment.md)** : Registre de risques et taxonomie, methodes d'evaluation (qualitative, quantitative, semi-quantitative), heat maps et matrices de risques, KRIs, risques emergents, analyse de scenarios et stress testing, outils GRC.

- **[Compliance & Regulatory](./references/compliance-regulatory.md)** : Programmes de conformite, anti-corruption (Sapin II, FCPA, UK Bribery Act), protection des donnees (RGPD, CCPA), lanceurs d'alerte (directive 2019/1937), monitoring de conformite, due diligence tiers.

- **[BCP & Insurance](./references/bcp-insurance.md)** : Business Impact Analysis, PCA/BCP, PRA/DRP, gestion de crise, tests de continuite (tabletop, simulation, full-scale), RTO/RPO, programmes d'assurance, transfert de risques, captives, D&O/cyber/property insurance.
