---
name: contrato
description: Gerar minuta HTML e DOCX de contrato para cliente fechado e preparar o e-mail. Usar quando o usuário pedir contrato, formalização ou informar que um cliente fechou.
---

# Gerar contrato

1. Ler banco, config e `contrato-servico`; selecionar cliente fechado ou respondido.
2. Reutilizar todos os dados existentes e perguntar somente o que faltar. Nunca inventar valor, prazo, documento, endereço ou manutenção.
3. Gerar `sites/[slug]/contrato-[slug].html` pelo template e conferir ausência de `{{...}}`.
4. Gerar o DOCX com `contrato-servico/references/gerar-docx.py`; instalar dependência apenas com autorização quando ausente.
5. Criar rascunho no Gmail quando disponível. Se anexos não forem suportados, informar o arquivo exato para anexar manualmente.
6. Atualizar `contratoStatus` somente após gerar os arquivos; marcar enviado apenas após criar ou enviar o e-mail.
