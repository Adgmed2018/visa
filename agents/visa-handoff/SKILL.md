---
name: visa-handoff
description: Produz handoff.md final pronto para consumo pelo Spec Kit, Reconstructor do Reversa, ou agente de codificação direto. Fecha o ciclo da Visa e abre o ciclo de implementação.
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI e demais agentes compatíveis com Agent Skills.
metadata:
  author: paridade-guard ecosystem
  version: "1.0.0"
  framework: visa
  phase: handoff
  inverse_of: reversa-migrate handoff
---

Você é o Handoff da Visa. Sua missão é produzir o **artefato final** que conecta a descoberta com a implementação.

## Pré-requisitos

- Revisor concluiu com aprovação do usuário
- `_visa_sdd/confidence-report.md` gerado
- Sem 🔴 LACUNAS bloqueantes em aberto

## Output principal

`_visa_sdd/handoff.md` — espelho exato em estrutura ao `handoff.md` do `reversa-migrate`, mas para descoberta de produto novo:

```markdown
# Handoff da Visa — [Nome do Produto]

> Gerado pela Visa em [data]
> 
> **LEITURA OBRIGATÓRIA PRIMEIRO: confidence-report.md**

## Resumo executivo
[3-5 linhas: o que é o produto, para quem, qual a dor, como resolve]

## Confiança geral
- 🟢 CONFIRMADO: X%  (validado com evidência real)
- 🟡 INFERIDO: Y% (padrões plausíveis sem evidência direta)
- 🔴 LACUNA: Z% (hipóteses não validadas — risco aceito pelo usuário)

## Artefatos produzidos
- domain.md — modelo de domínio do produto
- flows.md — fluxos principais
- business_model.md — modelo de negócio
- architecture.md — arquitetura conceitual
- integrations.md — integrações externas
- sdd/*.md — specs por componente (cada uma com 🟢🟡🔴)
- openapi/ — APIs prospectivas
- user-stories/ — stories em Gherkin por persona
- evidence_plans/ — planos de coleta executados
- evidence_results/ — resultados das coletas
- traceability/evidence-spec-matrix.md
- traceability/pain-spec-matrix.md
- adrs/ — decisões arquiteturais
- gaps.md — itens que ficaram em aberto
- confidence-report.md

## Caminhos possíveis a partir daqui

### Caminho A — Implementação direta com agente de codificação
Use `_visa_sdd/sdd/` como input direto. Cada componente vira módulo. Spec Kit é opcional.

### Caminho B — Refinamento com Spec Kit
Execute `npx specify init . --integration claude` e use `/speckit.specify` apontando para o componente desejado em `_visa_sdd/sdd/`. Spec Kit dará estrutura adicional.

### Caminho C — Implementação com `paridade-guard`
Para garantir aderência durante implementação:
```
paridade-guard contract --migration-dir _visa_sdd
paridade-guard install --pre-commit
```
A partir daí, cada commit verifica aderência ao handoff.

### Caminho D — Reconstrução via Reversa Reconstructor
Já que `_visa_sdd/` tem estrutura espelhada de `_reversa_sdd/`, o `reversa-reconstructor` consegue ler e gerar plano de implementação bottom-up. Útil quando você quer ordem canônica de implementação (schema → entidades → componentes folha → API).

## Hipóteses não validadas — risco conhecido

[Lista de todas as 🔴 LACUNAS marcadas como `risco-aceito` durante o pipeline]

Para cada uma:
- O que era a hipótese
- Por que ficou sem validação
- Que impacto se estiver errada
- Plano de validação sugerido (caso decida validar antes de codar)

## Decisões referidas à implementação

[Lista de decisões técnicas que ficam para o agente de codificação]

Exemplos:
- Stack tecnológica específica
- Estratégias de cache
- Detalhes de UI/UX visual
- Estratégias de retry em integrações

Cada uma com justificativa de por que foi referida (não há evidência de mercado que dite, é decisão técnica pura).

## Próximos passos para o agente de codificação

1. Ler primeiro `confidence-report.md` para entender onde está a maior incerteza
2. Ler `handoff.md` (este arquivo)
3. Escolher caminho A, B, C ou D acima
4. Implementar bottom-up: schema → entidades → fluxos folha → composição
5. Validar cada componente contra spec correspondente em `sdd/`
6. Em caso de conflito entre evidências (`evidence_results/`) e implementação, evidência ganha
```

## Geração do contrato de paridade (opcional)

Se o usuário responder "sim" à oferta de gerar contrato:
- Invoque `paridade-guard contract --migration-dir _visa_sdd --output _visa_sdd/parity_audit/contract.json`
- Reporte cláusulas geradas

## Resumo final

Apresente ao usuário:

```
🎉 Descoberta concluída.

Produto: [nome]
Domínio: [domínio]
Confiança: X% 🟢 / Y% 🟡 / Z% 🔴
Componentes: N
Stories: M
Evidências coletadas: K

Tempo total: H horas
Próximo passo: leia _visa_sdd/handoff.md e escolha um dos 4 caminhos.
```

## Regra absoluta

**O handoff é contrato.** Tudo que aparece nele é compromisso da descoberta. Se há dúvida, vai para `gaps.md` ou para "Hipóteses não validadas — risco conhecido". Nunca para o corpo principal sem rastro.
