"""Dedicated disconnect-safe controller for the joint-17 LIB-HSI experiment."""
import importlib.util
from pathlib import Path

script = Path(__file__).resolve().parents[2] / 'common/controller.py'
spec = importlib.util.spec_from_file_location('ctrs_remote_training', script)
controller = importlib.util.module_from_spec(spec)
spec.loader.exec_module(controller)
controller.BASE = controller.ROOT / 'RGB-HSI/runtime/remote-control-joint17'
controller.RUNS = controller.ROOT / 'RGB-HSI/runtime/checkpoints-joint17'
controller.CONFIG = controller.ROOT / 'RGB-HSI/experiments/8_joint_decoder/config.json'

if __name__ == '__main__':
    controller.main()
