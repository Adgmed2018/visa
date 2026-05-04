#!/usr/bin/env python3
"""
visa — CLI principal da Visa.

Comandos:
  install      Instala skills da Visa no projeto
  status       Mostra estado atual da descoberta
  validate     Valida que _visa_sdd/ tem todos os artefatos esperados
  bridge       Valida formato canônico e cria stub para paridade-guard ≥ 0.3.0
  uninstall    Remove skills/state da Visa do projeto (preserva _visa_sdd/)

Filosofia: a Visa em si roda dentro do agente de codificação (Claude Code,
Cursor, etc.) via skills. Este CLI é só plumbing: instalação, status,
bridges para o ecossistema (paridade-guard, Spec Kit, Reconstructor).
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import sys
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

VISA_VERSION = "1.4.0"

# Engines suportadas (espelho do detector.js do Reversa)
ENGINES = [
    {"id": "claude-code", "name": "Claude Code", "entry": "CLAUDE.md",
     "skills_dir": ".claude/skills", "universal": ".agents/skills"},
    {"id": "codex", "name": "Codex", "entry": "AGENTS.md",
     "skills_dir": ".agents/skills", "universal": ".agents/skills"},
    {"id": "cursor", "name": "Cursor", "entry": ".cursorrules",
     "skills_dir": ".agents/skills", "universal": ".agents/skills"},
    {"id": "gemini-cli", "name": "Gemini CLI", "entry": "GEMINI.md",
     "skills_dir": ".agents/skills", "universal": ".agents/skills"},
]

# Agentes da Visa
AGENTS = [
    # Orquestrador
    "visa",
    # Time de Descoberta (1-3)
    "visa-etnografo", "visa-estrategista", "visa-coletor",
    # Time de Síntese (4-7)
    "visa-paradigm-advisor", "visa-modelador",
    "visa-data-modeler", "visa-design-system",
    # Time de Spec (8-10)
    "visa-redator", "visa-strategist", "visa-inspector",
    # Time de Handoff (11-12)
    "visa-revisor", "visa-handoff",
    # Utilitário
    "visa-agents-help",
]

# Artefatos esperados em _visa_sdd/ ao final do pipeline (paralelo ao
# expected_legacy_artifacts.yaml do Reversa).
#
# Categorias:
# - required: presença obrigatória (validate retorna != 0 se falta).
# - canonical: subset de required que ADICIONALMENTE deve seguir formato
#   Reversa-compatível (front-matter YAML + IDs BR-FUTURE/AMB-FUTURE).
#   Em modo --strict, validate verifica formato; em modo padrão, apenas presença.
# - optional: presença não obrigatória.
EXPECTED_ARTIFACTS = {
    "required": [
        "landscape.md", "personas-inicial.md", "glossario.md",
        "pains.md", "opportunities.md",
        "domain.md", "flows.md", "architecture.md",
        "business_model.md", "discard_log.md", "ambiguity_log.md",
        "confidence-report.md", "gaps.md", "handoff.md",
    ],
    "canonical": [
        # Artefatos consumidos pelo paridade-guard ≥ 0.3.0.
        # DEVEM ter front-matter YAML com schemaVersion: 1 e kind correto.
        "business_model.md",
        "discard_log.md",
        "ambiguity_log.md",
        "confidence-report.md",
    ],
    "optional": [
        "concorrentes.md", "integrations.md",
        "sdd", "openapi", "user-stories",
        "evidence_plans", "evidence_results", "evidence_scripts",
        "adrs", "traceability/evidence-spec-matrix.md",
        "traceability/pain-spec-matrix.md",
    ],
}

# Mapeamento canonical kind → marcadores esperados no corpo.
# Usado por validate --strict para checagem mínima de formato.
CANONICAL_FORMAT_RULES = {
    "business_model.md": {
        "expected_kind": "target_business_rules",
        # Pelo menos UM dos prefixos deve estar presente para validate --strict
        # passar. O artefato pode ter zero regras (caso degenerado válido) só
        # se o front-matter declarar `total_rules: 0`.
        "id_prefixes": ["BR-FUTURE-", "BR-DESCARTAR-", "BR-HUMANA-"],
    },
    "discard_log.md": {
        "expected_kind": "discard_log",
        "id_prefixes": ["BR-DESCARTAR-"],
    },
    "ambiguity_log.md": {
        "expected_kind": "ambiguity_log",
        "id_prefixes": ["AMB-FUTURE-", "AMB-"],
    },
    "confidence-report.md": {
        "expected_kind": "paradigm_decision",
        "id_prefixes": [],  # paradigm_decision não usa IDs canônicos
    },
}


# ============================================================================
# Resolução de visa_root — onde está o diretório `agents/`
# ============================================================================
#
# A Visa pode ser invocada em 3 cenários diferentes:
#   1. Modo dev: `python3 bin/visa ...` no clone do repo
#      → __file__ = <repo>/bin/visa, agents/ em <repo>/agents/
#   2. Modo pacote instalado via pip: `visa ...` após `pip install visa-sdd`
#      → __file__ = <site-packages>/visa_sdd/cli.py, agents/ vai junto via package_data
#   3. Modo dev via pacote: `python3 -m visa_sdd.cli ...` em editable install
#      → mesmo que (2)
#
# Estratégia: tentar cada cenário em ordem; o primeiro que encontrar `agents/visa/SKILL.md`
# (sentinela) vence.

def _find_visa_root() -> Path:
    """Localiza o diretório que contém `agents/`."""
    here = Path(__file__).resolve()

    # Cenário 1: bin/visa (script standalone) → parent.parent é a raiz
    if here.parent.name == "bin":
        candidate = here.parent.parent
        if (candidate / "agents" / "visa" / "SKILL.md").exists():
            return candidate

    # Cenário 2/3: src/visa_sdd/cli.py
    # Sobe até achar 'agents/visa/SKILL.md'
    for parent in here.parents:
        if (parent / "agents" / "visa" / "SKILL.md").exists():
            return parent

    # Cenário 2 estrito: pacote instalado, agents/ é package_data dentro do pacote
    pkg_dir = here.parent  # <site-packages>/visa_sdd/
    if (pkg_dir / "agents" / "visa" / "SKILL.md").exists():
        return pkg_dir

    raise RuntimeError(
        f"Não consegui localizar o diretório `agents/` da Visa. "
        f"Tentei a partir de: {here}. Reinstale a Visa com `pip install visa-sdd` "
        f"ou clone o repo e rode `python3 bin/visa`."
    )


# ============================================================================
# install
# ============================================================================

def cmd_install(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).resolve()
    visa_root = _find_visa_root()

    print("┌─" + "─" * 60)
    print("│  Visa — Forward Spec Discovery for AI Agents")
    print("│  Espelho à frente do Reversa")
    print("└─" + "─" * 60)
    print()

    # Detectar engines
    detected = _detect_engines(project_root)
    if not detected:
        print("⚠️  Nenhum engine detectado (CLAUDE.md, AGENTS.md, etc.)")
        print("   Vou instalar para Claude Code por padrão.")
        detected = [e for e in ENGINES if e["id"] == "claude-code"]
    else:
        names = ", ".join(e["name"] for e in detected)
        print(f"✅ Engines detectadas: {names}")

    # Diretórios de instalação
    visa_state = project_root / ".visa"
    visa_output = project_root / "_visa_sdd"
    visa_state.mkdir(exist_ok=True)
    visa_output.mkdir(exist_ok=True)
    (visa_state / "context").mkdir(exist_ok=True)

    # Copiar agentes
    created_files: list[str] = []
    for agent in AGENTS:
        src = visa_root / "agents" / agent
        if not src.exists():
            print(f"   ⚠️  Agente fonte não encontrado: {agent}")
            continue
        for engine in detected:
            for skills_dir in {engine["skills_dir"], engine["universal"]}:
                dst = project_root / skills_dir / agent
                dst.parent.mkdir(parents=True, exist_ok=True)
                if dst.exists():
                    continue
                shutil.copytree(src, dst)
                created_files.append(str(dst.relative_to(project_root)))

    # State inicial
    state_path = visa_state / "state.json"
    if not state_path.exists():
        state: dict[str, Any] = {
            "version": VISA_VERSION,
            "project": project_root.name,
            "user_name": "",
            "chat_language": "pt-br",
            "doc_language": "Português",
            "answer_mode": "chat",
            "discovery_level": "essencial",
            "output_folder": "_visa_sdd",
            "phase": None,
            "completed": [],
            "pending": ["imersao", "descoberta", "validacao", "sintese",
                        "geracao", "revisao", "handoff"],
            "engines": [e["id"] for e in detected],
            "agents": AGENTS,
            "checkpoints": {},
            "created_files": created_files,
        }
        state_path.write_text(
            json.dumps(state, indent=2, ensure_ascii=False), encoding="utf-8")

    # Plan inicial
    plan_path = visa_state / "plan.md"
    if not plan_path.exists():
        plan_path.write_text(_initial_plan(project_root.name), encoding="utf-8")

    # Manifest SHA-256 (segue padrão Reversa).
    # IMPORTANTE: created_files lista diretórios (para uninstall); manifest
    # precisa dos arquivos individuais dentro deles para hash.
    manifest = {}
    for rel in created_files:
        full = project_root / rel
        if full.is_file():
            manifest[rel] = hashlib.sha256(full.read_bytes()).hexdigest()
        elif full.is_dir():
            # Hash de cada arquivo dentro do diretório
            for sub in full.rglob("*"):
                if sub.is_file():
                    sub_rel = str(sub.relative_to(project_root))
                    manifest[sub_rel] = hashlib.sha256(sub.read_bytes()).hexdigest()
    manifest_dir = visa_state / "_config"
    manifest_dir.mkdir(exist_ok=True)
    (manifest_dir / "files-manifest.json").write_text(
        json.dumps(manifest, indent=2), encoding="utf-8")

    # Versão
    (visa_state / "version").write_text(VISA_VERSION, encoding="utf-8")

    print()
    print(f"✅ Visa instalada (versão {VISA_VERSION})")
    print(f"   Engines: {', '.join(e['id'] for e in detected)}")
    print(f"   Agentes: {len(AGENTS)}")
    print(f"   Arquivos criados: {len(created_files)}")
    print()
    print("Próximo passo:")
    print("   Abra seu agente de codificação e digite: /visa")
    print()
    return 0


def _detect_engines(project_root: Path) -> list[dict[str, Any]]:
    detected = []
    for engine in ENGINES:
        if (project_root / engine["entry"]).exists():
            detected.append(engine)
    return detected


def _initial_plan(project_name: str) -> str:
    today = datetime.now(timezone.utc).date().isoformat()
    return f"""# Plano de Descoberta — {project_name}

> Criado pela Visa em {today}
> Marque cada tarefa com ✅ quando concluída.
> Você pode editar este plano antes de iniciar.

---

## Fase 1: Imersão 🌎

- [ ] **Etnógrafo** — Brief inicial e mapeamento do domínio
- [ ] **Etnógrafo** — Personas iniciais e jornadas óbvias
- [ ] **Etnógrafo** — Concorrentes e vocabulário do domínio

## Fase 2: Descoberta 🔍

> A Visa preenche esta seção com as jornadas reais após o Etnógrafo concluir.

- [ ] **Estrategista** — Análise das jornadas identificadas

## Fase 3: Validação ✓

- [ ] **Coletor** — Triagem e priorização das LACUNAS abertas
- [ ] **Coletor** — Geração de planos de coleta de evidência
- [ ] **(USUÁRIO)** — Executar coletas no mundo real
- [ ] **Coletor** — Atualizar 🔴 → 🟢/🟡/falseada conforme evidência

## Fase 4: Síntese 🧠

- [ ] **Modelador** — Modelo de domínio do produto
- [ ] **Modelador** — Fluxos principais
- [ ] **Modelador** — Modelo de negócio
- [ ] **Modelador** — Arquitetura conceitual e integrações

## Fase 5: Geração 📝

- [ ] **Redator** — Specs SDD por componente
- [ ] **Redator** — OpenAPI prospectivo (se aplicável)
- [ ] **Redator** — User stories por persona
- [ ] **Redator** — Matrizes de rastreabilidade

## Fase 6: Revisão 🔎

- [ ] **Revisor** — Auditoria de cobertura, confiança e contradições
- [ ] **Revisor** — Geração do confidence-report.md
- [ ] **(USUÁRIO)** — Aprovação para handoff

## Fase 7: Handoff 🤝

- [ ] **Handoff** — Geração de handoff.md
- [ ] **Handoff** — Geração opcional do contrato paridade-guard
- [ ] **Handoff** — Apresentação dos 4 caminhos de implementação
"""


# ============================================================================
# status
# ============================================================================

def cmd_status(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).resolve()
    state_path = project_root / ".visa" / "state.json"

    print("═" * 64)
    print(" Visa — status")
    print("═" * 64)

    if not state_path.exists():
        print(" Estado: ❌ Visa não instalada")
        print("         execute: visa install")
        print("═" * 64)
        return 1

    state = json.loads(state_path.read_text(encoding="utf-8"))

    print(f" Versão:        {state.get('version', '?')}")
    print(f" Projeto:       {state.get('project', '?')}")
    print(f" Nível:         {state.get('discovery_level', '?')}")
    print(f" Fase atual:    {state.get('phase') or '(não iniciada)'}")
    print(f" Concluídas:    {', '.join(state.get('completed', [])) or '(nenhuma)'}")
    print(f" Pendentes:     {', '.join(state.get('pending', [])) or '(nenhuma)'}")
    print()

    output_folder = project_root / state.get("output_folder", "_visa_sdd")
    if output_folder.exists():
        n_files = sum(1 for _ in output_folder.rglob("*.md"))
        print(f" Artefatos:     {n_files} arquivos .md em {output_folder.name}/")

        # Validar artefatos requeridos
        validation = _validate_artifacts(output_folder)
        print(f" Validação:     {validation['present_required']}/{validation['total_required']}"
              f" obrigatórios presentes")
        if validation["missing_required"]:
            print(f"   Faltando: {', '.join(validation['missing_required'][:3])}"
                  f"{'...' if len(validation['missing_required']) > 3 else ''}")
    else:
        print(f" Artefatos:     (pasta {output_folder.name}/ ainda não criada)")

    # Bridge para paridade-guard
    contract_path = project_root / "_visa_sdd" / "parity_audit" / "contract.json"
    if contract_path.exists():
        print(" paridade-guard: ✅ contrato gerado")
    else:
        print(" paridade-guard: ⚪ não conectado")

    print("═" * 64)
    return 0


# ============================================================================
# validate
# ============================================================================

def cmd_validate(args: argparse.Namespace) -> int:
    project_root = Path(args.project_root).resolve()
    output_folder = project_root / "_visa_sdd"

    if not output_folder.exists():
        print(f"❌ {output_folder.name}/ não existe")
        return 1

    strict = getattr(args, "strict", False)
    result = _validate_artifacts(output_folder, strict=strict)

    print("Validação de _visa_sdd/" + (" (modo --strict)" if strict else ""))
    print(f"  Obrigatórios: {result['present_required']}/{result['total_required']}")
    print(f"  Opcionais:    {result['present_optional']}/{result['total_optional']}")
    if strict:
        print(f"  Canônicos válidos: "
              f"{result['canonical_valid']}/{result['canonical_total']}")

    if result["missing_required"]:
        print("\n🛑 Artefatos obrigatórios faltando:")
        for m in result["missing_required"]:
            print(f"   - {m}")
        return 2

    if strict and result["canonical_issues"]:
        print("\n🛑 Artefatos canônicos com formato inválido:")
        for issue in result["canonical_issues"]:
            print(f"   - {issue}")
        print("\nDica: o Redator v1.1+ deve emitir front-matter YAML com "
              "`schemaVersion: 1` e `kind: <correto>`, e os IDs canônicos "
              "devem aparecer como `### BR-FUTURE-NNN` etc.")
        return 3

    if result["present_required"] == result["total_required"]:
        print("\n✅ Todos os artefatos obrigatórios presentes.")
        if strict:
            print("   E todos os canônicos seguem formato Reversa-compatível.")
        if result["missing_optional"]:
            print(f"   ({len(result['missing_optional'])} opcionais ausentes — ok)")
        if not strict:
            print("\nℹ️  Para validar TAMBÉM o formato canônico (front-matter, IDs):")
            print("   visa validate --strict")
        return 0

    return 1


# Regex auxiliares para checagem de formato canônico (mínima, sem PyYAML).
_FRONT_MATTER_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n", re.DOTALL)
_KIND_RE = re.compile(r"^kind\s*:\s*(.+?)\s*$", re.MULTILINE)
_SCHEMA_RE = re.compile(r"^schemaVersion\s*:\s*(\d+)\s*$", re.MULTILINE)


def _check_canonical_format(path: Path, rules: dict[str, Any]) -> list[str]:
    """Verifica formato canônico de um artefato.

    Retorna lista de problemas encontrados (vazia se ok).
    Não usa PyYAML — checagem mínima por regex.
    """
    problems: list[str] = []
    try:
        content = path.read_text(encoding="utf-8")
    except OSError as e:
        return [f"{path.name}: erro de leitura ({e})"]

    fm_match = _FRONT_MATTER_RE.match(content)
    if not fm_match:
        problems.append(f"{path.name}: front-matter YAML ausente "
                        f"(esperado bloco `---` no topo)")
        return problems

    fm_text = fm_match.group(1)
    body = content[fm_match.end():]

    # Verifica schemaVersion
    schema_match = _SCHEMA_RE.search(fm_text)
    if not schema_match:
        problems.append(f"{path.name}: campo `schemaVersion` ausente no front-matter")
    elif schema_match.group(1) != "1":
        problems.append(f"{path.name}: schemaVersion={schema_match.group(1)} "
                        f"(esperado: 1)")

    # Verifica kind
    kind_match = _KIND_RE.search(fm_text)
    if not kind_match:
        problems.append(f"{path.name}: campo `kind` ausente no front-matter")
    elif kind_match.group(1).strip() != rules["expected_kind"]:
        problems.append(f"{path.name}: kind={kind_match.group(1).strip()!r} "
                        f"(esperado: {rules['expected_kind']!r})")

    # Verifica presença de pelo menos um ID canônico (se aplicável).
    # Exceção: paradigm_decision não usa IDs (id_prefixes vazio).
    if rules["id_prefixes"]:
        if not any(prefix in body for prefix in rules["id_prefixes"]):
            problems.append(
                f"{path.name}: nenhum ID canônico encontrado "
                f"({'/'.join(rules['id_prefixes'])}). "
                f"O Redator v1.1+ deve emitir headings `### <PREFIX>NNN`."
            )

    return problems


def _validate_artifacts(output_folder: Path, strict: bool = False) -> dict[str, Any]:
    present_required = []
    missing_required = []
    for art in EXPECTED_ARTIFACTS["required"]:
        if (output_folder / art).exists():
            present_required.append(art)
        else:
            missing_required.append(art)

    present_optional = []
    missing_optional = []
    for art in EXPECTED_ARTIFACTS["optional"]:
        if (output_folder / art).exists():
            present_optional.append(art)
        else:
            missing_optional.append(art)

    # Validação canônica (apenas em --strict, e apenas para artefatos
    # presentes — falta de presença já foi reportada acima).
    canonical_issues: list[str] = []
    canonical_valid = 0
    canonical_total = len(EXPECTED_ARTIFACTS.get("canonical", []))
    if strict:
        for art in EXPECTED_ARTIFACTS.get("canonical", []):
            path = output_folder / art
            if not path.exists():
                continue  # presença já tratada
            rules = CANONICAL_FORMAT_RULES.get(art)
            if rules is None:
                continue
            issues = _check_canonical_format(path, rules)
            if issues:
                canonical_issues.extend(issues)
            else:
                canonical_valid += 1

    return {
        "total_required": len(EXPECTED_ARTIFACTS["required"]),
        "present_required": len(present_required),
        "missing_required": missing_required,
        "total_optional": len(EXPECTED_ARTIFACTS["optional"]),
        "present_optional": len(present_optional),
        "missing_optional": missing_optional,
        "canonical_total": canonical_total,
        "canonical_valid": canonical_valid,
        "canonical_issues": canonical_issues,
    }


# ============================================================================
# Gate computacional do Coletor (v1.2)
# ============================================================================
#
# Premissa: a Visa diferencia-se de geradores de PRD por TRAVAR o pipeline
# em hipóteses sem evidência. Até v1.1.1, isso era convenção de prompt:
# o agente Coletor instruía o LLM a parar, mas o CLI não fazia enforcement.
#
# v1.2: o CLI faz enforcement. Antes de `bridge` prosseguir, checa
# `_visa_sdd/gaps.md` por LACUNAS 🔴 não resolvidas. Para cada uma, exige
# decisão explícita registrada no front-matter ou no corpo:
#
#     ---
#     schemaVersion: 1
#     kind: gaps
#     accepted_risks:
#       - LACUNA-003: pricing-tier — "Aceito risco; validarei pós-MVP"
#       - LACUNA-007: integração-operadora — "Aceito risco; spike de 3 dias"
#     ---
#
# OU dentro do corpo:
#
#     ### LACUNA-003 [RISCO ACEITO]
#     - **Decisor**: Alexandre
#     - **Justificativa**: Validarei após MVP em produção.
#
# Lacunas SEM esse marcador bloqueiam o bridge. Override manual via
# `visa bridge --accept-all-risks "motivo"`.

# Padrões de detecção de LACUNAS no gaps.md
_LACUNA_HEADING_RE = re.compile(
    r"^###\s+(LACUNA-[A-Z0-9-]+)(?:\s+\[(.+?)\])?\s*$",
    re.MULTILINE,
)
_LACUNA_INLINE_RE = re.compile(
    r"🔴\s*(?:LACUNA[-:]\s*)?([A-Z0-9-]+)?",
)
_RISK_ACCEPTED_MARKERS = {"RISCO ACEITO", "RISK ACCEPTED", "ACEITO"}
_RESOLVED_MARKERS = {"RESOLVIDO", "RESOLVED", "VALIDADO", "FALSEADO"}


def _detect_lacunas(gaps_path: Path) -> dict[str, Any]:
    """Detecta LACUNAS em gaps.md e classifica por status.

    Retorna dict com:
      - all: lista de IDs de LACUNAS encontradas
      - pending: LACUNAS sem decisão (bloqueantes)
      - risk_accepted: LACUNAS com risco aceito explícito
      - resolved: LACUNAS resolvidas/validadas/falseadas
      - has_frontmatter_accepted_risks: bool — usuário usou front-matter
    """
    result: dict[str, Any] = {
        "all": [],
        "pending": [],
        "risk_accepted": [],
        "resolved": [],
        "has_frontmatter_accepted_risks": False,
    }
    if not gaps_path.exists():
        return result

    try:
        content = gaps_path.read_text(encoding="utf-8")
    except OSError:
        return result

    # 1. Front-matter: extrair lista accepted_risks: e resolved: se presentes
    fm_match = re.match(r"\A---\s*\n(.*?)\n---\s*\n", content, re.DOTALL)
    accepted_from_fm: set[str] = set()
    resolved_from_fm: set[str] = set()
    body = content
    if fm_match:
        fm_text = fm_match.group(1)
        body = content[fm_match.end():]
        # Match `accepted_risks:` seguido de lista YAML
        for m in re.finditer(r"accepted_risks\s*:\s*\n((?:\s+-\s+.*\n?)+)", fm_text):
            block = m.group(1)
            for line in block.splitlines():
                line = line.strip()
                if line.startswith("-"):
                    # `- LACUNA-003: motivo` ou `- LACUNA-003`
                    item = line[1:].strip()
                    lid = item.split(":")[0].strip()
                    if lid:
                        accepted_from_fm.add(lid)
                        result["has_frontmatter_accepted_risks"] = True
        for m in re.finditer(r"resolved\s*:\s*\n((?:\s+-\s+.*\n?)+)", fm_text):
            block = m.group(1)
            for line in block.splitlines():
                line = line.strip()
                if line.startswith("-"):
                    item = line[1:].strip()
                    lid = item.split(":")[0].strip()
                    if lid:
                        resolved_from_fm.add(lid)

    # 2. Corpo: heading-based LACUNAS
    for m in _LACUNA_HEADING_RE.finditer(body):
        lid = m.group(1)
        marker = (m.group(2) or "").strip().upper() if m.group(2) else ""
        result["all"].append(lid)
        if any(rm in marker for rm in _RISK_ACCEPTED_MARKERS):
            result["risk_accepted"].append(lid)
        elif any(rm in marker for rm in _RESOLVED_MARKERS):
            result["resolved"].append(lid)
        elif lid in accepted_from_fm:
            result["risk_accepted"].append(lid)
        elif lid in resolved_from_fm:
            result["resolved"].append(lid)
        else:
            result["pending"].append(lid)

    # 3. Inline 🔴 sem heading associado: contam como pending genéricas
    # (sem ID, mas indicam presença de LACUNA não resolvida no corpo)
    inline_matches = _LACUNA_INLINE_RE.findall(body)
    if inline_matches and not result["all"]:
        # Pelo menos uma 🔴 inline sem ID estruturado
        result["pending"].append("(LACUNA inline sem ID — estruture com `### LACUNA-NNN`)")
        result["all"].append("(inline)")

    return result


def _check_collector_gate(
    project_root: Path, accept_all: bool, accept_reason: str = ""
) -> tuple[bool, list[str]]:
    """Aplica o gate do Coletor.

    Retorna (allowed, messages) onde:
      - allowed=True: bridge pode prosseguir
      - messages: lista de strings para imprimir (info ou erro)
    """
    gaps_path = project_root / "_visa_sdd" / "gaps.md"
    lacunas = _detect_lacunas(gaps_path)
    msgs: list[str] = []

    total = len(lacunas["all"])
    if total == 0:
        # Sem gaps.md ou sem LACUNAS — pipeline limpo, bridge prossegue
        return True, []

    pending = lacunas["pending"]
    accepted = lacunas["risk_accepted"]
    resolved = lacunas["resolved"]

    msgs.append(
        f"🔍 Gate do Coletor: {total} LACUNA(s) detectada(s) em gaps.md"
    )
    msgs.append(
        f"   ✅ Resolvidas:    {len(resolved)}"
    )
    msgs.append(
        f"   ⚠️  Risco aceito: {len(accepted)}"
    )
    msgs.append(
        f"   🔴 PENDENTES:    {len(pending)}"
    )

    if not pending:
        return True, msgs

    if accept_all:
        msgs.append("")
        msgs.append("⚠️  --accept-all-risks ativado.")
        if accept_reason:
            msgs.append(f"   Motivo: {accept_reason}")
        else:
            msgs.append("   (sem motivo declarado — recomendado usar"
                        " --accept-all-risks=\"motivo\")")
        msgs.append(f"   {len(pending)} LACUNA(s) pendente(s) ignorada(s):")
        for lid in pending[:10]:
            msgs.append(f"     - {lid}")
        if len(pending) > 10:
            msgs.append(f"     ... e mais {len(pending) - 10}")
        return True, msgs

    # Bloqueio
    msgs.append("")
    msgs.append("🛑 BRIDGE BLOQUEADA pelo gate do Coletor.")
    msgs.append("")
    msgs.append(f"   {len(pending)} LACUNA(s) sem decisão explícita:")
    for lid in pending[:10]:
        msgs.append(f"     - {lid}")
    if len(pending) > 10:
        msgs.append(f"     ... e mais {len(pending) - 10}")
    msgs.append("")
    msgs.append("   Para cada LACUNA, escolha UMA das opções:")
    msgs.append("")
    msgs.append("   1) RESOLVER com evidência — atualize a LACUNA no gaps.md:")
    msgs.append("      ### LACUNA-003 [RESOLVIDO]")
    msgs.append("      - **Evidência**: 5/5 entrevistados confirmam")
    msgs.append("")
    msgs.append("   2) ACEITAR RISCO explicitamente — marque no heading:")
    msgs.append("      ### LACUNA-003 [RISCO ACEITO]")
    msgs.append("      - **Decisor**: <nome>")
    msgs.append("      - **Justificativa**: <texto>")
    msgs.append("")
    msgs.append("   3) ACEITAR RISCO via front-matter (em lote):")
    msgs.append("      ---")
    msgs.append("      accepted_risks:")
    msgs.append("        - LACUNA-003: pricing-tier — validarei pós-MVP")
    msgs.append("      ---")
    msgs.append("")
    msgs.append("   4) OVERRIDE manual no comando (com motivo):")
    msgs.append("      visa bridge --accept-all-risks=\"spike de 1 dia\"")
    msgs.append("")
    msgs.append("Por que isto bloqueia: a Visa diferencia-se de geradores de")
    msgs.append("PRD ao recusar avançar com hipóteses não validadas. Se você")
    msgs.append("não quer este gate, use --accept-all-risks ou edite gaps.md.")

    return False, msgs


# ============================================================================
# bridge — valida formato canônico + aplica gate do Coletor + cria stub
# ============================================================================

def cmd_bridge(args: argparse.Namespace) -> int:
    """Conecta Visa ao paridade-guard SEM cópia cosmética.

    A v1.0.0 fazia bridge copiando arquivos para `_reversa_sdd/migration/`,
    o que era enganador: os arquivos da Visa NÃO seguem o formato canônico
    `### BR-MIGRAR-NNN` que o extractor do paridade-guard espera. Resultado:
    o contrato saía com 1 cláusula sintética em vez das regras reais.

    A v1.1.0 trabalha em duas etapas:

    1. **Validar formato canônico**: verifica que `business_model.md`,
       `discard_log.md`, `ambiguity_log.md` (artefatos do Redator) têm
       front-matter Reversa-compatível e IDs `BR-FUTURE-NNN`/`AMB-FUTURE-NNN`.
       Se não tiverem, aborta — o pipeline da Visa não rodou até o Redator
       v1.1+ ou esses arquivos foram editados manualmente fora do formato.

    2. **Apontar paridade-guard direto para _visa_sdd**: cria um stub
       `_visa_sdd/migration/` com symlinks (ou cópias quando symlinks não
       são suportados) dos artefatos canônicos. Isso permite invocar
       `paridade-guard contract --project-root .` apontando direto para
       o output da Visa, sem renomear arquivos.

    Pré-requisito: paridade-guard ≥ 0.3.0 (com extractor forward).
    """
    project_root = Path(args.project_root).resolve()
    visa_dir = project_root / "_visa_sdd"

    if not visa_dir.exists():
        print(f"❌ {visa_dir} não existe. Execute a Visa primeiro.")
        return 1

    print("🌉 Conectando Visa ao paridade-guard")
    print(f"   Origem: {visa_dir}")
    print()

    # ============================================================================
    # Etapa 0: GATE DO COLETOR (v1.2)
    # ============================================================================
    accept_all = getattr(args, "accept_all_risks", None) is not None
    accept_reason = getattr(args, "accept_all_risks", "") or ""
    if not getattr(args, "skip_collector_gate", False):
        allowed, gate_msgs = _check_collector_gate(
            project_root, accept_all, accept_reason
        )
        for msg in gate_msgs:
            print(msg)
        if gate_msgs:
            print()
        if not allowed:
            return 4  # exit code dedicado para o gate
    else:
        print("⚠️  --skip-collector-gate ativado (use com cautela).")
        print()

    # ============================================================================
    # Etapa 1: validar artefatos canônicos
    # ============================================================================
    canonical_artifacts = {
        "business_model.md": "target_business_rules",
        "discard_log.md": "discard_log",
        "ambiguity_log.md": "ambiguity_log",
        "confidence-report.md": "paradigm_decision",
    }

    issues = []
    found = []
    for fname, expected_kind in canonical_artifacts.items():
        path = visa_dir / fname
        if not path.exists():
            issues.append(f"❌ {fname} não existe")
            continue

        content = path.read_text(encoding="utf-8")

        # Verifica front-matter
        if not content.startswith("---\n"):
            issues.append(
                f"⚠️  {fname}: sem front-matter YAML "
                f"(o paridade-guard tolera, mas o Redator v1.1+ deveria emitir)"
            )

        # Verifica presença de pelo menos um ID canônico (exceto paradigm_decision)
        if expected_kind != "paradigm_decision":
            expected_prefixes = {
                "target_business_rules": ["BR-FUTURE-", "BR-DESCARTAR-", "BR-HUMANA-"],
                "discard_log": ["BR-DESCARTAR-"],
                "ambiguity_log": ["AMB-FUTURE-", "AMB-"],
            }
            prefixes = expected_prefixes.get(expected_kind, [])
            if prefixes and not any(p in content for p in prefixes):
                issues.append(
                    f"⚠️  {fname}: nenhum ID canônico encontrado "
                    f"({'/'.join(prefixes)}). Provavelmente o Redator não rodou"
                    f" no formato v1.1+ — a ponte vai gerar contrato vazio."
                )
            else:
                found.append(fname)
        else:
            found.append(fname)

    if issues:
        print("Problemas detectados:")
        for issue in issues:
            print(f"   {issue}")
        print()

    if not found:
        print("🛑 Nenhum artefato canônico válido encontrado. Abortando bridge.")
        print("   Execute o pipeline da Visa até o Redator (fase 'geracao')")
        print("   e garanta que os artefatos seguem o formato v1.1+.")
        return 2

    # ============================================================================
    # Etapa 2: criar stub de migration_dir apontando para _visa_sdd
    # ============================================================================
    migration_stub = visa_dir / "migration"
    migration_stub.mkdir(exist_ok=True)

    bridged = 0
    for fname in canonical_artifacts:
        src = visa_dir / fname
        if not src.exists():
            continue
        dst_name_map = {
            "business_model.md": "target_business_rules.md",
            "discard_log.md": "discard_log.md",
            "ambiguity_log.md": "ambiguity_log.md",
            "confidence-report.md": "paradigm_decision.md",
        }
        dst = migration_stub / dst_name_map[fname]
        if dst.exists() or dst.is_symlink():
            dst.unlink()
        try:
            dst.symlink_to(src.resolve())
            bridged += 1
            print(f"   ✅ {fname} → migration/{dst.name} (symlink)")
        except (OSError, NotImplementedError):
            # Fallback: cópia (Windows sem privilégios)
            import shutil as _shutil
            _shutil.copy2(src, dst)
            bridged += 1
            print(f"   ✅ {fname} → migration/{dst.name} (cópia)")

    print()
    print(f"Ponte construída: {bridged} arquivos em {migration_stub.relative_to(project_root)}/")
    print()
    print("Próximos passos:")
    print("   1. paridade-guard contract \\")
    print("        --migration-dir _visa_sdd/migration \\")
    print("        --output _visa_sdd/parity_audit/contract.json")
    print("      (extractor v0.3+ entende BR-FUTURE-NNN e AMB-FUTURE-NNN)")
    print("   2. Inspecione _visa_sdd/parity_audit/contract.json")
    print("   3. paridade-guard install --pre-commit")
    print()
    print("ℹ️  paridade-guard ≥ 0.3.0 reconhece artefatos forward nativamente.")
    print("    Versões anteriores tratam BR-FUTURE como prefixo desconhecido")
    print("    e geram contrato vazio — atualize antes.")

    return 0


# ============================================================================
# uninstall
# ============================================================================

def cmd_uninstall(args: argparse.Namespace) -> int:
    """Remove skills/state da Visa do projeto.

    PRESERVA `_visa_sdd/` por padrão — esse é o output de descoberta do
    usuário, não da Visa. Para remover também `_visa_sdd/`, use --purge.
    """
    project_root = Path(args.project_root).resolve()
    state_dir = project_root / ".visa"

    if not state_dir.exists():
        print(f"⚪ Visa não está instalada em {project_root} (nada a remover).")
        return 0

    state_path = state_dir / "state.json"
    created_files: list[str] = []
    if state_path.exists():
        try:
            state = json.loads(state_path.read_text(encoding="utf-8"))
            created_files = state.get("created_files", [])
        except (json.JSONDecodeError, OSError):
            print("⚠️  Não consegui ler state.json — vou remover só o que conheço.")

    print("┌─" + "─" * 60)
    print("│  Visa — uninstall")
    print("└─" + "─" * 60)
    print()

    # Confirmação interativa, exceto se --yes
    if not args.yes:
        print("Vou remover:")
        print(f"  - {state_dir.relative_to(project_root)}/ (state, plan, manifest)")
        print(f"  - {len(created_files)} skills instaladas em "
              f".claude/skills/ e/ou .agents/skills/")
        if args.purge:
            print("  - _visa_sdd/ (output de descoberta) — POR CAUSA DE --purge")
        else:
            print("  PRESERVO: _visa_sdd/ (output de descoberta)")
        print()
        try:
            answer = input("Confirma? [y/N]: ").strip().lower()
        except (EOFError, KeyboardInterrupt):
            print("\nAbortado.")
            return 1
        if answer not in ("y", "yes", "s", "sim"):
            print("Abortado.")
            return 1

    removed_count = 0

    # 1. Remover skills (created_files)
    for rel in created_files:
        full = project_root / rel
        if full.is_symlink() or full.is_file():
            try:
                full.unlink()
                removed_count += 1
            except OSError as e:
                print(f"   ⚠️  falha ao remover {rel}: {e}")
        elif full.is_dir():
            try:
                shutil.rmtree(full)
                removed_count += 1
            except OSError as e:
                print(f"   ⚠️  falha ao remover {rel}: {e}")

    # 2. Limpar pastas .claude/skills/ e .agents/skills/ se ficaram vazias
    for skill_root in [".claude/skills", ".agents/skills"]:
        path = project_root / skill_root
        if path.exists() and not any(path.iterdir()):
            path.rmdir()
            # E também o pai, se ficou vazio
            parent = path.parent
            if parent.exists() and parent.name in (".claude", ".agents") and not any(parent.iterdir()):
                parent.rmdir()

    # 3. Remover .visa/
    try:
        shutil.rmtree(state_dir)
    except OSError as e:
        print(f"⚠️  falha ao remover {state_dir}: {e}")
        return 2

    # 4. Remover _visa_sdd/ apenas se --purge
    visa_sdd = project_root / "_visa_sdd"
    if args.purge and visa_sdd.exists():
        shutil.rmtree(visa_sdd)
        print("✅ _visa_sdd/ removido (--purge).")

    print()
    print(f"✅ Visa desinstalada: {removed_count} arquivos/pastas de skills + .visa/")
    if not args.purge and visa_sdd.exists():
        print(f"   _visa_sdd/ preservado em {visa_sdd.relative_to(project_root)}/")
        print("   Para remover também: visa uninstall --purge")
    return 0


# ============================================================================
# Roteamento
# ============================================================================

def main() -> int:
    parser = argparse.ArgumentParser(
        prog="visa",
        description="Visa — descoberta de produto via pipeline de agentes especializados",
    )
    parser.add_argument("--project-root", default=".",
                        help="Raiz do projeto (default: cwd)")
    parser.add_argument("--version", action="version",
                        version=f"visa {VISA_VERSION}")

    sub = parser.add_subparsers(dest="command", required=True)

    p_install = sub.add_parser("install", help="Instala skills da Visa no projeto")
    p_install.set_defaults(func=cmd_install)

    p_status = sub.add_parser("status", help="Mostra estado atual da descoberta")
    p_status.set_defaults(func=cmd_status)

    p_validate = sub.add_parser("validate", help="Valida artefatos esperados")
    p_validate.add_argument("--strict", action="store_true",
                            help="Valida também formato canônico (front-matter, IDs)")
    p_validate.set_defaults(func=cmd_validate)

    p_bridge = sub.add_parser("bridge",
                              help="Constrói ponte para paridade-guard ≥ 0.3.0")
    p_bridge.add_argument(
        "--accept-all-risks",
        nargs="?",
        const="(motivo não declarado)",
        default=None,
        metavar="MOTIVO",
        help="Aceita TODAS as LACUNAs 🔴 pendentes em gaps.md sem decisão "
             "explícita. Recomendado: --accept-all-risks=\"motivo\" para deixar "
             "rastro do override.",
    )
    p_bridge.add_argument(
        "--skip-collector-gate",
        action="store_true",
        help="Ignora completamente o gate do Coletor (não recomendado).",
    )
    p_bridge.set_defaults(func=cmd_bridge)

    p_uninstall = sub.add_parser("uninstall",
                                 help="Remove skills/state da Visa (preserva _visa_sdd/)")
    p_uninstall.add_argument("--yes", "-y", action="store_true",
                             help="Não pergunta confirmação")
    p_uninstall.add_argument("--purge", action="store_true",
                             help="Também remove _visa_sdd/ (output de descoberta)")
    p_uninstall.set_defaults(func=cmd_uninstall)

    args = parser.parse_args()
    result: int = args.func(args)
    return result


if __name__ == "__main__":
    sys.exit(main())
