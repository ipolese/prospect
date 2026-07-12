---
name: redesenhar
description: Redesenhar sites de leads com estética premium, conteúdo real, editor visual e comparador. Usar quando o usuário pedir refazer, melhorar ou redesenhar sites prospectados.
---

# Redesenhar sites

1. Ler `redesign-premium` antes de criar HTML.
2. Selecionar os leads indicados; se não houver indicação, usar os melhores leads novos. Confirmar apenas se a seleção for ambígua ou custosa.
3. Usar o navegador integrado para extrair conteúdo, imagens e identidade do site original e obter screenshot de referência.
4. Para cada cliente gerar `sites/[slug]/[slug].html` e `[slug]-editor.html`, sem fatos inventados.
5. Criar ou atualizar `comparar.html` com o template da skill, preservando clientes anteriores. Se o iframe antigo bloquear incorporação, salvar captura autorizada em `sites/[slug]/antigo.png` e registrar `oldImage` no comparador.
6. Rodar `python3 scripts/validate-site.py sites/[slug]/[slug].html`, revisar 360/375/768/1024/1280/1440px e atualizar banco, `leads.md` e dashboard para `redesenhado`.
7. Entregar links dos arquivos, confirmar o total atualizado e sugerir `$publicar` para abrir em localhost.
