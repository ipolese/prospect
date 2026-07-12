#!/usr/bin/env python3
"""Reverte um lote usando audit_log; exige confirmação."""
import argparse, json, sqlite3
from pathlib import Path
def main():
 p=argparse.ArgumentParser(); p.add_argument('event_ids',nargs='+',type=int); p.add_argument('--workspace',type=Path,default=Path.cwd()); p.add_argument('--confirm',action='store_true'); a=p.parse_args()
 if not a.confirm: raise SystemExit('use --confirm')
 c=sqlite3.connect(a.workspace/'prospector.db'); c.row_factory=sqlite3.Row
 for eid in a.event_ids:
  row=c.execute('SELECT * FROM audit_log WHERE id=?',(eid,)).fetchone()
  if not row or not row['antes_json']: continue
  before=json.loads(row['antes_json']); sets=[k for k in before if k not in ('slug','atualizado')]
  c.execute('UPDATE leads SET '+','.join(k+'=?' for k in sets)+' WHERE slug=?',[before[k] for k in sets]+[row['lead_slug']])
 c.commit(); c.close(); print('rollback concluído')
if __name__=='__main__': main()
