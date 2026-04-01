# 5分钟打造你的专属AI助手 🦞

大家好～我是鲲鹏AI探索局🐋

今天分享一个超酷的开源项目——OpenClaw，让你拥有完全可控的AI助手📱

---

## 📌 什么是OpenClaw？

简单说：**一个自托管AI网关**

你可以把它理解为一个"翻译官"：
你的聊天App（微信/Telegram/Discord） ↔ OpenClaw ↔ AI模型（GPT-4/Claude/Ollama）

✅ 数据完全自己控制，不泄露  
✅ 支持20+聊天平台  
✅ 一次部署，永久使用  
✅ 无需月费，只付API成本（或本地0成本）

---

## 🎯 我为什么选它？

之前用ChatGPT Plus，每月$20，还不能在手机App以外的地方用😅

OpenClaw解决了：
- 隐私担忧（数据不出我的VPS）
- 平台限制（Telegram/Discord都能聊）
- 成本（$5 VPS + ~$10 OpenAI API ≈ $15/月，更便宜）
- 自由度（随时换模型，自己写技能）

用了3个月，稳如老狗🐶

---

## ⚡ 5分钟安装教程

### 系统要求
- Node.js 24.x
- 2GB+ 内存
- 任意OS（macOS/Linux/Windows-WSL2）

### 一键安装

**macOS/Linux**：
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows**（推荐WSL2）：
同上，在WSL2里运行

**Windows PowerShell**：
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

---

## 🚀 初始配置

安装完运行：

```bash
openclaw onboard --install-daemon
```

按提示：
1. 选AI provider（OpenAI/Anthropic/Ollama等）
2. 填API key（或本地模型配置）
3. 生成Gateway token（自动保存）
4. 安装为系统服务（开机自启）

完成！🎉

---

## 📱 连接聊天平台

以**Telegram**为例：

### 1. 创建机器人

- Telegram搜索 @BotFather
- `/newbot` → 设置名字/用户名
- 复制Bot Token

### 2. 配置OpenClaw

编辑 `~/.openclaw/config.json`：

```json5
{
  "plugins": {
    "telegram": {
      "botToken": "你的Token"
    }
  }
}
```

重启：`openclaw restart`

### 3. 测试

Telegram打开你的机器人，发消息，收到AI回复！✅

---

## 🌐 其他平台

| 平台 | 难度 | 说明 |
|------|------|------|
| Telegram | ⭐ | 最简单，Bot API |
| Discord | ⭐⭐ | 需去开发者门户创建Bot |
| 飞书 | ⭐⭐ | 需安装feishu插件，配置Webhook |
| WhatsApp | ⭐⭐⭐ | 需BlueBubbles（Mac服务） |
| iMessage | ⭐⭐⭐ | 需BlueBubbles |

支持20+平台，详见官方文档📖

---

## 🎨 自定义助手

### 改名+头像

```json5
{
  "agent": {
    "name": "小鲲",
    "avatar": "https://xxx.com/avatar.png",
    "systemPrompt": "你是AI助手，说话简洁..."
  }
}
```

### 不同平台不同性格

Telegram简短，Discord活泼，飞书专业…自由配置

---

## 💡 我每天怎么用？

- **Telegram**：快速提问代码问题
- **Discord**：在服务器里@机器人查资料
- **iMessage**：手机聊天（通过BlueBubbles）
- **Cron任务**：每天早上9点发日报

---

## 📊 成本与性能

我的配置：
- VPS：$5/月（2核4G）
- OpenAI API：~$10/月
- **总计**：$15/月 vs ChatGPT Plus $20/月

优势：
- 支持所有平台
- 数据自己控制
- 随时切模型
- 可扩展技能

---

## ❓ 常见问题

**Q: 能用本地模型吗？**  
A: 可以！装Ollama，配置`provider: "ollama"`，0 API成本

**Q: 数据安全吗？**  
A: 完全在你自己的机器，只要provider可信就OK

**Q: 安装复杂吗？**  
A: 5分钟脚本搞定，新手按教程没问题

**Q: 适合我吗？**  
适合：技术爱好者、开发者、注重隐私的人  
不适合：完全不想折腾的用户

---

## 📚 完整教程

详细的安装+配置+高级技巧，我整理了一篇长文：

**完整博客** 👉 https://kunpeng-ai.com/blog/openclaw-getting-started

（包含所有代码片段、配置示例、故障排查）

---

## 💬 互动时间

你们会用OpenClaw做什么？  
有没有类似的自托管项目推荐？  
评论区聊聊～👇

---

#OpenClaw #AI助手 #自托管 #开源 #技术分享 #开发者

---

*本帖纯分享，无广告。OpenClaw完全开源免费（MIT协议）。*

*本帖内容基于我个人使用经验，如有错误欢迎指正。*
