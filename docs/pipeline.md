# SDD Pipeline — Ciclo Fechado de Desenvolvimento

Este documento descreve o pipeline completo de Spec-Driven Development (SDD) e como a Visa se integra ao ecossistema.

## Visão Geral

```mermaid
flowchart TB
    subgraph PRE["Pre-Discovery (Visa)"]
        E1["(&) Ethnographer<br/>Domain Mapping"]
        E2["(&) Strategist<br/>Journey Analysis"]
        E3["(&) Collector<br/>Evidence Gathering"]
    end

    subgraph SYN["Synthesis (Visa)"]
        S1["(&) Paradigm Advisor<br/>Architecture Patterns"]
        S2["(&) Modeler<br/>Domain Model"]
        S3["(&) Data Modeler<br/>Data Design"]
        S4["(&) Design System<br/>UI/UX Standards"]
    end

    subgraph SPEC["Specification (Visa)"]
        SP1["(&) Redactor<br/>SDD Specs"]
        SP2["(&) Strategist<br/>Business Rules"]
        SP3["(&) Inspector<br/>Quality Gates"]
    end

    subgraph HANDOFF["Handoff (Visa)"]
        H1["(&) Reviewer<br/>Final Audit"]
        H2["(&) Handoff<br/>Documentation"]
    end

    subgraph BRIDGE["Bridge"]
        BR["(&) visa bridge<br/>Collector Gate"]
    end

    subgraph IMP["Implementation"]
        PG["(**) paridade-guard<br/>Spec Gate"]
        GC["(&) git commit<br/>Code Implementation"]
    end

    PRE --> SYN --> SPEC --> HANDOFF --> BRIDGE
    BRIDGE --> PG --> GC

    PRE --> |"12 agents<br/>14 skills"| IMP

    style PRE fill:#1a1a2e,stroke:#6c5ce7
    style SYN fill:#1a1a2e,stroke:#00b894
    style SPEC fill:#1a1a2e,stroke:#fdcb6e
    style HANDOFF fill:#1a1a2e,stroke:#e17055
    style BRIDGE fill:#16213e,stroke:#e94560
    style IMP fill:#16213e,stroke:#e94560
```

## Fases do Pipeline

### Fase 1: Pré-Descoberta (Visa)

| Agent | Output | Confiança |
|-------|--------|-----------|
| `visa-etnografo` | `landscape.md`, `personas.md`, `glossario.md` | 🟢🟡 |
| `visa-estrategista` | `pains.md`, `opportunities.md`, `concorrentes.md` | 🟢🟡 |
| `visa-coletor` | `gaps.md`, `evidence_plans/`, `evidence_results/` | 🟢🟡🔴 |

### Fase 2: Síntese (Visa)

| Agent | Output | Confiança |
|-------|--------|-----------|
| `visa-paradigm-advisor` | `confidence-report.md` (paradigm) | 🟢🟡 |
| `visa-modelador` | `domain.md`, `flows.md`, `architecture.md` | 🟢🟡 |
| `visa-data-modeler` | Data model, `integrations.md` | 🟢🟡 |
| `visa-design-system` | Design tokens, UI standards | 🟢🟡 |

### Fase 3: Especificação (Visa)

| Agent | Output | Confiança |
|-------|--------|-----------|
| `visa-redator` | `business_model.md`, `discard_log.md`, `ambiguity_log.md` | 🟢🟡🔴 |
| `visa-strategist` | `user-stories.md`, `sdd/*.md` | 🟢🟡🔴 |
| `visa-inspector` | Quality gates, validation | 🟢🟡 |

### Fase 4: Handoff (Visa)

| Agent | Output | Confiança |
|-------|--------|-----------|
| `visa-revisor` | `confidence-report.md` (final), audit | 🟢🟡🔴 |
| `visa-handoff` | `handoff.md`, `openapi/` | 🟢🟡 |

### Fase 5: Bridge

```mermaid
sequenceDiagram
    participant User
    participant VisaCLI
    participant ColetorGate
    participant ParidadeGuard
    participant Git

    User->>VisaCLI: visa bridge
    VisaCLI->>ColetorGate: Check LACUNAs in gaps.md

    alt Gate Pass
        ColetorGate->>VisaCLI: Allowed
        VisaCLI->>VisaCLI: Create _visa_sdd/migration/
        VisaCLI->>ParidadeGuard: Bridge complete
    else Gate Block
        ColetorGate->>VisaCLI: Blocked (exit 4)
        VisaCLI->>User: Show unresolved LACUNAs
    end

    User->>ParidadeGuard: paridade-guard contract
    ParidadeGuard->>User: contract.json

    User->>Git: git commit
    Git->>ParidadeGuard: pre-commit hook
    ParidadeGuard->>Git: Allow/Bock
```

### Fase 6: Implementação Vigiada (paridade-guard)

O `paridade-guard` atua como gatekeeper no `pre-commit`:
- Lê `contract.json`
- Inspeca `git diff`
- Bloqueia commits que violem especificações

## Artefatos por Fase

```
_visa_sdd/
├── landscape.md              # Fase 1
├── personas-inicial.md      # Fase 1
├── glossario.md             # Fase 1
├── pains.md                 # Fase 1
├── opportunities.md         # Fase 1
├── gaps.md                  # Fase 1 (Coletor)
├── evidence_plans/          # Fase 1
├── evidence_results/        # Fase 1
├── evidence_scripts/       # Fase 1
│
├── domain.md                # Fase 2
├── flows.md                 # Fase 2
├── architecture.md          # Fase 2
├── integrations.md          # Fase 2
│
├── business_model.md        # Fase 3 [CANONICAL]
├── discard_log.md          # Fase 3 [CANONICAL]
├── ambiguity_log.md         # Fase 3 [CANONICAL]
├── confidence-report.md     # Fase 3 [CANONICAL]
├── user-stories.md         # Fase 3
├── sdd/                    # Fase 3
│
├── handoff.md              # Fase 4
│
└── parity_audit/           # Bridge
    └── contract.json       # paridade-guard
```

## Exit Codes

| Code | Significado | Ação |
|------|------------|------|
| `0` | Sucesso | Prosseguir |
| `1` | Erro geral | Verificar logs |
| `2` | Artefatos faltando | Completar pipeline |
| `3` | Formato inválido | Corrigir front-matter/IDs |
| `4` | Gate bloqueado | Resolver LACUNAs |

## Integração com Ecossistema

```mermaid
flowchart LR
    subgraph V["Visa (Forward Discovery)"]
        V1["(&) Ethnographer"]
        V2["(&) Strategist"]
        V3["(&) Coletor"]
        V4["(&) Redactor"]
    end

    subgraph PG["paridade-guard (Gatekeeper)"]
        PG1["(&) Contract"]
        PG2["(&) Inspector"]
        PG3["(&) pre-commit"]
    end

    subgraph R["Reversa (Reverse Discovery)"]
        R1["(&) Scout"]
R2["(&) Detective"]
        R3["(&) Writer"]
    end

    V4 --> |"BR-FUTURE-NNN"| PG1
    R3 --> |"BR-MIGRAR-NNN"| PG1
    PG2 --> |"validate"| R
    PG3 --> |"block"| V

    style V fill:#1a1a2e,stroke:#6c5ce7
    style PG fill:#16213e,stroke:#e94560
    style R fill:#1a1a2e,stroke:#00b894
```

## Métricas de Qualidade

| Métrica | Target | Atual |
|---------|--------|-------|
| Cobertura de artefatos | 100% obrigatórios | 14/14 |
| Confiança média | 🟢 > 70% | 🟢🟡 |
| LACUNAs resolvidas | 100% antes de handoff | varies |
| Tests passing | 40/40 | ✅ |
| CI/CD coverage | 100% | ✅ |
