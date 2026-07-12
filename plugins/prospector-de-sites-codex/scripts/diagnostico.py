#!/usr/bin/env python3
"""Diagnóstico local de instalação, permissões, portas e arquivos essenciais."""
from __future__ import annotations
import argparse, json, shutil, socket
from pathlib import Path
def main():
 p=argparse.ArgumentParser(); p.add_argument('--workspace',type=Path,default=Path.cwd()); a=p.parse_args(); root=a.workspace.resolve(); errors=[]
 for name in ('prospector-config.json','prospector.db','sites'):
  if not (root/name).exists(): errors.append(f'ausente: {name}')
 cfg=root/'prospector-config.json'
 if cfg.exists():
  try: json.loads(cfg.read_text(encoding='utf-8'))
  except Exception: errors.append('prospector-config.json inválido')
 for port in (8765,8766):
  s=socket.socket(); busy=s.connect_ex(('127.0.0.1',port))==0; s.close(); print(f'porta {port}: ' + ('ocupada' if busy else 'livre'))
 print('python:', shutil.which('python3') or shutil.which('python') or 'ausente')
 if errors:
  print('\n'.join('ERRO: '+e for e in errors)); raise SystemExit(1)
 print(f'OK: workspace {root}')
if __name__=='__main__': main()
