# 配置

公开仓库不提供个人默认音色、密钥或绝对路径。复制 `config/runtime.example.json` 到项目目录并按项目修改；项目 `DESIGN.md` 和用户当次指令优先。

## 配音

首选顺序：复用稿件一致的已有音轨 → 用户提供音频 → 已授权的 TTS。可选火山脚本通过环境变量读取密钥：

```powershell
$env:VOLCENGINE_TTS_API_KEY = '仅在当前终端设置，不写入仓库'
pwsh -File scripts/volcengine_tts.ps1 -TextFile project/narration.txt -OutputFile project/assets/narration.mp3 -Speaker '<你的音色ID>' -DryRun
```

确认 DryRun 后再移除 `-DryRun`。接口、资源 ID 和音色会变化，调用前核对服务商当前官方文档。不要把真实值写进 `.env.example`、截图、日志或问题单。

## 画面

默认 1920×1080、30fps。竖屏或方屏必须同时更新源图、标注 `canvas`、字幕安全区和最终清单。手部尺寸与 `hand-follow` 分开调；后者只改变手的缓动，不改变笔迹速度。

## 付费与缓存

执行任何云调用前明确提供商、模型、预计次数和缓存策略。网络中断且结果未知时先检查输出与服务记录，不盲目重试。音频缓存必须匹配原稿摘要、声音、模型和文件摘要。
