#!/usr/bin/env python3
"""Configura OAuth Google por variáveis de ambiente e arquivo local seguro."""
import argparse, json, os
from pathlib import Path
def main():
 p=argparse.ArgumentParser(); p.add_argument('--workspace',type=Path,default=Path.cwd()); p.add_argument('--token'); a=p.parse_args(); cfg=a.workspace/'.google-oauth.json'; data={'client_id':os.getenv('GOOGLE_CLIENT_ID',''),'scopes':['https://www.googleapis.com/auth/gmail.modify','https://www.googleapis.com/auth/spreadsheets']}
 if a.token: data['access_token']=a.token
 cfg.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8'); os.chmod(cfg,0o600); print('OAuth configurado em',cfg)
if __name__=='__main__': main()
