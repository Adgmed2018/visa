# Visa & paridade-guard
<small>by Adgmed2018</small>

**Forward Spec Discovery for AI Agents. Transforme conversas vagas em especificações executáveis e verificáveis.**

[![Visa](https://img.shields.io/badge/Visa-v1.1.1-blue?style=for-the-badge&labelColor=2d2d2d)](#)
[![paridade-guard](https://img.shields.io/badge/paridade--guard-v0.3.0-purple?style=for-the-badge&labelColor=2d2d2d)](#)
[![Tests](https://img.shields.io/badge/tests-40%2F40%20passing-success?style=for-the-badge&labelColor=2d2d2d)](#)
[![Python](https://img.shields.io/badge/python-3.10%2B-blue?style=for-the-badge&labelColor=2d2d2d)](#)
[![License](https://img.shields.io/badge/license-MIT-yellow?style=for-the-badge&labelColor=2d2d2d)](#license)

---

## Motivo do Projeto

O ecossistema de desenvolvimento assistido por IA (AI-assisted coding) vive hoje uma profunda ilusão de produtividade. Pipelines de prompts são inconsistentes. Agentes "mágicos" prometem criar aplicações inteiras a partir de um parágrafo, mas na prática entregam arquiteturas frágeis, arquivos fantasmas (que o LLM jura ter criado, mas não existem) e absoluta falta de auditoria real.

A Visa nasceu da **frustração técnica com essa ausência de rigor**. É incrivelmente difícil transformar conversas informais com o Claude, GPT ou Codex em artefatos confiáveis, versionáveis e que sigam um padrão lógico. O mercado focou em "escrever código mais rápido" em vez de "garantir que estamos construindo o sistema correto".

Precisávamos de um **sistema de engenharia verificável para agentes de IA** — um protocolo que eleve a extração de requisitos ao mesmo nível de exigência de um pipeline de CI/CD.

---

## Dores que o Visa resolve

A dupla Visa + paridade-guard ataca os principais modos de falha em pipelines de LLM:

- **Alucinações estruturais**: Arquivos que o LLM diz que criou (ou alterou), mas que de fato não existem ou estão incorretos no repositório.
- **Divergência entre spec e código**: O descompasso entre o que foi descrito e o que realmente é entregue na fase de implementação.
- **Falta de rastreabilidade e auditoria adversarial**: Impossibilidade de justificar o porquê de uma decisão técnica três semanas após o chat original.
- **Inconsistência em projetos grandes**: A dificuldade de manter o contexto vivo ao orquestrar múltiplos agentes ao longo do ciclo de vida.
- **Ausência de formato canônico**: A falta de um contrato confiável e determinístico para trânsito entre a geração de requisitos e a validação do código.
- **Cobertura falsa de testes e comandos fantasmas**: Quando a IA alega que os testes estão passando sem nunca ter executado um runner real.
- **Dificuldade de evolução**: A barreira massiva para migrar de prompts "mágicos" descartáveis para processos de engenharia de software de verdade com LLMs.

---

## O que é o Visa

A Visa é o motor de descoberta (*Forward Spec Discovery*) de um ciclo completo de **Spec-Driven Development (SDD)**.

Enquanto ferramentas analisam o passado (código legado) para extrair o presente, a Visa ataca o futuro: ela orquestra um time de agentes para descobrir, validar e modelar um domínio de negócio *antes* de qualquer código ser escrito. 

Ela trabalha em simbiose com o **paridade-guard**, que age como o portão de segurança (Gatekeeper). O `paridade-guard` converte os artefatos da Visa em um contrato e bloqueia commits caso o agente de codificação (Claude Code, Cursor) tente desviar do que foi especificado.

---

## Instalação

A instalação da Visa e do paridade-guard é feita diretamente via Python (stdlib pura).

```bash
# 1. Instalar a Visa
pip install visa-sdd

# 2. Instalar o gate de aderência
pip install paridade-guard>=0.3.0
```

Para inicializar a descoberta em um novo projeto:

```bash
cd meu-novo-projeto
touch CLAUDE.md # Ou .cursorrules
visa install
```

---

## Demo em 5 minutos

Você pode testar o ciclo computacional sem nem mesmo gastar tokens de LLM. Execute:

```bash
# 1. Setup inicial
mkdir demo-sdd && cd demo-sdd && touch CLAUDE.md
visa install

# 2. Simular a saída canônica do agente Redator (como se houvesse ocorrido a descoberta)
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
- **Justificativa**: Evidência coletada com 5 especialistas confirmou requerimento
EOF

# 3. Validar estruturalmente o formato canônico
visa validate --strict
# → ✅ Validação estrutural aprovada.

# 4. Construir ponte para o gate de implementação
visa bridge
# → 🌉 Symlinks gerados de _visa_sdd/ para o diretório de auditoria

# 5. paridade-guard gera o contrato (Gatekeeper)
paridade-guard contract \
  --migration-dir _visa_sdd/migration \
  --output _visa_sdd/parity_audit/contract.json

# 6. Ativar gate no repositório local
paridade-guard install --pre-commit
# → A partir de agora, qualquer commit que quebre BR-FUTURE-001 será abortado.
```

---

## Como funciona (O Pipeline Completo)

A integração forma um pipeline contínuo de 5 fases operadas nativamente no terminal:

1. **Descoberta:** Orquestrada via CLI com a Visa. O LLM extrai contexto, personas e necessidades.
2. **Coleta de Evidências (O Gate):** O agente *Coletor* detecta lacunas (ausência de dados) e **trava o pipeline** até que o humano traga evidências reais. Fim da adivinhação algorítmica.
3. **Spec Generation:** O agente *Redator* consolida tudo no formato canônico (`_visa_sdd/`).
4. **Bridge:** O comando `visa bridge` consolida e audita os diretórios, fechando as pontas para a próxima fase.
5. **Implementação Vigiada:** O código passa a ser escrito. O `paridade-guard` atua no `pre-commit hook` impedindo a violação das especificações levantadas.

---

## Agentes incluídos

A Visa orquestra os seguintes **8 agentes** especialistas para dissecar o domínio:

1. **visa** (Orquestrador) — Controla o avanço e policia a escala de evidências (🟢🟡🔴).
2. **visa-etnografo** — Mapeia o domínio de alto nível, personas e constrói o glossário.
3. **visa-estrategista** — Cruza perfis com jornadas para isolar dores críticas.
4. **visa-coletor** — O auditor. Interrompe hipóteses vazias emitindo roteiros de validação reais.
5. **visa-modelador** — Constrói a proposta de fluxos, arquitetura de software e design estrutural.
6. **visa-redator** — Emite as especificações imutáveis com IDs únicos (`BR-FUTURE-NNN`).
7. **visa-revisor** — Executa uma auditoria cruzada antes da consolidação do pacote.
8. **visa-handoff** — Transforma a documentação descoberta no formato de passagem de bastão (`handoff.md`).

---

## Comandos CLI

A CLI possui comandos pragmáticos e rígidos para o ciclo de SDD:

| Comando | Função |
|---------|--------|
| `visa install` | Instala skills no projeto e cria o estado isolado em `.visa/`. |
| `visa status` | Exibe o andamento macro da descoberta. |
| `visa validate` | Valida a presença dos artefatos obrigatórios. |
| `visa validate --strict` | Executa linting pesado nos formatos canônicos (front-matters, IDs). |
| `visa bridge` | **Comando vital.** Executa o gate do Coletor e conecta o output ao verificador de paridade. |
| `visa uninstall --purge` | Remove completamente os arquivos injetados do repositório. |

---

## Formato Canônico gerado

O output não é uma parede de texto informal. É um sistema de arquivos *machine-readable*:

```text
_visa_sdd/
├── landscape.md             # Visão etnográfica
├── gaps.md                  # Gestão de LACUNAS (onde o Coletor atua)
├── evidence_plans/          # Planos forçados de coleta de dados empíricos
├── business_model.md        # [CANÔNICO] Target Business Rules com schemaVersion: 1
├── ambiguity_log.md         # [CANÔNICO] Diário de decisões sobre incertezas
├── discard_log.md           # [CANÔNICO] Decisões explícitas de não-implementação
├── sdd/                     # Documentação aprofundada por componente
└── migration/               # [BRIDGE] Symlinks lidos pelo paridade-guard
```

---

## Limitações conhecidas

Somos devotos de uma engenharia de software pragmática e honesta. Conheça as limitações arquiteturais:

- **Regex para bloqueio de Lacunas**: O gate do Coletor (`visa bridge`) audita `gaps.md` usando Expressões Regulares contra cabeçalhos Markdown. Modificações pesadas no formato gerado quebram a trava temporariamente.
- **Falha silenciosa sem LLMs disciplinados**: A Visa não roda os modelos; ela injeta skills locais. Modelos de baixa capacidade intelectual podem produzir saídas Markdown inválidas, que falharão posteriormente no `visa validate --strict`.
- **Análise Semântica Passiva**: O `paridade-guard` não roda o código. Ele atua via inspeção estática no `git diff`. Não isenta a responsabilidade de executar testes unitários (TDD).

---

## Contributing

Pull Requests (PRs) para melhorias estruturais são sempre bem-vindos, contanto que mantenham a essência do "Ciclo SDD Fechado".
Ao enviar um PR:
1. Certifique-se de não adicionar bibliotecas de terceiros (somos 100% *stdlib*).
2. Garanta que a suíte de testes original (`test_visa.py`) passe perfeitamente.
3. Não suavize o gate computacional do Coletor. A exigência de evidências é sagrada.

Abra uma [Issue](#) para debater mudanças de arquitetura.

---

## License

MIT — veja [LICENSE](LICENSE) para os detalhes. O conhecimento pertence ao ecossistema.
