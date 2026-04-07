# artifacts/

노트북 실행 결과물이 저장되는 공유 디렉토리. 각 노트북의 출력이 다음 노트북의 입력이 됩니다.

## 구조

```
artifacts/
├── midi/                  # NB01 출력: Basic Pitch 채보 결과
│   ├── satie.mid
│   └── prokofiev.mid
├── analysis/              # NB01 출력: 피아노 전용 표현 분석
│   ├── satie_analysis.json
│   └── prokofiev_analysis.json
├── cues/                  # NB04 출력: 시각화 cue
│   ├── satie_visual_cues.json
│   └── prokofiev_visual_cues.json
├── collab_contract.json   # NB02/NB03 공통 계약 (입출력 스키마)
├── collab_somax/          # NB02 출력: Somax 협업 세션
│   ├── session_*.mid
│   └── session_report.json
├── collab_rave/           # NB03 출력: RAVE 스타일 렌더 + 메타
│   ├── *.wav
│   ├── style_metadata.json
│   └── stage_extension.json
└── performance_timeline.json  # NB05 출력: 공연 타임라인
```

## 데이터 흐름

```
assets/*.wav
  └→ NB01 (Listen) ─→ midi/, analysis/
                       ├→ NB02 (Somax) ─→ collab_somax/
                       ├→ NB03 (RAVE)  ─→ collab_rave/
                       ├→ NB04 (Visualize) ─→ cues/
                       └→ NB05 (Stage) ─→ performance_timeline.json
```

모든 산출물은 `.gitignore` 되어 있으며, `assets/*.wav`로부터 노트북 실행만으로 재현 가능합니다.
