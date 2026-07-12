#!/usr/bin/env python3
"""Validação local do manifesto sem depender de PyYAML ou rede."""
import json, sys
from pathlib import Path
def main():
 root=Path(sys.argv[1] if len(sys.argv)>1 else '.'); p=root/'.codex-plugin/plugin.json'; d=json.loads(p.read_text(encoding='utf-8')); required=('name','version','description','author','skills','interface')
 missing=[k for k in required if k not in d];
 if missing or d['author'].get('name') in (None,'') or d['interface'].get('displayName') in (None,''): raise SystemExit('manifesto inválido: '+','.join(missing))
 print('Manifesto válido:',p)
if __name__=='__main__': main()
