# Visa

<small>by [Adgmed2018](https://github.com/Adgmed2018) · forward complement to [Reversa](https://github.com/sandeco/reversa) by [@sandeco](https://github.com/sandeco)</small>

**Turn business domains into executable specifications for AI agents — before any code exists.**

[English Docs](docs/README.md) · [Português Docs](docs/pt/README.md) · [Español Docs](docs/es/README.md)

---

Visa is a **forward** specification-discovery framework. Install it inside an empty project (or any project starting from a fresh business domain) and it coordinates a team of specialized AI agents to turn vague conversations, market hypotheses, and stakeholder interviews into complete, traceable, executable specifications — ready for use by any coding agent.

## Why Visa exists

Most software projects start with a meeting, a slide, or a Notion page. The handoff to engineering is informal, the specification implicit, the assumptions buried in chat threads. AI coding agents amplify the cost: they execute fast, but they execute *whatever you say* — including the half-formed assumption that was never validated.

For **legacy systems**, [Reversa](https://github.com/sandeco/reversa) extracts the spec that already exists in the code. For **new systems** there is no code yet — only hypotheses. Without a structured discovery, the agent generates code for a product that maybe shouldn't exist, in an architecture that maybe doesn't fit, with rules nobody verified.

**Visa is the bridge between the business domain and AI agents.**

It coordinates a pipeline of agents — ethnographer, strategist, paradigm advisor, data modeler, design system, redactor, inspector, reviewer, handoff — to turn conversations, evidence, and constraints into:

- Specifications with versioned canonical IDs (`BR-FUTURE-NNN`, `AMB-FUTURE-NNN`)
- Domain models, ERDs, design tokens, paradigm decisions
- Acceptance criteria in Gherkin, ready for `paridade-guard` validation
- A consolidated `CLAUDE.md` (or `ANTIGRAVITY.md`, `AGENTS.md`, etc.) for the coding agent to honor

The output is not documentation for humans to read. **It is operational contracts that allow an agent to build the system with fidelity to what was discovered.**

Together, **Visa (forward) + Reversa (backward) + paridade-guard (gatekeeper)** form the only closed-loop SDD stack available open-source.

## Installation

In the project root (or in an empty folder for a new product):

```bash
pip install visa-sdd
```

Then in the project folder:

```bash
visa install
```

The installer will:

- Detect the AI engine present in the environment (Claude Code, Antigravity, Cursor, Codex, Gemini CLI, Windsurf)
- Copy 14 agents (skills) to `.claude/skills/` (Claude Code) or `.agents/skills/` (others)
- Create the engine entry file (`CLAUDE.md`, `ANTIGRAVITY.md`, etc.) if absent
- Create the `.visa/` structure with state, plan, and configuration

Visa never deletes or modifies existing files in your project. Agents write only to `.visa/` and the output folder (`_visa_sdd/` by default).

**Requirements:** Python 3.10+

> [!IMPORTANT]
> 🔒 **Guaranteed immutability of your project**
> The installer only creates new files (`CLAUDE.md`, `.claude/skills/`, `.visa/`, etc.) and never modifies or deletes any existing file in your project. During discovery, agents operate under a strict directive: all writes are restricted to `.visa/` and `_visa_sdd/` — no other file in your project is touched.

> [!CAUTION]
> 💾 **Version your project before starting**
> Although Visa never modifies your files, AI agents can make mistakes. We strongly recommend:
>
> - Initialize Git and commit before starting the discovery
> - Have the repository on GitHub (or GitLab, Bitbucket) for a remote backup
> - Make a local copy of the folder — `cp -r my-project my-project-backup`
>
> If something unexpected happens, restore with `git restore .` or from the backup.

> [!WARNING]
> 🔑 Visa does not request, store, or transmit API keys from any LLM service. All intelligence is delegated to the AI agent already present in your environment (Claude Code, Antigravity, Cursor, etc.) — no external authentication dependencies.

## How to use

After installation, open the project in the AI agent and activate Visa:

```
/visa
```

For engines without slash command support (like Codex):

```
visa
```

Visa will introduce itself, create a personalized discovery plan based on the business domain you describe, and coordinate the entire pipeline. Progress is saved in `.visa/state.json` at each checkpoint — if the session is interrupted, just type `/visa` to resume where you left off.

## How it works

Visa uses a 4-phase pipeline orchestrated by the Visa agent:

```
Pre-Discovery → Synthesis → Specification → Handoff
   Ethnographer    Paradigm     Redactor     Reviewer
   Strategist      Modeler      Strategist   Handoff
   Collector       Data         Inspector
                   Design
```

After Handoff, the canonical artifacts (`BR-FUTURE-NNN`) are consumed by `paridade-guard` to gate the implementation: code merged into `main` must trace back to an approved business rule.

## Agents

### Required

| Agent | Role |
|---|---|
| `visa` | Central orchestrator. Coordinates all agents, saves checkpoints, guides the user |
| `visa-etnografo` | Maps the surface: personas, journeys, competitors, domain vocabulary |
| `visa-estrategista` | Deep journey-by-journey analysis: pains, gains, friction, product opportunities |
| `visa-coletor` | Resolves 🔴 GAPS by generating evidence-collection plans (interviews, market tests, MVPs) |
| `visa-paradigm-advisor` | Decides target paradigm (Clean / OO+DI / FP / event-driven / actor) from constraints |
| `visa-modelador` | Synthesizes domain model, main flows, business model, integration map |
| `visa-data-modeler` | Proposes prospective database schema (ERD, DDL, FKs, CHECK constraints) |
| `visa-design-system` | Proposes prospective design tokens (palette, typography, spacing, components) |
| `visa-redator` | Generates SDD specs per component, OpenAPI prospectivo, business rules with canonical IDs |
| `visa-strategist` | Proposes go-to-market strategies and MVP roadmaps with explicit trade-offs |
| `visa-inspector` | Defines acceptance criteria in Gherkin for each `BR-FUTURE-NNN` |
| `visa-revisor` | Cross-reviews all specs, detects contradictions, prepares handoff |
| `visa-handoff` | Produces final `handoff.md` ready for Spec Kit, Reconstructor, or coding agent |

### Optional (installed by default)

| Agent | Role |
|---|---|
| `visa-agents-help` | Explains with analogies what each Visa agent does and when to use it |
| `visa-claude-md-builder` | Generates a consolidated `CLAUDE.md` (or equivalent) from `_visa_sdd/` artifacts |

### Vertical packs (regulated industries)

Use when the project targets a specific regulated vertical. Pre-loads `BR-FUTURE` rules and forces the Collector to mark missing regulatory evidence as 🔴 blocking GAPS.

| Agent | Vertical |
|---|---|
| `visa-vertical-fintech-pix` | Brazilian fintech: PIX (BACEN), DICT, MED, KYC/PLD, LGPD, BACEN Resolution 4.658 |
| `visa-vertical-healthtech-anvisa` | Healthtech: SaMD (RDC 657), CFM 2.314 telemedicine, CFM 1.821 EHR, ISO 13485 |
| `visa-vertical-legaltech-tributario` | Legaltech: e-CAC, PJe, ESAJ, SPED, OAB Provisão 49/2017, certificate-based authentication |

## What is generated

```
_visa_sdd/
├── landscape.json              # Surface domain map (Ethnographer)
├── opportunities.md            # Pains and gains per journey (Strategist)
├── gaps.md                     # 🔴 LACUNAS blocking advancement (Collector)
├── evidence_results/           # Resolved evidence per LACUNA
├── paradigm_decision.md        # Target paradigm with justification (Paradigm Advisor)
├── domain_model.md             # Entities, flows, business model (Modeler)
├── data_model.md               # ERD in Mermaid + DDL + integrity rules (Data Modeler)
├── design-system/              # Tokens: palette, typography, spacing (Design System)
├── business_model.md           # Canonical BR-FUTURE-NNN rules (Redactor)
├── discard_log.md              # What was deliberately left out of MVP (Redactor)
├── ambiguity_log.md            # AMB-FUTURE-NNN open ambiguities (Redactor)
├── gtm_strategy.md             # Go-to-market strategy (Strategist)
├── risk_register.md            # Risk register (Strategist)
├── mvp_roadmap.md              # Sprint roadmap (Strategist)
├── acceptance/                 # Gherkin .feature per BR-FUTURE-NNN (Inspector)
├── coverage_matrix.md          # BR-FUTURE → acceptance test mapping (Inspector)
├── compliance/                 # Regulatory checklists (only if vertical pack used)
├── review_report.md            # Cross-review findings (Reviewer)
└── handoff.md                  # Final handoff (Handoff)
```

## Confidence scale

Every statement in the specs is marked with:

| Mark | Meaning |
|---|---|
| 🟢 **CONFIRMED** | Validated with real evidence (customer interview, market data, MVP run, signed contract) |
| 🟡 **INFERRED** | Plausible hypothesis based on known patterns, but no direct evidence |
| 🔴 **GAP** | Pure hypothesis with no evidence. **Blocks advancement until interview, test, or research provides evidence.** |

Unlike Reversa (where 🔴 means "not determinable from code"), in Visa 🔴 means "not validated against the market". The user does not resolve a 🔴 GAP by thinking — they resolve it by **collecting evidence**. The Collector agent exists exactly for this function.

## Supported engines

| Engine | Entry file | Skills path | Activation |
|---|---|---|---|
| Claude Code ⭐ | `CLAUDE.md` | `.claude/skills/visa-*/` and `.agents/skills/visa-*/` | `/visa` |
| Google Antigravity ⭐ | `ANTIGRAVITY.md` | `.agents/skills/visa-*/` | `/visa` |
| Codex ⭐ | `AGENTS.md` | `.agents/skills/visa-*/` | `visa` |
| Cursor ⭐ | `.cursorrules` | `.agents/skills/visa-*/` | `/visa` |
| Gemini CLI | `GEMINI.md` | `.agents/skills/visa-*/` | `/visa` |
| Windsurf | `.windsurfrules` | `.agents/skills/visa-*/` | `/visa` |

## CLI commands

```bash
visa install      # Install Visa skills in the project
visa status       # Show current discovery state
visa validate     # Verify expected artifacts in _visa_sdd/
visa bridge       # Generate stub for paridade-guard ≥ 0.3.0
visa doctor       # Diagnostics: engine, skills, state, paridade-guard (NEW v1.5.0)
visa upgrade      # Update skills without reinstalling from scratch (NEW v1.5.0)
visa serve        # Minimal Web UI to visualize _visa_sdd/ (NEW v1.6.0)
visa telemetry    # Manage opt-in privacy-first telemetry (NEW v1.6.0)
visa uninstall    # Remove Visa from the project (preserves _visa_sdd/)
```

The `upgrade` command compares SHA-256 of each `SKILL.md` and updates only what changed, preserving `_visa_sdd/` and `.visa/state.json`.
The `bridge` command supports `--accept-all-risks "reason"` to override the Collector gate with audit trail.

## Internal structure

```
.visa/
├── state.json                  # Discovery state between sessions
├── plan.md                     # Personalized exploration plan (user-editable)
├── telemetry-optin.json        # Opt-in record (only if telemetry enabled)
├── telemetry.jsonl             # Local event log (only if telemetry enabled)
└── context/
    ├── landscape.json          # Generated by Ethnographer
    └── interviews.json         # Generated by Collector

.claude/skills/                 # Claude Code skills mirror
.agents/skills/                 # Universal skills (all compatible engines)
```

## Closed-loop SDD with Reversa and paridade-guard

```
business idea → Visa (forward spec) → BR-FUTURE-NNN → paridade-guard → verified code
                                                              ↑
                                              Reversa (from existing legacy)
```

When extending an existing system, run **Reversa first** to extract what is already there, then **Visa** to discover the new requirements, and finally **paridade-guard** to validate that implementation honors both. Details in [docs/closed-loop.md](docs/closed-loop.md).

## Contributing

Contributions are welcome. Open an issue to discuss before submitting a PR.

```bash
git clone https://github.com/Adgmed2018/visa.git
cd visa
pip install -e ".[dev]"
pytest
```

## License

MIT — see [LICENSE](LICENSE) for details.
