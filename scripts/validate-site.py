#!/usr/bin/env python3
"""Valida requisitos estruturais básicos de uma página de cliente."""
from __future__ import annotations
import argparse, re
from pathlib import Path
def main():
 p=argparse.ArgumentParser(); p.add_argument('html',type=Path); a=p.parse_args(); text=a.html.read_text(encoding='utf-8'); errors=[]
 if re.search(r'\{\{|__\w+__|lorem ipsum', text, re.I): errors.append('placeholder ou lorem ipsum encontrado')
 if not re.search(r'<title>\s*[^<]+</title>', text, re.I): errors.append('title ausente')
 if not re.search(r'<meta[^>]+name=["\']description["\'][^>]+content=["\'][^"\']+', text, re.I): errors.append('meta description ausente')
 if '<meta name="viewport"' not in text.lower(): errors.append('viewport ausente')
 if '<link rel="canonical"' not in text.lower(): errors.append('canonical ausente')
 if 'property="og:title"' not in text.lower(): errors.append('Open Graph og:title ausente')
 if '<script type="application/ld+json"' not in text.lower(): errors.append('JSON-LD ausente')
 if re.search(r'<img(?![^>]+\balt=)[^>]*>', text, re.I): errors.append('imagem sem alt')
 if re.search(r'http://', text, re.I): errors.append('referência http encontrada; revisar HTTPS')
 if errors:
  print('\n'.join(f'ERRO: {e}' for e in errors)); raise SystemExit(1)
 print(f'OK: {a.html}')
if __name__=='__main__': main()
