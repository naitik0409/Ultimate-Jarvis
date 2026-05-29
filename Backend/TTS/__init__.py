import os
import numpy as np
from . import pitch as pitch_module
from . import tone as tone_module
from . import emotion as emotion_module
from . import seriousness as seriousness_module
from . import laugh_caugh as laugh_module

TTS_AUDIO_PATH = os.path.join(os.path.dirname(os.path.dirname(__file__)), "Data", "speech.mp3")


def _load_audio(filepath: str) -> np.ndarray | None:
    if not os.path.exists(filepath) or os.path.getsize(filepath) == 0:
        return None
    try:
        import scipy.io.wavfile as wav
        sr, audio = wav.read(filepath)
        if audio.ndim > 1:
            audio = audio.mean(axis=1)
        audio = audio.astype(np.float64) / 32767.0
        return audio
    except Exception:
        try:
            import subprocess
            import tempfile
            wav_path = filepath.replace(".mp3", ".wav")
            subprocess.run(["ffmpeg", "-y", "-i", filepath, "-ac", "1", "-ar", "16000", wav_path],
                           capture_output=True, timeout=10)
            sr, audio = wav.read(wav_path)
            audio = audio.astype(np.float64) / 32767.0
            return audio
        except Exception:
            return None


def _compute_features(audio: np.ndarray, sr: int = 16000) -> dict:
    if audio is None or len(audio) == 0:
        return {}
    n = len(audio)
    rms = float(np.sqrt(np.mean(audio ** 2)))
    energy = float(np.sum(audio ** 2) / n)
    peak = float(np.max(np.abs(audio)))
    silence = 0.02
    voice_ratio = float(np.sum(np.abs(audio) > silence) / n)
    zero_crossings = float(np.sum(np.abs(np.diff(np.signbit(audio)))) / n)
    segments = np.array_split(audio, max(10, int(n / sr * 2)))
    seg_energies = [float(np.sqrt(np.mean(np.abs(s) ** 2))) for s in segments]
    energy_var = float(np.var(seg_energies)) if seg_energies else 0
    return {
        "duration": n / sr,
        "rms": rms,
        "energy": energy,
        "peak": peak,
        "voice_ratio": voice_ratio,
        "zero_crossing_rate": zero_crossings,
        "energy_variance": energy_var,
        "sample_rate": sr,
        "samples": n,
    }


def analyze_tts_output(filepath: str = TTS_AUDIO_PATH) -> dict:
    audio = _load_audio(filepath)
    if audio is None or len(audio) < 800:
        return {"available": False}

    features = _compute_features(audio)
    pitch_info = pitch_module.detect(audio)
    tone_info = tone_module.analyze(audio, pitch_info=pitch_info, features=features)
    emotion_info = emotion_module.classify(audio, pitch_info=pitch_info, features=features)
    seriousness_info = seriousness_module.analyze(audio, pitch_info=pitch_info, features=features)
    laugh_info = laugh_module.detect(audio, features=features)

    return {
        "available": True,
        "pitch": pitch_info,
        "tone": tone_info,
        "emotion": emotion_info,
        "seriousness": seriousness_info,
        "laugh": laugh_info,
        "features": features,
    }


def describe(filepath: str = TTS_AUDIO_PATH) -> str:
    analysis = analyze_tts_output(filepath)
    if not analysis.get("available"):
        return ""

    parts = []
    if analysis["emotion"].get("emotion") and analysis["emotion"].get("confidence", 0) > 0.3:
        parts.append(emotion_module.describe(analysis["emotion"]))
    if analysis["tone"].get("tone") and analysis["tone"].get("confidence", 0) > 0.3:
        td = tone_module.describe(analysis["tone"])
        if td and "unable" not in td:
            parts.append(td)
    if analysis["seriousness"].get("seriousness", 0.5) > 0.6:
        sd = seriousness_module.describe(analysis["seriousness"])
        if sd and "unable" not in sd:
            parts.append(sd)
    ld = laugh_module.describe(analysis["laugh"])
    if ld:
        parts.append(ld)
    return ". ".join(parts) if parts else ""


__all__ = [
    "analyze_tts_output",
    "describe",
]
