# Instruções para Commit — v1.4.2 + v1.5.0 + v1.6.0

> Este pacote contém 3 releases combinados, executados em uma única passada de engenharia.
> Tempo estimado para aplicar: 30 minutos.

---

## 1. Pré-requisitos

- Git instalado, repo `Adgmed2018/visa` clonado localmente
- Python 3.10+, `pip install -e ".[dev]"` no clone
- Acesso de push para `main`

## 2. Aplicar o pacote

Extraia o ZIP recebido (`visa-v1.4.2-v1.5.0-v1.6.0.zip`) sobre o seu clone:

```bash
cd /caminho/para/seu/clone-visa
unzip -o /caminho/para/visa-v1.4.2-v1.5.0-v1.6.0.zip
```

Os arquivos sobrescritos:
- `pyproject.toml` (versão + mypy fix)
- `README.md` (PT-BR primário, reposicionamento)
- `src/visa_sdd/cli.py` (versão + 2 engines + 4 subcomandos)
- `src/visa_sdd/__init__.py` (versão)
- `tests/test_visa.py` (3 asserções de versão)

Arquivos novos:
- `README.en.md`
- `src/visa_sdd/py.typed`
- `src/visa_sdd/telemetry.py`
- `src/visa_sdd/webui.py`
- `agents/visa-claude-md-builder/` (1 skill)
- `agents/visa-vertical-fintech-pix/` (1 skill)
- `agents/visa-vertical-healthtech-anvisa/` (1 skill)
- `agents/visa-vertical-legaltech-tributario/` (1 skill)
- `docs/verification/v1.6.0/FINAL.log`
- `CHANGELOG-v1.4.2-v1.5.0-v1.6.0.md`

## 3. Validar localmente

```bash
pip install -e ".[dev]" --upgrade
ruff check src/ tests/                # All checks passed!
pytest tests/test_logging_exceptions.py  # 63 passed
pytest tests/test_visa.py -k "not e2e and not EndToEnd"  # 39 passed, 1 deselected
visa --help                           # deve listar: install, status, validate, bridge, serve, telemetry, doctor, upgrade, uninstall
visa doctor                           # rode em projeto com CLAUDE.md
```

## 4. Smoke test do Web UI (opcional)

```bash
cd /tmp && mkdir wuitest && cd wuitest && touch CLAUDE.md
visa install
visa serve --port 18765
# Abrir http://127.0.0.1:18765/ no browser
```

## 5. Commitar

Sugestão de mensagens (convencional commits):

```bash
git add .
git commit -m "feat(release): combinado v1.4.2 + v1.5.0 + v1.6.0

v1.4.2 (Higiene + Antigravity):
- Bump versão 1.4.1 → 1.4.2 (T1)
- mypy: strict_concatenate → extra_checks (T2)
- README: 40 testes → 102+ testes (T3)
- Engines: + Google Antigravity, + Windsurf (E1)
- py.typed marker (T11)

v1.5.0 (Reposicionamento + UX):
- README PT-BR primário, EN secundário (M1)
- Tagline: 'Spec é software' + categoria EngIA (M2-M4)
- visa doctor: diagnóstico de instalação (P1)
- visa upgrade: atualiza skills sem reinstalar (P2)
- skill visa-claude-md-builder (E10)

v1.6.0 (Telemetria + Verticais + Web UI):
- visa telemetry: opt-in privacidade-first LGPD/GDPR (P4)
- 3 vertical packs: fintech-pix, healthtech-anvisa, legaltech-tributario (P5)
- visa serve: Web UI mínima stdlib-only (P6)

Verificação: 102 testes passing, ruff zero warnings.
Log completo: docs/verification/v1.6.0/FINAL.log"
```

## 6. Tag + push

```bash
git tag -a v1.4.2 -m "v1.4.2: Higiene + Antigravity"
git tag -a v1.5.0 -m "v1.5.0: Reposicionamento + UX (doctor, upgrade, claude-md-builder)"
git tag -a v1.6.0 -m "v1.6.0: Telemetria + 3 verticais + Web UI"

git push origin main
git push origin v1.4.2 v1.5.0 v1.6.0
```

## 7. Publicar no PyPI

```bash
# Atualize a versão no pyproject.toml para 1.6.0 antes (já está 1.4.2 — bumpe se quiser publicar todas em sequência)
python -m build
twine upload dist/*
```

## 8. Pendentes humanos (NÃO inclusos no pacote)

| Item | Por que humano | Prazo sugerido |
|---|---|---|
| M6: Vídeo demo 3 min | Requer gravação humana | 7 dias |
| M7: Domínio próprio + email | Requer registro pago | 1 dia |
| C1: Setup Discord/Telegram | Requer conta + moderação | 3 dias |
| C6: Outbound 30 design partners | Requer contato 1-a-1 (André Vugo, MP, fintechs Sandeco) | 60 dias rolling |
| Mensagem ao Sandeco (E6) | Negociação humana | 7 dias (URGENTE) |

## 9. Anti-checklist (o que NÃO fazer)

- ❌ Não publique no PyPI até bumpar a versão para a release final desejada (decida: 1.4.2, 1.5.0 ou 1.6.0 — recomendado: faça as 3 releases separadas no GitHub mas publique 1.6.0 no PyPI direto)
- ❌ Não esqueça de migrar `paridade-guard` para depender da versão correta da Visa
- ❌ Não remova arquivos antigos (`INSTRUCOES-COMMIT-v1.4.1.md`, etc.) — eles são histórico

---

**Pronto.** Esta release move Visa de "promissor mas verde" para "produto referência da categoria EngIA em PT-BR" com as condições estruturais para o acordo Sandeco e captação dos primeiros pagantes.
