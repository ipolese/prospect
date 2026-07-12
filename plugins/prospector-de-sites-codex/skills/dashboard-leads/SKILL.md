---
name: dashboard-leads
description: Criar e atualizar o dashboard local SQLite dos leads. Usar sempre que um fluxo do Prospector mudar leads, ou quando o usuário pedir dashboard, painel, controle de clientes ou banco de leads.
---

# Dashboard de leads (SQLite + página local)

Arquitetura na RAIZ da pasta conectada:

- **`prospector.db`** — banco SQLite, a FONTE DA VERDADE dos leads.
- **`dashboard-server.py` + lançador do sistema** — servidor administrativo em `127.0.0.1:8765`, com sessão, CSRF, validação de origem, limites de payload e rotas estáticas restritas.
- **`dashboard.html`** — a página do painel (gerada do template). Servida pelo servidor (modo banco) ou aberta por duplo clique (modo arquivo: só leitura + edições presas ao navegador). O badge no topo indica o modo.
- **`audit_log`** — histórico local de alterações, exclusões e upserts para permitir rastreabilidade e recuperação.

## Setup (uma vez, no /setup ou no primeiro uso)

1. Copie `references/dashboard-server.py`, `references/dashboard-app.js` e `references/iniciar-dashboard.bat` desta skill para a raiz da pasta conectada.
2. Crie o `prospector.db` com o schema abaixo (via python3/sqlite3 no bash).
3. Gere o `dashboard.html` a partir de `references/dashboard-template.html` substituindo `__DADOS__` pelo snapshot JSON.
4. Defina permissão `0600` para config e banco quando o sistema suportar. Nunca coloque senha no config.
5. Diga ao usuário que o dashboard administrativo e o preview de sites usam servidores separados.

## Schema do banco

```sql
CREATE TABLE IF NOT EXISTS leads(
  slug TEXT PRIMARY KEY, nome TEXT, nicho TEXT, cidade TEXT, nota REAL, avaliacoes INTEGER,
  email TEXT, telefone TEXT, whatsapp TEXT, siteAntigo TEXT, motivo TEXT,
  status TEXT DEFAULT 'novo', urlNova TEXT, dataProposta TEXT, valor REAL, obs TEXT,
  contratoStatus TEXT DEFAULT 'pendente', contratoEm TEXT, manutencao REAL, pago INTEGER DEFAULT 0,
  docCliente TEXT, endCliente TEXT,
  atualizado TEXT DEFAULT (datetime('now','localtime')));
```

Status: `novo | redesenhado | publicado-local | publicado | proposta-rascunho | proposta | respondeu | negociacao | fechado | perdido | descartado`. `placeId` do Google Maps é a identidade preferencial; `publicado-local` indica preview acessível apenas na máquina/rede local.

## Como os comandos atualizam (SEMPRE os 2 passos)

1. **Upsert no banco** via bash (exemplo):
```bash
python3 - <<'EOF'
import sqlite3
c = sqlite3.connect('CAMINHO/prospector.db')
c.execute("INSERT INTO leads (slug,nome,status,...) VALUES (?,?,?,...) ON CONFLICT(slug) DO UPDATE SET status=excluded.status, atualizado=datetime('now','localtime')", (...))
c.commit()
EOF
```
   - `/prospectar` → insere leads (`novo`) e descartados (`descartado`, motivo em `obs`). NUNCA sobrescreva um lead cujo status já avançou.
   - `$redesenhar` → `status='redesenhado'` · `$publicar` em localhost → `status='publicado-local'` · deploy público → `status='publicado'` · `$proposta` → `status='proposta'`.
   - Usuário conta que respondeu/fechou → `status='respondeu'|'fechado'`, `valor` (+ `manutencao` se houver mensalidade).
   - `/contrato` → `contratoStatus='enviado'` + `contratoEm`. Cliente assinou → `contratoStatus='assinado'`. Pagamento recebido → `pago=1`.
2. **Regenerar o snapshot**: leia todos os leads do banco e regrave `dashboard.html` do template com o JSON embutido atualizado (`{"atualizado": "...", "leads": [...]}`) — é o fallback para quem abre sem servidor.

Use `scripts/sync-dashboard.py` para regenerar o snapshot e `scripts/backup-db.py` antes de migrações ou operações em lote.
Para ações em lote via terminal, use `scripts/batch-status.py STATUS SLUG... --confirm`; cada alteração é registrada na auditoria.

Se o banco não existir ainda (usuário antigo), crie-o e importe os leads do snapshot embutido no `dashboard.html` atual antes do upsert. Respeite edições do usuário: antes de regravar um lead, leia o registro atual do banco.

## O que o painel faz sozinho (não reimplementar)

Kanban drag & drop, edição em modal, exclusão, busca, paginação automática, funil, follow-ups (proposta 4+ dias), receita fechada/potencial, vista Contratos (status pendente/enviado/assinado + link do documento + pago) e vista Financeiro (recebido, a receber, MRR de manutenções, projeção 12 meses) — tudo no template. O plugin só mantém o BANCO correto e o snapshot em dia.
