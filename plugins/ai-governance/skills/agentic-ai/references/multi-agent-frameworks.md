# Frameworks Multi-Agents — LangGraph, CrewAI et AutoGen

## Pourquoi les Systemes Multi-Agents

Un agent unique presente des limitations structurelles : fenetre de contexte saturee sur les longues taches, impossibilite de se specialiser dans plusieurs domaines simultanement, et absence de verification croisee. Les systemes multi-agents repondent a ces contraintes avec trois benefices majeurs.

**Parallelisme** : plusieurs agents travaillent simultanement sur des sous-taches independantes. Un agent qui scrape des donnees financieres pendant qu'un autre analyse les news reduit la latence totale de 60-70%.

**Specialisation** : chaque agent dispose d'un prompt systeme, de tools et d'un LLM adaptes a son domaine. Un agent SQL avec acces base de donnees, un agent Python avec sandbox d'execution, un agent redacteur avec memoire stylistique — chacun excelle dans son perimetre.

**Verification croisee** : un agent relit le travail d'un autre, detecte les erreurs, contradictions et hallucinations. Ce pattern "critique" est statistiquement plus efficace qu'une auto-correction par le meme agent.

Le cout : complexite de coordination, debugging plus difficile, risque de boucles et de conflicts entre agents. Ne pas utiliser les multi-agents par defaut — evaluer d'abord si un agent unique bien concu suffit.

---

## LangGraph

### Architecture

LangGraph modelise un workflow d'agents comme un graphe dirige avec etat partage. Chaque noeud est une fonction (ou un agent LLM). Les aretes definissent les transitions, qui peuvent etre conditionnelles (routing dynamique).

Concept cle : le **State** — un objet Pydantic partage entre tous les noeuds. Chaque noeud lit l'etat, le modifie, et passe la main selon les aretes definies.

### Code Complet : Workflow Editorial

```python
from langgraph.graph import StateGraph, END
from langgraph.checkpoint.memory import MemorySaver
from langchain_openai import ChatOpenAI
from langchain_core.prompts import ChatPromptTemplate
from pydantic import BaseModel, Field
from typing import Optional, Annotated
import operator

# Definition de l'etat partage
class EditorialState(BaseModel):
    topic: str
    research_notes: str = ""
    draft: str = ""
    review_feedback: str = ""
    final_article: str = ""
    revision_count: int = 0
    is_approved: bool = False

# LLMs specialises
fast_llm = ChatOpenAI(model="gpt-4o-mini", temperature=0.3)
quality_llm = ChatOpenAI(model="gpt-4o", temperature=0.2)

# Node 1 : Research Agent
def research_agent(state: EditorialState) -> EditorialState:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un chercheur expert. Fournis des informations factuelles, denses et sourcees sur le sujet donne."),
        ("user", f"Sujet: {state.topic}\n\nFournis des notes de recherche completes : chiffres cles, contexte, tendances, sources.")
    ])
    chain = prompt | fast_llm
    result = chain.invoke({})
    return EditorialState(**{**state.model_dump(), "research_notes": result.content})

# Node 2 : Writing Agent
def write_agent(state: EditorialState) -> EditorialState:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un redacteur expert. Redige des articles clairs, structures et engageants."),
        ("user", f"""Sujet: {state.topic}
Notes de recherche: {state.research_notes}
Feedback precedent (si revision): {state.review_feedback}

Redige un article de 800 mots structure avec introduction, 3 sections principales et conclusion.""")
    ])
    chain = prompt | quality_llm
    result = chain.invoke({})
    return EditorialState(**{**state.model_dump(), "draft": result.content})

# Node 3 : Review Agent
class ReviewDecision(BaseModel):
    feedback: str = Field(description="Critique detaillee et suggestions d'amelioration")
    approved: bool = Field(description="True si l'article peut etre publie tel quel")
    quality_score: int = Field(ge=1, le=10)

def review_agent(state: EditorialState) -> EditorialState:
    prompt = ChatPromptTemplate.from_messages([
        ("system", "Tu es un editeur senior avec 20 ans d'experience. Tes critiques sont constructives et precises."),
        ("user", f"""Sujet: {state.topic}
Article a evaluer:
{state.draft}

Evalue : exactitude factuelle, clarte, structure, engagement lecteur, qualite redactionnelle.""")
    ])
    chain = prompt | quality_llm.with_structured_output(ReviewDecision)
    review = chain.invoke({})

    updates = {
        "review_feedback": review.feedback,
        "is_approved": review.approved or state.revision_count >= 2,
        "revision_count": state.revision_count + 1
    }
    if review.approved or state.revision_count >= 2:
        updates["final_article"] = state.draft

    return EditorialState(**{**state.model_dump(), **updates})

# Routing conditionnel
def should_revise(state: EditorialState) -> str:
    if state.is_approved:
        return "publish"
    elif state.revision_count >= 3:
        return "publish"  # Forcer la publication apres 3 revisions
    else:
        return "revise"

# Construction du graphe
def build_editorial_workflow():
    workflow = StateGraph(EditorialState)

    workflow.add_node("research", research_agent)
    workflow.add_node("write", write_agent)
    workflow.add_node("review", review_agent)

    workflow.set_entry_point("research")
    workflow.add_edge("research", "write")
    workflow.add_edge("write", "review")
    workflow.add_conditional_edges(
        "review",
        should_revise,
        {"revise": "write", "publish": END}
    )

    # Checkpointing pour persistance
    checkpointer = MemorySaver()
    return workflow.compile(checkpointer=checkpointer)

# Execution
app = build_editorial_workflow()
config = {"configurable": {"thread_id": "article-001"}}
result = app.invoke(
    EditorialState(topic="L'impact des agents IA sur la productivite des equipes tech"),
    config=config
)
print(f"Article final ({result.revision_count} revision(s)):")
print(result.final_article)
```

### Human-in-the-Loop avec Interruption

```python
from langgraph.graph import StateGraph, END, interrupt

# Ajouter un noeud d'approbation humaine
def human_approval_node(state: EditorialState) -> EditorialState:
    # interrupt() suspend l'execution et attend une intervention externe
    human_input = interrupt({
        "message": "Approuvez-vous cet article ?",
        "draft": state.draft,
        "review_feedback": state.review_feedback
    })

    if human_input.get("approved"):
        return EditorialState(**{**state.model_dump(), "is_approved": True, "final_article": state.draft})
    else:
        return EditorialState(**{
            **state.model_dump(),
            "review_feedback": human_input.get("feedback", state.review_feedback)
        })

# L'execution reprend apres approbation humaine via update de l'etat
app_with_hitl = workflow.compile(
    checkpointer=checkpointer,
    interrupt_before=["human_approval"]  # Pause avant ce noeud
)
```

### Parallel Execution avec Send API

```python
from langgraph.types import Send

# Dispatcher qui cree des executions paralleles
def parallel_research_dispatcher(state: EditorialState) -> list:
    sources = ["academic_papers", "industry_reports", "news_articles", "social_media"]
    # Send cree une execution parallele pour chaque source
    return [Send("research_source", {"topic": state.topic, "source": src}) for src in sources]

workflow.add_conditional_edges("router", parallel_research_dispatcher)
```

---

## CrewAI

### Architecture

CrewAI abstrait les multi-agents avec trois concepts : **Agent** (role, backstory, tools, llm), **Task** (description, expected_output, agent assign), **Crew** (liste d'agents, liste de tasks, process).

Process sequentiel : tasks executees dans l'ordre. Process hierarchical : un manager LLM orchestre et delegue automatiquement.

### Code Complet : Crew d'Analyse Competitive

```python
from crewai import Agent, Task, Crew, Process
from crewai.tools import BaseTool
from langchain_openai import ChatOpenAI
from pydantic import BaseModel, Field
from typing import Type

# Tools personnalises
class WebScraperTool(BaseTool):
    name: str = "web_scraper"
    description: str = "Scrape le contenu d'une URL ou recherche des informations sur une entreprise"

    def _run(self, query: str) -> str:
        # Integration avec Firecrawl, Apify ou BeautifulSoup en production
        return f"Contenu scrappe pour: {query} [donnees simulees pour l'exemple]"

class FinancialDataTool(BaseTool):
    name: str = "financial_data"
    description: str = "Recupere les donnees financieres publiques d'une entreprise (revenus, croissance, valorisation)"

    def _run(self, company: str) -> str:
        return f"Donnees financieres de {company}: CA $500M, croissance 25% YoY [simulees]"

# Definition des agents specialises
market_analyst = Agent(
    role="Analyste Marche Senior",
    goal="Identifier les tendances du marche, la position concurrentielle et les opportunites de croissance",
    backstory="""Tu es un analyste marche avec 15 ans d'experience en SaaS B2B. Tu excelles
    dans l'identification des signaux faibles et la comparaison de positionnements strategiques.
    Tu utilises des donnees publiques, des rapports industriels et des analyses de terrain.""",
    tools=[WebScraperTool()],
    llm=ChatOpenAI(model="gpt-4o", temperature=0),
    verbose=True,
    allow_delegation=False  # Cet agent ne delegue pas
)

financial_analyst = Agent(
    role="Analyste Financier",
    goal="Evaluer la sante financiere et les indicateurs de performance des concurrents",
    backstory="""Ancien banquier d'investissement specialise dans le secteur tech. Tu analyses
    les metriques SaaS (ARR, churn, LTV/CAC, Rule of 40) avec rigueur et precision.""",
    tools=[FinancialDataTool()],
    llm=ChatOpenAI(model="gpt-4o", temperature=0),
    verbose=True,
    allow_delegation=False
)

strategy_writer = Agent(
    role="Consultant Strategie",
    goal="Synthetiser les analyses et produire des recommandations strategiques actionnables",
    backstory="""Ex-McKinsey avec specialisation en strategy tech. Tu transformes des analyses
    complexes en recommandations claires et priorisees pour les C-levels.""",
    tools=[],
    llm=ChatOpenAI(model="gpt-4o", temperature=0.2),
    verbose=True,
    allow_delegation=True  # Peut demander des complements aux autres agents
)

# Definition des taches
market_analysis_task = Task(
    description="""Analyse le paysage concurrentiel de {company} sur son marche principal.
    Identifie : les 5 principaux concurrents, leur positionnement, leurs avantages differentiels,
    leurs faiblesses apparentes, et les mouvements recents (lancements produits, partenariats, levees).""",
    expected_output="""Rapport d'analyse concurrentielle structure :
    1. Tableau comparatif des 5 concurrents (positionnement, forces, faiblesses)
    2. Carte de positionnement (prix vs valeur)
    3. Signaux d'alerte et opportunites identifiees
    Format: markdown, 600-800 mots""",
    agent=market_analyst
)

financial_analysis_task = Task(
    description="""Analyse les performances financieres des concurrents identifies de {company}.
    Compare les metriques SaaS cles : ARR estime, taux de croissance, efficacite commerciale.""",
    expected_output="""Analyse financiere comparative :
    1. Tableau des metriques financieres par concurrent
    2. Benchmark de la sante financiere (Rule of 40, burn multiple si disponible)
    3. Evaluation de la durabilite competitive
    Format: markdown avec tableaux, 400-600 mots""",
    agent=financial_analyst,
    context=[market_analysis_task]  # Depend du resultat de l'analyse marche
)

synthesis_task = Task(
    description="""A partir des analyses marche et financieres, produis un rapport de synthese
    strategique pour {company}. Inclus des recommandations prioritisees et un plan d'action 90 jours.""",
    expected_output="""Rapport strategique executif :
    1. Executive Summary (3 points cles)
    2. Opportunites strategiques (prioritisees par impact/effort)
    3. Menaces et risques a surveiller
    4. Plan d'action recommande sur 90 jours
    5. KPIs de suivi proposes
    Format: markdown professionnel, 800-1000 mots""",
    agent=strategy_writer,
    context=[market_analysis_task, financial_analysis_task]
)

# Assemblage du Crew
competitive_crew = Crew(
    agents=[market_analyst, financial_analyst, strategy_writer],
    tasks=[market_analysis_task, financial_analysis_task, synthesis_task],
    process=Process.sequential,  # ou Process.hierarchical avec manager_llm
    verbose=True,
    memory=True,               # Active la memoire partagee entre agents
    output_log_file="crew_output.log"
)

# Execution
result = competitive_crew.kickoff(inputs={"company": "Salesforce"})
print(result.raw)
```

### Delegation Automatique en Mode Hierarchique

```python
from crewai import Agent, Crew, Process

manager_llm = ChatOpenAI(model="gpt-4o", temperature=0)

hierarchical_crew = Crew(
    agents=[market_analyst, financial_analyst, strategy_writer],
    tasks=[synthesis_task],  # Une seule tache de haut niveau
    process=Process.hierarchical,
    manager_llm=manager_llm,  # Le manager decompose et delegue automatiquement
    verbose=True
)
# Le manager LLM decoupe la tache, assigne aux bons agents, consolide les resultats
```

---

## AutoGen

### Architecture

AutoGen (Microsoft) est base sur des **ConversableAgent** qui communiquent via des messages. Chaque agent peut recevoir, traiter et envoyer des messages. Le pattern fondamental : deux agents qui conversent jusqu'a une condition de terminaison.

### Code Complet : Debat entre Agents avec Judge

```python
import autogen
from autogen import ConversableAgent, GroupChat, GroupChatManager

# Configuration LLM partagee
llm_config = {
    "model": "gpt-4o",
    "temperature": 0.3,
    "api_key": "YOUR_API_KEY"
}

# Agent partisan du Pour
proponent = ConversableAgent(
    name="Partisan_Pour",
    system_message="""Tu defends avec conviction la these 'Pour' sur le sujet donne.
    Argumente avec des donnees, exemples concrets et logique rigoureuse.
    Reponds aux arguments de l'opposition point par point.
    Sois persuasif mais factuel.""",
    llm_config=llm_config,
    human_input_mode="NEVER",  # Pas d'input humain
    is_termination_msg=lambda msg: "DEBAT_TERMINE" in msg.get("content", "")
)

# Agent partisan du Contre
opponent = ConversableAgent(
    name="Partisan_Contre",
    system_message="""Tu defends avec conviction la these 'Contre' sur le sujet donne.
    Refutes les arguments adverses avec des preuves et contre-exemples.
    Identifie les failles logiques et les biais de l'opposition.
    Sois critique et rigoureux.""",
    llm_config=llm_config,
    human_input_mode="NEVER"
)

# Agent juge
judge = ConversableAgent(
    name="Juge",
    system_message="""Tu es un arbitre impartial. Apres {n_rounds} echanges de debat,
    tu evalues les arguments des deux partis et prononces un verdict motive.
    Tu n'interviens qu'a la fin du debat pour trancher.
    Ton verdict inclut : points forts de chaque camp, verdict motive, nuances importantes.
    Termines ton message par 'DEBAT_TERMINE'.""",
    llm_config={"model": "gpt-4o", "temperature": 0},
    human_input_mode="NEVER"
)

def run_structured_debate(topic: str, n_rounds: int = 3):
    """Orchestre un debat structure entre agents."""
    debate_topic = f"SUJET DU DEBAT: {topic}"

    # Phase 1 : Debat entre proponent et opponent
    chat_result = proponent.initiate_chat(
        recipient=opponent,
        message=f"{debate_topic}\n\nCommence par exposer tes arguments 'Pour'.",
        max_turns=n_rounds * 2,  # Chaque parti parle n_rounds fois
        summary_method="last_msg"
    )

    # Extraction de l'historique du debat
    debate_transcript = "\n\n".join([
        f"**{msg['role'].upper()} ({msg.get('name', 'Unknown')})**: {msg['content']}"
        for msg in chat_result.chat_history
    ])

    # Phase 2 : Le juge evalue
    judge_chat = judge.initiate_chat(
        recipient=proponent,  # Le juge s'adresse a l'agent initialisant
        message=f"""Voici la transcription complete du debat sur: {topic}

{debate_transcript}

Rends ton verdict motive.""",
        max_turns=1
    )

    return {
        "topic": topic,
        "debate_transcript": debate_transcript,
        "verdict": judge_chat.chat_history[-1]["content"]
    }

result = run_structured_debate(
    topic="Les agents IA autonomes representent-ils un risque net pour les emplois tech d'ici 2027 ?",
    n_rounds=3
)
print(result["verdict"])
```

### Group Chat avec Human Proxy

```python
from autogen import UserProxyAgent, GroupChat, GroupChatManager

# Human proxy pour supervision
human_proxy = UserProxyAgent(
    name="Human_Supervisor",
    human_input_mode="TERMINATE",  # Demande input humain a la fin
    max_consecutive_auto_reply=0,  # Ne genere jamais de reponse automatique
    is_termination_msg=lambda msg: "RAPPORT_FINAL" in msg.get("content", ""),
    code_execution_config=False
)

# GroupChat pour orchestration automatique
group_chat = GroupChat(
    agents=[proponent, opponent, judge, human_proxy],
    messages=[],
    max_round=10,
    speaker_selection_method="auto",  # Le manager decide qui parle
    allow_repeat_speaker=False
)

# Manager qui orchestre le group chat
manager = GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config,
    system_message="Tu orchestre le debat de facon equitable et structuree."
)

# Demarrage du groupe
human_proxy.initiate_chat(
    manager,
    message="Debattons de l'adoption de l'IA generative en entreprise."
)
```

---

## Comparaison LangGraph / CrewAI / AutoGen

| Critere | LangGraph | CrewAI | AutoGen |
|---------|-----------|--------|---------|
| **Modele de controle** | Graphe explicite (noeuds/aretes) | Role-based avec Crew | Conversation entre agents |
| **Flexibilite du flow** | Maximale (conditionnel, cycles, parallele) | Sequentiel ou hierarchical | Emergent (conversation libre) |
| **Debugging** | Excellent (LangSmith integration) | Moyen (logs verbose) | Moyen (historique conversations) |
| **Production-readiness** | Eleve (persistence, checkpoints, retries) | Moyen (en amelioration) | Moyen (Microsoft support) |
| **Courbe d'apprentissage** | Steep (concepts graphes requis) | Faible (tres intuitif) | Moyen (patterns conversation) |
| **Human-in-the-loop** | Natif et robuste | Partiel | Natif (UserProxyAgent) |
| **Parallisme** | Natif (Send API) | Non natif | Non natif |
| **Use cases ideaux** | Workflows complexes production | Prototypage rapide, equipes specialisees | Recherche, debat, code generation |
| **Ecosysteme** | LangChain (large) | Independant (croissant) | Microsoft (Azure integration) |

---

## Patterns d'Orchestration

### Pattern Supervisor

Un agent superviseur decompose la tache et delegue a des agents specialises. Il consolide les resultats et gere les erreurs. Implementer avec LangGraph (noeud supervisor avec routing conditionnel) ou CrewAI (process hierarchical).

**Avantage** : coherence globale, gestion des dependances.
**Quand l'utiliser** : taches complexes avec sous-taches heterogenes.

### Pattern Pipeline

Agents en serie, chaque agent traite et enrichit la sortie du precedent. Similaire a un ETL mais avec intelligence a chaque etape.

**Avantage** : simple, predictible, facile a debugger.
**Quand l'utiliser** : workflows avec etapes clairement sequentielles (research → write → review → publish).

### Pattern Debate/Critique

Deux agents avec perspectives opposees debattent, un troisieme arbitre. Reduit les hallucinations et angles morts.

**Avantage** : qualite elevee, reduction des biais d'un agent unique.
**Quand l'utiliser** : decisions critiques, analyses strategiques, evaluation de risques.

### Pattern Ensemble

Plusieurs agents independants traitent la meme tache en parallele, un agent consolide les resultats par vote ou synthese.

**Avantage** : robustesse, qualite par consensus.
**Quand l'utiliser** : classification, scoring, generation de contenu ou la diversite est valorisee.

---

## Anti-Patterns a Eviter

**Agent loops** : deux agents qui se renvoient la tache indefiniment. Prevention : `max_iterations` strict, condition de terminaison explicite, detection de repetition dans l'historique.

**Context overflow** : accumulation de messages dans le contexte jusqu'a depasser la fenetre. Prevention : summarization periodique, fenetre glissante, externalisation de la memoire en vector store.

**Tool abuse** : un agent appelle un tool des dizaines de fois inutilement. Prevention : description de tool claire (quand utiliser et quand NE PAS utiliser), rate limiting par tool, logging des appels avec alertes sur les outliers.

**Coordination overhead** : pour une tache simple, le cout de coordination depasse les benefices. Prevention : commencer par un agent unique, passer au multi-agents uniquement si le benchmark prouve un gain de qualite ou performance superieur a 20%.

**False autonomy** : designer un systeme "autonome" sans gardes-fous sur les actions irreversibles (emails, paiements, suppressions de donnees). Prevention : human-in-the-loop obligatoire pour toute action avec consequence externe irreversible.
