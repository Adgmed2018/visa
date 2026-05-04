---
name: visa-agents-help
description: Explica com analogias o que cada agente da Visa faz e quando usá-lo. Ative com `/visa-agents-help`. Espelho do reversa-agents-help, adaptado para os 14 agentes da Visa (descoberta forward).
license: MIT
compatibility: Claude Code, Codex, Cursor, Gemini CLI e demais agentes compatíveis com Agent Skills.
metadata:
  author: paridade-guard ecosystem
  version: "1.0.0"
  framework: visa
  role: help
  inverse_of: reversa-agents-help
---

Apresente exatamente o texto abaixo, sem alterações, sem resumir.

---

# Agentes da Visa — guia com analogias

A Visa é um time de especialistas em **descoberta forward** — vai de
domínio a especificação executável, antes de uma linha de código existir.
Cada agente faz uma coisa só — e faz bem.

A Visa é o espelho à frente do [Reversa](https://github.com/sandeco/reversa).
Onde o Reversa parte de código legado para extrair spec, a Visa parte de
domínio + entrevistas para construir spec.

---

## 🎼 Visa — orquestrador central
**Comando:** `/visa`

Um regente de orquestra não toca nenhum instrumento. Conhece a partitura
inteira e diz quem entra quando, em que ordem, em que ritmo.

> Use a Visa para iniciar ou retomar a descoberta completa. Ela cuida da
> sequência por você.

---

## 🗺️ Etnógrafo — o pesquisador de campo
**Comando:** `/visa-etnografo`

O etnógrafo passa semanas no terreno antes de escrever uma linha. Mapeia
quem mora no bairro, qual a língua, os rituais, os horários, sem julgar
nem propor mudanças. Apenas descreve o que vê.

> Use o Etnógrafo no começo. Ele mapeia o domínio na superfície —
> personas iniciais, glossário, landscape do mercado — sem entrar em
> análise causal.

---

## 🧭 Estrategista — o analista que cruza dados
**Comando:** `/visa-estrategista`

Depois do etnógrafo, vem o estrategista. Olha o mapa que o etnógrafo
desenhou e pergunta: *"Onde estão as oportunidades? Quais dores
realmente importam?"* Ele cruza personas com jornadas, identifica padrões.

> Use o Estrategista após o Etnógrafo. Ele extrai dores priorizadas e
> oportunidades de negócio.

---

## 🔍 Coletor — o detetive cético
**Comando:** `/visa-coletor`

Sherlock Holmes para hipóteses. Olha cada lacuna 🔴 e exige: *"Onde está
a evidência? Quem você entrevistou? Qual número confirma isso?"* Não
inventa, não preenche, **trava o pipeline** se hipótese aparece sem dado.

> Use o Coletor sempre que houver 🔴 LACUNA no projeto. Ele gera planos
> de coleta (entrevistas, smoke tests, dados públicos) e **bloqueia o
> bridge computacionalmente** (exit code 4) até você resolver ou aceitar
> risco explicitamente.

---

## 🎯 Paradigm Advisor — o conselheiro técnico
**Comando:** `/visa-paradigm-advisor`

Um arquiteto sênior chamado para decidir se o prédio será de concreto,
madeira ou aço. A escolha define tudo depois — não pode ser refeita.

> Use o Paradigm Advisor após Etnógrafo + Estrategista, antes do
> Modelador. Ele força decisão consciente do paradigma de programação
> (Clean Architecture, OO+DI, FP, event-driven) baseado em domínio e
> maturidade da equipe.

---

## 📐 Modelador — o cartógrafo
**Comando:** `/visa-modelador`

O cartógrafo recebe os relatórios do etnógrafo e do estrategista, e
desenha o mapa oficial: como funciona o sistema, quais entidades existem,
como elas se conectam.

> Use o Modelador após Estrategista + Paradigm Advisor. Ele sintetiza
> domínio, fluxos e arquitetura em diagramas executáveis.

---

## 🗄️ Data Modeler — o engenheiro de banco
**Comando:** `/visa-data-modeler`

O engenheiro civil que olha a planta arquitetônica e desenha a hidráulica
e elétrica. Ninguém vai morar bem se as conexões não forem pensadas
antes do reboco.

> Use o Data Modeler após o Modelador. Ele propõe ERD, tabelas, FKs,
> CHECK constraints — tudo prospectivo, com escala 🟢🟡🔴 sobre cada
> decisão. Detecta lacunas de modelagem que viram entrada para o Coletor.

---

## 🎨 Design System — o coordenador estético
**Comando:** `/visa-design-system`

O designer industrial que padroniza maçanetas, cores, materiais antes do
prédio começar. Sem isso cada quarto vira uma improvisação.

> Use o Design System em paralelo com o Modelador. Ele propõe paleta
> semântica, escala tipográfica, tokens de espaçamento, inventário de
> componentes — tudo antes de qualquer mockup. Marca com 🟡 o que é
> placeholder até identidade visual real chegar.

---

## ✍️ Redator — o escriba técnico
**Comando:** `/visa-redator`

O escriba que transforma decisões em texto canônico, com IDs estáveis e
formato auditável. Não cria, registra. Garante que cada regra tenha um
identificador único que sobrevive a refator.

> Use o Redator após Modelador + Data Modeler + Design System. Ele
> produz `business_model.md` com `BR-FUTURE-NNN`, `discard_log.md`,
> `ambiguity_log.md` — todos no formato canônico Reversa-compatível
> consumível pelo paridade-guard.

---

## 📋 Strategist — o estrategista de lançamento
**Comando:** `/visa-strategist`

O coach de startups que olha sua descoberta e pergunta: *"OK, e como
vocês vão lançar? Concierge? MVP? Plataforma?"* Sem isso, descoberta vira
PRD que ninguém implementa.

> Use o Strategist após o Redator. Ele propõe estratégia de go-to-market
> com 2-3 alternativas, recomendando uma justificadamente. Produz
> `mvp_roadmap.md`, `risk_register.md`, `gtm_strategy.md`.

---

## 🔬 Inspector — o auditor de aceitação
**Comando:** `/visa-inspector`

O auditor que escreve, antes da obra começar, a lista de critérios para
*"obra entregue"*. Sem isso, pedreiro entrega o que ele acha que é
suficiente.

> Use o Inspector após Strategist. Ele transforma cada `BR-FUTURE-NNN`
> em feature Gherkin executável (`.feature` files) e produz coverage
> matrix. É o que conecta a Visa ao paridade-guard.

---

## 🔍 Revisor — o auditor cruzado
**Comando:** `/visa-revisor`

O par que revisa o código de outro par. Não escreve nada novo. Encontra
inconsistência, contradição entre artefatos, lacunas que escaparam.

> Use o Revisor antes do Handoff. Ele faz auditoria cruzada entre todos
> os artefatos produzidos pelos agentes anteriores, gera
> `confidence-report.md` com `paradigm_decision` final consolidado.

---

## 🤝 Handoff — o gerente de entrega
**Comando:** `/visa-handoff`

O gerente que prepara o pacote final para entrega: documentação, riscos,
pontos abertos, próximos passos com 4 caminhos possíveis (Spec Kit /
Codex / Cursor / Reconstructor do Reversa).

> Use o Handoff por último. Ele consolida `handoff.md` com tudo que o
> agente de codificação precisa para começar a implementar.

---

## 🆘 Agents Help — este guia
**Comando:** `/visa-agents-help`

Você está aqui agora.

> Use quando esquecer qual agente faz o quê.

---

# Sequência típica

```
/visa
  └── /visa-etnografo
       └── /visa-estrategista
            └── /visa-coletor          (resolve 🔴 LACUNAs)
                 └── /visa-paradigm-advisor
                      └── /visa-modelador
                           ├── /visa-data-modeler
                           └── /visa-design-system
                                └── /visa-redator
                                     └── /visa-strategist
                                          └── /visa-inspector
                                               └── /visa-revisor
                                                    └── /visa-handoff
                                                         └── visa bridge → paridade-guard
```

A `visa` orquestrador conduz tudo isso por você. Estes comandos individuais
são para invocar agentes específicos quando necessário (ex: refazer só o
Modelador depois de mudar paradigma).

---

# Comparação com Reversa (espelho à trás)

| Visa (frente) | Reversa (trás) |
|---|---|
| visa | reversa |
| visa-etnografo | reversa-scout |
| visa-estrategista | reversa-archaeologist |
| visa-coletor | reversa-detective |
| visa-paradigm-advisor | reversa-paradigm-advisor |
| visa-modelador | reversa-architect |
| visa-data-modeler | reversa-data-master |
| visa-design-system | reversa-design-system |
| visa-redator | reversa-writer + curator + designer |
| visa-strategist | reversa-strategist |
| visa-inspector | reversa-inspector |
| visa-revisor | reversa-reviewer |
| visa-handoff | reversa-migrate |
| visa-agents-help | reversa-agents-help |

**Não espelhados (decisão consciente):**
- `reversa-visor` — extrai UI de screenshots; não aplica à descoberta forward
- `reversa-reconstructor` — auto-reimplementa código; Visa entrega ao usuário
  escolher o agente de codificação
