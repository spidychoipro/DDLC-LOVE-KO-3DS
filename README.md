# DDLC-LOVE 한국어판 · Nintendo 3DS

Nintendo 3DS용 DDLC-LOVE에 기존 한국어 패치의 번역을 적용하는 **비공식 개인 빌드 도구**입니다. Team Salvato, LukeZGD 및 한국어 패치 제작진의 공식 배포판이 아닙니다.

현재 버전은 **0.2.6-beta**입니다. 한글 입력과 출력에 대한 자동 검사는 통과했지만, 3DS 실기에서 모든 루트와 엔딩을 완주한 버전은 아닙니다. 버전별 수정 내역은 [CHANGELOG.md](CHANGELOG.md)에 있습니다.

## 포함된 기능

- 구형 LovePotion의 바이트 단위 글꼴 출력을 보완하는 UTF-8 한글 렌더러
- 기존 한국어 패치와 Lua 대사를 대응시키는 로컬 변환 절차
- 대사 줄바꿈, 긴 대사와 시의 페이지 넘김
- 원본 시 쓰기 안내 패널의 크기·배치·테두리·반투명 배경을 유지한 채 글자만 한국어로 표시
- 새 게임에서 Nintendo 3DS 기본 소프트웨어 키보드를 직접 호출
- 시스템 자판이 반환한 한글·영문·혼합 UTF-8 이름 및 마지막 음절을 그대로 저장
- 현대 한글 완성형 11,172자에 대한 이름 출력용 글꼴 생성
- 일반 시 및 특수 시 이미지의 한국어화
- `.3dsx`와 `.cia`의 로컬 생성 및 해시 검증

## 원본 파일 준비

이 저장소에는 게임 전체, 번역 데이터 전체, 글꼴, Nintendo DSP 펌웨어, 개인 저장 데이터를 넣지 않습니다. 다음 파일은 각 배포처에서 직접 준비합니다.

1. [DDLC-LOVE v1.1.9](https://github.com/LukeZGD/DDLC-LOVE/releases/tag/v1.1.9)의 `DDLC-3DS.zip`
2. [두근두근 문예부 한국어화 패치](https://sites.google.com/view/dokidokikor)의 **1.2 일반 사용자용 normal ZIP**
3. CIA를 만들 경우 같은 v1.1.9의 `DDLC-3DS.cia`
4. [devkitPro](https://devkitpro.org/)의 `mkromfs3ds`, [Project_CTR makerom 0.19.0](https://github.com/3DSGuy/Project_CTR/releases/tag/makerom-v0.19.0)

원본 DDLC는 [공식 사이트](https://ddlc.moe/)에서 받을 수 있습니다. 한국어 패치 제작진은 원 사이트 링크로 공유하도록 안내하고 있습니다. 이 저장소는 원본을 직접 준비한 사용자가 로컬에서 변환하는 방식입니다.

빌드까지 하지 않고 바로 설치하려면 [Releases](https://github.com/spidychoipro/DDLC-LOVE-KO-3DS/releases)에 첨부된 CIA·3DSX를 쓰면 됩니다. 그 파일에는 게임 자산과 번역이 들어 있으니 다시 배포할 때는 원 배포처 정책을 확인해야 합니다.

## Windows 빌드

Python 3.10 이상을 사용합니다. 아래 경로는 예시이며 자신의 파일 위치로 바꿉니다. 공백이 있는 경로는 따옴표로 묶습니다.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt
.\.venv\Scripts\python.exe build.py --assets "inputs/DDLC-3DS.zip" --korean "inputs/korean-normal-1.2.zip" --mkromfs "C:/devkitPro/tools/bin/mkromfs3ds.exe" --cia-template "inputs/DDLC-3DS.cia" --makerom "tools-local/makerom.exe" --fetch-reference
```

`--fetch-reference`는 고정된 커밋의 영문 비교 텍스트를 내려받고 파일별 SHA-256을 검사합니다. 내려받은 Ren'Py 스크립트를 실행하지 않습니다. 오프라인 환경에서는 같은 파일들을 담은 폴더를 `--reference-dir`로 지정합니다.

CIA가 필요 없으면 `--cia-template`과 `--makerom`을 생략합니다. `--lua`에 Lua 5.1 실행 파일을 지정하면 빌드 과정에서 추가 검사를 실행합니다.

생성 결과는 `dist/`에 있습니다.

- `DDLC-LOVE-KO-0.2.6.cia`: CFW 3DS용 설치본
- `DDLC-LOVE-KO-0.2.6.3dsx`: Homebrew Launcher/Azahar용 실행본
- `SHA256SUMS.txt`: 생성 파일 검증값

## 설치와 조작

### 3DS CIA

1. CIA를 SD 카드에 복사합니다.
2. FBI에서 설치하고 홈 메뉴에서 실행합니다.
3. 홈브루 사운드용 `sdmc:/3ds/dspfirm.cdc`가 준비되어 있는지 확인합니다. 본인의 기기에서 추출한 파일을 사용합니다.

FBI의 **Remote Install → Scan QR code**로 설치하는 방법과 설치 QR은 [Releases](https://github.com/spidychoipro/DDLC-LOVE-KO-3DS/releases) 페이지에 있습니다.

CIA Title ID는 `0004000000DDFB00`, 제품 코드는 `CTR-P-DLKO`입니다. 원본 DDLC-3DS의 Title ID와 구분했습니다. 이 ID가 다른 모든 홈브루와 충돌하지 않는다고 보장하지는 않습니다.

### 3DS 3DSX / Azahar

`.3dsx` 파일에 게임 데이터가 들어 있습니다. 실기는 SD 카드의 `/3ds/` 아래에 놓고 Homebrew Launcher에서 실행합니다. Azahar에서는 `.3dsx`를 파일 열기로 실행하거나 CIA를 설치합니다. Azahar의 가상 SD에도 홈브루 사운드용 DSP 파일이 필요합니다.

Azahar에서 시작 브금이 잠깐 빨라지면 게임별 Audio stretching을 끄면 됩니다. 설정 방법은 [Azahar 사운드 안내](docs/AZAHAR_AUDIO.md)를 참고하세요.

### 이름 입력: 3DS 기본 자판

`새 게임`을 선택하면 **Nintendo 3DS 기본 소프트웨어 키보드**가 바로 열립니다. 게임이 그리는 자판과 별도 한글 조합기는 사용하지 않습니다.

게임은 기본 자판에서 반환한 한글·영문·혼합 이름을 UTF-8로 그대로 저장합니다. 최대 12글자이며 마지막 한글 음절을 바이트 단위로 잘라내지 않습니다. 취소하면 제목 화면으로 돌아갑니다.

**한글 입력 페이지의 제공 여부는 기기에 설치된 시스템 키보드·지역·언어 환경에 달려 있습니다.** 이 게임이 다른 지역의 기본 자판에 한글 페이지를 추가하거나 시스템 자판을 교체하지는 않습니다. 기본 자판에서 한국어를 지원하는 환경에서는 그 자판의 한/영 전환을 사용합니다. Azahar의 입력창 역시 에뮬레이터와 호스트 입력기 동작에 영향을 받습니다.

이름에 따옴표·역슬래시·제어 문자를 넣으면 기존 저장 형식을 보호하기 위해 안내 메시지를 표시합니다.

### 기존 저장 데이터

이전 한국어 테스트본과 같은 `DDLC-3DS-KO` 저장 식별자를 사용합니다. 실제 경로는 `sdmc:/3ds/data/LovePotion/DDLC-3DS-KO/`입니다. 업데이트 전 이 폴더를 별도로 백업하는 것이 좋습니다. 새 게임을 선택하면 이름 입력 후 처음부터 진행합니다.

## 검증 범위

- Lua 5.1 문법 검사
- 현대 한글 11,172음절의 생성 글꼴 지원 검사
- 기본 자판 직접 호출, 한글·영문·혼합 이름, 마지막 음절과 저장 콜백 검사
- 취소, 글자 수 제한, 잘못된 문자, 중복 콜백 처리 검사
- UTF-8 글자 표시, 304픽셀 줄바꿈, 대사·시 페이지 처리 검사
- 시 쓰기 안내 원본 이미지 보존과 한글 패널 표시 검사
- CIA의 NCCH 헤더와 3단계 RomFS 해시, 패키지 내용 일치 검사

실기 설치, 기본 자판의 기기별 한/영 전환, 전체 분기와 엔딩, 장시간 메모리 사용은 추가 확인이 필요합니다. 확인하지 않은 항목을 완료로 표기하지 않습니다.

## 구조

- `runtime/`: 이 프로젝트의 렌더러·기본 자판 이름 입력 처리
- `tools/`: 로컬 추출, 번역 대응, 글꼴·이미지 변환, 패키징
- `tests/`: 입력·출력 검증
- `build.py`: 전체 로컬 빌드 절차
- `.github/workflows/tests.yml`: 원본 게임 없이 실행하는 소스·조합 검사

## 출처와 라이선스

원작: Team Salvato / [DDLC](https://ddlc.moe/). Lua 포트: [LukeZGD/DDLC-LOVE](https://github.com/LukeZGD/DDLC-LOVE). 3DS 런타임: [LovePotion 1.0.9](https://github.com/lovebrew/lovepotion/tree/1.0.9). 한국어 번역과 글꼴은 [원 패치 배포처](https://sites.google.com/view/dokidokikor)에 공로가 있습니다.

이 저장소의 코드에는 GPL-3.0을 적용합니다. 게임 자산·번역·글꼴·Nintendo 데이터에 대한 권리를 GPL로 바꾸는 것은 아닙니다. 포함 관계와 빌드 출처는 [THIRD_PARTY.md](THIRD_PARTY.md)를 확인해 주세요.
