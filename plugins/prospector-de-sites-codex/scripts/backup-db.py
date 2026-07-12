#!/usr/bin/env python3
"""Cria backup consistente e verifica integridade do banco."""
from __future__ import annotations
import argparse, shutil, sqlite3
from datetime import datetime
from pathlib import Path
def main() -> None:
    p=argparse.ArgumentParser(); p.add_argument('--workspace',type=Path,default=Path.cwd()); a=p.parse_args(); root=a.workspace.resolve(); db=root/'prospector.db'
    if not db.exists(): raise SystemExit('prospector.db não existe')
    conn=sqlite3.connect(db); ok=conn.execute('PRAGMA integrity_check').fetchone()[0]; conn.close()
    if ok != 'ok': raise SystemExit(f'integridade inválida: {ok}')
    dest=root/'backups'; dest.mkdir(exist_ok=True); target=dest/f"prospector-{datetime.now():%Y%m%d-%H%M%S}.db"; shutil.copy2(db,target); print(target)
if __name__=='__main__': main()
