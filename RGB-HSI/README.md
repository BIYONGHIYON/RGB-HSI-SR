# RGB-HSI 연구·실행 안내

[연구 소개·기준 결과·실험 목록](../README.md) · [알고리즘 설명](docs/research.md)

## 폴더 구조

```text
RGB-HSI/
├── common/                  RGB 모델·데이터 로더·손실·평가·결과 출력
├── experiments/
│   ├── 1_latent_compression/
│   └── 14_hsi_gradient_loss/
│       ├── README.md         목적·변경·조건·수치·차이·그래프·이미지·판정
│       ├── run.py            해당 실험 실행 진입점
│       ├── config.json       보관된 실행 설정이 있는 경우
│       ├── checkpoints/      로컬에 보관한 실제 best/latest 가중치
│       └── results/          수치·장면 선택·해시·compact 기록·figures/
├── data/                    LIB-HSI 원본 데이터; Git에서 제외
├── docs/                    연구 설명·공통 보고서 양식
├── references/              데이터 설명·공식 기반 코드·논문 재현 참고 자료
├── tests/                   RGB 공통 연산의 기존 검증 코드
└── runtime/                 새 실행 로그·출력; Git에서 제외
```

실험 번호는 오래된 순서이며 새 실험은 마지막 번호 다음에 추가합니다. 실험별 코드와 자료는 같은 폴더에 두고 공통 코드를 복제하지 않습니다. `best.pt`, `latest.pt`의 이름을 유지하고 후보·시드는 상위 폴더로 구분합니다. 가중치가 서버에만 있는 실험에는 빈 가중치나 임의 파일을 만들지 않습니다. 해당 보고서의 실제 경로와 해시를 확인합니다.

`common/lib_hsi.py`와 `common/registration.py`는 RGB-HSI 로딩과 정합에 필요하며, 평가 정의는 `common/train.py`에 유지했습니다. 기반 네트워크와 RGB용 adapter도 RGB 모델이 사용하므로 유지했습니다. PAN–MS 전용 로더·실행·미리보기는 포함하지 않습니다. 원본 수치·가중치 설정·학습 소스 해시는 수정하지 않습니다.

## 환경과 데이터

저장소 루트에서 실행합니다. Python 3.10 이상과 사용할 장치에 맞는 PyTorch를 설치합니다.

```bash
git submodule update --init RGB-HSI/references/upstream
python -m pip install -r RGB-HSI/requirements.txt
```

LIB-HSI는 `RGB-HSI/data/LIB-HSI`에 두거나 `--data-root`로 실제 경로를 지정합니다. 외장 SSD와 Windows의 기존 데이터를 이동할 필요는 없습니다.

## 기존 가중치 평가

체크포인트 내부 설정을 읽는 공통 진입점을 사용합니다. 학습을 시작하지 않으며 기존 결과를 덮어쓰지 않는 새 출력 폴더를 지정합니다.

```bash
python RGB-HSI/common/checkpoint.py \
  --checkpoint /absolute/path/to/best.pt \
  --data-root /absolute/path/to/LIB-HSI \
  --alignment-manifest RGB-HSI/experiments/7_lr_mean_consistency/results/alignment_manifest.json \
  --output-dir RGB-HSI/runtime/evaluation --device cpu
```

원래 정합을 사용하지 않은 가중치는 `--alignment-manifest`를 생략합니다. 동일한 정합 파일을 사용하며 체크포인트 내부 설정은 수정하지 않습니다. 과거 평가 장치·AMP 차이를 감안해야 합니다.

## 실험 실행과 결과 정리

실험 폴더의 `run.py --help`로 옵션을 확인합니다. 학습은 사용자의 명시적 요청과 공유 GPU 상태 확인 후 시작합니다. 보관 설정이 없는 과거 실험은 가중치 내부 설정을 사용해 평가하며 임의로 학습 설정을 복원하지 않습니다.

`common/export_results.py`는 고정 5장면, 수치, 그래프, 오프라인 204밴드 HTML과 report manifest를 생성합니다. `common/prepare_viewer_site.py`는 대표 연구 하나의 Pages 배포 파일을 준비합니다. 공개 주소는 기존 `/ssa-mrn/`을 유지하며 이전 뷰어는 각 실험의 `results/figures/band_viewer/`에 보관합니다.

원격 학습에 필요한 Windows 컨트롤러는 `common/controller.py`와 실험별 `controller.py`에 있습니다. `common/setup_controller.ps1`은 지정된 컨트롤러를 클라이언트 연결과 독립적으로 실행합니다. 실행 중인 외부 checkout·데이터·작업은 수정하지 않습니다.

[실험 보고서 양식](docs/experiment_template.md) · [실험 목록](experiments/catalog.json) · [관리 규칙](AGENTS.md)
