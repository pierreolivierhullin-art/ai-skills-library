---
name: regulatory
description: This skill should be used when the user asks about "MiFID II", "SEC regulations", "trading compliance", "tax reporting", "pattern day trader", "wash sale rules", "insider trading", "FINRA", "EMIR", "MAR", "best execution", "KYC", "AML", "réglementation financière", "conformité trading", "déclaration fiscale", "fiscalité du trading", "délit d'initié", "meilleure exécution", "connaissance client", "lutte anti-blanchiment", "AMF", "Autorité des marchés financiers", "régulateur", "ESMA", "Dodd-Frank", "Basel III", "Bâle III", "suitability", "appropriateness", "transaction reporting", "déclaration de transactions", "market abuse", "abus de marché", "short selling regulations", "réglementation vente à découvert", "UCITS", "AIFMD", "PRIIPs", "flat tax", "PFU", "prélèvement forfaitaire unique", "plus-values", "capital gains tax", or needs guidance on financial market regulations, compliance obligations, and tax reporting for trading.
version: 1.2.0
last_updated: 2026-02
---

# Financial Market Regulations & Compliance

## Overview

Ce skill couvre l'ensemble du cadre reglementaire applicable aux marches financiers, cote europeen (MiFID II/MiFIR, EMIR, MAR, PRIIPs, SFDR) et americain (SEC, FINRA, Reg NMS, Reg T). Il synthetise les obligations de reporting, la fiscalite des operations de marche, les regles de conformite operationnelle (best execution, AML/KYC, conflits d'interets) et les obligations de transparence. Utiliser ce skill comme reference systematique pour toute question touchant a la reglementation, la conformite et la fiscalite des marches financiers.

This skill covers the full regulatory framework applicable to financial markets, on both the European side (MiFID II/MiFIR, EMIR, MAR, PRIIPs, SFDR) and the US side (SEC, FINRA, Reg NMS, Reg T). Use it as the authoritative reference for any question related to regulation, compliance, and taxation of financial market activities.

## When This Skill Applies

Activer ce skill dans les situations suivantes / Activate this skill in the following situations:

- Question sur la reglementation MiFID II/MiFIR, EMIR, MAR, PRIIPs, ou SFDR
- Question about SEC regulations, FINRA rules, Reg NMS, or Reg T margin requirements
- Interrogation sur les regles de Pattern Day Trader (PDT) ou les exigences de capital minimum
- Question sur les wash sale rules, leur fenetre de 30 jours et leurs implications fiscales
- Guidance on insider trading prohibitions (Section 10b-5, MAR Article 14)
- Obligations de transaction reporting, position reporting, ou declarations 13F
- Question de fiscalite : plus-values, IFU, formulaire 2074, Schedule D, Form 8949
- FATCA, CRS, ou obligations d'echange automatique d'informations fiscales
- Best execution obligations, order handling, pre/post-trade transparency
- Suitability, appropriateness, ou product governance (target market)
- AML/KYC pour les comptes de trading, beneficial ownership, PEP screening
- Conflicts of interest, personal account dealing, record keeping obligations
- PRIIPs KID (Key Information Document) ou SFDR sustainability disclosures

## Core Principles

### 1. Investor Protection (Protection des investisseurs)

Placer la protection de l'investisseur au centre de toute decision reglementaire. Appliquer les regles de suitability et d'appropriateness avant toute recommandation. Assurer la transparence sur les couts, les risques et les conflits d'interets. Les obligations d'information priment sur les interets commerciaux.

Place investor protection at the center of every regulatory decision. Apply suitability and appropriateness rules before any recommendation. Ensure transparency on costs, risks, and conflicts of interest. Disclosure obligations prevail over commercial interests.

### 2. Market Integrity (Integrite des marches)

Maintenir des marches justes, ordonnees et transparents. Interdire toute forme de manipulation de marche, d'abus de marche (insider dealing, unlawful disclosure) et de pratiques deloyales. Declarer toute transaction suspecte (STOR) sans delai. Respecter les regimes de transparence pre- et post-negociation.

Maintain fair, orderly, and transparent markets. Prohibit all forms of market manipulation, market abuse (insider dealing, unlawful disclosure), and unfair practices. Report any suspicious transaction (STOR) without delay.

### 3. Systemic Risk Mitigation (Attenuation du risque systemique)

Respecter les obligations de clearing, de margining et de reporting sur les derives (EMIR). Declarer les positions au-dela des seuils reglementaires. Implementer les controles de risque pre-trade et post-trade. Surveiller les concentrations de positions et les expositions de contrepartie.

Comply with clearing, margining, and reporting obligations on derivatives (EMIR). Report positions beyond regulatory thresholds. Implement pre-trade and post-trade risk controls.

### 4. Regulatory Consistency (Coherence reglementaire)

Appliquer de maniere coherente les reglementations entre juridictions. Identifier les chevauchements et les conflits entre regimes (EU vs US). Adopter le standard le plus strict en cas de double soumission. Maintenir une veille reglementaire active et mettre a jour les procedures en continu.

Apply regulations consistently across jurisdictions. Identify overlaps and conflicts between regimes (EU vs US). Adopt the stricter standard when dual-regulated.

### 5. Proportionality & Documentation (Proportionnalite et documentation)

Adapter l'intensite des controles a la taille, la complexite et le profil de risque de l'activite. Documenter toutes les decisions, justifications et evaluations. Conserver les enregistrements conformement aux durees reglementaires (5 ans MiFID II, 6 ans FINRA). Rendre l'audit trail complet et accessible.

Scale control intensity to the size, complexity, and risk profile of the activity. Document all decisions, justifications, and assessments. Retain records per regulatory durations.

## Key Frameworks & Regulatory Architecture

### European Union Regulatory Stack

| Regulation | Scope | Autorite | Key Obligations |
|-----------|-------|----------|----------------|
| **MiFID II / MiFIR** | Marches d'instruments financiers | ESMA / NCAs | Autorisation, best execution, transparency, reporting |
| **EMIR (Refit)** | Derives OTC | ESMA / NCAs | Clearing, margining, trade reporting |
| **MAR** | Abus de marche | ESMA / NCAs | Insider dealing, manipulation, PDMR, STORs |
| **PRIIPs** | Produits packages pour retail | ESMA / NCAs | KID (Key Information Document) obligatoire |
| **SFDR** | Finance durable | ESMA / NCAs | Classifications Article 6/8/9, PAI disclosure |

### United States Regulatory Stack

| Regulation | Scope | Autorite | Key Obligations |
|-----------|-------|----------|----------------|
| **Securities Exchange Act** | Marches de titres | SEC | Registration, reporting, anti-fraud (10b-5) |
| **Reg NMS** | Structure de marche | SEC | Order protection, access, sub-penny |
| **Reg T** | Marge | Federal Reserve / FINRA | 50% initial margin, maintenance margin |
| **PDT Rule** | Day trading retail | FINRA | Minimum equity $25,000 |
| **Wash Sale Rule** | Fiscalite | IRS / SEC | 30-day window, loss disallowance |
| **FINRA Rules** | Broker-dealers | FINRA | Suitability (2111), best execution (5310) |

## Decision Guide

### Identifier le regime applicable

```
L'activite est exercee dans l'UE ou porte sur des instruments EU ?
  -> Appliquer MiFID II/MiFIR comme cadre principal
  -> Verifier EMIR si derives impliques
  -> Verifier MAR pour les obligations anti-abus de marche
  -> Verifier PRIIPs si distribution de produits packages a des retail
  -> Verifier SFDR si le produit fait reference a la durabilite

The activity is conducted in the US or involves US securities ?
  -> Apply Securities Exchange Act / Reg NMS as primary framework
  -> Check FINRA rules if broker-dealer involved
  -> Check Reg T for margin requirements
  -> Check PDT rule if day trading retail account
  -> Check wash sale rule for tax-loss harvesting strategies

L'activite est cross-border EU/US ?
  -> Appliquer les deux regimes / Apply both regimes
  -> Verifier les equivalence decisions et exemptions
  -> Adopter le standard le plus strict / Adopt the stricter standard
  -> Verifier les obligations FATCA et CRS
```

### Identifier les obligations de reporting

```
Transaction sur instruments financiers EU ?
  -> Transaction reporting sous MiFIR Art. 26 (J+1, vers NCA)
  -> Verifier si position reporting applicable (seuils Art. 57 MiFID II)
  -> Post-trade transparency (RTS 1 equity, RTS 2 non-equity)

Trade in US securities ?
  -> Trade reporting via FINRA (TRF, ORF, ADF)
  -> Check 13F filing if institutional manager > $100M
  -> Check 13D/13G if > 5% beneficial ownership
  -> Form 4 for insiders (Section 16)

Derivative trade (OTC or ETD) ?
  -> EMIR reporting to Trade Repository (EU)
  -> CFTC/SEC swap reporting (US)
  -> Position limits compliance check
```

### Determiner les obligations fiscales

```
Resident fiscal francais / French tax resident ?
  -> Plus-values mobilieres : PFU 30% (12.8% IR + 17.2% PS) ou bareme progressif
  -> IFU recu du courtier, pre-rempli declaration
  -> Formulaire 2074 si plus-values complexes (SRD, options, derives)
  -> Comptes a l'etranger : declaration 3916 obligatoire

US taxpayer ?
  -> Schedule D + Form 8949 for capital gains/losses
  -> Short-term (< 1 year) taxed as ordinary income
  -> Long-term (>= 1 year) preferential rates (0%, 15%, 20%)
  -> Wash sale rule: disallowed losses added to cost basis
  -> Mark-to-market election (Section 475(f)) for active traders
```

## Common Patterns & Anti-Patterns

### Patterns recommandes / Recommended patterns

- **Compliance-by-Design** : Integrer les controles de conformite des la conception du systeme de trading ou de la strategie d'investissement. Ne pas traiter la conformite comme un ajout post-implementation. Embed compliance controls from the design phase of any trading system or investment strategy.

- **Three Lines of Defense** : Appliquer le modele a trois lignes : (1) front office / business controles les risques operationnels, (2) compliance et risk management fournissent un cadre et une surveillance, (3) audit interne fournit une assurance independante. Apply the three lines model rigorously.

- **Automated Surveillance** : Automatiser la detection des abus de marche (wash trading, spoofing, layering, insider patterns) via des systemes de surveillance en temps reel. Generer des alertes parametrables avec escalation. Automate market abuse detection with real-time surveillance systems.

- **Regulatory Change Management** : Maintenir un processus formel de veille reglementaire. Evaluer l'impact de chaque nouvelle reglementation sur les processus existants. Documenter les gap analyses et les plans de remediation. Maintain a formal regulatory watch process.

- **Pre-Trade Compliance Checks** : Implementer des controles pre-trade automatises : limites de position, concentration sectorielle, restricted lists (insiders, PDMR), sanctions screening, suitability checks. Bloquer l'ordre si un controle echoue. Implement automated pre-trade checks.

### Anti-patterns a eviter / Anti-patterns to avoid

- **Regulatory Arbitrage Abusif** : Ne pas exploiter les differences entre juridictions pour contourner les obligations. Les regulateurs cooperent activement (ESMA-SEC MoUs, IOSCO MMoU). Le risque reputationnel et les sanctions depassent largement les gains potentiels.

- **Compliance Retrospective** : Ne pas attendre un controle ou une sanction pour mettre en place les controles. Les regulateurs appliquent des sanctions aggravees pour defaut d'organisation. Do not wait for an enforcement action to implement controls.

- **Over-Reliance on Disclaimers** : Les disclaimers et les terms & conditions ne remplacent pas les obligations reglementaires de suitability, d'appropriateness et de best execution. Un disclaimer ne protege pas contre une sanction pour mis-selling.

- **Manual-Only Compliance** : Ne pas s'appuyer uniquement sur des controles manuels pour des obligations a volume eleve (transaction reporting, surveillance). L'automatisation est indispensable pour la scalabilite et la fiabilite. Do not rely on manual-only controls for high-volume obligations.

- **Ignoring Record Keeping** : Ne pas negliger les obligations de conservation. Conserver toutes les communications (emails, chats, enregistrements telephoniques), toutes les decisions d'investissement, tous les ordres (y compris les ordres annules et modifies) pour la duree reglementaire. Ignoring record-keeping is a common enforcement trigger.

## Implementation Workflow

### Phase 1 : Cartographie reglementaire / Regulatory Mapping

1. Identifier toutes les juridictions applicables (lieu d'etablissement, lieu des clients, lieu de l'instrument)
2. Cartographier les reglementations applicables par activite (MiFID II, EMIR, MAR, SEC Act, FINRA)
3. Identifier les obligations de licence et d'autorisation (IF, CIF, broker-dealer registration)
4. Realiser une gap analysis entre l'existant et les exigences reglementaires
5. Prioriser les remediation actions par criticite et delai

### Phase 2 : Infrastructure de conformite / Compliance Infrastructure

1. Deployer un systeme de surveillance de marche (trade surveillance, communications monitoring)
2. Implementer les controles pre-trade (restricted lists, position limits, suitability checks)
3. Mettre en place le transaction reporting automatise (MiFIR Art. 26, EMIR, FINRA TRF)
4. Configurer les declencheurs d'alerte pour les obligations periodiques (13F, position reporting)
5. Implementer un systeme de record keeping conforme aux durees reglementaires

### Phase 3 : Politiques et procedures / Policies and Procedures

1. Rediger les politiques de best execution, order handling et allocation
2. Documenter la politique de gestion des conflits d'interets
3. Etablir la politique de personal account dealing (PAD)
4. Definir les procedures AML/KYC (CDD, EDD, ongoing monitoring, SAR/STR)
5. Formaliser la politique de remuneration conforme a MiFID II / Dodd-Frank

### Phase 4 : Fiscalite et reporting / Tax and Reporting

1. Configurer le calcul automatise des plus/moins-values (FIFO, cout moyen pondere, specific identification)
2. Implementer la detection des wash sales (fenetre de 30 jours, substantially identical securities)
3. Preparer les declarations fiscales (IFU/2074 France, Schedule D/Form 8949 US)
4. Configurer les declarations FATCA (formulaires W-8/W-9) et CRS
5. Automatiser les declarations periodiques (13F trimestriel, position reporting)

### Phase 5 : Formation et amelioration continue / Training and Continuous Improvement

1. Former l'ensemble du personnel aux obligations reglementaires applicables
2. Realiser des formations specifiques : MAR awareness, AML red flags, insider trading prevention
3. Executer des tests de conformite periodiques (mock audits, compliance testing program)
4. Maintenir une veille reglementaire active et un processus de change management
5. Documenter les lessons learned de chaque controle regulateur ou incident de conformite

## Modèle de maturité

### Niveau 1 — Non-informé
- Aucune connaissance des obligations réglementaires applicables à l'activité de trading
- Les déclarations fiscales sont incomplètes ou absentes
- Les règles de base (wash sale, PDT, seuils de déclaration) sont ignorées
- **Indicateurs** : nombre d'infractions non détectées élevé, aucun suivi du délai de reporting

### Niveau 2 — Conscient
- Les principales réglementations applicables (MiFID II ou SEC/FINRA) sont connues
- Les déclarations fiscales sont effectuées mais avec des erreurs ou retards fréquents
- Les obligations de reporting de base sont identifiées mais traitées manuellement
- **Indicateurs** : < 5 infractions/an, délai de reporting > J+3, taux de conformité ~ 60%

### Niveau 3 — Conforme
- Les obligations de reporting sont respectées dans les délais réglementaires
- Un processus de veille réglementaire est en place avec mise à jour trimestrielle
- Les contrôles pre-trade (restricted lists, position limits) sont implémentés
- **Indicateurs** : 0-2 infractions/an, délai de reporting J+1 respecté, taux de conformité > 85%

### Niveau 4 — Proactif
- Les évolutions réglementaires sont anticipées avec des plans d'adaptation pré-établis
- L'optimisation fiscale est intégrée dans la stratégie de trading (asset location, TLH)
- La surveillance automatisée des abus de marché est opérationnelle
- **Indicateurs** : 0 infraction/an, taux de conformité > 95%, coût fiscal optimisé à 90%

### Niveau 5 — Expert
- La conformité est intégrée by-design dans tous les processus de trading et d'investissement
- Le modèle Three Lines of Defense est pleinement opérationnel avec audit indépendant
- L'entité est reconnue comme référence par les régulateurs et les pairs du secteur
- **Indicateurs** : 0 infraction/an, taux de conformité 100%, coût fiscal optimisé à 95%+, délai de reporting systématiquement J+0

## Rythme opérationnel

| Cadence | Activité | Responsable | Livrable |
|---------|----------|-------------|----------|
| **Quotidien** | Transaction reporting et vérification des contrôles pre-trade | Compliance Officer | Rapport de transactions J+1 |
| **Hebdomadaire** | Veille réglementaire (nouvelles publications ESMA, SEC, AMF, FINRA) | Compliance Officer | Note de veille réglementaire |
| **Hebdomadaire** | Revue des alertes de surveillance de marché (abus, wash trading, spoofing) | Compliance Officer | Rapport d'alertes |
| **Mensuel** | Revue du transaction reporting et réconciliation avec le courtier | Compliance Officer / Back Office | Rapport de réconciliation |
| **Trimestriel** | Auto-évaluation de conformité + gap analysis réglementaire | Compliance Officer / Risk Manager | Rapport de conformité trimestriel |
| **Trimestriel** | Déclarations périodiques (13F, position reporting, seuils AMF) | Compliance Officer | Déclarations déposées |
| **Annuel** | Déclaration fiscale complète + audit de conformité global | Compliance Officer / Conseiller Fiscal | Déclaration fiscale + rapport d'audit |

## State of the Art (2025-2026)

La réglementation financière se renforce et se complexifie :

- **T+1 settlement** : Le passage au règlement T+1 aux US (2024) met la pression sur l'Europe pour suivre, transformant les processus post-trade.
- **MiFID III / MiFIR review** : La révision du cadre européen renforce les obligations de best execution, de transparence et de reporting.
- **Crypto-réglementation (MiCA)** : Le Markets in Crypto-Assets regulation entre en application, créant un cadre unifié européen pour les crypto-actifs.
- **Retail investor protection** : Les régulateurs renforcent la protection des particuliers (ESMA sur les CFDs, SEC sur les options, restrictions de levier).
- **ESG disclosure obligatoire** : Les fonds sont contraints de publier des informations ESG détaillées (SFDR Article 8/9), impactant les choix d'investissement retail.

## Template actionnable

### Checklist de conformité fiscale (France)

| Obligation | Échéance | Vérifié | Notes |
|---|---|---|---|
| **IFU reçu** — Formulaire de votre courtier | Février N+1 | ☐ | ___ |
| **Plus-values mobilières** — Calcul PV nettes | Avant déclaration | ☐ | ___ |
| **Flat tax / barème** — Choix du régime fiscal | Déclaration annuelle | ☐ | ___ |
| **Formulaire 2074** — Détail des cessions | Mai N+1 | ☐ | ___ |
| **Comptes à l'étranger** — Déclaration 3916 | Mai N+1 | ☐ | ___ |
| **Wash sale** — Vérifier pas de rachat < 30 jours | En continu | ☐ | ___ |
| **Seuil AMF** — Déclaration si > 5% du capital | En continu | ☐ | ___ |
| **Revenus dividendes** — Report sur 2DC | Mai N+1 | ☐ | ___ |

## Prompts types

- "Quelles sont mes obligations fiscales sur les plus-values de trading ?"
- "Comment déclarer mes revenus d'options en France ?"
- "Aide-moi à comprendre les règles du pattern day trader"
- "Quelles obligations MiFID II pour un investisseur particulier ?"
- "Comment éviter la wash sale rule dans mon portfolio ?"
- "Quels sont les seuils de déclaration AMF pour les positions ?"

## Skills connexes

| Skill | Lien |
|---|---|
| Juridique | `entreprise:juridique` — Cadre juridique et droit des marchés |
| Risk Management | `entreprise:risk-management` — Compliance et gestion des risques |
| Options Risk | `finance-de-marche:options-risk` — Réglementation des dérivés et marges |
| Portfolio | `finance-de-marche:portfolio` — Reporting et obligations de déclaration |
| Finance | `entreprise:finance` — Fiscalité et stratégie fiscale |

## Additional Resources

Consulter les fichiers de reference pour un approfondissement detaille / Consult the reference files for detailed deep dives:

- **[European Regulation](./references/european-regulation.md)** : MiFID II/MiFIR (authorisation, transparency, investor protection), EMIR (clearing, margining, trade reporting), MAR (insider dealing, market manipulation, PDMR, STORs), PRIIPs (KID), SFDR (Article 6/8/9, sustainability disclosures, PAI).

- **[US Regulation](./references/us-regulation.md)** : Securities Exchange Act, Reg NMS (order protection, access), Pattern Day Trader rules ($25K minimum equity), Reg T (50% initial margin), wash sale rules (30-day window, cost basis adjustment), insider trading (Section 10b-5, tipper/tippee), FINRA rules (suitability, best execution, margin).

- **[Reporting Obligations](./references/reporting-obligations.md)** : Transaction reporting (MiFIR Art. 26, FINRA TRF), position reporting, 13F/13D/13G filings, tax reporting (plus-values/IFU/formulaire 2074, Schedule D/Form 8949), FATCA/CRS, beneficial ownership disclosure.

- **[Trading Compliance](./references/trading-compliance.md)** : Best execution obligations, order handling & transparency, conflicts of interest management, suitability & appropriateness, record keeping, personal account dealing, AML/KYC for trading accounts.

- **[Études de cas](./references/case-studies.md)** — Cas pratiques détaillés illustrant les concepts clés du skill.
