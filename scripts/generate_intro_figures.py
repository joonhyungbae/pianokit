"""
Generate explanatory figures for the three tool intro pages.
Output: pianokit_web/public/figures/
  - basic_pitch_demo.png  (waveform → piano roll)
  - somax_demo.png        (input MIDI → Somax output MIDI)
  - rave_demo.png         (waveform style comparison)
"""
import sys, os, pathlib

# fluidsynth workaround
sys.modules.setdefault("fluidsynth", type(sys)("fluidsynth"))

import numpy as np
import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import mido
import librosa
import soundfile as sf

ROOT = pathlib.Path(__file__).resolve().parent.parent
OUT = ROOT / "pianokit_web" / "public" / "figures"
OUT.mkdir(parents=True, exist_ok=True)

# ── colour palette ──
BG = "#fafafa"
C_WAVE = "#6366f1"       # indigo
C_NOTE = "#3b82f6"       # blue
C_NOTE2 = "#f59e0b"      # amber (somax output)
C_RAVE1 = "#8b5cf6"      # violet
C_RAVE2 = "#10b981"      # emerald
C_RAVE3 = "#f97316"      # orange
C_GRID = "#e5e7eb"
C_TEXT = "#1e293b"
C_MUTED = "#94a3b8"

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

def note_label(midi_num):
    return f"{NOTE_NAMES[midi_num % 12]}{midi_num // 12 - 1}"


def load_midi_notes(path, max_time=None):
    mid = mido.MidiFile(str(path))
    notes = []
    for track in mid.tracks:
        t = 0.0
        active = {}
        for msg in track:
            t += mido.tick2second(msg.time, mid.ticks_per_beat,
                                  mido.bpm2tempo(120))
            if msg.type == "note_on" and msg.velocity > 0:
                active[msg.note] = (t, msg.velocity)
            elif msg.type in ("note_off", "note_on") and msg.note in active:
                start, vel = active.pop(msg.note)
                if max_time and start > max_time:
                    continue
                notes.append((start, t, msg.note, vel))
    return notes


# ═══════════════════════════════════════════
# 1. Basic Pitch demo: waveform + piano roll
# ═══════════════════════════════════════════
def make_basic_pitch_figure():
    wav_path = ROOT / "assets" / "satie_gymnopedie_no1.wav"
    mid_path = ROOT / "artifacts" / "midi" / "satie.mid"

    dur = 15.0  # first 15 seconds
    y, sr = librosa.load(str(wav_path), sr=22050, duration=dur)
    notes = [n for n in load_midi_notes(mid_path) if n[0] < dur]

    fig, (ax_w, ax_p) = plt.subplots(2, 1, figsize=(14, 5.5),
                                      gridspec_kw={"height_ratios": [1, 2]},
                                      facecolor=BG)
    fig.subplots_adjust(hspace=0.28, left=0.07, right=0.97, top=0.90, bottom=0.08)

    # waveform
    t = np.linspace(0, dur, len(y))
    ax_w.fill_between(t, y, color=C_WAVE, alpha=0.35, linewidth=0)
    ax_w.plot(t, y, color=C_WAVE, linewidth=0.3, alpha=0.6)
    ax_w.set_xlim(0, dur)
    ax_w.set_ylabel("녹음 원본", fontsize=12, color=C_TEXT)
    ax_w.set_yticks([])
    ax_w.tick_params(axis="x", labelbottom=False)
    ax_w.spines[["top", "right", "bottom"]].set_visible(False)
    ax_w.spines["left"].set_color(C_GRID)
    ax_w.set_facecolor(BG)

    # piano roll
    if notes:
        pitches = [n[2] for n in notes]
        lo, hi = min(pitches) - 1, max(pitches) + 2
    else:
        lo, hi = 48, 84

    for n_start, n_end, pitch, vel in notes:
        alpha = 0.35 + 0.65 * (vel / 127)
        ax_p.barh(pitch, n_end - n_start, left=n_start, height=0.7,
                  color=C_NOTE, alpha=alpha, linewidth=0)

    ax_p.set_xlim(0, dur)
    ax_p.set_ylim(lo, hi)
    ax_p.set_xlabel("시간 (초)", fontsize=11, color=C_TEXT)
    ax_p.set_ylabel("음높이", fontsize=12, color=C_TEXT)

    tick_pitches = [p for p in range(lo, hi + 1) if p % 12 in (0, 4, 7)]
    ax_p.set_yticks(tick_pitches)
    ax_p.set_yticklabels([note_label(p) for p in tick_pitches], fontsize=9)
    ax_p.tick_params(colors=C_MUTED, labelsize=9)
    ax_p.grid(axis="y", color=C_GRID, linewidth=0.5)
    ax_p.spines[["top", "right"]].set_visible(False)
    ax_p.spines[["left", "bottom"]].set_color(C_GRID)
    ax_p.set_facecolor(BG)

    # label between panels
    fig.text(0.52, 0.56, "▼  Basic Pitch  ▼", fontsize=12, fontweight="bold",
             color=C_NOTE, ha="center", va="center", alpha=0.7)

    fig.suptitle("Satie Gymnopédie No.1 — 처음 15초", fontsize=14,
                 fontweight="bold", color=C_TEXT, y=0.97)

    path = OUT / "basic_pitch_demo.png"
    fig.savefig(str(path), dpi=180, facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {path.relative_to(ROOT)}")


# ═══════════════════════════════════════════
# 2. Somax demo: input vs output piano roll
# ═══════════════════════════════════════════
def make_somax_figure():
    input_mid = ROOT / "artifacts" / "midi" / "satie.mid"
    somax_mids = sorted((ROOT / "artifacts" / "collab_somax").glob("session_*.mid"))

    dur = 20.0
    input_notes = [n for n in load_midi_notes(input_mid) if n[0] < dur]

    somax_notes = []
    if somax_mids:
        somax_notes = [n for n in load_midi_notes(somax_mids[0]) if n[0] < dur]

    fig, (ax_in, ax_out) = plt.subplots(2, 1, figsize=(14, 5.5),
                                         facecolor=BG, sharex=True)
    fig.subplots_adjust(hspace=0.25, left=0.07, right=0.97, top=0.90, bottom=0.08)

    all_pitches = [n[2] for n in input_notes + somax_notes] or list(range(48, 84))
    lo, hi = min(all_pitches) - 1, max(all_pitches) + 2

    for ax, notes, color, label in [
        (ax_in, input_notes, C_NOTE, "내 연주 (원본 MIDI)"),
        (ax_out, somax_notes, C_NOTE2, "Somax가 만든 응답"),
    ]:
        for n_start, n_end, pitch, vel in notes:
            alpha = 0.35 + 0.65 * (vel / 127)
            ax.barh(pitch, n_end - n_start, left=n_start, height=0.7,
                    color=color, alpha=alpha, linewidth=0)
        ax.set_ylim(lo, hi)
        ax.set_ylabel(label, fontsize=12, color=C_TEXT)
        tick_pitches = [p for p in range(lo, hi + 1) if p % 12 in (0, 4, 7)]
        ax.set_yticks(tick_pitches)
        ax.set_yticklabels([note_label(p) for p in tick_pitches], fontsize=9)
        ax.tick_params(colors=C_MUTED, labelsize=9)
        ax.grid(axis="y", color=C_GRID, linewidth=0.5)
        ax.spines[["top", "right"]].set_visible(False)
        ax.spines[["left", "bottom"]].set_color(C_GRID)
        ax.set_facecolor(BG)

    ax_out.set_xlim(0, dur)
    ax_out.set_xlabel("시간 (초)", fontsize=11, color=C_TEXT)

    fig.suptitle("Somax 협업 — 내 악보를 학습한 AI가 새 프레이즈로 응답",
                 fontsize=14, fontweight="bold", color=C_TEXT, y=0.97)

    path = OUT / "somax_demo.png"
    fig.savefig(str(path), dpi=180, facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {path.relative_to(ROOT)}")


# ═══════════════════════════════════════════
# 3. RAVE demo: waveform style comparison
# ═══════════════════════════════════════════
def make_rave_figure():
    rave_dir = ROOT / "artifacts" / "collab_rave"
    wavs = sorted(rave_dir.glob("*.wav"))

    # pick up to 3 style WAVs
    style_wavs = [w for w in wavs if w.stem not in ("stage_extension",)][:3]
    if not style_wavs:
        print("  ⚠ No RAVE WAVs found, skipping")
        return

    dur = 10.0
    n = len(style_wavs)
    colors = [C_RAVE1, C_RAVE2, C_RAVE3][:n]

    fig, axes = plt.subplots(n, 1, figsize=(14, 2.2 * n + 0.8),
                              facecolor=BG, sharex=True)
    if n == 1:
        axes = [axes]
    fig.subplots_adjust(hspace=0.3, left=0.07, right=0.97, top=0.88, bottom=0.10)

    for i, (wav_path, color) in enumerate(zip(style_wavs, colors)):
        y, sr = librosa.load(str(wav_path), sr=22050, duration=dur)
        t = np.linspace(0, len(y) / sr, len(y))
        ax = axes[i]

        ax.fill_between(t, y, color=color, alpha=0.3, linewidth=0)
        ax.plot(t, y, color=color, linewidth=0.3, alpha=0.6)
        ax.set_xlim(0, dur)
        ax.set_yticks([])

        style_name = wav_path.stem.replace("satie_", "").replace("_", " ").title()
        ax.set_ylabel(style_name, fontsize=12, color=C_TEXT, fontweight="bold")

        ax.spines[["top", "right", "bottom"]].set_visible(False)
        ax.spines["left"].set_color(C_GRID)
        ax.set_facecolor(BG)

    axes[-1].set_xlabel("시간 (초)", fontsize=11, color=C_TEXT)
    axes[-1].spines["bottom"].set_visible(True)
    axes[-1].spines["bottom"].set_color(C_GRID)

    fig.suptitle("RAVE 음색 변환 — 같은 선율, 다른 질감",
                 fontsize=14, fontweight="bold", color=C_TEXT, y=0.96)

    path = OUT / "rave_demo.png"
    fig.savefig(str(path), dpi=180, facecolor=BG)
    plt.close(fig)
    print(f"  ✓ {path.relative_to(ROOT)}")


if __name__ == "__main__":
    from matplotlib import font_manager as fm
    font_path = "/usr/share/fonts/opentype/noto/NotoSansCJK-Regular.ttc"
    if os.path.exists(font_path):
        fm.fontManager.addfont(font_path)
        plt.rcParams["font.family"] = fm.FontProperties(fname=font_path).get_name()
    else:
        plt.rcParams.update({
            "font.family": "sans-serif",
            "font.sans-serif": ["Noto Sans CJK KR", "NanumGothic", "DejaVu Sans"],
        })
    print("Generating intro figures...")
    make_basic_pitch_figure()
    make_somax_figure()
    make_rave_figure()
    print("Done.")
