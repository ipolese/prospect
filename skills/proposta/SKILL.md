---
name: proposta
description: Preparar propostas comerciais personalizadas para leads com site redesenhado e URL acessível. Usar quando o usuário pedir proposta, e-mail para cliente ou envio do novo site.
---

# Preparar proposta

1. Ler config, banco e `proposta-email`.
2. Selecionar leads com e-mail confirmado e status `publicado` ou `publicado-local`.
3. Bloquear envio externo quando `urlNova` usar `localhost`, `127.0.0.1` ou arquivo local: a URL não abrirá para o cliente. Oferecer configurar publicação pública ou produzir apenas uma prévia do texto.
4. Para URL pública validada, escrever e-mail com conteúdo real, sem preço e com um único link.
5. Rodar integralmente a checklist anti-spam.
6. Criar rascunho pelo conector Gmail quando disponível; caso contrário salvar o texto em `propostas/[slug].html` para cópia manual. Não enviar diretamente sem autorização explícita.
7. Atualizar status e data somente após o rascunho ou envio existir.
