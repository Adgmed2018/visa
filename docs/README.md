# Visa Documentation

Documentação completa do projeto Visa — Forward Spec Discovery for AI Agents.

## 📚 Estrutura de Documentação

```
docs/
├── adr/                      # Architecture Decision Records
│   ├── README.md             # Índice de ADRs
│   ├── ADR-0001-zero-external-dependencies.md
│   ├── ADR-0002-canonical-id-system.md
│   ├── ADR-0003-collector-gate.md
│   ├── ADR-0004-multi-agent-orchestration.md
│   └── ADR-0005-bridge-pattern.md
├── pipeline.md               # Diagrama do pipeline SDD
├── canonical-format.md       # Especificação do formato canônico
├── agents.md                 # Guia de agentes
└── troubleshooting.md        # Guia de troubleshooting
```

## 🔗 Links Rápidos

| Documento | Descrição |
|----------|-----------|
| [README principal](../README.md) | Visão geral do projeto |
| [CLI Reference](../README.md#cli-reference) | Referência completa de comandos |
| [Canonical Format](canonical-format.md) | Especificação do formato de artefatos |
| [Pipeline](pipeline.md) | Diagrama do ciclo SDD |
| [Agents](agents.md) | Detalhamento dos 14 agentes |
| [ADR Index](adr/README.md) | Decisões arquiteturais |

## 📖 Guias

### Getting Started
1. [Instalação](../README.md#installation)
2. [Quick Start](../README.md#quick-start)
3. [Demo 5 minutos](../README.md#demo-em-5-minutos)

### Uso Avançado
1. [Formato Canônico](canonical-format.md)
2. [Pipeline SDD](pipeline.md)
3. [Agentes](agents.md)
4. [Troubleshooting](troubleshooting.md)

### Desenvolvimento
1. [Contributing](../CONTRIBUTING.md)
2. [ADR Guidelines](adr/README.md)
3. [pyproject.toml](../pyproject.toml)

## 🛠️ Troubleshooting

Consulte [troubleshooting.md](troubleshooting.md) para problemas comuns e soluções.

### Problemas Comuns

| Problema | Solução |
|----------|--------|
| `visa: command not found` | Reinstale com `pip install -e .` |
| `LACUNA bloqueando bridge` | Execute `visa bridge --accept-all-risks="motivo"` |
| `Contract vazio` | Verifique se artefatos têm `schemaVersion: 1` |
| `Testes falhando` | Execute `python3 tests/test_visa.py` para diagnóstico |

## 🔄 Manutenção

| Item | Frequência | Responsável |
|------|------------|-------------|
| Atualizar ADRs | Quando decisão mudar | Mantenedor |
| Revisar SKILL.md | Monthly | Equipe |
| Atualizar dependências dev | Weekly (automático via pre-commit) | CI/CD |
| Coverage report | Per PR | CI/CD |

## 📝 Contribuindo com Documentação

1. Documente em Markdown (GFM)
2. Use [Mermaid](https://mermaid.js.org/) para diagramas
3. Adicione badges para status
4. Mantenha índice atualizado

---
