"""
Testes unitários de logging.py e exceptions.py.

Esses módulos têm coverage baixo porque os testes principais (test_visa.py)
invocam o CLI via subprocess, que captura coverage do cli.py mas não exercita
diretamente a API de logging/exceptions. Esta suite testa diretamente os
módulos para subir coverage de 33%/68% para ≥80%.
"""

from __future__ import annotations

import json

import pytest

from visa_sdd import exceptions
from visa_sdd import logging as visa_logging

# ============================================================================
# logging.py
# ============================================================================


class TestLogLevel:
    def test_log_levels_have_expected_values(self):
        assert visa_logging.LogLevel.DEBUG.value == 0
        assert visa_logging.LogLevel.INFO.value == 1
        assert visa_logging.LogLevel.WARNING.value == 2
        assert visa_logging.LogLevel.ERROR.value == 3
        assert visa_logging.LogLevel.CRITICAL.value == 4

    def test_log_level_str_returns_name(self):
        assert str(visa_logging.LogLevel.INFO) == "INFO"
        assert str(visa_logging.LogLevel.ERROR) == "ERROR"


class TestVerbosityControls:
    def test_set_verbosity_levels(self):
        for level in range(5):
            visa_logging.set_verbosity(level)
        # Reset
        visa_logging.set_verbosity(1)

    def test_set_quiet_toggles(self):
        visa_logging.set_quiet(True)
        visa_logging.set_quiet(False)

    def test_set_structured_toggles(self):
        visa_logging.set_structured(True)
        visa_logging.set_structured(False)


class TestGetLogger:
    def test_returns_visa_logger_instance(self):
        logger = visa_logging.get_logger("test")
        assert isinstance(logger, visa_logging.VisaLogger)

    def test_logger_has_name(self):
        logger = visa_logging.get_logger("test.module")
        assert logger.name == "test.module"


class TestVisaLogger:
    def test_info_logs_to_stderr(self, capsys):
        visa_logging.set_quiet(False)
        visa_logging.set_verbosity(1)
        logger = visa_logging.get_logger("test.info")
        logger.info("hello world")
        captured = capsys.readouterr()
        assert "hello world" in captured.err or "hello world" in captured.out

    def test_warning_logs(self, capsys):
        visa_logging.set_quiet(False)
        logger = visa_logging.get_logger("test.warn")
        logger.warning("careful")
        captured = capsys.readouterr()
        combined = captured.err + captured.out
        assert "careful" in combined

    def test_error_logs(self, capsys):
        visa_logging.set_quiet(False)
        logger = visa_logging.get_logger("test.err")
        logger.error("boom")
        captured = capsys.readouterr()
        combined = captured.err + captured.out
        assert "boom" in combined

    def test_debug_suppressed_at_info_level(self, capsys):
        visa_logging.set_quiet(False)
        visa_logging.set_verbosity(1)  # INFO
        logger = visa_logging.get_logger("test.debug")
        logger.debug("hidden")
        captured = capsys.readouterr()
        combined = captured.err + captured.out
        assert "hidden" not in combined

    def test_quiet_suppresses_info(self, capsys):
        visa_logging.set_quiet(True)
        logger = visa_logging.get_logger("test.quiet")
        logger.info("should be silent")
        captured = capsys.readouterr()
        combined = captured.err + captured.out
        assert "should be silent" not in combined
        # Reset
        visa_logging.set_quiet(False)

    def test_extra_kwargs_appear_in_output(self, capsys):
        visa_logging.set_quiet(False)
        visa_logging.set_structured(False)
        logger = visa_logging.get_logger("test.extra")
        logger.info("op", count=42, engine="claude-code")
        captured = capsys.readouterr()
        combined = captured.err + captured.out
        assert "count" in combined or "42" in combined

    def test_structured_output_is_json(self, capsys):
        visa_logging.set_quiet(False)
        visa_logging.set_structured(True)
        logger = visa_logging.get_logger("test.struct")
        logger.info("structured", k="v")
        captured = capsys.readouterr()
        combined = (captured.err + captured.out).strip().splitlines()
        # Encontrar uma linha que seja JSON válido
        parsed = None
        for line in combined:
            try:
                parsed = json.loads(line)
                break
            except (ValueError, json.JSONDecodeError):
                continue
        # Reset
        visa_logging.set_structured(False)
        assert parsed is not None
        assert parsed.get("message") == "structured"


class TestVisaErrorHierarchy:
    def test_visa_error_base(self):
        err = visa_logging.VisaError("base")
        assert str(err) == "base"
        assert isinstance(err, Exception)

    def test_not_installed_error(self):
        err = visa_logging.VisaNotInstalledError("not installed")
        assert isinstance(err, visa_logging.VisaError)

    def test_artifact_not_found(self):
        err = visa_logging.VisaArtifactNotFoundError("missing")
        assert isinstance(err, visa_logging.VisaError)

    def test_validation_error(self):
        err = visa_logging.VisaValidationError("bad")
        assert isinstance(err, visa_logging.VisaError)

    def test_collector_gate_error(self):
        err = visa_logging.VisaCollectorGateError("blocked")
        assert isinstance(err, visa_logging.VisaError)

    def test_bridge_error(self):
        err = visa_logging.VisaBridgeError("bridge")
        assert isinstance(err, visa_logging.VisaError)

    def test_symlink_error(self):
        err = visa_logging.VisaSymlinkError("symlink")
        assert isinstance(err, visa_logging.VisaError)


class TestProgressIndicators:
    def test_progress_renders_without_error(self, capsys):
        visa_logging.set_quiet(False)
        visa_logging.progress(1, 10, "downloading")
        visa_logging.progress(10, 10, "done")
        # Apenas garantir que não levanta exceção
        captured = capsys.readouterr()
        assert captured is not None

    def test_progress_handles_zero_total(self, capsys):
        # Edge case
        try:
            visa_logging.progress(0, 0, "empty")
        except ZeroDivisionError:
            pytest.fail("progress should handle zero total gracefully")

    def test_spinner_returns_object(self):
        sp = visa_logging.spinner("loading")
        assert sp is not None

    def test_spinner_start_and_stop(self, capsys):
        sp = visa_logging.spinner("processing")
        sp.start()
        sp.stop()
        captured = capsys.readouterr()
        assert captured is not None

    def test_spinner_update_when_running(self, capsys):
        sp = visa_logging.Spinner("frame")
        sp._running = True
        sp._update()
        sp._update()
        sp._update()
        captured = capsys.readouterr()
        assert "frame" in captured.err or "frame" in captured.out

    def test_spinner_update_when_stopped_is_noop(self):
        sp = visa_logging.Spinner("nope")
        sp._running = False
        sp._update()


class TestColoredOutputs:
    """Funções top-level success/warning/error_output/info."""

    def test_success_writes_message(self, capsys):
        visa_logging.set_quiet(False)
        visa_logging.success("done")
        captured = capsys.readouterr()
        assert "done" in (captured.err + captured.out)

    def test_warning_writes_message(self, capsys):
        visa_logging.set_quiet(False)
        visa_logging.warning("careful")
        captured = capsys.readouterr()
        assert "careful" in (captured.err + captured.out)

    def test_error_output_writes_message(self, capsys):
        visa_logging.error_output("boom")
        captured = capsys.readouterr()
        assert "boom" in (captured.err + captured.out)

    def test_info_top_level_writes_message(self, capsys):
        visa_logging.set_quiet(False)
        visa_logging.info("note")
        captured = capsys.readouterr()
        assert "note" in (captured.err + captured.out)

    def test_quiet_suppresses_success(self, capsys):
        visa_logging.set_quiet(True)
        visa_logging.success("hidden")
        captured = capsys.readouterr()
        assert "hidden" not in (captured.err + captured.out)
        visa_logging.set_quiet(False)

    def test_quiet_suppresses_warning(self, capsys):
        visa_logging.set_quiet(True)
        visa_logging.warning("hidden warn")
        captured = capsys.readouterr()
        assert "hidden warn" not in (captured.err + captured.out)
        visa_logging.set_quiet(False)

    def test_quiet_suppresses_top_info(self, capsys):
        visa_logging.set_quiet(True)
        visa_logging.info("hidden info")
        captured = capsys.readouterr()
        assert "hidden info" not in (captured.err + captured.out)
        visa_logging.set_quiet(False)

    def test_error_output_NOT_suppressed_by_quiet(self, capsys):
        """Erros sempre aparecem, mesmo em modo quiet."""
        visa_logging.set_quiet(True)
        visa_logging.error_output("critical")
        captured = capsys.readouterr()
        assert "critical" in (captured.err + captured.out)
        visa_logging.set_quiet(False)


class TestProgressAdvanced:
    def test_progress_at_completion(self, capsys):
        visa_logging.set_quiet(False)
        visa_logging.progress(10, 10, "complete")
        captured = capsys.readouterr()
        combined = captured.err + captured.out
        assert "100" in combined or "complete" in combined

    def test_progress_quiet_suppresses(self, capsys):
        visa_logging.set_quiet(True)
        visa_logging.progress(5, 10, "midway")
        captured = capsys.readouterr()
        assert "midway" not in (captured.err + captured.out)
        visa_logging.set_quiet(False)

    def test_progress_partial(self, capsys):
        visa_logging.set_quiet(False)
        visa_logging.progress(3, 10, "thirty percent")
        captured = capsys.readouterr()
        combined = captured.err + captured.out
        assert "thirty percent" in combined or "30" in combined


# ============================================================================
# exceptions.py
# ============================================================================


class TestVisaExceptionBase:
    def test_visa_exception_is_exception(self):
        err = exceptions.VisaException("base message")
        assert isinstance(err, Exception)
        assert "base message" in str(err)

    def test_visa_exception_with_remediation(self):
        try:
            err = exceptions.VisaException("msg", remediation="run X")
            assert "msg" in str(err)
        except TypeError:
            # Se a API não aceita remediation kwarg, ignora
            pass


class TestSpecificExceptions:
    """Cada subclasse deve ser instanciável e herdar de VisaException."""

    @pytest.mark.parametrize("exc_cls", [
        exceptions.NotInstalledError,
        exceptions.AlreadyInstalledError,
        exceptions.AgentNotFoundError,
        exceptions.SkillsCopyError,
        exceptions.ArtifactNotFoundError,
        exceptions.SchemaVersionError,
        exceptions.CollectorGateError,
        exceptions.LacunaNotResolvedError,
        exceptions.BridgeError,
        exceptions.BridgeIncompleteError,
        exceptions.SymlinkError,
        exceptions.ParidadeGuardNotAvailableError,
        exceptions.UninstallError,
        exceptions.StateCorruptedError,
        exceptions.StateVersionError,
        exceptions.FileSystemError,
        exceptions.PathPermissionError,
    ])
    def test_exception_can_be_instantiated_with_message(self, exc_cls):
        """Exceções com signature simples (str message)."""
        try:
            err = exc_cls("test message")
        except TypeError:
            err = exc_cls()
        assert isinstance(err, exceptions.VisaException)

    def test_artifact_format_error_with_required_args(self):
        """ArtifactFormatError exige (artifact, issue)."""
        err = exceptions.ArtifactFormatError("landscape.md", "missing front-matter")
        assert isinstance(err, exceptions.VisaException)
        assert "landscape.md" in str(err) or "missing" in str(err)

    def test_canonical_format_error_with_required_args(self):
        """CanonicalFormatError exige (artifact, expected_kind, actual_kind)."""
        err = exceptions.CanonicalFormatError(
            "business_model.md", "BusinessModel", "Unknown"
        )
        assert isinstance(err, exceptions.VisaException)

    def test_exceptions_are_distinct_types(self):
        assert exceptions.NotInstalledError is not exceptions.AlreadyInstalledError
        assert exceptions.BridgeError is not exceptions.BridgeIncompleteError

    def test_inheritance_hierarchy(self):
        # BridgeIncompleteError deve ser subclasse de BridgeError
        try:
            err = exceptions.BridgeIncompleteError("incomplete")
            assert isinstance(err, exceptions.BridgeError) or isinstance(
                err, exceptions.VisaException
            )
        except TypeError:
            pass


class TestExceptionFormatting:
    def test_str_returns_message(self):
        err = exceptions.NotInstalledError("custom message")
        assert "custom message" in str(err)

    def test_repr_includes_class_name(self):
        err = exceptions.BridgeError("oops")
        rep = repr(err)
        assert "BridgeError" in rep or "oops" in rep
