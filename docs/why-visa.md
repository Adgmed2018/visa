# Why Visa

## O problema

O ecossistema de codificação assistida por IA sofre de uma **ilusão profunda de produtividade**. Pipelines de prompt são inconsistentes. Agentes "mágicos" prometem criar aplicações inteiras a partir de um parágrafo, mas entregam arquiteturas frágeis, arquivos fantasmas (que o LLM diz ter criado mas não existem) e zero auditabilidade.

## A motivação

Visa nasceu da **frustração técnica com a falta de rigor**. É difícil transformar conversas informais com Claude, GPT ou Codex em artefatos versionáveis e confiáveis que sigam um padrão lógico. O mercado focou em "escrever código mais rápido" em vez de "garantir que estamos construindo o sistema correto".

## A tese

Precisávamos de um **sistema de engenharia de software verificável para agentes de IA** — um protocolo que eleva extração de requisitos ao mesmo nível de rigor de um pipeline CI/CD.

## O insight do espelhamento

O [Reversa](https://github.com/sandeco/reversa) (do Sandeco Macedo) já resolvia o problema de **trás para frente**: extrair specs de código legado existente. A Visa é o espelho à frente: extrair specs **antes que o código exista**.

| Reversa | Visa |
|---|---|
| Olha para o passado (código existente) | Olha para o futuro (produto a construir) |
| Lida com **certezas** (o código já existe) | Lida com **hipóteses** (a serem validadas) |
| Documenta o que foi feito | Especifica o que deve ser feito |

Os dois juntos, com o `paridade-guard` no meio, formam um **ciclo SDD fechado** — único no mercado de ferramentas open source de AI-assisted coding.

## Para quem é

- Desenvolvedores que usam Claude Code/Cursor/Codex/Gemini CLI e querem rigor
- Times que precisam **rastreabilidade** entre requisitos e código entregue
- Projetos onde **alucinação custa caro** (saúde, fintech, regulado)
- Quem já usa Reversa e quer fechar o ciclo
