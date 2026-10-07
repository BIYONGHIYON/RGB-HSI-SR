"""Portable controller configuration; no server or training process is started."""
import importlib.util
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[2]

class RepositoryPathTests(unittest.TestCase):
    def test_controller_uses_config_or_environment_dataset(self):
        spec = importlib.util.spec_from_file_location('migration_controller', ROOT / 'scripts/remote-training.py')
        controller = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(controller)
        for override in (False, True):
            with self.subTest(override=override), tempfile.TemporaryDirectory() as temp:
                root = Path(temp)
                for name in ('data', 'external', 'runs', 'logs'):
                    (root/name).mkdir()
                cfg = root/'config.json'
                cfg.write_text(json.dumps({'data_root': 'data'}))
                environment = {'RGB_HSI_DATA_ROOT': str(root/'external')} if override else {}
                with patch.object(controller, 'ROOT', root), patch.object(controller, 'RUNS', root/'runs'), patch.object(controller, 'BASE', root/'logs'), patch.dict(os.environ, environment, clear=True):
                    result = controller.prepare({'id':'test', 'mode':'start', 'config':str(cfg)})
                snapshot = json.loads((Path(result['log']).parent/'config.json').read_text())
                self.assertEqual(Path(snapshot['data_root']), root/('external' if override else 'data'))
                self.assertEqual(Path(result['output']), root/'runs/test')
                self.assertTrue(Path(result['command'][0]).is_file())
                self.assertNotIn('C:/CtrS', result['command'][0])
                self.assertEqual(json.loads(cfg.read_text()), {'data_root':'data'})

if __name__ == '__main__':
    unittest.main()
