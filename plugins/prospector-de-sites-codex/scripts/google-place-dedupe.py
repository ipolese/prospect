#!/usr/bin/env python3
"""Importa place_id e marca duplicatas; a coleta do Maps permanece no navegador autorizado."""
from __future__ import annotations
import argparse, json, sqlite3
from pathlib import Path
def main():
 p=argparse.ArgumentParser(); p.add_argument('json',type=Path); p.add_argument('--workspace',type=Path,default=Path.cwd()); a=p.parse_args(); rows=json.loads(a.json.read_text(encoding='utf-8')); c=sqlite3.connect(a.workspace/'prospector.db');
 for row in rows:
  if not row.get('placeId') or not row.get('slug'): continue
  c.execute('UPDATE leads SET placeId=? WHERE slug=?',(row['placeId'],row['slug']))
 c.commit(); dup=c.execute('SELECT placeId,group_concat(slug) FROM leads WHERE placeId IS NOT NULL GROUP BY placeId HAVING count(*)>1').fetchall(); c.close(); print('duplicatas place_id:',dup)
if __name__=='__main__': main()
