---
name: ai-risk
description: This skill should be used when the user asks about "AI risk", "hallucination", "model drift", "adversarial attacks", "AI safety", "red teaming AI", "prompt injection", "data poisoning", "model collapse", "AI alignment", "AI kill switch", or needs guidance on AI-specific risk assessment, mitigation, and safety engineering.
version: 1.0.0
---

# AI Risk Assessment & Safety Engineering

## Overview

Ce skill couvre l'ensemble du spectre des risques lies aux systemes d'intelligence artificielle : evaluation et taxonomie des risques, attaques adversariales, securite des modeles, alignement et safety, robustesse operationnelle et reponse aux incidents. Il synthetise les meilleures pratiques 2024-2026 incluant le NIST AI Risk Management Framework, les defenses contre le prompt injection, la securite des agents autonomes, les risques multi-modaux et les bases de donnees d'incidents AI. Utiliser ce skill comme reference systematique pour toute decision touchant a l'identification, l'evaluation, l'attenuation et le monitoring des risques specifiques a l'IA.

## When This Skill Applies

Activer ce skill dans les situations suivantes :

- Evaluation des risques d'un systeme IA avant deploiement (risk assessment)
- Identification et classification des risques techniques, operationnels, reputationnels ou securitaires
- Conception de defenses contre les attaques adversariales (prompt injection, data poisoning, model extraction)
- Detection et attenuation des hallucinations, du model drift, ou du model collapse
- Mise en place de red teaming pour des systemes IA (LLMs, agents, multi-modal)
- Implementation de mecanismes de safety : content filtering, kill switches, graceful degradation
- Conception d'une strategie d'alignement (Constitutional AI, RLHF, DPO, RLAIF)
- Reponse aux incidents impliquant des systemes IA (outputs nocifs, fuites de donnees, biais detectes)
- Evaluation de la dependance fournisseur, des couts, de la latence et de la disponibilite
- Conformite avec les cadres reglementaires exigeant une gestion des risques IA (EU AI Act, NIST AI RMF)

## Core Principles

### 1. Risk-First Thinking (Raisonnement par les risques)

Ne jamais deployer un systeme IA sans avoir identifie, evalue et documente les risques. Appliquer une approche structuree : identifier les menaces, evaluer la probabilite et l'impact, definir les mesures d'attenuation, et accepter formellement le risque residuel. Chaque risque doit avoir un proprietaire, un plan de mitigation et un seuil de declenchement d'alerte.

### 2. Defense in Depth (Defense en profondeur)

Combiner systematiquement plusieurs couches de protection. Pour un LLM en production : input validation + system prompt hardening + output filtering + monitoring + circuit breaker + human-in-the-loop. Une seule couche de defense sera inevitablement contournee. Chaque couche doit fonctionner independamment des autres.

### 3. Assume Breach (Presumer la compromission)

Concevoir les systemes en partant du principe que les guardrails seront contournes. Limiter le blast radius : restreindre les permissions des agents, isoler les environnements, plafonner les actions automatisees. Implementer des mecanismes de detection et de reponse rapide plutot que de se reposer uniquement sur la prevention.

### 4. Continuous Monitoring (Surveillance continue)

Les risques IA sont dynamiques : les modeles derivent, les attaquants innovent, les donnees changent. Implementer un monitoring continu des performances, de la qualite des outputs, des patterns d'utilisation anormaux, et de la distribution des inputs. Ne jamais considerer un deploiement comme "termine" — c'est le debut du cycle de surveillance.

### 5. Human Oversight (Supervision humaine)

Maintenir un controle humain proportionnel au niveau de risque. Les decisions a fort impact (financier, medical, legal, securitaire) necessitent un human-in-the-loop. Les decisions a faible impact tolerent un human-on-the-loop avec monitoring. Aucun systeme IA ne doit operer sans mecanisme de supervision adapte a son niveau de risque.

## Key Frameworks & Methods

### NIST AI Risk Management Framework (AI RMF 1.0)

Le cadre de reference mondial pour la gestion des risques IA. Structurer chaque initiative AI autour de ses quatre fonctions :

| Fonction | Objectif | Actions cles |
|----------|----------|--------------|
| **GOVERN** | Etablir la culture et la structure de gouvernance des risques IA | Definir les roles, responsabilites, politiques. Creer un AI risk board. Documenter l'appetit pour le risque. |
| **MAP** | Identifier et contextualiser les risques | Inventorier les systemes IA. Cataloguer les risques par categorie. Identifier les parties prenantes impactees. |
| **MEASURE** | Evaluer et quantifier les risques | Definir les metriques de risque. Conduire des evaluations regulieres. Benchmarker la robustesse et la fiabilite. |
| **MANAGE** | Traiter, monitorer et communiquer les risques | Prioriser et attenuer les risques. Implementer le monitoring. Preparer la reponse aux incidents. |

### Taxonomie des risques IA

| Categorie | Risques principaux | Severite typique |
|-----------|--------------------|-----------------|
| **Technique** | Hallucinations, model drift, model collapse, data quality issues | Haute |
| **Securitaire** | Prompt injection, data poisoning, model extraction, membership inference, data leakage | Critique |
| **Operationnel** | Vendor lock-in, couts incontroles, latence, disponibilite, scalabilite | Moyenne-Haute |
| **Reputationnel** | Outputs inappropries, biais detectes, deepfakes, perte de confiance | Haute |
| **Legal/Reglementaire** | Non-conformite EU AI Act, RGPD, responsabilite civile, propriete intellectuelle | Critique |
| **Ethique** | Biais systematiques, discrimination, manque de transparence, perte d'autonomie humaine | Haute |

### Matrice Probabilite x Impact

Utiliser cette matrice pour prioriser les risques identifies :

```
Impact:     |  Negligeable  |   Mineur    |   Majeur    |   Critique   |  Catastrophique
------------|---------------|-------------|-------------|--------------|----------------
Tres probable|   Modere     |    Eleve    |   Eleve     |   Critique   |   Critique
Probable     |   Faible     |   Modere    |   Eleve     |   Eleve      |   Critique
Possible     |   Faible     |   Faible    |   Modere    |   Eleve      |   Eleve
Peu probable |   Neg.       |   Faible    |   Faible    |   Modere     |   Eleve
Rare         |   Neg.       |   Neg.      |   Faible    |   Faible     |   Modere
```

**Regles de decision :**
- Critique : arret immediat, escalade direction, remediation obligatoire avant mise en production
- Eleve : plan d'action dans les 7 jours, mitigation partielle avant deploiement
- Modere : plan d'action dans les 30 jours, monitoring renforce
- Faible : acceptation documentee avec revue trimestrielle
- Negligeable : acceptation tacite, revue annuelle

### OWASP Top 10 for LLM Applications (2025)

Reference obligatoire pour securiser les applications basees sur des LLMs :

1. **LLM01 : Prompt Injection** — Manipulation des instructions via inputs utilisateur (direct) ou donnees externes (indirect)
2. **LLM02 : Insecure Output Handling** — Outputs non sanitises executes dans des contextes aval (XSS, injection SQL via LLM)
3. **LLM03 : Training Data Poisoning** — Corruption des donnees d'entrainement ou de fine-tuning
4. **LLM04 : Model Denial of Service** — Inputs malicieux causant une consommation excessive de ressources
5. **LLM05 : Supply Chain Vulnerabilities** — Modeles, datasets ou plugins compromis dans la chaine d'approvisionnement
6. **LLM06 : Sensitive Information Disclosure** — Fuite de donnees sensibles dans les outputs du modele
7. **LLM07 : Insecure Plugin Design** — Plugins LLM avec des permissions excessives ou sans input validation
8. **LLM08 : Excessive Agency** — Agent IA avec des permissions disproportionnees et sans controles suffisants
9. **LLM09 : Overreliance** — Dependance excessive aux outputs IA sans verification humaine
10. **LLM10 : Model Theft** — Extraction du modele ou de ses poids via des requetes systematiques

## Decision Guide

### Evaluer le niveau de risque d'un systeme IA

```
Le systeme prend-il des decisions autonomes a fort impact ?
  (medical, financier, legal, securitaire)
  -> Risque CRITIQUE : human-in-the-loop obligatoire, audit complet,
     conformite EU AI Act, red teaming approfondi

Le systeme genere-t-il du contenu public ?
  (chatbot client, generation marketing, recommandations)
  -> Risque ELEVE : content filtering multi-couche, monitoring
     des outputs, mecanisme de feedback, revue editoriale

Le systeme traite-t-il des donnees personnelles ou sensibles ?
  (PII, donnees medicales, financieres)
  -> Risque ELEVE : data leakage prevention, anonymisation,
     conformite RGPD, audit trail complet

Le systeme est-il un outil interne a faible autonomie ?
  (assistant developpeur, resume de documents, recherche interne)
  -> Risque MODERE : guardrails standards, monitoring basique,
     revue periodique des outputs

Le systeme est-il un prototype ou un PoC non deploye ?
  -> Risque FAIBLE : documenter les risques identifies pour
     le passage en production, sandboxing strict
```

### Choisir une strategie de mitigation

```
Prompt injection identifie comme risque principal ?
  -> Input validation + instruction hierarchy + output filtering
  -> Considerer sandwich defense et XML/delimiter-based prompts
  -> Tester avec des frameworks de red teaming automatise (garak, PyRIT)

Hallucinations critiques pour le cas d'usage ?
  -> RAG avec sources verifiees + citation obligatoire
  -> Confidence scoring + seuil de rejet
  -> Grounding verification automatisee

Model drift / degradation des performances ?
  -> Monitoring continu des metriques de qualite
  -> A/B testing des nouvelles versions de modele
  -> Rollback automatise si les metriques degradent

Risque de data leakage ?
  -> PII detection dans les inputs ET outputs
  -> Tokenisation/anonymisation des donnees sensibles
  -> Network isolation + egress filtering

Dependance fournisseur excessive ?
  -> Abstraction layer (LiteLLM, portkey, OpenRouter)
  -> Multi-provider strategy avec fallback
  -> Modeles open-source comme backup (Llama, Mistral, Qwen)
```

## Common Patterns & Anti-Patterns

### Patterns recommandes

- **Layered Defense for LLMs** : Combiner system prompt hardening + input sanitization + output filtering + monitoring + circuit breaker. Chaque couche intercepte ce que les autres manquent. Ne jamais se reposer sur le system prompt seul pour la securite.

- **Graceful Degradation** : Concevoir des fallback progressifs : si le LLM principal echoue, basculer sur un modele de secours, puis sur des reponses pre-definies, puis sur un message d'erreur informatif orientant vers un humain. Ne jamais renvoyer un output brut non valide.

- **Kill Switch Pattern** : Implementer un mecanisme d'arret immediat a chaque niveau : requete individuelle (timeout), session (blocage utilisateur), feature (feature flag), systeme entier (circuit breaker global). Chaque kill switch doit etre testable et actionnable en moins de 5 minutes.

- **Red Team / Blue Team continu** : Maintenir un programme de red teaming continu, pas uniquement avant le lancement. Utiliser des outils automatises (garak, PyRIT, Adversarial Robustness Toolbox) en complement du red teaming humain. Documenter chaque vulnerabilite trouvee et verifier la remediation.

- **Risk Register vivant** : Maintenir un registre des risques mis a jour en continu, pas un document statique. Chaque risque a un proprietaire, un statut, des metriques de suivi, et un plan d'action. Revue en comite mensuelle pour les risques eleves et critiques.

### Anti-patterns a eviter

- **Security by system prompt** : Ne jamais considerer le system prompt comme une frontiere de securite. Il est systematiquement extractible et contournable. Utiliser des mecanismes de securite hors du modele (code applicatif, filtres, permissions).

- **"Our model doesn't hallucinate"** : Tous les modeles generatifs hallucinent. La question n'est pas "si" mais "quand" et "avec quelles consequences". Concevoir pour la detection et l'attenuation, pas pour l'elimination.

- **Test-once-deploy-forever** : Ne jamais considerer les tests pre-deploiement comme suffisants. Les modeles evolvent, les attaques evoluent, les donnees evoluent. Implementer du testing continu en production (shadow testing, canary releases, monitoring actif).

- **Unlimited agent autonomy** : Ne jamais donner a un agent IA un acces illimite a des outils, APIs, ou donnees. Appliquer le principe de moindre privilege. Plafonner le nombre d'actions par session, le budget API, les permissions filesystem.

- **Ignoring low-probability high-impact risks** : Les risques rares mais catastrophiques (data breach via LLM, generation de contenu illegal, manipulation de decisions critiques) meritent une attention disproportionnee. Ne pas les ignorer parce qu'ils sont "peu probables".

## Implementation Workflow

### Phase 1 : Identification et cartographie des risques

1. Inventorier tous les systemes IA en production et en developpement
2. Categoriser chaque systeme selon la taxonomie des risques (technique, securitaire, operationnel, reputationnel, legal, ethique)
3. Conduire un threat modeling specifique IA (STRIDE adapte + risques LLM)
4. Documenter les scenarios de risque avec probabilite et impact
5. Etablir le registre des risques initial

### Phase 2 : Evaluation et priorisation

1. Appliquer la matrice probabilite x impact a chaque risque identifie
2. Conduire des evaluations techniques : tests de robustesse, red teaming initial, audit des donnees
3. Evaluer les risques supply chain (modeles, datasets, librairies)
4. Prioriser les risques et definir les seuils d'acceptation
5. Valider avec les parties prenantes et obtenir l'approbation formelle du risque residuel

### Phase 3 : Mitigation et controles

1. Implementer les defenses multi-couches pour les risques critiques et eleves
2. Deployer le monitoring de production (performance, qualite, securite, drift)
3. Configurer les kill switches et les mecanismes de graceful degradation
4. Mettre en place les alertes et les seuils d'escalade
5. Documenter les procedures de reponse aux incidents specifiques IA

### Phase 4 : Monitoring continu et amelioration

1. Executer le programme de red teaming continu (automatise + humain)
2. Monitorer les metriques de risque en temps reel (hallucination rate, drift score, blocked requests)
3. Revoir le registre des risques mensuellement
4. Integrer les retours des incidents et near-misses
5. Mettre a jour les defenses face aux nouvelles menaces (jailbreaks, techniques d'attaque emergentes)
6. Conduire des revues post-incident (blameless post-mortems) pour chaque incident IA

## Additional Resources

Consulter les fichiers de reference pour un approfondissement detaille :

- **[Risk Taxonomy](./references/risk-taxonomy.md)** : NIST AI RMF approfondi (govern, map, measure, manage), categories de risques IA detaillees, frameworks d'evaluation des risques, matrices probabilite x impact, monitoring des risques, acceptation du risque residuel.

- **[Adversarial Robustness](./references/adversarial-robustness.md)** : Attaques adversariales (evasion, poisoning, model stealing, backdoor), entrainement adversarial et defenses, red teaming des systemes IA, benchmarks de robustesse, validation des inputs pour LLMs, attaques de prompt injection et defenses.

- **[AI Safety & Alignment](./references/ai-safety-alignment.md)** : Fondamentaux de la safety IA, Constitutional AI, RLHF/DPO/RLAIF, filtrage et moderation de contenu, prevention des outputs nocifs, reponse aux incidents pour les systemes IA, kill switches et degradation gracieuse, paysage de la recherche en alignement.

- **[Operational Risks](./references/operational-risks.md)** : Detection et grounding des hallucinations, model drift (data drift, concept drift, performance decay), attenuation du vendor lock-in, gestion des couts, optimisation de la latence, disponibilite et redondance, bases de donnees d'incidents IA (AIAAIC), risques lies aux deepfakes.
