"""Read-only environment check for hand-drawn-explainer-video-nikola."""
from __future__ import annotations

import importlib.util
import json
from pathlib import Path
import platform
import shutil
import subprocess
import sys
from typing import Optional


ROOT = Path(__file__).resolve().parents[1]
BACKEND = ROOT / "vendor" / "srt-whiteboard-animation"


def command(name: str) -> Optional[str]:
    return shutil.which(name)


def main() -> int:
    venv_python = BACKEND / ".venv" / ("Scripts/python.exe" if platform.system() == "Windows" else "bin/python")
    required_files = [
        ROOT / "SKILL.md",
        BACKEND / "scripts/render_stream_whiteboard.py",
        BACKEND / "scripts/annotation_schema.py",
        BACKEND / "assets/drawing-hand.png",
        BACKEND / "LICENSE",
    ]
    checks: dict[str, object] = {
        "python": {"ok": sys.version_info >= (3, 10), "version": platform.python_version()},
        "skill_files": {"ok": all(p.is_file() for p in required_files)},
        "ffmpeg": {"ok": bool(command("ffmpeg")), "path": command("ffmpeg")},
        "ffprobe": {"ok": bool(command("ffprobe")), "path": command("ffprobe")},
        "node": {"ok": bool(command("node")), "path": command("node")},
        "browser": {"ok": any(command(x) for x in ("chrome", "msedge", "chromium", "chromium-browser"))},
        "powershell": {"ok": bool(command("pwsh") or command("powershell"))},
        "stroke_venv": {"ok": venv_python.is_file(), "path": str(venv_python)},
        "tts_key_configured": {"ok": bool(__import__("os").environ.get("VOLCENGINE_TTS_API_KEY")), "value_exposed": False},
    }
    if venv_python.is_file():
        probe = subprocess.run(
            [str(venv_python), "-c", "import av,cv2,numpy; from PIL import Image; print('ok')"],
            capture_output=True, text=True, timeout=30,
        )
        checks["stroke_dependencies"] = {"ok": probe.returncode == 0}
    else:
        checks["stroke_dependencies"] = {"ok": False, "reason": "run vendor/srt-whiteboard-animation/scripts/prepare_env.py"}

    capabilities = {
        "prompt_only": bool(checks["skill_files"]["ok"]),
        "stroke_story": bool(checks["stroke_venv"]["ok"] and checks["stroke_dependencies"]["ok"]),
        "final_mp4": bool(checks["ffmpeg"]["ok"] and checks["ffprobe"]["ok"]),
        "program_animation": bool(checks["node"]["ok"] and checks["ffmpeg"]["ok"] and checks["ffprobe"]["ok"]),
        "optional_volcengine_tts": bool(checks["powershell"]["ok"] and checks["tts_key_configured"]["ok"]),
    }
    result = {"root": str(ROOT), "checks": checks, "capabilities": capabilities}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if capabilities["prompt_only"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
