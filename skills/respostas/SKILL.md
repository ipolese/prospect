---
name: respostas
description: Verificar respostas de clientes às propostas no Gmail e atualizar o pipeline. Usar quando o usuário pedir verificar respostas, retornos ou situação das propostas.
---

# Verificar respostas

1. Selecionar no banco leads com status `proposta`.
2. Usar o conector Gmail, se disponível, buscando mensagens do lead após `dataProposta` e conferindo a thread original.
3. Considerar resposta somente mensagem enviada pelo endereço do lead, não cópia da própria proposta.
4. Atualizar respondidos para `respondeu`, registrar data/observação e regenerar dashboard.
5. Se Gmail não estiver conectado, informar a limitação e entregar a lista de buscas a executar; não marcar ninguém por suposição.
