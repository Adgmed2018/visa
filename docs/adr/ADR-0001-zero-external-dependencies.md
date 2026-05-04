# ADR-0001: Zero External Dependencies (Stdlib Pure)

## Status

**Accepted** — v1.0.0

## Context

A Visa é o motor de Forward Spec Discovery de um ecossistema SDD. Ela orquestra agentes especializados para descobrir especificações antes da implementação.

**Problema**: Muitas ferramentas de IA-assisted coding criam dependência de bibliotecas externas que:
- Aumentam a superfície de ataque (supply chain security)
- Introduzem incompatibilidades entre versões
- Fragilizam a portabilidade (especialmente em ambientes corporativos restritos)
- Criam atrito na instalação (`pip install visa-sdd` deveria "just work")

**Alternativas Considered**:
1. Usar bibliotecas estabelecidas (PyYAML para parsing, click para CLI)
2. Implementar parsing YAML com regex + stdlib
3. stdlib puro com parsing manual

## Decision

**A Visa usa 100% Python stdlib — sem dependências externas em runtime.**

### Implementação

- **YAML parsing**: front-matter verificado via regex, não via PyYAML
- **CLI parsing**: `argparse` nativo (stdlib)
- **Logging**: `sys.stderr.write()` com formatação manual
- **File operations**: `pathlib.Path`, `shutil`, `hashlib` (stdlib)
- **Testing**: pytest (opcional, `[test]`) mas tests rodam com stdlib runner

### Justificativa Técnica

| Aspecto | Biblioteca Externa | Stdlib |
|---------|-------------------|--------|
| Install time | +2-5s por dependência | Instant |
| Security surface | CVE risk | Zero (stdlib is core) |
| Portability |Pode quebrar em edge cases| Garantida |
| Debugging |第三方 errors| Full visibility |

### Exceções Controladas

```
[project.optional-dependencies]
test = ["pytest>=7.0"]      # Desenvolvimento
e2e = ["paridade-guard>=0.3.0"]  # Integração
dev = ["ruff", "mypy"]     # Ferramentas de desenvolvimento
```

## Consequences

### Positive
- ✅ `pip install visa-sdd` "just works" em qualquer ambiente Python 3.10+
- ✅ Zero CVEs de dependências
- ✅ Install instantâneo
- ✅ Fully auditable (every line is visible)
- ✅ CI simplificado (menos caching, menos install steps)

### Negative
- ❌ Regex parsing de YAML é menos robusto que PyYAML
- ❌ CLI mais verboso (argparse vs click)
- ❌ Sem cores automáticas (precisamos de escape codes manuais)

### Mitigations
- `visa validate --strict` usa regex validado e testado
- Cores via `chalk`-style ANSI codes (manuais)
- Tests cobrem edge cases de parsing

## References

- [Python stdlib docs](https://docs.python.org/3/library/)
- [YAML 1.2 spec](https://yaml.org/spec/1.2.2/) (para regex mapping)
- [paridade-guard](https://github.com/Adgmed2018/paridade-guard) (companion gate)
