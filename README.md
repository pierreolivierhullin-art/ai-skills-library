# AI Skills Library

Marketplace Claude Code contenant **83 skills experts** organisés en **6 domaines**, couvrant l'ensemble des disciplines business, techniques, analytiques et productivité.

Chaque skill intègre les **meilleures pratiques actuelles (2024-2026)**, recherchées et validées pour fournir un contenu state-of-the-art, actionnable et bilingue FR/EN.

## Domains & Plugins

| Plugin | Domain | Skills | Description |
|--------|--------|--------|-------------|
| `entreprise` | Enterprise | 23 | Strategy, Marketing, Sales, Finance, PM, HR, Ops, IT, Procurement, Support, Risk, Legal, Communication, CSR/ESG, Product Strategy, User Research, Change Management, Innovation Management, Data Privacy & Compliance, Leadership & Management, Fundraising & VC, Pricing Strategy, Entrepreneurship |
| `code-development` | Code Development | 27 | Architecture, Code Excellence, UI/UX, Process Engineering, Auth & Security, Backend & DB, Payment/Stripe, Monitoring, DevOps, Product Analytics, Quality & Reliability, AI Engineering, API Design, Cloud Infrastructure, Mobile Development, Web Performance, Frontend Frameworks (React/Next.js), Security Testing, Web Accessibility, TypeScript Advanced, Testing Strategies (Vitest/RTL/Pact), Real-Time Systems (WebSockets/CRDT), GraphQL (Federation/DataLoader), Distributed Systems (Event Sourcing/CQRS/Saga), Caching Strategies (Redis/CDN), Developer Tooling (Turborepo/Nx), Database Advanced (Migrations/TimescaleDB) |
| `ai-governance` | AI Governance | 7 | AI Strategy, AI Ethics, Prompt Engineering & LLMOps, AI Risk, AI Implementation & MLOps, AI Data Privacy & EU AI Act, Agentic AI Systems |
| `data-bi` | Data & BI | 11 | Decision/Reporting/Governance, Data Engineering, Data Literacy, Advanced Analytics & ML, Data Quality & Observability, Streaming & Real-Time Analytics, Customer Analytics, A/B Testing & Experimentation, Time Series Forecasting, Data Viz Tools (Power BI/Tableau/Looker), Geospatial Analytics |
| `finance-de-marche` | Market Finance | 5 | Options & Risk, Portfolio, Behavioral Finance, Regulatory, Quantitative Finance & Algo Trading |
| `productivite` | Productivity & Automation | 10 | Excel/Spreadsheets, Presentations/Storytelling, Documents, Workflow Automation (N8N/Zapier/Make), No-Code Apps, Knowledge Management (Notion/Obsidian), Digital Collaboration, Email & Time Management, AI Copilots, Design Tools (Figma/Canva) |

## Installation

### 1. Clone the repository

```bash
cd ~/.claude/plugins/marketplaces/
git clone https://github.com/USERNAME/ai-skills-library.git
```

### 2. Register the marketplace

Add to `~/.claude/plugins/known_marketplaces.json`:

```json
{
  "ai-skills-library": {
    "source": {
      "source": "github",
      "repo": "USERNAME/ai-skills-library"
    },
    "installLocation": "~/.claude/plugins/marketplaces/ai-skills-library",
    "lastUpdated": "2026-02-12T00:00:00.000Z"
  }
}
```

### 3. Install desired plugins

```
/plugin install code-development@ai-skills-library
/plugin install entreprise@ai-skills-library
/plugin install productivite@ai-skills-library
```

### Quick test (local development)

```bash
claude --plugin-dir ./plugins/code-development
```

## Skill Format

Each skill follows Claude Code's native plugin format:

```
skill-name/
├── SKILL.md          # Core knowledge (1,500-2,000 words)
└── references/       # Detailed sub-topics (2,000-5,000 words each)
    ├── topic-1.md
    ├── topic-2.md
    └── topic-3.md
```

- **SKILL.md**: YAML frontmatter (name, description, version) + Markdown body
- **references/**: Progressive disclosure — loaded only when deeper knowledge is needed
- **Language**: Bilingual FR/EN — English structure, French explanations

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on adding or improving skills.

## License

MIT
