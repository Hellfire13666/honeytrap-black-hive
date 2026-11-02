import json
import tempfile
import unittest
from pathlib import Path
from honeytrap import safe_event, save_event, classify, demo, report

class BlackHiveTests(unittest.TestCase):
    def test_decoy(self): self.assertEqual(classify('/.env'),'CONFIG DECOY')
    def test_unknown_sanitized(self):
        e=safe_event('/private?secret=a','POST','192.0.2.1','salt')
        self.assertEqual(e['path'],'/other')
        self.assertNotIn('192.0.2.1',str(e))
        self.assertNotIn('secret',str(e))
    def test_stable_fingerprint(self):
        self.assertEqual(safe_event('/admin','GET','127.0.0.1','salt')['visitor_fingerprint'],safe_event('/admin','GET','127.0.0.1','salt')['visitor_fingerprint'])
    def test_distinct_salts(self): self.assertNotEqual(safe_event('/admin','GET','127.0.0.1','a')['visitor_fingerprint'],safe_event('/admin','GET','127.0.0.1','b')['visitor_fingerprint'])
    def test_save_and_report(self):
        with tempfile.TemporaryDirectory() as d:
            folder=Path(d)
            save_event(folder,safe_event('/admin','GET','127.0.0.1','x'))
            report(folder)
            self.assertTrue((folder/'report.html').is_file())
            self.assertEqual(json.loads((folder/'events.jsonl').read_text().splitlines()[0])['path'],'/admin')
    def test_demo(self):
        with tempfile.TemporaryDirectory() as d:
            folder=Path(d)
            demo(folder)
            self.assertEqual(len((folder/'events.jsonl').read_text().splitlines()),3)
if __name__=='__main__': unittest.main()
