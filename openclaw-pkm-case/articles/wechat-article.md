# 用OpenClaw构建个人知识管理系统：从零到生产部署的完整实战指南

## 前言

作为一个技术从业者，我每天要处理大量信息：
- 飞书文档中的会议记录
- 技术文章的阅读笔记  
- 项目进展和待办事项
- 技术问题的解决方案

这些知识分散在各个地方，很难系统化管理。试过Notion、Obsidian等工具，但要么需要手动整理，要么缺乏AI能力。

直到我遇到了OpenClaw——这个自托管AI网关让我能够**自动化整个知识管理流程**。

本文是一个完整的实战案例，手把手教你搭建属于你自己的AI驱动PKM系统。

---

## 一、为什么选择OpenClaw做PKM？

### 1.1 PKM的核心需求

一个理想的PKM系统需要：

1. **多源聚合**：能接入各种平台（聊天、文档、邮件）
2. **智能处理**：自动摘要、分类、标签
3. **快速检索**：语义搜索，不是简单的关键字匹配
4. **定期回顾**：自动生成报告，提醒重要内容
5. **数据自主**：所有数据掌握在自己手里

### 1.2 OpenClaw的优势

| 功能 | OpenClaw | 传统方案（Notion/Obsidian） |
|------|----------|---------------------------|
| 多平台接入 | ✅ 20+聊天平台 | ❌ 仅限自有生态 |
| AI处理 | ✅ 内置AI能力 | ❌ 依赖插件/手动 |
| 自动化 | ✅ cron+技能 | ⚠️ 有限 |
| 数据控制 | ✅ 自托管 | ✅ 自托管 |
| 可扩展性 | ✅ 自定义技能 | ❌ 封闭系统 |

**结论**：如果你需要AI自动化，OpenClaw是目前最灵活的选择。

---

## 二、系统架构详解

### 2.1 整体架构图

```
┌─────────────────────────────────────────────────────┐
│                   用户交互层                         │
│  ┌─────────┐  ┌─────────┐  ┌─────────┐           │
│  │ 飞书     │  │Telegram │  │Discord  │ ...      │
│  └────┬────┘  └────┬────┘  └────┬────┘           │
│       │           │           │                  │
│       └───────────┼───────────┘                  │
│                   ▼                              │
│          ┌────────────────┐                     │
│          │  OpenClaw      │                     │
│          │    Gateway     │                     │
│          └───────┬────────┘                     │
│                  │                              │
│    ┌─────────────┼─────────────┐               │
│    ▼             ▼             ▼               │
│  ┌─────┐     ┌─────┐     ┌─────────┐          │
│  │AI   │     │技能 │     │记忆系统  │          │
│  │模型 │     │模块 │     │(向量存储)│          │
│  └─────┘     └─────┘     └─────────┘          │
│                                      │          │
│      ┌──────────────────────────────┼──────────┘
│      ▼                              ▼
│  回复用户 + 自动保存到知识库 + 定时报告
└─────────────────────────────────────────────────────┘
```

### 2.2 核心组件说明

1. **OpenClaw Gateway**
   - 消息路由中心
   - 接收来自各平台的消息
   - 分发到AI模型或技能处理
   - 统一回复格式

2. **AI模型层**
   - OpenAI、Anthropic、Google等云端模型
   - Ollama、LocalAI等本地模型
   - 可根据任务选择不同模型

3. **技能模块**
   - `summarize`：自动生成文档摘要
   - `tagify`：基于内容自动打标签
   - `daily-report`：生成每日知识报告
   - `search`：语义搜索

4. **记忆系统**
   - 存储所有对话和知识
   - 向量化支持语义检索
   - 支持多种后端（SQLite、PostgreSQL、Redis）

5. **定时任务**
   - cron：定时执行技能（如每日报告）
   - heartbeat：健康监控，异常告警

---

## 三、环境搭建

### 3.1 安装OpenClaw

**macOS/Linux**:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows（推荐WSL2）**:

```powershell
# 在WSL2终端中执行
curl -fsSL https://openclaw.ai/install.sh | bash
```

系统要求：
- Node.js 24.x（安装脚本会自动安装）
- 内存 ≥ 4GB
- 磁盘 ≥ 5GB

### 3.2 初始配置

```bash
openclaw onboard --install-daemon
```

配置过程约2分钟：

1. **选择AI Provider**
   - 推荐：Ollama（本地免费，无需API key）
   - 或：OpenAI API（质量更好，需付费）

2. **生成Gateway Token**
   - 这是管理凭证，请妥善保存

3. **安装为系统服务**
   - 勾选 `--install-daemon` 可实现开机自启

4. **验证状态**

```bash
openclaw status
openclaw logs
```

看到 `gateway: running` 表示成功。

---

## 四、连接飞书（知识来源）

飞书作为主要知识入口，用于：
- 保存文档笔记
- 接收每日报告
- 通过@机器人快速交互

### 4.1 安装Feishu插件

```bash
openclaw plugins install feishu
```

### 4.2 配置飞书开发者应用

1. 访问 [飞书开发者后台](https://open.feishu.cn/)
2. 创建应用，获取 `App ID` 和 `App Secret`
3. 启用权限：
   - `im:message`（接收/发送消息）
   - `drive:readonly`（读取文档）
   - `docx:readonly`（读取文档内容）
4. 生成 `Encrypt Key`（事件订阅加密用）
5. 配置事件订阅：
   - URL：运行 `openclaw urls` 获取 `Feishu Event URL`
   - Token：使用 `Event Verification Token`
   - 订阅事件：`im.message.receive_v1`、`docx:readonly`相关事件

⚠️ **重要**：飞书要求URL必须HTTPS且域名已ICP备案！

### 4.3 更新OpenClaw配置

编辑 `~/.openclaw/config.json`：

```json
{
  "plugins": {
    "feishu": {
      "appId": "your_app_id",
      "appSecret": "your_app_secret",
      "encryptKey": "your_encrypt_key",
      "eventVerificationToken": "your_verification_token"
    }
  }
}
```

重启服务：

```bash
openclaw restart
```

---

## 五、记忆系统配置

记忆系统是PKM的核心，负责知识存储和检索。

### 5.1 基础配置

```json
{
  "memory": {
    "enabled": true,
    "provider": "sqlite",
    "maxEntries": 10000,
    "ttlDays": 30,
    "autoSave": true
  }
}
```

**参数说明**：
- `provider`：存储后端（sqlite适合单机，postgres适合多实例）
- `maxEntries`：最大记忆条目数，避免无限增长
- `ttlDays`：自动清理30天前的记忆
- `autoSave`：自动保存所有对话

### 5.2 使用示例

**自动保存**：所有对话都会自动存入记忆

```
用户：OpenClaw的安装步骤是什么？
助手：1. 运行安装脚本... 2. 执行onboarding... [自动保存]
```

**语义搜索**：

```
用户：@PKM助手 搜索OpenClaw安装相关的笔记
助手：找到3条相关记忆：
1. 2026-03-30: OpenClaw完整安装步骤...
2. 2026-04-01: Node.js版本问题...
3. 2026-04-02: WSL2安装问题...
```

---

## 六、自定义技能开发

技能是OpenClaw的扩展机制，可以开发各种自动化功能。

### 6.1 技能目录结构

```
~/.openclaw/
├── skills/
│   ├── summarize.js
│   ├── tagify.js
│   ├── daily-report.js
│   └── search.js
└── config.json
```

### 6.2 技能示例1：自动摘要

**功能**：为文档或对话生成简洁摘要

```javascript
// skills/summarize.js
export const name = 'summarize';
export const description = '自动生成文档摘要';

export async function execute(ctx, args) {
  const { content, maxLength = 100 } = args;
  
  if (!content) {
    return { error: '缺少content参数' };
  }
  
  // 调用AI生成摘要
  const summary = await ctx.agent.generate(
    `用${maxLength}字概括：\n${content}`
  );
  
  // 保存到记忆
  await ctx.memory.remember({
    type: 'summary',
    content: summary,
    source: args.title || 'unknown'
  });
  
  return { summary };
}

export const schema = {
  type: 'object',
  properties: {
    content: { type: 'string' },
    title: { type: 'string' },
    maxLength: { type: 'number' }
  },
  required: ['content']
};
```

**使用方式**：

```
@PKM助手 执行 summarize content="长篇文档内容..."
```

### 6.3 技能示例2：自动标签

**功能**：分析内容并自动打标签

```javascript
// skills/tagify.js
export const name = 'tagify';
export async function execute(ctx, args) {
  const { content } = args;
  
  const prompt = `为以下内容生成3-5个标签（逗号分隔）：\n\n${content}`;
  const tagsText = await ctx.agent.generate(prompt);
  
  const tags = tagsText
    .split(/[,，、\n]/)
    .map(t => t.trim())
    .filter(t => t.length > 0);
    
  return { tags: tags.slice(0, 5) };
}
```

### 6.4 技能示例3：每日报告

**功能**：每天9点自动生成昨日知识总结

```javascript
// skills/daily-report.js
export const name = 'daily-report';

export async function execute(ctx) {
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  
  const memories = await ctx.memory.search('', {
    limit: 50,
    from: yesterday.toISOString()
  });
  
  const stats = `
📊 每日知识报告 (${yesterday.toLocaleDateString('zh-CN')})

📝 新增知识条目: ${memories.length} 条
⏰ 生成时间: ${new Date().toLocaleString('zh-CN')}

📋 最新条目:
${memories.slice(0, 10).map(m => `• ${m.content.substring(0, 50)}...`).join('\n')}
  `.trim();
  
  // 发送到飞书群组
  await ctx.feishu.sendMessage({
    chatId: ctx.config.skills?.dailyReport?.targetChat,
    content: stats
  });
  
  return { success: true, count: memories.length };
}
```

### 6.5 启用技能

在 `config.json` 中注册：

```json
{
  "skills": {
    "enabled": ["summarize", "tagify", "daily-report", "search"],
    "daily-report": {
      "targetChat": "your_feishu_group_chat_id"
    }
  }
}
```

重启服务：

```bash
openclaw restart
```

---

## 七、定时任务与监控

### 7.1 cron定时任务

在 `config.json` 配置：

```json
{
  "cron": {
    "enabled": true,
    "schedule": "0 9 * * *",  // 每天9:00
    "task": "daily-report"
  }
}
```

OpenClaw会自动在指定时间执行对应技能。

### 7.2 heartbeat监控

创建 `HEARTBEAT.md` 定义检查任务：

```markdown
# 每30分钟检查

1. 检查OpenClaw状态：`openclaw status`
2. 检查Feishu连接：`curl -f https://your-domain.com/api/plugins/feishu/events`
3. 检查记忆存储：`ls ~/.openclaw/memory/`
4. 如有异常，发送通知到飞书群组
```

---

## 八、生产环境部署

### 8.1 Nginx反向代理（必需）

飞书Webhook要求HTTPS，需要Nginx配置：

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
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

**SSL证书获取（Let's Encrypt）**:

```bash
sudo certbot --nginx -d your-domain.com
# 自动续期：certbot renew
```

**注意**：国内域名必须ICP备案，否则飞书无法验证Webhook。

### 8.2 systemd服务配置

创建 `/etc/systemd/system/openclaw.service`：

```ini
[Unit]
Description=OpenClaw AI Gateway
After=network.target

[Service]
Type=simple
User=yourname
WorkingDirectory=/home/yourname/.openclaw
ExecStart=/usr/local/bin/openclaw gateway
Restart=always
RestartSec=10
LimitNOFILE=65536

[Install]
WantedBy=multi-user.target
```

启用服务：

```bash
sudo systemctl daemon-reload
sudo systemctl enable openclaw
sudo systemctl start openclaw
sudo systemctl status openclaw
```

### 8.3 日志与监控

```bash
# 实时监控日志
openclaw logs --follow

# 查看错误日志
openclaw logs --level error --tail 50

# cron定时检查
*/30 * * * * openclaw status >> /var/log/openclaw/health.log
*/30 * * * * openclaw logs --level error --tail 5 >> /var/log/openclaw/errors.log
```

---

## 九、实际使用场景

### 场景1：快速笔记

**流程**：
1. 在飞书文档中写笔记
2. @PKM助手并发送"保存到记忆"
3. 技能自动提取关键词，存入向量数据库
4. 后续可通过语义搜索快速找到

### 场景2：知识问答

```
用户：@PKM助手 我之前说过OpenClaw怎么安装吗？
助手：检索到2条相关记忆：
1. 2026-03-30: OpenClaw安装步骤...
2. 2026-04-01: Node.js版本问题...
   
简要回答：运行安装脚本后执行openclaw onboard...
```

### 场景3：每日报告

**自动流程**（每天9:00）：
1. cron触发 `daily-report` 技能
2. 检索昨日所有记忆
3. 统计新增条目、类型分布
4. 生成格式化报告
5. 发送到飞书群组

**报告示例**：

```
📊 每日知识报告 (2026-04-01)

📝 新增知识条目: 12 条
🏷️ 知识类型分布: summary:5, note:4, qa:3
⏰ 生成时间: 2026-04-02 09:00:15

📋 最新条目:
• summary: OpenClaw安装步骤详解...
• note: Node.js版本问题解决方案...
• qa: 如何配置Feishu webhook...

💡 建议：可以@我搜索特定主题，如"安装问题"
```

---

## 十、优化与扩展

### 10.1 性能优化

```json
{
  "cache": {
    "enabled": true,
    "maxSize": 1000,
    "ttl": 3600
  },
  "memory": {
    "provider": "postgres",  // PostgreSQL性能更好
    "poolSize": 10,
    "vectorDim": 1536
  }
}
```

### 10.2 安全加固

- 修改默认端口（8080 → 随机高端口）
- 启用API密钥验证
- 配置防火墙（仅开放443和自定义端口）
- 定期备份 `~/.openclaw/` 到云存储

### 10.3 扩展技能 ideas

- **Auto-tagging**：基于内容自动分类（已有tagify）
- **Document linking**：发现文档间的关联关系
- **Knowledge graph**：构建知识网络可视化
- **Cross-platform sync**：同步Notion、Obsidian数据
- **Email parser**：解析重要邮件存入知识库
- **GitHub monitor**：监控star增长、issue趋势

---

## 十一、总结

通过这个实战案例，你已经学会了：

✅ 用OpenClaw + Feishu搭建知识入口  
✅ 配置记忆系统实现语义检索  
✅ 开发4个核心技能（摘要、标签、报告、搜索）  
✅ 设置cron自动化与heartbeat监控  
✅ 生产环境部署（Nginx + systemd）  

**这套系统真正做到了**：
- 零手动整理：所有内容自动摘要、标签、归档
- 秒级检索：语义搜索，不用记关键字
- 智能回顾：每日报告，温故知新
- 完全自主：数据在自己服务器

**下一步**：
1. 根据你的需求调整技能逻辑
2. 接入更多平台（Telegram、Discord等）
3. 开发更复杂的技能（知识图谱、自动化流程）
4. 分享你的使用经验

---

## 配套资源

完整项目代码已开源，包括：

```
openclaw-pkm-case/
├── blog-article-zh.mdx    # 本文博客原文
├── blog-article-en.mdx    # 英文版
├── articles/              # 各平台适配版本
│   ├── zhihu-answer.md    # 知乎精简版
│   ├── wechat-article.md  # 公众号版（本文）
│   ├── csdn-article.md    # CSDN版
│   ├── devto-post.md      # Dev.to版
│   └── xiaohongshu-post.md # 小红书版
├── images/                # 配图
├── scripts/              # 生成脚本
├── skills/               # 所有技能源码
│   ├── summarize.js
│   ├── tagify.js
│   ├── daily-report.js
│   └── search.js
├── config.example.json   # 配置示例
└── README.md             # 项目说明
```

**获取地址**：
- GitHub: https://github.com/kunpeng-ai-research/ai-research/tree/main/openclaw-pkm-case
- 博客: https://kunpeng-ai.com/blog/openclaw-pkm-case

---

## 互动

有问题？欢迎：
- 在博客评论区提问
- GitHub提Issue
- 加入OpenClaw官方Discord社区

**祝你搭建出属于自己的AI知识管理平台！** 🚀
