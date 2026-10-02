import unittest

from phar3on.sanitize import html_escape, sanitize_text


class TestSanitize(unittest.TestCase):
    def test_ansi_and_xss_are_removed(self):
        payload = '\x1b[31mhello\n<script>alert(1)</script>'
        out = sanitize_text(payload)
        self.assertNotIn('script', out.lower())
        self.assertIn('hello', out)
        self.assertEqual(html_escape('<script>alert(1)</script>'), '&lt;script&gt;alert(1)&lt;/script&gt;')
