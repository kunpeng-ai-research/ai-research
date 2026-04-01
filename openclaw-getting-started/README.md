# OpenClaw 入门指南 - 从零搭建个人AI助手

[![中文教程](https://img.shields.io/badge/中文-教程-blue)](https://kunpeng-ai.com/blog/openclaw-getting-started)
[![English Guide](https://img.shields.io/badge/English-Guide-green)](https://kunpeng-ai.com/en/blog/openclaw-getting-started)
[![OpenClaw](https://img.shields.io/badge/OpenClaw-自托管AI网关-orange)](https://github.com/openclaw/openclaw)

> 本文由鲲鹏AI探索局整理，首发于 https://kunpeng-ai.com

---

## 📖 简介

本仓库收录了 **OpenClaw 完整入门指南** 的配套内容和示例代码。

OpenClaw 是一个自托管 AI 网关，让你在 WhatsApp、Telegram、Discord、飞书等任意聊天 App 中使用 AI，数据完全由自己控制。

**核心特性**：
- ✅ 支持 20+ 聊天平台
- ✅ 可对接 OpenAI、Anthropic、Google、Ollama 等任何 AI provider
- ✅ 数据完全自控，无隐私泄露风险
- ✅ 5分钟快速安装，跨平台支持
- ✅ 插件化架构，高度可扩展

---

## 🚀 快速开始

### 1. 安装 OpenClaw

**macOS / Linux**：
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows（推荐 WSL2）**：
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows PowerShell**：
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

### 2. 运行配置向导

```bash
openclaw onboard --install-daemon
```

按提示选择 AI provider（OpenAI/Anthropic/Ollama 等），配置 API key。

### 3. 连接聊天平台（以 Telegram 为例）

1. Telegram 搜索 @BotFather → `/newbot` → 获取 Bot Token
2. 编辑 `~/.openclaw/config.json`：

```json5
{
  "plugins": {
    "telegram": {
      "botToken": "你的Bot Token"
    }
  }
}
```

3. 重启：`openclaw restart`
4. 在 Telegram 中打开你的机器人，开始对话！

---

## 📚 详细教程

| 语言 | 链接 |
|------|------|
| **中文完整教程** | [📖 阅读全文](https://kunpeng-ai.com/blog/openclaw-getting-started) |
| **English Guide** | [📖 Read Full Guide](https://kunpeng-ai.com/en/blog/openclaw-getting-started) |

教程包含：
- OpenClaw 技术架构解析
- 各平台安装配置（Telegram、Discord、飞书、WhatsApp、iMessage）
- 自定义助手身份和系统提示词
- 自动化任务（Cron Jobs）
- 自定义技能开发
- 故障排查与性能优化
- 生产环境部署建议

---

## 🛠️ 示例配置

### 多平台差异化身份

```json5
{
  "channels": {
    "telegram": {
      "agent": {
        "name": "TG助手",
        "systemPrompt": "Telegram回答简短，适合手机阅读"
      }
    },
    "discord": {
      "agent": {
        "name": "Discord Bot",
        "systemPrompt": "Discord可以活泼点，用emoji"
      }
    }
  }
}
```

### 本地模型 + 云端 fallback

```json5
{
  "models": {
    "default": {
      "provider": "openai",
      "model": "gpt-4o"
    },
    "fallback": {
      "provider": "ollama",
      "model": "llama3.2:3b",
      "baseUrl": "http://localhost:11434"
    }
  }
}
```

---

## 📦 本项目结构

```
.
├── README.md                    # 本文件
├── blog-article-zh.mdx          # 中文博客原文（MDX格式）
├── blog-article-en.mdx          # 英文博客原文
├── articles/                    # 各平台文章版本
│   ├── zhihu-answer-v2.md      # 知乎精简版（950字）
│   ├── wechat-article-v2.md    # 公众号版（2000字+配图说明）
│   ├── csdn-article-v2.md      # CSDN版（4000字，技术关键词前置）
│   ├── reddit-post.md          # Reddit讨论帖
│   └── xiaohongshu-post.md     # 小红书合规图文
├── images/                      # 配图资源
│   ├── openclaw-getting-started-cover.png  # 封面图 1200×630
│   ├── xiaohongshu_01.png ~ xiaohongshu_09.png  # 小红书9张竖屏图
│   └── (其他截图...)
└── scripts/                     # 生成脚本
    ├── generate-cover.py       # 封面图生成
    └── generate-xiaohongshu-images.py  # 小红书图片生成
```

---

## 🔧 常用命令速查

```bash
openclaw status              # 查看状态
openclaw logs                # 查看日志
openclaw restart             # 重启网关
openclaw config edit         # 编辑配置
openclaw plugins list        # 列出插件
openclaw cron list           # 列出定时任务
openclaw update              # 更新OpenClaw
openclaw doctor              # 健康检查
```

---

## ❓ 常见问题

**Q: 可以用本地模型吗？**  
A: 可以！装 [Ollama](https://ollama.com)，配置 `provider: "ollama"`。

**Q: 消息延迟高怎么办？**  
A: 检查 `openclaw logs`，看是AI provider慢还是网络问题。

**Q: 数据安全吗？**  
A: OpenClaw运行在你自己的设备，数据存储在 `~/.openclaw/`，完全可控。

**Q: 如何备份？**  
A: 复制整个 `~/.openclaw/` 目录即可。

更多FAQ请阅读完整教程。

---

## 📚 相关资源

- **[OpenClaw 官方文档](https://docs.openclaw.ai)** - 最权威的参考资料
- **[OpenClaw GitHub](https://github.com/openclaw/openclaw)** - 源码、Issues、PR
- **[OpenClaw Discord](https://discord.gg/clawd)** - 活跃社区，快速答疑
- **[支持的平台列表](https://docs.openclaw.ai/channels/index)** - 20+平台完整列表
- **[自动化指南](https://docs.openclaw.ai/automation/cron-jobs)** - Cron、Heartbeat、Hooks
- **[技能开发](https://docs.openclaw.ai/cli/agent)** - 自定义TypeScript技能

---

## 🤝 贡献

本仓库内容采用 CC BY-NC-SA 4.0 协议，欢迎分享和引用。

发现错误？欢迎提 Issue 或 PR。

---

## 📄 许可证

教程内容：CC BY-NC-SA 4.0  
OpenClaw 本身：MIT License

---

## 👤 关于作者

**鲲鹏AI探索局** - 专注 AI Agent 与自托管方案

- 博客：https://kunpeng-ai.com
- GitHub：https://github.com/kunpeng-ai
- Twitter/X：[@kunpeng_ai](https://x.com/kunpeng_ai)（待开通）

---

**最后更新**: 2026-03-30  
**OpenClaw 版本**: 2026.3.24

---

## ⭐ 如果本教程对你有帮助，请给 OpenClaw 官方仓库点 Star！

[![Star OpenClaw](https://img.shields.io/github/stars/openclaw/openclaw?style=social)](https://github.com/openclaw/openclaw)
