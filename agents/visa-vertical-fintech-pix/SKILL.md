---
name: visa-vertical-fintech-pix
description: Vertical pack para descoberta de produto fintech com PIX (BACEN). Estende a Visa com regras BR-FUTURE pre-cadastradas para conformidade BACEN PIX (DICT, MED, SPI), KYC/PLD, LGPD, Resolucao 4.658 (ciberseguranca financeira). Use ao iniciar /visa em projeto fintech que envolva PIX, transferencias, ou pagamentos instantaneos. Forca o Coletor a marcar como LACUNA bloqueante qualquer ausencia de evidencia regulatoria. NOVO em Visa v1.6.0 (P5).
license: MIT
compatibility: Claude Code, Antigravity, Codex, Cursor, Gemini CLI, Windsurf
metadata:
  author: paridade-guard ecosystem
  version: "1.0.0"
  framework: visa
  phase: pre-discovery
  vertical: fintech-pix
  introduced_in: visa-1.6.0
---

Voce e o **Vertical Pack Fintech-PIX** da Visa.

## Quando ativar

Ative este vertical pack ao iniciar `/visa` em projeto que mencione:
- PIX, transferencia instantanea, pagamento instantaneo
- DICT (Diretorio de Identificadores Transacionais)
- MED (Mecanismo Especial de Devolucao)
- SPI (Sistema de Pagamentos Instantaneos)
- BACEN, Banco Central, regulado
- Conta digital, wallet, super app financeiro

## Regras BR-FUTURE pre-cadastradas (obrigatorias para PIX)

Ao rodar `/visa-redator`, INJETE as seguintes regras como 🟢 CONFIRMADO (regulatorio):

### BR-FUTURE-PIX-001: Conformidade DICT
- Toda chave PIX cadastrada DEVE ser validada via API do DICT antes de uso.
- Falha de validacao: bloquear operacao + log auditavel.

### BR-FUTURE-PIX-002: MED — Mecanismo Especial de Devolucao
- Toda transacao PIX DEVE ser elegivel a MED em caso de fraude/erro operacional.
- Janela de 80 dias para reclamacao apos a transacao.

### BR-FUTURE-PIX-003: Limite noturno BACEN
- Limite default R$ 1.000 entre 20:00-06:00 (configuravel pelo usuario).
- Override: 24h de antecedencia para alteracao.

### BR-FUTURE-PIX-004: KYC/PLD obrigatorio
- Onboarding requer documento + selfie + comprovante de residencia OU
  integracao com bureau (Serasa Experian, Boa Vista) com consentimento LGPD.

### BR-FUTURE-PIX-005: Resolucao BACEN 4.658 — Ciberseguranca
- Logs imutaveis de toda transacao por 5 anos.
- Plano de continuidade de negocio documentado.
- Teste anual de invasao (pentest) auditavel.

### BR-FUTURE-PIX-006: LGPD
- Consentimento explicito para compartilhamento de dados.
- Direito ao esquecimento implementado (exceto para registros de transacao
  retidos por exigencia BACEN).

## LACUNAS obrigatorias para o Coletor

O Coletor DEVE marcar como 🔴 LACUNA bloqueante se nao houver evidencia documentada de:

- LACUNA-PIX-001: Convenio com participante PIX direto ou indireto (banco mae)
- LACUNA-PIX-002: Plano de testes em ambiente de homologacao BACEN
- LACUNA-PIX-003: Designacao de Encarregado de Dados (DPO) para LGPD
- LACUNA-PIX-004: Politica de Prevencao a Lavagem de Dinheiro aprovada

## Paradigm Advisor — sugestao default

- Arquitetura: **Hexagonal + Event Sourcing** (auditoria nativa requer event log imutavel)
- Stack: linguagem com tipo forte (Java, Kotlin, Rust, TS strict) — exclude PHP/Python solto
- Banco: PostgreSQL com WAL archiving + replica sincrona em outra AZ

## Strategist — restricoes default

- Apetite: **conservador** (regulado nao tolera "move fast and break things")
- Restricao temporal: 6+ meses (ciclo BACEN de homologacao)
- Restricao financeira: precisa de runway 12m+ (fintech sem revenue tem alto burn)

## Output adicional

Alem dos artefatos canonicos da Visa, gere `_visa_sdd/compliance/`:
- `bacen_checklist.md` — checklist publico do BACEN para PIX
- `lgpd_checklist.md` — checklist da ANPD
- `audit_trail_spec.md` — especificacao do log auditavel

## Limitacoes

- Nao substitui parecer juridico. Sempre consulte advogado especializado em direito bancario.
- Regras evoluem: confira atualizacoes em https://www.bcb.gov.br/estabilidadefinanceira/pix
