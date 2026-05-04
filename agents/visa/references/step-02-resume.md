# Step 02 — Resume

> Lido pela Visa orquestradora quando `.visa/state.json` existe e `phase` está definida.

## Objetivo

Retomar o pipeline na fase exata onde parou, sem repetir trabalho concluído.

## Roteiro

1. Leia `.visa/state.json`. Você terá:
   - `phase`: fase atual (imersao | descoberta | validacao | sintese | geracao | revisao | handoff)
   - `completed`: lista de fases já concluídas
   - `pending`: lista de fases pendentes
   - `user_name`: nome do usuário (use para personalizar)

2. Cumprimente o usuário em tom de continuidade:
   ```
   [Nome], voltei. Estávamos na fase **[phase]**.
   
   Já concluído: [join(completed, ", ")]
   Pendente: [join(pending, ", ")]
   
   Posso continuar de onde paramos?
   ```

3. Se o usuário confirmar, leia `.visa/plan.md` para identificar a próxima
   tarefa não marcada com ✅ e ative o agente correspondente.

4. Se o usuário disser "comece de novo" ou similar, **NÃO apague** `.visa/`
   nem `_visa_sdd/`. Pergunte:
   ```
   Recomeçar do zero apaga o que já foi descoberto. Você quer:
   1. Recomeçar do zero (apaga _visa_sdd/)
   2. Voltar uma fase (mantém _visa_sdd/, refaz fase X)
   3. Ir para uma fase específica (ex: pular para validação)
   ```

5. Sempre que retomar um agente, **releia primeiro os artefatos que ele
   já produziu** em `_visa_sdd/` antes de continuar — para evitar
   inconsistência com decisões anteriores.

## Detecção de drift

Antes de continuar, verifique:
- O usuário editou `_visa_sdd/*.md` manualmente desde a última sessão?
  Se sim, considere essas edições como verdade e atualize sua memória de contexto.
- A `.visa/state.json` pode estar dessincronizada — sempre prefira o que está
  no markdown sobre o que está no state.

## Anti-padrão

- ❌ Repetir agentes já concluídos sem perguntar
- ❌ Apagar artefatos sem confirmação explícita
- ❌ Ignorar edições manuais do usuário em `_visa_sdd/`
