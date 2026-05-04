"""visa-sdd — Forward Spec Discovery for AI Agents.

Espelho à frente do Reversa: descoberta de produto via pipeline de 8 agentes
especializados (skills .md), com saída canônica consumível pelo paridade-guard.
"""

from __future__ import annotations

__version__ = "1.3.0"

# Exports públicos
from .exceptions import (
    VisaException,
    NotInstalledError,
    AlreadyInstalledError,
    AgentNotFoundError,
    SkillsCopyError,
    ArtifactNotFoundError,
    ArtifactFormatError,
    CanonicalFormatError,
    SchemaVersionError,
    CollectorGateError,
    LacunaNotResolvedError,
    BridgeError,
    BridgeIncompleteError,
    SymlinkError,
    ParidadeGuardNotAvailableError,
    UninstallError,
    StateCorruptedError,
    StateVersionError,
    FileSystemError,
    PathPermissionError,
    PathNotFoundError,
    ManifestError,
    ManifestMismatchError,
    handle_exception,
)

from .logging import (
    get_logger,
    set_verbosity,
    set_quiet,
    set_structured,
    VisaLogger,
    progress,
    spinner,
    Spinner,
    box_draw,
    success,
    warning,
    error_output,
    info,
    LogLevel,
)
