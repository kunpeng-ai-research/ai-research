# OpenClaw完整入门指南：中国用户必看

## 一句话总结
OpenClaw是一个自托管AI网关，让你在微信、Telegram、Discord、飞书等任意聊天App中使用AI，数据完全由自己控制，特别适合注重隐私的国内用户。

---

## 什么是OpenClaw？

OpenClaw是**自托管AI网关**，连接你的聊天软件（微信/Telegram/Discord/飞书）和AI模型（GPT-4/Claude/Ollama）。

**核心价值**：
- ✅ 数据100%自控，不泄露给第三方
- ✅ 支持20+平台（含飞书、Telegram、Discord）
- ✅ 支持国产大模型（Ollama本地部署）
- ✅ 一次部署，永久使用
- ✅ 无月费，只付API成本（或本地0成本）

**适合谁**：
- 注重隐私的开发者
- 需要多平台统一AI助手的用户
- 想摆脱月费订阅制的技术爱好者
- 企业内网部署（数据不出内网）

---

## 中国用户特别注意⚠️

### 1. 网络环境问题

**问题**: GitHub下载慢、npm镜像超时

**解决方案**:
```bash
# 配置淘宝npm镜像（在~/.npmrc添加）
registry=https://registry.npmmirror.com/

# 安装Node.js（使用官方镜像站）
# 下载地址: https://npmmirror.com/mirrors/node/
```

**OpenClaw安装脚本下载失败**:
```powershell
# 手动下载并安装
iwr -useb https://openclaw.ai/install.ps1 -OutFile install.ps1
.\install.ps1
```

### 2. AI Provider选择

| Provider | 是否需要代理 | 成本 | 推荐度 |
|---------|------------|------|--------|
| OpenAI | ✅ 需要 | 按token | ⭐⭐⭐⭐ |
| Anthropic | ✅ 需要 | 按token | ⭐⭐⭐⭐ |
| Ollama（本地） | ❌ 不需要 | 0（硬件成本） | ⭐⭐⭐⭐⭐ |
| 国内API | ❌ 不需要 | 按token | ⭐⭐⭐ |

**推荐方案**: Ollama本地模型 + OpenAI API fallback

### 3. Windows权限问题

**PowerShell执行策略**:
```powershell
# 查看当前执行策略
Get-ExecutionPolicy

# 临时允许脚本执行（当前会话）
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 永久修改（需管理员）
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**管理员权限**:
- 右键PowerShell → "以管理员身份运行"
- 或在命令行中使用 `Start-Process powershell -Verb RunAs`

### 4. 系统选择建议

| 方案 | 难度 | 性能 | 推荐度 |
|------|------|------|--------|
| WSL2（推荐） | ⭐⭐ | 优秀 | ⭐⭐⭐⭐⭐ |
| Windows原生 | ⭐⭐⭐ | 良好 | ⭐⭐⭐⭐ |
| Docker | ⭐⭐ | 优秀 | ⭐⭐⭐⭐ |
| macOS/Linux | ⭐ | 优秀 | ⭐⭐⭐⭐⭐ |

**Win10/11用户**: 优先选WSL2，稳定性最好

---

## 详细安装步骤（Windows WSL2方案）

### 第1步：安装WSL2

1. **打开PowerShell（管理员）**:
   ```
   wsl --install
   ```

2. **安装Ubuntu**（Microsoft Store搜索"Ubuntu"）

3. **启动WSL2**，设置用户名和密码

4. **更新系统**:
   ```bash
   sudo apt update && sudo apt upgrade -y
   ```

### 第2步：配置Node.js环境

```bash
# 使用nvm安装Node.js 24.x
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 24
nvm use 24
```

### 第3步：安装OpenClaw

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

脚本会自动：
- 检测系统
- 安装Node.js（如果缺失）
- 安装OpenClaw CLI
- 运行onboarding向导

### 第4步：配置AI模型

运行向导：
```bash
openclaw onboard --install-daemon
```

**选择Provider**:
- 新手推荐: OpenAI（需API key）
- 国内用户推荐: Ollama（本地模型，0成本）

**Ollama配置示例**:
```bash
# 先安装Ollama（WSL2内）
curl -fsSL https://ollama.com/install.sh | sh

# 运行Ollama服务
ollama serve &

# 下载模型
ollama pull llama3.2:3b

# OpenClaw配置选择"Local (Ollama)"
# Base URL: http://localhost:11434
# Model: llama3.2:3b
```

---

## 常见错误解决方案

### 错误1：安装脚本下载失败

**现象**: `curl: (60) SSL certificate problem`

**解决**:
```bash
# 临时跳过SSL验证（不安全但可用）
curl -k https://openclaw.ai/install.sh | bash

# 或下载离线包手动安装
iwr -useb https://openclaw.ai/install.ps1 -OutFile install.ps1
.\install.ps1
```

### 错误2：Node.js版本不兼容

**现象**: `Error: Node.js version 20.x is not supported`

**解决**:
```bash
# 使用nvm切换版本
nvm install 24
nvm use 24
```

### 错误3：权限不足

**现象**: `Permission denied` 或 `Access is denied`

**解决**:
- **WSL2**: 确保在Ubuntu用户下（非root）
- **Windows原生**: 以管理员身份运行PowerShell
- 修改执行策略（见上文）

### 错误4：端口8080被占用

**现象**: `Error: listen EADDRINUSE: :::8080`

**解决**:
```bash
# 查找占用端口的进程
netstat -ano | findstr :8080

# 方案1：停止占用进程
taskkill /PID <PID> /F

# 方案2：修改OpenClaw配置（推荐）
openclaw config edit
# 修改 "gateway": { "port": 8081 }
```

### 错误5：onboarding卡住/失败

**现象**: 输入API key后无响应

**解决**:
1. 查看日志:
   ```bash
   openclaw logs --follow
   ```

2. 常见原因:
   - API key无效（检查是否过期）
   - 网络超时（代理问题）
   - `.env`文件权限不足

3. 重试onboarding:
   ```bash
   openclaw onboard --reset
   ```

---

## 连接飞书（国内重点）

飞书是国内最常用的办公平台，OpenClaw对接飞书需要配置Webhook。

### 步骤1：创建飞书应用

1. 访问 [飞书开发者后台](https://open.feishu.cn/app)
2. 点击"创建应用" → "自建应用"
3. 填写应用名称（如"OpenClaw助手"）
4. 上传图标（可选）

### 步骤2：配置权限

**权限管理** → 添加权限：
- `im:message`（接收和发送消息）
- `im:chat`（获取群组信息）

**订阅事件** → 添加事件订阅：
- `im.message.receive_v1`（接收消息事件）

### 步骤3：获取App ID和App Secret

**应用首页** → 复制：
- **App ID**
- **App Secret**

### 步骤4：配置OpenClaw

```bash
# 先安装飞书插件（如果未安装）
openclaw plugins install feishu

# 编辑配置
openclaw config edit
```

在 `plugins` 部分添加：

```json5
{
  "plugins": {
    "feishu": {
      "appId": "你的App ID",
      "appSecret": "你的App Secret",
      // 可选：加密密钥（提高安全性）
      // "encryptionKey": "your-encryption-key"
    }
  }
}
```

保存并重启：
```bash
openclaw restart
```

### 步骤5：获取Webhook URL

```bash
openclaw urls
```

输出示例：
```
Feishu event URL: https://your-domain.com/api/plugins/feishu/events
```

复制该URL，回到飞书开发者后台。

### 步骤6：配置事件订阅

**事件订阅** → 添加订阅：
- 选择事件类型: `im.message.receive_v1`
- Request URL: 粘贴上一步的URL
- 点击"保存并启用"

**重要**: 如果URL验证失败，请确保：
1. 域名已解析到服务器IP
2. Nginx反向代理配置正确（见下文）
3. HTTPS证书有效（飞书要求HTTPS）

### 步骤7：安装机器人

**机器人** → 添加机器人 → 选择"自定义"
- 复制机器人 `App ID` 和 `App Secret`（与步骤3相同）
- 点击"安装到" → 选择"全员"或指定部门/群组

### 步骤8：测试

在飞书中打开任意聊天窗口（或群组），@你的机器人发送消息：

```
你好，你是谁？
```

应该收到AI回复！

---

## 故障排查（飞书专用）

### 问题1：消息收不到

**排查步骤**:
1. 检查网关状态: `openclaw status`
2. 查看飞书事件订阅日志（开发者后台）
3. 查看OpenClaw日志: `openclaw logs | grep feishu`

**常见原因**:
- 事件订阅URL错误
- 机器人未安装到当前聊天
- 权限不足（检查 `im:message` 权限）

### 问题2：Webhook验证失败

**原因**: 飞书要求HTTPS且证书有效

**解决**:
- 确保域名已备案（国内必须）
- 使用Let's Encrypt免费证书
- Nginx配置SSL（见生产部署章节）

### 问题3：回复消息失败（403/401）

**原因**: App ID或App Secret错误

**解决**:
- 重新复制App ID和App Secret（从应用首页）
- 确保机器人已安装

---

## 配置文件详解

OpenClaw的配置文件位于 `~/.openclaw/config.json`（Windows WSL2: `/home/你的用户名/.openclaw/config.json`）

### 完整配置结构（带注释）

```json5
{
  // ==================== 网关配置 ====================
  "gateway": {
    "port": 8080,           // 网关监听端口
    "host": "0.0.0.0",      // 监听地址（0.0.0.0表示所有IP）
    "logLevel": "info"      // 日志级别: error/warn/info/debug
  },

  // ==================== AI助手身份 ====================
  "agent": {
    "name": "小鲲",          // 助手显示名称
    "avatar": "https://example.com/avatar.png",  // 头像URL
    "systemPrompt": "你是鲲鹏AI探索局的助手，专注于AI技术解答。", // 系统提示词
    "defaultModel": "gpt-4o"  // 默认模型（可选）
  },

  // ==================== AI模型配置 ====================
  "models": {
    "default": {
      "provider": "openai",   // provider: openai/anthropic/ollama/google
      "model": "gpt-4o",      // 模型名称
      "apiKey": "sk-xxx",     // API key（实际存储在.env）
      "baseUrl": "https://api.openai.com/v1",  // API地址
      "maxTokens": 4096,      // 最大token数
      "temperature": 0.7      // 温度参数（0-2）
    },

    // fallback模型（当default失败时使用）
    "fallback": {
      "provider": "ollama",
      "model": "llama3.2:3b",
      "baseUrl": "http://localhost:11434"
    }
  },

  // ==================== 插件配置 ====================
  "plugins": {
    "telegram": {
      "botToken": "123456:ABC-DEF...",
      "allowedChats": []  // 限制可交互的用户ID（空表示所有）
    },

    "discord": {
      "token": "你的Discord Bot Token",
      "clientId": "你的Application ID",
      "allowedChannels": []  // 限制频道ID
    },

    "feishu": {
      "appId": "你的App ID",
      "appSecret": "你的App Secret",
      "encryptionKey": "可选加密密钥"
    }
  },

  // ==================== 渠道差异化配置 ====================
  "channels": {
    "telegram": {
      "agent": {
        "name": "TG助手",
        "systemPrompt": "在Telegram上，回答要简短，适合手机阅读，最多3句话。"
      }
    },

    "discord": {
      "agent": {
        "name": "Discord Bot",
        "systemPrompt": "在Discord服务器，可以活泼点，适当使用emoji。"
      }
    },

    "feishu": {
      "agent": {
        "name": "飞书助手",
        "systemPrompt": "在飞书工作场景，回答保持专业、简洁。"
      }
    }
  },

  // ==================== 高级配置 ====================
  "cache": {
    "enabled": true,      // 启用缓存
    "ttl": 3600,          // 缓存时间（秒）
    "maxSize": 1000       // 最大缓存条目
  },

  "logging": {
    "file": "~/.openclaw/logs/gateway.log",  // 日志文件路径
    "maxSize": "10m",     // 最大文件大小
    "maxFiles": 5         // 保留日志文件数
  }
}
```

---

## 常用命令速查

```bash
# 查看状态
openclaw status

# 查看实时日志
openclaw logs --follow

# 查看错误日志
openclaw logs --level error

# 重启网关
openclaw restart

# 编辑配置
openclaw config edit

# 验证配置语法
openclaw config validate

# 查看已安装插件
openclaw plugins list

# 安装插件
openclaw plugins install feishu

# 卸载插件
openclaw plugins uninstall <插件名>

# 直接向AI发送测试消息
openclaw agent --message "测试消息"

# 更新OpenClaw
openclaw update

# 健康检查
openclaw doctor

# 查看Webhook URLs（用于飞书等）
openclaw urls
```

---

## 生产环境部署（可选）

### Nginx反向代理配置

编辑 `/etc/nginx/sites-available/openclaw`（Linux）或C:\nginx\conf\nginx.conf（Windows）：

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 你的域名

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

**HTTPS配置（飞书要求）**:
```bash
# 使用Certbot获取免费证书
sudo certbot --nginx -d your-domain.com
```

### 系统服务管理

**Linux (systemctl)**:
```bash
sudo systemctl start openclaw-gateway
sudo systemctl enable openclaw-gateway  # 开机自启
sudo systemctl status openclaw-gateway
sudo journalctl -u openclaw-gateway -f   # 查看日志
```

**Windows (Service)**:
```powershell
# 启动服务
Start-Service OpenClawGateway

# 设置为自动启动
Set-Service OpenClawGateway -StartupType Automatic

# 查看状态
Get-Service OpenClawGateway
```

### 自动备份脚本

创建 `~/backup-openclaw.sh`:
```bash
#!/bin/bash
BACKUP_DIR="/backup/openclaw"
DATE=$(date +%Y%m%d_%H%M%S)
tar -czf $BACKUP_DIR/openclaw-$DATE.tar.gz ~/.openclaw/
# 保留最近7天备份
find $BACKUP_DIR -name "openclaw-*.tar.gz" -mtime +7 -delete
```

添加到crontab（每天凌晨2点备份）:
```
0 2 * * * /home/yourname/backup-openclaw.sh
```

---

## FAQ精选（15个常见问题）

### 安装问题

**Q1: Windows用WSL2还是原生安装？**

A: 推荐WSL2，理由：
- ✅ 稳定性更好（官方推荐）
- ✅ 兼容Linux生态（Docker、Shell脚本）
- ✅ 性能损耗小
- ✅ 社区支持好

原生安装也可以，但遇到问题解决起来麻烦。

**Q2: Node.js版本不对怎么办？**

A: 使用nvm（WSL2）或nvm-windows（原生）切换版本：
```bash
nvm install 24
nvm use 24
```

**Q3: 安装脚本卡住不动？**

A: 可能是网络问题。查看日志：
```bash
openclaw logs --follow
```
常见原因：
- API key无效（检查格式）
- 网络超时（设置代理或重试）
- 防火墙阻止（关闭防火墙测试）

### 配置问题

**Q4: 配置文件格式错误怎么办？**

A: 使用验证命令：
```bash
openclaw config validate
```
或在线JSON校验工具：https://jsonlint.com/

**Q5: 如何修改助手名称和头像？**

A: 编辑 `config.json`:
```json5
{
  "agent": {
    "name": "小鲲",
    "avatar": "https://你的域名/avatar.png"
  }
}
```
重启生效：`openclaw restart`

**Q6: 不同平台可以用不同身份吗？**

A: 可以！在 `channels` 中配置：
```json5
{
  "channels": {
    "telegram": {
      "agent": { "name": "TG助手" }
    },
    "feishu": {
      "agent": { "name": "飞书助手" }
    }
  }
}
```

### 使用问题

**Q7: 消息延迟高怎么办？**

A: 排查步骤：
1. 检查AI provider状态（OpenAI高峰期慢）
2. ping测试网络延迟: `ping api.openai.com`
3. 查看日志: `openclaw logs | grep latency`
4. 优化：使用更快的模型或本地Ollama

**Q8: 可以用哪些本地模型？**

A: Ollama支持的模型列表：https://ollama.com/library
推荐：
- `llama3.2:3b` - 轻量，速度快
- `mistral` - 平衡性能和质量
- `codellama:7b` - 代码专用

**Q9: 消息历史会保存吗？**

A: OpenClaw本身不保存历史（Stateless），历史由各平台管理（Telegram Cloud、Discord等）。如需长期存储，需自行实现或使用RAG插件。

**Q10: 可以同时连接多个平台吗？**

A: 可以！这是OpenClaw的核心功能。配置多个插件（telegram、discord、feishu等），同一个AI助手同时服务所有平台。

### 故障问题

**Q11: 收不到消息？**

A: 检查清单：
- [ ] `openclaw status` 确认网关运行
- [ ] 平台Bot是否在线（Telegram:@BotFather → /mybots）
- [ ] 配置文件是否正确（`openclaw config validate`）
- [ ] 防火墙是否放行端口（80/443或8080）
- [ ] 日志错误: `openclaw logs`

**Q12: 提示401/403错误？**

A: API key错误或权限不足：
- OpenAI: 检查 `sk-` 开头的key是否正确
- Telegram: Bot Token是否复制完整
- 飞书: App ID/Secret是否正确

**Q13: Gateway启动失败？**

A: 常见原因：
- 端口被占用: 修改 `gateway.port`
- 权限不足: 管理员运行或修改文件权限
- 配置错误: `openclaw config validate` 检查

**Q14: 如何查看详细日志？**

A:
```bash
# 实时日志（调试模式）
openclaw logs --follow --level debug

# 查看错误日志
openclaw logs --level error

# 查看最近100行
openclaw logs --tail 100
```

**Q15: 数据安全吗？会不会泄露？**

A:
- ✅ 数据存储在你自己设备（`~/.openclaw/`）
- ✅ 可以选择本地模型（Ollama），数据完全不外传
- ✅ 如果使用OpenAI等云端，数据按provider政策处理
- ✅ 建议: 敏感数据用本地模型，非敏感用云端API

---

## 资源与支持

### 官方资源

| 资源 | 链接 | 说明 |
|------|------|------|
| 官方文档 | https://docs.openclaw.ai | 最权威 |
| GitHub仓库 | https://github.com/openclaw/openclaw | 源码、Issues |
| Discord社区 | https://discord.gg/clawd | 活跃社区，快速答疑 |
| 安装脚本 | https://openclaw.ai/install.sh | 一键安装 |
| 支持的平台 | https://docs.openclaw.ai/channels/index | 20+平台列表 |
| 自动化指南 | https://docs.openclaw.ai/automation/cron-jobs | Cron、Heartbeat |

### 国内镜像

- npm镜像: https://registry.npmmirror.com/
- Node.js下载: https://npmmirror.com/mirrors/node/
- Ollama下载: https://ollama.com/download (有国内镜像)

### 视频教程

- YouTube: [OpenClaw完整设置教程](https://www.youtube.com/watch?v=SaWSPZoPX34) (28分钟)
- B站: 搜索"OpenClaw入门"（待更新）

### 问题反馈

**提交Issue**（GitHub）:
1. 访问 https://github.com/openclaw/openclaw/issues
2. 搜索是否已有相同问题
3. 提供详细信息：
   - OpenClaw版本 (`openclaw --version`)
   - 操作系统
   - 错误日志（`openclaw logs`）
   - 复现步骤

**Discord社区**（推荐）:
- 更快的响应速度
- 可以贴代码、截图
- 社区互助

### 贡献指南

OpenClaw是开源项目（MIT协议），欢迎贡献：
- 🐛 提交Bug报告
- 💡 提出新功能建议
- 📝 改进文档
- 🔧 提交PR修复代码
- 🌐 翻译文档（中文社区需要）

---

## 总结

OpenClaw给你一个**完全可控的AI助手**，特别适合：
- ✅ 注重隐私的中国用户
- ✅ 需要多平台统一体验的开发者
- ✅ 想摆脱月费订阅制的技术爱好者
- ✅ 企业内网部署（数据不出内网）

**安装真的只需5分钟**（WSL2用户），但本教程提供了详细的故障排查，确保你遇到问题时能找到解决方案。

现在就开始吧！🚀

---

**完整版博客**（含最新更新）:  
https://kunpeng-ai.com/blog/openclaw-getting-started

**反馈**: 欢迎在博客评论区或Discord社区留言！

---

*本文首发于鲲鹏AI探索局，转载请注明出处。*  
*最后更新: 2026-03-31*
