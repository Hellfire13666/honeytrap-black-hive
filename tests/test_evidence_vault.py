import json, tempfile, unittest, sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]))
from EVIDENCE_VAULT import create,read_events
class EvidenceVaultTests(unittest.TestCase):
    def test_empty(self):
        with tempfile.TemporaryDirectory() as t:
            folder=Path(t); result=create(folder)
            self.assertEqual(result['event_count'],0)
            self.assertTrue((folder/'report.html').exists())
    def test_sanitize_and_aggregate(self):
        with tempfile.TemporaryDirectory() as t:
            folder=Path(t)
            event={'timestamp_utc':'2026-11-01T20:00:00+00:00','path':'/admin','method':'GET','category':'ADMIN DECOY','visitor_fingerprint':'abc','cookie':'super-secret','ip':'192.0.2.1'}
            (folder/'events.jsonl').write_text(json.dumps(event)+'\nnot-json\n'+json.dumps(event)+'\n')
            result=create(folder)
            self.assertEqual(result['event_count'],2)
            self.assertEqual(result['fingerprints'],1)
            self.assertEqual(result['routes']['/admin'],2)
            for filename in ['report.html','summary.json','events-sanitized.csv']:
                contents=(folder/filename).read_text()
                self.assertNotIn('super-secret',contents)
                self.assertNotIn('192.0.2.1',contents)
    def test_html_escape(self):
        with tempfile.TemporaryDirectory() as t:
            folder=Path(t)
            (folder/'events.jsonl').write_text(json.dumps({'path':'<script>alert(1)</script>'})+'\n')
            create(folder)
            s=(folder/'report.html').read_text()
            self.assertNotIn('<script>alert(1)</script>',s)
            self.assertIn('&lt;script&gt;',s)
if __name__=='__main__':unittest.main()
