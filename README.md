# AI Skills Library

Marketplace Claude Code contenant **36 skills experts** organisés en **5 domaines**, couvrant l'ensemble des disciplines business, techniques et analytiques.

Chaque skill intègre les **meilleures pratiques actuelles (2024-2026)**, recherchées et validées pour fournir un contenu state-of-the-art, actionnable et bilingue FR/EN.

## Domains & Plugins

| Plugin | Domain | Skills | Description |
|--------|--------|--------|-------------|
| `entreprise` | Enterprise | 14 | Strategy, Marketing, Sales, Finance, PM, HR, Ops, IT, Procurement, Support, Risk, Legal, Communication, CSR/ESG |
| `code-development` | Code Development | 11 | Architecture, Code Excellence, UI/UX, Process Engineering, Auth & Security, Backend & DB, Payment/Stripe, Monitoring, DevOps, Product Analytics, Quality & Reliability |
| `ai-governance` | AI Governance | 4 | AI Strategy, AI Ethics, Prompt Engineering & LLMOps, AI Risk |
| `data-bi` | Data & BI | 3 | Decision/Reporting/Governance, Data Engineering, Data Literacy |
| `finance-de-marche` | Market Finance | 4 | Options & Risk, Portfolio, Behavioral Finance, Regulatory |

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
