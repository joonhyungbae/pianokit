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

eval "$(conda shell.bash hook)"

GPU_MODE="auto"
if [[ "${1:-}" == "--cpu" ]]; then
  GPU_MODE="cpu"
elif [[ "${1:-}" == "--gpu" ]]; then
  GPU_MODE="gpu"
fi

if conda run -n "${ENV_NAME}" python -c "print('ok')" >/dev/null 2>&1; then
  echo "Conda env '${ENV_NAME}' already exists. Reusing it."
else
  echo "Creating conda env '${ENV_NAME}' (python=${PYTHON_VERSION})..."
  conda create -y -n "${ENV_NAME}" "python=${PYTHON_VERSION}" pip
fi

conda activate "${ENV_NAME}"

echo "Installing base packages from conda-forge..."
conda install -y -c conda-forge \
  jupyterlab notebook ipykernel ipywidgets \
  numpy scipy pandas matplotlib \
  librosa soundfile ffmpeg fluidsynth git

if [[ "${GPU_MODE}" == "gpu" ]] || { [[ "${GPU_MODE}" == "auto" ]] && command -v nvidia-smi >/dev/null 2>&1; }; then
  echo "Installing GPU PyTorch stack..."
  conda install -y -c pytorch -c nvidia pytorch torchvision torchaudio pytorch-cuda=12.1
else
  echo "Installing CPU PyTorch stack..."
  conda install -y -c pytorch pytorch torchvision torchaudio cpuonly
fi

echo "Installing pip packages for all notebooks..."
python -m pip install --upgrade pip
python -m pip install \
  basic-pitch \
  pretty_midi midi2audio \
  demucs \
  audiocraft \
  diffusers transformers accelerate safetensors bitsandbytes sentencepiece \
  einops \
  imageio imageio-ffmpeg \
  opencv-python pillow \
  tqdm

echo "Registering Jupyter kernel..."
python -m ipykernel install --user --name "${ENV_NAME}" --display-name "Python (${ENV_NAME})"

cat <<'EOF'

Setup complete.

How to use:
1) Activate env:
   conda activate pianokit
2) Open notebooks:
   jupyter lab
3) In Jupyter, select kernel:
   Python (pianokit)

Options:
- ./setup.sh        # auto detect GPU (nvidia-smi 기준)
- ./setup.sh --gpu  # force GPU stack
- ./setup.sh --cpu  # force CPU stack

EOF
