#!/usr/bin/env python3
"""Regenera o snapshot do dashboard a partir do SQLite, sem expor segredos."""
from __future__ import annotations
import argparse, json, sqlite3
from datetime import datetime
from pathlib import Path

def main() -> None:
    p = argparse.ArgumentParser(); p.add_argument('--workspace', type=Path, default=Path.cwd()); args = p.parse_args()
    root = args.workspace.resolve(); db = root/'prospector.db'; template = root/'dashboard-template.html'; out = root/'dashboard.html'
    if not db.exists() or not template.exists(): raise SystemExit('prospector.db e dashboard-template.html são obrigatórios')
    conn = sqlite3.connect(db); conn.row_factory = sqlite3.Row
    leads = [dict(row) for row in conn.execute('SELECT * FROM leads ORDER BY atualizado DESC, nome').fetchall()]; conn.close()
    snapshot = json.dumps({'atualizado': datetime.now().isoformat(timespec='seconds'), 'leads': leads}, ensure_ascii=False)
    html = template.read_text(encoding='utf-8')
    start = '<script id="dados" type="application/json">'; end = '</script>'
    a = html.find(start); b = html.find(end, a + len(start)) if a >= 0 else -1
    if a < 0 or b < 0: raise SystemExit('template sem bloco JSON dados')
    out.write_text(html[:a+len(start)] + snapshot + html[b:], encoding='utf-8')
    print(f'Dashboard regenerado: {len(leads)} leads')
if __name__ == '__main__': main()
