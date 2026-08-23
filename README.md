# AI Intel Brief

AI 情报简报 — 由 [ORCHE](https://github.com/Kevin350350/ORCHE) 的 `ai-intel-brief` Skill 自动生成。

**网站**：<https://ai-intel-brief.icpc.com.tw/>

每份简报包含：今日焦点 · 追踪主题 · 前沿人物动态 · 技术突破 · 开源生态 · Claude Code 专区 · 横向热度 · 行动建议。HTML 内嵌音频播放器（OpenAI TTS 生成）。

## 结构

```
YYYY-MM-DD.html      # 当日简报
audio/YYYY-MM-DD.mp3 # 当日音频
index.html           # 当天简报副本（根目录入口）
```

旧简报改 URL 日期即可查阅：`https://ai-intel-brief.icpc.com.tw/2026-04-18.html`

## 音频保留

HTML 永久保留；站点上的音频采用 **滚动 60 天**保留窗。超过窗口的 MP3 从当前 Git HEAD 移除，但仍可从 Git 历史恢复；旧 HTML 的播放器可能返回 404，这是既定行为，不回补旧音频。

每次生成简报后、commit 前先检查，再执行修剪：

```bash
python3 prune_audio.py --as-of YYYY-MM-DD
python3 prune_audio.py --as-of YYYY-MM-DD --apply
```

脚本以 `git ls-tree` 判断站点实际追踪内容，不依赖 sparse checkout 的本地可见档案。
