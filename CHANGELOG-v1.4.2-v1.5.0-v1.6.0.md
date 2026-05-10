# Changelog — v1.4.2 → v1.5.0 → v1.6.0

> Release combinado executado em uma única passada de engenharia.
> Verificacao: `docs/verification/v1.6.0/FINAL.log`

---

## v1.6.0 — Telemetria + 3 Verticais + Web UI (NOVO)

### Adicionado
- **`visa serve`** (P6): Web UI mínima single-file (`http.server` stdlib, zero deps externas) para visualizar `_visa_sdd/`, listar artefatos, listar `BR-FUTURE-NNN`, ver state. Renderizador markdown próprio (sem deps). Sandboxed: HTTP só em localhost, paths fora de `project_root` bloqueados.
- **`visa telemetry [on|off|status|purge]`** (P4): telemetria **opt-in** privacidade-first. ID anônimo (sha256 de MAC+username, nunca exportado em claro). Eventos contados (sem conteúdo). Log local `.visa/telemetry.jsonl`. Endpoint remoto opcional via env `VISA_TELEMETRY_ENDPOINT`. Direito ao esquecimento via `purge`. Conformidade LGPD/GDPR documentada em `src/visa_sdd/telemetry.py`.
- **3 vertical packs (P5):**
  - `visa-vertical-fintech-pix`: 6 BR-FUTURE pré-cadastradas (DICT, MED, KYC/PLD, BACEN 4.658, LGPD) + 4 LACUNAS regulatórias bloqueantes.
  - `visa-vertical-healthtech-anvisa`: 6 BR-FUTURE (SaMD RDC 657, CFM 2.314 telemedicina, CFM 1.821 PEP, prescrição digital, LGPD-Saúde, ISO 13485) + 4 LACUNAS.
  - `visa-vertical-legaltech-tributario`: 6 BR-FUTURE (e-CAC/PJe/SPED, OAB 49/2017, LGPD jurídico, certificado digital, auditoria IA) + 4 LACUNAS.

### Pendente humano (não automatizável)
- C1: Setup Discord/Telegram da comunidade Visa
- C6: Outbound para 30 design partners (Adgmed2018 precisa executar)

---

## v1.5.0 — Reposicionamento + UX

### Adicionado
- **`visa doctor`** (P1): diagnóstico completo de instalação. Checa engine detectada, skills presentes, state coerente, artefatos `_visa_sdd/`, disponibilidade do `paridade-guard`. Exit codes: 0 saudável, 1 avisos, 2 erros críticos.
- **`visa upgrade`** (P2): atualiza skills sem reinstalar do zero. Compara hash sha256 de `SKILL.md` e copia só o que mudou. Preserva `_visa_sdd/` e `.visa/state.json`. Atualiza `version` no state.
- **Skill `visa-claude-md-builder`** (E10): novo agente que gera `CLAUDE.md` (ou ANTIGRAVITY.md, AGENTS.md, .cursorrules, GEMINI.md, .windsurfrules) consolidado a partir dos artefatos canônicos em `_visa_sdd/`. É a "memória de longo prazo" do projeto para o agente de codificação.

### Mudado
- **README.md** (M1+M2+M3+M4): reescrito em PT-BR como narrativa primária. EN movido para `README.en.md`. Nova tagline: **"Spec é software. E software exige engenharia."** Nova categoria: **"EngIA tooling / EI Engineering"** (não mais "Spec Governance"). Tabela Comparison reposicionada contra Reversa/Spec Kit/Jama/DOORS (categoria correta) ao invés de Cursor/Aider (categoria errada).
- README cita ecossistema EngIA brasileiro (Sandeco Macedo, livro "AI End").

### Pendente humano (não automatizável)
- M6: Vídeo demo 3 minutos (gravação humana)
- M7: Domínio próprio + email institucional (registro humano)

---

## v1.4.2 — Higiene Técnica + Antigravity

### Adicionado
- **2 engines novas** (E1): `Google Antigravity` (entry: `ANTIGRAVITY.md`) e `Windsurf` (entry: `.windsurfrules`). Total agora: 6 engines suportadas.
- **`py.typed` marker** (T11): `src/visa_sdd/py.typed` permite mypy/pyright detectarem tipos do pacote.

### Corrigido
- **`pyproject.toml`** (T2): `strict_concatenate = true` (deprecado em mypy 2.x) → `extra_checks = true`. Evita erro fatal em builds futuros.

### Mudado
- **Bump versão 1.4.1 → 1.4.2** (T1) em `pyproject.toml`, `src/visa_sdd/cli.py`, `src/visa_sdd/__init__.py`, `tests/test_visa.py` (3 asserções).
- **README.md** (T3): "40 testes passando" → "102+ testes passando" (subdeclaração corrigida; o real é 102 + 1 e2e deselected).

---

## Resultado verificado

| Métrica | Baseline (v1.4.1) | Após release (v1.6.0) | Delta |
|---|---|---|---|
| Testes passando | 102 + 1 e2e | 102 + 1 e2e | mantido |
| Ruff warnings | 0 | 0 | mantido |
| Engines suportadas | 4 | 6 | +2 (Antigravity, Windsurf) |
| Subcomandos CLI | 5 | 9 | +4 (doctor, upgrade, telemetry, serve) |
| Agentes (skills) | 14 | 18 | +4 (claude-md-builder, 3 verticais) |
| Linhas de código `cli.py` | 1.090 | 1.326 | +236 |
| Novos módulos Python | 0 | 2 | telemetry.py, webui.py |
| Dependências externas | 0 | 0 | mantido |
| README idioma primário | EN | **PT-BR** | reposicionamento |

