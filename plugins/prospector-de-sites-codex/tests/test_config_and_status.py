import json, unittest
from pathlib import Path
ROOT=Path(__file__).parents[1]
class ConfigStatusTests(unittest.TestCase):
 def test_manifest_and_schema_exist(self):
  self.assertTrue((ROOT/'.codex-plugin/plugin.json').exists()); self.assertTrue((ROOT/'config.schema.json').exists()); json.loads((ROOT/'config.schema.json').read_text())
 def test_pipeline_states_are_documented(self):
  text=(ROOT/'skills/dashboard-leads/references/dashboard-server.py').read_text()
  for state in ('negociacao','perdido','proposta-rascunho'): self.assertIn(state,text)
if __name__=='__main__': unittest.main()
