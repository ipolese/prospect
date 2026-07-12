#!/usr/bin/env python3
"""Relatório de possíveis duplicatas por domínio e telefone normalizados."""
from __future__ import annotations
import argparse, re, sqlite3
from pathlib import Path
def norm(value): return re.sub(r'[^a-z0-9]','',str(value or '').lower().replace('www.',''))
def main():
 p=argparse.ArgumentParser(); p.add_argument('--workspace',type=Path,default=Path.cwd()); a=p.parse_args(); c=sqlite3.connect(a.workspace/'prospector.db'); c.row_factory=sqlite3.Row
 rows=c.execute('SELECT slug,nome,siteAntigo,telefone,whatsapp FROM leads').fetchall(); groups={}
 for r in rows:
  for key in (norm(r['siteAntigo']), norm(r['telefone'] or r['whatsapp'])):
   if key: groups.setdefault(key,[]).append(r['slug'])
 for key, slugs in groups.items():
  if len(slugs)>1: print(key, ','.join(sorted(set(slugs))))
 c.close()
if __name__=='__main__': main()
