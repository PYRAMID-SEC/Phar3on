import tempfile
import unittest
from pathlib import Path

from phar3on.chainlog import ChainLog


class TestChainLog(unittest.TestCase):
    def test_hash_chain_verifies_and_catches_tampering(self):
        with tempfile.TemporaryDirectory() as tmp:
            path = Path(tmp) / 'evidence.jsonl'
            log = ChainLog(path)
            log.append({'event': 'alpha'})
            log.append({'event': 'beta'})
            ok, problems = log.verify()
            self.assertTrue(ok)
            self.assertEqual(problems, [])

            lines = path.read_text(encoding='utf-8').splitlines()
            modified = lines[0].replace('alpha', 'gamma')
            path.write_text(modified + '\n' + '\n'.join(lines[1:]), encoding='utf-8')
            ok, problems = log.verify()
            self.assertFalse(ok)
            self.assertTrue(any('Tampering' in p for p in problems))
