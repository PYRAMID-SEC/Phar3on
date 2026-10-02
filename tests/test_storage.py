import tempfile
import unittest
from pathlib import Path

from phar3on.config import Phar3onConfig
from phar3on.storage import Storage


class TestStorage(unittest.TestCase):
    def test_storage_roundtrip(self):
        with tempfile.TemporaryDirectory() as tmp:
            config = Phar3onConfig(data_dir=Path(tmp), db_path=Path(tmp) / 'events.db')
            storage = Storage(config)
            storage.add_event({'id': 'evt-1', 'timestamp': '2024-01-01', 'source_ip': '127.0.0.1', 'event_type': 'test', 'severity': 'LOW', 'details': {'ok': True}, 'mitre_ids': ['T1110']})
            events = storage.get_events('127.0.0.1')
            self.assertEqual(len(events), 1)
            storage.close()
