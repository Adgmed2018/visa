# Closed-Loop SDD — Visa + paridade-guard

## Visão geral

O ciclo SDD fechado garante que o código entregue **honra a especificação descoberta**, sem dependência de boa vontade do agente de codificação.

```
                              ┌─────────────────────┐
                              │   Visa (forward)    │
                              │  14 agentes em      │
                              │  Claude/Cursor/etc. │
                              └──────────┬──────────┘
                                         │
                                         ▼
                              ┌─────────────────────┐
                              │  Artefatos canônicos│
                              │  BR-FUTURE-NNN      │
                              │  AMB-FUTURE-NNN     │
                              └──────────┬──────────┘
                                         │
                              visa bridge │
                                         ▼
                              ┌─────────────────────┐
                              │   paridade-guard    │
                              │   ≥ 0.3.0           │
                              │   gatekeeper        │
                              └──────────┬──────────┘
                                         │
                              ┌──────────┴──────────┐
                              ▼                     ▼
                          ✅ aprova              ❌ bloqueia
                          implementação         se desviar da spec
```

## Como funciona

1. **Visa produz spec:** os 14 agentes geram artefatos em `_visa_sdd/` com IDs canônicos.
2. **`visa bridge` traduz:** converte os IDs `BR-FUTURE-NNN` em cláusulas que o paridade-guard entende.
3. **paridade-guard valida:** durante CI, compara código entregue vs spec original. Bloqueia merge se houver desvio.

## Setup

```bash
pip install visa-sdd>=1.4.0
pip install paridade-guard>=0.3.0
```

No CI (GitHub Actions exemplo):

```yaml
- name: Validate spec
  run: visa validate --strict

- name: Run paridade-guard
  run: paridade-guard validate _visa_sdd/migration/target_business_rules.md
```

## IDs canônicos

| Prefixo | Significado |
|---|---|
| `BR-FUTURE-NNN` | Regra de negócio a implementar |
| `BR-DESCARTAR-NNN` | Regra deliberadamente descartada |
| `BR-HUMANA-NNN` | Decisão humana pendente |
| `AMB-FUTURE-NNN` | Ambiguidade a resolver |
| `LACUNA-NNN` | Lacuna de evidência (acionada pelo Coletor) |

Detalhes do schema em [canonical-format.md](canonical-format.md).

## Por que isso importa

Sem o ciclo fechado, é fácil o agente "alucinar" implementação que não bate com a spec discutida. O `paridade-guard` é o policial que **força a coerência** entre o que foi pedido e o que foi entregue.
