import tempfile, unittest
from pathlib import Path
from LIVE_SIGNAL import handler_factory,summary,DEMO_PATHS
from honeytrap import safe_event,save_event
from EVIDENCE_VAULT import create
class SignalTests(unittest.TestCase):
 def test_allowed_demo(self): self.assertEqual(DEMO_PATHS['/demo/admin'],'/admin')
 def test_safe_event_fields(self):
  e=safe_event('/admin','GET','127.0.0.1','salt')
  self.assertNotIn('ip',e)
  self.assertNotIn('headers',e)
 def test_report(self):
  with tempfile.TemporaryDirectory() as d:
   folder=Path(d)
   save_event(folder,safe_event('/admin','GET','127.0.0.1','salt'))
   s=create(folder)
   self.assertEqual(s['event_count'],1)
   self.assertEqual(summary(folder)['/admin'],1)
