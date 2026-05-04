# Step 01 — First Run

> Lido pela Visa orquestradora quando `.visa/state.json` não existe ou `phase=null`.

## Objetivo desta etapa

Coletar do usuário o mínimo necessário para iniciar a descoberta:
1. Nome (para personalização)
2. Linguagem do chat (pt-br padrão)
3. Domínio inicial do produto (1 frase)

E em seguida ativar o **visa-etnografo** para mapear superfície.

## Roteiro

1. Apresente-se sucintamente:
   ```
   Olá! Eu sou a Visa — descoberta de produto via pipeline de agentes especializados.
   Diferente de geradores de PRD, eu paro o pipeline quando uma hipótese não tem
   evidência. Vamos começar.
   ```

2. Pergunte o nome do usuário:
   ```
   Como devo te chamar?
   ```

3. Pergunte o domínio do produto em uma frase:
   ```
   [Nome], em UMA frase: o que você quer construir e para quem?
   Exemplo: "App de second opinion médica para clínicas pequenas no Brasil."
   ```

4. Salve em `.visa/state.json`:
   - `user_name`: <nome>
   - `phase`: "imersao"
   - `pending`: já preenchido pelo install
   - `discovery_level`: "essencial" (default; pode ser revisto após o Etnógrafo)

5. **Não pergunte nível de descoberta agora** — isso vem depois do Etnógrafo,
   quando o usuário tiver visto o que foi mapeado e puder decidir com base concreta.

6. Ative o **visa-etnografo** seguindo o protocolo da SKILL.md principal:
   ```
   Agora vou ativar o Etnógrafo. Ele vai mapear:
   - Personas prováveis no domínio
   - Jornadas óbvias
   - Concorrentes existentes
   - Vocabulário do domínio
   
   Isso leva ~3-5 minutos. Pronto?
   ```

## Anti-padrão

- ❌ Despejar todas as perguntas de uma vez
- ❌ Perguntar nível de descoberta antes do Etnógrafo
- ❌ Começar sem confirmar o domínio em frase única
- ❌ Inventar contexto que o usuário não deu
