import json, tempfile, unittest
from pathlib import Path
from LIVE_WATCH import collect, handler_factory, PAGE

class LiveWatchTests(unittest.TestCase):
    def test_empty(self):
        with tempfile.TemporaryDirectory() as t:
            d=collect(Path(t));self.assertEqual(d['total'],0);self.assertEqual(d['recent'],[])
    def test_sanitized(self):
        with tempfile.TemporaryDirectory() as t:
            p=Path(t);(p/'events.jsonl').write_text(json.dumps({'timestamp_utc':'2026-11-01T21:00:00Z','path':'/admin','method':'GET','category':'VOLUNTARY DEMO','visitor_fingerprint':'abc','cookie':'SECRET','ip':'1.2.3.4'})+'\n')
            result=collect(p);self.assertEqual(result['total'],1);self.assertEqual(result['routes']['/admin'],1)
            self.assertNotIn('SECRET',json.dumps(result));self.assertNotIn('1.2.3.4',json.dumps(result))
            self.assertNotIn('visitor_fingerprint',result['recent'][0])
    def test_page(self):
        self.assertIn('setInterval(poll,2000)',PAGE)
        self.assertIn('textContent',PAGE)
