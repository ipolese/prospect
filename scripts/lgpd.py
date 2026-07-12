#!/usr/bin/env python3
"""Consentimento, exportação e exclusão de dados de um lead (LGPD)."""
from __future__ import annotations
import argparse, json, sqlite3
from datetime import datetime
from pathlib import Path
def main():
 p=argparse.ArgumentParser(); p.add_argument('acao',choices=['consentir','exportar','excluir']); p.add_argument('slug'); p.add_argument('--workspace',type=Path,default=Path.cwd()); p.add_argument('--confirm',action='store_true'); a=p.parse_args(); db=a.workspace/'prospector.db'; c=sqlite3.connect(db); c.row_factory=sqlite3.Row
 if a.acao=='consentir': c.execute('CREATE TABLE IF NOT EXISTS privacy_consent(slug TEXT PRIMARY KEY, finalidade TEXT, concedido_em TEXT, revogado_em TEXT)'); c.execute("INSERT OR REPLACE INTO privacy_consent VALUES(?,?,?,NULL)",(a.slug,'prospeccao-comercial',datetime.now().isoformat())); c.commit(); print('consentimento registrado')
 elif a.acao=='exportar':
  row=c.execute('SELECT * FROM leads WHERE slug=?',(a.slug,)).fetchone(); print(json.dumps(dict(row) if row else {},ensure_ascii=False,indent=2))
 else:
  if not a.confirm: raise SystemExit('use --confirm para excluir'); c.execute('DELETE FROM leads WHERE slug=?',(a.slug,)); c.execute('DELETE FROM privacy_consent WHERE slug=?',(a.slug,)); c.commit(); print('dados excluídos')
 c.close()
if __name__=='__main__': main()
