#!/usr/bin/env python3
"""Valida instalação cross-platform sem modificar credenciais."""
import argparse, shutil, sys
from pathlib import Path
def main():
 p=argparse.ArgumentParser(); p.add_argument('--workspace',type=Path,default=Path.cwd()); a=p.parse_args(); errors=[]
 for f in ('prospector-config.json','prospector.db','sites','dashboard-server.py','dashboard-app.js','servidor-sites.py'):
  if not (a.workspace/f).exists(): errors.append(f)
 print('python:',sys.version.split()[0],'platform:',sys.platform,'curl:',bool(shutil.which('curl')))
 if errors: print('ausentes:',', '.join(errors)); raise SystemExit(1)
 print('instalação OK')
if __name__=='__main__': main()
