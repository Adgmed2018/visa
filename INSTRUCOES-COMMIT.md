# Instruções para Aplicar v1.4.1 (Auditoria do v1.4.0)

## O que mudou de v1.4.0 → v1.4.1

Esta release foi gerada após **auditoria adversarial do ZIP v1.4.0** usando o Prompt Master de Auditoria (4 fases). Encontrei e corrigi 3 problemas reais que escaparam à v1.4.0.

## Tabela Verificada

| Métrica | v1.4.0 | v1.4.1 |
|---|---|---|
| Pytest | 87 passed + 1 xfail + **1 failed** (SkipTest spurious) | **102 passed + 1 skipped + 0 failed** |
| Coverage total | 80% | **84%** |
| Coverage logging.py | 67% | **85%** |
| mypy strict | 0 erros | **0 erros** |
| ruff | All passed | **All passed** |

## 3 Bugs Corrigidos

### 1. set_quiet(True) não suprimia INFO/DEBUG (lógica invertida)
**Local:** `src/visa_sdd/logging.py:112`
**Antes:** `if _G_QUIET and level.value >= LogLevel.WARNING.value: pass` (no-op)
**Depois:** `if _G_QUIET and level.value < LogLevel.WARNING.value: return`

### 2. Teste e2e do paridade-guard registrava como FAILED quando deveria ser SKIPPED
**Local:** `tests/test_visa.py:784`
**Antes:** `raise SkipTest(...)` (exception customizada local)
**Depois:** `pytest.skip(...)` (API oficial do pytest)

### 3. Coverage de logging.py em 67%
**Solução:** 14 testes novos em `tests/test_logging_exceptions.py` cobrindo Spinner, success/warning/error_output/info, suppression behavior, edge cases de progress.

## Como Aplicar

```bash
cd ~/projects
mv visa visa-v1.4.0-backup-$(date +%Y%m%d)
unzip ~/Downloads/visa-v1.4.1-audited.zip -d ./
cd visa-v1.4.0  # nome da pasta extraída

# Migra .git
cp -r ../visa-v1.4.0-backup-*/visa/.git ./

# Verifica local
python3 -m venv .venv && . .venv/bin/activate
pip install -e ".[dev,test]"
pytest tests/ -v          # esperado: 102 passed, 1 skipped
mypy --strict src/visa_sdd/   # Success: no issues
ruff check src/ tests/        # All checks passed

# Commit
git add -A
git commit -m "v1.4.1: audit closure — fix set_quiet + SkipTest + coverage 84%

Auditoria adversarial do ZIP v1.4.0 usando Prompt Master de Auditoria.
3 bugs reais corrigidos:
- src/visa_sdd/logging.py:112 set_quiet lógica invertida
- tests/test_visa.py:784 SkipTest customizado → pytest.skip()
- 14 testes novos em test_logging_exceptions.py (logging 67% → 85%)

Métricas verificadas (docs/verification/v1.4.1/AUDIT.log):
- 102 testes passing + 1 skip (e2e externo) + 0 failed
- coverage total: 80% → 84%
- coverage logging.py: 67% → 85%
- mypy strict: 0 erros
- ruff: All checks passed"

git push origin main
```

## Validação Local Esperada

Após aplicar, esses comandos devem retornar exatamente isso:

```bash
$ pytest tests/ -q | tail -1
102 passed, 1 skipped in ~3s

$ mypy --strict src/visa_sdd/ | tail -1
Success: no issues found in 4 source files

$ ruff check src/ tests/ | tail -1
All checks passed!

$ visa --version
visa 1.4.1
```

## O Que NÃO Foi Mudado (Intencional)

- **Refactor modular do CLI** continua para v1.5.0 (out-of-scope do hotfix)
- **Frente 2 (validação LLM real dos 6 SKILLs)** continua exigindo sessão Claude Code real
- **Case study externo** continua exigindo mão humana
