# Contribuindo com a Visa

Obrigado pelo interesse em contribuir. Este guia descreve como reportar
bugs, propor melhorias e enviar pull requests.

## Antes de abrir issue ou PR

Leia o **README** e o **AUTO-AVALIACAO.md** primeiro — eles declaram as
limitações conhecidas e o que está no roadmap. Se o seu issue/PR cai numa
limitação já declarada (ex: Coletor sem gate computacional), será marcado
como duplicate.

## Reportando bugs

Use o template de issue. Inclua:

1. Versão da Visa (`visa --version`)
2. Engine de codificação (Claude Code / Codex / Cursor / Gemini CLI)
3. Comando exato que falhou
4. Output literal (incluindo stack trace)
5. O que você esperava acontecer

## Propondo melhorias

Antes de codar:

1. Abra issue descrevendo o problema (não a solução). Ajuda a alinhar.
2. Aguarde feedback antes de gastar tempo em PR grande.
3. PRs pequenos (<300 linhas) têm review mais rápido.

## Pull Requests

### Antes de submeter

```bash
# Rode a suite Visa completa
python3 tests/test_visa.py

# Rode também a suite do paridade-guard (para garantir cadeia end-to-end)
pip install paridade-guard>=0.3.0
cd /caminho/para/paridade-guard && python3 -m pytest tests/

# Resultado esperado:
# Visa:           PASSED: 31    FAILED: 0    SKIPPED: 0
# paridade-guard: 69 passed
```

Se você adicionou comportamento novo, adicione testes. PRs sem testes serão
solicitadas a adicionar.

### Estilo de código

- Python: stdlib pura. Não adicione dependências externas sem discussão.
- Tipos: `from __future__ import annotations` no topo de cada arquivo.
- Strings: aspas duplas para texto, simples para literais técnicos.
- Comentários em português (consistente com o projeto).

### Convenção de commit

Não exigida formalmente, mas mensagens claras ajudam:

```
patch(redator): corrige IDs BR-FUTURE quando descrição vazia
feat(cli): adiciona flag --json para validate
docs: corrige link quebrado no README
test(bridge): cobre cenário de pipeline incompleto
```

## Mudando os SKILLs (`agents/`)

As skills `.md` são prompts orientacionais para LLMs. Ao mudar uma:

1. Mantenha o front-matter YAML intacto (`name`, `description`, `license`,
   `metadata.inverse_of`).
2. Preserve a escala 🟢🟡🔴 de confiança em todos os agentes que a usam.
3. Se mudar formato de output (ex: nomes de IDs canônicos), atualize
   também os testes em `tests/test_visa.py` e o extractor do paridade-guard.

## Mudando o CLI (`src/visa_sdd/cli.py`)

1. Mantenha compat backward com `state.json` antigo (campo `version`
   determina migração).
2. Comandos novos devem ter teste em `tests/test_visa.py`.
3. Documentar no README + adicionar ao `--help`.

## Código de conduta

Sem código de conduta formal por enquanto. Norte: trate revisores e
autores com respeito; assuma boa fé; ataque o código, não a pessoa.

## Licença das contribuições

Ao submeter PR, você concorda que sua contribuição será licenciada sob
MIT (igual ao projeto).
