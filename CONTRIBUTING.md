# Contributing to AI Skills Library

## Adding a New Skill

### 1. Create the skill directory

```bash
mkdir -p plugins/<domain>/skills/<skill-name>/references
```

### 2. Write SKILL.md

Follow the standard template:

```markdown
---
name: skill-name
description: This skill should be used when the user asks to "trigger phrase 1", "trigger phrase 2", discusses topic, or needs guidance on specific-area.
version: 1.0.0
---

# Skill Title

## Overview
## When This Skill Applies
## Core Principles
## Key Frameworks & Methods
## Decision Guide
## Common Patterns & Anti-Patterns
## Implementation Workflow
## Additional Resources
```

### 3. Writing Rules

- **Frontmatter description**: Third person English — "This skill should be used when..."
- **Body**: Imperative form — "Evaluate the situation", not "You should evaluate"
- **Word count**: 1,500-2,000 words for SKILL.md, 2,000-5,000 for each reference file
- **Language**: Bilingual FR/EN
  - English: frontmatter, section titles, technical terms
  - French: explanations, examples, business context
- **Trigger phrases**: English, specific, in quotes in the description
- **State-of-the-art**: Research current best practices (2024-2026) before writing

### 4. Write Reference Files

Create 2-5 reference files in `references/` covering detailed sub-topics. Each reference file should include a "State of the Art" section.

### 5. Validation Checklist

- [ ] Valid YAML frontmatter (name, description, version)
- [ ] Description contains specific trigger phrases
- [ ] SKILL.md word count: 1,500-2,000
- [ ] All reference files are mentioned in SKILL.md's "Additional Resources" section
- [ ] Imperative form throughout
- [ ] No trigger collisions with existing skills
