import unittest

from phar3on.brain.scoring import score_session


class TestScoring(unittest.TestCase):
    def test_session_score_and_label(self):
        session = [
            {'event_type': 'port_scan'},
            {'event_type': 'web_probe'},
            {'event_type': 'credential_bruteforce'},
            {'event_type': 'bait_access'},
        ]
        score, label, reasons, stage = score_session(session)
        self.assertGreater(score, 0)
        self.assertIn(label, {'LOW', 'MEDIUM', 'HIGH', 'CRITICAL'})
        self.assertTrue(reasons)
        self.assertIn(stage, {'Recon', 'Credential Access', 'Collection'})
