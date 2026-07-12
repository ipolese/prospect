#!/usr/bin/env python3
"""Captura screenshot de um site com Playwright instalado."""
import argparse
from pathlib import Path
def main():
 p=argparse.ArgumentParser(); p.add_argument('url'); p.add_argument('output',type=Path); p.add_argument('--width',type=int,default=1440); p.add_argument('--height',type=int,default=900); a=p.parse_args()
 try: from playwright.sync_api import sync_playwright
 except ImportError: raise SystemExit('instale Playwright para capturas automáticas')
 with sync_playwright() as pw:
  browser=pw.chromium.launch(headless=True); page=browser.new_page(viewport={'width':a.width,'height':a.height}); page.goto(a.url,wait_until='networkidle',timeout=30000); page.screenshot(path=str(a.output),full_page=True); browser.close()
 print(a.output)
if __name__=='__main__': main()
