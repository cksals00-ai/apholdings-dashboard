import json,tempfile,unittest
from pathlib import Path
from unittest.mock import patch,MagicMock
import newsletter_control_probe as p
class ControlProbeTests(unittest.TestCase):
 def test_scope_only_replays_real_scope_checker_without_repeating_historical_news(self):
  with tempfile.TemporaryDirectory() as folder,patch.dict('os.environ',{'GITHUB_RUN_ID':'123'}),patch.object(p,'TextModel') as model,patch('newsletter_scope_controls.check') as scope,patch.object(p,'verify_controls') as history,patch.object(p,'controls_valid') as valid:
   p.run('/runtime',folder,scope_only=True)
   scope.assert_called_once();history.assert_not_called();valid.assert_not_called()
   self.assertTrue(json.loads(Path(folder,'controls.json').read_text())['scope_only'])
if __name__=='__main__':unittest.main()
