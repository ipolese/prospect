#!/usr/bin/env python3
"""Valida sinais visuais estáticos: links, overflow e contraste básico."""
import argparse,re
from pathlib import Path
def main():
 p=argparse.ArgumentParser(); p.add_argument('html',type=Path); a=p.parse_args(); s=a.html.read_text(encoding='utf-8'); errors=[]
 if re.search(r'width\s*:\s*\d{4,}px',s,re.I): errors.append('largura fixa excessiva')
 if re.search(r'href=["\'](?:#|javascript:)[^"\']*["\']',s,re.I): errors.append('link vazio/javascript')
 if re.search(r'color:\s*#(?:fff|ffffff)\b[^}]*background:\s*#(?:fff|ffffff)\b',s,re.I): errors.append('possível contraste insuficiente')
 if errors: print('\n'.join(errors)); raise SystemExit(1)
 print('checagem visual estática OK; confirmar com navegador')
if __name__=='__main__': main()
