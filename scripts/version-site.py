#!/usr/bin/env python3
"""Salva uma versão nomeada de uma página antes de edição/publicação."""
from __future__ import annotations
import argparse, shutil
from datetime import datetime
from pathlib import Path
def main():
 p=argparse.ArgumentParser(); p.add_argument('html',type=Path); p.add_argument('--label',default='backup'); a=p.parse_args(); src=a.html.resolve()
 if not src.is_file() or src.suffix.lower()!='.html': raise SystemExit('arquivo HTML inválido')
 dest=src.parent/'versions'; dest.mkdir(exist_ok=True); target=dest/f'{src.stem}-{datetime.now():%Y%m%d-%H%M%S}-{a.label}.html'; shutil.copy2(src,target); print(target)
if __name__=='__main__': main()
