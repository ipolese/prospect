#!/usr/bin/env python3
"""Remove leads descartados antigos após confirmação explícita de retenção."""
from __future__ import annotations
import argparse, sqlite3
from datetime import datetime, timedelta
from pathlib import Path
def main():
 p=argparse.ArgumentParser(); p.add_argument('--workspace',type=Path,default=Path.cwd()); p.add_argument('--days',type=int,default=365); p.add_argument('--confirm',action='store_true'); a=p.parse_args()
 if not a.confirm: raise SystemExit('use --confirm para executar a retenção')
 c=sqlite3.connect(a.workspace/'prospector.db'); cutoff=(datetime.now()-timedelta(days=a.days)).strftime('%Y-%m-%d %H:%M:%S'); c.execute("DELETE FROM leads WHERE status='descartado' AND atualizado < ?",(cutoff,)); print('removidos:',c.total_changes); c.commit(); c.close()
if __name__=='__main__': main()
