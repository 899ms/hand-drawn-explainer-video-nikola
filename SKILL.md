---
name: hand-drawn-explainer-video-nikola
description: 制作、修改和验收中文手绘知识讲解视频，交付配音、字幕、时间轴、可编辑工程和真实 MP4。支持三条清楚分离的路线：彩色 Q 版人物故事的逐笔绘制、怪诞小黑草图的逐笔绘制，以及 SVG/HTML 流程卡片和知识图形的程序动画。用户说“边讲边画”“一笔一笔画出来”“白板手绘”“先画左边再画右边”“知识讲解动画”或希望把文稿、SRT、人物故事做成手绘视频时使用。也支持只输出生图/图生视频提示词。不用于写实数字人或假装已经完成无法验证的成片。
compatibility: Codex Skill。提示词模式无本地依赖；逐笔渲染器已随仓库打包，首次使用需创建隔离 Python 环境；程序动画模式需 Node.js、HyperFrames、浏览器和 FFmpeg。云配音、图像生成和视频模型均为可选能力，可能需要用户自己的账号或费用。
---

# Nikola 手绘讲解视频

把中文主题、文稿或 SRT 变成真正可播放、可检查、可继续编辑的手绘讲解视频。先识别用户要的是“画面被逐笔画出来”，还是“手绘风独立元素运动”；不能为了方便把一种效果冒充另一种效果。

## 先选择交付范围

- **只要提示词**：读 [prompt-workflow.md](references/prompt-workflow.md)，输出自包含提示词，不调用收费接口。
- **样片**：制作用户指定片段；未指定时用 10–15 秒代表镜头验证人物、笔迹、字幕和节奏。
- **完整视频**：先读 [安装与预检](references/preflight-and-recovery.md) 和 [完整流程](references/automation-workflow.md)。先内部验证代表镜头，再继续全片；只有用户要求逐步确认或存在关键选择时才暂停。
- **修改已有视频**：保留未被要求修改的音轨、时间轴和素材，只重做受影响阶段。

## 按视觉意图路由

| 用户真正想要的效果 | 路线 | 必读 |
|---|---|---|
| “画面被画出来”“边讲边画”“逐笔落墨”“笔尖跟着线走” | 逐笔人物/故事 | [stroke-story-workflow.md](references/stroke-story-workflow.md) |
| “讲一部分画一部分”“先左后右”“娓娓道来”并穿插关键词 | 逐笔双语义岛 | [semantic-island-storytelling.md](references/semantic-island-storytelling.md) |
| 怪诞小黑、纯白草图、少量红橙蓝批注 | Nikola 怪诞草图 | [nikola-absurd-sketch-style.md](references/nikola-absurd-sketch-style.md) + 逐笔流程 |
| 流程卡片、概念关系、独立元素组合、确定性文字 | 程序动画 | HyperFrames + SVG/HTML + GSAP，读 [automation-workflow.md](references/automation-workflow.md) |
| 自然连续人物动作或复杂镜头运动 | 场景视频 | 先核实可用视频模型、成本和一致性限制 |
| Flow/Nano Banana 生图或图生视频提示词 | 提示词 | [prompt-workflow.md](references/prompt-workflow.md) |

逐笔路线使用 `vendor/srt-whiteboard-animation/` 中随仓库发布的 MIT 后端快照。它不包含第二份 `SKILL.md`，不会单独触发或要求重复确认；主 Skill 统一负责路由、配音、字幕、渲染和验收。运行环境不可用时保存已完成资产并报告缺口；除非用户明确同意，不以 SVG 动画冒充真实逐笔绘制。

## 可选视觉风格

- **Q 版人物故事**：自然肤色、人物身体、年龄和服装锚点清楚，适合传记、历史和人物观点。参考 [q-human-story-style.md](references/q-human-story-style.md) 与 [乔布斯案例](examples/stroke-story/steve-jobs/README.md)。
- **Nikola 怪诞小黑草图**：纯白、稀疏黑线、少量红橙蓝、留白和冷幽默动作主体，适合方法、系统、状态和隐喻。它是本仓库公开的通用设计预设，不依赖另一个私有 Skill。
- **程序化知识图形**：暖白纸面、可控 SVG 元素、流程卡片和确定性文字，适合规则、步骤、关系和对比。参考 [程序动画案例](examples/program-animation/skill-demo/README.md)。

参考图只影响当前项目，除非用户明确要求保存为新预设。人物、画风、动效和声音分别记录，不把换画风等同于换音色或重做旁白。

## 公开默认与本地配置

仓库中的 [preferences.json](preferences.json) 只含无密钥默认值。用户指令和项目 `DESIGN.md` 优先。配音不是强制能力：可使用用户提供的音频、任意已授权 TTS，或可选的火山脚本；不要因为缺少某个提供商账号阻止提示词和无配音流程。

首次使用先读 [安装说明](docs/INSTALL.md) 和 [配置说明](docs/CONFIGURATION.md)，再运行：

```text
python scripts/setup_check.py
```

完整视频在首次配音或长渲染前还要运行路线对应的预检。预检失败只阻止依赖该能力的阶段，不重做已经通过的音频、插画或字幕。

## 核心制作规则

1. **保留内容**：分别保存原稿、合成读音稿和字幕；未经授权不删观点、数字和限定词。
2. **声音先行**：优先复用内容一致的完整音轨；新音轨尽量整段或按自然章节合成。
3. **时间来自真实音频**：使用有效时间戳、强制对齐或复核后的句级停顿；不能把平均分配说成逐字对齐。
4. **动画服务于解释**：逐笔路线按语义区域持续落墨；程序路线拆成可控元素。整图平移、缩放或淡入淡出只能辅助。
5. **控制可画性**：真实笔迹速度取决于区域时间和源图复杂度；`hand-follow` 只平滑手部，不能让线条真正减速。
6. **精确文字后期生成**：日期、专名、Logo、长中文和关键数字使用字幕或确定性文字层，不交给图片模型猜写。
7. **先验证代表镜头**：检查人物一致性、抬笔、补色、遮挡、关键词和字幕，再批量渲染。
8. **成片必须真实验收**：完整解码 MP4，检查全部场景、语义边界、切点、音轨和最后 0.3–0.5 秒。

## 安全、费用和准确性

- 不把 API Key、Token、Cookie、请求头、本机绝对路径或私有模型目录写入仓库、命令参数、报告或工程 ZIP。
- 账号型配音、生图和视频服务可能收费；先复用缓存，不盲目重试状态不明的请求。
- 真实人物、公司、Logo、日期和数字需要可靠来源或确定性资产。风格参考不能保证实体准确。
- 用户要求完整视频时，最少交付真实 MP4；工具支持时同时保留 SRT、旁白、时间轴、源图、标注和可编辑工程。

质量与交付细节见 [quality-and-delivery.md](references/quality-and-delivery.md)。仓库结构、贡献和许可见 [README](README.md)。
