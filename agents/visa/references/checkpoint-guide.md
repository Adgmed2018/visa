# Checkpoint Guide

> Como atualizar `.visa/state.json` consistentemente após cada agente concluir.

## Estrutura do state.json

```json
{
  "version": "1.1.0",
  "project": "<nome do projeto>",
  "user_name": "<nome>",
  "chat_language": "pt-br",
  "doc_language": "Português",
  "answer_mode": "chat",
  "discovery_level": "essencial | completo | detalhado",
  "output_folder": "_visa_sdd",
  "phase": "<fase atual>",
  "completed": ["fase1", "fase2"],
  "pending": ["fase3", "fase4"],
  "engines": ["claude-code"],
  "agents": ["visa", "visa-etnografo", ...],
  "checkpoints": {
    "imersao": {
      "completed_at": "ISO-8601",
      "agent": "visa-etnografo",
      "artifacts": ["landscape.md", "personas-inicial.md", "glossario.md"]
    }
  },
  "created_files": [...]
}
```

## Quando salvar

Após cada agente concluir, antes de ativar o próximo:

1. Mover a fase de `pending` para `completed`
2. Atualizar `phase` para a próxima fase em `pending` (ou null se acabou)
3. Adicionar entrada em `checkpoints[<fase>]` com:
   - `completed_at`: ISO-8601 UTC
   - `agent`: nome do agente que rodou
   - `artifacts`: lista de arquivos produzidos em `_visa_sdd/`
4. Marcar tarefa correspondente em `.visa/plan.md` com ✅

## Mapeamento fase → agente principal

| Fase | Agente principal | Artefatos esperados |
|---|---|---|
| imersao | visa-etnografo | landscape.md, personas-inicial.md, glossario.md, concorrentes.md |
| descoberta | visa-estrategista | pains.md, opportunities.md (uma análise por jornada) |
| validacao | visa-coletor | gaps.md (atualizado), evidence_plans/, evidence_scripts/ |
| sintese | visa-modelador | domain.md, flows.md, business_model.md (rascunho), architecture.md |
| geracao | visa-redator | business_model.md (canônico), discard_log.md, ambiguity_log.md, sdd/, openapi/, user-stories/, traceability/ |
| revisao | visa-revisor | confidence-report.md |
| handoff | visa-handoff | handoff.md |

## Atomicidade

Sempre escreva o state.json em duas etapas para evitar corrupção em caso
de interrupção:

1. Escreva em `.visa/state.json.tmp`
2. Renomeie para `.visa/state.json` (rename é atômico no POSIX)

Implementação típica em Python:
```python
import json, os
tmp = state_path.with_suffix('.json.tmp')
tmp.write_text(json.dumps(state, indent=2, ensure_ascii=False), encoding='utf-8')
os.replace(tmp, state_path)
```

## Quando NÃO atualizar

- Se um agente abortou no meio (usuário cancelou, contexto estourou):
  NÃO mover a fase para completed. Deixe `phase` no atual. Próxima sessão
  retoma de onde estava.
- Se artefatos esperados não foram criados: marque o agente como falhou em
  `checkpoints[<fase>].failed_at` em vez de `completed_at`.
