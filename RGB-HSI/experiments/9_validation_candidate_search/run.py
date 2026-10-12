"""축소 학습셋의 구조 후보 비교 실행 진입점. 실행 옵션과 설정은 명시적으로 지정합니다."""
from pathlib import Path
import subprocess
import sys

ROOT = Path(__file__).resolve().parents[3]
HERE = Path(__file__).resolve().parent
if __name__ == '__main__':
    args = sys.argv[1:]
    if '--config' not in args and (HERE / 'config.json').is_file():
        args = ['--config', str(HERE / 'config.json'), *args]
    raise SystemExit(subprocess.call([sys.executable, str(ROOT / 'RGB-HSI/common/train.py'), *args], cwd=ROOT))
