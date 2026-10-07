# 개인 연구 저장소 이관

- 원본: [CtrS `23c4d9b`](https://github.com/BIYONGHIYON/CtrS/tree/23c4d9b86fed044d4578d397e533a4f9e9e4ada5)
- 새 연구 저장소: [RGB-HSI-SR](https://github.com/BIYONGHIYON/RGB-HSI-SR)
- 이관일: 2026-10-07

RGB–HSI 코드·RGB01~11 보고서·예비실험·정합 기록·수치·이미지·오프라인 HTML 및 원본 Git에 있는 가중치를 복사했습니다. 원본 전체 Git 역사는 소유자의 로컬 `CtrS-archive-20261007/repository.bundle`에 보존합니다. CtrS 공개 이력은 PAN–MS 경로만 남기도록 재작성했고, 이 개인 저장소는 출처를 기록한 스냅샷으로 시작합니다. 원본 커밋 URL은 재작성 뒤 공개 브랜치에서 접근되지 않을 수 있습니다. 과거 커밋 작성자나 실험 날짜를 새 이관 작성자로 소급하지 않습니다.

공식 SSA-MRN submodule은 같은 커밋을 유지합니다. 공통 PAN–MS 모델 코드는 RGB core의 의존성이며, PAN K4/K6 보고서·결과·가중치는 출처 확인용으로 복사했습니다. PAN–MS 개선 연구의 현재 저장소는 CtrS입니다. ECRformer 코드와 결과는 이 저장소에 옮기지 않았습니다.

## 보존 검증

[source_manifest.json](migration/source_manifest.json)은 이관 전 파일별 SHA-256입니다. [team_removed_paths.json](migration/team_removed_paths.json)은 CtrS 정리 브랜치에서 제거한 경로 목록이며 모두 개인 사본에 먼저 복사했습니다. 문서 URL·실행 경로 등 이관 중 바뀐 파일은 [verification.json](migration/verification.json)에 기록합니다. 가중치·평가 JSON·이미지·기존 HTML은 그대로 보존합니다.

RGB11 등 보고서에 서버 경로로만 기록된 best/latest는 여전히 서버에 있습니다. 이관은 그 경로·해시를 보존하며 서버 파일을 이동하거나 삭제하지 않습니다. 과거 checkpoint 안의 config와 파일 해시도 수정하지 않습니다. 새 PC에서 사용하려면 원본을 복사한 뒤 설정의 데이터·가중치 경로를 해당 PC에 맞춰 지정하세요.

## 운영

새 데이터와 실행 결과는 로컬 경로에 둡니다. 새 개인 저장소의 컨트롤러 task와 출력 폴더는 팀 저장소와 구분합니다. 공유 GPU에서는 기존 사용 확인 절차를 유지합니다. 기존 CtrS Pages 링크는 새 뷰어가 배포된 뒤 이전 안내 페이지로 전환합니다.
