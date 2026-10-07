# RGB-HSI-SR

고해상도 RGB와 저해상도 HSI를 결합하는 **개인 RGB–HSI 공간 초해상도 연구**입니다. CtrS에서 진행한 RGB01~RGB11 연구를 분리했습니다. 팀의 PAN–MS 팬샤프닝 재현·성능 개선은 [CtrS](https://github.com/BIYONGHIYON/CtrS)에서 진행합니다.

| 문서 | 내용 |
|---|---|
| [현재 연구](SSA-MRN/README.md) | RGB11 결과, 해석 및 대표 이미지 |
| [연구 설명](SSA-MRN/docs/research.md) | 17특징·공동 디코더·23탭·LR 일관성·손실 |
| [이전 실험](SSA-MRN/docs/previous_experiments.md) | RGB01~11과 예비실험 |
| [204밴드 웹뷰어](https://biyonghiyon.github.io/RGB-HSI-SR/ssa-mrn/) | RGB11의 고정 5장면 |
| [실행 방법](docs/setup.md) | 환경·데이터 경로·원격 실행 준비 |
| [이관 기록](MIGRATION.md) | 출처, 보존 파일 및 서버 가중치 범위 |

## 현재 결과

LIB-HSI 합성 area ×4, 204밴드, train393 / validation45 / test75입니다. RGB11은 RGB07 계열의 구조에 HSI 경계 손실을 더한 추가 학습 실험입니다.

| test75 · 300타일 | MSE ↓ | PSNR dB ↑ | SAM ° ↓ |
|---|---:|---:|---:|
| 23탭 + LR 보정 | 0.0011539606 | 30.0649 | 2.44504 |
| 동일 학습량 대조군 | 0.0004378418 | 34.3916 | 2.15071 |
| RGB11 선택 후보 | 0.0004376169 | 34.3948 | 2.14986 |

대조군 대비 PSNR +0.0032 dB, SAM −0.00085°로 개선 폭은 작습니다. 실제 센서 HR-HSI 정답 평가가 아니며, RGB09보다 평균 MSE는 높습니다. 이전 시험셋을 반복 확인했다는 한계도 유지합니다.

![RGB11 예시: LR HSI · RGB · 예측 · 정답](SSA-MRN/docs/assets/rgb11_gradient_suite/sample_01.png)

## 코드 받기

```bash
git clone --recurse-submodules https://github.com/BIYONGHIYON/RGB-HSI-SR.git
cd RGB-HSI-SR
```

기존 체크포인트와 스크립트의 상대 경로 호환성을 위해 `SSA-MRN/` 구조를 유지합니다. 공식 upstream 및 PAN–MS 기반 코드·보고서는 연구 출처 확인용 스냅샷입니다. 원본 데이터는 포함하지 않습니다. Git에 이미 보관된 가중치는 복사했고, 서버에만 있는 가중치는 기존 보고서의 위치·해시를 보존했습니다. 새 학습은 이 이관 작업에서 시작하지 않았습니다.
