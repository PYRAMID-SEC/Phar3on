import tempfile
import unittest
from pathlib import Path

from phar3on.cli import main


class TestCLI(unittest.TestCase):
    def test_version_output(self):
        self.assertEqual(main(['--version']), 0)

    def test_decoy_generate(self):
        with tempfile.TemporaryDirectory() as tmp:
            folder = Path(tmp) / 'bait'
            self.assertEqual(main(['decoy', 'generate', str(folder)]), 0)
            self.assertTrue((folder / '.env').exists())
