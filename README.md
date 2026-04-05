# pianokit

음대 피아노 전공생을 위한 MIR·AI 워크숍.

**확장**과 **협업**이라는 두 축을 통해 피아노 연주를 탐험합니다.

## 워크숍 구조

```
┌─────────────────────────────────────────────────┐
│ 기반                                            │
│  NB01  AI가 내 연주를 듣다 (listen)             │
│        → MIDI + 표현 분석                       │
└────────────────┬────────────────────────────────┘
                 │
        ┌────────┴────────┐
        ▼                 ▼
┌─────────────────┐ ┌─────────────────┐
│ 확장형          │ │ 확장형          │
│  NB02  시각 차원│ │  NB03  음악 차원│
│  (visualize)    │ │  (expand)       │
│  → cue·p5.js    │ │  → 변주 MIDI    │
└────────┬────────┘ └────────┬────────┘
         │                   │
         └─────────┬─────────┘
                   ▼
         ┌─────────────────┐
         │ 협업형          │
         │  NB04  AI와 대화│
         │  (collaborate)  │
         │  → 해석·매핑 제안│
         └────────┬────────┘
                  ▼
         ┌─────────────────┐
         │ 통합            │
         │  NB05  무대     │
         │  (stage)        │
         │  → 공연 타임라인│
         └─────────────────┘
```

## 노트북 안내

| 노트북 | 축 | 역할 |
|---|---|---|
| [01_listen.ipynb](01_listen.ipynb) | **기반** | Basic Pitch 채보 + 피아노 전용 분석 (velocity, IOI CV, register) |
| [02_visualize.ipynb](02_visualize.ipynb) | **확장형 · 시각** | cue 9개 추출, 매핑 딕셔너리 직접 편집, p5.js WEBGL |
| [03_expand.ipynb](03_expand.ipynb) | **확장형 · 음악** | 규칙 기반 MIDI 변환 (반전·역행·이조·재화성화) |
| [04_collaborate.ipynb](04_collaborate.ipynb) | **협업형** | AI 해석 피드백 + 시각 매핑 제안 (학생이 비교·판단) |
| [05_stage.ipynb](05_stage.ipynb) | **통합** | 타임라인 편집, 미니 공연 구성, 웹 앱 연동 |

## 두 축의 의미

### 확장 (Expansion)
연주가 단일한 소리 이벤트에 머무르지 않고 **새로운 차원으로 번지는 것**:
- **시각 차원**(NB02): 같은 연주가 매핑 선택에 따라 질적으로 다른 시각 세계가 됨
- **음악 차원**(NB03): 원 연주가 반전·변주·재화성화를 통해 새 작품이 됨

### 협업 (Collaboration)  
AI가 **응답**하고 연주자가 그 응답을 **수용·거부·비교**:
- **해석의 대화**(NB04 Mode B): AI가 수치를 짚음 → "맞게 읽었나?"
- **시각의 대화**(NB04 Mode C): AI가 매핑 제안 → NB02의 내 매핑과 비교

AI가 음악을 생성하지 않고 **제안·해석**하는 형태이므로 음악적 품질 문제가 없습니다.

## 두 곡 대비

| | Satie — Gymnopédie No.1 | Prokofiev — Toccata Op.11 |
|---|---|---|
| 성격 | 서정형 | 동력형 |
| 텍스처 | 얇음·지속 | 두꺼움·타격 |
| 템포 | ~72 BPM | ~160+ BPM |
| 음역 | C3-C5 | 전 건반 |

라이선스는 [assets/ATTRIBUTIONS.md](assets/ATTRIBUTIONS.md) 참고.

## 설치 및 실행

```bash
./setup.sh           # GPU 자동 감지
./setup.sh --cpu     # CPU 전용
conda activate pianokit
jupyter lab
```

모든 처리는 **로컬 규칙 기반**입니다. 외부 API나 비용이 없습니다.

## 데이터 흐름

```
assets/*.wav
  └→ NB01 ─→ artifacts/midi/, artifacts/analysis/
             ├→ NB02 ─→ artifacts/cues/
             ├→ NB03 ─→ artifacts/responses/*.mid
             └→ NB04 ─→ artifacts/responses/*_interpretive.md, mapping_suggestions.json
                        └→ NB05 ─→ artifacts/performance_timeline.json
                                    └→ pianokit_web/public/stage_data/ (→ /stage 라우트)
```

각 노트북은 이전 단계 산출물에 의존합니다. 번호 순서대로 실행하세요.

## 웹 앱 공연 모드

```bash
cd pianokit_web
npm install
npm run dev
```

`http://localhost:5173/stage` 에서 풀스크린 공연:
- Satie/Prokofiev 전환
- 프리셋 매핑 3종 + AI 제안 매핑
- 실시간 p5.js WEBGL 장면
