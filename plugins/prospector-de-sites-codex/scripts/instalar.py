#!/usr/bin/env python3
"""Instala arquivos operacionais na pasta de trabalho sem credenciais."""
from __future__ import annotations
import argparse, shutil
from pathlib import Path
def main():
 p=argparse.ArgumentParser(); p.add_argument('--workspace',type=Path,default=Path.cwd()); p.add_argument('--plugin',type=Path,default=Path(__file__).parents[1]); a=p.parse_args(); root=a.workspace.resolve(); root.mkdir(parents=True,exist_ok=True); (root/'sites').mkdir(exist_ok=True); (root/'backups').mkdir(exist_ok=True)
 for src in [a.plugin/'scripts/servidor-sites.py',a.plugin/'scripts/dashboard-server.py',a.plugin/'skills/dashboard-leads/references/dashboard-server.py',a.plugin/'skills/dashboard-leads/references/dashboard-app.js']:
  if src.exists(): shutil.copy2(src,root/src.name)
 print('Instalação local concluída:',root)
if __name__=='__main__': main()
