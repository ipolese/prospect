#!/usr/bin/env python3
"""Calendário local de tarefas/follow-ups."""
import argparse, json
from datetime import datetime
from pathlib import Path
def main():
 p=argparse.ArgumentParser(); p.add_argument('acao',choices=['add','list']); p.add_argument('--workspace',type=Path,default=Path.cwd()); p.add_argument('--slug'); p.add_argument('--data'); p.add_argument('--texto'); a=p.parse_args(); f=a.workspace/'tasks.json'; tasks=json.loads(f.read_text()) if f.exists() else []
 if a.acao=='add': tasks.append({'slug':a.slug,'data':a.data or datetime.now().date().isoformat(),'texto':a.texto or 'Follow-up','concluida':False}); f.write_text(json.dumps(tasks,ensure_ascii=False,indent=2)); print('tarefa criada')
 else: print(json.dumps(tasks,ensure_ascii=False,indent=2))
if __name__=='__main__': main()
