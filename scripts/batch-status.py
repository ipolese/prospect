#!/usr/bin/env python3
"""Altera status de um lote de leads com confirmação e registro de auditoria."""
from __future__ import annotations
import argparse, json, sqlite3
from pathlib import Path
VALID={'novo','redesenhado','publicado-local','publicado','proposta-rascunho','proposta','respondeu','negociacao','fechado','perdido','descartado'}
def main():
 p=argparse.ArgumentParser(); p.add_argument('status',choices=sorted(VALID)); p.add_argument('slugs',nargs='+'); p.add_argument('--workspace',type=Path,default=Path.cwd()); p.add_argument('--confirm',action='store_true'); a=p.parse_args()
 if not a.confirm: raise SystemExit('use --confirm para alterar o lote')
 c=sqlite3.connect(a.workspace/'prospector.db'); c.row_factory=sqlite3.Row; count=0
 for slug in a.slugs:
  row=c.execute('SELECT * FROM leads WHERE slug=?',(slug,)).fetchone()
  if not row: continue
  c.execute("UPDATE leads SET status=?, atualizado=datetime('now','localtime') WHERE slug=?",(a.status,slug)); c.execute('INSERT INTO audit_log(lead_slug,evento,origem,antes_json,depois_json) VALUES(?,?,?,?,?)',(slug,'batch-status','batch',json.dumps(dict(row),ensure_ascii=False),json.dumps({'status':a.status},ensure_ascii=False))); count+=1
 c.commit(); c.close(); print('atualizados:',count)
if __name__=='__main__': main()
