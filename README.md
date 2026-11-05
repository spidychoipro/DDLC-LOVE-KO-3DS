<div align="center">
  <img src="docs/banner.svg" alt="DDLC-LOVE 한국어판 · Nintendo 3DS" width="100%">
  <br><br>
  <a href="https://github.com/spidychoipro/DDLC-LOVE-KO-3DS/releases/latest"><img src="https://img.shields.io/github/v/release/spidychoipro/DDLC-LOVE-KO-3DS?style=flat-square&label=release&color=ff5c8a" alt="release"></a>
  <a href="https://github.com/spidychoipro/DDLC-LOVE-KO-3DS/actions/workflows/tests.yml"><img src="https://img.shields.io/github/actions/workflow/status/spidychoipro/DDLC-LOVE-KO-3DS/tests.yml?style=flat-square&label=checks" alt="checks"></a>
  <img src="https://img.shields.io/badge/platform-Nintendo%203DS-e60012?style=flat-square" alt="platform">
  <img src="https://img.shields.io/github/license/spidychoipro/DDLC-LOVE-KO-3DS?style=flat-square&color=a78bfa" alt="license">
  <a href="https://github.com/spidychoipro/DDLC-LOVE-KO-3DS/releases"><img src="https://img.shields.io/github/downloads/spidychoipro/DDLC-LOVE-KO-3DS/total?style=flat-square&color=2ea043" alt="downloads"></a>
</div>

<br>

> [!WARNING]
> **비공식 개인 빌드입니다.** Team Salvato, LukeZGD, 한국어 패치 제작진과 무관하며 공식 배포판이 아닙니다.
> 이 저장소에는 게임 본체, 번역 데이터, 글꼴, DSP 펌웨어, 세이브 파일이 들어 있지 않습니다. 원본은 각 배포처에서 직접 준비합니다.

Nintendo 3DS용 [DDLC-LOVE](https://github.com/LukeZGD/DDLC-LOVE)에 기존 한국어 패치의 번역을 적용하는 로컬 빌드 도구입니다. 게임을 다시 그리지 않고, 원본 런타임 위에서 한글 출력과 이름 입력만 손봅니다.

현재 **0.2.7-beta**는 실제 3DS에 설치해 첫 실행 안내와 게임 진행이 정상인 것을 확인했습니다. Azahar에서도 같은 빌드가 동작합니다. 전체 루트와 엔딩을 끝까지 완주한 버전은 아닙니다.

## 목차

| | | |
|:--|:--|:--|
| [미리보기](#미리보기) | [주요 기능](#주요-기능) | [지원-환경](#지원-환경) |
| [설치](#설치) | [첫-실행](#첫-실행) | [이름-입력](#이름-입력) |
| [저장-데이터](#저장-데이터) | [직접-빌드](#직접-빌드) | [검증-범위](#검증-범위) |
| [문제-해결](#문제-해결) | [프로젝트-구조](#프로젝트-구조) | [FAQ](#faq) |

## 미리보기

<p align="center">
  <img src="docs/install-qr.png" width="220" alt="DDLC-LOVE-KO CIA 설치 QR">
</p>
<p align="center">
  <sub>FBI → Remote Install → Scan QR code 로 0.2.7-beta CIA(73MB)를 바로 설치한다.</sub>
</p>

## 주요 기능

<table>
<tr>
<td width="50%" valign="top">
<b>한글 렌더러</b><br>
구형 LovePotion의 바이트 단위 글꼴 출력을 보완해서 UTF-8 한글을 제대로 그린다.
</td>
<td width="50%" valign="top">
<b>기본 소프트웨어 키보드</b><br>
새 게임에서 3DS 시스템 자판을 직접 호출한다. 게임이 자판을 다시 그리지 않는다.
</td>
</tr>
<tr>
<td valign="top">
<b>이름 글꼴 11,172자</b><br>
현대 한글 완성형 전체를 이름 출력용으로 생성하고, 마지막 음절을 잘라내지 않는다.
</td>
<td valign="top">
<b>대사 변환</b><br>
기존 한국어 패치와 Lua 대사를 로컬에서 대응시킨다. 9,943개 호출의 영어 잔여 0건.
</td>
</tr>
<tr>
<td valign="top">
<b>시·이미지 한국어화</b><br>
일반 시와 특수 시 이미지의 글자 영역만 한글로 바꾼다.
</td>
<td valign="top">
<b>패키징·검증</b><br>
<code>.3dsx</code>와 <code>.cia</code>를 로컬에서 만들고 NCCH/RomFS 해시를 검사한다.
</td>
</tr>
<tr>
<td valign="top">
<b>입력 가드</b><br>
자판에서 돌아온 직후 남은 입력으로 자동 넘김·스킵이 걸리지 않게 정리한다.
</td>
<td valign="top">
<b>진단 로그</b><br>
첫 실행 단계와 글꼴 페이지를 <code>hardware-startup.log</code>에 남긴다.
</td>
</tr>
</table>

## 지원 환경

| 구분 | 지원 | 비고 |
|:--|:--:|:--|
| 3DS / 3DS XL / 2DS | ✅ | CFW(Luma3DS) 필요 |
| New 3DS / New 2DS XL | ✅ | Luma의 New 3DS CPU 강제 설정은 Off 권장 |
| Azahar | ✅ | CIA 설치 또는 `.3dsx` 직접 실행 |
| Citra | ⚠️ | 검증하지 않음 |
| 홈브루 사운드 | ✅ | `sdmc:/3ds/dspfirm.cdc`를 본인 기기에서 추출 |
| 전체 루트 완주 | ⏳ | 아직 확인하지 않음 |

## 설치

<details open>
<summary><b>CIA — FBI QR 설치 (권장)</b></summary>

<br>

1. 3DS에서 **FBI**를 실행한다.
2. **Remote Install → Scan QR code**를 고른다.
3. 화면의 QR을 3DS 카메라로 읽는다.
4. 설치 확인 화면에서 **Yes**를 누른다.
5. 홈 메뉴에서 실행한다.

QR 직링크: <https://github.com/spidychoipro/DDLC-LOVE-KO-3DS/releases/download/v0.2.7-beta/DDLC-LOVE-KO-0.2.7.cia>

SD 카드로 넣으려면 릴리스에서 `DDLC-LOVE-KO-<버전>.cia`를 받아 **FBI → SD → Install and delete CIA**를 사용한다.

| 항목 | 값 |
|:--|:--|
| Title ID | `0004000000DDFB00` |
| 제품 코드 | `CTR-P-DLKO` |
| CIA title version | 9 |
| 사운드 | `sdmc:/3ds/dspfirm.cdc` 필요 |

</details>

<details>
<summary><b>3DSX — Homebrew Launcher</b></summary>

<br>

1. `DDLC-LOVE-KO-<버전>.3dsx`를 SD 카드의 `/3ds/` 아래에 복사한다.
2. Homebrew Launcher에서 실행한다.
3. DSP 파일이 없으면 사운드가 나오지 않는다.

</details>

<details>
<summary><b>Azahar</b></summary>

<br>

CIA를 설치하거나 `.3dsx`를 파일 열기로 실행한다. 가상 SD에도 `dspfirm.cdc`가 필요하다. 처음 브금이 빨라지면 게임별 **Audio stretching**을 끈다. 자세한 내용은 [Azahar 사운드 안내](docs/AZAHAR_AUDIO.md)를 본다.

</details>

## 첫 실행

첫 실행에서 10016번 안내가 한글로 나오고 <kbd>A</kbd>로 게임이 시작된다. 여기서 멈추던 문제가 0.2.7의 수정 대상이었고, 실제 3DS에서 해결된 것을 확인했다.

멈춤이 다시 생기면 SD의 아래 파일에서 마지막으로 완료한 준비 단계를 확인한다.

```text
sdmc:/3ds/data/LovePotion/DDLC-3DS-KO/hardware-startup.log
```

로그에는 이름이나 저장 내용 대신 시작 단계와 글꼴 페이지 번호만 남는다.

## 이름 입력

`새 게임`을 선택하면 **Nintendo 3DS 기본 소프트웨어 키보드**가 바로 열린다. 게임이 그리는 자판이나 별도 한글 조합기는 쓰지 않는다.

- 한글·영문·혼합 이름을 UTF-8로 그대로 저장한다.
- 최대 12글자이며, 마지막 한글 음절을 바이트 단위로 자르지 않는다.
- 취소하면 타이틀 화면으로 돌아간다.
- 따옴표·역슬래시·제어 문자는 저장 형식 보호를 위해 거부하고 안내를 띄운다.

> [!NOTE]
> 한글 입력 페이지가 있는지는 기기에 설치된 시스템 키보드·지역·언어 환경에 따라 다르다. 이 게임이 다른 지역 자판에 한글 페이지를 추가하거나 시스템 자판을 교체하지는 않는다.

## 저장 데이터

이전 한국어 테스트본과 같은 `DDLC-3DS-KO` 식별자를 쓴다.

```text
sdmc:/3ds/data/LovePotion/DDLC-3DS-KO/
```

업데이트 전에 이 폴더를 백업해 두는 게 좋다. 새 게임을 선택하면 이름 입력 후 처음부터 진행한다.

## 직접 빌드

### 준비물

| 파일 | 출처 |
|:--|:--|
| `DDLC-3DS.zip` | [DDLC-LOVE v1.1.9](https://github.com/LukeZGD/DDLC-LOVE/releases/tag/v1.1.9) |
| `korean-normal-1.2.zip` | [두근두근 문예부 한국어화 패치](https://sites.google.com/view/dokidokikor) 1.2 일반 사용자용 |
| `DDLC-3DS.cia` | 같은 v1.1.9 릴리스 (CIA 빌드용) |
| `mkromfs3ds` | [devkitPro](https://devkitpro.org/) |
| `makerom` | [Project_CTR makerom 0.19.0](https://github.com/3DSGuy/Project_CTR/releases/tag/makerom-v0.19.0) |

원본 DDLC는 [공식 사이트](https://ddlc.moe/)에서 받는다. 한국어 패치 제작진이 원 사이트 링크 공유를 안내하므로, 원본을 직접 준비한 사용자가 로컬에서 변환하는 방식이다.

### Windows

Python 3.10 이상이 필요하다. 경로는 예시이니 자신의 파일 위치로 바꾸고, 공백이 있는 경로는 따옴표로 묶는다.

```powershell
python -m venv .venv
.\.venv\Scripts\python.exe -m pip install -r requirements.txt

.\.venv\Scripts\python.exe build.py `
  --assets "inputs/DDLC-3DS.zip" `
  --korean "inputs/korean-normal-1.2.zip" `
  --mkromfs "C:/devkitPro/tools/bin/mkromfs3ds.exe" `
  --cia-template "inputs/DDLC-3DS.cia" `
  --makerom "tools-local/makerom.exe" `
  --fetch-reference
```

<details>
<summary><b>빌드 옵션</b></summary>

<br>

- `--fetch-reference`: 고정 커밋의 영문 비교 텍스트를 받고 파일별 SHA-256을 검사한다. Ren'Py 스크립트를 실행하지 않는다.
- `--reference-dir`: 오프라인에서 같은 파일을 담은 폴더를 지정한다.
- `--cia-template`, `--makerom`: CIA가 필요 없으면 둘 다 생략한다.
- `--lua`: Lua 5.1 실행 파일을 지정하면 빌드 중 추가 검사를 실행한다.

</details>

### 결과물

| 파일 | 용도 |
|:--|:--|
| `dist/DDLC-LOVE-KO-<버전>.cia` | CFW 3DS / Azahar 설치본 |
| `dist/DDLC-LOVE-KO-<버전>.3dsx` | Homebrew Launcher / Azahar 실행본 |
| `dist/SHA256SUMS.txt` | 생성 파일 검증값 |

## 검증 범위

| 검사 | 상태 |
|:--|:--:|
| Lua 5.1 문법 | ✅ |
| 현대 한글 11,172음절 글꼴 | ✅ |
| 기본 자판 호출·이름 저장 콜백 | ✅ |
| 취소·글자 수·잘못된 문자·중복 콜백 | ✅ |
| UTF-8 표시·304px 줄바꿈·페이지 처리 | ✅ |
| 대사 9,943개 영어 잔여 | ✅ 0건 |
| CIA NCCH/RomFS 3단계 해시 | ✅ |
| 그리기 콜백 내 GPU 업로드 금지 | ✅ |
| 실기 첫 실행·게임 진행 | ✅ 사용자 확인 |
| Azahar 동작 | ✅ |
| 전체 분기·엔딩·장시간 메모리 | ⏳ 미확인 |

> [!IMPORTANT]
> 확인하지 않은 항목을 완료로 표기하지 않는다. 전체 루트 완주 전에는 "완전 검증된 정식판"이라고 부르지 않는다.

## 문제 해결

<details>
<summary><b>첫 실행에서 10016 안내가 멈춤</b></summary>

<br>

0.2.7에서 수정된 증상이다. 새 CIA로 업데이트하고 재실행한다. 기존 세이브는 지우지 않는다. New 3DS/XL에서 Luma의 **New 3DS CPU**를 `Clock+L2` 또는 `L2`로 강제했다면 `Off`로 두고 확인한다. 그래도 멈추면 `hardware-startup.log`의 마지막 단계를 확인한다.

</details>

<details>
<summary><b>브금이 처음에 빨라짐 (Azahar)</b></summary>

<br>

Azahar의 게임별 **Audio stretching**을 끈다. 이 게임(Title ID `0004000000DDFB00`)에만 적용한다. 자세한 내용은 [docs/AZAHAR_AUDIO.md](docs/AZAHAR_AUDIO.md).

</details>

<details>
<summary><b>한글 자판이 안 보임</b></summary>

<br>

이 빌드는 3DS 시스템 자판을 호출한다. 자판에 한글 페이지가 있는지는 기기 지역·언어 설정에 달려 있다. Azahar에서는 호스트 입력기와 에뮬레이터 입력창 동작에 영향을 받는다.

</details>

<details>
<summary><b>설치가 안 됨</b></summary>

<br>

CFW(Luma3DS)가 필요하다. FBI가 최신인지, SD 카드에 여유 공간이 있는지, CIA 다운로드가 끝까지 됐는지 확인한다. 릴리스의 `SHA256SUMS.txt`와 해시를 비교한다.

</details>

<details>
<summary><b>소리가 안 남</b></summary>

<br>

`dspfirm.cdc`가 `sdmc:/3ds/dspfirm.cdc`에 있어야 한다. 본인 기기에서 추출한 파일을 사용한다.

</details>

## 프로젝트 구조

```text
.
├─ runtime/                 한글 렌더러, 기본 자판 이름 입력, 입력 가드
├─ tools/                   추출, 번역 대응, 글꼴·이미지 변환, 패키징
├─ tests/                   Lua 회귀 검사
├─ docs/                    설치 QR, 실기 대응, 사운드 안내
├─ build.py                 전체 로컬 빌드 절차
└─ .github/workflows/       원본 게임 없이 도는 소스·조합 검사
```

## FAQ

<details>
<summary><b>공식 배포판인가요?</b></summary>

<br>

아니다. 비공식 개인 빌드 도구이고, 원작·Lua 포트·한국어 패치 제작진과 무관하다.

</details>

<details>
<summary><b>롬이나 게임 파일을 배포하나요?</b></summary>

<br>

아니다. 이 저장소에는 도구와 런타임 수정만 있다. 게임 자산과 번역은 원 배포처에서 직접 준비한다.

</details>

<details>
<summary><b>번역은 다 됐나요?</b></summary>

<br>

정적 대사 9,943개에서 일반 영어 잔여는 0건이다. 다만 전체 루트와 엔딩을 실기에서 완주한 검증은 아직 없다.

</details>

<details>
<summary><b>세이브가 사라졌어요</b></summary>

<br>

같은 `DDLC-3DS-KO` 식별자를 쓰므로 업데이트로 경로가 바뀌지는 않는다. 업데이트 전에 백업한 폴더가 있으면 되돌린다.

</details>

<details>
<summary><b>다른 3DS 게임에도 쓸 수 있나요?</b></summary>

<br>

아니다. DDLC-LOVE의 런타임과 이 게임의 대사 구조에 맞춘 수정이다.

</details>

## 기여 · 버그 제보

- 버그나 불편은 [Issues](https://github.com/spidychoipro/DDLC-LOVE-KO-3DS/issues)에 남긴다.
- 실기 증상은 기기 종류, CFW/Luma 버전, CIA title version, `hardware-startup.log` 마지막 줄을 같이 적으면 빨리 좁힐 수 있다.
- 코드 변경은 브랜치를 따서 PR로 올린다. `main` 직접 커밋은 피한다.

## 출처와 라이선스

| 대상 | 출처 |
|:--|:--|
| 원작 | Team Salvato / [DDLC](https://ddlc.moe/) |
| Lua 포트 | [LukeZGD/DDLC-LOVE](https://github.com/LukeZGD/DDLC-LOVE) |
| 3DS 런타임 | [LovePotion 1.0.9](https://github.com/lovebrew/lovepotion/tree/1.0.9) |
| 한국어 번역·글꼴 | [원 패치 배포처](https://sites.google.com/view/dokidokikor) |

이 저장소의 코드에는 **GPL-3.0**을 적용한다. 게임 자산·번역·글꼴·Nintendo 데이터에 대한 권리를 GPL로 바꾸는 것은 아니다. 포함 관계와 빌드 출처는 [THIRD_PARTY.md](THIRD_PARTY.md)를 확인한다.

<div align="center">
  <br>
  <sub>DDLC-LOVE 한국어판 · 비공식 개인 빌드 · <a href="https://github.com/spidychoipro/DDLC-LOVE-KO-3DS/releases/latest">최신 릴리스</a> · <a href="CHANGELOG.md">변경 이력</a></sub>
</div>
