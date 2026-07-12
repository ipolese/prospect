#!/usr/bin/env python3
"""Pré-validação sem navegador; detecta sinais de layout não responsivo."""
import argparse,re
from pathlib import Path
def main():
 p=argparse.ArgumentParser(); p.add_argument('html',type=Path); a=p.parse_args(); s=a.html.read_text(encoding='utf-8').lower(); errors=[]
 if 'viewport' not in s: errors.append('viewport ausente')
 if 'media' not in s and 'clamp(' not in s: errors.append('nenhum breakpoint/clamp encontrado')
 if re.search(r'width\s*:\s*\d{4,}px',s): errors.append('largura fixa excessiva')
 if errors: print('\n'.join(errors)); raise SystemExit(1)
 print('estrutura responsiva mínima OK; valide também com navegador real')
if __name__=='__main__': main()
