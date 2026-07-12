import importlib.util, tempfile, threading, unittest
from http.server import ThreadingHTTPServer
from pathlib import Path
from urllib.request import urlopen
def load(path):
 spec=importlib.util.spec_from_file_location('preview_http',path); m=importlib.util.module_from_spec(spec); spec.loader.exec_module(m); return m
preview=load(Path(__file__).parents[1]/'scripts/servidor-sites.py')
class PreviewHTTPTests(unittest.TestCase):
 def test_server_serves_allowed_site_and_blocks_secret(self):
  with tempfile.TemporaryDirectory() as tmp:
   root=Path(tmp); (root/'sites/demo').mkdir(parents=True); (root/'sites/demo/index.html').write_text('<h1>ok</h1>'); (root/'prospector-config.json').write_text('secret')
   try: server=ThreadingHTTPServer(('127.0.0.1',0), preview.handler_for(root))
   except PermissionError: self.skipTest('sandbox não permite abrir socket local')
   thread=threading.Thread(target=server.serve_forever,daemon=True); thread.start()
   try:
    base=f'http://127.0.0.1:{server.server_address[1]}'
    with urlopen(base+'/sites/demo/index.html') as response: self.assertEqual(response.status,200); self.assertIn('nosniff',str(response.headers).lower())
    with self.assertRaises(Exception): urlopen(base+'/prospector-config.json')
   finally: server.shutdown(); thread.join()
if __name__=='__main__': unittest.main()
