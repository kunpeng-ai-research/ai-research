# OpenClaw 完整入门指南：5分钟搭建你的个人AI助手

> 作者：鲲鹏AI探索局  
> 原创首发于：https://kunpeng-ai.com/blog/openclaw-getting-started

---

## 一、什么是OpenClaw？

你是否厌倦了ChatGPT的月费、Claude的配额限制、以及各种云端AI的数据隐私担忧？

OpenClaw给你一个全新的选择：**完全自托管的AI网关**。

简单说，OpenClaw是一个"翻译官"：
- 你的聊天软件（WhatsApp/Telegram/Discord/飞书） → OpenClaw → AI模型（GPT-4/Claude/Ollama）

**整个过程在你自己的设备上完成，数据绝不外泄。**

![OpenClaw架构图](架构图-placeholder.png)

---

## 二、为什么选OpenClaw？

### 对比：OpenClaw vs 云端AI助手

| 维度 | OpenClaw | ChatGPT/Claude |
|------|----------|---------------|
| 数据隐私 | ✅ 100%自控 | ❌ 第三方服务器 |
| 平台支持 | ✅ 20+平台同时在线 | ❌ 只能官方App |
| 模型选择 | ✅ 任意provider | ❌ 只能provider自家模型 |
| 成本 | ✅ 一次性部署 | ❌ 按月付费 |
| 可定制性 | ✅ 完全自由 | ❌ 封闭系统 |
| 可用性 | ✅ 24/7离线可用 | ❌ 依赖外网 |

**一句话：OpenClaw让你做AI的主人，而不是租客。**

---

## 三、5分钟快速安装

### 系统要求

- Node.js 24.x（22.14+ 也可）
- 2GB+ 内存（运行模型建议4GB+）
- 1GB 磁盘空间
- 能访问AI provider API（如果用本地模型则不需要网络）

### 安装命令

**macOS / Linux：**

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows（推荐WSL2）：**

```bash
# 在WSL2终端中运行
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows原生（PowerShell）：**

```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

---

## 四、初始配置（2分钟）

安装完成后，运行引导：

```bash
openclaw onboard --install-daemon
```

### 第1步：选择AI provider

OpenClaw支持：
- **OpenAI**（GPT-4, GPT-4o, o1等）
- **Anthropic**（Claude 3.5 Sonnet, Claude 3 Opus）
- **Google**（Gemini Pro, Gemini Flash）
- **本地模型**（通过Ollama）

首次使用，建议选OpenAI或Anthropic（需要API key）。

### 第2步：配置Gateway Token

系统自动生成管理员token，保存到 `.env` 文件。**请妥善保管**。

### 第3步：安装为系统服务

`--install-daemon` 参数会让OpenClaw开机自启，实现24/7在线。

### 第4步：完成

验证Gateway是否运行：

```bash
openclaw status
```

看到 `Gateway is running on http://127.0.0.1:8080` 就表示成功！

---

## 五、连接聊天平台（以Telegram为例）

### 1. 创建Telegram机器人

1. 打开Telegram，搜索 **@BotFather**
2. 发送 `/newbot`
3. 按提示输入机器人名称和用户名
4. BotFather会返回一个 **Bot Token**（长字符串）

![Telegram BotFather截图](telegram-botfather-placeholder.png)

### 2. 配置OpenClaw

```bash
openclaw config edit
```

在 `plugins` 部分添加：

```json5
{
  "plugins": {
    "telegram": {
      "botToken": "你的Bot Token"
    }
  }
}
```

保存文件，重启Gateway：

```bash
openclaw restart
```

### 3. 测试

在Telegram中打开你的机器人，发送消息：

```
你好，你是谁？
```

几秒后，你会收到AI的智能回复！

---

## 六、其他平台快速配置

### Discord

1. [Discord开发者门户](https://discord.com/developers/applications) 创建应用 → 添加Bot → 复制Token
2. 邀请Bot到你的服务器（需要 `bot` 权限）
3. OpenClaw配置：

```json5
{
  "plugins": {
    "discord": {
      "token": "你的Bot Token",
      "clientId": "你的Application ID"
    }
  }
}
```

![Discord Bot邀请截图](discord-bot-placeholder.png)

### 飞书（Feishu）

需要先安装插件：

```bash
openclaw plugins install feishu
```

然后在 `~/.openclaw/config.json` 中配置：

```json5
{
  "plugins": {
    "feishu": {
      "appId": "你的App ID",
      "appSecret": "你的App Secret"
    }
  }
}
```

详细配置参考：[飞书插件官方文档](https://docs.openclaw.ai/channels/feishu)

### WhatsApp

WhatsApp不支持Bot API，需要通过 **BlueBubbles**（macOS服务）间接连接。

适合Mac用户，配置稍复杂，详见官方文档。

---

## 七、自定义你的助手

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

重启后生效。

### 设置System Prompt

`systemPrompt` 决定了助手的性格和行为。

**示例：技术助手风格**

```json5
{
  "agent": {
    "systemPrompt": "你是鲲鹏AI探索局的助手，专门帮助开发者解决AI/ML技术问题。\n\n你的原则：\n- 回答简洁，不啰嗦\n- 提供可执行的代码示例\n- 遇到不确定的问题会说\"我不确定\"而不是瞎猜\n- 对技术问题保持专业，对闲聊可以轻松一点"
  }
}
```

### 不同平台不同身份

OpenClaw允许为每个平台设置独立身份：

```json5
{
  "channels": {
    "telegram": {
      "agent": {
        "name": "Telegram助手",
        "systemPrompt": "在Telegram上，回答要简短，适合手机阅读，最多3句话。"
      }
    },
    "discord": {
      "agent": {
        "name": "Discord Bot",
        "systemPrompt": "在Discord服务器，可以适当使用emoji，语气活泼一点。"
      }
    }
  }
}
```

---

## 八、常用命令速查

```bash
# 查看状态
openclaw status

# 查看日志（排查问题）
openclaw logs

# 重启网关
openclaw restart

# 编辑配置
openclaw config edit

# 查看已安装插件
openclaw plugins list

# 安装新插件
openclaw plugins install <插件名>

# 卸载插件
openclaw plugins uninstall <插件名>

# 直接向AI发消息（测试用）
openclaw agent --message "你的消息"

# 更新OpenClaw
openclaw update

# 健康检查
openclaw doctor
```

---

## 九、常见问题 FAQ

**Q1: 可以用本地模型吗？怎么连Ollama？**

可以！在配置中选 `ollama` provider：

```json5
{
  "models": {
    "default": {
      "provider": "ollama",
      "model": "llama3.2:3b",
      "baseUrl": "http://localhost:11434"
    }
  }
}
```

确保Ollama在运行：`ollama serve`

**Q2: 消息延迟高怎么办？**

可能原因：
- AI provider响应慢（OpenAI高峰期常见）
- 网络问题
- 消息太长，模型生成本身就慢

解决：`openclaw logs` 查看日志，定位问题。

**Q3: 数据安全吗？**

OpenClaw运行在你自己的设备，所有消息、配置都存储在本地 `~/.openclaw/`。只要你不选不靠谱的provider，数据就不会流出你的控制范围。

**Q4: 如何备份和迁移？**

整个OpenClaw工作目录就是你的全部配置。复制 `~/.openclaw/` 到新设备，重新安装OpenClaw，把目录放回去即可。

**Q5: 可以同时连多个平台吗？**

当然！OpenClaw的设计就是一次部署，多平台同时在线。配置越多平台，体验越统一。

---

## 十、总结

OpenClaw给你一个**完全可控的AI助手**，它不是ChatGPT的替代品，而是升级版：

- ✅ 数据自控，隐私无忧
- ✅ 20+平台统一体验
- ✅ 支持任何AI模型
- ✅ 一次部署，永久使用
- ✅ 完全可定制

**5分钟安装，无限可能。**

---

## 下一步

完成基础配置后，你可以：

1. **探索插件系统**：浏览器自动化、文件操作、数据库查询等强大功能
2. **学习自动化**：用cron jobs做定时任务，heartbeat做周期性检查
3. **开发自定义技能**：用JavaScript/TypeScript写自己的工具
4. **多设备部署**：把Gateway部署到树莓派、服务器，实现24/7在线

---

## 相关链接

- **完整版教程**：[OpenClaw完整入门指南（含高级技巧）](https://kunpeng-ai.com/blog/openclaw-getting-started)
- **官方文档**：[docs.openclaw.ai](https://docs.openclaw.ai)
- **GitHub仓库**：[github.com/openclaw/openclaw](https://github.com/openclaw/openclaw)
- **Discord社区**：[discord.gg/clawd](https://discord.gg/clawd)
- **支持的平台**：[docs.openclaw.ai/channels/index](https://docs.openclaw.ai/channels/index)

---

> 本文为原创内容，首发于**鲲鹏AI探索局**。  
> 转载请注明出处：https://kunpeng-ai.com/blog/openclaw-getting-started
