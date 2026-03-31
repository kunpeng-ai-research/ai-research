# OpenClaw 完整入门指南：打造你的专属AI助手

> 作者：鲲鹏AI探索局  
> 原创首发于：https://kunpeng-ai.com/blog/openclaw-getting-started

---

## 一、什么是OpenClaw？

你是否厌倦了ChatGPT的月费、Claude的配额限制，以及各种云端AI的数据隐私担忧？

**OpenClaw给你一个全新的选择：完全自托管的AI网关。**

简单说，OpenClaw是一个"翻译官"：
```
你的聊天App（微信/Telegram/Discord/飞书）
        ↓
    OpenClaw网关
        ↓
    AI模型（GPT-4/Claude/Ollama）
```

**核心优势**：
- ✅ **数据100%自控** - 不泄露给任何第三方
- ✅ **支持20+平台** - 一个助手 everywhere
- ✅ **支持国产模型** - Ollama本地部署，0成本
- ✅ **一次部署，永久使用** - 无月费
- ✅ **完全可定制** - 自由扩展

---

## 二、中国用户特别注意

### ⚠️ 网络环境问题

**GitHub下载慢？** 使用国内镜像：
```bash
# npm淘宝镜像
https://registry.npmmirror.com/

# Node.js下载
https://npmmirror.com/mirrors/node/
```

**OpenClaw安装脚本失败？** 手动下载：
```powershell
iwr -useb https://openclaw.ai/install.ps1 -OutFile install.ps1
.\install.ps1
```

### 🖥️ Windows安装方案

| 方案 | 难度 | 推荐度 | 说明 |
|------|------|--------|------|
| **WSL2** | ⭐⭐ | ⭐⭐⭐⭐⭐ | 最稳定，社区支持好 |
| **Windows原生** | ⭐⭐⭐ | ⭐⭐⭐⭐ | 直接，但权限问题多 |
| **Docker** | ⭐⭐ | ⭐⭐⭐⭐ | 隔离性好，需Docker基础 |

**推荐**: Win10/11用户优先选WSL2

### 🔐 权限问题解决

**PowerShell执行策略**:
```powershell
# 查看当前策略
Get-ExecutionPolicy

# 临时允许（当前会话）
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 永久修改（管理员权限）
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

**管理员权限**: 右键PowerShell → "以管理员身份运行"

---

## 三、5分钟快速安装（WSL2方案）

### 第1步：安装WSL2

```powershell
# 管理员PowerShell运行
wsl --install
```

然后在Microsoft Store安装Ubuntu，启动后设置用户名和密码。

### 第2步：配置Node.js

```bash
# 在WSL2 Ubuntu终端中
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash
source ~/.bashrc
nvm install 24
nvm use 24
```

### 第3步：安装OpenClaw

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

脚本会自动完成所有配置。

### 第4步：配置AI模型

```bash
openclaw onboard --install-daemon
```

**新手推荐配置**：
- AI Provider: **Ollama（本地）** - 0成本，无网络限制
- 或 **OpenAI** - 质量高，需API key（$5-10/月）

**Ollama配置**:
```bash
# WSL2内安装Ollama
curl -fsSL https://ollama.com/install.sh | sh
ollama pull llama3.2:3b  # 下载模型
```

OpenClaw配置选择"Local (Ollama)"，Base URL: `http://localhost:11434`

---

## 四、连接飞书（国内重点）

飞书是国内最常用的办公平台，OpenClaw支持完整的飞书集成。

### 1. 创建飞书应用

访问 https://open.feishu.cn/app
- 创建应用 → 自建应用
- 填写名称（如"OpenClaw助手"）
- 上传图标

### 2. 配置权限

**权限管理** → 添加：
- `im:message` - 收发消息
- `im:chat` - 获取群组信息

**订阅事件** → 添加：
- `im.message.receive_v1` - 接收消息

### 3. 获取App ID和App Secret

应用首页 → 复制App ID和App Secret

### 4. OpenClaw配置

```bash
# 安装飞书插件（首次）
openclaw plugins install feishu

# 编辑配置
openclaw config edit
```

添加：
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

重启：`openclaw restart`

### 5. 配置Webhook

```bash
openclaw urls
```

复制Feishu event URL，回到飞书开发者后台：
- 事件订阅 → 添加订阅
- URL粘贴，保存并启用

### 6. 安装机器人

机器人 → 添加机器人 → 自定义 → 安装到全员/指定部门

### 7. 测试

在飞书中@机器人发送消息，应收到AI回复！

---

## 五、常见错误解决方案

### 错误1：安装脚本下载失败

```bash
# 方案1: 跳过SSL验证（临时）
curl -k https://openclaw.ai/install.sh | bash

# 方案2: 手动下载
iwr -useb https://openclaw.ai/install.ps1 -OutFile install.ps1
.\install.ps1
```

### 错误2：Node.js版本不对

```bash
nvm install 24
nvm use 24
```

### 错误3：权限不足

- WSL2: 确保在普通用户下（非root）
- Windows: 以管理员身份运行

### 错误4：端口8080被占用

```bash
# 查找占用进程
netstat -ano | findstr :8080

# 修改OpenClaw端口
openclaw config edit
# 修改 "gateway.port": 8081
```

### 错误5：onboarding卡住

```bash
# 查看日志
openclaw logs --follow

# 重置onboarding
openclaw onboard --reset
```

---

## 六、配置文件详解

配置文件：`~/.openclaw/config.json`

### 核心配置示例

```json5
{
  "gateway": {
    "port": 8080,
    "host": "0.0.0.0",
    "logLevel": "info"
  },

  "agent": {
    "name": "小鲲",
    "avatar": "https://example.com/avatar.png",
    "systemPrompt": "你是鲲鹏AI探索局的助手，专注于AI技术解答。"
  },

  "models": {
    "default": {
      "provider": "ollama",
      "model": "llama3.2:3b",
      "baseUrl": "http://localhost:11434"
    }
  },

  "plugins": {
    "telegram": {
      "botToken": "你的Token"
    },
    "feishu": {
      "appId": "你的App ID",
      "appSecret": "你的App Secret"
    }
  }
}
```

---

## 七、常用命令

```bash
openclaw status              # 查看状态
openclaw logs                # 查看日志
openclaw restart             # 重启
openclaw config edit         # 编辑配置
openclaw config validate     # 验证配置
openclaw plugins list        # 插件列表
openclaw urls                # 查看Webhook URLs
openclaw doctor              # 健康检查
openclaw update              # 更新
```

---

## 八、FAQ（10个常见问题）

**Q: 数据安全吗？**  
A: OpenClaw运行在你自己的设备，数据存储在 `~/.openclaw/`，完全可控。用本地Ollama模型，数据完全不外传。

**Q: 消息延迟高？**  
A: 可能原因：AI provider响应慢、网络延迟、消息太长。查看日志定位：`openclaw logs`

**Q: 可以连微信吗？**  
A: 微信官方不支持Bot API。可以通过第三方方案（如微信网页版）或使用Telegram/飞书替代。

**Q: 支持哪些国产模型？**  
A: 通过Ollama支持：llama3.2、qwen、chatglm等（需Ollama支持）。也支持通过API接入国内云厂商（百度、阿里、腾讯）。

**Q: 如何备份？**  
A: 复制整个 `~/.openclaw/` 目录即可。

**Q: 可以24小时在线吗？**  
A: 可以！安装为系统服务（`--install-daemon`），开机自启，持续运行。

**Q: 有移动端App吗？**  
A: OpenClaw本身是服务端，但你可以通过任何聊天App（Telegram、飞书、Discord）使用它，相当于跨平台移动助手。

**Q: 免费吗？**  
A: OpenClaw软件免费（MIT协议）。如果用本地Ollama，0成本。如果用OpenAI等，需支付API费用（按使用量）。

**Q: 适合企业用吗？**  
A: 非常适合！数据自控、可内网部署、支持LDAP/SSO（需自定义开发）。推荐Docker或K8s部署。

**Q: 遇到问题怎么办？**  
A: 1. 查看日志 `openclaw logs` 2. 官方文档 https://docs.openclaw.ai 3. Discord社区 https://discord.gg/clawd

---

## 九、下一步

恭喜！你已经完成了OpenClaw的基本设置。现在可以：

1. **探索插件系统**：浏览器自动化、文件操作、数据库查询
2. **学习自动化**：Cron Jobs定时任务
3. **开发自定义技能**：用TypeScript写自己的工具
4. **生产部署**：Nginx反代、HTTPS、系统服务

---

## 十、总结

OpenClaw给你一个**完全可控、多平台统一**的AI助手。

**5分钟安装，无限可能。** 🚀

---

**完整教程（持续更新）**:  
https://kunpeng-ai.com/blog/openclaw-getting-started

**官方文档**: https://docs.openclaw.ai  
**GitHub**: https://github.com/openclaw/openclaw  
**Discord**: https://discord.gg/clawd

---

> 本文为原创内容，首发于**鲲鹏AI探索局**。  
> 转载请注明出处：https://kunpeng-ai.com/blog/openclaw-getting-started
