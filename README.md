# Visa — Forward Spec Discovery for AI Agents

> Espelho à frente do [Reversa](https://github.com/sandeco/reversa).
> Enquanto o Reversa transforma código legado em especificação, a Visa
> transforma domínio de negócio em especificação executável por agentes de IA.

[![tests](https://img.shields.io/badge/tests-40%2F40%20passing-brightgreen)](#testes)
[![paridade-guard](https://img.shields.io/badge/paridade--guard-%E2%89%A50.3.0-blue)](https://github.com/Adgmed2018/paridade-guard)
[![license](https://img.shields.io/badge/license-MIT-green)](LICENSE)
[![python](https://img.shields.io/badge/python-%E2%89%A53.10-blue)]()
[![agents](https://img.shields.io/badge/agents-14-purple)]()

**Versão atual: 1.3.0** (ver [CHANGELOG](CHANGELOG.md))

---

## TL;DR técnico

Framework de descoberta de produto via pipeline de **14 agentes especializados**
(skills `.md` para Claude Code / Codex / Cursor / Gemini CLI). Diferente de
geradores de PRD:

1. **Trava o pipeline em hipóteses sem evidência** — agente *Coletor* gera
   planos de coleta (entrevistas, smoke tests, dados públicos), e o **CLI
   tem gate computacional** (v1.2): `visa bridge` recusa prosseguir com
   exit code 4 se `gaps.md` tem 🔴 LACUNAS sem decisão explícita.
2. **Emite artefatos no formato canônico Reversa** (`schemaVersion: 1`,
   IDs estáveis `BR-FUTURE-NNN` / `AMB-FUTURE-NNN`) — consumíveis nativamente
   por `paridade-guard ≥ 0.3.0`.
3. **Compõe ciclo SDD em PT** com Reversa (trás) e paridade-guard (meio):
   descoberta → spec → implementação → verificação.

---

## Instalação

### Via pip (recomendado)

```bash
pip install visa-sdd
visa --version  # 1.1.1
```

### Via clone (modo dev)

```bash
git clone https://github.com/Adgmed2018/visa
cd visa
python3 bin/visa --version  # 1.1.1
# Opcional: pip install -e . para colocar `visa` no PATH
```

### Pré-requisito para o ciclo completo

Para que o `bridge` da Visa entregue cláusulas reais ao verificador:

```bash
pip install paridade-guard>=0.3.0
```

Versões anteriores do paridade-guard tratam `BR-FUTURE-NNN` como prefixo
desconhecido e geram contrato vazio.

---

## Demo de 5 minutos (reproduzível)

```bash
# 1. Setup
mkdir demo && cd demo && touch CLAUDE.md
visa install
# ✅ Visa instalada (versão 1.1.1)
#    Engines: claude-code
#    Agentes: 8

# 2. Para o demo, criamos o artefato canônico mínimo.
#    Em uso real, isso é gerado pelo visa-redator durante a sessão Claude Code.
cat > _visa_sdd/business_model.md <<'EOF'
---
schemaVersion: 1
kind: target_business_rules
producedBy: visa-redator
---
# Target Business Rules

## Regras IMPLEMENTAR

### BR-FUTURE-001
- **Origem**: `_visa_sdd/evidence_results/lac-001.md`
- **Confiança**: 🟢
- **Descrição**: Validação de CRM ativo antes de criar agendamento
- **Justificativa**: 5/5 médicos entrevistados confirmaram requerimento
EOF

# 3. Validar formato canônico
visa validate --strict

# 4. Construir ponte para o paridade-guard
visa bridge

# 5. Extrair contrato com cláusulas reais
paridade-guard contract \
  --migration-dir _visa_sdd/migration \
  --output _visa_sdd/parity_audit/contract.json

# Saída literal esperada:
# ✅ Contrato gerado: _visa_sdd/parity_audit/contract.json
#    Cláusulas: 1  (bloqueantes: 1, advertências: 0)
#    Por tipo:  {'regra-futuro': 1}
#    Avisos: 4 (state.json ausente, paradigm/discard/ambiguity_log ausentes)
#
# Para um demo com 7 cláusulas e 6 tipos diferentes,
# veja AUTO-AVALIACAO.md → "Métricas reproduzíveis" → "Demo completo".
```

---

## Os 14 agentes (espelhamento parcial honesto do Reversa)

A Visa cobre o **ciclo de descoberta forward**. Os 14 agentes estão
organizados em 5 times sequenciais, espelhando conceitualmente — mas não
1:1 — os 18 agentes do Reversa.

### 🎼 Orquestrador

| Visa | Função | Reversa |
|---|---|---|
| **visa** | Conduz o pipeline de ponta a ponta com escala 🟢🟡🔴 | reversa |

### 🗺️ Time de Descoberta (1-3)

| Visa | Função | Reversa |
|---|---|---|
| **visa-etnografo** | Mapeia domínio na superfície (personas iniciais, glossário) | reversa-scout |
| **visa-estrategista** | Cruza personas com jornadas, extrai dores priorizadas | reversa-archaeologist |
| **visa-coletor** ⭐ | Resolve LACUNAS forçando evidência real | reversa-detective |

### 🎯 Time de Síntese (4-7)

| Visa | Função | Reversa |
|---|---|---|
| **visa-paradigm-advisor** | Decide paradigma alvo (Clean / OO+DI / FP / event-driven) | reversa-paradigm-advisor |
| **visa-modelador** | Sintetiza domínio, fluxos, arquitetura | reversa-architect |
| **visa-data-modeler** | Modela esquema de dados prospectivo (ERD, tabelas, FKs) | reversa-data-master |
| **visa-design-system** | Propõe tokens (paleta, tipografia, espaçamento) | reversa-design-system |

### ✍️ Time de Spec (8-10)

| Visa | Função | Reversa |
|---|---|---|
| **visa-redator** | Gera specs canônicas + IDs `BR-FUTURE-NNN` | reversa-writer (+ curator + designer consolidados) |
| **visa-strategist** | Estratégia de go-to-market e MVP roadmap | reversa-strategist |
| **visa-inspector** | Define acceptance tests prospectivos em Gherkin | reversa-inspector |

### 🤝 Time de Handoff (11-12)

| Visa | Função | Reversa |
|---|---|---|
| **visa-revisor** | Auditoria cruzada antes do handoff | reversa-reviewer |
| **visa-handoff** | Produz handoff.md final com 4 caminhos | reversa-migrate |

### 🆘 Utilitário

| Visa | Função | Reversa |
|---|---|---|
| **visa-agents-help** | Guia com analogias dos 14 agentes | reversa-agents-help |

⭐ O **Coletor** é a peça única no ecossistema de geradores de spec em PT:
trava o pipeline em hipóteses sem evidência e produz plano específico de
coleta. **Importante (v1.2+):** o gate é **computacional**, não apenas
convenção de prompt. `visa bridge` recusa prosseguir (exit code 4) se
`gaps.md` tem 🔴 LACUNAS sem decisão explícita registrada como
`[RESOLVIDO]`, `[RISCO ACEITO]`, ou `accepted_risks:` no front-matter.
Override manual via `visa bridge --accept-all-risks="motivo"`.

---

## Diferenças do Reversa (honestidade documental)

A Visa é **inspirada** pelo Reversa e emite formato **compatível** com ele,
mas tem assimetrias estruturais que esta seção declara explicitamente para
não criar expectativas falsas:

| Aspecto | Reversa | Visa |
|---|---|---|
| Linguagem | Node.js (npm) | Python (pip) |
| Distribuição | `npm install -g reversa` | `pip install visa-sdd` |
| Versão atual | 1.2.21 (madura) | 1.3.0 (beta) |
| Total de agentes | 18 | **14** (12 espelhados + 2 consolidados) |
| Templates `.md` populados | 12 templates em `templates/migration/artifacts/` | 0 (formatos descritos como prosa nos SKILL.md) |
| Stack alvo | Análise de código legado | Descoberta de produto novo |
| Direção temporal | Backward (passado → presente) | Forward (futuro → presente) |
| Aprovação oficial | Repo oficial do @sandeco | Extensão voluntária Reversa-compatível, sem afiliação |

### Espelhamento dos agentes — caso a caso

**Espelhados 1:1 (12)**:
visa, visa-etnografo, visa-estrategista, visa-coletor, visa-paradigm-advisor,
visa-modelador, visa-data-modeler, visa-design-system, visa-strategist,
visa-inspector, visa-revisor, visa-handoff, visa-agents-help.

**Consolidados em `visa-redator` (3 → 1)**: `reversa-writer + reversa-curator
+ reversa-designer`. Razão: na Visa, "decidir o que migra/descarta" e
"desenhar specs do novo" são a mesma operação que "escrever o spec
canônico", já que não há legado para curar nem código existente para
redesenhar.

**Não espelhados (decisão consciente, 2)**:
- `reversa-visor` — extrai UI a partir de screenshots do legado. Não aplica
  à descoberta forward, onde não há produto pré-existente para fotografar.
- `reversa-reconstructor` — auto-reimplementa código a partir de spec.
  A Visa termina no handoff e deixa o usuário escolher o agente de
  codificação (Claude Code, Codex, Cursor, ou o próprio reconstructor do
  Reversa).

**Cobertura**: 14 de 16 agentes aplicáveis = **87.5% de espelhamento sobre
o conjunto que faz sentido**. A Visa cobre o ciclo de descoberta, **não
pretende espelhamento 1:1** — pretende cobertura conceitual completa do
que é traduzível de backward para forward.

### Por que a Visa não tem templates `.md` populados como o Reversa

O Reversa reúne 12 templates como referência canônica para o LLM. A Visa,
em vez disso, embute o template literal dentro do `visa-redator/SKILL.md`
(ver linhas 30-110 do SKILL). Decisão de trade-off: menos arquivos, mas
acoplamento maior entre agente e formato. v1.4 pode separar.

---

## Gate computacional do Coletor (v1.2)

O **Coletor** é a peça única que diferencia a Visa de geradores de PRD
do mercado. Outros geradores produzem hipóteses e seguem em frente como
se fossem fato. A Visa **trava** computacionalmente.

### Como funciona

`visa bridge` lê `_visa_sdd/gaps.md`, detecta padrões de LACUNA e
classifica cada uma:

| Classificação | Como marcar | Bridge prossegue? |
|---|---|---|
| Resolvida | `### LACUNA-NNN [RESOLVIDO]` no heading | ✅ |
| Risco aceito (heading) | `### LACUNA-NNN [RISCO ACEITO]` | ✅ |
| Risco aceito (front-matter) | `accepted_risks: [LACUNA-NNN]` | ✅ |
| Override manual | `visa bridge --accept-all-risks="motivo"` | ✅ (com warning) |
| Override total | `visa bridge --skip-collector-gate` | ✅ (não recomendado) |
| Pendente | nenhuma das acima | ❌ exit code 4 |

### Saída quando bloqueia

```
🔍 Gate do Coletor: 2 LACUNA(s) detectada(s) em gaps.md
   ✅ Resolvidas:    1
   ⚠️  Risco aceito: 0
   🔴 PENDENTES:    1

🛑 BRIDGE BLOQUEADA pelo gate do Coletor.

   1 LACUNA(s) sem decisão explícita:
     - LACUNA-001

   Para cada LACUNA, escolha UMA das opções:
   1) RESOLVER com evidência — atualize a LACUNA no gaps.md...
   2) ACEITAR RISCO explicitamente — marque no heading...
   3) ACEITAR RISCO via front-matter (em lote)...
   4) OVERRIDE manual no comando (com motivo)...
```

### Por que isto importa

Sem gate computacional, "Coletor" era convenção de prompt — disciplina
dependia do LLM seguir a instrução e do usuário ser disciplinado. Com
gate, **o CLI obriga** registro explícito de cada decisão. Você pode
aceitar risco, mas não pode passar batido.

Esse é o único mecanismo no ecossistema Reversa+Visa+paridade-guard que
**força registro de decisões sobre incerteza**. É o que torna a Visa
mais que um gerador de PRD bonito.

---


A Visa propaga uma escala única em todos os artefatos:

- 🟢 **CONFIRMADO** — validado com evidência real (entrevista, dado de mercado, MVP rodado, contrato assinado)
- 🟡 **INFERIDO** — hipótese plausível baseada em padrão conhecido, sem evidência direta
- 🔴 **LACUNA** — hipótese pura. Bloqueia avanço até virar entrevista, teste ou pesquisa.

No `paridade-guard` ≥ 0.3.0, mapeada para severidade:

| Confiança | Severidade no contrato |
|---|---|
| 🟢 | bloqueante |
| 🟡 | advertência |
| 🔴 | advertência (não devia chegar até aqui — voltar ao Coletor) |

---

## Escala de confiança

A Visa propaga uma escala única em todos os artefatos:

- 🟢 **CONFIRMADO** — validado com evidência real (entrevista, dado de mercado, MVP rodado, contrato assinado)
- 🟡 **INFERIDO** — hipótese plausível baseada em padrão conhecido, sem evidência direta
- 🔴 **LACUNA** — hipótese pura. **Bloqueia avanço** computacionalmente até virar entrevista, teste ou pesquisa, OU ser explicitamente marcada como risco aceito.

No `paridade-guard` ≥ 0.3.0, mapeada para severidade:

| Confiança | Severidade no contrato |
|---|---|
| 🟢 | bloqueante |
| 🟡 | advertência |
| 🔴 | advertência (não devia chegar até aqui — voltar ao Coletor) |

---

## Comandos do CLI

```bash
visa install                # Instala skills no projeto
visa status                 # Estado atual da descoberta
visa validate               # Valida presença dos 14 artefatos obrigatórios
visa validate --strict      # E também o formato canônico (front-matter, IDs)
visa bridge                 # Gate do Coletor + valida formato + cria stub
visa bridge --accept-all-risks="motivo"   # Override do gate (v1.2)
visa bridge --skip-collector-gate         # Ignora gate (não recomendado)
visa uninstall              # Remove skills + .visa/ (preserva _visa_sdd/)
visa uninstall --purge      # Remove também _visa_sdd/
visa uninstall --yes        # Não interativo (para scripts)
visa --version              # 1.3.0
visa --help
```

---

## Estrutura produzida em `_visa_sdd/`

```
_visa_sdd/
├── landscape.md              ← visa-etnografo
├── personas-inicial.md       ← visa-etnografo
├── glossario.md              ← visa-etnografo
├── pains.md                  ← visa-estrategista
├── opportunities.md          ← visa-estrategista
├── domain.md                 ← visa-modelador
├── flows.md                  ← visa-modelador
├── architecture.md           ← visa-modelador
├── gaps.md                   ← visa-coletor
├── evidence_plans/           ← visa-coletor
├── evidence_scripts/         ← visa-coletor
├── evidence_results/         ← preenchido pelo usuário após coleta
├── business_model.md         ← visa-redator (FORMATO CANÔNICO ⭐)
├── discard_log.md            ← visa-redator (FORMATO CANÔNICO)
├── ambiguity_log.md          ← visa-redator (FORMATO CANÔNICO)
├── confidence-report.md      ← visa-revisor (FORMATO CANÔNICO)
├── sdd/<componente>.md       ← visa-redator
├── handoff.md                ← visa-handoff
└── migration/                ← visa bridge (symlinks para artefatos canônicos)
    ├── target_business_rules.md  → ../business_model.md
    ├── ambiguity_log.md           → ../ambiguity_log.md
    ├── discard_log.md             → ../discard_log.md
    └── paradigm_decision.md       → ../confidence-report.md
```

⭐ Os 4 artefatos canônicos seguem o template Reversa
(`schemaVersion: 1` + IDs `BR-FUTURE-NNN`/`BR-DESCARTAR-NNN`/`BR-HUMANA-NNN`/`AMB-FUTURE-NNN`)
e são consumidos diretamente pelo extractor do paridade-guard ≥ 0.3.0.

---

## Testes

```bash
# Suite Visa (com paridade-guard ≥ 0.3.0 instalado)
python3 tests/test_visa.py
# PASSED: 40    FAILED: 0    SKIPPED: 0
# (em CI: exit 0)

# Suite Visa (SEM paridade-guard instalado)
# PASSED: 39    FAILED: 0    SKIPPED: 1  (TestEndToEndComParidadeGuard)
# (em CI: exit 2 — distingue de "tudo passou")

# Suite paridade-guard
cd /caminho/para/paridade-guard && python3 -m pytest tests/
# 69 passed
```

Cobertura:

- **TestSkills** (6): front-matter, espelhamento conceitual, escala 🟢🟡🔴
- **TestInstall** (5): 4 engines, manifest SHA-256, idempotência
- **TestStatusValidate** (6): detecção de artefatos faltantes/completos, modo `--strict`
- **TestBridge** (5): validação canônica, symlinks, abort em pipeline incompleto
- **TestCollectorGate** (9) ⭐ **v1.2**: gate computacional do Coletor — bloqueio em LACUNAS pendentes, aceitação via `[RESOLVIDO]`/`[RISCO ACEITO]` no heading, aceitação via `accepted_risks:` no front-matter, override `--accept-all-risks` com motivo, `--skip-collector-gate`, ausência de gaps.md, 🔴 inline sem ID estruturado
- **TestUninstall** (4): remove skills, preserva `_visa_sdd/`, suporta `--purge`, idempotente
- **TestReferences** (4): garante que arquivos referenciados pelo orquestrador existem
- **TestEndToEndComParidadeGuard** ⭐ (1): cadeia completa Visa→bridge→paridade-guard, valida cláusulas reais com IDs e severities corretos. Levanta `SkipTest` visível com exit code 2 em ambiente sem paridade-guard.

Total: **40 testes Visa + 69 paridade-guard = 109 testes**.

CI configurada em `.github/workflows/tests.yml` rodando em Python 3.10, 3.11, 3.12.

---

## Compatibilidade

| Engine de codificação | Suporte |
|---|---|
| Claude Code | ✅ via `.claude/skills/` |
| Codex | ✅ via `.agents/skills/` |
| Cursor | ✅ via `.agents/skills/` |
| Gemini CLI | ✅ via `.agents/skills/` |
| Outras (Windsurf, Cline, Roo, Kiro, Amazon Q) | ⚠️ não testadas, mas seguem mesmo padrão de Agent Skills |

| Ferramenta | Versão mínima |
|---|---|
| Python | 3.10 (stdlib pura, zero dependências) |
| paridade-guard | 0.3.0 (extractor forward) |
| Reversa | qualquer versão com `schemaVersion: 1` |

---

## Limitações conhecidas

Lista declarativa e honesta. Não pretende esconder nada que apareça em
auditoria adversarial.

1. **Detecção de LACUNAS por regex.** O gate do Coletor v1.2 usa regex
   contra `### LACUNA-NNN` no markdown. Se o `visa-coletor` produzir
   formato diferente (ex: HTML, table-only), o gate não detecta. v1.3
   pode mudar para parsing estruturado.

2. **14 agentes vs 18 do Reversa.** A Visa cobre o ciclo de descoberta
   forward, **não pretende espelhamento 1:1**. Cobertura sobre o conjunto
   aplicável: 14/16 = 87.5%. Os 2 não espelhados (`reversa-visor`,
   `reversa-reconstructor`) são decisões conscientes documentadas em
   [Diferenças do Reversa](#diferenças-do-reversa-honestidade-documental).

3. **Skills sem schema validation do output.** O LLM pode emitir Markdown
   que falhe no `validate --strict` posteriormente. Mitigação parcial:
   `visa-redator` v1.1+ tem template literal no SKILL.md.

4. **Bridge requer paridade-guard ≥ 0.3.0.** Versões anteriores tratam
   `BR-FUTURE-NNN` como prefixo desconhecido. Bridge alerta sobre isso.

5. **Sem ainda testado em produção real.** A Visa foi testada
   estruturalmente (40 testes automatizados) mas não em sessão real de
   Claude Code contra um domínio complexo. A qualidade do output em campo
   depende fortemente do modelo de LLM.

6. **Não testada em Windows.** Symlinks no `bridge` têm fallback para cópia,
   mas validação manual em Windows pendente.

---

## Roadmap

### v1.3 (planejada)

- **Parsing estruturado de gaps.md** (em vez de regex contra heading).
  Mais robusto a variações de formato.
- **Skills testadas em pelo menos 2 domínios reais** (saúde + outro).
- **Templates `.md` separados**: extrair templates inline do
  `visa-redator/SKILL.md` para `templates/canonical/` (espelha Reversa).
- **Caso de uso real documentado** como case study.

### v1.4+ (especulativa)

- Espelhar mais agentes do Reversa que façam sentido para descoberta
  (designer, paradigm-advisor adaptado).
- Suporte a `npx visa install` (versão Node.js compatível) para
  alinhamento de UX com Reversa.

---

## Links

- **paridade-guard** (gate de paridade): https://github.com/Adgmed2018/paridade-guard
- **Reversa** (espelho à trás): https://github.com/sandeco/reversa
- **Issues / contribuições**: https://github.com/Adgmed2018/visa/issues
- **Como contribuir**: ver [CONTRIBUTING.md](CONTRIBUTING.md)
- **Changelog completo**: ver [CHANGELOG.md](CHANGELOG.md)
- **Auto-avaliação técnica detalhada**: ver [AUTO-AVALIACAO.md](AUTO-AVALIACAO.md)

---

## Licença

[MIT](LICENSE).

## Agradecimentos

A tese (descoberta forward + verificação meio + extração backward = ciclo
SDD fechado em PT) foi formada em diálogo com o trabalho do
[@sandeco](https://github.com/sandeco) no Reversa. A Visa é uma extensão
**voluntária e Reversa-compatível**, sem afiliação oficial.
