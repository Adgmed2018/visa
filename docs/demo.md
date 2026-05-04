# Visa Demo — Interactive Walkthrough

Este guia oferece um demo interativo completo da Visa em 5 minutos.

## Demo 1: Ciclo Completo (Sem LLM)

Execute este demo sem gastar tokens de LLM. Simula o output canônico de um pipeline completo.

```bash
# 1. Setup
mkdir demo-visa && cd demo-visa
touch CLAUDE.md
visa install

# 2. Criar artefatos simulados (como se pipeline tivesse rodado)
mkdir -p _visa_sdd

# 3. Artefato canônico válido (como output do Redator v1.1+)
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
- **Justificativa**: 5/5 especialistas entrevistados confirmam requerimento

### BR-FUTURE-002
- **Origem**: Inferência do Modelador
- **Confiança**: 🟡
- **Descrição**: Lembrete automático 24h antes da consulta
- **Justificativa**: Padrão de mercado SaaS de saúde

### BR-FUTURE-003
- **Origem**: `_visa_sdd/evidence_results/lac-002.md`
- **Confiança**: 🟢
- **Descrição**: Cancelamento com reembolso parcial até 48h antes
- **Justificativa**: Requerimento legal confirmado
EOF

# 4. Ambiguity log
cat > _visa_sdd/ambiguity_log.md <<'EOF'
---
schemaVersion: 1
kind: ambiguity_log
producedBy: visa-redator
---

# Ambiguity Log

### AMB-FUTURE-001
- **Descrição**: Persona "secretária" não foi entrevistada
- **Detectado por**: visa-coletor
- **Origem**: `_visa_sdd/gaps.md`
- **Status**: PENDENTE
EOF

# 5. Confidence report
cat > _visa_sdd/confidence-report.md <<'EOF'
---
schemaVersion: 1
kind: paradigm_decision
producedBy: visa-revisor
---

# Confidence Report

## Decisão

**Paradigma**: Clean Architecture com Use Cases

## Justificativa
- Separação clara de concerns
- Testabilidade alta
- Domínio explícito

## Confiança Geral
🟢 Alta — Validado com equipe de arquitetura
EOF

# 6. Validate
visa validate --strict
# → ✅ 4/4 canônicos válidos

# 7. Bridge
visa bridge
# → 🌉 Symlinks gerados

# 8. Instalar paridade-guard (se não tiver)
pip install paridade-guard>=0.3.0 || echo "paridade-guard não instalado"

# 9. Gerar contrato
paridade-guard contract \
  --migration-dir _visa_sdd/migration \
  --output _visa_sdd/parity_audit/contract.json

# 10. Verificar contrato
cat _visa_sdd/parity_audit/contract.json | python3 -m json.tool

# 11. Instalar pre-commit hook
paridade-guard install --pre-commit

# 12. Cleanup
visa uninstall --yes --purge
```

---

## Demo 2: Gate do Coletor

Demonstra o gate computacional bloqueando pipeline com LACUNAs pendentes.

```bash
# Setup
mkdir demo-gate && cd demo-gate
touch CLAUDE.md
visa install

# Criar artefato válido
cat > _visa_sdd/business_model.md <<'EOF'
---
schemaVersion: 1
kind: target_business_rules
producedBy: visa-redator
---

# Target Business Rules

### BR-FUTURE-001
- **Confiança**: 🟢
- **Descrição**: Regra de teste
EOF

# Criar gaps.md COM lacuna pendente
cat > _visa_sdd/gaps.md <<'EOF'
# Gaps

### LACUNA-001
- 🔴 LACUNA não resolvida
- **Impacto**: Alto
- **Evidência necessária**: Entrevistas com stakeholders
EOF

# Tentar bridge (deve bloquear)
visa bridge
# → 🛑 BRIDGE BLOQUEADA pelo gate do Coletor
# → exit code: 4

# Resolver lacuna
cat > _visa_sdd/gaps.md <<'EOF'
---
resolved:
  - LACUNA-001
---

# Gaps

### LACUNA-001 [RESOLVIDO]
- **Evidência**: 5/5 entrevistados confirmam requerimento
EOF

# Tentar bridge novamente (deve passar)
visa bridge
# → ✅ Bridge completo

# Cleanup
visa uninstall --yes --purge
```

---

## Demo 3: Override com Motivo

Demonstra override consciente do gate.

```bash
mkdir demo-override && cd demo-override
touch CLAUDE.md
visa install

cat > _visa_sdd/business_model.md <<'EOF'
---
schemaVersion: 1
kind: target_business_rules
producedBy: visa-redator
---

# Target Business Rules

### BR-FUTURE-001
- **Confiança**: 🟡
- **Descrição**: Regra provisória
EOF

cat > _visa_sdd/gaps.md <<'EOF'
# Gaps

### LACUNA-001
- 🔴 LACUNA não resolvida
EOF

# Override com motivo (transparente)
visa bridge --accept-all-risks="spike de 1 dia após MVP"
# → ⚠️  --accept-all-risks ativado
# →   Motivo: spike de 1 dia após MVP
# →   1 LACUNA(s) pendente(s) ignorada(s):
# →     - LACUNA-001
# → ✅ Bridge completo

visa uninstall --yes --purge
```

---

## Demo 4: Pipeline Completo (Com LLM)

Este demo usa o pipeline real com LLM. Requer tokens.

```bash
# Setup
mkdir demo-llm && cd demo-llm
touch CLAUDE.md  # Ou .cursorrules para Cursor

# Instalar Visa
visa install

# No Claude Code, Cursor, etc., digite:
/visa

# Siga a orchestration através dos agentes:
# 1. Ethnographer → landscape.md, personas
# 2. Strategist → pains.md, opportunities
# 3. Collector → gaps.md (com evidências coletadas)
# 4. Modeler → domain.md, flows
# 5. Redactor → business_model.md (canônico)
# 6. Reviewer → confidence-report.md
# 7. Handoff → handoff.md

# Validar
visa validate --strict

# Bridge
visa bridge

# Ativar gate
pip install paridade-guard>=0.3.0
paridade-guard contract --migration-dir _visa_sdd/migration --output contract.json
paridade-guard install --pre-commit

# A partir de agora, commits são validados contra specs
```

---

## Validation Commands

```bash
# Check installation
visa status

# Validate artifacts
visa validate
visa validate --strict

# Debug mode
python -v bin/visa install

# Show version
visa --version
```

---

## Expected Outputs

### `visa install`
```
┌─ Visa — Forward Spec Discovery for AI Agents
│  Espelho à frente do Reversa
└─
✅ Engines detectadas: Claude Code
✅ Visa instalada (versão 1.3.0)
   Engines: claude-code
   Agentes: 14
   Arquivos criados: 42
```

### `visa status`
```
═══════════════════════════════════════════════════════════════════════
 Visa — status
═══════════════════════════════════════════════════════════════════════
 Versão:        1.3.0
 Projeto:       meu-projeto
 Nível:         essencial
 Fase atual:    (não iniciada)
═══════════════════════════════════════════════════════════════════════
```

### `visa validate --strict`
```
Validação de _visa_sdd/ (modo --strict)
  Obrigatórios: 14/14
  Opcionais:    3/12
  Canônicos válidos: 4/4

✅ Todos os artefatos obrigatórios presentes.
   E todos os canônicos seguem formato Reversa-compatível.
```

### `visa bridge` (com gate pass)
```
🌉 Conectando Visa ao paridade-guard
   Origem: _visa_sdd

🔍 Gate do Coletor: 0 LACUNA(s) detectada(s) em gaps.md

✅ business_model.md → migration/target_business_rules.md (symlink)
✅ ambiguity_log.md → migration/ambiguity_log.md (symlink)
✅ confidence-report.md → migration/paradigm_decision.md (symlink)

Ponte construída: 3 arquivos em _visa_sdd/migration/
```

---

## Cleanup

```bash
# Uninstall keeping _visa_sdd
visa uninstall --yes

# Uninstall purging everything
visa uninstall --yes --purge
```

---

<p align="center">
<strong>Demo completo! Agora você conhece o ciclo SDD.</strong>
</p>
