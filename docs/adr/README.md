# Architecture Decision Records (ADRs)

Este diretório contém as decisões arquiteturais documentadas do projeto Visa.

## ADR Index

| ID | Título | Status | Versão |
|----|--------|--------|--------|
| [ADR-0001](ADR-0001-zero-external-dependencies.md) | Zero External Dependencies (Stdlib Pure) | ✅ Accepted | v1.0.0 |
| [ADR-0002](ADR-0002-canonical-id-system.md) | Canonical ID System (BR-FUTURE/AMB-FUTURE) | ✅ Accepted | v1.0.0 |
| [ADR-0003](ADR-0003-collector-gate.md) | Collector Gate (v1.2) | ✅ Accepted | v1.2.0 |
| [ADR-0004](ADR-0004-multi-agent-orchestration.md) | Multi-Agent Orchestration Architecture | ✅ Accepted | v1.0.0 |
| [ADR-0005](ADR-0005-bridge-pattern.md) | Bridge Pattern for paridade-guard Integration | ✅ Accepted | v1.1.0 |

## O que é um ADR?

Um ADR (Architecture Decision Record) é um documento que captura uma decisão importante de arquitetura, junto com o contexto que levou a essa decisão e as consequências dela.

### Formato padrão

```markdown
# ADR-XXXX: Título

## Status
**Status** — Versão

## Context
O problema ou contexto que motivou a decisão.

## Decision
A decisão tomada.

## Consequences
### Positive
Benefícios da decisão.

### Negative
Drawbacks da decisão.

### Mitigations
Como mitigamos os drawbacks.
```

## Quando criar um ADR?

Crie um ADR quando:
- A decisão afeta múltiplos componentes
- A decisão tem consequências de longo prazo
- A decisão pode ser questionada no futuro
- A decisão envolve trade-offs significativos

## Processo de submissão

1. Crie um branch `adr/XXXX-description`
2. Documente o contexto, decisão e consequências
3. Abra um PR com `RFC` no título
4. Após aprovação, atualize o status para `Accepted`
5. Adicione ao índice

## Referências

- [Michael Nygard - Documenting Architecture Decisions](https://cognitect.com/blog/2011/11/15/documenting-architecture-decisions)
- [Y-Start ADR Template](https://github.com/joelparkerhenderson/architecture-decision-record)
