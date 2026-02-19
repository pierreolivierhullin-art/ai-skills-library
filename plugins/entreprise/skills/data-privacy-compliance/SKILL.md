---
name: data-privacy-compliance
version: 1.0.0
description: >
  Use this skill when the user asks about "RGPD", "GDPR", "data privacy", "DMA", "DSA", "privacy by design", "DPIA", "data protection officer", "DPO", "consent management", "data subject rights", "personal data protection", "CCPA", "data breach notification", "cookies compliance", "privacy compliance program", discusses regulatory obligations for personal data, data mapping, or needs guidance on building a privacy compliance program, managing data subject requests, and implementing privacy engineering.
---

# Data Privacy & Compliance — RGPD, DMA, DSA & Privacy by Design

## Overview

Le paysage reglementaire de la donnee personnelle et des plateformes numeriques est devenu une contrainte strategique pour toute organisation qui collecte, traite ou commercialise des donnees. Trois reglements europeens structurent ce paysage : **RGPD** (General Data Protection Regulation, 2018), **DMA** (Digital Markets Act, 2023) et **DSA** (Digital Services Act, 2024).

**Le cout de la non-conformite** : amendes jusqu'a 4% du CA mondial pour le RGPD, 10-20% du CA mondial pour le DMA, 6% pour le DSA. Mais l'enjeu depasse la conformite : la confiance client est un actif strategique dans un contexte de hyper-sensibilite aux donnees.

**La distinction conformite vs privacy by design** : La conformite est reactive (repondre aux exigences) ; le privacy by design est proactif (integrer la protection de la vie privee dans les produits et processus des la conception). Les organisations matures visent le second.

**Perimetre de ce skill** :
- RGPD : principes, droits des personnes, obligations des entreprises
- DMA : obligations des gatekeepers, interoperabilite, acces aux donnees
- DSA : moderations de contenus, transparence, obligations des tres grandes plateformes
- Privacy by Design : methodes d'integration de la vie privee dans les processus
- DPIA : methodologie d'analyse d'impact

## Core Principles

**1. Licite, loyal, transparent.** Toute collecte de donnee doit avoir une base legale (consentement, contrat, obligation legale, interet vital, mission de service public, interet legitime). Aucune donnee ne peut etre collectee "au cas ou". Le principe de transparence exige d'informer clairement les personnes concernees.

**2. Minimisation des donnees.** Collecter uniquement ce qui est necessaire a la finalite declaree. Evaluer regulierement : "avons-nous encore besoin de cette donnee ?" Les donnees inutiles sont un risque (violation possible) et un cout (stockage, maintenance, conformite).

**3. Limitation des finalites.** Une donnee collectee pour finalite A ne peut pas etre utilisee pour finalite B sans nouvelle base legale. Le changement de finalite est l'une des erreurs les plus frequentes (ex : donnees clients utilisees pour de la prospection sans consentement).

**4. Exactitude et conservation limitee.** Donnees a jour, purges automatiques. Definir des durees de retention par type de donnee et automatiser la suppression. La retention infinie est non-conforme.

**5. Securite et confidentialite integrees.** La securite technique (chiffrement, controle d'acces, pseudonymisation) est une obligation RGPD, pas une option. Documenter les mesures de securite dans le registre de traitement.

**6. Responsabilite (accountability).** Prouver la conformite, pas seulement etre conforme. Documenter : registre de traitement, DPIAs, formations, politiques. L'accountability est un principe fondamental : le CNIL peut demander a voir ces preuves a tout moment.

## Reglements Cles

### RGPD — General Data Protection Regulation

**Champ d'application** : Toute organisation (UE ou non) traitant des donnees de personnes en UE.

**Bases legales (Article 6)** :
- **Consentement** : libre, specifique, eclaire, univoque. Retirable a tout moment. Ne pas pre-cocher des cases.
- **Contrat** : necessaire a l'execution du contrat avec la personne.
- **Obligation legale** : traitement impose par la loi.
- **Interet vital** : protection de la vie.
- **Mission de service public** : autorite publique.
- **Interet legitime** : base flexible mais necessite un test de balance (interet de l'organisme vs droits de la personne). Non applicable aux autorites publiques.

**Droits des personnes** :
- Droit d'acces (Article 15) : recevoir une copie des donnees en 1 mois
- Droit de rectification (Article 16) : corriger les donnees inexactes
- Droit a l'effacement (Article 17) : "droit a l'oubli" sous conditions
- Droit a la portabilite (Article 20) : exporter les donnees dans un format standard
- Droit d'opposition (Article 21) : s'opposer au traitement fonde sur l'interet legitime
- Droit de ne pas etre soumis a une decision automatisee (Article 22)

**Obligations cles** :
- Registre de traitement (Article 30) : obligatoire pour les organisations > 250 salaries ou traitant des donnees sensibles
- DPIA (Article 35) : obligatoire si traitement "a risque eleve"
- DPO (Article 37) : obligatoire pour certaines categories (autorites publiques, traitement de donnees sensibles a grande echelle)
- Notification de violation (Article 33) : 72h pour notifier la CNIL, sans delai inutile pour les personnes si risque eleve

**Donnees sensibles (Article 9)** : sante, origine ethnique, opinions politiques, convictions religieuses, donnees genetiques/biometriques, vie/orientation sexuelle, appartenance syndicale. Interdiction de principe sauf exceptions.

### DMA — Digital Markets Act (2023)

**Cible** : Gatekeepers (grandes plateformes designees par la Commission europeenne — actuellement : Alphabet/Google, Apple, Meta, Amazon, Microsoft, ByteDance).

**Obligations cles pour les gatekeepers** :
- Interoperabilite des services de messagerie
- Interdiction de traitement croise des donnees entre services sans consentement explicite
- Acces equitable aux donnees pour les professionnels sur la plateforme
- Interdiction du self-preferencing (avantager ses propres services)
- Interdiction du tying (imposer ses propres services)
- Transparence sur les algorithmes de classement

**Pour les autres organisations** : Principalement des opportunites (acces aux donnees des gatekeepers, interoperabilite) et des impacts indirects (nouvelles API, donnees accessibles).

### DSA — Digital Services Act (2024)

**Cible** : Intermediaires en ligne par taille (micro-entreprises exemptees, tres grandes plateformes/moteurs de recherche avec > 45M utilisateurs en UE soumis aux obligations les plus strictes).

**Obligations par categorie** :
- **Toutes les plateformes** : point de contact, signalement de contenus illegaux, transparence publicitaire
- **Plateformes d'hebergement** : mecanisme de signalement, notification aux autorites, politique de conditions
- **Tres grandes plateformes (VLOP)** : evaluation des risques systemiques annuelle, audit independant, acces des chercheurs aux donnees, transparence algorithmique

## Privacy by Design — 7 Principes (Cavoukian)

1. **Proactif, pas reactif** : anticiper et prevenir, pas corriger
2. **Vie privee par defaut** : parametres les plus protecteurs par defaut, sans action de l'utilisateur
3. **Integre dans la conception** : pas ajoutee en fin de projet comme une couche vernis
4. **Fonctionnalite totale** : vie privee ET securite, pas de compromis
5. **Securite de bout en bout** : protection tout au long du cycle de vie
6. **Visibilite et transparence** : auditable, verifiable
7. **Respect de la vie privee des utilisateurs** : centree sur l'individu

**Implementation pratique** : Privacy Threat Modeling (LINDDUN), Privacy Impact Assessment integre aux sprints, PETs (Privacy-Enhancing Technologies) : anonymisation, pseudonymisation, chiffrement homomorphe, donnees synthetiques.

## Decision Guide

### Quelle base legale choisir ?

| Situation | Base legale recommandee | Pitfall |
|---|---|---|
| Newsletter marketing | Consentement | Ne pas utiliser interet legitime |
| Facturation client | Contrat | Consentement inutile |
| Analyse fraude | Interet legitime | Documenter le test de balance |
| Donnees sante | Consentement explicite | Base legale Art. 9 requise |
| Conservation comptable | Obligation legale | Specifier la loi applicable |

### Quand realiser une DPIA ?

**Obligatoire si le traitement** :
- Score/profilage avec effets significatifs
- Traitement automatise pour decisions importantes
- Surveillance systematique a grande echelle
- Donnees sensibles a grande echelle
- Appariement ou combinaison de jeux de donnees
- Personnes vulnerables (enfants, patients)
- Usage innovant de technologie (biometrie, IA)
- Transfert hors UE avec risque

**Seuil pratique** : Si 2 criteres ou plus sur la liste CNIL/G29, DPIA obligatoire.

## Workflow — Programme de Conformite RGPD

**Etape 1 — Cartographie** (4-8 semaines) :
- Inventaire des traitements par BU
- Identification des bases legales
- Cartographie des flux de donnees (quelles donnees, d'ou, vers ou, combien de temps)
- Identification des sous-traitants

**Etape 2 — Analyse des ecarts** (2-4 semaines) :
- Comparaison etat actuel vs exigences RGPD
- Priorisation des non-conformites par niveau de risque
- Roadmap de mise en conformite

**Etape 3 — Mise en conformite** (3-12 mois) :
- Registre de traitement formalise
- Politiques de confidentialite mises a jour
- Contrats sous-traitants (DPA - Data Processing Agreements)
- Gestion du consentement (CMP - Consent Management Platform)
- Procedures droits des personnes (formulaire, processus, SLA 1 mois)
- Procedures de violation de donnees (playbook 72h)

**Etape 4 — Formation et culture** :
- Formation DPO et juridique : niveau expert
- Formation equipes techniques : privacy by design, secure coding
- Formation managers : sensibilisation aux donnees sensibles
- Formation generale : phishing, gestion des mots de passe, signalement incidents

**Etape 5 — Maintenance continue** :
- Registre mis a jour a chaque nouveau traitement
- DPIAs pour les nouveaux projets a risque
- Revue annuelle des bases legales et durees de retention
- Veille reglementaire (CNIL, EDPB, jurisprudence)

## Maturity Model — Privacy Compliance

| Niveau | Caracteristique | Indicateurs |
|---|---|---|
| **1 — Naif** | Pas de conscience reglementaire | Pas de registre, pas de DPO, cookies non conformes |
| **2 — Reactif** | Conformite apres incident ou mise en demeure | Registre basique, politique de confidentialite generique |
| **3 — Conforme** | Conformite documentee et maintenue | Registre complet, DPIAs realisees, DPO operationnel |
| **4 — Privacy by Design** | Vie privee integree dans les processus | Threat modeling en sprint, PETs deployes, formation continue |
| **5 — Differentiation** | La vie privee comme avantage concurrentiel | Label CNIL, privacy-first comme argument marketing, trusted data partner |

## Templates

### Registre de Traitement (extrait de colonnes)
| Finalite | Base legale | Categories de donnees | Duree de retention | Destinataires | Transferts hors UE | Mesures de securite |

### Checklist DPIA (simplifiee)
- [ ] Description du traitement et de ses finalites
- [ ] Necessite et proportionnalite (minimisation)
- [ ] Risques identifies (acces non autorise, perte de donnees, divulgation)
- [ ] Mesures envisagees pour chaque risque
- [ ] Avis du DPO
- [ ] Consultation de la CNIL si risque residuel eleve

## Limites et Points de Vigilance

- Le RGPD n'est pas un dossier a finaliser une fois : c'est un processus continu
- L'interet legitime n'est pas une base legale "fourre-tout" : documenter systematiquement le test de balance
- Les cookies tiers sont en cours de suppression : anticiper le cookieless avec des alternatives (first-party data, cohortes)
- Les transferts hors UE post-Schrems II : verifier les Clauses Contractuelles Types et les mesures supplementaires pour chaque transfert vers les US ou autres pays tiers
- DMA et DSA evoluent rapidement : les lignes directrices de la Commission continuent d'etre publiees
- La CNIL sanctionne aussi les petites structures : le RGPD s'applique quelle que soit la taille
