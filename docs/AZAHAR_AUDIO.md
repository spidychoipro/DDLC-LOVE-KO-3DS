# Azahar에서 자판 복귀 뒤 처음만 빨라지는 브금

Azahar 2126.2에서 기본 자판을 닫은 직후 브금이 빨라졌다가 정상 속도로 돌아오는 현상을 확인했습니다. 게임의 음원 샘플레이트는 정상이며, 시작 직후 출력 녹음과 원본 음악을 비교해 초기 배속을 재현했습니다.

이 PC에서는 문예부 CIA의 게임별 Audio stretching(오디오 시간 보정)을 꺼서 적용했고, 사용자가 처음부터 정상 속도로 들린다고 확인했습니다. 전역 오디오 시간 보정은 원래 켜짐 상태로 복원했습니다.

## 다른 PC에서 적용

Azahar 게임 목록에서 문예부를 오른쪽 클릭해 게임별 설정/속성을 열고 Audio에서 Audio stretching을 끕니다. 전역 설정 상속 대신 이 게임에만 끄기로 지정합니다. 문예부 CIA의 Title ID는 `0004000000DDFB00`입니다.

해당 게임별 설정 파일은 `%APPDATA%/Azahar/config/custom/0004000000DDFB00.ini`입니다. 기존 설정의 다른 항목을 유지하면서 Audio 절의 다음 값이 적용되는지 확인할 수 있습니다.

```ini
[Audio]
enable_audio_stretching\use_global=false
enable_audio_stretching\default=false
enable_audio_stretching=false
```

3DSX 실행본은 실행 항목의 게임별 설정을 별도로 확인해야 할 수 있습니다. 이 PC에서 최종 확인한 설치본은 위 Title ID의 0.2.8 CIA입니다.

## 원인과 검증 범위

Azahar의 [TimeStretcher 구현](https://github.com/azahar-emu/azahar/blob/master/src/audio_core/time_stretch.cpp)은 밀린 샘플 양에 따라 SoundTouch의 재생 템포를 조절합니다. [오디오 설정 구현](https://github.com/azahar-emu/azahar/blob/master/src/citra_qt/configuration/configure_audio.cpp)은 게임별 시간 보정 설정을 지원합니다.

이번 자판 복귀 뒤 일시적인 배속은 이 보정을 끈 비교 실행에서 사용자가 정상으로 확인했습니다. 변경 후 정상 여부의 최종 근거는 사용자의 청감 확인이며, 3DS 실기 전체 플레이 검증은 별도입니다. 이 대응은 Azahar 게임별 설정에 적용합니다.
