# ADR-0003: Collector Gate (v1.2)

## Status

**Accepted** — v1.2.0

## Context

A Visa diferencia-se de geradores de PRD por **travar o pipeline em hipóteses sem evidência**.

**Problema histórico (v1.1)**:
- O agente Coletor instruía o LLM a parar via convenção de prompt
- O CLI não fazia enforcement
- LLMs podiam ignorar a instrução e prosseguir
- Resultado: especificações com 🟢🟡🔴 falsos

**Evolução**:
- v1.0: Convenção de prompt ("pare se não tiver evidência")
- v1.1: Mensagem informativa no CLI
- v1.2: **Enforcement computacional** via Collector Gate

## Decision

**O CLI `visa bridge` executa o Collector Gate que bloqueia o pipeline se LACUNAS sem decisão forem detectadas.**

### Fluxo do Gate

```
┌─────────────────────────────────────────┐
│  visa bridge                            │
│  ↓                                      │
│  Detectar LACUNAs em gaps.md            │
│  ↓                                      │
│  LACUNA detectada?                      │
│  ├── NÃO → Prosseguir                   │
│  └── SIM → Checar status                │
│        ├── [RESOLVIDO] → Pass           │
│        ├── [RISCO ACEITO] → Pass        │
│        └── PENDENTE → BLOQUEAR (exit 4)│
└─────────────────────────────────────────┘
```

### Critérios de Decisão

| Status | Heading Marker | Front-matter | Ação |
|--------|---------------|--------------|------|
| Resolvido | `[RESOLVIDO]` | `resolved:` | Pass |
| Risco Aceito | `[RISCO ACEITO]` | `accepted_risks:` | Pass |
| Pendente | (qualquer outro) | (ausente) | **Block** |

### Override Manual

```bash
# Override com motivo (recomendado)
visa bridge --accept-all-risks="spike de 1 dia"

# Skip completo (não recomendado)
visa bridge --skip-collector-gate
```

### Formato gaps.md Aceito

```yaml
---
accepted_risks:
  - LACUNA-003: pricing-tier — validarei pós-MVP
  - LACUNA-007: integração-operadora — spike de 3 dias
resolved:
  - LACUNA-001
---

# Gaps

### LACUNA-001 [RESOLVIDO]
- **Evidência**: 5/5 entrevistados confirmam

### LACUNA-003 [RISCO ACEITO]
- **Decisor**: Alexandre
- **Justificativa**: Validarei após MVP

### LACUNA-007
- 🔴 LACUNA não resolvida — BLOQUEIA
```

## Consequences

### Positive
- ✅ **Enforcement real** — não depende de prompt
- ✅ **Rastreabilidade** — decisões explícitas registradas
- ✅ **Qualidade** — só prossegue com evidência ou decisão consciente
- ✅ **Auditoria** — histórico de overrides para retroalimentação

### Negative
- ❌ Fricção adicional no workflow
- ❌ Usuário pode ficar frustrado com bloqueios frequentes
- ❌ Regex pode falhar com format更改 heavy

### Mitigations
- `--accept-all-risks` permite override consciente
- Documentação clara dos blockers
- `--skip-collector-gate` disponível (mas documentado como não recomendado)

## References

- [gaps.md specification](https://github.com/Adgmed2018/visa/blob/main/agents/visa-coletor/SKILL.md)
- [paridade-guard contract](https://github.com/Adgmed2018/paridade-guard)
