"""Static regression checks for hand-drawn-explainer-video-nikola."""
from __future__ import annotations

import json
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def text(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def main() -> int:
    skill = text("SKILL.md")
    zh = text("SKILL.zh-CN.md")
    workflow = text("references/stroke-story-workflow.md")
    islands = text("references/semantic-island-storytelling.md")
    quality = text("references/quality-and-delivery.md")
    prefs = json.loads(text("preferences.json"))
    checks = {
        "frontmatter_name": "name: hand-drawn-explainer-video-nikola" in skill,
        "trigger_routes": all(x in skill for x in ("边讲边画", "逐笔双语义岛", "程序动画")),
        "bundled_backend": "vendor/srt-whiteboard-animation" in skill and "不包含第二份 `SKILL.md`" in skill,
        "no_silent_svg_fallback": "不以 SVG 动画冒充真实逐笔绘制" in skill,
        "public_voice_defaults": prefs.get("speaker") == "" and prefs.get("voice_resource") == "",
        "credential_policy": "Never store credentials" in prefs.get("credentials", ""),
        "chinese_entry": "经过解码和画面抽检的 MP4" in zh,
        "backend_runtime_files": all((ROOT / p).is_file() for p in (
            "vendor/srt-whiteboard-animation/scripts/render_stream_whiteboard.py",
            "vendor/srt-whiteboard-animation/scripts/annotation_schema.py",
            "vendor/srt-whiteboard-animation/assets/drawing-hand.png",
            "vendor/srt-whiteboard-animation/LICENSE",
            "vendor/srt-whiteboard-animation/UPSTREAM.md",
        )),
        "backend_not_triggerable": not (ROOT / "vendor/srt-whiteboard-animation/SKILL.md").exists(),
        "skeleton_default": prefs.get("stroke_story_ink_path") == "skeleton",
        "preflight_documented": "stroke_story_preflight.py" in workflow and "prepare_env.py" in workflow,
        "audio_complexity_budget": "区域可用时长 ÷ 线条与色块复杂度" in islands,
        "deterministic_keywords": "确定性 ASS/HTML 文字层" in islands,
        "hand_speed_boundary": "hand-follow" in workflow and "不改变旁白、笔迹" in workflow,
        "final_overlay_opt_in": "--source-overlay never" in workflow,
        "tail_frame_qa": "最后 0.3–0.5 秒" in quality,
        "style_docs": all((ROOT / p).is_file() for p in (
            "references/nikola-absurd-sketch-style.md", "references/q-human-story-style.md", "docs/STYLES.md")),
        "public_docs": all((ROOT / p).is_file() for p in (
            "README.md", "docs/INSTALL.md", "docs/CONFIGURATION.md", "SECURITY.md", "CONTRIBUTING.md")),
        "license_files": all((ROOT / p).is_file() for p in (
            "LICENSE", "LICENSE-MEDIA.md", "THIRD_PARTY_NOTICES.md")),
        "examples": all((ROOT / p).is_file() for p in (
            "examples/stroke-story/steve-jobs/steve-jobs-biography.mp4",
            "examples/program-animation/skill-demo/index.html",
        )),
    }
    print(json.dumps(checks, ensure_ascii=False, indent=2))
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    raise SystemExit(main())
