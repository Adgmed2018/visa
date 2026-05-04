"""
Visa exceptions — error classes para erros específicos.

Este módulo define exceções customizadas para diferentes tipos de erro
na Visa, cada uma com código de erro correspondente.
"""

from __future__ import annotations

from typing import Any


class VisaException(Exception):
    """Base exception para todos os erros da Visa."""
    
    # Exit code associado ao erro
    exit_code: int = 1
    
    # Código interno do erro
    code: str = "ERR_VISA"
    
    def __init__(
        self,
        message: str,
        *,
        context: dict[str, Any] | None = None,
        hint: str | None = None,
    ) -> None:
        """
        Args:
            message: Mensagem descritiva do erro
            context: Contexto adicional (paths, IDs, etc.)
            hint: Dica para o usuário resolver o erro
        """
        super().__init__(message)
        self.message = message
        self.context = context or {}
        self.hint = hint
    
    def __str__(self) -> str:
        parts = [self.message]
        if self.context:
            parts.append(f"Context: {self.context}")
        if self.hint:
            parts.append(f"Hint: {self.hint}")
        return "\n".join(parts)
    
    def to_dict(self) -> dict[str, Any]:
        """Serializa para dict (para output JSON)."""
        return {
            "error": self.__class__.__name__,
            "code": self.code,
            "message": self.message,
            "context": self.context,
            "hint": self.hint,
            "exit_code": self.exit_code,
        }


# =============================================================================
# Installation Errors
# =============================================================================

class NotInstalledError(VisaException):
    """Visa não está instalada no projeto."""
    
    code = "ERR_NOT_INSTALLED"
    exit_code = 1
    
    def __init__(
        self,
        project_root: str,
        *,
        hint: str | None = "Execute 'visa install' para instalar",
    ) -> None:
        super().__init__(
            f"Visa não está instalada em {project_root}",
            context={"project_root": project_root},
            hint=hint,
        )


class AlreadyInstalledError(VisaException):
    """Visa já está instalada."""
    
    code = "ERR_ALREADY_INSTALLED"
    exit_code = 1


class AgentNotFoundError(VisaException):
    """Agente não encontrado."""
    
    code = "ERR_AGENT_NOT_FOUND"
    exit_code = 1


class SkillsCopyError(VisaException):
    """Erro ao copiar skills."""
    
    code = "ERR_SKILLS_COPY"
    exit_code = 2


# =============================================================================
# Validation Errors
# =============================================================================

class ArtifactNotFoundError(VisaException):
    """Artefato obrigatório não encontrado."""
    
    code = "ERR_ARTIFACT_NOT_FOUND"
    exit_code = 2
    
    def __init__(
        self,
        artifact: str,
        *,
        hint: str | None = None,
    ) -> None:
        super().__init__(
            f"Artefato obrigatório não encontrado: {artifact}",
            context={"artifact": artifact},
            hint=hint or "Execute o pipeline de descoberta até a fase correspondente",
        )


class ArtifactFormatError(VisaException):
    """Artefato com formato inválido."""
    
    code = "ERR_ARTIFACT_FORMAT"
    exit_code = 3
    
    def __init__(
        self,
        artifact: str,
        issue: str,
        *,
        hint: str | None = "Verifique o front-matter YAML e IDs canônicos",
    ) -> None:
        super().__init__(
            f"Formato inválido em {artifact}: {issue}",
            context={"artifact": artifact, "issue": issue},
            hint=hint,
        )


class CanonicalFormatError(VisaException):
    """Artefato canônico não segue formato esperado."""
    
    code = "ERR_CANONICAL_FORMAT"
    exit_code = 3
    
    def __init__(
        self,
        artifact: str,
        expected_kind: str,
        actual_kind: str | None,
        *,
        hint: str | None = None,
    ) -> None:
        hint = hint or (
            f"O front-matter deve ter 'kind: {expected_kind}'. "
            "O Redator v1.1+ deve emitir front-matter correto."
        )
        super().__init__(
            f"{artifact}: kind={actual_kind or 'ausente'} (esperado: {expected_kind})",
            context={
                "artifact": artifact,
                "expected_kind": expected_kind,
                "actual_kind": actual_kind,
            },
            hint=hint,
        )


class SchemaVersionError(VisaException):
    """Versão de schema incompatível."""
    
    code = "ERR_SCHEMA_VERSION"
    exit_code = 3


# =============================================================================
# Collector Gate Errors
# =============================================================================

class CollectorGateError(VisaException):
    """Gate do coletor bloqueou o pipeline."""
    
    code = "ERR_COLLECTOR_GATE"
    exit_code = 4
    
    def __init__(
        self,
        lacunas: list[str],
        *,
        hint: str | None = None,
    ) -> None:
        super().__init__(
            f"Gate bloqueado: {len(lacunas)} LACUNA(s) pendente(s)",
            context={"lacunas": lacunas, "count": len(lacunas)},
            hint=hint or (
                "Para cada LACUNA, resolva com evidência ou marque [RISCO ACEITO] "
                "ou use --accept-all-risks='motivo' para override"
            ),
        )


class LacunaNotResolvedError(VisaException):
    """LACUNA específica não resolvida."""
    
    code = "ERR_LACUNA_NOT_RESOLVED"
    exit_code = 4


# =============================================================================
# Bridge Errors
# =============================================================================

class BridgeError(VisaException):
    """Erro durante operação de bridge."""
    
    code = "ERR_BRIDGE"
    exit_code = 2


class BridgeIncompleteError(VisaException):
    """Pipeline incompleto para bridge."""
    
    code = "ERR_BRIDGE_INCOMPLETE"
    exit_code = 2
    
    def __init__(
        self,
        missing: list[str],
        *,
        hint: str | None = None,
    ) -> None:
        super().__init__(
            f"Pipeline incompleto: artefatos canônicos faltando",
            context={"missing_artifacts": missing},
            hint=hint or "Execute o pipeline da Visa até o Redator (fase 'geracao')",
        )


class SymlinkError(VisaException):
    """Erro ao criar symlink."""
    
    code = "ERR_SYMLINK"
    exit_code = 2


class ParidadeGuardNotAvailableError(VisaException):
    """paridade-guard não está instalado."""
    
    code = "ERR_PARIDADE_GUARD"
    exit_code = 2
    
    def __init__(
        self,
        *,
        hint: str | None = "Execute 'pip install paridade-guard>=0.3.0' para instalar",
    ) -> None:
        super().__init__(
            "paridade-guard não está disponível",
            hint=hint,
        )


# =============================================================================
# Uninstall Errors
# =============================================================================

class UninstallError(VisaException):
    """Erro durante desinstalação."""
    
    code = "ERR_UNINSTALL"
    exit_code = 2


# =============================================================================
# State Errors
# =============================================================================

class StateCorruptedError(VisaException):
    """State.json corrompido ou incompatível."""
    
    code = "ERR_STATE_CORRUPTED"
    exit_code = 1


class StateVersionError(VisaException):
    """Versão do state incompatível."""
    
    code = "ERR_STATE_VERSION"
    exit_code = 1


# =============================================================================
# File System Errors
# =============================================================================

class FileSystemError(VisaException):
    """Erro genérico de sistema de arquivos."""
    
    code = "ERR_FILESYSTEM"
    exit_code = 2


class PathPermissionError(VisaException):
    """Sem permissão para acessar/criar path."""
    
    code = "ERR_PERMISSION"
    exit_code = 2


class PathNotFoundError(VisaException):
    """Path não encontrado."""
    
    code = "ERR_PATH_NOT_FOUND"
    exit_code = 2


# =============================================================================
# Manifest Errors
# =============================================================================

class ManifestError(VisaException):
    """Erro de manifest."""
    
    code = "ERR_MANIFEST"
    exit_code = 2


class ManifestMismatchError(VisaException):
    """Manifest SHA-256 não confere."""
    
    code = "ERR_MANIFEST_MISMATCH"
    exit_code = 2


# =============================================================================
# Error Handler Utility
# =============================================================================

def handle_exception(exc: Exception) -> int:
    """Handler centralizado para exceções.
    
    Args:
        exc: Exceção capturada
    
    Returns:
        Exit code apropriado
    """
    from .logging import error_output, get_logger
    
    logger = get_logger("visa.error")
    
    if isinstance(exc, VisaException):
        logger.error(
            exc.message,
            code=exc.code,
            **exc.context,
        )
        if exc.hint:
            logger.warning(f"Hint: {exc.hint}")
        error_output(str(exc))
        return exc.exit_code
    
    # Exceção não-Visa
    logger.error(
        f"Erro inesperado: {type(exc).__name__}",
        error=str(exc),
    )
    error_output(f"Erro inesperado: {exc}")
    return 1
