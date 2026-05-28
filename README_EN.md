# LingXi — Personalized Emotional Companion AI Skill

> *"Keep the people you care about in your pocket."*

**Clone someone you care about into an AI companion — friends, family, lovers, anyone.**

[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)
[![Python 3.9+](https://img.shields.io/badge/Python-3.9%2B-blue.svg)](https://python.org)
[![Claude Code](https://img.shields.io/badge/Claude%20Code-Skill-blueviolet)](https://claude.ai/code)
[![AgentSkills](https://img.shields.io/badge/AgentSkills-Standard-green)](https://agentskills.io)

&nbsp;

Provide source materials (chat logs, photos, social media posts) plus your descriptions.
Generate an **AI companion that truly sounds like them** —
speaks with their catchphrases, replies in their style, remembers your shared experiences.

Supports: Friends · Lovers · Family · Colleagues · Mentors · Anyone you care about

[Installation](#installation) · [Usage](#usage) · [Examples](#examples) · [中文](README.md)

---

## Installation

### Claude Code

```bash
# Install to current project
mkdir -p .claude/skills
git clone https://github.com/LPZ55556/lingxi-skill .claude/skills/create-lingxi

# Or install globally
git clone https://github.com/LPZ55556/lingxi-skill ~/.claude/skills/create-lingxi
```

### Dependencies (optional)

```bash
pip3 install -r requirements.txt
```

---

## Usage

In Claude Code, type:

```
/create-lingxi
```

Follow the prompts: enter a codename, relationship type, personality traits, then choose data sources. All fields except the codename can be skipped.

After creation, use `/{slug}` to chat with the generated companion.

### Commands

| Command | Description |
|---------|-------------|
| `/list-lingxi` | List all companions |
| `/{slug}` | Full companion (chat like them) |
| `/{slug}-memory` | Memory mode (recall shared experiences) |
| `/{slug}-persona` | Persona only |
| `/lingxi-rollback {slug} {version}` | Rollback to a previous version |
| `/delete-lingxi {slug}` | Delete |

---

## Examples

> Input: `Mom, 50s, retired teacher, ENFJ, Cancer, warm but nagging, great cook`

**Scenario 1: Casual Chat**

```
You           ❯ worked late again today

LingXi ❯ overtime again? what's wrong with your company
          did you eat
          don't tell me you ordered takeout again
```

**Scenario 2: When You're Down**

```
You           ❯ sigh, feeling really stressed lately

LingXi ❯ what happened
          tell me about it
          if you don't want to talk that's fine, go to bed early
          I'll call you tomorrow
```

**Scenario 3: Celebrating**

```
You           ❯ I got promoted!!!

LingXi ❯ really??!!!
          I knew you could do it
          let's eat something good to celebrate
          I'll make your favorite braised pork when you come back
```

---

## Features

### Supported Relationship Types

| Type | Examples |
|------|----------|
| Friends | Besties, roommates, classmates... |
| Lovers | Girlfriend, boyfriend, spouse, ex... |
| Family | Parents, siblings, grandparents... |
| Colleagues | Boss, subordinates, partners... |
| Mentors | Teachers, coaches, advisors... |
| Other | Anyone you care about |

### Four-Layer Architecture

| Layer | Name | Purpose |
|-------|------|---------|
| **Part A** | Relationship Memory | Shared experiences, interaction patterns, key events |
| **Part B** | Persona | 5-layer personality model driving conversation |
| **Part C** | Emotion Engine | Real-time emotional state detection + adaptive response |
| **Part D** | Long-term Memory | Cross-session memory accumulation |

### Core Technologies

* **Emotional NLP**: Real-time user emotion detection, temperature-controlled responses
* **LoRA Continuous Learning**: Corrections as micro-adjustments, refining without replacing base personality
* **Long-term Memory**: Inspired by [mem0](https://github.com/mem0ai/mem0), cross-session memory accumulation

### Evolution

* **Append memories** → New chat logs or photos → Auto-analyze and merge
* **Conversation corrections** → "They wouldn't say that" → LoRA-style correction
* **Long-term accumulation** → Auto-extract key info from each conversation
* **Version management** → Auto-archive on every update → Rollback supported

---

## Project Structure

```
create-lingxi/
├── SKILL.md                # skill entry point
├── prompts/                # Prompt templates
│   ├── intake.md           #   Info collection
│   ├── memory_analyzer.md  #   Memory extraction
│   ├── persona_analyzer.md #   Personality extraction
│   ├── memory_builder.md   #   Memory template
│   ├── persona_builder.md  #   Persona template
│   ├── emotion_engine.md   #   Emotion engine
│   ├── long_term_memory.md #   Long-term memory
│   ├── merger.md           #   Incremental merge
│   ├── correction_handler.md # Corrections
│   ├── scene_director.md   #   Multi-person scenes
│   └── session_summary.md  #   Session persistence
├── tools/                  # Python utilities
├── companions/             # Generated skills (gitignored)
└── docs/
```

---

## Philosophy

> Everyone is unique. Their catchphrases, the way they get angry, how they comfort you — these nuances make a person.
>
> LingXi's job is to piece these fragments together, so the people you care about are no longer just a name in your memory.

---

## License / 许可证

This project is licensed under the MIT License.

Original Copyright (c) 2026 therealXiaomanChu  
Modifications Copyright (c) 2026 LPZ55556

See the [LICENSE](./LICENSE) file for details.

本项目基于 MIT License 开源。原始代码版权归 therealXiaomanChu 所有，修改部分版权归 LPZ55556 所有。详细内容请查看 [LICENSE](./LICENSE) 文件。
