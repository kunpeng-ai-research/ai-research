# OpenClaw完整入门指南：5分钟搭建你的个人AI助手

## 一句话总结
OpenClaw是一个自托管AI网关，让你在WhatsApp、Telegram、Discord等任意聊天App中使用AI，数据完全由自己控制。

---

## 什么是OpenClaw？

OpenClaw是一个**自托管网关**，连接你已有的聊天软件（WhatsApp、Telegram、Discord、飞书、微信等）和AI模型（GPT-4、Claude、Gemini、本地Ollama）。

**核心价值**：
- ✅ 数据100%自控，不泄露给第三方
- ✅ 20+平台同时在线，一个助手 everywhere
- ✅ 支持任何AI provider，不绑定单一服务
- ✅ 一次性部署，持续使用，无月费
- ✅ 完全可定制、可扩展

适合人群：注重隐私的开发者、技术爱好者、想要统一AI助手体验的用户。

---

## 5分钟快速安装

### 系统要求
- Node.js 24.x（22.14+ 也可）
- 2GB+ 内存
- 1GB 磁盘空间

### macOS / Linux

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

### Windows

**推荐 WSL2**（更稳定）：

```bash
# 在WSL2终端中运行
curl -fsSL https://openclaw.ai/install.sh | bash
```

**原生 PowerShell**：

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

---

## 初始配置（onboarding）

安装后运行：

```bash
openclaw onboard --install-daemon
```

### 1. 选择AI provider

首次推荐选 **OpenAI** 或 **Anthropic**（需API key）。

也支持：
- Google Gemini
- Azure OpenAI
- 本地模型（Ollama）

### 2. 配置Gateway Token

系统自动生成管理员token，保存到 `.env`。

### 3. 安装为系统服务（可选）

`--install-daemon` 参数会让OpenClaw开机自启。

### 4. 完成

验证Gateway运行：

```bash
openclaw status
```

看到 `Gateway is running` 就成功了。

---

## 连接聊天平台（以Telegram为例）

### 1. 创建Telegram机器人

- 在Telegram中搜索 @BotFather
- 发送 `/newbot`
- 按提示设置名称和用户名
- 复制 BotFather 返回的 **Bot Token**

### 2. 配置OpenClaw

```bash
openclaw config edit
```

在 `plugins` 中添加：

```json5
{
  "plugins": {
    "telegram": {
      "botToken": "你的Bot Token"
    }
  }
}
```

保存并重启：

```bash
openclaw restart
```

### 3. 测试

在Telegram中打开你的机器人，发送：

```
你好
```

你会收到AI的回复！

---

## 其他平台配置

### Discord

1. [Discord Developer Portal](https://discord.com/developers/applications) 创建应用 → 添加Bot → 获取Token
2. 邀请Bot到服务器
3. OpenClaw配置：

```json5
{
  "plugins": {
    "discord": {
      "token": "Bot Token",
      "clientId": "Application ID"
    }
  }
}
```

### 飞书

需要先安装插件：

```bash
openclaw plugins install feishu
```

然后配置 `feishu` 部分（appId + appSecret）。

详细：[Feishu插件文档](https://docs.openclaw.ai/channels/feishu)

### WhatsApp

需要 **BlueBubbles**（macApp），通过它间接连接WhatsApp。

适合Mac用户，配置稍复杂，详见官方文档。

---

## 自定义助手

### 修改名称和头像

编辑 `~/.openclaw/config.json`：

```json5
{
  "agent": {
    "name": "小鲲",
    "avatar": "https://example.com/avatar.png",
    "systemPrompt": "你是一个有用的AI助手，说话简洁明了。"
  }
}
```

### 不同平台不同身份

可以为每个平台设置独立的系统提示词：

```json5
{
  "channels": {
    "telegram": {
      "agent": {
        "name": "Telegram助手",
        "systemPrompt": "在Telegram上，回答要简短，适合手机阅读。"
      }
    }
  }
}
```

---

## 常用命令

```bash
openclaw status      # 查看状态
openclaw logs        # 查看日志
openclaw restart     # 重启网关
openclaw config edit # 编辑配置
openclaw update      # 更新OpenClaw
openclaw doctor      # 健康检查
```

---

## 常见问题

**Q: 可以用本地模型吗？**
A: 可以！配置中选 `ollama` provider，确保 `ollama serve` 在运行。

**Q: 消息延迟高怎么办？**
A: 检查 `openclaw logs` 看是AI provider慢还是网络问题。

**Q: 数据安全吗？**
A: OpenClaw运行在你自己的设备，所有数据存储在本地 `~/.openclaw/`，完全可控。

**Q: 如何备份？**
A: 复制整个 `~/.openclaw/` 目录到新设备即可。

---

## 总结

OpenClaw让你拥有一个**完全可控的AI助手**，支持20+聊天平台，5分钟安装，数据不出你的设备。

如果你想摆脱云端服务的限制，OpenClaw值得一试。

---

## 延伸阅读

- [完整版教程（含高级技巧）](https://kunpeng-ai.com/blog/openclaw-getting-started)
- [OpenClaw官方文档](https://docs.openclaw.ai)
- [OpenClaw GitHub](https://github.com/openclaw/openclaw)
- [支持的平台列表](https://docs.openclaw.ai/channels/index)

---

**本文首发于**：[鲲鹏AI探索局](https://kunpeng-ai.com/blog/openclaw-getting-started)  
**转载请注明出处**
