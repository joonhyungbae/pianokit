# pianokit — 제작 계획서 (v2)

> 이 문서는 pianokit_web 앱바 서브메뉴 구조에 1:1로 대응하는 Colab 노트북 + p5.js 코드 제작 계획입니다.

---

## 전체 원칙

- 대상: 코딩 경험 없는 서울대 음대생 (90분 특강)
- 모든 노트북은 Google Colab 무료 티어 (T4 GPU)에서 실행 가능
- 오디오 결과물은 `IPython.display.Audio`로 노트북 내 재생
- 이미지 결과물은 `matplotlib` 또는 `IPython.display.Image`로 표시
- 파일 다운로드는 `google.colab.files.download()`
- 예시 파일은 GitHub 레포 `assets/`에서 자동 다운로드
- 에러 최소화: 버전 핀, 워닝 suppress, 설치 출력 `%%capture`
- **노트북 간 참조 시 번호가 아닌 서브메뉴 이름으로 안내** (예: "노트북 4" ✗ → "'내 멜로디 + AI' 노트북" ✓)

### 노트북 셀 작성 형식

모든 노트북은 **한국어 마크다운 셀**과 **코드 셀**이 교차하는 튜토리얼 형식으로 작성한다.

```
┌─────────────────────────────────────┐
│ [마크다운 셀]                        │
│ • 이 단계에서 무엇을 하는지 설명     │
│ • 왜 이 과정이 필요한지 맥락 제공     │
│ • 학생이 할 행동이 있으면 ▶ 로 안내  │
├─────────────────────────────────────┤
│ [코드 셀]                            │
│ • 학생이 ▶ 실행 버튼만 누르면 됨     │
│ • 수정이 필요한 변수는 셀 상단에 배치 │
│ • 한글 주석으로 핵심 코드 설명        │
├─────────────────────────────────────┤
│ [마크다운 셀]                        │
│ • 결과 해석 또는 다음 단계 안내       │
└─────────────────────────────────────┘
```

**마크다운 셀 원칙:**
- 모든 코드 셀 앞에 반드시 마크다운 셀이 있어야 함
- 전문 용어는 처음 등장할 때 괄호로 쉬운 설명 추가 (예: "MIDI (악보 데이터)")
- 학생 액션이 필요한 셀은 "▶"로 시작
- 선택적 셀은 "(선택)" 표시
- 💡 팁, ⚠️ 주의, ⏰ 소요 시간 등 이모지로 시각적 구분

**코드 셀 원칙:**
- 학생이 수정할 값은 셀 최상단에 `# ← 여기를 수정하세요` 주석과 함께 배치
- 나머지 코드는 수정 없이 실행만 하면 되도록
- 핵심 동작에만 간결한 한글 주석 (모든 줄에 주석 달지 않음)
- 출력/시각화는 코드 셀 안에서 바로 이루어지도록

---

## 웹 앱 서브메뉴 ↔ 제작물 매핑

| 메인 탭 | 서브메뉴 | 제작물 | 유형 |
|---------|---------|-------|------|
| 시작 | 준비하기 | — | 웹 안내 전용 (※ 각 STEP 노트북 링크 안내) |
| 시작 | 강사 소개 | — | 웹 안내 전용 |
| 시작 | 로드맵 | — | 웹 안내 전용 |
| **STEP 1** | **자동 채보** | **`01_transcription.ipynb`** | Colab 노트북 |
| **STEP 1** | **소스 분리** | **`02_source_separation.ipynb`** | Colab 노트북 |
| **STEP 2** | **텍스트 → 음악** | **`03_text_to_music.ipynb`** | Colab 노트북 |
| **STEP 2** | **내 멜로디 + AI** | **`04_melody_conditioning.ipynb`** | Colab 노트북 |
| STEP 2 | 유료 도구 비교 | — | 웹 안내 전용 (강사 데모) |
| STEP 3 | 세 가지 접근 비교 | — | 웹 안내 전용 |
| STEP 3 | 실시간 비주얼 만들기 | — | 웹 안내 전용 (p5.js 코드는 웹 앱 인라인으로 제공) |
| **STEP 3** | **AI 오디오리액티브** | **`05_audio_reactive.ipynb`** | Colab 노트북 |
| **STEP 3** | **AI 영상 생성** | **`06_video_generation.ipynb`** | Colab 노트북 |
| 마무리 | 도구 총정리 | — | 웹 안내 전용 |
| **마무리** | **더 해보기** | **`07_image_generation.ipynb`** | Colab 노트북 (심화) |
| 마무리 | 리소스 | — | 웹 안내 전용 |

---

## 레포 구조

```
pianokit/
├── README.md
├── notebooks/
│   ├── 01_transcription.ipynb          ← STEP 1 > 자동 채보
│   ├── 02_source_separation.ipynb      ← STEP 1 > 소스 분리
│   ├── 03_text_to_music.ipynb          ← STEP 2 > 텍스트 → 음악
│   ├── 04_melody_conditioning.ipynb    ← STEP 2 > 내 멜로디 + AI
│   ├── 05_audio_reactive.ipynb         ← STEP 3 > AI 오디오리액티브
│   ├── 06_video_generation.ipynb       ← STEP 3 > AI 영상 생성
│   └── 07_image_generation.ipynb       ← 마무리 > 더 해보기 (심화)
├── assets/
│   ├── piano_chopin.wav
│   ├── piano_jazz.wav
│   ├── piano_simple.wav
│   ├── concerto_example.wav
│   └── melody_example.mid
└── pianokit_web/                        ← 기존 웹 앱 (p5.js 코드는 여기 인라인으로 포함)
```

---

## 제작 순서

1. **노트북 1: 자동 채보** — 수업 핵심 시작점
2. **노트북 2: 소스 분리** — 노트북 1과 구조 유사
3. **노트북 3: 텍스트 → 음악** — MusicGen 기본
4. **노트북 4: 멜로디 컨디셔닝** — 노트북 1의 결과물 활용
5. **노트북 7: 이미지 생성** — diffusers 패턴이 단순
6. **노트북 5: 오디오리액티브** — 가장 복잡
7. **노트북 6: 영상 생성** — T4 호환 검증 필요

---

## 노트북 1: 자동 채보 (`01_transcription.ipynb`)

> 웹 매핑: STEP 1 > 자동 채보 (Step1Transcription)
> 웹 설명: "이 곡 치고 싶은데 악보가 없다"

### 도구
- **Basic Pitch** (Spotify, 오픈소스)

### 설치할 패키지
- basic-pitch
- librosa
- soundfile
- matplotlib
- midi2audio + fluidsynth (MIDI → 오디오 재생용)

### 셀 구조

#### 0. 설치

> [마크다운]
> # 🎹 자동 채보 — 내 연주를 MIDI로
>
> 피아노 연주 오디오 파일을 넣으면, AI가 음표를 인식하여 **MIDI (악보 데이터)**로 변환합니다.
> 이 MIDI를 나중에 AI 작곡의 입력으로 사용합니다.
>
> **도구**: [Basic Pitch](https://basicpitch.spotify.com/) — Spotify가 만든 오픈소스 채보 AI
>
> ▶ 맨 먼저 아래 셀을 실행해주세요. 설치에 2~3분 정도 걸립니다.

> [코드] — 설치
> - %%capture로 출력 숨김
> - apt-get install fluidsynth
> - pip install basic-pitch librosa soundfile midi2audio matplotlib

#### 1. 오디오 업로드

> [마크다운]
> ## 1. 내 연주 파일 올리기
>
> ▶ 본인 피아노 연주 파일을 업로드하세요. (mp3 또는 wav)
>
> 스마트폰으로 녹음한 파일도 괜찮습니다. 30초~1분 정도면 충분합니다.
> 녹음 파일이 없으면 이 셀은 건너뛰고, 다음 셀에서 예시 파일을 사용하세요.

> [코드] — 업로드
> - google.colab.files.upload()
> - 업로드된 파일 경로를 변수 `input_audio`에 저장
> - "✅ 파일이 업로드되었습니다: {파일명}" 출력

#### 2. 예시 파일 (선택)

> [마크다운]
> ## 2. (선택) 예시 파일 사용
>
> ▶ 녹음 파일이 없으면 이 셀을 실행하세요. 예시 피아노 연주를 다운로드합니다.

> [코드] — 예시 다운로드 + 재생
> - wget으로 assets/에서 예시 3개 다운로드
>   - piano_chopin.wav (쇼팽 녹턴 발췌, 30초)
>   - piano_jazz.wav (재즈 피아노, 30초)
>   - piano_simple.wav (스케일/아르페지오, 15초)
> - `input_audio = "piano_chopin.wav"  # ← 다른 파일로 바꿔보세요`
> - 원본 오디오 재생 위젯 (IPython.display.Audio)

#### 3. AI 채보 실행

> [마크다운]
> ## 3. AI로 음표 인식하기
>
> Basic Pitch는 오디오의 파형을 분석해서 어떤 음이 언제, 얼마나 세게 연주되었는지를
> 자동으로 알아냅니다. 사람이 귀로 듣고 악보를 쓰는 것과 같은 일을 AI가 하는 것입니다.
>
> ▶ 아래 셀을 실행하세요.

> [코드] — Basic Pitch 실행
> - basic_pitch.inference.predict(input_audio)
> - 결과 MIDI 파일 저장 → output.mid
> - "✅ 변환 완료! {인식된 음표 수}개의 음표를 찾았습니다." 출력

#### 4. 결과 확인

> [마크다운]
> ## 4. 결과 확인 — 피아노롤
>
> 아래는 AI가 인식한 음표를 시각화한 **피아노롤**입니다.
> - 가로축: 시간 (초)
> - 세로축: 음높이 (높을수록 고음)
> - 색상: 세기 (진할수록 강하게 연주)
>
> 아래에서 변환된 MIDI를 다시 소리로 들어볼 수도 있습니다.
> 원본 연주와 비교해보세요 — 어떤 차이가 있나요?

> [코드] — 피아노롤 시각화 + MIDI 재생
> - matplotlib 피아노롤 (x: 시간, y: 피치, color: 벨로시티)
> - y축 범위를 실제 사용 음역대에 맞춤
> - MIDI → 오디오 변환 (fluidsynth) → 재생 위젯
> - 원본 오디오 재생 위젯도 나란히 배치 (비교 청취)

#### 5. MIDI 다운로드

> [마크다운]
> ## 5. MIDI 파일 다운로드
>
> ▶ 아래 셀을 실행하면 MIDI 파일이 다운로드됩니다.
>
> 💡 이 MIDI를 **'내 멜로디 + AI' 노트북**에서 사용합니다. 꼭 저장해두세요!

> [코드] — 다운로드
> - google.colab.files.download("output.mid")

---

## 노트북 2: 소스 분리 (`02_source_separation.ipynb`)

> 웹 매핑: STEP 1 > 소스 분리 (Step1SourceSeparation)
> 웹 설명: "합주 연습인데 반주 트랙이 필요하다"

### 도구
- **Demucs** (Meta, 오픈소스)

### 설치할 패키지
- demucs
- librosa (시각화용)
- soundfile
- matplotlib

### 셀 구조

#### 0. 설치

> [마크다운]
> # 🎵 소스 분리 — 음원에서 악기별 트랙 분리
>
> 여러 악기가 섞인 음원에서 **피아노만 추출**하거나, **반주만 남길** 수 있습니다.
> 합주 연습용 반주 트랙을 만들거나, 좋아하는 곡의 피아노 파트만 따로 들어볼 수 있습니다.
>
> **도구**: [Demucs](https://github.com/facebookresearch/demucs) — Meta가 만든 오픈소스 소스 분리 AI
>
> ⏰ 시간이 부족하면 이 노트북은 수업 후에 해보세요. Colab에 다 준비되어 있습니다.
>
> ▶ 먼저 아래 셀을 실행해주세요. 설치에 2~3분 정도 걸립니다.

> [코드] — 설치
> - %%capture로 출력 숨김
> - pip install demucs librosa soundfile matplotlib

#### 1. 오디오 업로드

> [마크다운]
> ## 1. 음원 올리기
>
> ▶ 여러 악기가 섞인 음원을 업로드하세요.
>
> 피아노 협주곡, 밴드 음악, 보컬이 있는 곡 등 악기가 여러 개 섞인 음원이 좋습니다.
> 음원이 없으면 이 셀은 건너뛰고, 다음 셀에서 예시 파일을 사용하세요.

> [코드] — 업로드
> - google.colab.files.upload()
> - 업로드된 파일 경로 저장

#### 2. 예시 파일 (선택)

> [마크다운]
> ## 2. (선택) 예시 파일 사용
>
> ▶ 음원이 없으면 이 셀을 실행하세요. 피아노 협주곡 예시를 다운로드합니다.

> [코드] — 예시 다운로드 + 재생
> - wget으로 assets/concerto_example.wav 다운로드
> - 원본 오디오 재생 위젯

#### 3. 소스 분리 실행

> [마크다운]
> ## 3. AI로 악기별 분리하기
>
> Demucs는 음원의 파형 패턴을 분석해서, 각 악기가 어떤 소리를 내고 있는지 구분합니다.
> 하나의 음원에서 **보컬, 드럼, 베이스, 기타/피아노** 네 가지 트랙을 분리합니다.
>
> ⏰ 1~2분 정도 걸립니다. ▶ 아래 셀을 실행하세요.

> [코드] — Demucs 실행
> - demucs.separate.main() 또는 CLI 호출
> - htdemucs 모델 사용 (4-stem: drums, bass, vocals, other)
> - tqdm 진행률 표시
> - "✅ 분리 완료!" 출력

#### 4. 결과 확인

> [마크다운]
> ## 4. 분리된 트랙 들어보기
>
> 아래에서 각 트랙을 따로 들어볼 수 있습니다.
> 원본과 번갈아 들으면서 얼마나 깔끔하게 분리되었는지 확인해보세요.

> [코드] — 트랙별 재생 + 시각화
> - 각 트랙별 재생 위젯:
>   - "🎹 기타/피아노 (other)"
>   - "🥁 드럼 (drums)"
>   - "🎸 베이스 (bass)"
>   - "🎤 보컬 (vocals)"
> - 각 트랙의 파형 시각화 (matplotlib, 4행 subplot)

#### 5. 트랙 다운로드

> [마크다운]
> ## 5. 트랙 다운로드
>
> ▶ 원하는 트랙을 다운로드하세요.
> 분리한 트랙은 '텍스트 → 음악'이나 'AI 오디오리액티브' 노트북의 입력으로도 활용할 수 있습니다.

> [코드] — 다운로드
> - 전체 zip 다운로드 + 개별 트랙 다운로드 옵션

---

## 노트북 3: 텍스트 → 음악 (`03_text_to_music.ipynb`)

> 웹 매핑: STEP 2 > 텍스트 → 음악 (Step2TextToMusic)
> 웹 설명: "배경음악이 필요한데 시간이 없다"

### 도구
- **MusicGen** (Meta, 오픈소스)

### 설치할 패키지
- audiocraft
- (torch는 Colab 기본 제공 — 호환 버전 확인)

### 셀 구조

#### 0. 설치

> [마크다운]
> # 🎼 텍스트 → 음악 — 글로 음악을 만듭니다
>
> 원하는 분위기를 영어 텍스트로 설명하면, AI가 그에 맞는 음악을 만들어줍니다.
> "슬픈 피아노 녹턴"이라고 쓰면 정말 그런 느낌의 곡이 생성됩니다.
>
> **도구**: [MusicGen](https://github.com/facebookresearch/audiocraft) — Meta가 만든 오픈소스 음악 생성 AI
>
> ▶ 먼저 아래 셀을 실행해주세요. 설치에 2~3분 정도 걸립니다.

> [코드] — 설치
> - %%capture로 출력 숨김
> - pip install audiocraft
> - 주의: Colab 기본 torch 버전과 audiocraft 호환성 체크

#### 1. 모델 로드

> [마크다운]
> ## 1. AI 모델 불러오기
>
> MusicGen은 텍스트 설명을 이해하고, 그에 맞는 오디오 파형을 처음부터 만들어냅니다.
> 약 3억 개의 파라미터를 가진 모델을 사용합니다.
>
> ⏰ 모델 로딩에 1~2분 걸립니다. ▶ 아래 셀을 실행하세요.

> [코드] — 모델 로드
> - from audiocraft.models import MusicGen
> - model = MusicGen.get_pretrained('facebook/musicgen-small')
> - model.set_generation_params(duration=8)  # 8초 생성
> - "✅ 모델 로딩 완료!" 출력

#### 2. 텍스트로 음악 생성

> [마크다운]
> ## 2. 프롬프트 입력 → 음악 생성
>
> ▶ 아래 `prompt` 변수에 원하는 음악의 분위기를 **영어로** 적고 실행하세요.
> 아래 예시 중 하나를 그대로 복사해도 좋고, 직접 만들어도 됩니다.
>
> **프롬프트 예시:**
> | 프롬프트 | 설명 |
> |---------|------|
> | `expressive solo piano, Chopin-like nocturne, melancholy` | 서정적인 쇼팽 스타일 |
> | `bright jazz piano trio with upright bass and brushed drums` | 밝은 재즈 트리오 |
> | `ambient piano with deep reverb, minimal, meditative` | 명상적 앰비언트 |
> | `dramatic orchestral piece with solo piano, cinematic` | 영화음악 느낌 |
> | `cheerful ragtime piano, Scott Joplin style` | 경쾌한 래그타임 |

> [코드] — 프롬프트 입력 + 생성 + 재생
> - `prompt = "expressive solo piano, Chopin-like nocturne, melancholy"  # ← 여기를 수정하세요`
> - wav = model.generate([prompt])
> - 결과 오디오 재생 위젯
> - 파일 저장: generated_music.wav

#### 3. 프롬프트 바꿔보기

> [마크다운]
> ## 3. 다른 프롬프트로 다시 생성해보기
>
> ▶ 프롬프트를 바꿔서 다시 실행해보세요. 같은 모델인데 완전히 다른 음악이 나옵니다.
>
> 💡 2~3가지 프롬프트를 시도해보세요. 단어 하나 바꿔도 결과가 달라집니다.

> [코드] — 다른 프롬프트로 생성
> - `prompt = "bright jazz piano trio with upright bass and brushed drums"  # ← 여기를 수정하세요`
> - 동일한 생성 + 재생 코드

#### 4. 결과 다운로드

> [마크다운]
> ## 4. 결과 다운로드
>
> ▶ 마음에 드는 결과물을 다운로드하세요.
> 생성한 음악을 'AI 오디오리액티브' 노트북의 입력으로 사용할 수도 있습니다.

> [코드] — 다운로드
> - google.colab.files.download("generated_music.wav")

---

## 노트북 4: 멜로디 컨디셔닝 (`04_melody_conditioning.ipynb`)

> 웹 매핑: STEP 2 > 내 멜로디 + AI (Step2MelodyAI)
> 웹 설명: "4마디 아이디어를 AI와 함께 확장하기"

### 도구
- **MusicGen melody** (Meta, 오픈소스)

### 설치할 패키지
- audiocraft
- midi2audio + fluidsynth (MIDI → 오디오 변환용)

### 셀 구조

#### 0. 설치

> [마크다운]
> # 🎹 내 멜로디 + AI — 내 멜로디를 기반으로 새로운 음악을
>
> '자동 채보' 노트북에서 추출한 MIDI 멜로디를 AI에게 들려주면,
> 여러분의 **멜로디를 기반으로** 완전히 새로운 스타일의 음악을 만들어줍니다.
>
> 같은 4마디 멜로디가 재즈가 되기도 하고, 오케스트라가 되기도 합니다.
>
> **도구**: [MusicGen melody](https://github.com/facebookresearch/audiocraft) — 멜로디 컨디셔닝 기능
>
> ▶ 먼저 아래 셀을 실행해주세요. 설치에 2~3분 정도 걸립니다.

> [코드] — 설치
> - %%capture로 출력 숨김
> - apt-get install fluidsynth
> - pip install audiocraft midi2audio

#### 1. MIDI 업로드

> [마크다운]
> ## 1. MIDI 파일 올리기
>
> ▶ '자동 채보' 노트북에서 만든 MIDI 파일을 업로드하세요.
>
> MIDI 파일이 없으면 이 셀은 건너뛰고, 다음 셀에서 예시 파일을 사용하세요.

> [코드] — 업로드
> - google.colab.files.upload()
> - 업로드된 파일 경로 저장

#### 2. 예시 MIDI (선택)

> [마크다운]
> ## 2. (선택) 예시 MIDI 사용
>
> ▶ MIDI 파일이 없으면 이 셀을 실행하세요. 예시 멜로디를 다운로드합니다.

> [코드] — 예시 다운로드
> - wget으로 assets/melody_example.mid 다운로드

#### 3. MIDI → 오디오 변환

> [마크다운]
> ## 3. MIDI를 소리로 변환
>
> MusicGen은 MIDI를 직접 읽지 못하고, **오디오(소리 파형)**를 입력으로 받습니다.
> 그래서 MIDI를 먼저 소리로 변환하는 과정이 필요합니다.
>
> ▶ 아래 셀을 실행하세요.

> [코드] — MIDI → WAV 변환 + 재생
> - fluidsynth 또는 midi2audio로 변환
> - 변환된 오디오 재생 위젯
> - "✅ 변환 완료! 이 소리가 AI의 입력이 됩니다." 출력

#### 4. 모델 로드

> [마크다운]
> ## 4. 멜로디 컨디셔닝 모델 불러오기
>
> 이번에는 '텍스트 → 음악' 노트북에서 사용한 것과는 다른 모델을 사용합니다.
> **musicgen-melody** 모델은 멜로디를 입력받아, 그 위에 새로운 편곡을 입히는 능력이 있습니다.
>
> ⏰ 1~2분 걸립니다. ▶ 아래 셀을 실행하세요.

> [코드] — 모델 로드
> - from audiocraft.models import MusicGen
> - model = MusicGen.get_pretrained('facebook/musicgen-melody')
> - model.set_generation_params(duration=8)
> - "✅ 모델 로딩 완료!" 출력

#### 5. 멜로디 + 프롬프트로 생성

> [마크다운]
> ## 5. 내 멜로디를 새로운 스타일로
>
> ▶ 아래 `prompt`에 원하는 스타일을 적고 실행하세요.
> AI가 여러분의 멜로디를 기반으로 그 스타일의 음악을 만들어줍니다.
>
> **프롬프트 예시:**
> | 프롬프트 | 결과 |
> |---------|------|
> | `transform this melody into a warm jazz arrangement` | 재즈 편곡 |
> | `orchestral version with strings and woodwinds` | 오케스트라 편곡 |
> | `lo-fi hip hop beat built around this piano melody` | 로파이 힙합 |

> [코드] — 멜로디 컨디셔닝 생성 + 재생
> - `prompt = "transform this melody into a warm jazz arrangement"  # ← 여기를 수정하세요`
> - model.generate_with_chroma([prompt], melody_wavs, melody_sample_rate)
> - 결과 오디오 재생
> - 원본 멜로디도 나란히 재생 (비교 청취)

#### 6. 프롬프트 바꿔보기

> [마크다운]
> ## 6. 같은 멜로디, 다른 스타일
>
> ▶ 프롬프트만 바꿔서 다시 실행해보세요.
>
> 💡 같은 멜로디인데 프롬프트에 따라 완전히 다른 음악이 됩니다.
> 재즈가 되기도 하고, 오케스트라가 되기도 합니다.

> [코드] — 다른 프롬프트로 생성
> - `prompt = "orchestral version with strings and woodwinds"  # ← 여기를 수정하세요`
> - 동일 생성 + 재생 코드

#### 7. 결과 다운로드

> [마크다운]
> ## 7. 결과 다운로드
>
> ▶ 마음에 드는 결과물을 다운로드하세요.
> 생성한 음악을 'AI 오디오리액티브' 노트북의 입력으로 사용할 수도 있습니다.

> [코드] — 다운로드
> - google.colab.files.download()

---

## 노트북 5: AI 오디오리액티브 (`05_audio_reactive.ipynb`)

> 웹 매핑: STEP 3 > AI 오디오리액티브 (Step3AudioReactive)
> 웹 설명: "AI가 음악을 '듣고' 영상을 그립니다"

### 도구
- **Stable Diffusion** (diffusers 라이브러리) + **librosa** (오디오 분석) + **ffmpeg** (영상 합성)
- ※ 웹 앱에서 "Deforum Stable Diffusion"으로 안내하던 것을 커스텀 파이프라인으로 대체.
  Deforum은 유지보수가 어렵고 자주 깨지므로 diffusers 기반으로 직접 구성.
  → 웹 앱 Step3AudioReactive 컴포넌트의 도구명을 "Stable Diffusion 오디오리액티브"로 수정 필요.

### 설치할 패키지
- diffusers
- transformers
- accelerate
- librosa
- soundfile
- matplotlib
- Pillow
- ffmpeg-python (또는 시스템 ffmpeg)

### 셀 구조

#### 0. 설치

> [마크다운]
> # 🎬 AI 오디오리액티브 — AI가 음악을 듣고 영상을 그립니다
>
> 피아노 연주를 AI에게 들려주면, 음악의 비트·음량·음색 변화를 분석하여
> **프레임 단위로 이미지를 생성**하고, 이를 이어붙여 영상을 만듭니다.
>
> 조용한 구간에서는 이미지가 부드럽게 흐르고, 클라이맥스에서는 격렬하게 변합니다.
>
> **도구**: Stable Diffusion (이미지 생성) + librosa (오디오 분석) + ffmpeg (영상 합성)
>
> ⏰ 이 노트북은 시간이 걸립니다 (10초 영상 기준 5~10분). 수업 후에 천천히 해보세요.
>
> ▶ 먼저 아래 셀을 실행해주세요. 설치에 2~3분 정도 걸립니다.

> [코드] — 설치
> - %%capture로 출력 숨김
> - apt-get install ffmpeg
> - pip install diffusers transformers accelerate librosa soundfile ffmpeg-python Pillow matplotlib

#### 1. 오디오 업로드

> [마크다운]
> ## 1. 피아노 연주 파일 올리기
>
> ▶ 영상을 만들 피아노 연주 파일을 업로드하세요.
>
> STEP 1~2에서 만든 오디오를 사용하면, 본인의 연주가 영상이 되는 경험을 할 수 있습니다.
> 파일이 없으면 다음 셀에서 예시를 사용하세요.

> [코드] — 업로드
> - google.colab.files.upload()
> - 업로드된 파일 경로 저장

#### 2. 예시 파일 (선택)

> [마크다운]
> ## 2. (선택) 예시 파일 사용
>
> ▶ 파일이 없으면 이 셀을 실행하세요. 쇼팽 녹턴 예시를 다운로드합니다.

> [코드] — 예시 다운로드 + 재생
> - wget으로 assets/piano_chopin.wav 다운로드
> - 원본 오디오 재생 위젯

#### 3. 오디오 분석

> [마크다운]
> ## 3. 음악 특성 분석
>
> 영상에 음악을 반영하려면, 먼저 음악에서 **어떤 변화가 일어나는지** 수치로 추출해야 합니다.
> AI가 분석하는 세 가지 특성:
>
> | 특성 | 의미 | 영상에서의 역할 |
> |------|------|---------------|
> | **RMS (음량)** | 소리의 크기 | 음량 클수록 이미지 변화 격렬 |
> | **Spectral Centroid (음색)** | 소리의 밝기 | 고음 많을수록 밝은 분위기 |
> | **Beat (비트)** | 박자 위치 | 비트마다 장면 전환 |
>
> ▶ 아래 셀을 실행하면 분석 결과를 그래프로 볼 수 있습니다.

> [코드] — librosa 분석 + 시각화
> - librosa로 추출: RMS, spectral centroid, beat
> - matplotlib 시각화:
>   - 파형 + RMS envelope
>   - spectral centroid 곡선
>   - 비트 위치 마커
> - 모든 값을 0~1로 정규화하여 변수에 저장

#### 4. 이미지 생성 모델 로드

> [마크다운]
> ## 4. 이미지 생성 AI 불러오기
>
> **Stable Diffusion**은 텍스트 설명에 맞는 이미지를 생성하는 AI입니다.
> 이 모델로 프레임 하나하나를 만들고, 이어붙여서 영상으로 합칩니다.
>
> ⏰ 모델 로딩에 1~2분 걸립니다. ▶ 아래 셀을 실행하세요.

> [코드] — SD 모델 로드
> - SD 1.5 사용 (T4 메모리 고려, SDXL Turbo도 옵션)
> - FP16 로드
> - pipe.to("cuda")
> - "✅ 모델 로딩 완료!" 출력

#### 5. 프롬프트 입력

> [마크다운]
> ## 5. 영상의 시각적 분위기 설정
>
> ▶ 영상이 어떤 느낌이면 좋겠는지 영어로 적어주세요.
> 이 프롬프트가 모든 프레임의 기본 분위기를 결정합니다.
>
> **프롬프트 예시:**
> | 프롬프트 | 분위기 |
> |---------|-------|
> | `abstract flowing shapes, dark blue and gold, digital art` | 추상적, 어두운 고급감 |
> | `underwater world with bioluminescent creatures` | 신비로운 해저 세계 |
> | `cosmic nebula with swirling colors` | 우주 성운 |

> [코드] — 프롬프트 설정
> - `prompt = "abstract flowing shapes, dark blue and gold, digital art"  # ← 여기를 수정하세요`
> - `negative_prompt = "text, watermark, blurry, low quality"`

#### 6. 음악 ↔ 영상 매핑 원리

> [마크다운] — 설명 전용, 코드 없음
> ## 6. 어떻게 음악이 영상에 반영되나요?
>
> 3단계에서 분석한 음악 특성이 이미지 생성 파라미터에 매핑됩니다:
>
> | 음악 특성 | → | 영상 파라미터 | 효과 |
> |-----------|---|-------------|------|
> | 음량 (RMS) | → | `strength` | 음량 클수록 이미지 변화 격렬 |
> | 음색 (spectral centroid) | → | `guidance_scale` | 고음 많을수록 프롬프트에 충실 |
> | 비트 (beat) | → | seed 변화 | 비트마다 새로운 이미지 전환 |
>
> 조용한 피아노 솔로 → 부드럽게 흐르는 영상
> 포르티시모 클라이맥스 → 화면이 격렬하게 변화
>
> 다음 셀에서 실제로 프레임을 생성합니다.

#### 7. 프레임 생성

> [마크다운]
> ## 7. 프레임 생성
>
> ▶ 아래 셀을 실행하면 프레임을 하나씩 생성합니다. **시간이 가장 오래 걸리는 단계**입니다.
>
> ⏰ 10초 영상 (80프레임) 기준 약 5~10분 소요
>
> 중간중간 생성된 프레임을 미리 볼 수 있습니다.

> [코드] — 프레임 생성 루프
> - `duration_sec = 10  # ← 영상 길이 (초). 조절 가능`
> - `fps = 8  # ← 초당 프레임 수`
> - 프레임별 루프:
>   - 현재 시간의 RMS → strength (0.3~0.8 범위)
>   - 현재 시간의 centroid → guidance_scale (5~12 범위)
>   - 비트 감지 시 seed 변경
>   - img2img 파이프라인으로 이미지 생성
>   - 이전 프레임을 init_image로 사용 (연속성 유지)
> - tqdm 진행률 표시
> - 10프레임마다 중간 결과 표시

#### 8. 영상 합성

> [마크다운]
> ## 8. 프레임 → 영상으로 합치기
>
> 생성된 프레임을 이어붙이고, 원본 음악을 입혀서 최종 영상을 만듭니다.
>
> ▶ 아래 셀을 실행하세요.

> [코드] — ffmpeg 영상 합성
> - ffmpeg로 프레임 이미지들 → 영상
> - 원본 오디오 합치기
> - 최종: output_video.mp4
> - 영상 재생 (IPython.display.HTML 또는 Video)

#### 9. 결과 다운로드

> [마크다운]
> ## 9. 결과 다운로드
>
> ▶ 완성된 영상을 다운로드하세요.

> [코드] — 다운로드
> - google.colab.files.download("output_video.mp4")

---

## 노트북 6: AI 영상 생성 (`06_video_generation.ipynb`)

> 웹 매핑: STEP 3 > AI 영상 생성 (Step3VideoGen)
> 웹 설명: "텍스트 한 줄로 영상을 만든다"

### 도구 (3개 옵션, 독립 섹션)
- **옵션 A: AnimateDiff** — 이미지 → 영상
- **옵션 B: CogVideoX** — 텍스트 → 영상
- **옵션 C: Open-Sora** — 텍스트 → 영상

### 설치할 패키지
- diffusers, transformers, accelerate (공통)
- 각 옵션별 추가 의존성

### 셀 구조

#### 0. 공통 설치

> [마크다운]
> # 🎥 AI 영상 생성 — 텍스트 한 줄로 영상을 만듭니다
>
> 텍스트 설명이나 이미지를 입력하면 AI가 짧은 영상을 만들어줍니다.
> 음악과 별도로 생성한 뒤, 나중에 편집 소프트웨어에서 합치면 뮤직비디오가 됩니다.
>
> 아래 세 가지 도구 중 **원하는 것만 골라서** 실행하세요. 전부 할 필요는 없습니다.
>
> | 도구 | 입력 | 출력 | 특징 |
> |------|------|------|------|
> | **AnimateDiff** | 이미지 + 텍스트 | 2~4초 영상 | 포스터/커버를 움직이게 |
> | **CogVideoX** | 텍스트만 | 4~6초 영상 | 높은 품질, 느림 |
> | **Open-Sora** | 텍스트만 | 영상 | 오픈소스 Sora 대안 |
>
> ▶ 먼저 공통 패키지를 설치합니다.

> [코드] — 공통 설치
> - %%capture로 출력 숨김
> - pip install diffusers transformers accelerate

---

#### 옵션 A: AnimateDiff

> [마크다운]
> ## 옵션 A: AnimateDiff — 이미지를 움직이게
>
> 이미지 1장 + 텍스트 설명을 넣으면 짧은 영상 (2~4초)이 만들어집니다.
> 예를 들어, 앨범 커버 이미지를 넣고 "camera slowly zooming in"이라고 하면
> 카메라가 천천히 다가가는 영상이 됩니다.
>
> ⏰ 생성에 3~5분 소요

> [마크다운]
> ### A-1. 이미지 업로드
>
> ▶ 움직이게 만들 이미지를 업로드하세요. 없으면 예시 이미지를 사용합니다.

> [코드] — 이미지 업로드 또는 예시
> - 업로드 위젯
> - 예시 이미지: 추상적 피아노 이미지 (URL에서 다운로드)
> - 이미지 표시

> [마크다운]
> ### A-2. 프롬프트 입력 → 영상 생성
>
> ▶ 이미지가 어떻게 움직이면 좋겠는지 영어로 적고 실행하세요.

> [코드] — AnimateDiff 실행
> - `prompt = "camera slowly zooming in, soft lighting"  # ← 여기를 수정하세요`
> - AnimateDiffPipeline 로드 (FP16, T4 호환)
> - 생성 → gif 또는 mp4
> - 결과 표시 + 다운로드

---

#### 옵션 B: CogVideoX

> [마크다운]
> ## 옵션 B: CogVideoX — 텍스트만으로 영상 생성
>
> 이미지 없이 **텍스트만으로** 영상을 만듭니다.
> "어두운 콘서트홀에서 피아노를 연주하는 장면"이라고 하면 그런 영상이 생성됩니다.
>
> ⚠️ 모델이 크므로 T4에서 느릴 수 있습니다. 안 되면 Colab Pro가 필요합니다.
>
> ⏰ 생성에 5~10분 소요

> [마크다운]
> ### B-1. 모델 로드
>
> ▶ 아래 셀을 실행하세요. 모델 다운로드에 시간이 걸립니다.

> [코드] — 모델 로드
> - T4 메모리 고려: quantization 또는 경량 버전
> - 안 되면 에러 메시지 + "Colab Pro가 필요합니다" 안내

> [마크다운]
> ### B-2. 프롬프트 입력 → 영상 생성
>
> ▶ 만들고 싶은 영상을 영어로 설명하세요.
>
> 예시: `A grand piano in a dark concert hall, camera slowly zooming in, cinematic lighting`

> [코드] — 생성 + 표시 + 다운로드
> - `prompt = "A grand piano in a dark concert hall, camera slowly zooming in, cinematic lighting"  # ← 여기를 수정하세요`
> - 생성, 결과 표시, 다운로드

---

#### 옵션 C: Open-Sora

> [마크다운]
> ## 옵션 C: Open-Sora — 오픈소스 영상 생성
>
> OpenAI의 Sora와 비슷한 컨셉의 오픈소스 모델입니다.
> 텍스트만으로 영상을 생성합니다.
>
> ⚠️ T4 호환 여부에 따라 실행이 안 될 수 있습니다.
> 안 되는 경우 위의 AnimateDiff나 CogVideoX를 사용하세요.

> [코드] — 설치 + 모델 로드 + 생성
> - T4 호환 검증 후 구체 코드 작성
> - 안 되면 안내 메시지 출력

> [코드] — 다운로드

### 주의사항
- 세 옵션 중 T4에서 실행 불가한 것이 있을 수 있음
- 해당 섹션에 "⚠️ 이 모델은 더 큰 GPU가 필요합니다" 안내 포함
- 각 옵션에 예상 소요 시간 명시

---

## 노트북 7: 이미지 생성 (`07_image_generation.ipynb`)

> 웹 매핑: 마무리 > 더 해보기 (WrapupExploreMore)
> 수업 후 심화용. 포스터, 앨범 커버, 무대 컨셉 이미지 생성.

### 도구 (3개 옵션, 독립 섹션)
- **옵션 A: Flux schnell** — 텍스트 → 이미지 (빠름)
- **옵션 B: Stable Diffusion** — 텍스트 → 이미지 (세밀 조정)
- **옵션 C: SD img2img** — 이미지 변형

### 셀 구조

#### 0. 공통 설치

> [마크다운]
> # 🖼️ AI 이미지 생성 — 포스터, 앨범 커버, 무대 컨셉을 만들어보세요
>
> 텍스트로 이미지를 만들거나, 기존 이미지를 새로운 스타일로 변형할 수 있습니다.
> 공연 포스터, 앨범 커버, 무대 컨셉 이미지 등에 활용해보세요.
>
> 아래 세 가지 도구 중 **원하는 것만 골라서** 실행하세요.
>
> | 도구 | 입력 | 특징 |
> |------|------|------|
> | **Flux schnell** | 텍스트 | 4스텝 초고속 생성 |
> | **Stable Diffusion** | 텍스트 | 세밀한 파라미터 조정 가능 |
> | **SD img2img** | 이미지 + 텍스트 | 기존 이미지를 스타일 변형 |
>
> ▶ 먼저 공통 패키지를 설치합니다.

> [코드] — 공통 설치
> - %%capture로 출력 숨김
> - pip install diffusers transformers accelerate

---

#### 옵션 A: Flux schnell

> [마크다운]
> ## 옵션 A: Flux schnell — 초고속 이미지 생성
>
> Black Forest Labs가 만든 Flux.1 schnell은 **단 4스텝**만에 이미지를 생성합니다.
> Apache 2.0 라이선스로 무료입니다.
>
> ⏰ 이미지 1장 생성에 약 30초

> [마크다운]
> ### A-1. 모델 로드
>
> ▶ 아래 셀을 실행하세요. 모델 다운로드에 1~2분 걸립니다.

> [코드] — 모델 로드
> - FluxPipeline, FP16 또는 quantized (T4 호환)
> - "✅ 모델 로딩 완료!" 출력

> [마크다운]
> ### A-2. 프롬프트 입력 → 이미지 생성
>
> ▶ 만들고 싶은 이미지를 영어로 설명하세요.
>
> **프롬프트 예시:**
> | 프롬프트 | 느낌 |
> |---------|------|
> | `minimalist concert poster, solo pianist on dark stage, single spotlight` | 미니멀 공연 포스터 |
> | `watercolor painting of piano keys transforming into ocean waves` | 수채화 앨범 커버 |
> | `abstract digital art inspired by Chopin nocturne, deep blue and gold` | 추상 디지털 아트 |

> [코드] — 생성 + 표시 + 다운로드
> - `prompt = "minimalist concert poster, solo pianist on dark stage, single spotlight"  # ← 여기를 수정하세요`
> - 1~2장 생성
> - 결과 이미지 표시 + 다운로드

---

#### 옵션 B: Stable Diffusion txt2img

> [마크다운]
> ## 옵션 B: Stable Diffusion — 세밀 조정 이미지 생성
>
> Stable Diffusion은 Flux보다 느리지만, 더 세밀하게 파라미터를 조정할 수 있습니다.
>
> **핵심 파라미터:**
> - `guidance_scale`: 프롬프트에 얼마나 충실할지 (7~12 권장, 높을수록 충실)
> - `num_inference_steps`: 생성 단계 수 (20~50, 많을수록 정교하지만 느림)
> - `negative_prompt`: 원하지 않는 요소 (예: "blurry, low quality, text")

> [마크다운]
> ### B-1. 모델 로드 → 프롬프트 입력 → 생성
>
> ▶ 프롬프트를 수정하고 셀을 실행하세요.

> [코드] — 모델 로드 + 생성 + 표시 + 다운로드
> - SD 1.5 또는 SDXL (T4 메모리 고려)
> - `prompt = "..."  # ← 여기를 수정하세요`
> - `negative_prompt = "blurry, low quality, text, watermark"`
> - `guidance_scale = 7.5  # ← 조정해보세요 (7~12)`
> - `num_inference_steps = 30  # ← 조정해보세요 (20~50)`
> - 결과 표시 + 다운로드

---

#### 옵션 C: img2img — 이미지 스타일 변형

> [마크다운]
> ## 옵션 C: img2img — 기존 이미지를 새로운 스타일로
>
> 본인의 사진이나 그림을 넣고, AI가 새로운 스타일로 변형합니다.
> 예를 들어, 공연 사진을 넣고 "watercolor painting"이라고 하면 수채화풍으로 변합니다.
>
> **핵심 파라미터 — `strength`:**
> - `0.3` → 원본이 거의 유지됨 (살짝 변형)
> - `0.7` → 원본 구도는 남지만 스타일 변형
> - `1.0` → 원본 거의 무시, 완전 새로 생성

> [마크다운]
> ### C-1. 이미지 업로드
>
> ▶ 변형할 이미지를 업로드하세요.

> [코드] — 이미지 업로드
> - 업로드 위젯
> - 업로드된 이미지 표시

> [마크다운]
> ### C-2. 스타일 변형
>
> ▶ 프롬프트와 strength를 수정하고 실행하세요.

> [코드] — 스타일 변형 + 표시 + 다운로드
> - `prompt = "watercolor painting, artistic"  # ← 여기를 수정하세요`
> - `strength = 0.7  # ← 0~1 사이. 조정해보세요`
> - 결과 표시 (원본과 변형 나란히) + 다운로드

---

## 예시 파일 (assets/)

| 파일명 | 용도 | 내용 | 길이 | 출처 |
|--------|------|------|------|------|
| piano_chopin.wav | 자동 채보, 오디오리액티브 | 쇼팽 녹턴 발췌 | 30초 | CC 라이선스 |
| piano_jazz.wav | 자동 채보 | 재즈 피아노 즉흥 | 30초 | CC 라이선스 |
| piano_simple.wav | 자동 채보 | 스케일/아르페지오 | 15초 | 직접 녹음 |
| concerto_example.wav | 소스 분리 | 피아노 협주곡 발췌 | 30초 | CC 라이선스 |
| melody_example.mid | 내 멜로디 + AI | 8마디 피아노 멜로디 | — | 직접 제작 |

---

## 노트북 간 흐름 안내

학생이 STEP 간 결과물 연결을 이해할 수 있도록, 각 노트북의 시작과 끝에 흐름 안내를 넣는다.

| 노트북 | 시작 안내 | 종료 안내 |
|--------|----------|----------|
| 01 자동 채보 | — (첫 노트북) | "이 MIDI를 '내 멜로디 + AI' 노트북에서 사용합니다" |
| 02 소스 분리 | "STEP 1의 두 번째 도구입니다" | "분리한 트랙을 '텍스트 → 음악'이나 '오디오리액티브' 노트북의 입력으로 활용해보세요" |
| 03 텍스트 → 음악 | — | "생성한 음악을 'AI 오디오리액티브' 노트북의 입력으로 사용할 수 있습니다" |
| 04 멜로디 컨디셔닝 | "'자동 채보' 노트북에서 만든 MIDI가 필요합니다" | "생성한 음악을 'AI 오디오리액티브' 노트북의 입력으로 사용할 수 있습니다" |
| 05 오디오리액티브 | "STEP 1~2에서 만든 오디오를 입력으로 사용할 수 있습니다" | — |
| 06 영상 생성 | — | — |
| 07 이미지 생성 | — | — |

---

## 웹 앱 수정 사항

노트북을 7개로 분리함에 따라 웹 앱 컴포넌트도 수정이 필요하다.

### 1. StartPrepare: 단일 노트북 → 개별 노트북 안내

**현재**: "Colab 노트북을 열어주세요" (단수) + "맨 위 '설치' 셀을 실행해주세요"
**수정**: "수업은 단계별로 각각의 Colab 노트북을 사용합니다. 각 페이지에서 해당 노트북을 열 수 있습니다." + 첫 번째로 열 노트북(자동 채보) 링크 제공

### 2. Step1Transcription: "섹션" → "노트북"

**현재**: "STEP 1A: 자동 채보 섹션"
**수정**: "'자동 채보' 노트북" + Colab 열기 버튼 URL 업데이트

### 3. Step1SourceSeparation: "섹션" → "노트북"

**현재**: "STEP 1B: 소스 분리 섹션"
**수정**: "'소스 분리' 노트북" + Colab 열기 버튼 URL 업데이트

### 4. Step2TextToMusic: "섹션" → "노트북"

**현재**: "STEP 2 Part 1: 텍스트 → 음악 섹션"
**수정**: "'텍스트 → 음악' 노트북" + Colab 열기 버튼 URL 업데이트

### 5. Step2MelodyAI: "섹션" → "노트북"

**현재**: "STEP 2 Part 2: 멜로디 컨디셔닝 섹션"
**수정**: "'내 멜로디 + AI' 노트북" + Colab 열기 버튼 URL 업데이트

### 6. Step3AudioReactive: 도구명 변경

**현재**: "Deforum Stable Diffusion" + "Deforum Colab 노트북 열기"
**수정**: "Stable Diffusion 오디오리액티브" + "'AI 오디오리액티브' 노트북 열기" + Colab URL 업데이트

### 7. WrapupExploreMore: 심화 프레이밍 재구성

**현재**: Deforum, AnimateDiff, CogVideoX/Open-Sora, Flux/SD 모두 "심화 노트북"으로 안내
**수정**:
- 상단: "STEP 3에서 소개한 노트북 바로가기" → 노트북 05, 06 링크 (이미 메인 서브메뉴에 있는 것)
- 하단: "추가 심화 노트북" → 노트북 07 (이미지 생성)만 심화로 안내
- Flux/SD가 진짜 유일한 심화 노트북

### 8. 소요 시간 통일

| 항목 | 통일 값 |
|------|---------|
| 패키지 설치 | 2~3분 |
| 오디오리액티브 생성 (10초 기준) | 5~10분 |

---

## 웹 앱 Colab URL 연동

각 노트북이 완성되면 웹 앱의 해당 서브메뉴 컴포넌트에 **"Colab에서 열기"** 버튼의 URL을 업데이트:

| 컴포넌트 | 노트북 | Colab URL 형식 |
|----------|--------|---------------|
| StartPrepare | 01 (첫 노트북) | `https://colab.research.google.com/github/{user}/{repo}/blob/main/notebooks/01_transcription.ipynb` |
| Step1Transcription | 01 | `…/01_transcription.ipynb` |
| Step1SourceSeparation | 02 | `…/02_source_separation.ipynb` |
| Step2TextToMusic | 03 | `…/03_text_to_music.ipynb` |
| Step2MelodyAI | 04 | `…/04_melody_conditioning.ipynb` |
| Step3AudioReactive | 05 | `…/05_audio_reactive.ipynb` |
| Step3VideoGen | 06 | `…/06_video_generation.ipynb` |
| WrapupExploreMore | 05, 06, 07 | 각각 개별 링크 |

---

## 검증 체크리스트

각 노트북 제작 후 확인할 사항:

- [ ] Colab 무료 티어 (T4)에서 처음부터 끝까지 실행 가능
- [ ] 모든 셀에 한글 마크다운 안내가 있음
- [ ] 설치 셀이 에러 없이 완료됨 (2~3분 이내)
- [ ] 예시 파일 다운로드가 정상 작동
- [ ] 결과물이 노트북 내에서 재생/표시됨
- [ ] 다운로드 기능 정상 작동
- [ ] 웹 앱의 해당 서브메뉴 설명과 내용이 일치
- [ ] 노트북 간 참조 시 번호가 아닌 서브메뉴 이름 사용
- [ ] 시작/종료 흐름 안내가 포함되어 있음

웹 앱 수정 후 확인할 사항:

- [ ] StartPrepare의 안내가 개별 노트북 체제와 일치
- [ ] 모든 "섹션" 표현이 "노트북"으로 변경됨
- [ ] Step3AudioReactive의 도구명이 "Stable Diffusion 오디오리액티브"로 변경됨
- [ ] WrapupExploreMore의 심화 노트북 프레이밍이 재구성됨
- [ ] 모든 Colab 링크가 실제 노트북 URL로 연결됨
- [ ] 소요 시간 안내가 노트북과 웹에서 동일
