# Security Policy

Este documento descreve a política de segurança do projeto Visa.

## Reportando Vulnerabilidades

Se você descobrir uma vulnerabilidade de segurança, por favor:

1. **Não abra issue pública** — reporte via email ou mensagem privada
2. **Forneça detalhes suficientes** para reproduzir o problema
3. **Aguarde confirmação** antes de publicizar

**Email**: Abra uma issue com label `security` marcada como confidencial (GitHub)

## Escopo de Segurança

| Componente | Escopo | Notas |
|------------|--------|-------|
| `src/visa_sdd/cli.py` | ✅ Sim | CLI principal |
| `src/visa_sdd/logging.py` | ✅ Sim | Logging estruturado |
| `src/visa_sdd/exceptions.py` | ✅ Sim | Error handling |
| `agents/*.md` | ⚠️ Leitura | SKILL.md são inputs, não executados |
| `tests/*.py` | ❌ Não | Scripts de teste |
| Docs | ❌ Não | Documentação |

## Ameaças Consideradas

### 1. Path Traversal

**Descrição**: Arquivos criados fora do diretório esperado.

**Mitigação**:
```python
# Verificar que path está dentro do projeto
def safe_path(base: Path, target: Path) -> Path:
    resolved = target.resolve()
    if not str(resolved).startswith(str(base.resolve())):
        raise SecurityError("Path traversal detected")
    return resolved
```

### 2. Symlink Attacks

**Descrição**: Criação de symlinks maliciosos durante `visa bridge`.

**Mitigação**:
```python
# Verificar antes de criar symlink
def safe_symlink(src: Path, dst: Path) -> None:
    if dst.is_symlink() or dst.is_file():
        dst.unlink()  # Remove existente
    dst.symlink_to(src.resolve())
```

### 3. Manifest Tampering

**Descrição**: Modificação do SHA-256 manifest.

**Mitigação**:
```python
# Verificar integridade do manifest
def verify_manifest(project_root: Path) -> bool:
    manifest_path = project_root / ".visa" / "_config" / "files-manifest.json"
    manifest = json.loads(manifest_path.read_text())
    
    for rel_path, expected_hash in manifest.items():
        full = project_root / rel_path
        if not full.exists():
            return False
        actual_hash = hashlib.sha256(full.read_bytes()).hexdigest()
        if actual_hash != expected_hash:
            return False
    return True
```

### 4. Arbitrary Code Execution via Skills

**Descrição**: Skills maliciosas injectadas em `agents/`.

**Mitigação**:
- Skills são SKILL.md (Markdown), não Python executável
- Manifest SHA-256 verifica integridade
- Apenas arquivos com extensão `.md` são instalados

### 5. Dependency Confusion

**Descrição**: Pacote malicioso com nome similar.

**Mitigação**:
- Visa não tem dependências externas (100% stdlib)
- Verificação de签名 não aplicável (sem dependências)

## Práticas de Desenvolvimento Seguro

### Princípios

1. **Minimalismo**: 100% stdlib — superfície de ataque mínima
2. **Defense in Depth**: Múltiplas camadas de validação
3. **Fail Secure**: Falhas devem bloquear, não permitir bypass
4. **Auditability**: SHA-256 manifest para verificação

### Code Review Checklist

- [ ] Paths são normalizados e validados
- [ ] Symlinks não apontam para fora do projeto
- [ ] Manifest é verificado em uninstall
- [ ] Exit codes são apropriados para cada erro
- [ ] Não há hardcoded secrets

### Testing de Segurança

```bash
# Verificar que não há secrets hardcoded
grep -r "password\|secret\|api_key\|token" src/ tests/ || echo "✅ No hardcoded secrets"

# Verificar que manifest é gerado
python3 -c "
from pathlib import Path
import json

manifest = Path('.visa/_config/files-manifest.json')
if manifest.exists():
    data = json.loads(manifest.read_text())
    print(f'✅ Manifest has {len(data)} entries')
else:
    print('❌ Manifest not found')
"

# Testar path traversal
python3 -c "
from pathlib import Path

def safe_path(base, target):
    resolved = Path(target).resolve()
    if not str(resolved).startswith(str(base.resolve())):
        raise Exception('Path traversal')
    return resolved

# Test
base = Path('/tmp/project')
try:
    safe_path(base, '/etc/passwd')
    print('❌ Path traversal allowed!')
except Exception:
    print('✅ Path traversal blocked')
"
```

## Vulnerabilidades Conhecidas

| ID | Severity | Status | Description |
|----|----------|--------|-------------|
| None | - | - | Nenhuma vulnerabilidade conhecida |

## Atualizações de Segurança

Este policy é revisado mensalmente. Última revisão: 2025-01-15

---

## Contato

Para questões de segurança: Abra issue com label `security` ou contate diretamente.

---

<p align="center">
<strong>Security is not a feature — it's a requirement.</strong>
</p>
