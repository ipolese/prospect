---
name: prospectar
description: Prospectar clientes no Google Maps, avaliar sites fracos e registrar leads no banco/dashboard. Usar quando o usuário pedir buscar clientes, achar leads, prospectar um nicho ou uma cidade.
---

# Prospectar leads

1. Ler `prospector-config.json`, `prospector.db` e `leads.md`; orientar `$setup` se o config não existir.
2. Determinar nicho e cidade pelos argumentos ou padrões configurados. Se o nicho escolhido for `Todos` (sem distinção de maiúsculas/minúsculas), percorrer todos os nichos configurados, ignorando o próprio item `Todos`, com no máximo 10 nichos e 100 leads por execução. Consolidar os resultados sem duplicar leads por domínio ou telefone; interromper e salvar checkpoint a cada nicho.
3. Usar o navegador integrado conforme `prospeccao-maps`. Excluir negócios já avaliados.
4. Coletar qualificados e descartados, com fonte e motivo objetivo. Nunca inventar e-mail, avaliação ou contato.
5. Salvar no SQLite e em `leads.md`; atualizar `dashboard.html` conforme `dashboard-leads`.
6. Criar Google Sheets somente se um conector compatível estiver disponível; caso contrário entregar CSV local sem bloquear o fluxo.
7. Confirmar `Dashboard atualizado: [N] leads` e sugerir `$redesenhar`.
