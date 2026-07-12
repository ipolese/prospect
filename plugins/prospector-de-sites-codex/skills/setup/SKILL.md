---
name: setup
description: Configurar ou atualizar o Prospector de Sites no Codex, criando config, banco, dashboard e preview localhost. Usar quando o usuário pedir setup, configuração inicial ou alterar preferências do prospector.
---

# Configurar o Prospector

1. Usar a raiz do workspace escolhido pelo usuário. Criar nela `prospector-config.json`, `prospector.db`, `dashboard.html`, `sites/` e os lançadores locais quando ausentes.
2. Coletar apenas dados faltantes: assinatura (nome, apresentação e WhatsApp), nichos, cidade, meta de leads e modo de e-mail (`rascunho` por padrão).
3. Salvar o config sem exigir hospedagem:

```json
{
  "assinatura": {"nome":"", "apresentacao":"", "whatsapp":""},
  "prospeccao": {"nichos":[
    "Todos",
    "nutricionistas", "psicologos", "advogados", "psiquiatras",
    "dentistas", "dermatologistas", "fisioterapeutas", "fonoaudiologos",
    "terapeutas ocupacionais", "clinicas de estetica", "studios de pilates", "academias",
    "clinicas veterinarias", "pet shops", "saloes de beleza", "barbearias",
    "arquitetos", "designers de interiores", "contadores", "consultores financeiros",
    "imobiliarias", "escolas de idiomas", "cursos profissionalizantes", "fotografos",
    "cerimonialistas", "restaurantes", "pousadas", "oficinas mecanicas"
  ], "cidade":"", "leadsPorBusca":10},
  "envio": {"modo":"rascunho"},
  "publicacao": {"provedor":"localhost", "porta":8766, "host":"127.0.0.1"},
  "hostgator": {"habilitado":false, "usuario":"", "dominio":"", "servidor":"", "porta":22, "chaveSsh":"", "pastaBase":"clientes"}
}
```

4. Nunca solicitar nem armazenar senha. O deploy opcional usa SFTP em modo batch com chave SSH protegida pelo sistema. FTP simples é proibido.
5. Seguir `dashboard-leads` para inicializar banco e dashboard. Copiar de `../../scripts/` os lançadores e o servidor de preview para a raiz do workspace.
6. Testar o preview executando `python3 servidor-sites.py --port 8766` na raiz e validar `http://127.0.0.1:8766/`. O servidor deve expor somente `sites/`.
7. Disponibilizar também `dashboard-app.js`, `scripts/sync-dashboard.py`, `scripts/backup-db.py`, `scripts/dedupe-leads.py`, `scripts/google-place-dedupe.py`, `scripts/validate-site.py`, `scripts/visual-check.py`, `scripts/capture-site.py`, `scripts/google-connectors.py`, `scripts/lgpd.py`, `scripts/tasks-calendar.py` e `scripts/providers.py` na pasta de trabalho.
8. Executar `python3 scripts/diagnostico.py --workspace .` antes de encerrar e informar qualquer erro.
9. Encerrar indicando o ciclo: `$prospectar` → `$redesenhar` → `$publicar` (localhost) → `$proposta`.
