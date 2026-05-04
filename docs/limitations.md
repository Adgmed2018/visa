# Limitações da Visa v1.4.0

Transparência radical: aqui está o que **a Visa ainda NÃO faz bem** ou onde requer cuidado.

## Limitações funcionais

### 1. Validação LLM real dos 6 SKILLs novos pendente

Os 6 agentes adicionados na v1.3.0 (`paradigm-advisor`, `data-modeler`, `design-system`, `strategist`, `inspector`, `agents-help`) têm fixtures estruturais de teste, mas **a execução em LLM real (3 runs por SKILL em domínio controlado)** está prevista para v1.4.1. Protocolo está em `tests/llm-validation/`.

### 2. Bug conhecido: `set_quiet(True)` não suprime info

Em `visa_sdd.logging`, o caminho de `info()` não checa o flag `_G_QUIET`. Marcado como `xfail` em `tests/test_logging_exceptions.py`. Fix planejado para v1.4.1.

### 3. Sem case study externo

O case study "Second Opinion Médica" é interno. Não há ainda um case de usuário externo rodando o pipeline em projeto real.

### 4. Coverage por módulo desigual

| Módulo | Coverage v1.4.0 | Meta v1.5.0 |
|---|---|---|
| `cli.py` | 82% | 90% |
| `exceptions.py` | 87% | 90% |
| `logging.py` | 67% | 85% |
| **Total** | **80%** | **88%** |

## Limitações arquiteturais

### 5. CLI ainda monolítico

`cli.py` tem ~1.085 linhas em arquivo único. Refactor em módulos (`commands/`, `core/`, `parsing/`, `models/`) está planejado mas **não foi feito nesta release** — a prioridade desta versão foi corrigir bugs reais (SyntaxError, ruff, mypy) descobertos pela primeira execução de fato dos checkers.

### 6. Sem testes de carga ou performance

A suite atual cobre correctness, não performance. Para projetos com `_visa_sdd/` muito grande, comportamento sob escala não foi medido.

### 7. Pipeline de 14 agentes pode causar fadiga de contexto em LLMs

Em projetos grandes, contexto pode estourar. Use checkpoint via `state.json` (já implementado) e quebre o pipeline em múltiplas sessões.

## Limitações de ecossistema

### 8. Dependência de `paridade-guard ≥ 0.3.0`

O ciclo fechado SDD requer paridade-guard instalado. Sem ele, a Visa funciona standalone mas perde o gatekeeper.

### 9. Reversa upstream pode divergir

Conforme o Reversa (do Sandeco) evolui, decisões de espelhamento podem ficar desatualizadas. Cobertura atual: 14/16 = 87.5%.

## Roadmap de mitigação

| Versão | Foco |
|---|---|
| v1.4.0 (esta) | Bug fixes reais, ruff/mypy strict verde, coverage 80%, README enxuto |
| v1.4.1 | Validação LLM real dos 6 SKILLs + fix do bug `set_quiet` |
| v1.5.0 | Refactor modular do CLI + coverage ≥85% + 1 case study externo |
| v2.0.0 | API estável, breaking changes consolidados |

Veja [CHANGELOG.md](../CHANGELOG.md) para detalhes por release.
