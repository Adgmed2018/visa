#!/usr/bin/env python3
"""
Testes funcionais para a Visa.

Cobertura:
    - install cria estrutura correta com skills, state.json, plan.md, manifest
    - status reporta estado real
    - validate detecta artefatos faltantes
    - bridge cria mapeamento _visa_sdd/ → _reversa_sdd/migration/
    - Skills SKILL.md tem frontmatter válido
    - Espelhamento agente-por-agente com Reversa está correto
"""

from __future__ import annotations

import json
import subprocess
import sys
import tempfile
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parent.parent
VISA_BIN = ROOT / "bin" / "visa"


class SkipTest(Exception):
    """Sinaliza que um teste foi pulado por falta de pré-requisito.

    Diferente de retornar silenciosamente: no runner, casos SkipTest
    aparecem como SKIPPED separadamente de PASSED. Em CI, isso evita o
    falso positivo de cobertura que aconteceria se o teste retornasse
    como passed em ambiente sem o pré-requisito.
    """


def _run_visa(*args, cwd):
    """Invoca o CLI da Visa em um diretório específico."""
    import os
    env = {**os.environ, "PYTHONIOENCODING": "utf-8"}
    result = subprocess.run(
        [sys.executable, str(VISA_BIN), "--project-root", str(cwd), *args],
        capture_output=True, text=True, check=False,
        encoding="utf-8", env=env,
    )
    return result


# ============================================================================
# Skills (frontmatter, completude)
# ============================================================================

class TestSkills:

    EXPECTED_AGENTS = [
        # Orquestrador
        "visa",
        # Time de Descoberta
        "visa-etnografo", "visa-estrategista", "visa-coletor",
        # Time de Síntese
        "visa-paradigm-advisor", "visa-modelador",
        "visa-data-modeler", "visa-design-system",
        # Time de Spec
        "visa-redator", "visa-strategist", "visa-inspector",
        # Time de Handoff
        "visa-revisor", "visa-handoff",
        # Utilitário
        "visa-agents-help",
    ]

    def test_todos_agentes_existem(self):
        for agent in self.EXPECTED_AGENTS:
            skill = ROOT / "agents" / agent / "SKILL.md"
            assert skill.exists(), f"SKILL.md faltando: {agent}"

    def test_todo_skill_tem_frontmatter(self):
        for agent in self.EXPECTED_AGENTS:
            skill = ROOT / "agents" / agent / "SKILL.md"
            content = skill.read_text(encoding="utf-8")
            assert content.startswith("---\n"), f"{agent}: falta frontmatter"
            assert "\n---\n" in content, f"{agent}: frontmatter mal fechado"

    def test_frontmatter_tem_campos_obrigatorios(self):
        required_fields = ["name:", "description:", "license:", "metadata:"]
        for agent in self.EXPECTED_AGENTS:
            content = (ROOT / "agents" / agent / "SKILL.md").read_text(encoding="utf-8")
            head = content.split("\n---\n")[0]
            for field in required_fields:
                assert field in head, f"{agent}: falta campo {field}"

    def test_orquestrador_referencia_outros_agentes(self):
        content = (ROOT / "agents" / "visa" / "SKILL.md").read_text(encoding="utf-8")
        # O orquestrador deve mencionar pelo menos os principais agentes
        assert "etnógrafo" in content.lower() or "etnografo" in content.lower()
        assert "estrategista" in content.lower()
        assert "coletor" in content.lower()

    def test_espelhamento_com_reversa_documentado(self):
        """Cada agente da Visa que tem espelho no Reversa deve declarar
        inverse_of no metadata. Agentes consolidados ou utilitários
        documentam a relação no SKILL.md mas inverse_of pode ser composto.
        """
        # Mapping 1:1 — cada agente Visa espelha exatamente um do Reversa
        one_to_one = {
            "visa": "reversa",
            "visa-etnografo": "reversa-scout",
            "visa-estrategista": "reversa-archaeologist",
            "visa-coletor": "reversa-detective",
            "visa-paradigm-advisor": "reversa-paradigm-advisor",
            "visa-modelador": "reversa-architect",
            "visa-data-modeler": "reversa-data-master",
            "visa-design-system": "reversa-design-system",
            "visa-strategist": "reversa-strategist",
            "visa-inspector": "reversa-inspector",
            "visa-revisor": "reversa-reviewer",
            "visa-handoff": "reversa-migrate",
            "visa-agents-help": "reversa-agents-help",
        }
        for agent, expected_inverse in one_to_one.items():
            content = (ROOT / "agents" / agent / "SKILL.md").read_text(encoding="utf-8")
            assert "inverse_of:" in content, f"{agent}: falta inverse_of"
            assert expected_inverse in content, \
                f"{agent}: inverse_of deveria mencionar {expected_inverse}"

        # visa-redator é consolidação (writer + curator + designer)
        # Só exige que mencione reversa-writer (o principal espelho)
        redator = (ROOT / "agents" / "visa-redator" / "SKILL.md").read_text(encoding="utf-8")
        assert "inverse_of:" in redator
        assert "reversa-writer" in redator

    def test_escala_confianca_em_todos_agentes_relevantes(self):
        """Etnógrafo, Estrategista, Coletor, Modelador, Redator, Revisor
        devem mencionar a escala 🟢🟡🔴."""
        relevant = ["visa", "visa-etnografo", "visa-estrategista",
                    "visa-coletor", "visa-modelador", "visa-redator",
                    "visa-revisor"]
        for agent in relevant:
            content = (ROOT / "agents" / agent / "SKILL.md").read_text(encoding="utf-8")
            assert "🟢" in content and "🟡" in content and "🔴" in content, \
                f"{agent}: falta escala de confiança"


# ============================================================================
# Install
# ============================================================================

class TestInstall:

    def test_install_cria_estrutura_basica(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            # Simula projeto com Claude Code
            (tmp_root / "CLAUDE.md").write_text("# project")

            r = _run_visa("install", cwd=tmp_root)
            assert r.returncode == 0, f"install falhou:\n{r.stdout}\n{r.stderr}"

            # Verifica estrutura criada
            assert (tmp_root / ".visa").is_dir()
            assert (tmp_root / ".visa" / "state.json").exists()
            assert (tmp_root / ".visa" / "plan.md").exists()
            assert (tmp_root / ".visa" / "version").exists()
            assert (tmp_root / "_visa_sdd").is_dir()

    def test_install_copia_todos_os_agentes(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / "CLAUDE.md").write_text("# project")
            _run_visa("install", cwd=tmp_root)

            skills_dir = tmp_root / ".claude" / "skills"
            for agent in TestSkills.EXPECTED_AGENTS:
                assert (skills_dir / agent / "SKILL.md").exists(), \
                    f"{agent} não foi copiado"

    def test_install_state_json_estruturado(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / "CLAUDE.md").write_text("# project")
            _run_visa("install", cwd=tmp_root)

            state = json.loads((tmp_root / ".visa" / "state.json").read_text())
            assert state["version"] == "1.4.2"
            assert state["phase"] is None
            assert state["discovery_level"] == "essencial"
            assert "claude-code" in state["engines"]
            assert len(state["agents"]) == 14
            assert state["pending"][0] == "imersao"  # primeira fase

    def test_install_gera_manifest_sha256(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / "CLAUDE.md").write_text("# project")
            _run_visa("install", cwd=tmp_root)

            manifest_path = tmp_root / ".visa" / "_config" / "files-manifest.json"
            assert manifest_path.exists()
            manifest = json.loads(manifest_path.read_text())
            # Deve ter pelo menos um entry para cada SKILL.md copiado
            skills_in_manifest = [k for k in manifest if k.endswith("SKILL.md")]
            assert len(skills_in_manifest) >= 8, \
                f"Manifest tem só {len(skills_in_manifest)} SKILLs"

            # Cada hash deve ter 64 caracteres (SHA-256)
            for path, h in manifest.items():
                assert len(h) == 64, f"Hash inválido em {path}"

    def test_install_idempotente(self):
        """Rodar install duas vezes não deve quebrar ou duplicar."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / "CLAUDE.md").write_text("# project")

            r1 = _run_visa("install", cwd=tmp_root)
            assert r1.returncode == 0

            r2 = _run_visa("install", cwd=tmp_root)
            assert r2.returncode == 0  # não deve falhar

            # State não deveria ser sobrescrito
            state = json.loads((tmp_root / ".visa" / "state.json").read_text())
            assert state["version"] == "1.4.2"


# ============================================================================
# Status / Validate
# ============================================================================

class TestStatusValidate:

    def test_status_sem_install_alerta(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = _run_visa("status", cwd=Path(tmp))
            # Retorna 1 mas com mensagem clara
            assert "não instalada" in r.stdout

    def test_status_apos_install_mostra_estado(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / "CLAUDE.md").write_text("# project")
            _run_visa("install", cwd=tmp_root)

            r = _run_visa("status", cwd=tmp_root)
            assert r.returncode == 0
            assert "1.4.2" in r.stdout
            assert "essencial" in r.stdout

    def test_validate_detecta_artefatos_faltantes(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / "CLAUDE.md").write_text("# project")
            _run_visa("install", cwd=tmp_root)

            # _visa_sdd/ existe mas vazia
            r = _run_visa("validate", cwd=tmp_root)
            # Deve falhar porque falta tudo
            assert r.returncode == 2  # missing required
            assert "Faltando" in r.stdout or "faltando" in r.stdout

    def test_validate_passa_com_artefatos_completos(self):
        """Modo padrão (sem --strict): basta presença dos 14 obrigatórios."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / "CLAUDE.md").write_text("# project")
            _run_visa("install", cwd=tmp_root)

            # Lista atualizada para v1.1.1: inclui discard_log, ambiguity_log
            visa_sdd = tmp_root / "_visa_sdd"
            required = [
                "landscape.md", "personas-inicial.md", "glossario.md",
                "pains.md", "opportunities.md", "domain.md", "flows.md",
                "architecture.md",
                "business_model.md", "discard_log.md", "ambiguity_log.md",
                "confidence-report.md", "gaps.md", "handoff.md",
            ]
            for name in required:
                (visa_sdd / name).write_text(f"# {name}\nplaceholder")

            r = _run_visa("validate", cwd=tmp_root)
            assert r.returncode == 0, f"validate falhou:\n{r.stdout}"

    def test_validate_strict_rejeita_placeholder_sem_frontmatter(self):
        """Modo --strict: artefatos canônicos sem front-matter falham."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / "CLAUDE.md").write_text("# project")
            _run_visa("install", cwd=tmp_root)

            visa_sdd = tmp_root / "_visa_sdd"
            required = [
                "landscape.md", "personas-inicial.md", "glossario.md",
                "pains.md", "opportunities.md", "domain.md", "flows.md",
                "architecture.md",
                "business_model.md", "discard_log.md", "ambiguity_log.md",
                "confidence-report.md", "gaps.md", "handoff.md",
            ]
            for name in required:
                (visa_sdd / name).write_text(f"# {name}\nplaceholder")

            # validate sem strict: passa
            r = _run_visa("validate", cwd=tmp_root)
            assert r.returncode == 0

            # validate --strict: falha porque canônicos não têm front-matter
            r_strict = _run_visa("validate", "--strict", cwd=tmp_root)
            assert r_strict.returncode == 3, \
                f"--strict deveria retornar 3 (formato inválido), foi {r_strict.returncode}\n{r_strict.stdout}"
            assert "front-matter" in r_strict.stdout.lower() or \
                   "formato" in r_strict.stdout.lower()

    def test_validate_strict_aceita_artefatos_canonicos_corretos(self):
        """Com front-matter válido + IDs canônicos, --strict passa."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / "CLAUDE.md").write_text("# project")
            _run_visa("install", cwd=tmp_root)

            visa_sdd = tmp_root / "_visa_sdd"
            # Não-canônicos: placeholder simples
            for name in ["landscape.md", "personas-inicial.md", "glossario.md",
                         "pains.md", "opportunities.md", "domain.md",
                         "flows.md", "architecture.md", "gaps.md", "handoff.md"]:
                (visa_sdd / name).write_text(f"# {name}")

            # Canônicos: front-matter + IDs
            (visa_sdd / "business_model.md").write_text("""\
---
schemaVersion: 1
kind: target_business_rules
producedBy: visa-redator
---

# Target Business Rules

### BR-FUTURE-001
- **Confiança**: 🟢
- **Descrição**: Regra de exemplo
""", encoding="utf-8")
            (visa_sdd / "discard_log.md").write_text("""\
---
schemaVersion: 1
kind: discard_log
producedBy: visa-redator
---

# Discard Log

### BR-DESCARTAR-001
- **Descrição**: Descartado
""", encoding="utf-8")
            (visa_sdd / "ambiguity_log.md").write_text("""\
---
schemaVersion: 1
kind: ambiguity_log
producedBy: visa-redator
---

# Ambiguity Log

### AMB-FUTURE-001
- **Descrição**: Ambíguo
- **Status**: PENDENTE
""", encoding="utf-8")
            (visa_sdd / "confidence-report.md").write_text("""\
---
schemaVersion: 1
kind: paradigm_decision
producedBy: visa-revisor
---

# Confidence Report
Paradigma: Clean Architecture
""")

            r = _run_visa("validate", "--strict", cwd=tmp_root)
            assert r.returncode == 0, \
                f"--strict deveria passar com artefatos canônicos:\n{r.stdout}"
            assert "canônico" in r.stdout.lower() or \
                   "Reversa-compatível" in r.stdout


# ============================================================================
# Bridge
# ============================================================================

class TestBridge:
    """Bridge v1.1: aponta paridade-guard para _visa_sdd diretamente, sem cópia.

    Validamos o comportamento NOVO:
    - cria stub `_visa_sdd/migration/` com symlinks (ou cópias) dos artefatos canônicos
    - rejeita pipeline incompleto (sem business_model.md, etc.)
    - o conteúdo apontado preserva os IDs `BR-FUTURE-NNN` originais
    """

    # Fixture: artefato canônico válido produzido pelo Redator v1.1+
    CANONICAL_BUSINESS_RULES = """\
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
- **Justificativa**: 5/5 médicos entrevistados; risco regulatório alto
"""

    CANONICAL_AMBIGUITY = """\
---
schemaVersion: 1
kind: ambiguity_log
producedBy: visa-redator
---

# Ambiguity Log

## Itens

### AMB-FUTURE-001
- **Descrição**: Persona "secretária" não foi entrevistada
- **Detectado por**: visa-coletor
- **Origem**: `_visa_sdd/gaps.md`
- **Status**: PENDENTE
"""

    PARADIGM = """\
---
schemaVersion: 1
kind: paradigm_decision
---

# Paradigm Decision

## Decisão

Paradigma: Clean Architecture com Use Cases
"""

    def _setup_canonical_visa_sdd(self, tmp_root: Path):
        visa_sdd = tmp_root / "_visa_sdd"
        visa_sdd.mkdir()
        (visa_sdd / "business_model.md").write_text(
            self.CANONICAL_BUSINESS_RULES, encoding="utf-8")
        (visa_sdd / "ambiguity_log.md").write_text(
            self.CANONICAL_AMBIGUITY, encoding="utf-8")
        (visa_sdd / "confidence-report.md").write_text(
            self.PARADIGM, encoding="utf-8")
        return visa_sdd

    def test_bridge_cria_migration_stub_em_visa_sdd(self):
        """v1.1: stub fica em _visa_sdd/migration/, não em _reversa_sdd/migration/."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            self._setup_canonical_visa_sdd(tmp_root)

            r = _run_visa("bridge", cwd=tmp_root)
            assert r.returncode == 0, f"bridge falhou:\n{r.stdout}\n{r.stderr}"

            stub = tmp_root / "_visa_sdd" / "migration"
            assert stub.is_dir()
            assert (stub / "target_business_rules.md").exists()
            assert (stub / "ambiguity_log.md").exists()
            assert (stub / "paradigm_decision.md").exists()

    def test_bridge_preserva_ids_canonicos(self):
        """O arquivo apontado deve conter os IDs originais BR-FUTURE-NNN."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            self._setup_canonical_visa_sdd(tmp_root)
            _run_visa("bridge", cwd=tmp_root)

            stub_business = tmp_root / "_visa_sdd" / "migration" / "target_business_rules.md"
            content = stub_business.read_text(encoding="utf-8")
            assert "BR-FUTURE-001" in content
            assert "Validação de CRM" in content
            assert "schemaVersion: 1" in content

    def test_bridge_rejeita_pipeline_incompleto(self):
        """Sem business_model.md canônico, bridge aborta."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            visa_sdd = tmp_root / "_visa_sdd"
            visa_sdd.mkdir()
            # Só artefatos da fase de imersão — Redator não rodou
            (visa_sdd / "landscape.md").write_text("# Landscape")

            r = _run_visa("bridge", cwd=tmp_root)
            assert r.returncode == 2, f"esperado returncode 2, foi {r.returncode}"
            assert "Abortando" in r.stdout or "abortando" in r.stdout.lower()

    def test_bridge_alerta_mas_continua_se_so_alguns_canonicos(self):
        """Se business_model.md está válido mas ambiguity_log.md falta, bridge segue
        com warning (não trava)."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            visa_sdd = tmp_root / "_visa_sdd"
            visa_sdd.mkdir()
            (visa_sdd / "business_model.md").write_text(
                self.CANONICAL_BUSINESS_RULES, encoding="utf-8")
            (visa_sdd / "confidence-report.md").write_text(
                self.PARADIGM, encoding="utf-8")
            # ambiguity_log.md ausente

            r = _run_visa("bridge", cwd=tmp_root)
            assert r.returncode == 0, f"bridge deveria seguir:\n{r.stdout}"
            assert (tmp_root / "_visa_sdd" / "migration" / "target_business_rules.md").exists()

    def test_bridge_sem_visa_sdd_falha_grácil(self):
        with tempfile.TemporaryDirectory() as tmp:
            r = _run_visa("bridge", cwd=Path(tmp))
            assert r.returncode == 1
            assert "não existe" in r.stdout


# ============================================================================
# Collector Gate — comando v1.2
# ============================================================================

class TestCollectorGate:
    """v1.2: gate computacional do Coletor.

    `visa bridge` recusa prosseguir se `gaps.md` tem LACUNAS 🔴 sem
    decisão explícita (resolvido / risco aceito / override).
    """

    # Fixture: business_model.md canônico mínimo (necessário para o bridge passar
    # da etapa 1 quando o gate da etapa 0 não bloquear).
    CANONICAL_BM = """\
---
schemaVersion: 1
kind: target_business_rules
producedBy: visa-redator
---

# Target Business Rules

### BR-FUTURE-001
- **Confiança**: 🟢
- **Descrição**: Regra de exemplo
"""

    def _setup(self, tmp_root: Path):
        (tmp_root / "CLAUDE.md").write_text("# project")
        _run_visa("install", cwd=tmp_root)
        (tmp_root / "_visa_sdd" / "business_model.md").write_text(
            self.CANONICAL_BM, encoding="utf-8")

    def test_gate_bloqueia_quando_ha_lacuna_pendente(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            self._setup(tmp_root)
            (tmp_root / "_visa_sdd" / "gaps.md").write_text(
                "# Gaps\n\n### LACUNA-001\n- 🔴 LACUNA não resolvida\n",
                encoding="utf-8")

            r = _run_visa("bridge", cwd=tmp_root)
            assert r.returncode == 4, \
                f"esperava exit 4 (gate), foi {r.returncode}\n{r.stdout}"
            assert "BRIDGE BLOQUEADA" in r.stdout
            assert "LACUNA-001" in r.stdout

    def test_gate_aceita_lacuna_marcada_como_resolvido_no_heading(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            self._setup(tmp_root)
            (tmp_root / "_visa_sdd" / "gaps.md").write_text(
                "# Gaps\n\n"
                "### LACUNA-001 [RESOLVIDO]\n"
                "- **Evidência**: 5/5 entrevistados\n",
                encoding="utf-8")

            r = _run_visa("bridge", cwd=tmp_root)
            assert r.returncode == 0, \
                f"esperava exit 0 (gate aprova), foi {r.returncode}\n{r.stdout}"
            assert "Resolvidas:    1" in r.stdout
            assert "PENDENTES:    0" in r.stdout

    def test_gate_aceita_lacuna_marcada_como_risco_aceito_no_heading(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            self._setup(tmp_root)
            (tmp_root / "_visa_sdd" / "gaps.md").write_text(
                "# Gaps\n\n"
                "### LACUNA-001 [RISCO ACEITO]\n"
                "- **Decisor**: Alexandre\n"
                "- **Justificativa**: Pós-MVP\n",
                encoding="utf-8")

            r = _run_visa("bridge", cwd=tmp_root)
            assert r.returncode == 0, f"{r.returncode}\n{r.stdout}"
            assert "Risco aceito: 1" in r.stdout

    def test_gate_aceita_via_frontmatter_accepted_risks(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            self._setup(tmp_root)
            (tmp_root / "_visa_sdd" / "gaps.md").write_text(
                "---\n"
                "accepted_risks:\n"
                "  - LACUNA-001: pricing-tier — pós-MVP\n"
                "---\n\n"
                "# Gaps\n\n### LACUNA-001\n- 🔴 pricing\n",
                encoding="utf-8")

            r = _run_visa("bridge", cwd=tmp_root)
            assert r.returncode == 0, f"{r.returncode}\n{r.stdout}"
            assert "Risco aceito: 1" in r.stdout

    def test_gate_override_via_accept_all_risks_com_motivo(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            self._setup(tmp_root)
            (tmp_root / "_visa_sdd" / "gaps.md").write_text(
                "# Gaps\n\n### LACUNA-001\n- 🔴 sem decisão\n",
                encoding="utf-8")

            r = _run_visa(
                "bridge", "--accept-all-risks=spike de 1 dia",
                cwd=tmp_root,
            )
            assert r.returncode == 0, f"{r.returncode}\n{r.stdout}"
            assert "--accept-all-risks ativado" in r.stdout
            assert "spike de 1 dia" in r.stdout

    def test_gate_override_sem_motivo_emite_warning(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            self._setup(tmp_root)
            (tmp_root / "_visa_sdd" / "gaps.md").write_text(
                "# Gaps\n### LACUNA-001\n- 🔴 sem decisão\n",
                encoding="utf-8")

            r = _run_visa("bridge", "--accept-all-risks", cwd=tmp_root)
            assert r.returncode == 0
            assert ("sem motivo declarado" in r.stdout or
                    "motivo não declarado" in r.stdout.lower())

    def test_gate_skip_completo(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            self._setup(tmp_root)
            (tmp_root / "_visa_sdd" / "gaps.md").write_text(
                "### LACUNA-001\n- 🔴\n", encoding="utf-8")

            r = _run_visa("bridge", "--skip-collector-gate", cwd=tmp_root)
            assert r.returncode == 0
            assert "skip-collector-gate ativado" in r.stdout

    def test_gate_sem_gaps_md_nao_bloqueia(self):
        """Se gaps.md não existe, bridge prossegue normalmente."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            self._setup(tmp_root)
            # Não cria gaps.md

            r = _run_visa("bridge", cwd=tmp_root)
            assert r.returncode == 0, f"{r.returncode}\n{r.stdout}"

    def test_gate_inline_lacuna_sem_id_estruturado_bloqueia(self):
        """🔴 inline sem ### LACUNA-NNN também bloqueia (orienta a estruturar)."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            self._setup(tmp_root)
            (tmp_root / "_visa_sdd" / "gaps.md").write_text(
                "# Gaps\n\nAlgo importante: 🔴 não validado.\n",
                encoding="utf-8")

            r = _run_visa("bridge", cwd=tmp_root)
            assert r.returncode == 4
            assert "BLOQUEADA" in r.stdout


# ============================================================================
# Uninstall — comando v1.1.1
# ============================================================================

class TestUninstall:
    """v1.1.1: comando uninstall implementado (era fantasma na v1.1)."""

    def test_uninstall_remove_skills_e_state(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / "CLAUDE.md").write_text("# project")
            _run_visa("install", cwd=tmp_root)
            assert (tmp_root / ".visa").exists()
            assert (tmp_root / ".claude" / "skills").exists()

            r = _run_visa("uninstall", "--yes", cwd=tmp_root)
            assert r.returncode == 0, f"uninstall falhou:\n{r.stdout}\n{r.stderr}"
            assert not (tmp_root / ".visa").exists(), \
                ".visa/ deveria ter sido removida"
            # skills devem ter sido removidos
            claude_skills = tmp_root / ".claude" / "skills"
            assert not claude_skills.exists() or not any(claude_skills.iterdir()), \
                "skills deveriam ter sido removidos ou pasta esvaziada"

    def test_uninstall_preserva_visa_sdd_por_default(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / "CLAUDE.md").write_text("# project")
            _run_visa("install", cwd=tmp_root)
            # Usuário criou conteúdo em _visa_sdd/
            (tmp_root / "_visa_sdd" / "user-content.md").write_text("conteúdo do usuário", encoding="utf-8")

            r = _run_visa("uninstall", "--yes", cwd=tmp_root)
            assert r.returncode == 0
            assert (tmp_root / "_visa_sdd").exists(), "_visa_sdd/ deveria estar preservada"
            assert (tmp_root / "_visa_sdd" / "user-content.md").exists()

    def test_uninstall_purge_remove_visa_sdd(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / "CLAUDE.md").write_text("# project")
            _run_visa("install", cwd=tmp_root)
            (tmp_root / "_visa_sdd" / "x.md").write_text("x")

            r = _run_visa("uninstall", "--yes", "--purge", cwd=tmp_root)
            assert r.returncode == 0
            assert not (tmp_root / "_visa_sdd").exists(), \
                "--purge deveria ter removido _visa_sdd/"

    def test_uninstall_sem_visa_instalada_e_idempotente(self):
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            r = _run_visa("uninstall", "--yes", cwd=tmp_root)
            assert r.returncode == 0  # não falha se já não estava instalada
            assert "não está instalada" in r.stdout or "nada a remover" in r.stdout


# ============================================================================
# References — garante que arquivos referenciados pelo orquestrador existem
# ============================================================================

class TestReferences:
    """Defeito histórico (v1.0): pastas references/ vazias quebravam o
    orquestrador. v1.1 garante presença mínima de arquivos referenciados
    explicitamente em SKILL.md (linha 33-34, 43 do orquestrador)."""

    def test_orquestrador_step_01_existe(self):
        path = ROOT / "agents" / "visa" / "references" / "step-01-first-run.md"
        assert path.exists(), \
            "step-01-first-run.md é referenciado pelo orquestrador e deve existir"

    def test_orquestrador_step_02_existe(self):
        path = ROOT / "agents" / "visa" / "references" / "step-02-resume.md"
        assert path.exists()

    def test_orquestrador_checkpoint_guide_existe(self):
        path = ROOT / "agents" / "visa" / "references" / "checkpoint-guide.md"
        assert path.exists()

    def test_todas_pastas_references_tem_pelo_menos_readme(self):
        """Sem README.md, install pode pular pastas vazias e o agente pode
        tentar ler arquivos inexistentes."""
        for agent_dir in (ROOT / "agents").iterdir():
            ref_dir = agent_dir / "references"
            if not ref_dir.exists():
                continue
            files = list(ref_dir.iterdir())
            assert files, f"{agent_dir.name}/references/ está vazia"


# ============================================================================
# End-to-end real: Visa → bridge → paridade-guard → cláusulas extraídas
# ============================================================================

class TestEndToEndComParidadeGuard:
    """Cadeia completa: install → escrever artefato canônico → bridge →
    paridade-guard contract → verificar cláusulas reais extraídas.

    Pula se paridade-guard não estiver instalado (skip, não fail) — esses
    testes só rodam quando o ambiente tem ambos.
    """

    def _paridade_guard_disponivel(self) -> bool:
        import shutil as _shutil
        return _shutil.which("paridade-guard") is not None

    def test_ciclo_completo_extrai_clausulas_reais(self):
        if not self._paridade_guard_disponivel():
            pytest.skip(
                "paridade-guard não está instalado neste ambiente — "
                "este teste valida a tese central da v1.1+ e DEVE rodar antes "
                "de qualquer release. Instale com: pip install paridade-guard>=0.3.0"
            )

        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            (tmp_root / "CLAUDE.md").write_text("# project")

            # 1. Install Visa
            _run_visa("install", cwd=tmp_root)

            # 2. Escrever business_model.md no formato canônico
            visa_sdd = tmp_root / "_visa_sdd"
            (visa_sdd / "business_model.md").write_text("""\
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
- **Justificativa**: 5/5 médicos entrevistados
- **Compatibilidade com paradigma alvo**: Use Case com guard

### BR-FUTURE-002
- **Origem**: Inferência do Modelador
- **Confiança**: 🟡
- **Descrição**: Lembrete automático 24h antes da consulta
- **Justificativa**: Padrão de mercado SaaS de saúde
- **Compatibilidade com paradigma alvo**: Job assíncrono
""", encoding="utf-8")

            (visa_sdd / "ambiguity_log.md").write_text("""\
---
schemaVersion: 1
kind: ambiguity_log
producedBy: visa-redator
---

# Ambiguity Log

## Itens

### AMB-FUTURE-001
- **Descrição**: Persona "secretária" não foi entrevistada
- **Detectado por**: visa-coletor
- **Origem**: `_visa_sdd/gaps.md`
- **Status**: PENDENTE
""", encoding="utf-8")

            (visa_sdd / "confidence-report.md").write_text("""\
---
schemaVersion: 1
kind: paradigm_decision
---

# Confidence Report

## Decisão

Paradigma: Clean Architecture com Use Cases
""", encoding="utf-8")

            # 3. Bridge
            r = _run_visa("bridge", cwd=tmp_root)
            assert r.returncode == 0, f"bridge falhou:\n{r.stdout}"

            # 4. paridade-guard contract
            r_pg = subprocess.run(
                ["paridade-guard",
                 "--project-root", str(tmp_root),
                 "contract",
                 "--migration-dir", "_visa_sdd/migration",
                 "--output", "_visa_sdd/parity_audit/contract.json"],
                capture_output=True, text=True
            )
            assert r_pg.returncode == 0, \
                f"paridade-guard falhou:\n{r_pg.stdout}\n{r_pg.stderr}"

            # 5. Validar contrato
            contract_path = tmp_root / "_visa_sdd" / "parity_audit" / "contract.json"
            assert contract_path.exists()

            contract = json.loads(contract_path.read_text(encoding="utf-8"))
            ids = [c["id"] for c in contract["clauses"]]

            # Asserts decisivos: as cláusulas ativas devem aparecer
            assert "BR-FUTURE-001" in ids, \
                f"BR-FUTURE-001 não foi extraído. Cláusulas: {ids}"
            assert "BR-FUTURE-002" in ids
            assert "AMB-FUTURE-001" in ids

            # Paradigma capturado
            assert "Clean Architecture" in contract["paradigm"], \
                f"Paradigma não capturado: {contract['paradigm']!r}"

            # Severities corretas
            by_id = {c["id"]: c for c in contract["clauses"]}
            assert by_id["BR-FUTURE-001"]["severity"] == "bloqueante"
            assert by_id["BR-FUTURE-002"]["severity"] == "advertencia"
            assert by_id["AMB-FUTURE-001"]["severity"] == "bloqueante"


# ============================================================================
# Runner
# ============================================================================

def _run_class(cls):
    instance = cls()
    methods = sorted(m for m in dir(instance) if m.startswith("test_"))
    passed = failed = skipped = 0
    skip_reasons: list[str] = []
    for m in methods:
        try:
            getattr(instance, m)()
            print(f"  ✅ {m}")
            passed += 1
        except SkipTest as s:
            print(f"  ⏭️  SKIPPED {m}: {s}")
            skipped += 1
            skip_reasons.append(f"{cls.__name__}::{m}: {s}")
        except AssertionError as e:
            print(f"  ❌ {m}: {e}")
            failed += 1
        except Exception as e:
            import traceback
            print(f"  💥 {m}: {type(e).__name__}: {e}")
            traceback.print_exc(limit=2)
            failed += 1
    return passed, failed, skipped, skip_reasons


if __name__ == "__main__":
    total_p = total_f = total_s = 0
    all_skip_reasons: list[str] = []
    for cls in [TestSkills, TestInstall, TestStatusValidate, TestBridge,
                TestCollectorGate, TestUninstall, TestReferences,
                TestEndToEndComParidadeGuard]:
        print(f"\n{cls.__name__}")
        print("-" * 70)
        p, f, s, reasons = _run_class(cls)
        total_p += p
        total_f += f
        total_s += s
        all_skip_reasons.extend(reasons)

    print(f"\n{'=' * 70}")
    print(f"PASSED: {total_p}    FAILED: {total_f}    SKIPPED: {total_s}")
    if all_skip_reasons:
        print("\nSkipped tests (NÃO foram exercidos — não confunda com passed):")
        for reason in all_skip_reasons:
            print(f"  - {reason}")
    print(f"{'=' * 70}")
    # Exit codes: 0 só se TUDO passou e zero foi skipado.
    # 1 se houve falha. 2 se houve skip (CI deveria distinguir antes de release).
    if total_f > 0:
        sys.exit(1)
    if total_s > 0:
        sys.exit(2)
    sys.exit(0)
