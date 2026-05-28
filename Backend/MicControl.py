import os
import threading

MIC_FILE = r"Frontend\Files\Mic.data"

HOTKEY = "ctrl+shift+m"


def _ensure_file():
    os.makedirs(os.path.dirname(MIC_FILE), exist_ok=True)
    if not os.path.exists(MIC_FILE):
        with open(MIC_FILE, "w", encoding="utf-8") as f:
            f.write("True")


def is_active() -> bool:
    _ensure_file()
    try:
        with open(MIC_FILE, "r", encoding="utf-8") as f:
            return f.read().strip() == "True"
    except Exception:
        return True


def set_active(state: bool):
    _ensure_file()
    with open(MIC_FILE, "w", encoding="utf-8") as f:
        f.write("True" if state else "False")


def toggle():
    new_state = not is_active()
    set_active(new_state)
    status = "active" if new_state else "sleep"
    print(f"\n  Mic {status}. ({HOTKEY} to toggle)")
    return new_state


def _listen_hotkey():
    import keyboard
    keyboard.add_hotkey(HOTKEY, toggle)
    keyboard.wait()


def start_listener():
    _ensure_file()
    thread = threading.Thread(target=_listen_hotkey, daemon=True)
    thread.start()
