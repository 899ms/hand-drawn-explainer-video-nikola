# 安装

## 最轻量方式

把仓库目录放到 Codex 的 Skills 目录，并确保文件夹名为 `hand-drawn-explainer-video-nikola`。提示词模式不需要媒体依赖；运行脚本需要 Python 3.10 或更高版本。Windows 若同时安装多个版本，可把下列 `python` 换成 `py -3.12` 或已确认的解释器绝对路径。

```powershell
git clone https://github.com/hi-nikola/hand-drawn-explainer-video-nikola.git "$env:USERPROFILE/.codex/skills/hand-drawn-explainer-video-nikola"
python "$env:USERPROFILE/.codex/skills/hand-drawn-explainer-video-nikola/scripts/setup_check.py"
```

也可以克隆到任意目录，再运行仓库中的 `scripts/install.ps1`。安装器不会覆盖已有目录。

## 启用逐笔故事渲染

逐笔后端已经打包，不需要另装 `srt-whiteboard-animation` Skill。首次运行：

```powershell
python vendor/srt-whiteboard-animation/scripts/prepare_env.py
python scripts/stroke_story_preflight.py --report preflight-stroke-story.json
```

脚本在后端目录创建隔离的 `.venv`，不会写入系统 Python。若公司网络不能访问 Python 包源，可手动创建虚拟环境并安装 `requirements-media.txt`，然后向预检传入 `--backend-python`。

## 完整 MP4 与程序动画

- 最终合成需要 FFmpeg 和 FFprobe；安装后确认两者可从命令行直接调用。
- 程序动画需要 Node.js 20+、Chromium/Chrome/Edge 和 HyperFrames。示例工程会通过 npm 安装 GSAP，不在仓库中复制其发行文件。
- 云配音和图像/视频生成是可选能力，需要各自账号、网络与可能产生的费用。也可以直接提供旁白音频和源图。

## OpenAI Skill 上传

OpenAI Skills API 支持上传一个目录或单个 ZIP。打包时 ZIP 根目录应直接包含 `SKILL.md`，不要多套一层文件夹。具体接口和限制以 [OpenAI 官方 Skills 文档](https://developers.openai.com/api/reference/python/resources/skills/methods/create) 为准。

安装完成后重新启动或刷新支持 Skills 的客户端，并用 README 中的触发提示词测试。
