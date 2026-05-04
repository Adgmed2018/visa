# Quick Start — Visa em 5 minutos

Este tutorial leva você do zero a um pipeline SDD funcional em 5 minutos.

## Pré-requisitos

- Python 3.10+
- Um agente de codificação suportado: Claude Code, Cursor, Codex CLI ou Gemini CLI

## Passo 1 — Instalar (30s)

```bash
pip install visa-sdd
visa --version              # confirma instalação
```

## Passo 2 — Inicializar projeto (30s)

```bash
mkdir meu-app && cd meu-app
touch CLAUDE.md             # marca o engine = Claude Code
                            # use AGENTS.md p/ Codex, .cursorrules p/ Cursor, GEMINI.md p/ Gemini
visa install
```

Saída esperada:

```
✅ Engine detectado: Claude Code
✅ 14 skills instaladas em .claude/skills/
✅ State criado em .visa/state.json
```

## Passo 3 — Rodar o pipeline (3 min)

Abra seu agente de codificação na pasta `meu-app/` e execute:

```
/visa
```

O orquestrador convoca os 14 agentes em sequência:

1. **Pré-Descoberta:** etnografo → estrategista → coletor (com gate de evidências)
2. **Síntese:** paradigm-advisor → modelador → data-modeler → design-system
3. **Spec:** redator → strategist → inspector
4. **Handoff:** revisor → handoff

Os artefatos são salvos em `_visa_sdd/`.

## Passo 4 — Validar e fazer bridge (1 min)

```bash
visa status                 # mostra progresso
visa validate               # checa que todos os 14 artefatos esperados existem
visa bridge                 # cria stub canônico para paridade-guard
```

## Próximos passos

- Veja o [pipeline detalhado](pipeline.md)
- Entenda o [formato canônico](canonical-format.md)
- Conecte com [paridade-guard](closed-loop.md)
- Resolva problemas em [troubleshooting](troubleshooting.md)
