# **pianokit — 제작 지시서**

이 문서는 Claude Code가 각 단계별 Colab 노트북과 p5.js 코드를 만들 때 참고하는 지시서입니다.

---

## **전체 원칙**

* 대상: 코딩 경험 없는 서울대 음대생  
* 모든 노트북은 Google Colab 무료 티어 (T4 GPU)에서 실행 가능해야 함  
* 모든 셀 위에 한글 마크다운 안내를 넣을 것  
* 오디오 결과물은 IPython.display.Audio로 노트북 내에서 바로 재생 가능하게  
* 이미지 결과물은 matplotlib 또는 IPython.display.Image로 노트북 내에서 바로 표시  
* 파일 다운로드는 google.colab.files.download()로 제공  
* 예시 파일은 GitHub 레포 또는 URL에서 자동 다운로드하는 셀을 포함  
* 에러 메시지를 최소화하도록 버전 핀 및 워닝 suppress 처리

---

## **노트북 1: STEP 1 \+ STEP 2 통합**

수업 시간에 실제로 사용하는 핵심 노트북. 설치를 한 번만 하면 STEP 1과 STEP 2를 모두 커버.

### **파일명**

`01_transcription_generation.ipynb`

### **구조**

```
[0. 설치]
[STEP 1A: 자동 채보]
[STEP 1B: 소스 분리]
[STEP 2 Part 1: 텍스트 → 음악]
[STEP 2 Part 2: 멜로디 컨디셔닝]
[전체 결과물 다운로드]
```

---

### **0\. 설치**

**마크다운:**

```
# 🎹 AI를 활용한 피아노 오디오비주얼 창작
## 서울대학교 공연현장실습 특강

**맨 먼저 이 셀을 실행해주세요.** 필요한 도구들을 설치합니다. 2~3분 정도 걸립니다.
```

**설치할 패키지:**

* basic-pitch  
* demucs  
* audiocraft (MusicGen)  
* librosa  
* soundfile  
* midi2audio (또는 fluidsynth)  
* matplotlib  
* IPython (내장)

**주의사항:**

* audiocraft는 torch 버전에 민감함. Colab 기본 torch와 호환되는 버전으로 설치  
* fluidsynth는 apt-get으로 시스템 패키지 먼저 설치 필요 (MIDI → 오디오 변환용)  
* 설치 후 런타임 재시작이 필요하면 안내 마크다운 추가  
* 설치 로그가 길어지므로 `%%capture` 또는 `> /dev/null 2>&1` 사용해서 출력 최소화

---

### **STEP 1A: 자동 채보**

**마크다운:**

```
## STEP 1A: 자동 채보 — 내 연주를 MIDI로

피아노 연주 오디오를 넣으면 MIDI(악보 데이터)가 나옵니다.
이 MIDI를 STEP 2에서 AI 작곡의 입력으로 사용합니다.
```

**셀 1: 오디오 업로드**

* 마크다운: "▶ 본인 피아노 연주 파일을 업로드하세요. (mp3 또는 wav)"  
* google.colab.files.upload()로 파일 업로드 위젯 제공  
* 업로드된 파일 경로를 변수에 저장  
* 업로드 후 "파일이 업로드되었습니다: {파일명}" 출력

**셀 2: 예시 파일 (업로드 대신 사용)**

* 마크다운: "▶ 녹음 파일이 없으면 이 셀을 실행하세요. 예시 피아노 연주를 다운로드합니다."  
* wget 또는 urllib로 예시 피아노 오디오 다운로드 (GitHub 레포의 assets/에서)  
* 예시 파일 2\~3개 제공 (쇼팽 녹턴 일부, 재즈 피아노, 간단한 스케일)  
* 원본 오디오 재생 위젯

**셀 3: Basic Pitch 실행**

* 마크다운: "▶ 이 셀을 실행하면 AI가 오디오를 분석하여 MIDI로 변환합니다."  
* basic\_pitch.inference.predict()로 오디오 → MIDI 변환  
* 결과: MIDI 파일 저장

**셀 4: 결과 시각화**

* 마크다운: "아래는 AI가 인식한 음표입니다. (피아노롤)"  
* matplotlib으로 피아노롤 시각화  
  * x축: 시간, y축: 피치, 색상: 벨로시티  
  * 보기 좋게 피아노 건반 범위에 맞춰 y축 범위 설정  
* MIDI를 다시 오디오로 변환하여 재생 위젯 제공 (원본과 비교 가능하도록)

**셀 5: MIDI 다운로드**

* 마크다운: "▶ MIDI 파일을 다운로드하세요. STEP 2에서 사용합니다."  
* google.colab.files.download()  
* 파일을 노트북 내 경로에도 유지 (STEP 2에서 자동으로 불러올 수 있도록)

---

### **STEP 1B: 소스 분리**

**마크다운:**

```
## STEP 1B: 소스 분리 — 음원에서 악기별 트랙 분리

음원에서 피아노만 뽑거나, 반주만 남길 수 있습니다.
시간이 부족하면 이 섹션은 수업 후에 해보세요.
```

**셀 1: 오디오 업로드 (또는 예시 파일)**

* 마크다운: "▶ 여러 악기가 섞인 음원을 업로드하세요. (피아노 협주곡 등)"  
* 업로드 위젯  
* 예시 파일: 피아노 협주곡 일부 (저작권 프리 또는 CC 라이선스)

**셀 2: Demucs 실행**

* 마크다운: "▶ 이 셀을 실행하면 음원을 악기별로 분리합니다. 1\~2분 정도 걸립니다."  
* demucs.separate 실행  
* htdemucs 모델 사용 (4-stem: drums, bass, vocals, other)  
* 또는 htdemucs\_ft (6-stem: piano 별도 분리가 더 잘 됨)  
* 진행 상황 표시

**셀 3: 결과 재생**

* 마크다운: "분리된 트랙을 들어보세요."  
* 각 트랙별 재생 위젯:  
  * "🎹 피아노 (또는 other)"  
  * "🥁 드럼"  
  * "🎸 베이스"  
  * "🎤 보컬"  
* 원본과 분리 결과를 번갈아 들을 수 있게

**셀 4: 트랙 다운로드**

* 마크다운: "▶ 원하는 트랙을 다운로드하세요."  
* 각 트랙별 다운로드 또는 전체 zip

---

### **STEP 2 Part 1: 텍스트 → 음악**

**마크다운:**

```
## STEP 2 Part 1: 텍스트 → 음악

원하는 분위기를 텍스트로 설명하면 AI가 음악을 만들어줍니다.
```

**셀 1: 모델 로드**

* 마크다운: "▶ AI 음악 생성 모델을 불러옵니다."  
* audiocraft의 MusicGen 모델 로드  
* 모델 크기: `small` 또는 `medium` (T4 메모리 고려)  
* 로딩 시간 표시

**셀 2: 프롬프트 입력 및 생성**

* 마크다운:

```
▶ 아래에 원하는 음악의 분위기를 영어로 적고 실행하세요.

프롬프트 예시:
- expressive solo piano, Chopin-like nocturne, melancholy
- bright jazz piano trio with upright bass and brushed drums
- ambient piano with deep reverb, minimal, meditative
- dramatic orchestral piece with solo piano, cinematic
- cheerful ragtime piano, Scott Joplin style
```

* 프롬프트 입력: 변수에 문자열로 (셀 상단에서 수정 가능하게)  
* 생성 길이: 8\~10초 (시간 절약)  
* model.generate() 실행  
* 결과 오디오 재생 위젯  
* 결과 오디오 파일 저장

**셀 3: 프롬프트 바꿔보기**

* 마크다운: "▶ 프롬프트를 바꿔서 다시 실행해보세요. 다른 결과가 나옵니다."  
* 위와 같은 구조 반복 (또는 프롬프트 변수만 바꾸고 같은 셀 재실행 안내)

**셀 4: 결과 다운로드**

* google.colab.files.download()

---

### **STEP 2 Part 2: 멜로디 컨디셔닝**

**마크다운:**

```
## STEP 2 Part 2: 내 멜로디 + AI

STEP 1A에서 뽑은 MIDI를 AI에게 들려주면,
여러분의 멜로디를 기반으로 새로운 음악을 만들어줍니다.
```

**셀 1: MIDI → 오디오 변환**

* 마크다운: "▶ STEP 1A에서 만든 MIDI를 오디오로 변환합니다."  
* STEP 1A에서 저장한 MIDI 파일 경로를 자동으로 참조  
* fluidsynth 또는 midi2audio로 MIDI → WAV 변환  
* 변환된 오디오 재생 위젯  
* MIDI 파일이 없는 경우: 예시 MIDI 자동 로드 \+ 안내 메시지

**셀 2: 멜로디 컨디셔닝 생성**

* 마크다운:

```
▶ 아래 프롬프트를 수정하고 실행하세요.
같은 멜로디인데 프롬프트에 따라 완전히 다른 음악이 됩니다.

프롬프트 예시:
- transform this melody into a warm jazz arrangement
- orchestral version with strings and woodwinds
- lo-fi hip hop beat built around this piano melody
```

* melody 파라미터에 변환된 오디오 파일 사용  
* model.generate\_with\_chroma() 사용  
* 결과 오디오 재생  
* 원본 멜로디와 나란히 재생할 수 있게 (비교 청취)

**셀 3: 프롬프트 바꿔보기**

* 같은 멜로디에 다른 프롬프트 → 재실행  
* 2\~3번 반복 유도

**셀 4: 결과 다운로드**

* 마음에 드는 결과물 다운로드  
* "이 음악을 STEP 3에서 비주얼과 합칩니다."

---

### **전체 결과물 다운로드**

**마크다운:**

```
## 전체 결과물 다운로드

오늘 만든 모든 파일을 한 번에 다운로드합니다.
```

* 모든 결과물(MIDI, 분리 트랙, 생성 음악)을 하나의 zip으로 묶어 다운로드  
* 파일 목록 출력

---

## **노트북 2: Deforum Stable Diffusion**

수업 중에는 강사가 미리 만든 결과물만 보여주고, 학생들은 수업 후에 직접 돌려보는 심화 노트북.

### **파일명**

`02_deforum_audio_reactive.ipynb`

### **구조**

```
[0. 설치]
[1. 오디오 업로드]
[2. 오디오 분석]
[3. Stable Diffusion 설정]
[4. 오디오리액티브 파라미터 매핑]
[5. 프레임 생성]
[6. 영상 합성]
[7. 결과 다운로드]
```

### **핵심 요구사항**

* Deforum Stable Diffusion의 Colab 노트북을 기반으로 하되, 한글 안내를 추가하고 불필요한 옵션을 제거하여 단순화  
* 또는 직접 파이프라인 구성: librosa(오디오 분석) \+ diffusers(Stable Diffusion) \+ ffmpeg(영상 합성)  
* 오디오 분석:  
  * librosa로 비트, RMS(진폭), 스펙트럼 특성 추출  
  * 시간별 특성값을 정규화  
* SD 파라미터 매핑:  
  * RMS → guidance\_scale 또는 strength (음량이 클수록 변화 격렬)  
  * 스펙트럼 센트로이드 → 프롬프트 가중치 또는 색상 변화  
  * 비트 → seed 변화 시점 (비트마다 이미지 전환)  
* 프롬프트: 학생이 입력할 수 있게 (예: "abstract flowing shapes, dark blue and gold")  
* FPS: 8\~12 (생성 속도와 품질 균형)  
* 영상 길이: 10\~30초 권장 (너무 길면 시간 오래 걸림)  
* ffmpeg로 프레임 → 영상 합성 \+ 원본 오디오 합치기  
* 최종 결과: mp4 파일 다운로드

### **주의사항**

* T4 GPU에서 SD 1.5 또는 SDXL Turbo 사용 (메모리 고려)  
* 생성 시간 예상치를 안내: "10초 영상 기준 약 5\~15분 소요"  
* 진행률 표시 (tqdm)

---

## **노트북 3: AI 영상 생성**

수업 후 심화용. 텍스트/이미지에서 영상을 생성하는 도구 모음.

### **파일명**

`03_video_generation.ipynb`

### **구조**

```
[0. 설치]
[옵션 A: AnimateDiff — 이미지 → 영상]
[옵션 B: CogVideoX — 텍스트 → 영상]
[옵션 C: Open-Sora — 텍스트 → 영상]
```

### **핵심 요구사항**

* 세 도구를 하나의 노트북에, 각각 독립 섹션으로 구성  
* 학생이 원하는 것만 골라서 실행할 수 있게  
* 각 섹션에 "이 도구는 무엇인가" 한글 설명 포함

**옵션 A: AnimateDiff**

* diffusers 라이브러리의 AnimateDiffPipeline 사용  
* 입력: 이미지 1장 (업로드 또는 예시) \+ 프롬프트  
* 출력: 짧은 영상 (2\~4초, gif 또는 mp4)  
* T4에서 실행 가능한 설정으로

**옵션 B: CogVideoX**

* 입력: 텍스트 프롬프트만  
* 출력: 영상 (4\~6초)  
* T4 메모리를 고려한 경량 설정 (quantization 등)  
* 모델 크기가 크므로, T4에서 돌아가는지 사전 검증 필요. 안 되면 대안 모델 제시.

**옵션 C: Open-Sora**

* 입력: 텍스트 프롬프트  
* 출력: 영상  
* T4 호환 여부 확인 필요

### **주의사항**

* 세 옵션 중 T4에서 실행이 안 되는 것이 있을 수 있음. 그 경우 해당 섹션에 "이 모델은 더 큰 GPU가 필요합니다. Colab Pro를 사용하거나, 로컬에서 실행하세요." 안내  
* 각 옵션에 예상 소요 시간 명시

---

## **노트북 4: 이미지 생성**

수업 후 심화용. Flux와 Stable Diffusion으로 이미지를 생성하는 노트북.

### **파일명**

`04_image_generation.ipynb`

### **구조**

```
[0. 설치]
[옵션 A: Flux schnell — 텍스트 → 이미지]
[옵션 B: Stable Diffusion — 텍스트 → 이미지]
[옵션 C: Stable Diffusion img2img — 이미지 변형]
```

### **핵심 요구사항**

**옵션 A: Flux schnell**

* Black Forest Labs의 Flux.1 schnell 모델 (Apache 2.0)  
* diffusers 라이브러리 사용  
* 4스텝 생성 (빠름)  
* T4에서 실행 가능한 설정 (FP16 또는 quantized)  
* 프롬프트 예시:  
  * "minimalist concert poster, solo pianist on dark stage, single spotlight"  
  * "watercolor painting of piano keys transforming into ocean waves"  
  * "abstract digital art inspired by Chopin nocturne, deep blue and gold"  
* 한 번에 1\~2장 생성  
* 결과 이미지 표시 \+ 다운로드

**옵션 B: Stable Diffusion**

* SD 1.5 또는 SDXL (T4 메모리 고려)  
* diffusers 라이브러리  
* 텍스트 → 이미지  
* 네거티브 프롬프트 가이드 포함  
* 스텝 수, guidance scale 등 파라미터 설명

**옵션 C: img2img**

* 기존 이미지를 입력 → 스타일 변형  
* 업로드 위젯으로 이미지 입력  
* strength 파라미터 설명 (0에 가까울수록 원본 유지, 1에 가까울수록 크게 변형)

---

## **p5.js 코드 4종**

수업 STEP 3 \> 실시간 비주얼 만들기에서 학생들이 복붙하여 사용하는 검증된 코드.

### **파일 위치**

`p5js_codes/` 디렉토리 아래 각각 별도 파일

---

### **코드 1: 파형 (waveform.js)**

**동작:**

* 마이크 입력의 파형(waveform)을 실시간으로 그림  
* 오디오 진폭에 따라 파형의 높이와 색상이 변함  
* 조용할 때: 가느다란 선, 어두운 색  
* 클 때: 두꺼운 파형, 밝은 색

**기술 요구사항:**

* p5.js의 p5.AudioIn()으로 마이크 입력  
* p5.FFT()로 waveform 데이터 추출  
* beginShape() / vertex() / endShape()로 파형 그리기  
* getLevel()로 전체 진폭 → stroke 색상/두께에 매핑  
* 배경: 검은색 (약간의 투명도로 잔상 효과)

---

### **코드 2: 파티클 (particles.js)**

**동작:**

* 마이크 입력의 주파수 스펙트럼에 반응하는 파티클 시스템  
* 저음(bass): 큰 파티클, 느리게 이동  
* 고음(treble): 작은 파티클, 빠르게 이동  
* 전체 진폭에 따라 파티클 생성 속도 변화

**기술 요구사항:**

* p5.FFT()로 스펙트럼 데이터 추출  
* 스펙트럼을 저음/중음/고음 대역으로 나누어 각 대역의 에너지 계산  
* 파티클 클래스: 위치, 속도, 크기, 수명, 색상  
* 매 프레임 진폭에 비례하여 새 파티클 생성  
* 수명이 다하면 fade out  
* 배경: 검은색 (매 프레임 약간 투명하게 덮어서 잔상)

---

### **코드 3: 기하학 (geometric.js)**

**동작:**

* 화면 중앙에 기하학적 도형(원, 다각형)이 비트에 맞춰 확대/축소, 회전  
* 스펙트럼 에너지에 따라 꼭짓점 수와 색상이 변화  
* 비트 감지 시 도형이 펄스(확 커졌다 줄어듦)

**기술 요구사항:**

* p5.FFT()로 스펙트럼 \+ getEnergy('bass')로 저음 에너지  
* 저음 에너지가 임계값을 넘으면 비트로 감지 → 도형 크기 스파이크  
* 도형: beginShape()으로 정다각형 그리기, 꼭짓점 수 \= 중음 에너지에 매핑  
* 회전: frameCount 기반 \+ 에너지에 따라 회전 속도 변화  
* 색상: HSB 모드, hue \= 스펙트럼 센트로이드에 매핑  
* 배경: 검은색

---

### **코드 4: 색면 (color\_field.js)**

**동작:**

* 화면 전체가 오디오에 반응하는 색면  
* 저음이 강할 때: 어두운 색 (남색, 보라)  
* 고음이 강할 때: 밝은 색 (노랑, 흰색)  
* 진폭에 따라 색면의 노이즈/텍스처가 변화

**기술 요구사항:**

* p5.FFT()로 스펙트럼 데이터  
* 화면을 그리드로 나누고 각 셀의 색상을 스펙트럼 값에 매핑  
* noise() 함수로 유기적인 색상 변화  
* 저음 에너지 → 배경 색상의 brightness/hue  
* 고음 에너지 → 그리드 해상도 또는 하이라이트 양  
* lerpColor()로 부드러운 색상 전환

---

### **모든 p5.js 코드 공통 요구사항**

* 코드 첫 줄에 주석으로 제목: `// 🌊 파형 비주얼 — pianokit`  
* 마이크 접근: 사용자가 화면을 클릭해야 오디오 컨텍스트가 시작되도록 (브라우저 정책)  
  * setup()에서 userStartAudio() 호출  
  * "화면을 클릭하면 시작됩니다" 텍스트 표시 → 클릭 후 사라짐  
* 캔버스 크기: windowWidth, windowHeight (전체 화면)  
* windowResized() 함수로 반응형  
* 배경: 검은색 계열  
* 성능: requestAnimationFrame 기반, 60fps 목표  
* p5.js Web Editor (editor.p5js.org)에서 바로 실행 가능해야 함  
  * 외부 라이브러리 import 없이 p5.js 기본 기능 \+ p5.sound만 사용  
* 코드 길이: 각각 80\~150줄 이내 (학생이 읽기 부담 없게)

---

## **예시 파일 (assets/)**

### **피아노 오디오 예시**

수업 중 학생이 녹음을 안 가져왔을 경우를 대비한 예시 파일.

| 파일명 | 내용 | 길이 | 출처 |
| ----- | ----- | ----- | ----- |
| piano\_chopin.wav | 쇼팽 녹턴 발췌 | 30초 | 저작권 프리 또는 CC |
| piano\_jazz.wav | 재즈 피아노 즉흥 | 30초 | 저작권 프리 또는 CC |
| piano\_simple.wav | 간단한 스케일/아르페지오 | 15초 | 직접 녹음 |

### **피아노 협주곡 예시 (소스 분리용)**

| 파일명 | 내용 | 길이 | 출처 |
| ----- | ----- | ----- | ----- |
| concerto\_example.wav | 피아노 협주곡 발췌 | 30초 | 저작권 프리 또는 CC |

### **MIDI 예시 (멜로디 컨디셔닝 대비용)**

| 파일명 | 내용 |
| ----- | ----- |
| melody\_example.mid | 간단한 8마디 피아노 멜로디 |

---

## **GitHub 레포 구조**

```
pianokit/
├── README.md
├── notebooks/
│   ├── 01_transcription_generation.ipynb
│   ├── 02_deforum_audio_reactive.ipynb
│   ├── 03_video_generation.ipynb
│   └── 04_image_generation.ipynb
├── p5js_codes/
│   ├── waveform.js
│   ├── particles.js
│   ├── geometric.js
│   └── color_field.js
├── assets/
│   ├── piano_chopin.wav
│   ├── piano_jazz.wav
│   ├── piano_simple.wav
│   ├── concerto_example.wav
│   └── melody_example.mid
└── resources.md
```

---

## **제작 순서 권장**

1. **p5.js 코드 4종** — 가장 독립적이고 검증이 쉬움. 먼저 만들고 p5.js 에디터에서 테스트.  
2. **노트북 1** (STEP 1+2 통합) — 수업의 핵심. 각 셀을 하나씩 만들며 Colab에서 실행 테스트.  
3. **예시 파일 준비** — 노트북 1 테스트에 필요.  
4. **노트북 4** (이미지 생성) — 비교적 단순. Flux, SD는 diffusers로 패턴이 비슷.  
5. **노트북 2** (Deforum) — 가장 복잡. 노트북 1, 4가 완성된 후 착수.  
6. **노트북 3** (영상 생성) — T4 호환 여부 검증이 핵심. 안 되는 모델이 있을 수 있음.

