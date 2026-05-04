"""
Logging estruturado para a Visa.

Este módulo implementa logging estruturado sem dependências externas,
usando apenas Python stdlib.

Formato de output:
    [LEVEL] timestamp | logger_name | message | extra_field=value

Uso:
    from visa_sdd.logging import get_logger, set_verbosity

    logger = get_logger("visa.install")
    logger.info("Installing skills", engine="claude-code", count=14)
    logger.warning("Engine not detected", path="/path/to/CLAUDE.md")
    logger.error("Installation failed", error="FileNotFoundError")
"""

from __future__ import annotations

import json
import os
import sys
from datetime import datetime, timezone
from enum import Enum
from pathlib import Path
from typing import Any


class LogLevel(Enum):
    """Níveis de log."""
    DEBUG = 0
    INFO = 1
    WARNING = 2
    ERROR = 3
    CRITICAL = 4

    def __str__(self) -> str:
        return self.name


# Configuração global
_G_LOG_LEVEL = LogLevel.INFO
_G_STRUCTURED = False  # JSON output quando True
_G QUIET = False


def set_verbosity(level: int) -> None:
    """Define nível de verbosidade.
    
    Args:
        level: 0=DEBUG, 1=INFO, 2=WARNING, 3=ERROR
    """
    global _G_LOG_LEVEL
    levels = [LogLevel.DEBUG, LogLevel.INFO, LogLevel.WARNING, LogLevel.ERROR, LogLevel.CRITICAL]
    _G_LOG_LEVEL = levels[min(level, len(levels) - 1)]


def set_quiet(quiet: bool) -> None:
    """Ativa modo quieto (suprime output não-essencial)."""
    global _G_QUIET
    _G_QUIET = quiet


def set_structured(structured: bool) -> None:
    """Ativa output JSON estruturado."""
    global _G_STRUCTURED
    _G_STRUCTURED = structured


def _get_timestamp() -> str:
    """Retorna timestamp ISO-8601."""
    return datetime.now(timezone.utc).isoformat(timespec="milliseconds")


def _format_message(level: LogLevel, logger_name: str, message: str, **extra: Any) -> str:
    """Formata mensagem de log."""
    timestamp = _get_timestamp()
    
    if extra:
        extra_str = " | " + " | ".join(f"{k}={_format_value(v)}" for k, v in extra.items())
    else:
        extra_str = ""
    
    return f"[{level.name:8}] {timestamp} | {logger_name:20} | {message}{extra_str}"


def _format_value(value: Any) -> str:
    """Formata valor para output."""
    if isinstance(value, Path):
        return str(value)
    if isinstance(value, (list, tuple)):
        return ", ".join(str(v) for v in value)
    if isinstance(value, dict):
        return json.dumps(value)
    return str(value)


def _should_log(level: LogLevel) -> bool:
    """Verifica se deve fazer log baseado no nível."""
    return level.value >= _G_LOG_LEVEL.value


class VisaLogger:
    """Logger estruturado para a Visa."""
    
    def __init__(self, name: str) -> None:
        self.name = name
        self._extra: dict[str, Any] = {}
    
    def _log(self, level: LogLevel, message: str, **extra: Any) -> None:
        """Log interno."""
        if _G_QUIET and level.value >= LogLevel.WARNING.value:
            # Em modo quieto, Warning+ ainda aparecem
            pass
        
        if not _should_log(level):
            return
        
        # Merge extra
        merged_extra = {**self._extra, **extra}
        
        if _G_STRUCTURED:
            output = self._format_json(level, message, merged_extra)
        else:
            output = _format_message(level, self.name, message, **merged_extra)
        
        # Output para stderr (não stdout, para não poluir output do CLI)
        sys.stderr.write(output + "\n")
        sys.stderr.flush()
    
    def _format_json(self, level: LogLevel, message: str, extra: dict[str, Any]) -> str:
        """Formata output JSON estruturado."""
        record = {
            "level": level.name,
            "timestamp": _get_timestamp(),
            "logger": self.name,
            "message": message,
            **extra
        }
        return json.dumps(record, ensure_ascii=False)
    
    def debug(self, message: str, **extra: Any) -> None:
        """Log debug."""
        self._log(LogLevel.DEBUG, message, **extra)
    
    def info(self, message: str, **extra: Any) -> None:
        """Log info."""
        self._log(LogLevel.INFO, message, **extra)
    
    def warning(self, message: str, **extra: Any) -> None:
        """Log warning."""
        self._log(LogLevel.WARNING, message, **extra)
    
    def warn(self, message: str, **extra: Any) -> None:
        """Alias para warning."""
        self.warning(message, **extra)
    
    def error(self, message: str, **extra: Any) -> None:
        """Log error."""
        self._log(LogLevel.ERROR, message, **extra)
    
    def critical(self, message: str, **extra: Any) -> None:
        """Log critical."""
        self._log(LogLevel.CRITICAL, message, **extra)
    
    def with_extra(self, **extra: Any) -> "VisaLogger":
        """Retorna novo logger com extra fields."""
        new_logger = VisaLogger(self.name)
        new_logger._extra = {**self._extra, **extra}
        return new_logger


# Cache de loggers
_LOGGERS: dict[str, VisaLogger] = {}


def get_logger(name: str) -> VisaLogger:
    """Obtém logger pelo nome."""
    if name not in _LOGGERS:
        _LOGGERS[name] = VisaLogger(name)
    return _LOGGERS[name]


# =============================================================================
# Error Classes
# =============================================================================

class VisaError(Exception):
    """Erro base da Visa."""
    
    code: str = "ERR_VISA"
    
    def __init__(self, message: str, **extra: Any) -> None:
        super().__init__(message)
        self.message = message
        self.extra = extra
        self._log()
    
    def _log(self) -> None:
        """Log o erro."""
        logger = get_logger("visa.error")
        logger.error(self.message, code=self.code, **self.extra)
    
    def to_dict(self) -> dict[str, Any]:
        """Converte para dict (para output estruturado)."""
        return {
            "error": self.__class__.__name__,
            "code": self.code,
            "message": self.message,
            **self.extra
        }


class VisaNotInstalledError(VisaError):
    """Visa não está instalada no projeto."""
    
    code = "ERR_NOT_INSTALLED"


class VisaArtifactNotFoundError(VisaError):
    """Artefato não encontrado."""
    
    code = "ERR_ARTIFACT_NOT_FOUND"


class VisaValidationError(VisaError):
    """Erro de validação de artefato."""
    
    code = "ERR_VALIDATION"


class VisaCollectorGateError(VisaError):
    """Gate do coletor bloqueou o pipeline."""
    
    code = "ERR_COLLECTOR_GATE"


class VisaBridgeError(VisaError):
    """Erro durante o bridge."""
    
    code = "ERR_BRIDGE"


class VisaSymlinkError(VisaError):
    """Erro ao criar symlink."""
    
    code = "ERR_SYMLINK"


# =============================================================================
# Progress / Status output
# =============================================================================

def progress(current: int, total: int, message: str = "") -> None:
    """Output de progresso para operações longas."""
    if _G_QUIET:
        return
    
    percent = (current / total * 100) if total > 0 else 0
    bar = "█" * int(percent / 5) + "░" * (20 - int(percent / 5))
    
    sys.stderr.write(f"\r[{bar}] {percent:3.0f}% | {message}    ")
    sys.stderr.flush()
    
    if current >= total:
        sys.stderr.write("\n")
        sys.stderr.flush()


def spinner(message: str = "") -> "Spinner":
    """Retorna um spinner para animations."""
    return Spinner(message)


class Spinner:
    """Spinner animado simples."""
    
    def __init__(self, message: str = "") -> None:
        self.message = message
        self._running = False
        self._frames = ["⠋", "⠙", "⠹", "⠸", "⠼", "⠴", "⠦", "⠧", "⠇", "⠏"]
        self._index = 0
    
    def start(self) -> None:
        """Inicia o spinner."""
        self._running = True
        self._update()
    
    def stop(self) -> None:
        """Para o spinner."""
        self._running = False
        sys.stderr.write("\r" + " " * (len(self.message) + 20) + "\r")
        sys.stderr.flush()
    
    def _update(self) -> None:
        """Atualiza o spinner."""
        if not self._running:
            return
        
        frame = self._frames[self._index % len(self._frames)]
        sys.stderr.write(f"\r{frame} {self.message}")
        sys.stderr.flush()
        
        self._index += 1


# =============================================================================
# Banner / Box drawing
# =============================================================================

def box_draw(title: str, lines: list[str], width: int = 64) -> str:
    """Desenha uma box com título.
    
    Args:
        title: Título da box
        lines: Linhas de conteúdo
        width: Largura total
    
    Returns:
        String formatada com box
    """
    output: list[str] = []
    
    # Corner
    output.append("┌" + "─" * (width - 2) + "┐")
    
    # Title
    if title:
        title_line = f"│  {title.center(width - 4)}  │"
        output.append(title_line)
        output.append("├" + "─" * (width - 2) + "┤")
    
    # Content
    for line in lines:
        if len(line) > width - 4:
            line = line[:width - 7] + "..."
        output.append(f"│  {line.ljust(width - 4)}  │")
    
    # Bottom
    output.append("└" + "─" * (width - 2) + "┘")
    
    return "\n".join(output)


def success(message: str) -> None:
    """Output de sucesso (verde no terminal)."""
    if _G_QUIET:
        return
    sys.stderr.write(f"\033[92m✅ {message}\033[0m\n")
    sys.stderr.flush()


def warning(message: str) -> None:
    """Output de warning (amarelo no terminal)."""
    if _G_QUIET:
        return
    sys.stderr.write(f"\033[93m⚠️  {message}\033[0m\n")
    sys.stderr.flush()


def error_output(message: str) -> None:
    """Output de erro (vermelho no terminal)."""
    sys.stderr.write(f"\033[91m❌ {message}\033[0m\n")
    sys.stderr.flush()


def info(message: str) -> None:
    """Output de info (azul no terminal)."""
    if _G_QUIET:
        return
    sys.stderr.write(f"\033[94mℹ️  {message}\033[0m\n")
    sys.stderr.flush()
