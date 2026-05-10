# Canonical Format Specification

Este documento especifica o formato canônico dos artefatos gerados pela Visa.

## Visão Geral

Os artefatos canônicos são arquivos Markdown com front-matter YAML que seguem um schema versionado. Eles são:

1. **Machine-readable** — parseáveis por regex sem PyYAML
2. **Versioned** — com `schemaVersion` para evolução
3. **Typed** — com `kind` para diferenciação
4. **Rastreáveis** — com IDs canônicos (`BR-FUTURE-NNN`)

## Front-Matter Schema

```yaml
---
schemaVersion: 1
kind: <tipo_do_artefato>
producedBy: <agente_que_gerou>
timestamp: <ISO-8601>
---
```

### Campos Obrigatórios

| Campo | Tipo | Descrição |
|-------|------|-----------|
| `schemaVersion` | int | Versão do schema (atual: 1) |
| `kind` | string | Tipo do artefato (específico por tipo) |
| `producedBy` | string | Agente que gerou (e.g., `visa-redator`) |
| `timestamp` | string | Timestamp ISO-8601 (opcional) |

## Artefatos Canônicos

### 1. business_model.md

**Kind**: `target_business_rules`

```yaml
---
schemaVersion: 1
kind: target_business_rules
producedBy: visa-redator
timestamp: 2025-01-15T10:30:00Z
---
```

**Corpo**: Lista de regras de negócio

```markdown
### BR-FUTURE-001
- **Origem**: `_visa_sdd/evidence_results/lac-001.md`
- **Confiança**: 🟢
- **Descrição**: CRM validation before scheduling
- **Justificativa**: 5/5 specialists interviewed
- **Compatibilidade com paradigma alvo**: Use Case with guard
```

**ID Prefixes aceitos**:
- `BR-FUTURE-` — Regra a implementar
- `BR-DESCARTAR-` — Regra descartada intencionalmente
- `BR-HUMANA-` — Decisão humana (override)

### 2. discard_log.md

**Kind**: `discard_log`

```yaml
---
schemaVersion: 1
kind: discard_log
producedBy: visa-redator
---
```

**Corpo**: Regras deliberadamente não implementadas

```markdown
### BR-DESCARTAR-001
- **Descrição**: Integração com legacy system X
- **Motivo**: Custo de migração > benefício
- **Decisor**: Alexandre
- **Data**: 2025-01-15
```

### 3. ambiguity_log.md

**Kind**: `ambiguity_log`

```yaml
---
schemaVersion: 1
kind: ambiguity_log
producedBy: visa-redator
---
```

**Corpo**: Incertezas identificadas

```markdown
### AMB-FUTURE-001
- **Descrição**: Persona "secretária" não entrevistada
- **Detectado por**: visa-coletor
- **Origem**: `_visa_sdd/gaps.md`
- **Status**: PENDENTE
```

### 4. confidence-report.md

**Kind**: `paradigm_decision`

```yaml
---
schemaVersion: 1
kind: paradigm_decision
producedBy: visa-revisor
---
```

**Corpo**: Decisão de paradigma

```markdown
# Confidence Report

## Decisão

**Paradigma**: Clean Architecture com Use Cases

## Justificativa
- Separação clara de concerns
- Testabilidade alta
- Domínio explícito

## Confiança Geral
🟡 Média — Requer validação com equipe
```

### 5. gaps.md

**Kind**: `gaps`

```yaml
---
schemaVersion: 1
kind: gaps
accepted_risks:
  - LACUNA-003: pricing-tier — validarei pós-MVP
resolved:
  - LACUNA-001
---
```

**Corpo**: Lacunas de evidência

```markdown
### LACUNA-001 [RESOLVIDO]
- **Evidência**: 5/5 entrevistados confirmam

### LACUNA-003 [RISCO ACEITO]
- **Decisor**: Alexandre
- **Justificativa**: Validarei pós MVP

### LACUNA-007
- 🔴 LACUNA não resolvida
```

## Verificação

Execute `visa validate --strict` para verificar conformidade:

```bash
visa validate --strict
# Validação de _visa_sdd/ (modo --strict)
#   Obrigatórios: 14/14
#   Opcionais: 0/12
#   Canônicos válidos: 4/4
#
# ✅ Todos os artefatos obrigatórios presentes.
#    E todos os canônicos seguem formato Reversa-compatível.
```

## Regex Patterns

### Detecção de Front-Matter

```regex
\A---\s*\n(.*?)\n---\s*\n
```

### Extração de schemaVersion

```regex
^schemaVersion\s*:\s*(\d+)\s*$
```

### Extração de kind

```regex
^kind\s*:\s*(.+?)\s*$
```

### Detecção de IDs canônicos

```regex
###\s+(BR-FUTURE-[A-Z0-9-]+)
###\s+(BR-DESCARTAR-[A-Z0-9-]+)
###\s+(AMB-FUTURE-[A-Z0-9-]+)
```

## Evolução de Schema

| Version | Changes |
|---------|---------|
| 1 | Initial release (v1.0.0+) |

Para evoluir o schema:
1. Criar novo ADR com justificativa
2. Atualizar versão para 2
3. Manter backward compatibility (v1 e v2)
4. Deprecar v1 após transição
