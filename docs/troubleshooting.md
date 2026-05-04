# Troubleshooting Guide

Este guia aborda problemas comuns e suas soluções.

## Problemas de Instalação

### `visa: command not found`

**Sintoma**: Após instalação, `visa` não é reconhecido.

**Solução**:
```bash
# Reinstale em modo editável
pip uninstall visa-sdd -y
pip install -e .

# Ou reinstale via pip
pip uninstall visa-sdd -y
pip install visa-sdd
```

**Verificação**:
```bash
visa --version
# deve retornar: visa 1.3.0
```

---

### ModuleNotFoundError: No module named 'visa_sdd'

**Sintoma**: Erro ao importar o módulo.

**Solução**:
```bash
# Verifique se está no diretório correto do projeto
cd caminho/para/visa-main
pip install -e .

# Ou use o bin direto
python bin/visa --version
```

---

## Problemas do CLI

### `visa install` não detecta engine

**Sintoma**: Nenhum engine detectado (CLAUDE.md, AGENTS.md, etc.)

**Solução**:
```bash
# Crie um arquivo de entrada
touch CLAUDE.md  # Para Claude Code
# OU
touch .cursorrules  # Para Cursor
# OU
touch AGENTS.md  # Para Codex

visa install
```

**Engines suportadas**:
| Engine | Arquivo |
|--------|---------|
| Claude Code | `CLAUDE.md` |
| Cursor | `.cursorrules` |
| Codex | `AGENTS.md` |
| Gemini CLI | `GEMINI.md` |

---

### `visa bridge` bloqueado com "BRIDGE BLOQUEADA"

**Sintoma**: Exit code 4, mensagem "BRIDGE BLOQUEADA pelo gate do Coletor"

**Causa**: LACUNAs pendentes em `gaps.md` sem decisão explícita.

**Solução (3 opções)**:

**Opção 1: Resolver com evidência**
```markdown
### LACUNA-001 [RESOLVIDO]
- **Evidência**: 5/5 entrevistados confirmam
```

**Opção 2: Aceitar risco explicitamente**
```markdown
### LACUNA-001 [RISCO ACEITO]
- **Decisor**: Seu Nome
- **Justificativa**: Validarei pós-MVP
```

**Opção 3: Override manual**
```bash
visa bridge --accept-all-risks="spike de 1 dia"
```

---

### `visa validate --strict` falha com "front-matter ausente"

**Sintoma**: Return code 3, artefato sem front-matter YAML.

**Causa**: O artefato canônico não tem o front-matter correto.

**Solução**: Adicione front-matter conforme especificação:

```markdown
---
schemaVersion: 1
kind: target_business_rules
producedBy: visa-redator
---

# Target Business Rules

### BR-FUTURE-001
- **Confiança**: 🟢
- **Descrição**: Sua regra
```

**Verifique**:
```bash
# Deve começar com ---
cat _visa_sdd/business_model.md | head -1
# deve retornar: ---
```

---

### Contract gerado está vazio

**Sintoma**: `paridade-guard contract` gera contrato com 0 cláusulas.

**Causas comuns**:
1. Artefatos sem front-matter
2. IDs canônicos ausentes (`BR-FUTURE-` não encontrado)
3. Versão antiga do paridade-guard

**Solução**:
```bash
# 1. Verifique artefatos
visa validate --strict

# 2. Atualize paridade-guard
pip install paridade-guard>=0.3.0 --upgrade

# 3. Regenerar bridge
visa bridge

# 4. Regenerar contrato
paridade-guard contract \
  --migration-dir _visa_sdd/migration \
  --output _visa_sdd/parity_audit/contract.json
```

---

## Problemas de Testes

### Test suite falha

**Sintoma**: `python3 tests/test_visa.py` retorna falhas.

**Solução**:
```bash
# 1. Verifique versão do Python
python --version  # deve ser 3.10+

# 2. Reinstale dependências de teste
pip install pytest>=7.0

# 3. Execute com verbose
python3 tests/test_visa.py -v

# 4. Para debugging, execute classe por classe
python3 -c "
from test_visa import TestInstall
t = TestInstall()
t.test_install_cria_estrutura_basica()
print('✅ Test passed')
"
```

---

### Tests com SKIPPED (exit code 2)

**Sintoma**: Tests passam mas com SKIPPED.

**Causa**: `paridade-guard` não está instalado (para testes e2e).

**Solução**:
```bash
# Instale paridade-guard para testes completos
pip install paridade-guard>=0.3.0

# Execute novamente
python3 tests/test_visa.py
```

---

## Problemas de Git

### Skills não são removidas com uninstall

**Sintoma**: `.claude/skills/` ainda existe após `visa uninstall`.

**Solução**:
```bash
# Remova manualmente
rm -rf .claude/skills/visa*
rm -rf .agents/skills/visa*

# Ou use purge
visa uninstall --yes --purge
```

---

## Problemas de Performance

### `visa install` lento

**Solução**:
```bash
# Use cache
pip install -e . --no-build-isolation

# Ou verifique rede
ping pypi.org
```

---

### `visa status` retorna dados desatualizados

**Causa**: State.json desatualizado.

**Solução**:
```bash
# Remova state antigo
rm -rf .visa/

# Reinstale
visa install
```

---

## Debug Mode

Para debug detalhado:

```bash
# Execute com Python verbose
python -v bin/visa install

# Ou com traceback
python bin/visa install --project-root . 2>&1 | head -50
```

---

## Como Reportar Issues

Se o problema persistir, abra uma issue com:

1. **Versão**: `visa --version`
2. **Python**: `python --version`
3. **OS**: `uname -a` ou `systeminfo`
4. **Comando exato**: O comando que falhou
5. **Output completo**: `visa <command> 2>&1`
6. **Logs**: Se aplicável

**Template**:
```markdown
## Environment
- visa: 1.3.0
- python: 3.12.0
- os: Windows 11

## Command
visa bridge

## Output
[cola o output aqui]

## Expected
[o que deveria acontecer]

## Actual
[o que aconteceu]
```
