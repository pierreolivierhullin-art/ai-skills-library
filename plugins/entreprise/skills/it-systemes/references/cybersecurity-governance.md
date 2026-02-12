# Cybersecurity Governance — ISO 27001, EBIOS RM, NIS2, Security Policies & Incident Response

## Overview

Ce document de reference couvre la gouvernance de la cybersecurite du point de vue du DSI et du RSSI : mise en oeuvre d'un SMSI (Systeme de Management de la Securite de l'Information) selon ISO 27001/27701, analyse de risques (EBIOS RM, ISO 27005), politique de securite (PSSI), sensibilisation des collaborateurs, reponse aux incidents, et conformite reglementaire (RGPD, NIS2, DORA, SOC 2, HDS). Utiliser ce guide pour structurer et ameliorer la posture de securite de l'organisation, en privilegiant une approche risque proportionnee et une culture positive de la securite.

---

## ISO 27001 / 27701 — Systeme de Management de la Securite

### ISO 27001:2022 — Structure et exigences

La norme ISO 27001 (derniere revision 2022) est le referentiel international pour les SMSI. Elle definit les exigences pour etablir, implementer, maintenir et ameliorer continuellement un SMSI.

#### Structure de la norme (clauses 4 a 10)

| Clause | Titre | Contenu cle |
|---|---|---|
| **4** | Contexte de l'organisation | Parties interessees, perimetre du SMSI, processus |
| **5** | Leadership | Engagement de la direction, politique de securite, roles et responsabilites |
| **6** | Planification | Appreciation des risques, traitement des risques, objectifs de securite |
| **7** | Support | Ressources, competences, sensibilisation, communication, documentation |
| **8** | Fonctionnement | Mise en oeuvre du plan de traitement des risques |
| **9** | Evaluation de la performance | Surveillance, mesure, audit interne, revue de direction |
| **10** | Amelioration | Non-conformites, actions correctives, amelioration continue |

#### Annexe A — Les 93 mesures de securite (revision 2022)

La revision 2022 reorganise les mesures en 4 themes (contre 14 dans la version 2013) :

| Theme | Nombre | Exemples |
|---|---|---|
| **Organizational** (37) | Politiques, roles, classification, relations fournisseurs, continuite | Politique de securite, gestion des actifs, relations fournisseurs |
| **People** (8) | Selection, sensibilisation, responsabilites, fin de contrat | Sensibilisation, responsabilites, processus disciplinaire |
| **Physical** (14) | Perimetres, equipements, cables, maintenance | Controles d'acces physique, protection des equipements |
| **Technological** (34) | Acces, chiffrement, protection malware, backup, logs | MFA, chiffrement, gestion des vulnerabilites, DLP |

Nouvelles mesures ajoutees en 2022 :
- **A.5.7** : Threat intelligence
- **A.5.23** : Information security for cloud services
- **A.5.30** : ICT readiness for business continuity
- **A.7.4** : Physical security monitoring
- **A.8.9** : Configuration management
- **A.8.10** : Information deletion
- **A.8.11** : Data masking
- **A.8.12** : Data leakage prevention
- **A.8.16** : Monitoring activities
- **A.8.23** : Web filtering
- **A.8.28** : Secure coding

### Parcours d'implementation ISO 27001

Duree typique : 12 a 18 mois pour une premiere certification.

```
Phase 1 — Initialisation (Mois 1-2)
  - Obtenir l'engagement de la direction (obligatoire ISO 27001 clause 5)
  - Definir le perimetre du SMSI (quels systemes, quels sites, quels processus)
  - Nommer le responsable du SMSI (souvent le RSSI)
  - Realiser un gap analysis initial (ecart par rapport aux exigences)
  - Planifier le projet de certification

Phase 2 — Analyse de risques et traitement (Mois 3-5)
  - Choisir la methodologie d'analyse de risques (EBIOS RM recommande en France)
  - Identifier les actifs, les menaces, les vulnerabilites
  - Evaluer les risques (probabilite x impact)
  - Definir le plan de traitement des risques (mesures de l'Annexe A)
  - Obtenir la validation de la direction (acceptation du risque residuel)

Phase 3 — Mise en oeuvre des mesures (Mois 5-12)
  - Deployer les mesures de securite (techniques, organisationnelles, physiques)
  - Rediger la documentation obligatoire (PSSI, procedures, DdA, registre des risques)
  - Former et sensibiliser les collaborateurs
  - Mettre en place le monitoring et les indicateurs

Phase 4 — Verification et amelioration (Mois 12-15)
  - Conduire un audit interne complet
  - Realiser la revue de direction
  - Corriger les non-conformites identifiees
  - Preparer l'audit de certification

Phase 5 — Certification (Mois 15-18)
  - Audit de certification Stage 1 (revue documentaire)
  - Audit de certification Stage 2 (audit sur site, verification de la mise en oeuvre)
  - Traitement des non-conformites eventuelles
  - Delivrance du certificat (valide 3 ans, audit de surveillance annuel)
```

### ISO 27701 — Extension Vie Privee

ISO 27701 etend ISO 27001 a la gestion des donnees personnelles. Elle est pertinente pour :
- Demontrer la conformite RGPD de maniere structuree
- Les organisations traitant des volumes importants de donnees personnelles
- Les sous-traitants (data processors) souhaitant rassurer leurs clients

L'implementation se fait en extension d'un SMSI ISO 27001 existant (prerequis).

---

## Analyse de Risques — EBIOS RM & ISO 27005

### EBIOS RM (Expression des Besoins et Identification des Objectifs de Securite — Risk Manager)

EBIOS RM est la methode officielle de l'ANSSI (Agence Nationale de la Securite des Systemes d'Information) pour l'analyse de risques cyber. Publiee en 2018, elle est la methode de reference pour les OIV (Operateurs d'Importance Vitale), les OSE (Operateurs de Services Essentiels) et toute organisation souhaitant une approche structuree des risques cyber.

#### Les 5 ateliers EBIOS RM

| Atelier | Objectif | Participants | Livrable |
|---|---|---|---|
| **1. Cadrage et socle de securite** | Definir le perimetre, les missions, les valeurs metier, le socle de securite existant | RSSI, metiers, direction | Perimetre, valeurs metier, socle de securite |
| **2. Sources de risques** | Identifier les sources de risques (attaquants) et leurs objectifs vises | RSSI, equipe securite, renseignement | Cartographie des sources de risques et objectifs |
| **3. Scenarios strategiques** | Definir les chemins d'attaque de haut niveau, identifier les parties prenantes de l'ecosysteme exploitables | RSSI, architecte, equipe securite | Scenarios strategiques, risques sur l'ecosysteme |
| **4. Scenarios operationnels** | Detailler les modes operatoires techniques pour chaque scenario strategique | RSSI, equipe securite, equipe IT, pentester | Scenarios techniques, vraisemblance |
| **5. Traitement du risque** | Definir les mesures de securite, evaluer le risque residuel, etablir le cadre de suivi | RSSI, direction, equipe securite | Plan de traitement, risque residuel, cadre de suivi |

#### Exemple de deroulement

Pour un atelier EBIOS RM sur un systeme d'information de gestion RH :

**Atelier 1** — Valeurs metier identifiees : donnees personnelles des employes, processus de paie, processus de recrutement. Socle de securite : antivirus deploye, firewall perimetrique, sauvegardes quotidiennes.

**Atelier 2** — Sources de risques : cybercriminel (objectif : exfiltration de donnees pour revente), employe malveillant (objectif : modification de sa paie), concurrent (objectif : vol de la base candidats).

**Atelier 3** — Scenario strategique : un cybercriminel exploite un sous-traitant de maintenance applicative pour acceder au SIRH et exfiltrer les donnees personnelles.

**Atelier 4** — Scenario operationnel : phishing cible sur un admin du sous-traitant -> vol de credentials VPN -> acces au SIRH -> exfiltration via protocole autorise (HTTPS) -> exfiltration de 50,000 dossiers employes.

**Atelier 5** — Mesures : MFA sur tous les acces VPN fournisseurs, PAM (Privileged Access Management) pour les comptes admin, DLP sur les flux sortants, audit de securite du sous-traitant, clause contractuelle de securite.

### ISO 27005 — Framework complementaire

ISO 27005 fournit un cadre generique pour le management des risques de securite de l'information, compatible avec ISO 27001. Il est moins prescriptif qu'EBIOS RM mais plus flexible pour les organisations internationales. Les deux sont compatibles et complementaires : utiliser ISO 27005 comme cadre general et EBIOS RM comme methode detaillee pour les analyses approfondies.

---

## Politique de Securite (PSSI)

### Structure d'une PSSI

La PSSI (Politique de Securite des Systemes d'Information) est le document fondateur de la securite de l'organisation. Structure recommandee :

#### 1. Politique generale (document de direction — 5-10 pages)

- Engagement de la direction
- Perimetre d'application
- Objectifs de securite
- Organisation de la securite (roles : RSSI, correspondants securite, CSIRT)
- Cadre reglementaire applicable
- Principes fondamentaux (need-to-know, moindre privilege, defense en profondeur)
- Sanctions en cas de non-respect

#### 2. Politiques thematiques (10-20 documents)

| Politique | Contenu cle |
|---|---|
| **Gestion des acces** | Politique de mots de passe, MFA, revue des droits, comptes privilegies (PAM) |
| **Classification de l'information** | Niveaux (public, interne, confidentiel, secret), marquage, regles de manipulation |
| **Utilisation des ressources IT** | Charte informatique, BYOD, usage acceptable, shadow IT |
| **Protection des donnees personnelles** | RGPD, PIA, droits des personnes, retention |
| **Gestion des incidents** | Processus de detection, qualification, escalade, notification |
| **Continuite / Reprise** | PCA/PRA, roles, activation, tests |
| **Relations fournisseurs** | Exigences securitaires, audits, clauses contractuelles |
| **Developpement securise** | Secure SDLC, revue de code, tests de securite, gestion des vulnerabilites |
| **Chiffrement** | Politique de chiffrement (donnees au repos, en transit, gestion des cles) |
| **Securite physique** | Controle d'acces, videoprotection, clean desk |
| **Logs et monitoring** | Politique de journalisation, retention, surveillance |
| **Gestion des vulnerabilites** | Scan, priorisation, patch management, delais de remediation |

#### 3. Procedures operationnelles (documents techniques)

Procedures detaillees pour l'equipe securite et IT : procedure de reponse a incident, procedure de gestion des vulnerabilites, procedure de revue des droits d'acces, procedure de backup et restauration, etc.

---

## Sensibilisation a la Securite

### Principes d'un programme de sensibilisation efficace

1. **Continu, pas ponctuel** : un email annuel ne suffit pas. Programmer des actions mensuelles.
2. **Adapte aux audiences** : dirigeants (risques strategiques), managers (responsabilites), IT (bonnes pratiques techniques), metiers (comportements quotidiens).
3. **Positif, pas punitif** : encourager les bons comportements plutot que sanctionner les mauvais. Recompenser le signalement de phishing.
4. **Mesure** : tracker le taux de clic sur les simulations de phishing, le taux de completion des formations, le nombre de signalements.
5. **Ancre dans le reel** : utiliser des exemples concrets de l'entreprise ou du secteur, pas des scenarios generiques.

### Programme type annuel

| Mois | Action | Format | Audience |
|---|---|---|---|
| Janvier | Campagne phishing #1 | Simulation | Tous |
| Fevrier | Formation securite des mots de passe | E-learning (20 min) | Tous |
| Mars | Workshop securite pour les developpeurs | Presentiel (2h) | Dev/IT |
| Avril | Campagne phishing #2 | Simulation | Tous |
| Mai | Sensibilisation RGPD et donnees personnelles | E-learning (30 min) | Tous |
| Juin | Exercice de crise cyber (tabletop) | Presentiel (4h) | Direction + RSSI + IT |
| Juillet | Newsletter securite estivale (BYOD, WiFi public) | Email + intranet | Tous |
| Aout | Campagne phishing #3 | Simulation | Tous |
| Septembre | Mois de la cybersecurite (European Cyber Security Month) | Multi-format | Tous |
| Octobre | Formation ingenierie sociale | E-learning (20 min) | Tous |
| Novembre | Campagne phishing #4 | Simulation | Tous |
| Decembre | Bilan annuel securite et objectifs N+1 | Presentation direction | Direction + managers |

### KPIs de sensibilisation

| KPI | Cible initiale | Cible mature |
|---|---|---|
| Taux de clic phishing | < 15% | < 5% |
| Taux de signalement phishing | > 20% | > 60% |
| Taux de completion des formations | > 80% | > 95% |
| Delai moyen de signalement | < 24h | < 2h |
| Score de culture securite (enquete) | > 3/5 | > 4/5 |

---

## Reponse aux Incidents

### Organisation du CSIRT / SOC

**SOC (Security Operations Center)** : equipe de surveillance en continu (24/7 pour les organisations critiques) qui detecte et qualifie les evenements de securite. Peut etre interne, externalise (MSSP) ou hybride.

**CSIRT (Computer Security Incident Response Team)** : equipe de reponse aux incidents qui intervient lorsqu'un incident est confirme. Conduit l'investigation, le confinement, l'eradication et la recuperation.

### Processus de reponse aux incidents (aligne NIST SP 800-61)

```
1. Preparation
   - Equipe CSIRT constituee et formee
   - Playbooks de reponse documentes par type d'incident
   - Outils deployes (SIEM, EDR, SOAR, forensics)
   - Contacts d'urgence (juridique, communication, DPO, ANSSI, autorites)
   - Exercices de crise reguliers

2. Detection et analyse
   - Detection : SIEM (alertes, correlations), EDR (comportements suspects), IDS/IPS, signalement utilisateur
   - Triage : severite (critique, haute, moyenne, basse), impact, urgence
   - Classification : type d'incident (ransomware, phishing, DDoS, data breach, insider threat)
   - Notification initiale : escalade selon la severite

3. Confinement
   - Court terme : isoler le systeme compromis, bloquer l'IP/le compte, couper l'acces reseau
   - Long terme : segmenter le reseau, renforcer les controles, preparer l'eradication
   - Preservation des preuves : images forensiques, logs, memoire volatile

4. Eradication
   - Identifier et supprimer la cause racine (malware, backdoor, compte compromis)
   - Patcher les vulnerabilites exploitees
   - Reinitialiser les credentials compromis
   - Verifier l'absence de persistence (scheduled tasks, registry, services)

5. Recuperation
   - Restaurer les systemes a partir de sauvegardes verifiees
   - Remettre en service progressivement (environnement de test d'abord)
   - Surveillance renforcee post-incident (30 jours minimum)
   - Validation par les metiers

6. Post-incident (retour d'experience)
   - Rapport d'incident detaille (timeline, impact, cause racine, actions)
   - Post-mortem blameless (focus sur les processus, pas sur les personnes)
   - Actions d'amelioration (techniques, organisationnelles, processus)
   - Mise a jour des playbooks et des mesures de securite
```

### Obligations de notification

| Regulation | Qui notifier | Delai | Seuil de declenchement |
|---|---|---|---|
| **RGPD** | CNIL + personnes concernees (si risque eleve) | 72 heures | Violation de donnees personnelles |
| **NIS2** | ANSSI (via le CSIRT national) | 24h (alerte) puis 72h (notification) puis 1 mois (rapport) | Incident significatif sur un service essentiel/important |
| **DORA** | Autorite competente (ACPR, AMF) | Sans delai indu | Incident ICT majeur (secteur financier) |
| **HDS** | ARS + ANSSI | 72 heures | Incident affectant des donnees de sante |

---

## Conformite Reglementaire

### NIS2 (Network and Information Security Directive 2)

La directive NIS2 (entree en vigueur en 2024-2025, transposition en droit national dans chaque etat membre de l'UE) elargit considerablement le perimetre de la securite des reseaux et des systemes d'information.

#### Entites concernees

| Categorie | Exemples de secteurs | Seuil |
|---|---|---|
| **Entites essentielles** | Energie, transport, banque, sante, eau, infrastructure numerique, administration publique | > 250 employes ou CA > 50M EUR |
| **Entites importantes** | Poste, gestion des dechets, chimie, alimentation, fabrication, services numeriques, recherche | > 50 employes ou CA > 10M EUR |

#### Obligations principales NIS2

- **Gouvernance** : la direction est responsable de la cybersecurite (obligation de formation des dirigeants, responsabilite personnelle).
- **Mesures de securite** : analyse de risques, politiques de securite, gestion des incidents, continuite d'activite, securite de la chaine d'approvisionnement, gestion des vulnerabilites, chiffrement, controle d'acces, MFA.
- **Notification d'incidents** : 24h pour l'alerte initiale, 72h pour la notification complete, 1 mois pour le rapport final.
- **Sanctions** : jusqu'a 10M EUR ou 2% du CA mondial pour les entites essentielles, 7M EUR ou 1.4% du CA pour les entites importantes.

### DORA (Digital Operational Resilience Act)

DORA (applicable a partir de janvier 2025) impose des exigences de resilience operationnelle numerique au secteur financier europeen.

#### Exigences cles DORA

1. **Gestion des risques ICT** : cadre de gestion des risques lies aux technologies de l'information et de la communication.
2. **Tests de resilience** : tests de penetration avances (TLPT — Threat-Led Penetration Testing) pour les entites significatives.
3. **Gestion des incidents ICT** : processus de gestion, classification et notification des incidents.
4. **Gestion des risques lies aux tiers ICT** : registre des prestataires ICT, evaluation des risques, clauses contractuelles, plans de sortie.
5. **Partage d'informations** : mecanismes de partage d'informations sur les menaces cyber entre entites financieres.

### SOC 2

SOC 2 (System and Organization Controls 2) est un referentiel d'audit developpe par l'AICPA pour les fournisseurs de services. Particulierement pertinent pour les editeurs SaaS et les hebergeurs.

#### Les 5 criteres TSC (Trust Services Criteria)

| Critere | Description | Obligatoire |
|---|---|---|
| **Security** (Common Criteria) | Protection des systemes contre les acces non autorises | Oui (toujours) |
| **Availability** | Disponibilite des systemes selon les SLA | Optionnel |
| **Processing Integrity** | Traitement complet, precis et autorise | Optionnel |
| **Confidentiality** | Protection des informations confidentielles | Optionnel |
| **Privacy** | Collecte, utilisation, conservation des donnees personnelles | Optionnel |

SOC 2 Type I : evaluation de la conception des controles a un instant T.
SOC 2 Type II : evaluation de la conception ET de l'efficacite operationnelle des controles sur une periode (generalement 6-12 mois). Type II est largement prefere.

### HDS (Hebergement de Donnees de Sante)

La certification HDS est obligatoire en France pour tout hebergeur de donnees de sante a caractere personnel. Basee sur ISO 27001 avec des exigences supplementaires specifiques au secteur de la sante.

Deux niveaux :
- **Hebergeur d'infrastructure physique** : datacenter physique.
- **Hebergeur infogrant** : services d'hebergement managed (le plus courant pour les editeurs SaaS sante).

---

## Zero Trust Architecture

### Principes fondamentaux

Le Zero Trust repose sur le principe "Never trust, always verify" :

1. **Verifier explicitement** : authentifier et autoriser chaque acces en fonction de l'identite, du device, de la localisation, du contexte.
2. **Moindre privilege** : accorder uniquement les acces strictement necessaires, pour la duree strictement necessaire.
3. **Supposer la compromission** : concevoir les systemes en supposant que le reseau est deja compromis. Minimiser le blast radius.

### Piliers d'implementation Zero Trust

| Pilier | Mesures | Outils |
|---|---|---|
| **Identite** | MFA systematique, SSO, acces conditionnel, verification continue | Azure AD / Entra ID, Okta, Ping Identity |
| **Device** | Conformite du device, MDM/MAM, posture assessment | Intune, Jamf, CrowdStrike Falcon |
| **Reseau** | Micro-segmentation, ZTNA (remplacement VPN), chiffrement de bout en bout | Zscaler, Cloudflare Access, Illumio |
| **Application** | Authentification applicative, WAF, runtime protection | Cloudflare WAF, AWS WAF, Palo Alto Prisma |
| **Donnees** | Classification, DLP, chiffrement, droits d'acces granulaires | Microsoft Purview, Varonis, Thales CipherTrust |
| **Visibilite** | SIEM, EDR/XDR, UEBA, logging centralise | Splunk, Microsoft Sentinel, CrowdStrike, Elastic |

### Feuille de route Zero Trust type

```
Phase 1 (0-6 mois) — Quick Wins
  - MFA sur tous les acces (VPN, cloud, applications critiques)
  - SSO centralise (SAML/OIDC) pour les applications principales
  - EDR deploye sur tous les endpoints
  - Logging centralise dans un SIEM

Phase 2 (6-12 mois) — Fondations
  - Acces conditionnel base sur le risque (identite + device + contexte)
  - ZTNA en remplacement du VPN pour les applications internes
  - Micro-segmentation des reseaux critiques
  - PAM (Privileged Access Management) pour les comptes admin

Phase 3 (12-24 mois) — Industrialisation
  - Classification automatique des donnees et DLP
  - Verification continue de la posture des devices
  - XDR (Extended Detection and Response) integrant tous les piliers
  - Automatisation de la reponse (SOAR) pour les incidents courants

Phase 4 (24+ mois) — Maturite
  - Zero Trust complete sur tous les flux (internes et externes)
  - AI-driven threat detection et reponse automatisee
  - Continuous validation (BAS — Breach and Attack Simulation)
  - Integration Zero Trust dans le DevSecOps pipeline
```

---

## State of the Art (2024-2026)

### Tendances majeures en cybersecurite gouvernance

1. **NIS2 et DORA — operationnalisation** : apres la phase de transposition legislative (2024-2025), les organisations entrent dans la phase d'operationnalisation de NIS2 et DORA (2025-2026). Les exigences de gouvernance (responsabilite des dirigeants, formation obligatoire, gestion des risques des tiers) transforment la cybersecurite d'un sujet technique en un sujet de direction generale. Les sanctions financieres significatives (jusqu'a 10M EUR ou 2% du CA) accelerent la prise de conscience.

2. **AI for Cybersecurity et Cybersecurity for AI** : l'IA transforme la cybersecurite sur deux axes. D'une part, l'IA ameliore la detection (correlation d'alertes, detection d'anomalies, UEBA, analyse de malware), la reponse (automatisation SOAR, triage IA), et la prediction (threat intelligence augmentee). D'autre part, la securite de l'IA elle-meme devient un enjeu : protection des modeles ML (adversarial attacks, model poisoning), securisation des deployements LLM (prompt injection, data leakage), gouvernance des donnees d'entrainement.

3. **Zero Trust generalise et SASE** : le Zero Trust n'est plus un concept mais une realite operationnelle. Les solutions SASE (Secure Access Service Edge) combinent SD-WAN + CASB + ZTNA + SWG + FWaaS dans une plateforme unifiee (Zscaler, Palo Alto Prisma, Cloudflare One, Netskope). Le VPN d'entreprise classique est en voie de disparition, remplace par le ZTNA (Zero Trust Network Access).

4. **Supply chain security renforcee** : les attaques via la chaine d'approvisionnement (SolarWinds, MOVEit, Codecov) ont impose le renforcement de la securite des tiers. NIS2 exige explicitement la gestion des risques de la chaine d'approvisionnement. Les pratiques incluent : evaluation systematique des fournisseurs (questionnaires, audits, certifications), clauses contractuelles de securite, SBOM (Software Bill of Materials), verification de la provenance (SLSA), monitoring continu des tiers (SecurityScorecard, BitSight).

5. **Cyber resilience > cybersecurite** : le paradigme evolue de la prevention (empecher toute attaque) vers la resilience (supposer la compromission, minimiser l'impact, recuperer rapidement). Les organisations matures investissent dans le chaos engineering securite (Breach and Attack Simulation — AttackIQ, SafeBreach), les exercices de crise reguliers, et les capacites de restauration rapide (backup immutable, PRA automatise).

6. **Identity-first security** : l'identite devient le perimetre de securite principal. Les solutions IAM/IGA (Identity Governance and Administration) s'enrichissent : verification continue, acces juste-a-temps (JIT), certification automatique des acces, gouvernance des identites machines (service accounts, API keys, certificates). Les passkeys (FIDO2/WebAuthn) commencent a remplacer les mots de passe.

7. **Cloud-native security (CNAPP)** : les outils de securite convergent vers les CNAPP (Cloud-Native Application Protection Platforms) qui combinent CSPM (Cloud Security Posture Management), CWPP (Cloud Workload Protection), CIEM (Cloud Infrastructure Entitlement Management), et runtime protection. Wiz, Palo Alto Prisma Cloud, et CrowdStrike dominent ce marche en forte croissance.

8. **Securite des environnements OT/IoT** : la convergence IT/OT (Operational Technology) expose les systemes industriels aux cybermenaces. NIS2 couvre explicitement les secteurs industriels. Les solutions de securite OT (Claroty, Nozomi Networks, Dragos) se developpent pour proteger les SCADA, PLC et systemes industriels. L'approche Zero Trust s'etend a l'OT avec des defis specifiques (systemes legacy, protocoles proprietaires, disponibilite critique).

9. **Automatisation de la conformite (GRC-as-Code)** : la gestion de la conformite evolue des tableurs et des audits manuels vers l'automatisation. Les outils GRC modernes (Drata, Vanta, Anecdotes, Thoropass) automatisent la collecte de preuves, la verification continue des controles, et la preparation des audits (ISO 27001, SOC 2, RGPD). L'approche "compliance-as-code" encode les controles de conformite dans les pipelines CI/CD.

10. **Cybersecurite quantique — preparation** : bien que les ordinateurs quantiques capables de casser les algorithmes actuels ne soient pas attendus avant 2030-2035, la menace "harvest now, decrypt later" justifie une preparation des maintenant. Le NIST a finalise les premiers algorithmes de cryptographie post-quantique (ML-KEM, ML-DSA, SLH-DSA) en 2024. Les organisations doivent inventorier leurs usages cryptographiques, planifier la migration vers les algorithmes post-quantiques, et tester les implementations hybrides.
