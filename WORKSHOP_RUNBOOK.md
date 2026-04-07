# PianoKit Somax-RAVE 워크숍 런북 (120분)

이 문서는 현재 파이프라인(`06_somax_collab.ipynb` -> `07_rave_collab.ipynb` -> `05_stage.ipynb`)을
수업에서 안정적으로 운영하기 위한 실행용 가이드입니다.

## 1) 수업 목표

- Somax 기반 협업 세션 생성 결과를 이해하고 재생성한다.
- RAVE 스타일 변환을 최소 1개 프로파일에서 성공한다.
- Stage 타임라인에 협업 결과를 병합해 시연한다.
- 결과물(JSON + 오디오)의 재현성과 선택 근거를 설명한다.

## 2) 120분 운영안

- `0-10분` 오리엔테이션: 전체 흐름, 산출물 계약, 실패 대응 원칙 공유
- `10-20분` 사전 점검: 환경/모델/경로 확인 (TA 체크리스트 기준)
- `20-50분` NB06 실행: Somax 세션 생성 및 `session_report.json` 검증
- `50-80분` NB07 실행: RAVE 1프로파일 우선 변환 (`warm_legato` 권장)
- `80-105분` NB05 실행: RAVE source 자동 병합 + `/stage` 시연
- `105-120분` 발표/피드백: 선택 근거, 재현성 로그, 개선 포인트

## 2-b) 웹 라우트 운영

- 워크숍 홈: `/`
- 오리엔테이션: `/workshop/intro`
- Somax 단계: `/workshop/nb06`
- RAVE 단계: `/workshop/nb07`
- Stage 통합 단계: `/workshop/nb05`
- 시연 뷰어: `/stage`

강의자는 단계 URL을 직접 공유해 실습 위치를 고정합니다.

## 3) 트랙 분기 (완주/안전)

- **완주 트랙**
  - NB06 -> NB07(최소 1개, 가능하면 3개 프로파일) -> NB05
- **안전 트랙**
  - NB06 또는 사전 제공 `collab_rave` 산출물 사용 -> NB05 중심 시연
  - 목표는 "통합 시연 완주"로 유지하고, 고급 변환은 과제로 이관

## 4) 필수 체크포인트 (수업 중 즉시 확인)

- **CP1 (NB06 완료 직후)**
  - `artifacts/collab_somax/session_report.json` 존재
  - `output_midi`, `output_wav` 파일이 실제로 존재
- **CP2 (NB07 시작 전)**
  - `RAVE_MODEL_PATHS` 비어 있지 않음
  - 모델 경로가 실제 파일로 확인됨
- **CP3 (NB07 완료 직후)**
  - `artifacts/collab_rave/*.wav` 최소 1개 생성
  - `style_metadata.json`, `stage_extension.json` 생성
- **CP4 (NB05 내보내기 직후)**
  - `artifacts/performance_timeline.json` 생성
  - `sources`에 `rave_<profile>` 키 반영 여부 확인
- **CP5 (웹 시연 직전)**
  - `pianokit_web/public/stage_data/`에 JSON/WAV 동기화 완료
  - `/stage`에서 source 전환 및 재생 확인

## 5) 평가 루브릭 (3단계)

### A. 프로세스

- **1단계**: 노트북 일부만 실행, 연결 산출물 누락
- **2단계**: NB06->NB07->NB05를 순서대로 실행하고 산출물 제출
- **3단계**: 실패-복구 과정과 파라미터 변경 근거까지 기록

### B. 결과물 품질

- **1단계**: 오디오/Stage 시연 중 하나 이상 실패
- **2단계**: Stage에서 source 전환/재생이 정상 동작
- **3단계**: 스타일 차이를 청취 근거로 설명 가능

### C. 재현성

- **1단계**: 경로/모델/설정 기록 불충분
- **2단계**: 핵심 경로와 실행 조건이 기록되어 동일 환경 재현 가능
- **3단계**: 타인이 짧은 안내만으로 재현 가능하도록 정리

### D. 협업/해석

- **1단계**: 선택 이유가 모호함
- **2단계**: 매핑/프로파일 선택 이유를 설명
- **3단계**: 트레이드오프(예: 밀도 vs 명료도)를 근거로 비교 설명

## 6) TA 운영 체크리스트

### 수업 전 (D-1 / D-day 시작 전)

- [ ] `06_somax_collab.ipynb`가 최소 1회 실행 완료된 샘플 아티팩트 준비
- [ ] `07_rave_collab.ipynb`용 모델 파일 경로 확인
- [ ] `fluidsynth` 및 SoundFont 경로 확인
- [ ] `pianokit_web` 빌드 가능 여부 확인
- [ ] 안전 트랙용 `artifacts/collab_rave` 백업본 준비

### 수업 중 (문제 발생 시 우선순위)

- [ ] 모델 경로 문제: 경로 교정 -> 1프로파일만 실행
- [ ] 변환 시간 초과: 짧은 입력 또는 단일 프로파일로 축소
- [ ] NB06 렌더 실패: 사전 제공 Somax WAV로 NB07 진행
- [ ] NB07 실패 지속: 안전 트랙 전환 후 NB05 시연 완주
- [ ] `/stage_data` 결손 경고가 뜨면 NB05 export/동기화를 다시 실행

### 수업 후

- [ ] 팀별 산출물(JSON/WAV) 수집
- [ ] 재현성 로그(실행환경/버전/경로) 수집
- [ ] 다음 차시 개선 포인트 3개 이상 정리

## 7) 권장 제출물

- `session_report.json`
- `style_metadata.json`
- `stage_extension.json`
- `performance_timeline.json`
- 1분 이내 데모 영상(또는 발표 녹화) + 선택 근거 5줄

## 8) 자주 막히는 지점과 즉시 대응

- **`Missing session_report.json`**
  - NB06 미실행 상태. NB06부터 실행하거나 샘플 아티팩트 사용
- **`SoundFont not found`**
  - SoundFont 경로 수정 또는 사전 환경 이미지 사용
- **`RAVE model path not found`**
  - 모델 경로 재지정 후 NB07 재시도
- **NB07 추론 시간 과다**
  - 프로파일 1개로 제한, 나머지는 과제로 이관

---

운영 원칙: **수업 목표는 "완전한 설치 성공"이 아니라 "파이프라인 이해 + 시연 완주"**입니다.
