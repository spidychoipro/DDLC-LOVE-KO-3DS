# GitHub 업로드

1. 이 `GitHub-ready` 폴더 안의 파일만 새 저장소에 올립니다.
2. 저장소 설명 예시: `Nintendo 3DS DDLC-LOVE Korean localization tools using the native 3DS software keyboard.`
3. 저장소 이름 예시: `DDLC-LOVE-KO-3DS`.
4. GitHub 웹의 **Add file → Upload files** 또는 Git을 사용합니다. `.github`와 `.gitignore` 같은 숨김 파일도 포함합니다.
5. 업로드 후 Actions의 `Native keyboard and source checks` 결과를 확인합니다.

소스는 버전별 커밋과 태그(`v0.2.0-beta` ~ `v0.2.6-beta`)로 들어 있고, 각 태그마다 릴리스가 있습니다. 최신 릴리스에는 로컬에서 빌드한 CIA·3DSX와 `SHA256SUMS.txt`, 설치 QR을 함께 두고, README는 변경 내역 대신 `CHANGELOG.md`를 가리킵니다.

이 폴더 바깥에 있는 개인용 CIA/3DSX, 원본 패치 ZIP, DSP 파일, 게임 저장 데이터는 올리지 않습니다. 다른 사람이 빌드할 때는 README에 연결된 원 배포처에서 입력 파일을 준비하도록 안내합니다.

`dist/`와 `work/`는 빌드 결과이며 `.gitignore`에 포함됩니다. 전체 배포 폴더를 통째로 GitHub에 드래그하지 마세요.

릴리스 설명은 `CHANGELOG.md`의 0.2.6-beta 항목을 바탕으로 작성할 수 있습니다. 실기 완주가 끝나기 전에는 완전 검증된 정식판이라고 표기하지 않습니다.
