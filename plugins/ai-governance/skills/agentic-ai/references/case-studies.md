# Etudes de Cas — Agents IA en Production

## Introduction

Ces quatre etudes de cas documentent des deployments reels d'agents IA en entreprise. Chaque cas couvre le contexte metier, les choix architecturaux, les guardrails implementes, les resultats mesures et les lecons applicables a d'autres projets similaires. Les architectures sont suffisamment detaillees pour servir de reference lors de projets analogues.

---

## Cas 1 — Agent de Support Client Tier 1 : 70% d'Automatisation

### Contexte et Problematique

**Entreprise** : SaaS B2B de gestion de projets, 400 clients, plan tarifaire $50-500/mois.
**Volume** : 5 000 tickets/mois via Zendesk, segmentes en trois categories : questions produit (45%), problemes techniques (35%), demandes administratives (20%).
**Equipe initiale** : 8 agents support, temps de reponse moyen 4 heures, cout par ticket $18, taux d'escalade Tier 2 : 40%.
**Probleme central** : 60% des tickets Tier 1 suivaient des scripts repetitifs documentables. L'equipe perdait du temps sur des cas resolus identiquement 50 fois par semaine.

**Objectif** : automatiser 50-70% des tickets Tier 1 sans degrader le NPS (Net Promoter Score), liberer les agents pour les cas complexes a forte valeur.

### Architecture Technique

```
[Zendesk Webhook] → [Classification Agent] → [Resolution Agent] → [Escalation Router]
                           |                        |                     |
                    [Ticket DB]              [Knowledge RAG]        [Human Queue]
                    [Customer CRM]           [Ticket History]       [Zendesk API]
```

**Stack** : LangChain (ReAct agent), GPT-4o pour la resolution, GPT-4o-mini pour la classification, ChromaDB pour le RAG de la base de connaissances (450 articles, 2 300 chunks).

**Tools disponibles** :
- `lookup_customer` : infos compte, abonnement, historique tickets
- `search_knowledge_base` : RAG sur la documentation produit
- `check_known_issues` : bugs et incidents en cours
- `update_ticket_status` : modifier le statut Zendesk
- `send_response` : envoyer une reponse au client
- `escalate_to_human` : transferer avec contexte resume

### Workflow Detaille

```python
from langchain.agents import create_react_agent, AgentExecutor
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Literal

class TicketClassification(BaseModel):
    category: Literal["product_question", "technical_issue", "admin_request", "complaint", "out_of_scope"]
    urgency: Literal["low", "medium", "high", "critical"]
    complexity: Literal["simple", "medium", "complex"]
    confidence: float = Field(ge=0, le=1)
    auto_resolvable: bool

def process_ticket(ticket: dict) -> dict:
    # Etape 1 : Classification rapide (GPT-4o-mini, < 1s)
    classification = classify_ticket(ticket["subject"], ticket["body"])

    # Seuil de confiance : ne pas tenter l'auto-resolution si incertitude
    if not classification.auto_resolvable or classification.confidence < 0.85:
        return escalate(ticket, reason="Complexite ou incertitude elevee", classification=classification)

    if classification.complexity == "complex":
        return escalate(ticket, reason="Complexite trop elevee pour auto-resolution", classification=classification)

    # Etape 2 : Resolution par l'agent ReAct
    agent_result = resolution_agent.invoke({
        "input": f"""
Ticket #{ticket['id']} — {classification.category}
Client: {ticket['customer_email']}
Sujet: {ticket['subject']}
Message: {ticket['body']}

Resous ce ticket en suivant le protocole support. Si tu ne peux pas resoudre avec confiance > 0.8, escalade.
"""
    })

    # Etape 3 : Verification du resultat
    if agent_result.get("confidence", 0) < 0.8:
        return escalate(ticket, reason="Confiance resolution insuffisante", agent_output=agent_result)

    # Etape 4 : Envoi reponse et cloture
    send_response(ticket["id"], agent_result["response"])
    close_ticket(ticket["id"], auto_resolved=True)

    return {
        "status": "auto_resolved",
        "ticket_id": ticket["id"],
        "category": classification.category,
        "resolution_time_s": agent_result.get("duration_s")
    }
```

### Guardrails Implementes

**Guardrail 1 — Seuil de confiance** : l'agent estime sa confiance apres chaque resolution. En dessous de 0.8, escalade systematique avec contexte complet. Ce seuil unique a ete le parametre le plus impactant sur le taux d'escalade inappropriee.

**Guardrail 2 — Refus hors-scope** : liste de categories bloquees (reclamations juridiques, demandes de remboursement > $500, sujets sensibles). Detection via classifier rapide avant tout traitement.

**Guardrail 3 — Logging exhaustif** : chaque ticket automatise est enregistre avec : classification, tools appeles, reponse generee, score de confiance. Review hebdomadaire par le lead support.

**Guardrail 4 — Pas d'action irreversible sans confirmation** : l'agent peut envoyer des reponses informatives mais ne peut pas modifier l'abonnement, emettre de remboursement ou supprimer des donnees — ces actions sont reservees aux humains.

**Guardrail 5 — Escalade transparente** : quand l'agent escalade, il transmet un resume structure (contexte client, tentatives de resolution, raison d'escalade). Les agents humains voient exactement ce que l'IA a deja essaye.

### Resultats Mesures (apres 90 jours)

| Metrique | Avant | Apres | Evolution |
|----------|-------|-------|-----------|
| Tickets auto-resolus | 0% | 70% | +70pts |
| Temps de reponse moyen | 4h | 8 min (auto) / 2h (humain) | -87% auto |
| Cout par ticket | $18 | $4.20 (moyen pondere) | -77% |
| NPS | 42 | 44 | +2pts (stable) |
| Escalades Tier 2 | 40% | 18% | -22pts |
| Agents redeploys | 0 | 3 (en support complexe) | — |

**Incidents post-deployment** : 12 reponses incorrectes detectees sur les 90 premiers jours (0.5% des tickets auto-resolus), toutes corrigees dans l'heure par les humains notifies. Aucun impact client majeur.

### Lecons Applicables

**Commencer par les cas simples et frequents** : les 20% de cas les plus frequents representaient 60% du volume. Automatiser ces cas en premier a maximise l'impact avec un risque minimal.

**Le seuil de confiance est le parametre critique** : trop haut (> 0.9), trop peu de tickets resolus automatiquement. Trop bas (< 0.7), trop d'erreurs. Calibrer sur un echantillon de 500 tickets historiques.

**La qualite du RAG determine la qualite des reponses** : le premier mois, 40% des erreurs venaient d'une base de connaissances mal structuree. Investir dans la qualite et la fraicheur des documents avant de deployer l'agent.

**Redeployer, ne pas supprimer** : les 3 agents liberes sont passes sur du support complexe (integration API clients, onboarding enterprise). Le NPS sur ces segments a augmente de 8 points.

---

## Cas 2 — Pipeline d'Intelligence Competitive Multi-Agents

### Contexte et Problematique

**Entreprise** : scale-up SaaS RH, Series B, 8 concurrents directs identifies.
**Equipe** : 2 analysts en charge strategique + directeur strategie.
**Situation initiale** : veille competitive artisanale — 8 heures par semaine par analyst pour surveiller les news, les mouvements produit, les levees de fonds, les offres d'emploi (signal d'intention) et les avis clients (G2, Capterra).
**Probleme** : information souvent obsolete (> 1 semaine), couverture partielle (impossible de suivre 8 concurrents completement manuellement), biais de selection des analysts.

**Objectif** : rapport de veille competitive complet, livre chaque lundi matin a 8h, avec < 20 minutes de review humaine.

### Architecture Multi-Agents (LangGraph)

```
                        ┌─────────────────┐
                        │  Orchestrator   │
                        │  (Supervisor)   │
                        └────────┬────────┘
              ┌──────────────────┼──────────────────┐
              ▼                  ▼                  ▼
    ┌─────────────────┐ ┌───────────────┐ ┌─────────────────┐
    │  web_researcher  │ │  fin_analyzer │ │ product_tracker │
    │  (news, blogs,  │ │  (SEC, Crunch,│ │  (changelogs,   │
    │   LinkedIn,     │ │   LinkedIn    │ │   releases,     │
    │   job postings) │ │   funding)    │ │   pricing)      │
    └─────────────────┘ └───────────────┘ └─────────────────┘
              └──────────────────┬──────────────────┘
                                 ▼
                    ┌─────────────────────────┐
                    │    synthesis_writer      │
                    │  (rapport Notion auto)  │
                    └─────────────────────────┘
```

**4 agents specialises** :
- `web_researcher` : scraping news, blogs sectoriels, LinkedIn updates, offres d'emploi (signal de croissance ou pivot)
- `financial_analyzer` : levees de fonds (Crunchbase, TechCrunch), financements publics, indicateurs financiers publics
- `product_tracker` : changelogs produit, nouvelles features, modifications de pricing, integrations partenaires
- `synthesis_writer` : consolidation, analyse, redaction du rapport final Notion

### Implementation LangGraph

```python
from langgraph.graph import StateGraph, END
from langgraph.types import Send
from pydantic import BaseModel, Field
from typing import dict, list, Optional
from datetime import datetime, timedelta

class CompetitiveIntelState(BaseModel):
    competitors: list[str]
    time_window_days: int = 7
    web_research: dict[str, str] = {}          # competitor -> findings
    financial_data: dict[str, str] = {}
    product_updates: dict[str, str] = {}
    synthesis: str = ""
    notion_page_id: Optional[str] = None

def parallel_research_dispatcher(state: CompetitiveIntelState) -> list[Send]:
    """Lance 3 agents en parallele pour chaque concurrent."""
    sends = []
    for competitor in state.competitors:
        sends.extend([
            Send("web_researcher", {"competitor": competitor, "days": state.time_window_days}),
            Send("financial_analyzer", {"competitor": competitor, "days": state.time_window_days}),
            Send("product_tracker", {"competitor": competitor, "days": state.time_window_days})
        ])
    return sends

def web_researcher_node(inputs: dict) -> dict:
    competitor = inputs["competitor"]
    days = inputs["days"]
    # Outils : Tavily Search, LinkedIn Scraper, Indeed API (offres emploi)
    findings = research_web_sources(competitor, days)
    return {"web_research": {competitor: findings}}

def financial_analyzer_node(inputs: dict) -> dict:
    competitor = inputs["competitor"]
    # Outils : Crunchbase API, SEC EDGAR, PitchBook (si acces)
    financials = fetch_financial_data(competitor, inputs["days"])
    return {"financial_data": {competitor: financials}}

def product_tracker_node(inputs: dict) -> dict:
    competitor = inputs["competitor"]
    # Outils : scraping changelog pages, G2/Capterra reviews, Product Hunt
    updates = track_product_changes(competitor, inputs["days"])
    return {"product_updates": {competitor: updates}}

def synthesis_writer_node(state: CompetitiveIntelState) -> CompetitiveIntelState:
    """Consolide toutes les donnees et genere le rapport."""
    prompt = f"""Tu es un analyste strategique senior.
Voici les donnees de veille competitive de la semaine (du {(datetime.now() - timedelta(days=7)).strftime('%Y-%m-%d')} a aujourd'hui) :

RECHERCHE WEB:
{format_dict(state.web_research)}

DONNEES FINANCIERES:
{format_dict(state.financial_data)}

EVOLUTIONS PRODUIT:
{format_dict(state.product_updates)}

Redige un rapport de veille strategique structure :
1. Executive Summary (3 signaux majeurs de la semaine)
2. Par concurrent : activite, signaux, interpretation
3. Implications strategiques et recommandations
4. Alertes a surveiller la semaine prochaine"""

    report = llm.invoke(prompt).content
    notion_id = publish_to_notion(report, title=f"Veille Competitive — {datetime.now().strftime('%Y-W%W')}")
    send_slack_notification(f"Rapport veille competitive disponible : {notion_id}")

    return CompetitiveIntelState(**{**state.model_dump(), "synthesis": report, "notion_page_id": notion_id})

# Execution hebdomadaire via cron job ou Airflow
workflow = StateGraph(CompetitiveIntelState)
workflow.add_node("dispatcher", parallel_research_dispatcher)
workflow.add_node("web_researcher", web_researcher_node)
workflow.add_node("financial_analyzer", financial_analyzer_node)
workflow.add_node("product_tracker", product_tracker_node)
workflow.add_node("synthesis_writer", synthesis_writer_node)

workflow.set_entry_point("dispatcher")
workflow.add_edge("web_researcher", "synthesis_writer")
workflow.add_edge("financial_analyzer", "synthesis_writer")
workflow.add_edge("product_tracker", "synthesis_writer")
workflow.add_edge("synthesis_writer", END)

app = workflow.compile()
```

### Resultats Mesures (apres 60 jours)

| Metrique | Avant | Apres | Evolution |
|----------|-------|-------|-----------|
| Temps analyst/semaine | 8h x 2 = 16h | 20 min review x 2 | -97% |
| Concurrents couverts | 4-5 (partiel) | 8 (complet) | +60-100% |
| Fraicheur des donnees | < 1 semaine | < 24h | -85% delai |
| Signaux detectes/semaine | ~15 | ~75 | +5x |
| Precision signaux importants | 70% (estime) | 82% (valide par analysts) | +12pts |

**Cout operationnel** : $45/semaine en API LLM + $20 en outils de scraping = $65/semaine vs 16h x $80/h = $1 280/semaine precedemment. ROI < 1 mois.

### Lecons Applicables

**Les multi-agents brillent pour les taches avec sources heterogenes** : la separation web/finance/produit n'etait pas arbitraire — chaque agent avait des tools et un prompt systeme optimises pour son domaine. Un agent unique avec tous les tools etait 30% moins precis dans les tests A/B.

**La parallelisation est le vrai gain de performance** : sans parallelisme, 8 concurrents x 3 types d'analyse = 24 appels sequentiels (~40 minutes). Avec Send API en parallele : ~8 minutes.

**La qualite du rapport depend du prompt du synthesis_writer** : investir 80% du temps de prompt engineering sur l'agent de synthese, pas sur les agents de collecte.

**Prevoir une boucle de feedback** : les analysts ajoutent des annotations au rapport Notion. Ces annotations alimentent le fine-tuning du synthesis_writer via few-shot examples mis a jour mensuellement.

---

## Cas 3 — Agent de Code Review Automatique

### Contexte et Problematique

**Equipe** : 20 developpeurs, stack Python/FastAPI + React, 30-40 PRs par semaine.
**Probleme** : temps d'attente moyen pour une premiere review : 6 heures. Les reviewers humains, satures, manquaient des issues de securite et de performance sur 35% des PRs (mesure via audit retrospectif).
**Contrainte critique** : ne jamais bloquer une PR automatiquement, ne jamais approuver sans validation humaine. L'agent est un assistant, pas un decision-maker.

**Objectif** : premier feedback sous 5 minutes apres ouverture de PR, qualite superieure au feedback humain sur les categories systematisables (securite, style, tests manquants).

### Architecture LangGraph avec Integration GitHub

```
[GitHub PR Opened] → [GitHub Actions Webhook]
                              |
                    ┌─────────▼─────────┐
                    │   code_analyzer   │
                    │  (diff parsing,   │
                    │   AST analysis)   │
                    └─────────┬─────────┘
                    ┌─────────▼─────────┐
                    │ security_checker  │
                    │  (OWASP top 10,  │
                    │   secrets, SQLi) │
                    └─────────┬─────────┘
                    ┌─────────▼─────────┐
                    │  test_suggester   │
                    │ (coverage gaps,  │
                    │  edge cases)     │
                    └─────────┬─────────┘
                    ┌─────────▼─────────┐
                    │  feedback_writer  │
                    │ (PR comment      │
                    │  formate MD)     │
                    └─────────┬─────────┘
                              |
                    [GitHub PR Comment API]
```

### Implementation

```python
from langgraph.graph import StateGraph, END
from pydantic import BaseModel, Field
from typing import list, Optional
import ast
import re

class PRReviewState(BaseModel):
    pr_id: str
    pr_title: str
    pr_description: str
    diff: str
    files_changed: list[str]
    code_analysis: str = ""
    security_issues: list[dict] = []
    test_suggestions: list[str] = []
    performance_notes: list[str] = []
    final_feedback: str = ""
    severity: str = "info"  # info, warning, critical

def code_analyzer_node(state: PRReviewState) -> PRReviewState:
    prompt = f"""Analyse ce diff de code Python/TypeScript.
Identifie : complexite cyclomatique elevee, duplications, violations de separation of concerns,
anti-patterns, fonctions trop longues (> 50 lignes), nommage confus.

DIFF:
{state.diff[:8000]}  # Limite pour le contexte

Sois specifique : ligne, fichier, probleme exact, suggestion d'amelioration."""

    analysis = llm.invoke(prompt).content
    return PRReviewState(**{**state.model_dump(), "code_analysis": analysis})

def security_checker_node(state: PRReviewState) -> PRReviewState:
    # Regex pre-screening pour patterns dangereux (rapide, avant LLM)
    danger_patterns = {
        "sql_injection": r"f['\"].*SELECT.*{.*}",
        "hardcoded_secret": r"(password|api_key|secret|token)\s*=\s*['\"][^'\"]{8,}['\"]",
        "eval_usage": r"\beval\s*\(",
        "shell_injection": r"os\.system|subprocess\.call.*shell=True",
        "path_traversal": r"open\s*\([^)]*\.\./",
        "xxe_risk": r"etree\.parse|minidom\.parse"
    }

    pre_scan_findings = []
    for vuln_type, pattern in danger_patterns.items():
        matches = re.findall(pattern, state.diff, re.IGNORECASE)
        if matches:
            pre_scan_findings.append({"type": vuln_type, "count": len(matches)})

    # LLM pour analyse approfondie (OWASP Top 10 contextualisee)
    prompt = f"""Tu es un expert securite applicative (OWASP, SANS).
Pre-scan detecte : {pre_scan_findings}

Analyse ce diff pour : injection (SQL, commande, LDAP), broken auth, exposition de donnees sensibles,
XXE, acces non-authorise, misconfiguration securite, XSS, deserialisation, composants vulnerables, logging inadequat.

DIFF:
{state.diff[:6000]}

Pour chaque issue : localisation exacte, severite (LOW/MEDIUM/HIGH/CRITICAL), remediation concrete."""

    security_analysis = llm.invoke(prompt).content

    # Parse la severite maximale
    severity = "info"
    if "CRITICAL" in security_analysis.upper():
        severity = "critical"
    elif "HIGH" in security_analysis.upper():
        severity = "high"
    elif "MEDIUM" in security_analysis.upper():
        severity = "medium"

    security_issues = [{"analysis": security_analysis, "pre_scan": pre_scan_findings}]
    return PRReviewState(**{**state.model_dump(), "security_issues": security_issues, "severity": severity})

def test_suggester_node(state: PRReviewState) -> PRReviewState:
    prompt = f"""Analyste QA expert. Pour ce diff, identifie :
1. Les cas limites (edge cases) non testes
2. Les cas d'erreur non geres (exceptions, timeouts, donnees nulles)
3. Les tests d'integration manquants
4. Les tests de regression necessaires suite a ces changements

Sois concret : fournis des noms de fonctions de test et les assertions cles.

DIFF:
{state.diff[:6000]}"""

    suggestions = llm.invoke(prompt).content
    return PRReviewState(**{**state.model_dump(), "test_suggestions": [suggestions]})

def feedback_writer_node(state: PRReviewState) -> PRReviewState:
    severity_emoji = {"info": "ℹ", "medium": "⚠", "high": "🔴", "critical": "🚨"}
    emoji = severity_emoji.get(state.severity, "ℹ")

    feedback = f"""## {emoji} Code Review Automatique — {state.pr_title}

> **Note** : Ce feedback est genere automatiquement. Il assiste le reviewer humain et ne remplace pas sa validation.

### Analyse du Code
{state.code_analysis}

### Securite
{state.security_issues[0]['analysis'] if state.security_issues else 'Aucune issue detectee.'}

### Couverture de Tests
{state.test_suggestions[0] if state.test_suggestions else 'Tests semblent adequats.'}

---
*Agent de code review v2.1 — Modele: GPT-4o — Temps d'execution: {'{execution_time}'}s*
*Pour contester ce feedback : commenter `/review-feedback incorrect`*"""

    return PRReviewState(**{**state.model_dump(), "final_feedback": feedback})

# Publication sur GitHub PR
def post_pr_comment(pr_id: str, feedback: str, severity: str):
    import requests
    headers = {"Authorization": f"Bearer {GITHUB_TOKEN}", "Accept": "application/vnd.github.v3+json"}
    payload = {"body": feedback}

    # Ne jamais REQUEST_CHANGES automatiquement — uniquement COMMENT
    response = requests.post(
        f"https://api.github.com/repos/{REPO}/pulls/{pr_id}/reviews",
        json={"body": feedback, "event": "COMMENT"},  # JAMAIS "REQUEST_CHANGES" ou "APPROVE"
        headers=headers
    )
    return response.json()
```

### Resultats Mesures (apres 120 jours)

| Metrique | Avant | Apres | Evolution |
|----------|-------|-------|-----------|
| Temps premier feedback | 6h | 4 min | -98% |
| Security issues detectees/mois | 12 | 19 | +58% |
| Issues manquees par reviewer | 35% | 18% | -17pts |
| Temps review humaine moyenne | 45 min | 28 min | -38% |
| Satisfaction developpeurs | 6.2/10 | 7.8/10 | +1.6pts |

**Incidents** : 3 faux positifs de securite en 4 mois (analyse incorrecte), tous corriges par le reviewer humain. 0 approbation automatique incorrecte (gardrail maintenu strictement).

### Lecons Applicables

**Les agents d'assistance sont plus surs que les agents autonomes pour le code** : la contrainte "commentaire uniquement, jamais d'approbation ou de blocage" n'etait pas optionnelle. Elle a ete la seule condition d'adoption par l'equipe. Les developpeurs acceptent l'aide IA mais rejettent l'autonomie IA sur les decisions de merge.

**Le pre-screening regex avant LLM economise 30% des tokens** : les patterns de securite evidents (SQL injection patterns, secrets hardcodes) sont detectes en millisecondes par regex. Le LLM se concentre sur les issues complexes que le regex ne peut pas detecter.

**Integrer le feedback loop des le debut** : la commande `/review-feedback incorrect` permettait aux devs de signaler les faux positifs. Ces signaux ont permis d'ameliorer le prompt en 3 iterations sur 60 jours.

---

## Cas 4 — Agent de Data Analysis : Self-Service BI

### Contexte et Problematique

**Equipe** : 2 data analysts pour 200 employes dans une scale-up e-commerce.
**Volume** : 50 demandes ad-hoc par mois (Slack : "combien de clients actifs en France en janvier ?", "quelle est notre LTV moyenne par canal acquisition ?").
**Probleme** : chaque demande simple prenait 30-120 minutes (comprehension du besoin, ecriture SQL, validation, export, reponse). Les analysts etaient en permanence interrompus par ces demandes simples au detriment des analyses strategiques.

**Objectif** : les employes non-techniques posent leurs questions en langage naturel et obtiennent une reponse avec visualisation en < 5 minutes. Les analysts ne traitent que les demandes complexes.

### Architecture Plan-Execute avec Sandbox

```
[Slack Message] → [Intent Parser] → [SQL Generator] → [Human Validation*]
                                                               |
                                    ┌──────────────────────────┘
                                    ▼
                             [SQL Executor]
                             (production DB)
                                    |
                             [Python Analyzer]
                             (sandbox E2B)
                                    |
                             [Viz Generator]
                             (matplotlib/plotly)
                                    |
                             [Slack Responder]

*Validation humaine uniquement pour les requetes sur les tables sensibles (RH, finance)
```

### Implementation Plan-Execute

```python
from pydantic import BaseModel, Field
from typing import Literal, Optional
from e2b_code_interpreter import Sandbox
import sqlparse

class DataRequest(BaseModel):
    original_question: str
    user_id: str
    channel: str

class QueryPlan(BaseModel):
    approach: str = Field(description="Explication de l'approche en langage naturel")
    sql_query: str = Field(description="Requete SQL pour extraire les donnees")
    requires_python: bool = Field(description="True si une transformation Python est necessaire")
    python_code: Optional[str] = Field(description="Code Python pour analyse/visualisation")
    visualization_type: Literal["table", "bar_chart", "line_chart", "pie_chart", "none"]
    sensitive_tables: list[str] = Field(description="Tables sensibles utilisees (RH, finance, etc.)")
    requires_human_validation: bool

# Schema de la base de donnees injecte dans le contexte
DB_SCHEMA = """
Tables disponibles:
- orders (id, customer_id, created_at, total_amount, status, channel, country)
- customers (id, email, created_at, country, acquisition_channel, lifetime_value)
- products (id, name, category, price, stock_quantity)
- order_items (order_id, product_id, quantity, unit_price)
- web_sessions (session_id, customer_id, created_at, source, pages_visited, duration_s)

Tables SENSIBLES (validation humaine requise):
- employees (id, name, salary, department, hire_date) — RH
- financial_statements (period, revenue, costs, ebitda) — Finance
"""

def generate_query_plan(request: DataRequest) -> QueryPlan:
    prompt = f"""Tu es un expert SQL et data analyst. Genere un plan d'execution pour cette question.

SCHEMA BASE DE DONNEES:
{DB_SCHEMA}

QUESTION: {request.original_question}

Regles:
- N'utilise QUE les tables documentees dans le schema
- Limite automatiquement : LIMIT 10000 sur toutes les requetes
- Ajoute requires_human_validation = True si tables sensibles utilisees
- Le code Python doit etre autonome et produire un fichier image si visualisation"""

    return planner_llm.with_structured_output(QueryPlan).invoke(prompt)

def validate_sql_safety(sql: str) -> tuple[bool, str]:
    """Validation syntaxique et securite avant execution."""
    parsed = sqlparse.parse(sql)

    # Bloquer toutes les modifications
    forbidden_keywords = ["INSERT", "UPDATE", "DELETE", "DROP", "CREATE", "ALTER", "TRUNCATE", "GRANT"]
    sql_upper = sql.upper()

    for keyword in forbidden_keywords:
        if keyword in sql_upper:
            return False, f"Requete de modification refusee : {keyword}"

    # Verifier la presence du LIMIT
    if "LIMIT" not in sql_upper:
        return False, "LIMIT manquant — requete refusee pour protection ressources"

    return True, "OK"

def execute_analysis_pipeline(request: DataRequest) -> dict:
    # Etape 1 : Planification
    plan = generate_query_plan(request)
    print(f"Plan: {plan.approach}")

    # Etape 2 : Validation humaine si tables sensibles
    if plan.requires_human_validation:
        return request_human_validation(request, plan)

    # Etape 3 : Validation securite SQL
    is_safe, reason = validate_sql_safety(plan.sql_query)
    if not is_safe:
        return {"error": f"Requete bloquee : {reason}", "plan": plan.approach}

    # Etape 4 : Execution SQL (lecture seule sur replica)
    data = execute_on_read_replica(plan.sql_query)

    if data.get("error"):
        # Re-planification en cas d'erreur SQL
        corrected_plan = replan_on_error(plan, data["error"])
        data = execute_on_read_replica(corrected_plan.sql_query)

    # Etape 5 : Analyse Python dans sandbox securise
    if plan.requires_python and plan.python_code:
        with Sandbox() as sandbox:
            # Injection des donnees dans le sandbox
            sandbox.files.write("/data/results.json", json.dumps(data["rows"]))

            # Code Python de l'agent + import des donnees
            full_code = f"""
import json
import pandas as pd
import matplotlib.pyplot as plt

data = json.load(open('/data/results.json'))
df = pd.DataFrame(data)

{plan.python_code}

plt.tight_layout()
plt.savefig('/output/chart.png', dpi=150, bbox_inches='tight')
print("STATS:", df.describe().to_string())
"""
            execution = sandbox.run_code(full_code)
            chart_data = sandbox.files.read("/output/chart.png")
    else:
        chart_data = None

    # Etape 6 : Formatage et envoi Slack
    response = format_and_send_slack(
        channel=request.channel,
        question=request.original_question,
        data=data,
        chart=chart_data,
        plan_summary=plan.approach
    )

    return {"status": "success", "rows_analyzed": len(data.get("rows", [])), "slack_ts": response["ts"]}

def request_human_validation(request: DataRequest, plan: QueryPlan) -> dict:
    """Workflow de validation humaine pour requetes sensibles."""
    validation_msg = f"""*Validation requise* pour la requete de {request.user_id} :

Question : {request.original_question}
Tables sensibles : {', '.join(plan.sensitive_tables)}
SQL propose :
```sql
{plan.sql_query}
```

Approuver ? /approve ou /reject"""

    send_slack_to_data_team(validation_msg)
    return {"status": "pending_validation", "message": "Demande transmise aux data analysts pour validation (tables sensibles detectees)"}
```

### Resultats Mesures (apres 90 jours)

| Metrique | Avant | Apres | Evolution |
|----------|-------|-------|-----------|
| Demandes traitees sans analyst | 0% | 62% | +62pts |
| Temps de reponse (simples) | 45 min | 4 min | -91% |
| Demandes/mois traitees | 50 | 85 (+35% adoption) | +70% |
| Temps analyst sur demandes ad-hoc | ~40h/mois | ~15h/mois | -62% |
| Erreurs SQL detectees avant exec | 0 | 100% (validation systeme) | — |
| Incidents donnees sensibles | — | 0 | — |

**Adoption** : 68% des employes non-techniques utilisent l'agent au moins 1 fois par semaine apres 30 jours (objectif initial : 40%).

### Lecons Applicables

**Le human-in-the-loop sur les operations critiques est indispensable** : la validation humaine sur les tables sensibles n'a pas ete percue comme une friction — elle a ete percue comme une protection. Les employees non-techniques apprecient de savoir qu'un humain valide les requetes sur les donnees RH et financieres.

**Executer sur un replica de lecture, jamais sur la production** : la separation replica/prod n'est pas optionnelle. Meme avec un SQL SELECT, une requete mal ecrite peut saturer les ressources de la base principale. Le replica isole les risques.

**La re-planification sur erreur SQL est critique** : 18% des premieres tentatives SQL echouaient (schema mal compris, alias incorrects). Sans re-planification, le taux de succes tombait a 65%. Avec re-planification automatique, il monte a 89%.

**Monitorer les requetes les plus frequentes** : les 10 questions les plus posees representaient 55% du volume. Les convertir en dashboards statiques a reduit la charge de l'agent de 30% et ameliore la latence pour les cas frequents.

---

## Synthese Cross-Cas

### Patterns Recurrents de Succes

**Commencer par le perimetre le plus contraint** : chaque projet a commence avec un perimetre reduit (support Tier 1 uniquement, veille sur 2 concurrents, review Python uniquement, requetes SQL simples). L'expansion progressive a permis de valider la confiance sans risque majeur.

**Human-in-the-loop non-negociable sur les irreversibles** : remboursements, approbations de code, requetes sur donnees sensibles, envois massifs — ces actions restent humaines dans tous les cas documentes. L'IA est un amplificateur de productivite, pas un remplacant pour les decisions irreversibles.

**La qualite des donnees d'entrainement/context determine la qualite de sortie** : base de connaissances support (Cas 1), schema DB complet avec descriptions (Cas 4), contexte concurrent riche (Cas 2). Investir dans la qualite du contexte retourne 10x sur la qualite des reponses.

**Mesurer avant d'optimiser** : les quatre projets ont commence avec un baseline mesure sur 30-60 jours historiques. Sans baseline, impossible de prouver la valeur ou d'identifier les axes d'amelioration.

### Referentiel de ROI par Type d'Agent

| Type d'agent | Complexite implementation | Delai ROI | ROI 12 mois |
|--------------|--------------------------|-----------|-------------|
| Support Tier 1 | Moyenne | 2-3 mois | 5-10x |
| Veille competitive | Elevee (multi-agents) | 1 mois | 15-20x |
| Code review assistance | Moyenne | 3-4 mois | 3-5x |
| Self-service BI | Elevee | 2-3 mois | 8-12x |

Ces chiffres sont indicatifs — le ROI reel depend fortement de la qualite d'implementation, du volume traite et de la maturite data/process de l'entreprise.
