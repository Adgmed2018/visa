# Contributing to Visa

Thank you for your interest in contributing to Visa — Forward Spec Discovery for AI Agents.

## Quick Links

| Resource | Link |
|----------|------|
| README | [README.md](README.md) |
| Architecture Decisions | [docs/adr/](docs/adr/) |
| Auto-evaluation | [AUTO-AVALIACAO.md](AUTO-AVALIACAO.md) |
| Issues | [GitHub Issues](https://github.com/Adgmed2018/visa/issues) |
| Discussions | [GitHub Discussions](https://github.com/Adgmed2018/visa/discussions) |

---

## Development Setup

### Prerequisites

- Python 3.10+
- Git

### Clone & Install

```bash
# Clone repository
git clone https://github.com/Adgmed2018/visa.git
cd visa

# Install in development mode
pip install -e .

# Install development dependencies
pip install -e ".[dev]"

# Verify installation
visa --version
```

### Running Tests

```bash
# Run full test suite
python3 tests/test_visa.py

# Expected output:
# PASSED: 40    FAILED: 0    SKIPPED: 0
```

---

## Code Standards

### Philosophy

**100% stdlib** — No third-party dependencies in runtime.

```python
# ✅ Good: Using stdlib only
from pathlib import Path
from datetime import datetime
import json

# ❌ Bad: Adding external dependencies
import yaml  # Not allowed
from rich import print  # Not allowed
```

### Type Annotations

All new code must include type annotations:

```python
from __future__ import annotations
from pathlib import Path

def process_artifact(path: Path, strict: bool = False) -> dict[str, str]:
    """Process artifact with type hints."""
    ...
```

### Docstrings

Follow Google style docstrings:

```python
def cmd_bridge(args: argparse.Namespace) -> int:
    """Build bridge to paridade-guard.
    
    Args:
        args: Parsed command-line arguments
        
    Returns:
        Exit code (0 on success)
        
    Raises:
        CollectorGateError: If collector gate blocks pipeline
    """
    ...
```

### Error Handling

Use custom exceptions from `visa_sdd.exceptions`:

```python
from visa_sdd.exceptions import ArtifactNotFoundError, CollectorGateError

def validate_artifacts(output_folder: Path) -> None:
    if not (output_folder / "business_model.md").exists():
        raise ArtifactNotFoundError(
            "business_model.md",
            hint="Run the Redactor agent to generate canonical artifacts"
        )
```

---

## Testing Guidelines

### Test Structure

```python
class TestBridge:
    """Tests for visa bridge command."""
    
    def test_bridge_cria_migration_stub(self):
        """Test creates migration stub directory."""
        with tempfile.TemporaryDirectory() as tmp:
            tmp_root = Path(tmp)
            self._setup_canonical_visa_sdd(tmp_root)
            
            r = _run_visa("bridge", cwd=tmp_root)
            assert r.returncode == 0
            assert (tmp_root / "_visa_sdd" / "migration").is_dir()
```

### Running Specific Tests

```bash
# Test single class
python3 -c "
from test_visa import TestBridge
t = TestBridge()
t.test_bridge_cria_migration_stub()
print('✅ Passed')
"

# Run with pytest (if installed)
pytest tests/test_visa.py::TestBridge -v
```

### End-to-End Testing

For e2e tests with paridade-guard:

```bash
# Install paridade-guard
pip install paridade-guard>=0.3.0

# Run e2e tests
python3 tests/test_visa.py
# Tests should show: PASSED: 40, SKIPPED: 0
```

---

## Submitting Changes

### Before Submitting

1. **Run tests**: `python3 tests/test_visa.py`
2. **Run linting**: `ruff check .` (if installed)
3. **Update documentation**: If you changed CLI, update README.md
4. **Add tests**: For new functionality, add tests in `tests/test_visa.py`

### Commit Messages

Follow conventional commits:

```
type(scope): description

types:
  feat: New feature
  fix: Bug fix
  docs: Documentation changes
  test: Test changes
  refactor: Code refactoring
  perf: Performance improvements
  chore: Tooling changes

examples:
  feat(cli): add --json flag for structured output
  fix(bridge): resolve symlink fallback on Windows
  docs(readme): update CLI reference
  test(collector): add gate blocking tests
```

### Pull Request Process

1. Fork the repository
2. Create a feature branch: `git checkout -b feat/my-feature`
3. Make your changes
4. Run tests: `python3 tests/test_visa.py`
5. Commit with clear message
6. Push to your fork
7. Open Pull Request with:
   - Clear title
   - Description of changes
   - Link to related issue
   - Screenshots (if UI changes)

### Review Timeline

| PR Size | Expected Review |
|---------|-----------------|
| <100 lines | 1-2 days |
| 100-300 lines | 2-5 days |
| >300 lines | 1-2 weeks (consider splitting) |

---

## Changing Agents (SKILL.md)

Agents are located in `agents/` directory:

```
agents/
├── visa/SKILL.md              # Orchestrator
├── visa-etnografo/SKILL.md    # Discovery
├── visa-coletor/SKILL.md      # Evidence collector
├── visa-redator/SKILL.md      # Spec generator
└── ...
```

### When Changing an Agent

1. **Keep front-matter intact**:
   ```yaml
   ---
   name: visa-redator
   description: Emite especificações imutáveis
   license: MIT
   metadata:
     inverse_of: reversa-writer
   ---
   ```

2. **Preserve confidence scale**: 🟢🟡🔴

3. **Update tests if output format changes**

---

## Architecture Decisions

New architectural decisions should be documented as ADRs:

```bash
# Create new ADR
touch docs/adr/ADR-XXXX-title.md
```

Follow the [ADR template](docs/adr/README.md).

---

## Bug Reports

Use the issue template with:

1. **Visa version**: `visa --version`
2. **Python version**: `python --version`
3. **OS**: Windows/macOS/Linux
4. **Engine**: Claude Code/Cursor/Codex/Gemini CLI
5. **Command**: Exact command that failed
6. **Full output**: Including error messages
7. **Expected vs Actual**: What should happen vs what happened

Example:
```markdown
## Environment
- visa: 1.3.0
- python: 3.12.0
- os: macOS 14.0

## Command
visa bridge

## Output
🛑 BRIDGE BLOQUEADA pelo gate do Coletor.
   1 LACUNA(s) pendente(s):
     - LACUNA-001

## Expected
Bridge should complete successfully

## Actual
Pipeline blocked due to unresolved LACUNA
```

---

## Feature Requests

Before requesting features:

1. Check [existing issues](https://github.com/Adgmed2018/visa/issues)
2. Check [roadmap](AUTO-AVALIACAO.md)
3. Open discussion for alignment

For features, explain:
- **Problem**: What problem does it solve?
- **Solution**: How should it work?
- **Alternatives**: What else did you consider?

---

## Code of Conduct

We follow the principle: **assume good faith, attack code not people**.

- Be respectful in discussions
- Focus on technical arguments
- Help newcomers
- Give constructive feedback

---

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

---

<p align="center">
<strong>Built with rigor. Shipped with confidence.</strong>
</p>
