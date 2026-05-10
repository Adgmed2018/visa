"""Telemetria opt-in da Visa.

PRIVACIDADE FIRST:
- DESLIGADA por padrao. Ninguem e rastreado sem opt-in explicito.
- Nenhum dado de conteudo (specs, codigo, nomes de projeto) e enviado.
- So eventos contados (install, validate, bridge, doctor, upgrade) + versao da Visa + engine usada.
- Pode ser desligada a qualquer momento via env `VISA_TELEMETRY=off` ou `visa telemetry off`.
- Endpoint nao foi configurado por default — o opt-in registra localmente em `.visa/telemetry.jsonl`.
  Para enviar para servidor proprio, defina `VISA_TELEMETRY_ENDPOINT=https://...`

Conformidade LGPD/GDPR:
- Identificador: hash sha256 anonimo da combinacao MAC+username (nunca enviado em claro).
- Direito ao esquecimento: `visa telemetry purge` apaga tudo localmente.
- Sem cookies, sem fingerprinting de browser (CLI nao e browser).

Introducido em v1.6.0 (P4).
"""
from __future__ import annotations

import hashlib
import json
import os
import platform
import sys
import time
import uuid
from pathlib import Path
from typing import Any

TELEMETRY_VERSION = "1"
LOCAL_LOG_NAME = "telemetry.jsonl"
OPT_IN_FILENAME = "telemetry-optin.json"


def _is_enabled(project_root: Path) -> bool:
    """Telemetria so roda se opt-in foi explicito E env nao desabilitou."""
    if os.environ.get("VISA_TELEMETRY", "").lower() in ("off", "0", "no", "false"):
        return False
    optin = project_root / ".visa" / OPT_IN_FILENAME
    if not optin.exists():
        return False
    try:
        data = json.loads(optin.read_text(encoding="utf-8"))
        return bool(data.get("opted_in"))
    except (OSError, json.JSONDecodeError):
        return False


def _anon_id() -> str:
    """Identificador anonimo: hash de MAC+username. Nunca exporta o claro."""
    raw = f"{uuid.getnode()}-{os.environ.get('USER', 'unknown')}".encode()
    return hashlib.sha256(raw).hexdigest()[:16]


def opt_in(project_root: Path) -> None:
    """Registra opt-in explicito para este projeto."""
    visa_dir = project_root / ".visa"
    visa_dir.mkdir(parents=True, exist_ok=True)
    optin = visa_dir / OPT_IN_FILENAME
    optin.write_text(json.dumps({
        "opted_in": True,
        "opted_in_at": int(time.time()),
        "telemetry_version": TELEMETRY_VERSION,
        "anon_id": _anon_id(),
    }, indent=2), encoding="utf-8")


def opt_out(project_root: Path) -> None:
    """Desliga telemetria neste projeto."""
    optin = project_root / ".visa" / OPT_IN_FILENAME
    if optin.exists():
        optin.unlink()


def purge(project_root: Path) -> int:
    """Apaga TODO log de telemetria local (LGPD direito ao esquecimento)."""
    log = project_root / ".visa" / LOCAL_LOG_NAME
    optin = project_root / ".visa" / OPT_IN_FILENAME
    n = 0
    for f in (log, optin):
        if f.exists():
            f.unlink()
            n += 1
    return n


def emit(project_root: Path, event: str, **props: Any) -> None:
    """Registra evento de telemetria. No-op se opt-in desligado."""
    if not _is_enabled(project_root):
        return
    record: dict[str, Any] = {
        "ts": int(time.time()),
        "event": event,
        "anon_id": _anon_id(),
        "telemetry_version": TELEMETRY_VERSION,
        "visa_version": props.pop("visa_version", "unknown"),
        "python_version": f"{sys.version_info.major}.{sys.version_info.minor}",
        "platform": platform.system().lower(),
        **props,
    }
    log = project_root / ".visa" / LOCAL_LOG_NAME
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as f:
        f.write(json.dumps(record, ensure_ascii=False) + "\n")

    # Envio remoto opcional
    endpoint = os.environ.get("VISA_TELEMETRY_ENDPOINT", "").strip()
    if endpoint:
        try:
            import urllib.request
            req = urllib.request.Request(
                endpoint,
                data=json.dumps(record).encode("utf-8"),
                headers={"Content-Type": "application/json"},
                method="POST",
            )
            urllib.request.urlopen(req, timeout=2)
        except Exception:
            pass
