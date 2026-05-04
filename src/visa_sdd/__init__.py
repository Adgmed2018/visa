"""visa-sdd — Forward Spec Discovery for AI Agents.

Espelho à frente do Reversa: descoberta de produto via pipeline de 8 agentes
especializados (skills .md), com saída canônica consumível pelo paridade-guard.
"""

from __future__ import annotations

__version__ = "1.4.0"

# Exports públicos
from .exceptions import (
    AgentNotFoundError,
    AlreadyInstalledError,
    ArtifactFormatError,
    ArtifactNotFoundError,
    BridgeError,
    BridgeIncompleteError,
    CanonicalFormatError,
    CollectorGateError,
    FileSystemError,
    LacunaNotResolvedError,
    ManifestError,
    ManifestMismatchError,
    NotInstalledError,
    ParidadeGuardNotAvailableError,
    PathNotFoundError,
    PathPermissionError,
    SchemaVersionError,
    SkillsCopyError,
    StateCorruptedError,
    StateVersionError,
    SymlinkError,
    UninstallError,
    VisaException,
    handle_exception,
)
from .logging import (
    LogLevel,
    Spinner,
    VisaLogger,
    box_draw,
    error_output,
    get_logger,
    info,
    progress,
    set_quiet,
    set_structured,
    set_verbosity,
    spinner,
    success,
    warning,
)
