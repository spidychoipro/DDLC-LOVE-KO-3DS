# DDLC-LOVE 한국어판 · Nintendo 3DS

[![Native keyboard and source checks](https://github.com/spidychoipro/DDLC-LOVE-KO-3DS/actions/workflows/tests.yml/badge.svg)](https://github.com/spidychoipro/DDLC-LOVE-KO-3DS/actions/workflows/tests.yml)

Nintendo 3DS용 [DDLC-LOVE](https://github.com/LukeZGD/DDLC-LOVE)에 기존 한국어 패치의 번역을 적용하는 비공식 개인 빌드 도구입니다. Team Salvato, LukeZGD, 한국어 패치 제작진의 공식 배포판이 아닙니다.

현재 버전은 **0.2.7-beta**입니다. 실제 3DS에 설치해 첫 실행 안내와 게임 진행이 정상인 것을 확인했고, Azahar에서도 같은 빌드가 동작합니다. 전체 루트와 엔딩을 끝까지 완주한 버전은 아닙니다.

버전별 수정 내역은 [CHANGELOG.md](CHANGELOG.md)에 따로 정리되어 있습니다.

## 주요 기능

- 구형 LovePotion의 바이트 단위 글꼴 출력을 보완하는 UTF-8 한글 렌더러
- 기존 한국어 패치와 Lua 대사를 대응시키는 로컬 변환 절차
- 대사 줄바꿈, 긴 대사와 시의 페이지 넘김
- 새 게임에서 Nintendo 3DS 기본 소프트웨어 키보드를 직접 호출
- 시스템 자판이 반환한 한글·영문·혼합 UTF-8 이름 저장 (최대 12글자)
- 현대 한글 완성형 11,172자에 대한 이름 출력용 글꼴 생성
- 일반 시와 특수 시 이미지의 한국어화
- `.3dsx`와 `.cia`의 로컬 생성 및 해시 검증
- 시작 단계 기록으로 첫 실행 문제를 추적하는 진단 로그

## 설치

### CIA (권장)

FBI → **Remote Install → Scan QR code** 로 아래 QR을 읽으면 CIA(73MB)를 바로 내려받아 설치합니다. 이 QR은 0.2.7-beta를 가리킵니다.

![DDLC-LOVE-KO CIA 설치 QR](docs/install-qr.png)

QR 직링크: <https://github.com/spidychoipro/DDLC-LOVE-KO-3DS/releases/download/v0.2.7-beta/DDLC-LOVE-KO-0.2.7.cia>

최신 릴리스 목록: <https://github.com/spidychoipro/DDLC-LOVE-KO-3DS/releases/latest>

SD 카드로 설치하려면 릴리스에서 `DDLC-LOVE-KO-<버전>.cia`를 받아 FBI → SD → **Install and delete CIA**를 사용합니다.

- Title ID: `0004000000DDFB00`
- 제품 코드: `CTR-P-DLKO`
- 홈브루 사운드용 `sdmc:/3ds/dspfirm.cdc`는 본인 기기에서 추출해 따로 준비해야 합니다.

CFW가 설치된 기기나 Azahar에서만 설치됩니다. 이 Title ID가 다른 모든 홈브루와 충돌하지 않는다고 보장하지는 않습니다.

### 3DSX / Azahar

`.3dsx` 파일에는 게임 데이터가 들어 있습니다. 실기에서는 SD 카드의 `/3ds/` 아래에 두고 Homebrew Launcher로 실행합니다. Azahar에서는 파일 열기로 `.3dsx`를 열거나 CIA를 설치합니다. Azahar의 가상 SD에도 DSP 파일이 필요합니다.

## 이름 입력

`새 게임`을 선택하면 **Nintendo 3DS 기본 소프트웨어 키보드**가 바로 열립니다. 게임이 그리는 자판이나 별도 한글 조합기는 사용하지 않습니다.

게임은 기본 자판에서 반환한 이름을 UTF-8로 그대로 저장하며, 마지막 한글 음절을 바이트 단위로 잘라내지 않습니다. 취소하면 타이틀 화면으로 돌아갑니다.

한글 입력 페이지가 있는지는 기기에 설치된 시스템 키보드·지역·언어 환경에 따라 다릅니다. 이 게임이 다른 지역 자판에 한글 페이지를 추가하거나 시스템 자판을 교체하지는 않습니다. 이름에 따옴표·역슬래시·제어 문자를 넣으면 저장 형식을 보호하기 위해 안내 메시지를 표시합니다.

## 저장 데이터

이전 한국어 테스트본과 같은 `DDLC-3DS-KO` 저장 식별자를 사용합니다. 실제 경로는 `sdmc:/3ds/data/LovePotion/DDLC-3DS-KO/`입니다. 업데이트 전에 이 폴더를 백업해 두는 것이 좋습니다.

## 직접 빌드

### 준비물

이 저장소에는 게임 전체, 번역 데이터 전체, 글꼴, Nintendo DSP 펌웨어, 개인 저장 데이터를 넣지 않습니다. 아래 파일은 각 배포처에서 직접 준비합니다.

1. [DDLC-LOVE v1.1.9](https://github.com/LukeZGD/DDLC-LOVE/releases/tag/v1.1.9)의 `DDLC-3DS.zip`
2. [두근두근 문예부 한국어화 패치](https://sites.google.com/view/dokidokikor)의 **1.2 일반 사용자용 normal ZIP**
3. CIA를 만들 경우 같은 v1.1.9의 `DDLC-3DS.cia`
4. [devkitPro](https://devkitpro.org/)의 `mkromfs3ds`, [Project_CTR makerom 0.19.0](https://github.com/3DSGuy/Project_CTR/releases/tag/makerom-v0.19.0)

원본 DDLC는 [공식 사이트](https://ddlc.moe/)에서 받을 수 있습니다. 한국어 패치 제작진은 원 사이트 링크로 공유하도록 안내하고 있으므로, 원본을 직접 준비한 사용자가 로컬에서 변환하는 방식입니다.

### Windows

Python 3.10 이상이 필요합니다. 아래 경로는 예시이니 자신의 파일 위치로 바꾸고, 공백이 있는 경로는 따옴표로 묶습니다.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe build.py --assets "inputs/DDLC-3DS.zip" --korean "inputs/korean-normal-1.2.zip" --mkromfs "C:/devkitPro/tools/bin/mkromfs3ds.exe" --cia-template "inputs/DDLC-3DS.cia" --makerom "tools-local/makerom.exe" --fetch-reference
```

`--fetch-reference`는 고정된 커밋의 영문 비교 텍스트를 내려받고 파일별 SHA-256을 검사합니다. 내려받은 Ren'Py 스크립트를 실행하지는 않습니다. 오프라인 환경에서는 같은 파일을 담은 폴더를 `--reference-dir`로 지정합니다.

CIA가 필요 없으면 `--cia-template`과 `--makerom`을 생략합니다. `--lua`에 Lua 5.1 실행 파일을 지정하면 빌드 과정에서 추가 검사를 실행합니다.

### 결과물

생성 결과는 `dist/`에 있습니다.

- `DDLC-LOVE-KO-<버전>.cia`: CFW 3DS용 설치본
- `DDLC-LOVE-KO-<버전>.3dsx`: Homebrew Launcher/Azahar용 실행본
- `SHA256SUMS.txt`: 생성 파일 검증값

## 검증 범위

- Lua 5.1 문법 검사
- 현대 한글 11,172음절의 생성 글꼴 지원 검사
- 기본 자판 직접 호출, 한글·영문·혼합 이름, 마지막 음절과 저장 콜백 검사
- 취소, 글자 수 제한, 잘못된 문자, 중복 콜백 처리 검사
- UTF-8 글자 표시, 304픽셀 줄바꿈, 대사·시 페이지 처리 검사
- 9,943개 대사 호출의 일반 영어 잔여 검사 (0건)
- CIA의 NCCH 헤더와 3단계 RomFS 해시, 패키지 내용 일치 검사
- 그리기 콜백 안에서 GPU 글꼴 업로드·쿼드 할당이 없는지 확인하는 회귀 검사

이번 빌드는 실제 3DS에서 첫 실행 안내와 게임 진행을 확인했고, Azahar에서도 같은 동작을 확인했습니다. 기본 자판의 기기별 한/영 전환, 전체 분기와 엔딩, 장시간 메모리 사용은 추가 확인이 필요합니다. 확인하지 않은 항목을 완료로 표기하지 않습니다.

## 구조

- `runtime/`: 한글 렌더러와 기본 자판 이름 입력 처리
- `tools/`: 로컬 추출, 번역 대응, 글꼴·이미지 변환, 패키징
- `tests/`: 입력·출력 검증
- `build.py`: 전체 로컬 빌드 절차
- `.github/workflows/tests.yml`: 원본 게임 없이 실행하는 소스·조합 검사

## 출처와 라이선스

원작: Team Salvato / [DDLC](https://ddlc.moe/). Lua 포트: [LukeZGD/DDLC-LOVE](https://github.com/LukeZGD/DDLC-LOVE). 3DS 런타임: [LovePotion 1.0.9](https://github.com/lovebrew/lovepotion/tree/1.0.9). 한국어 번역과 글꼴은 [원 패치 배포처](https://sites.google.com/view/dokidokikor)에 공로가 있습니다.

이 저장소의 코드에는 GPL-3.0을 적용합니다. 게임 자산·번역·글꼴·Nintendo 데이터에 대한 권리를 GPL로 바꾸는 것은 아닙니다. 포함 관계와 빌드 출처는 [THIRD_PARTY.md](THIRD_PARTY.md)를 확인해 주세요.
