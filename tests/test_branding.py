import pathlib
import unittest

ROOT = pathlib.Path(__file__).resolve().parents[1]


class TestBranding(unittest.TestCase):
    def test_license_and_headers(self):
        license_text = (ROOT / 'LICENSE').read_text(encoding='utf-8')
        self.assertIn('Ahmed Tarek Salah', license_text)
        for py_file in (ROOT / 'src').rglob('*.py'):
            text = py_file.read_text(encoding='utf-8')
            self.assertTrue(text.startswith('# Phar3on - Built by Ahmed Tarek Salah - Copyright (c) 2026 Ahmed Tarek Salah - MIT License'))
