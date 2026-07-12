#!/usr/bin/env python3
"""Migra o SQLite local de forma idempotente e registra a versão do schema."""
from __future__ import annotations
import argparse, sqlite3
from pathlib import Path
def main():
 p=argparse.ArgumentParser(); p.add_argument('--workspace',type=Path,default=Path.cwd()); a=p.parse_args(); db=a.workspace/'prospector.db'; c=sqlite3.connect(db)
 c.execute('CREATE TABLE IF NOT EXISTS schema_meta (chave TEXT PRIMARY KEY, valor TEXT NOT NULL)')
 c.execute('CREATE TABLE IF NOT EXISTS audit_log (id INTEGER PRIMARY KEY AUTOINCREMENT, lead_slug TEXT, evento TEXT NOT NULL, origem TEXT NOT NULL DEFAULT "system", antes_json TEXT, depois_json TEXT, criado_em TEXT DEFAULT (datetime("now","localtime")))')
 c.execute('CREATE TABLE IF NOT EXISTS leads_deleted AS SELECT *, datetime("now","localtime") AS removido FROM leads WHERE 0') if c.execute("SELECT 1 FROM sqlite_master WHERE type='table' AND name='leads'").fetchone() else None
 c.execute("INSERT INTO schema_meta(chave,valor) VALUES('version','2') ON CONFLICT(chave) DO UPDATE SET valor='2'")
 c.commit(); c.close(); print('SQLite schema versão 2')
if __name__=='__main__': main()
