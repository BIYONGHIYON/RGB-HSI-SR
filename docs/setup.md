# 실행 환경과 기존 결과 사용

저장소 최상위에서 명령을 실행합니다. Python 3.10 이상과 해당 장치에 맞는 PyTorch를 먼저 설치하고 `python -m pip install -r SSA-MRN/requirements.txt`로 나머지 패키지를 설치하세요. `git submodule update --init --recursive`로 공식 core를 받습니다.

## 데이터와 가중치

LIB-HSI 데이터는 `SSA-MRN/data/dataset/RGB-HSI/LIB-HSI`에 두거나 `train_lib.py --data-root <실제 경로>`를 지정합니다. 원본 데이터는 Git에 넣지 않습니다. 기존 Windows 데이터 경로 `C:\CtrS\SSA-MRN\data\dataset\RGB-HSI\LIB-HSI`를 읽는 것도 가능합니다. 데이터를 복사·삭제할 필요는 없습니다.

기존 보고서의 `C:\CtrS-*`는 과거 실행 위치입니다. 모든 과거 경로를 새 위치라고 간주하지 마세요. 서버에만 있는 checkpoint는 먼저 별도 위치로 복사하고 SHA-256을 확인합니다. 과거 checkpoint 내부 config는 원본 그대로 보존합니다.

## 소규모 동작 확인

```bash
python SSA-MRN/scripts/train_lib.py --config SSA-MRN/configs/lib_rgb_hsi_joint17_k4_consistency_tiles.json --data-root /absolute/path/to/LIB-HSI --smoke
```

이 명령은 실제 소규모 학습을 수행하므로 GPU 사용 가능 여부를 확인한 뒤 실행합니다. 이관 과정에서는 실행하지 않았습니다. RGB11 가중치를 평가하려면 `export_results.py --help`의 checkpoint/data-root/output-dir 인수를 사용하세요. RGB11은 처음부터 10에폭만 학습한 모델이 아닙니다.

## Windows 원격 연결과 독립된 컨트롤러 준비

새 checkout에서 `.venv`를 만들거나 아래 `-PythonPath`에 사용할 Python을 명시합니다. 기존 팀 task와 다른 이름을 사용합니다.

```powershell
powershell -NoProfile -ExecutionPolicy Bypass -File scripts\setup-remote-control.ps1 -TaskName RGB-HSI-SR-Control -PythonPath "C:\RGB-HSI-SR\.venv\Scripts\pythonw.exe"
```

이는 컨트롤러만 시작합니다. 실제 학습은 별도로 요청해야 합니다. Windows 계정은 로그인 상태를 유지해야 하며, 클라이언트 SSH 연결 종료와 서버 로그아웃·종료는 다릅니다. 현재 서버에 이 task를 설치하거나 학습을 실행하지 않았습니다.

컨트롤러는 실행한 Python을 사용하고 설정의 `data_root`를 존중합니다. worker 환경에서 `RGB_HSI_DATA_ROOT`를 설정하면 그 값을 우선합니다. 팀 task를 덮어쓰지 않도록 같은 이름의 task가 있으면 등록을 거부합니다.

```powershell
python scripts\remote-training.py status
python scripts\remote-training.py logs --follow
```

새 학습을 준비할 때 선택한 config의 데이터 경로와 출력 경로를 검토하세요. 과거 `warm07` 컨트롤러는 실행 당시 생성한 config가 필요하며 자동으로 새 가중치나 설정을 만들지 않습니다.

기존 pilot 설정의 시작 가중치는 `SSA-MRN/experiments/checkpoints/imported/rgb07/best.pt`를 가리킵니다. RGB07 보고서의 원본 best를 그 위치로 복사하고 해시를 확인하거나, 사용하는 설정 파일에 실제 경로를 지정하세요. 파일이 없으면 실행을 진행하지 마세요. 기본 `remote-training.py`의 설정은 과거 RGB06 triple17이며, RGB07 기반을 실행할 때는 `--config SSA-MRN/configs/lib_rgb_hsi_joint17_k4_consistency_tiles.json`을 명시합니다. 이는 실행 예고가 아니라 설정 선택 방법입니다.
