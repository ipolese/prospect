#!/usr/bin/env python3
"""Planeja/retoma execução de Todos por nicho, com checkpoint JSON atômico."""
from __future__ import annotations
import argparse, json
from pathlib import Path
def main():
 p=argparse.ArgumentParser(); p.add_argument('--workspace',type=Path,default=Path.cwd()); p.add_argument('--nichos',nargs='+',required=True); p.add_argument('--done',action='append',default=[]); a=p.parse_args(); path=a.workspace/'.prospector-checkpoint.json'; data={'nichos':[n for n in a.nichos if n.lower()!='todos'],'concluidos':a.done,'atualizado':__import__('datetime').datetime.now().isoformat()}; tmp=path.with_suffix('.tmp'); tmp.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8'); tmp.replace(path); print(json.dumps(data,ensure_ascii=False))
if __name__=='__main__': main()
