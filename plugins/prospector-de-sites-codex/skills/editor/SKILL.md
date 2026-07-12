---
name: editor
description: Criar ou regenerar o editor visual de uma página redesenhada pelo Prospector. Usar quando o usuário pedir editar textos ou imagens de um site criado.
---

# Editor visual

1. Identificar o cliente ou listar `sites/*/*.html` quando necessário.
2. Ler a página final e `redesign-premium/references/editor-visual.md`.
3. Gerar `[slug]-editor.html` injetando a camada imediatamente antes de `</body>`.
4. Antes de substituir a página original, executar `python3 scripts/version-site.py sites/[slug]/[slug].html --label antes-da-edicao`.
5. Verificar que a exportação remove a camada do editor e preserva o HTML final.
5. Informar: clicar em texto edita; clicar em imagem troca; “Exportar página” baixa a versão limpa.
