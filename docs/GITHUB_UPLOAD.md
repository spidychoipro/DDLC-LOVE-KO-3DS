# GitHub 업로드

1. 이 `GitHub-ready` 폴더 안의 파일만 저장소 소스로 올립니다.
2. 저장소 설명 예시: `Nintendo 3DS DDLC-LOVE Korean localization tools using the native 3DS software keyboard.`
3. 저장소 이름 예시: `DDLC-LOVE-KO-3DS`.
4. GitHub 웹의 **Add file → Upload files** 또는 Git을 사용합니다. `.github`와 `.gitignore` 같은 숨김 파일도 포함합니다.
5. 업로드 후 Actions의 `Native keyboard and source checks` 결과를 확인합니다.

현재 정리된 상태:

- 소스는 `main`에 버전별 커밋 6개로 들어 있고, 각 커밋에 `v0.2.0-beta` ~ `v0.2.5-beta` 태그가 붙어 있습니다.
- 각 태그마다 릴리스가 있고, 릴리스 자산으로 그 버전의 소스 ZIP을 붙였습니다.
- `v0.2.5-beta`에는 로컬에서 빌드한 `DDLC-LOVE-KO-0.2.5.cia`, `.3dsx`, `SHA256SUMS.txt`도 붙였습니다. 설치 QR은 `docs/install-qr.png`이고 링크는 이 릴리스 CIA 직링크입니다.

원본 패치 ZIP, DSP 펌웨어, 게임 저장 데이터는 저장소에도 릴리스에도 넣지 않습니다. 다른 사람이 빌드할 때는 README에 연결된 원 배포처에서 입력 파일을 준비하도록 안내합니다. CIA·3DSX에는 게임 자산과 번역이 들어 있으므로 다시 배포할 때는 원 배포처 정책을 확인해야 합니다.

`dist/`와 `work/`는 빌드 결과이며 `.gitignore`에 포함됩니다. 전체 배포 폴더를 통째로 GitHub에 드래그하지 마세요.

릴리스 설명은 `CHANGELOG.md`의 해당 버전 항목을 바탕으로 작성했습니다. 실기 완주가 끝나기 전에는 완전 검증된 정식판이라고 표기하지 않습니다.
