#!/usr/bin/env bash
set -euo pipefail

ENV_NAME="pianokit"
PYTHON_VERSION="3.10"

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "${SCRIPT_DIR}"

if ! command -v conda >/dev/null 2>&1; then
  echo "Error: conda가 설치되어 있지 않습니다. (Miniconda/Anaconda 필요)" >&2
  exit 1
fi

# Some conda activation/deactivation hooks reference unset variables.
# Keep nounset for our script, but temporarily relax it around conda shell code.
set +u
eval "$(conda shell.bash hook)"
set -u

run_conda() {
  set +u
  conda "$@"
  local status=$?
  set -u
  return $status
}

GPU_MODE="gpu"
if [[ "${1:-}" == "--cpu" ]]; then
  GPU_MODE="cpu"
elif [[ "${1:-}" == "--gpu" ]]; then
  GPU_MODE="gpu"
fi

if run_conda run -n "${ENV_NAME}" python -c "print('ok')" >/dev/null 2>&1; then
  echo "Conda env '${ENV_NAME}' already exists. Reusing it."
else
  echo "Creating conda env '${ENV_NAME}' (python=${PYTHON_VERSION})..."
  run_conda create -y -n "${ENV_NAME}" "python=${PYTHON_VERSION}" pip
fi

run_conda activate "${ENV_NAME}"

echo "Installing base packages from conda-forge..."
run_conda install -y -c conda-forge \
  jupyterlab notebook ipykernel ipywidgets \
  numpy scipy pandas matplotlib \
  librosa pysoundfile ffmpeg fluidsynth git \
  nodejs

if [[ "${GPU_MODE}" == "gpu" ]] && command -v nvidia-smi >/dev/null 2>&1; then
  echo "Installing GPU PyTorch stack..."
  run_conda install -y -c pytorch -c nvidia pytorch torchvision torchaudio pytorch-cuda=12.1
else
  if [[ "${GPU_MODE}" == "gpu" ]]; then
    echo "GPU mode requested but nvidia-smi was not found. Falling back to CPU PyTorch stack..."
  fi
  echo "Installing CPU PyTorch stack..."
  run_conda install -y -c pytorch pytorch torchvision torchaudio cpuonly
fi

echo "Installing pip packages for current workshop notebooks..."
python -m pip install --upgrade pip
python -m pip install \
  basic-pitch \
  pretty_midi midi2audio mido \
  pillow

WEB_DIR="${SCRIPT_DIR}/pianokit_web"
if [[ -f "${WEB_DIR}/package-lock.json" ]]; then
  echo "Installing web dependencies with npm ci..."
  (
    cd "${WEB_DIR}"
    npm ci
  )
elif [[ -f "${WEB_DIR}/package.json" ]]; then
  echo "Installing web dependencies with npm install..."
  (
    cd "${WEB_DIR}"
    npm install
  )
else
  echo "Skipping web dependency install: package.json not found."
fi

echo "Registering Jupyter kernel..."
python -m ipykernel install --user --name "${ENV_NAME}" --display-name "Python (${ENV_NAME})"

cat <<'EOF'

Setup complete.

How to use:
1) Activate env:
   conda activate pianokit
2) Open notebooks in order:
   01_listen.ipynb       -> 기반: AI가 내 연주를 듣다
   02_visualize.ipynb    -> 확장형·시각: 내 연주가 눈에 보이다
   03_expand.ipynb       -> 확장형·음악: 내 연주를 변주하다
   04_collaborate.ipynb  -> 협업형: AI와 대화하다
   05_stage.ipynb        -> 통합: 무대 위에서
3) In Jupyter, select kernel: Python (pianokit)
4) Start the workshop web app:
   ./web.sh

Options:
- ./setup.sh        # prefer GPU, fallback to CPU if unavailable
- ./setup.sh --gpu  # same as default, explicit GPU preference
- ./setup.sh --cpu  # force CPU stack

EOF
