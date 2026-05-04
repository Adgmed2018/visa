# ADR-0002: Canonical ID System (BR-FUTURE/AMB-FUTURE)

## Status

**Accepted** — v1.0.0

## Context

A Visa gera especificações que precisam ser:
1. **Rastreáveis** — identificar cada decisão de negócio unicamente
2. **Consumíveis** — pelo paridade-guard para validação de commit
3. **Auditáveis** — permitir追溯 (traceback) de conversa → spec → implementation

**Problema**: Sem IDs canônicos, é impossível:
- Mapear spec para código implementado
- Detectar duplicação de regras
- Fazer auditoria adversarial
- Gerar contratos para paridade-guard

**Alternativas Considered**:
1. UUIDs (garantem unicidade mas são opacos)
2. Números sequenciais (simples mas sem contexto semântico)
3. Prefixo + número (legível mas sem hierarquia)
4. Hierárquico com dots (verbose)

## Decision

**Usar ID canônico com prefixo semântico + número sequencial.**

### Sistema de IDs

| Prefix | Meaning | Example |
|--------|---------|---------|
| `BR-FUTURE-NNN` | Business rule to implement | `BR-FUTURE-001` |
| `BR-DESCARTAR-NNN` | Deliberate non-implementation | `BR-DESCARTAR-001` |
| `BR-HUMANA-NNN` | Human decision (override) | `BR-HUMANA-001` |
| `AMB-FUTURE-NNN` | Ambiguity to resolve | `AMB-FUTURE-001` |
| `AMB-NNN` | Ambiguity (minor) | `AMB-001` |
| `LACUNA-NNN` | Evidence gap | `LACUNA-001` |

### Formato no Markdown

```markdown
### BR-FUTURE-001
- **Origem**: `_visa_sdd/evidence_results/lac-001.md`
- **Confiança**: 🟢
- **Descrição**: CRM validation before scheduling
- **Justificativa**: Evidence from 5 specialists
```

### Regras de Geração

1. **NNN é sequencial** — não se repete dentro de um artefato
2. **Prefixo é imutável** — não mudar após criado
3. **Origem é rastreável** — cada BR aponta para a evidência que o gerou

## Consequences

### Positive
- ✅ IDs são legíveis (human-readable)
- ✅ Prefix encodes semantic meaning
- ✅ paridade-guard consegue extrair via regex
- ✅ Traceability implícita (origem no campo)

### Negative
- ❌ Não detecta conflito entre BRs em artefatos diferentes
- ❌ NNN resetaria se artefato for recriado

### Mitigations
- paridade-guard valida global uniqueness via full scan
- Manifest SHA-256 garante que artefato não foi recriado silenciosamente

## References

- [paridade-guard extractor](https://github.com/Adgmed2018/paridade-guard)
- [Reversa BR-MIGRAR pattern](https://github.com/sandeco/reversa)
