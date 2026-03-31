# OpenClaw入门到实战：自托管AI网关完整部署指南

> 作者：鲲鹏AI探索局 | 标签：OpenClaw, AI Agent, 自托管, 多平台聊天, 网关部署

## 摘要

本文详细介绍OpenClaw——一个开源自托管AI网关的安装、配置和实战部署全过程。通过实际案例演示如何连接Telegram、Discord、飞书等20+聊天平台，实现数据完全可控的AI助手。特别针对中国用户的Windows环境、网络问题、飞书接入提供详细解决方案。

**关键词**：OpenClaw, AI网关, 自托管, 多平台集成, 隐私保护, 飞书机器人, Windows部署, Ollama

---

## 一、OpenClaw技术架构深度解析

### 1.1 OpenClaw核心设计

OpenClaw是一个**插件化AI网关**，采用Node.js + TypeScript开发，核心架构分为三层：

```
┌─────────────────────────────────────┐
│        Chat Platforms Layer         │
│  (Telegram, Discord, Feishu, ...)   │
└───────────────┬─────────────────────┘
                │ HTTP/Webhook
┌───────────────▼─────────────────────┐
│         OpenClaw Gateway            │
│  ┌────────────┐  ┌──────────────┐  │
│  │   Router   │  │   Plugins    │  │
│  └────────────┘  └──────────────┘  │
└───────────────┬─────────────────────┘
                │ Provider API
┌───────────────▼─────────────────────┐
│      AI Providers Layer             │
│  (OpenAI, Anthropic, Ollama, ...)   │
└─────────────────────────────────────┘
```

**核心组件**:
- **Gateway**: 主服务进程，监听HTTP端口（默认8080）
- **Router**: 消息路由，根据配置分发到不同AI模型
- **Plugins**: 平台适配器（Telegram、Discord、Feishu等）
- **Models**: AI模型抽象层，统一接口

### 1.2 技术栈

- **运行时**: Node.js 24.x (22.14+ supported)
- **语言**: TypeScript
- **通信协议**: HTTP + Webhook + Bot APIs
- **配置格式**: JSON5（支持注释）
- **插件系统**: 动态加载，热重载

### 1.3 应用场景

| 场景 | 说明 | 推荐配置 |
|------|------|---------|
| 个人AI助手 | 通过Telegram/Discord/飞书与AI对话 | 云端API + 本地缓存 |
| 企业内网 | 数据不出内网，合规要求 | Ollama本地模型 |
| 24小时客服 | 自动回复常见问题 | 固定prompt + 知识库 |
| IoT智能体 | 树莓派部署，控制智能家居 | 轻量模型 + 自定义技能 |

---

## 二、环境搭建与安装实战

### 2.1 系统要求

| 组件 | 最低配置 | 推荐配置 | 说明 |
|------|---------|---------|------|
| OS | Win10/WSL2 | Ubuntu 22.04+ | WSL2性能最佳 |
| Node.js | 22.14+ | 24.x | 官方推荐 |
| RAM | 2GB | 4GB+ | Ollama需更多 |
| Disk | 1GB | 5GB+ | 含模型文件 |
| Network | 可访问AI API | 低延迟 | 本地模型不需要 |

### 2.2 安装方案对比（Windows用户重点）

#### 方案对比表

| 方案 | 安装难度 | 运行性能 | 稳定性 | 推荐指数 | 适用人群 |
|------|---------|---------|--------|---------|---------|
| **WSL2** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 所有Win10/11用户 |
| **Windows原生** | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | 不想用WSL的进阶用户 |
| **Docker** | ⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | 已有Docker环境 |
| **macOS/Linux** | ⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | 非Windows用户 |

**结论**: Win10/11用户无脑选WSL2

### 2.3 WSL2安装详细步骤

#### Step 1: 启用WSL2

以**管理员**打开PowerShell：

```powershell
# 启用WSL功能
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# 启用虚拟机功能
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 重启计算机
Restart-Computer
```

#### Step 2: 安装WSL2内核更新包

访问 https://aka.ms/wsl2update 下载并安装。

#### Step 3: 设置WSL2为默认版本

```powershell
wsl --set-default-version 2
```

#### Step 4: 安装Ubuntu

打开Microsoft Store，搜索"Ubuntu"，点击"安装"（推荐Ubuntu 22.04 LTS）。

首次启动Ubuntu，设置用户名和密码（与Windows账户无关）。

#### Step 5: 更新Ubuntu系统

在Ubuntu终端中：

```bash
sudo apt update && sudo apt upgrade -y
sudo apt install -y curl git
```

#### Step 6: 配置Node.js（使用nvm）

```bash
# 安装nvm
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# 加载nvm
source ~/.bashrc

# 安装Node.js 24
nvm install 24
nvm use 24
nvm alias default 24

# 验证
node --version  # 应显示 v24.x
npm --version
```

#### Step 7: 安装OpenClaw

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

安装脚本会自动：
1. 检测系统环境
2. 安装OpenClaw CLI（如果npm未安装会先安装）
3. 运行 `openclaw onboard` 交互式配置
4. 可选安装为系统服务

#### Step 8: 验证安装

```bash
openclaw --version
# 输出: OpenClaw 2026.3.24

openclaw status
# 应显示 Gateway: running
```

---

## 三、配置AI模型（关键决策）

### 3.1 AI Provider选择指南

| Provider | 是否需要代理 | 成本 | 响应速度 | 质量 | 推荐场景 |
|---------|------------|------|---------|------|---------|
| **OpenAI** | ✅ 需要 | 按token | 快 | ⭐⭐⭐⭐⭐ | 高质量对话、代码 |
| **Anthropic** | ✅ 需要 | 按token | 中 | ⭐⭐⭐⭐⭐ | 长文本、安全性 |
| **Ollama** | ❌ 不需要 | 0（硬件） | 取决于配置 | ⭐⭐⭐⭐ | 国内用户、隐私优先 |
| **Google Gemini** | ✅ 需要 | 按token | 快 | ⭐⭐⭐⭐ | 多模态（图像） |
| **Azure OpenAI** | ✅ 需要 | 按token | 快 | ⭐⭐⭐⭐⭐ | 企业Azure环境 |

**中国用户推荐组合**:
- **主模型**: Ollama `llama3.2:3b`（轻量，速度快）
- **备用模型**: OpenAI `gpt-4o-mini`（质量高，按需使用）

### 3.2 Ollama本地部署（0成本方案）

#### 安装Ollama

在WSL2 Ubuntu中：

```bash
curl -fsSL https://ollama.com/install.sh | sh
```

验证安装：
```bash
ollama --version
# Ollama is running

# 查看服务状态
systemctl status ollama  # 应显示 active (running)
```

#### 下载模型

```bash
# 轻量模型（推荐新手）
ollama pull llama3.2:3b

# 中等模型（质量更好）
ollama pull mistral

# 代码专用
ollama pull codellama:7b
```

#### 测试Ollama

```bash
ollama run llama3.2:3b "你好，请介绍一下你自己"
```

应该收到模型回复。

#### OpenClaw配置Ollama

编辑配置：
```bash
openclaw config edit
```

修改 `models.default`:
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

重启网关：
```bash
openclaw restart
```

### 3.3 OpenAI配置（需API key）

#### 获取API key

1. 访问 https://platform.openai.com/api-keys
2. 登录（可能需要代理）
3. 点击"Create new secret key"
4. 复制key（格式：`sk-...`）

⚠️ **国内提醒**: OpenAI API需要国际信用卡，可通过正规渠道代购（注意风险）

#### OpenClaw配置

```json5
{
  "models": {
    "default": {
      "provider": "openai",
      "model": "gpt-4o-mini",  // 性价比高
      "apiKey": "sk-你的密钥"
    }
  }
}
```

---

## 四、平台连接实战

### 4.1 Telegram（最简单）

#### 1. 创建Bot

- 打开Telegram，搜索 @BotFather
- 发送 `/newbot`
- 输入Bot名称（如 `MyOpenClawBot`）
- 输入用户名（需唯一，如 `my_openclaw_bot`）
- 复制BotFather返回的 **Bot Token**

#### 2. 配置OpenClaw

```bash
openclaw config edit
```

在 `plugins` 添加：
```json5
{
  "plugins": {
    "telegram": {
      "botToken": "你的Bot Token"
    }
  }
}
```

#### 3. 重启并测试

```bash
openclaw restart
```

在Telegram中打开你的Bot，发送：
```
你好
```

收到AI回复即成功！

---

### 4.2 Discord（企业协作）

#### 1. Discord开发者门户配置

访问 https://discord.com/developers/applications

- **New Application** → 输入名称 → Create
- 左侧 **Bot** → Add Bot → Yes, do it!
- 复制 **Token**（类似 `MTk...`）
- **Privileged Gateway Intents** 开启：
  - ✅ Presence Intent
  - ✅ Server Members Intent
  - ✅ Message Content Intent

#### 2. 邀请Bot到服务器

- 左侧 **OAuth2** → URL Generator
- Scopes: 勾选 `bot`
- Bot Permissions: 选择 `Send Messages`, `Read Message History`等（最小权限原则）
- 复制生成的URL，在浏览器打开，选择服务器并授权

#### 3. OpenClaw配置

```json5
{
  "plugins": {
    "discord": {
      "token": "你的Bot Token",
      "clientId": "你的Application ID",
      "allowedChannels": []  // 可选：限制频道ID
    }
  }
}
```

重启后，在Discord中@Bot测试。

---

### 4.3 飞书（国内重点，详细步骤）

#### 前置条件
- 企业飞书账号或个人开发者账号
- 已备案域名（Webhook要求HTTPS）
- 服务器公网IP或内网穿透

#### Step 1: 创建飞书应用

1. 访问 https://open.feishu.cn/app
2. 点击"创建应用" → 选择"自建应用"
3. 填写：
   - 应用名称: `OpenClaw助手`
   - 应用描述: `基于OpenClaw的AI助手`
   - 上传图标（可选）
4. 点击"创建"

#### Step 2: 配置权限

**权限管理** → 添加权限：
```
im:message           # 发送和接收消息
im:chat              # 获取群组信息（可选）
```

**订阅事件** → 添加事件订阅：
```
im.message.receive_v1   # 接收消息事件
```

#### Step 3: 获取凭证

应用首页 → 复制：
- **App ID**（格式：`cli_...`）
- **App Secret**（格式：`...`）

#### Step 4: 安装OpenClaw飞书插件

```bash
openclaw plugins install feishu
```

#### Step 5: 配置OpenClaw

编辑 `~/.openclaw/config.json`:

```json5
{
  "plugins": {
    "feishu": {
      "appId": "cli_xxxxxxxxxxxxx",
      "appSecret": "xxxxxxxxxxxxxxxxxxxx",
      "encryptionKey": "可选：32位随机字符串（提高安全性）"
    }
  }
}
```

保存并重启：
```bash
openclaw restart
```

#### Step 6: 获取Webhook URL

```bash
openclaw urls
```

输出示例：
```
Feishu event URL: https://your-domain.com/api/plugins/feishu/events
```

**重要**: 确保该URL满足：
- ✅ HTTPS（飞书强制要求）
- ✅ 公网可访问（飞书服务器能访问）
- ✅ 域名已备案（国内要求）

#### Step 7: 配置事件订阅

飞书开发者后台：
- **事件订阅** → 添加订阅
- 事件类型: `im.message.receive_v1`
- Request URL: 粘贴上一步的URL
- 点击"保存并启用"

如果验证失败：
1. 检查HTTPS证书是否有效（Let's Encrypt免费证书）
2. 检查Nginx配置是否正确
3. 查看OpenClaw日志: `openclaw logs | grep feishu`

#### Step 8: 安装机器人

- 左侧 **机器人** → 添加机器人
- 选择"自定义"
- 复制机器人App ID和App Secret（与步骤3相同）
- 点击"安装到" → 选择"全员"或指定部门/群组

#### Step 9: 测试

在飞书中：
1. 打开任意聊天窗口（或群组）
2. @你的机器人发送消息
3. 应收到AI回复

**调试技巧**:
```bash
# 查看飞书相关日志
openclaw logs --follow | grep feishu

# 验证Webhook是否收到事件
# 在飞书开发者后台 → 事件订阅 → 查看"最近事件"
```

---

## 五、故障排查全攻略

### 5.1 日志查看与解读

#### 查看实时日志

```bash
# 实时日志（默认info级别）
openclaw logs --follow

# 调试级别（更详细）
openclaw logs --follow --level debug

# 仅查看错误
openclaw logs --level error

# 查看最近N行
openclaw logs --tail 100
```

#### 日志分析示例

```
# 正常请求
[INFO] 2026-03-30T14:20:00.123Z gateway: received message from telegram user 12345
[INFO] 2026-03-30T14:20:00.456Z model: calling openai/gpt-4o (tokens: 150)
[INFO] 2026-03-30T14:20:01.789Z gateway: sent reply to telegram

# 错误示例
[ERROR] 2026-03-30T14:20:00.456Z plugin.feishu: invalid appId or appSecret
[WARN] 2026-03-30T14:20:00.789Z model: rate limit exceeded (429)
```

### 5.2 健康检查

```bash
openclaw doctor
```

输出示例：
```
✔ Node.js: 24.0.0
✔ Gateway: running (port 8080)
✔ Plugins: telegram, discord, feishu
✔ Models: ollama/llama3.2:3b
✗ Ollama: not running (if using local models, start with: ollama serve)
```

### 5.3 常见错误代码

| 错误码 | 含义 | 可能原因 | 解决方案 |
|--------|------|---------|---------|
| 401 | 未授权 | API key错误 | 检查provider的apiKey |
| 403 | 禁止访问 | 权限不足 | 检查Bot权限（Discord）、App权限（飞书） |
| 404 | 未找到 | Webhook URL错误 | `openclaw urls` 检查URL |
| 429 | 限流 | API调用超限 | 降低频率或升级plan |
| 500 | 服务器错误 | OpenClaw内部错误 | 查看日志 `openclaw logs` |
| ECONNREFUSED | 连接拒绝 | AI服务未启动 | 检查Ollama: `ollama serve` |
| EADDRINUSE | 端口占用 | 8080被其他程序占用 | 修改 `gateway.port` 或停止占用进程 |

### 5.4 端口占用排查

```bash
# Windows（管理员PowerShell）
netstat -ano | findstr :8080
# 记录PID，然后:
tasklist | findstr <PID>

# WSL2 Ubuntu
sudo netstat -tulpn | grep :8080
sudo kill -9 <PID>
```

### 5.5 网络诊断

```bash
# 测试到AI provider的网络
ping api.openai.com
curl -I https://api.openai.com/v1/models

# 测试Ollama本地连接
curl http://localhost:11434/api/tags

# 测试端口监听
ss -tlnp | grep 8080  # Linux
netstat -an | findstr 8080  # Windows
```

---

## 六、生产环境部署

### 6.1 Nginx反向代理（必读）

OpenClaw默认监听 `127.0.0.1:8080`，生产环境需Nginx提供公网访问。

#### 安装Nginx

**Ubuntu**:
```bash
sudo apt install nginx
```

**Windows** (WSL2): 同上，或使用Windows原生Nginx

#### 配置站点

编辑 `/etc/nginx/sites-available/openclaw`:

```nginx
server {
    listen 80;
    server_name your-domain.com;  # 你的域名或IP

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_http_version 1.1;
        proxy_set_header Upgrade $http_upgrade;
        proxy_set_header Connection "upgrade";
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
        proxy_read_timeout 300s;
    }
}
```

启用并测试：
```bash
sudo ln -s /etc/nginx/sites-available/openclaw /etc/nginx/sites-enabled/
sudo nginx -t  # 测试配置
sudo systemctl reload nginx
```

#### HTTPS配置（飞书要求）

飞书要求Webhook必须HTTPS。

```bash
# 安装Certbot
sudo apt install certbot python3-certbot-nginx

# 获取免费SSL证书
sudo certbot --nginx -d your-domain.com

# 自动续期测试
sudo certbot renew --dry-run
```

### 6.2 系统服务管理

#### systemctl（Linux）

```bash
# 安装为系统服务（如果onboarding时未安装）
openclaw config set gateway.daemon.enabled true

# 管理服务
sudo systemctl start openclaw-gateway
sudo systemctl enable openclaw-gateway  # 开机自启
sudo systemctl status openclaw-gateway
sudo systemctl restart openclaw-gateway

# 查看日志
sudo journalctl -u openclaw-gateway -f
```

#### Windows Service

```powershell
# 查看服务
Get-Service OpenClawGateway

# 启动
Start-Service OpenClawGateway

# 停止
Stop-Service OpenClawGateway

# 重启
Restart-Service OpenClawGateway

# 设置开机自启
Set-Service OpenClawGateway -StartupType Automatic
```

### 6.3 自动备份策略

#### 备份脚本

创建 `~/backup-openclaw.sh`:

```bash
#!/bin/bash
BACKUP_DIR="/backup/openclaw"
OPENCLAW_DIR="$HOME/.openclaw"
DATE=$(date +%Y%m%d_%H%M%S)

# 创建备份目录
mkdir -p $BACKUP_DIR

# 打包备份
tar -czf $BACKUP_DIR/openclaw-$DATE.tar.gz -C $OPENCLAW_DIR .

# 清理7天前的备份
find $BACKUP_DIR -name "openclaw-*.tar.gz" -mtime +7 -delete

echo "[INFO] Backup completed: openclaw-$DATE.tar.gz"
```

赋予执行权限：
```bash
chmod +x ~/backup-openclaw.sh
```

#### Crontab定时备份

```bash
crontab -e
```

添加（每天凌晨2点执行）:
```
0 2 * * * /home/yourname/backup-openclaw.sh >> /var/log/openclaw-backup.log 2>&1
```

---

## 七、性能优化建议

### 7.1 模型选择策略

| 场景 | 推荐模型 | Token成本 | 速度 | 质量 |
|------|---------|----------|------|------|
| 日常聊天 | gpt-4o-mini / llama3.2:3b | 低 | 快 | 良 |
| 代码生成 | gpt-4o / codellama | 中 | 中 | 优 |
| 复杂分析 | claude-3-5-sonnet | 高 | 慢 | 极优 |
| 离线使用 | llama3.2:3b (Ollama) | 0 | 取决于硬件 | 良 |

### 7.2 缓存配置

减少重复API调用：

```json5
{
  "cache": {
    "enabled": true,
    "ttl": 3600,      // 缓存1小时
    "maxSize": 1000   // 最多1000条
  }
}
```

### 7.3 流式输出

提升用户体验：
```json5
{
  "models": {
    "default": {
      "stream": true  // 启用流式
    }
  }
}
```

---

## 八、监控与告警

### 8.1 日志轮转

配置logrotate（Linux）:
```bash
sudo nano /etc/logrotate.d/openclaw
```

内容：
```
/home/yourname/.openclaw/logs/*.log {
  daily
  rotate 30
  compress
  delaycompress
  missingok
  notifempty
  create 644 yourname yourname
  postrotate
    systemctl restart openclaw-gateway > /dev/null 2>&1 || true
  endscript
}
```

### 8.2 异常告警

结合cron jobs定期检查：
```bash
# 每小时检查网关状态
openclaw cron create --schedule "0 * * * *" \
  --message "检查OpenClaw状态" \
  --to +1234567890
```

---

## 九、进阶功能

### 9.1 多平台差异化身份

不同平台显示不同名称和性格：

```json5
{
  "channels": {
    "telegram": {
      "agent": {
        "name": "TG助手",
        "systemPrompt": "简洁，适合手机阅读，最多3句话。"
      }
    },
    "discord": {
      "agent": {
        "name": "Discord Bot",
        "systemPrompt": "活泼，可以适当使用emoji。"
      }
    },
    "feishu": {
      "agent": {
        "name": "飞书助手",
        "systemPrompt": "专业，适合工作场景。"
      }
    }
  }
}
```

### 9.2 自定义技能开发

技能是OpenClaw的扩展功能，用TypeScript编写。

示例：计算器技能（`~/.openclaw/skills/calculator.ts`）:

```typescript
import { Skill } from 'openclaw';

export default {
  name: 'calculator',
  triggers: ['计算', 'calculate', 'calc'],
  async execute(context) {
    const expr = context.args.join(' ');
    try {
      // ⚠️ 生产环境不要用eval！
      const result = eval(expr);
      return `计算结果: ${result}`;
    } catch (e) {
      return `计算失败: ${e.message}`;
    }
  }
} as Skill;
```

重启OpenClaw后即可使用：@机器人 "计算 12*34"

---

## 十、总结与展望

OpenClaw提供了一个**灵活、可控、可扩展**的AI助手解决方案。

### 核心优势总结

1. **数据主权** - 所有数据在本地，无隐私泄露风险
2. **平台中立** - 20+平台，一次配置，处处可用
3. **模型自由** - 任意provider，随时切换
4. **成本可控** - 无月费，只付API费用（或本地0成本）
5. **开放生态** - 插件化架构，社区可贡献

### 适用场景评估

| 场景 | 是否适合 | 理由 |
|------|---------|------|
| 个人开发者 | ✅ 强烈推荐 | 隐私保护+多平台统一 |
| 技术爱好者 | ✅ 推荐 | 可定制性强，折腾乐趣 |
| 企业内网 | ✅ 推荐 | 数据不出内网，合规 |
| 完全不想折腾的用户 | ❌ 不推荐 | 直接用ChatGPT更省心 |
| 超大并发需求 | ⚠️ 需评估 | 单网关约100+并发，大规模需集群 |

### 未来路线图

根据GitHub Issues，OpenClaw计划：
- 🎯 更多平台（微信原生、钉钉）
- 🎯 多网关集群管理
- 🎯 可视化配置Web UI
- 🎯 技能市场（社区插件商店）
- 🎯 RAG集成（知识库检索）

---

## 参考资料

1. [OpenClaw官方文档](https://docs.openclaw.ai)
2. [GitHub仓库](https://github.com/openclaw/openclaw)
3. [Discord社区](https://discord.gg/clawd)
4. [支持的平台列表](https://docs.openclaw.ai/channels/index)
5. [自动化指南](https://docs.openclaw.ai/automation/cron-jobs)
6. [技能开发](https://docs.openclaw.ai/cli/agent)

---

> **作者**: 鲲鹏AI探索局  
> **转载请注明出处**: https://kunpeng-ai.com/blog/openclaw-getting-started  
> **最后更新**: 2026-03-31  
> **OpenClaw版本**: 2026.3.24
