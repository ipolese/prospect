---
name: publicar
description: Publicar ou apresentar páginas redesenhadas pelo Prospector, usando localhost por padrão e HostGator apenas se configurada. Usar quando o usuário pedir publicar, servir, abrir localmente, preview ou colocar site no ar.
---

# Publicar sites

1. Ler `prospector-config.json`. Se não existir, usar localhost em `127.0.0.1:8766`; não bloquear por ausência de cPanel.
2. Selecionar o cliente indicado ou todos com status `redesenhado`.
3. Gerar `sites/[slug]/proposta.html` com o template de `proposta-email/references/capa-proposta-template.html`. No modo local, usar URLs relativas para o redesign e o site original.
4. Se `publicacao.provedor` for ausente ou `localhost`, copiar `scripts/servidor-sites.py` e os lançadores para a raiz do workspace quando necessário, iniciar o servidor e validar:
   - página: `http://127.0.0.1:[porta]/sites/[slug]/[slug].html`
   - capa: `http://127.0.0.1:[porta]/sites/[slug]/proposta.html`
5. Registrar `urlNova` com a URL local e status `publicado-local`. Esse estado significa pronto para apresentação, não disponível na internet.
6. Somente quando o usuário pedir URL pública e `hostgator.habilitado=true`, seguir `deploy-hostgator`. Nunca migrar silenciosamente do local para produção.
7. Informar claramente se a URL só funciona neste computador/rede. Para propostas enviadas a clientes externos, solicitar um provedor público antes de criar o rascunho.
