import unittest
from pathlib import Path
from HIVE_MENU import choice, report_url
class HiveMenuTests(unittest.TestCase):
    def test_demo(self): self.assertEqual(choice('1')[-1],'demo')
    def test_guard(self): self.assertEqual(choice('2')[-1],'guard')
    def test_vault(self): self.assertEqual(choice('3')[-1],'vault')
    def test_invalid(self):
        with self.assertRaises(ValueError):choice('5')
    def test_launcher_targets_local_menu(self):
        self.assertIn('BLACK-HIVE-COMMAND-CENTER.py',(Path(__file__).parents[1]/'INSTALL-DESKTOP.sh').read_text())

class VaultOpenTests(unittest.TestCase):
    def test_open_vault_returns_none_when_missing(self):
        from unittest.mock import patch
        import HIVE_MENU
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as d, patch.object(HIVE_MENU, "ROOT", Path(d)):
            self.assertIsNone(report_url())
    def test_open_vault_file_uri(self):
        from unittest.mock import patch
        import HIVE_MENU
        from tempfile import TemporaryDirectory
        with TemporaryDirectory() as d, patch.object(HIVE_MENU, "ROOT", Path(d)):
            q=Path(d)/"HoneyReports"/"report.html"
            q.parent.mkdir()
            q.write_text("<html></html>")
            self.assertEqual(report_url(), q.resolve().as_uri())
