#!/usr/bin/env python3
"""Clientes leves para Gmail/Sheets usando token do ambiente."""
from __future__ import annotations
import json, os, urllib.parse, urllib.request
class GoogleAPI:
 def __init__(self, token=None): self.token=token or os.environ.get('GOOGLE_ACCESS_TOKEN')
 def request(self,url,method='GET',body=None):
  if not self.token: raise RuntimeError('GOOGLE_ACCESS_TOKEN ausente')
  req=urllib.request.Request(url,method=method,headers={'Authorization':'Bearer '+self.token,'Content-Type':'application/json'})
  with urllib.request.urlopen(req, json.dumps(body).encode() if body else None) as r: return json.loads(r.read())
class GmailConnector(GoogleAPI):
 def search(self,q): return self.request('https://gmail.googleapis.com/gmail/v1/users/me/messages?q='+urllib.parse.quote(q))
 def create_draft(self,raw_message): return self.request('https://gmail.googleapis.com/gmail/v1/users/me/drafts','POST',{'message':{'raw':raw_message}})
class SheetsConnector(GoogleAPI):
 def append(self,spreadsheet_id,range_name,values): return self.request(f'https://sheets.googleapis.com/v4/spreadsheets/{spreadsheet_id}/values/{urllib.parse.quote(range_name)}:append?valueInputOption=USER_ENTERED','POST',{'values':values})
