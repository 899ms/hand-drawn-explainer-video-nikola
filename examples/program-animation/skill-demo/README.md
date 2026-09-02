# 程序动画示例

36 秒可编辑 HTML/SVG/HyperFrames 工程，展示八个镜头、整段旁白、时间轴和确定性文字。它适合流程、关系和独立元素运动，不是逐笔故事路线。

```powershell
npm install
npm run check
npm run dev
npm run render
```

`npm install` 安装固定版本的 GSAP；生命周期脚本从 npm 包复制浏览器文件到 `assets/gsap.min.js`。该生成文件不提交到仓库，许可遵循 GSAP 自身条款。HyperFrames 由命令按固定版本调用。

旁白只作案例资产。新项目应按用户提供的声音、音轨或已授权 TTS 重新配置，不能把案例音色当成所有用户的默认值。
