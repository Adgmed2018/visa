# Instruções de Commit — visa-sdd v1.4.2

## Passo a passo

### 1. Verificar

```bash
cd /caminho/do/repo/visa
python -m pip install -e ".[test]"
python -m pytest tests/ -v
# Esperado: 102 passed, 1 skipped, 0 failed

python -m ruff check src/ tests/
# Esperado: All checks passed!

python -m build
# Esperado: Successfully built
```

### 2. Commit

```bash
git add -A
git commit -m "fix: auditoria Windows — 4 correções cross-platform

- fix(cli): UnicodeEncodeError cp1252 — UTF-8 forçado em main()
- fix(test): encoding='utf-8' em todas as chamadas read_text/write_text com emoji
- fix(test): _run_visa() agora passa encoding + PYTHONIOENCODING para subprocess
- fix(test): 'which' → shutil.which() para compatibilidade Windows"
```

### 3. Push e tag

```bash
git push origin main
git tag -a v1.4.2 -m "v1.4.2 — Windows cross-platform encoding fixes"
git push origin v1.4.2
```

## Arquivos alterados

| Arquivo | Operação | Descrição |
| --- | --- | --- |
| `src/visa_sdd/cli.py` | **EDITADO** | UTF-8 stdout/stderr reconfigure em main() |
| `tests/test_visa.py` | **EDITADO** | encoding em _run_visa, read_text, write_text; shutil.which |
| `CHANGELOG.md` | **EDITADO** | Entry v1.4.2 |
| `docs/verification/v1.4.2/FINAL.log` | **NOVO** | Log reproduzível |
