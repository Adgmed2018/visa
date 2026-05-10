# Visa

<small>por [Adgmed2018](https://github.com/Adgmed2018) · complemento *forward* do [Reversa](https://github.com/sandeco/reversa) de [@sandeco](https://github.com/sandeco)</small>

**Transforma domínios de negócio em especificações executáveis para agentes de IA — antes de qualquer código existir.**

[English Docs](../README.md) · **Português Docs** · [Español Docs](../es/README.md)

---

A Visa é um framework de **descoberta forward de especificação**. Instale dentro de um projeto vazio (ou qualquer projeto começando de um domínio de negócio novo) e ela coordena uma equipe de agentes de IA especializados para transformar conversas vagas, hipóteses de mercado e entrevistas com stakeholders em especificações completas, rastreáveis e executáveis — prontas para uso por qualquer agente de codificação.

## Por que a Visa existe

A maioria dos projetos de software começa com uma reunião, um slide ou uma página no Notion. O handoff para engenharia é informal, a especificação implícita, as premissas enterradas em threads de chat. Agentes de IA para código amplificam o custo: eles executam rápido, mas executam *qualquer coisa que você diga* — incluindo a premissa pela metade que nunca foi validada.

Para **sistemas legados**, o [Reversa](https://github.com/sandeco/reversa) extrai a spec que já existe no código. Para **sistemas novos** ainda não há código — apenas hipóteses. Sem uma descoberta estruturada, o agente gera código para um produto que talvez não devesse existir, numa arquitetura que talvez não caiba, com regras que ninguém verificou.

**A Visa é a ponte entre o domínio de negócio e os agentes de IA.**

Ela coordena um pipeline de agentes — etnógrafo, estrategista, paradigm advisor, modelador de dados, design system, redator, inspector, revisor, handoff — para transformar conversas, evidências e restrições em:

- Especificações com IDs canônicos versionados (`BR-FUTURE-NNN`, `AMB-FUTURE-NNN`)
- Modelos de domínio, ERDs, design tokens, decisões de paradigma
- Critérios de aceitação em Gherkin, prontos para validação pelo `paridade-guard`
- Um `CLAUDE.md` consolidado (ou `ANTIGRAVITY.md`, `AGENTS.md`, etc.) para o agente de código honrar

O resultado não é documentação para humanos lerem. **São contratos operacionais que permitem ao agente construir o sistema com fidelidade ao que foi descoberto.**

Juntos, **Visa (forward) + Reversa (backward) + paridade-guard (gatekeeper)** formam o único stack SDD de ciclo fechado open-source disponível.

## Instalação

Na raiz do projeto (ou em uma pasta vazia para um produto novo):

```bash
pip install visa-sdd
```

Em seguida, na pasta do projeto:

```bash
visa install
```

O instalador irá:

- Detectar a engine de IA presente no ambiente (Claude Code, Antigravity, Cursor, Codex, Gemini CLI, Windsurf)
- Copiar 14 agentes (skills) para `.claude/skills/` (Claude Code) ou `.agents/skills/` (outras)
- Criar o arquivo entry da engine (`CLAUDE.md`, `ANTIGRAVITY.md`, etc.) se ausente
- Criar a estrutura `.visa/` com state, plano e configuração

A Visa nunca apaga ou modifica arquivos existentes no seu projeto. Os agentes escrevem apenas em `.visa/` e na pasta de output (`_visa_sdd/` por padrão).

**Requisitos:** Python 3.10+

> [!IMPORTANT]
> 🔒 **Imutabilidade garantida do seu projeto**
> O instalador apenas cria arquivos novos (`CLAUDE.md`, `.claude/skills/`, `.visa/`, etc.) e nunca modifica ou apaga nenhum arquivo existente. Durante a descoberta, os agentes operam sob diretiva estrita: todas as escritas são restritas a `.visa/` e `_visa_sdd/` — nenhum outro arquivo é tocado.

> [!CAUTION]
> 💾 **Versione seu projeto antes de começar**
> Apesar de a Visa nunca modificar seus arquivos, agentes de IA podem errar. Recomendamos:
>
> - Inicie Git e faça commit antes da descoberta
> - Tenha o repositório no GitHub (ou GitLab, Bitbucket) para backup remoto
> - Faça uma cópia local da pasta — `cp -r meu-projeto meu-projeto-backup`
>
> Se algo inesperado acontecer, restaure com `git restore .` ou da cópia.

> [!WARNING]
> 🔑 A Visa não solicita, armazena nem transmite chaves de API de nenhum serviço de LLM. Toda inteligência é delegada ao agente de IA já presente no seu ambiente — sem dependências de autenticação externa.

## Como usar

Após a instalação, abra o projeto no agente de IA e ative a Visa:

```
/visa
```

Para engines sem suporte a slash command (como Codex):

```
visa
```

A Visa se apresenta, cria um plano de descoberta personalizado a partir do domínio que você descrever e coordena o pipeline inteiro. O progresso é salvo em `.visa/state.json` em cada checkpoint — se a sessão for interrompida, basta digitar `/visa` para retomar de onde parou.

## Como funciona

A Visa usa um pipeline de 4 fases orquestrado pelo agente Visa:

```
Pré-Descoberta → Síntese → Especificação → Handoff
   Etnógrafo     Paradigma   Redator        Revisor
   Estrategista  Modelador   Strategist     Handoff
   Coletor       Dados       Inspector
                 Design
```

Após o Handoff, os artefatos canônicos (`BR-FUTURE-NNN`) são consumidos pelo `paridade-guard` para gatear a implementação: código mergeado em `main` precisa rastrear até uma regra de negócio aprovada.

## Agentes

### Obrigatórios

| Agente | Papel |
|---|---|
| `visa` | Orquestrador central. Coordena, salva checkpoints, guia o usuário |
| `visa-etnografo` | Mapeia a superfície: personas, jornadas, concorrentes, vocabulário |
| `visa-estrategista` | Análise jornada-por-jornada: dores, ganhos, fricções, oportunidades |
| `visa-coletor` | Resolve 🔴 LACUNAS gerando planos de coleta de evidência |
| `visa-paradigm-advisor` | Decide paradigma alvo (Clean / OO+DI / FP / event-driven / actor) |
| `visa-modelador` | Sintetiza modelo de domínio, fluxos, modelo de negócio, integrações |
| `visa-data-modeler` | Propõe esquema de dados prospectivo (ERD, DDL, FKs, CHECK) |
| `visa-design-system` | Propõe design tokens prospectivos (paleta, tipografia, spacing) |
| `visa-redator` | Gera specs SDD por componente, OpenAPI, regras com IDs canônicos |
| `visa-strategist` | Propõe estratégias de go-to-market e roteiro de MVP com trade-offs |
| `visa-inspector` | Define critérios de aceitação em Gherkin para cada `BR-FUTURE-NNN` |
| `visa-revisor` | Revisão cruzada das specs, detecta contradições, prepara handoff |
| `visa-handoff` | Produz `handoff.md` final pronto para Spec Kit, Reconstructor ou agente |

### Opcionais (instalados por padrão)

| Agente | Papel |
|---|---|
| `visa-agents-help` | Explica com analogias o que cada agente faz e quando usar |
| `visa-claude-md-builder` | Gera `CLAUDE.md` consolidado a partir dos artefatos `_visa_sdd/` |

### Vertical packs (indústrias reguladas)

Use quando o projeto mira vertical regulado específico. Pré-carrega regras `BR-FUTURE` e força o Coletor a marcar ausência de evidência regulatória como 🔴 LACUNA bloqueante.

| Agente | Vertical |
|---|---|
| `visa-vertical-fintech-pix` | Fintech BR: PIX (BACEN), DICT, MED, KYC/PLD, LGPD, BACEN 4.658 |
| `visa-vertical-healthtech-anvisa` | Healthtech: SaMD (RDC 657), CFM 2.314, CFM 1.821, ISO 13485 |
| `visa-vertical-legaltech-tributario` | Legaltech: e-CAC, PJe, ESAJ, SPED, OAB Provisão 49/2017 |

## O que é gerado

```
_visa_sdd/
├── landscape.json              # Mapa do domínio (Etnógrafo)
├── opportunities.md            # Dores e ganhos por jornada (Estrategista)
├── gaps.md                     # 🔴 LACUNAS bloqueando avanço (Coletor)
├── evidence_results/           # Evidências resolvidas por LACUNA
├── paradigm_decision.md        # Paradigma alvo justificado (Paradigm Advisor)
├── domain_model.md             # Entidades, fluxos, modelo de negócio (Modelador)
├── data_model.md               # ERD em Mermaid + DDL + integridade (Data Modeler)
├── design-system/              # Tokens (Design System)
├── business_model.md           # Regras BR-FUTURE-NNN canônicas (Redator)
├── discard_log.md              # O que ficou de fora do MVP (Redator)
├── ambiguity_log.md            # AMB-FUTURE-NNN ambiguidades abertas (Redator)
├── gtm_strategy.md             # Estratégia GTM (Strategist)
├── risk_register.md            # Registro de riscos (Strategist)
├── mvp_roadmap.md              # Roteiro de sprints (Strategist)
├── acceptance/                 # Gherkin .feature por BR-FUTURE-NNN (Inspector)
├── coverage_matrix.md          # BR-FUTURE → mapa de testes de aceitação
├── compliance/                 # Checklists regulatórios (se vertical)
├── review_report.md            # Achados da revisão cruzada (Revisor)
└── handoff.md                  # Handoff final
```

## Escala de confiança

Toda afirmação nas specs é marcada com:

| Marca | Significado |
|---|---|
| 🟢 **CONFIRMADO** | Validado com evidência real (entrevista, dado de mercado, MVP, contrato) |
| 🟡 **INFERIDO** | Hipótese plausível baseada em padrões conhecidos, sem evidência direta |
| 🔴 **LACUNA** | Hipótese pura sem evidência. **Bloqueia avanço até virar entrevista, teste ou pesquisa.** |

Diferente do Reversa (onde 🔴 significa "não determinável do código"), na Visa 🔴 significa "não validado contra o mercado". O usuário não resolve uma 🔴 LACUNA pensando — resolve **coletando evidência**. O agente Coletor existe exatamente para essa função.

## Engines suportadas

| Engine | Entry file | Skills path | Ativação |
|---|---|---|---|
| Claude Code ⭐ | `CLAUDE.md` | `.claude/skills/visa-*/` e `.agents/skills/visa-*/` | `/visa` |
| Google Antigravity ⭐ | `ANTIGRAVITY.md` | `.agents/skills/visa-*/` | `/visa` |
| Codex ⭐ | `AGENTS.md` | `.agents/skills/visa-*/` | `visa` |
| Cursor ⭐ | `.cursorrules` | `.agents/skills/visa-*/` | `/visa` |
| Gemini CLI | `GEMINI.md` | `.agents/skills/visa-*/` | `/visa` |
| Windsurf | `.windsurfrules` | `.agents/skills/visa-*/` | `/visa` |

## Comandos CLI

```bash
visa install      # Instala skills da Visa no projeto
visa status       # Mostra estado atual da descoberta
visa validate     # Verifica artefatos esperados em _visa_sdd/
visa bridge       # Gera stub para paridade-guard ≥ 0.3.0
visa doctor       # Diagnóstico: engine, skills, state, paridade-guard (NOVO v1.5.0)
visa upgrade      # Atualiza skills sem reinstalar do zero (NOVO v1.5.0)
visa serve        # Web UI mínima para visualizar _visa_sdd/ (NOVO v1.6.0)
visa telemetry    # Telemetria opt-in privacidade-first (NOVO v1.6.0)
visa uninstall    # Remove a Visa do projeto (preserva _visa_sdd/)
```

O `upgrade` compara SHA-256 de cada `SKILL.md` e atualiza só o que mudou, preservando `_visa_sdd/` e `.visa/state.json`.
O `bridge` aceita `--accept-all-risks "motivo"` para liberar o gate do Coletor com auditoria.

## Estrutura interna

```
.visa/
├── state.json                  # Estado entre sessões
├── plan.md                     # Plano de descoberta (editável)
├── telemetry-optin.json        # Registro de opt-in (se ativada)
├── telemetry.jsonl             # Log local de eventos (se ativada)
└── context/
    ├── landscape.json          # Gerado pelo Etnógrafo
    └── interviews.json         # Gerado pelo Coletor

.claude/skills/                 # Mirror para Claude Code
.agents/skills/                 # Skills universais
```

## Ciclo fechado SDD com Reversa e paridade-guard

```
ideia de negócio → Visa (forward spec) → BR-FUTURE-NNN → paridade-guard → código verificado
                                                                  ↑
                                                Reversa (de legado existente)
```

Para estender um sistema existente, rode **Reversa primeiro** para extrair o que já está lá, depois **Visa** para descobrir os novos requisitos, e por fim **paridade-guard** para validar que a implementação honra ambos. Detalhes em [docs/closed-loop.md](../closed-loop.md).

## Contribuindo

Contribuições são bem-vindas. Abra uma issue para discutir antes de submeter um PR.

```bash
git clone https://github.com/Adgmed2018/visa.git
cd visa
pip install -e ".[dev]"
pytest
```

## Licença

MIT — veja [LICENSE](../../LICENSE).
