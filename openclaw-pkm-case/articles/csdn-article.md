# 用OpenClaw构建个人知识管理系统完整教程：自动化PKM实战

## 摘要

本文详细讲解如何使用OpenClaw自托管AI网关构建智能化的个人知识管理系统（PKM）。涵盖架构设计、Feishu集成、自定义技能开发、cron定时任务、生产环境部署等完整流程。包含4个核心技能源码、完整配置文件、Nginx反向代理配置和systemd服务设置。

**关键词**: OpenClaw, PKM, 知识管理, 自托管, AI助手, 实战教程

---

## 一、项目背景与需求分析

### 1.1 知识管理的痛点

作为技术从业者，日常需要处理：
- 会议记录、项目文档
- 技术文章、学习笔记
- 代码片段、解决方案
- 待办事项、日程安排

**常见问题**：
- ❌ 信息分散在不同平台，难以统一
- ❌ 手动整理耗时耗力
- ❌ 检索依赖关键字，不够智能
- ❌ 缺乏自动化，知识回顾不及时

### 1.2 为什么选择OpenClaw？

OpenClaw作为自托管AI网关，具备独特优势：

**对比传统方案**：

| 维度 | OpenClaw | Notion | Obsidian |
|------|----------|--------|----------|
| AI能力 | ✅ 内置模型调用 | ⚠️ 需插件 | ❌ 无 |
| 多平台接入 | ✅ 20+聊天平台 | ❌ 仅Web/App | ❌ 仅本地 |
| 自动化 | ✅ cron+技能 | ⚠️ API有限 | ❌ 无 |
- ✅ 自托管数据自主
- ✅ 技能无限扩展
- ✅ 模型自由切换

---

## 二、系统架构设计

### 2.1 整体架构

```
┌────────────────────────────────────────────┐
│         用户交互层（飞书/Telegram）          │
└─────────────────┬──────────────────────────┘
                  │
        ┌─────────▼─────────┐
        │  OpenClaw Gateway │
        │   消息路由中心      │
        └─────────┬─────────┘
                  │
    ┌─────────────┼─────────────┐
    ▼             ▼             ▼
┌───────┐     ┌───────┐     ┌─────────┐
│ AI    │     │ 技能  │     │ 记忆    │
│ 模型  │     │ 模块  │     │ 系统    │
└───────┘     └───────┘     └─────────┘
                            │
                  ┌─────────┴──────────┐
                  ▼                     ▼
           语义检索+自动保存        定期报告
```

### 2.2 核心组件详解

1. **OpenClaw Gateway**
   - 接收各平台消息
   - 路由到AI或技能
   - 统一回复格式
   - 端口默认8080

2. **AI模型层**
   - OpenAI API（质量优先）
   - Anthropic Claude（安全对话）
   - Ollama本地（免费隐私）

3. **技能模块**（本文重点）
   - `summarize`: 自动摘要
   - `tagify`: 自动标签
   - `daily-report`: 每日报告
   - `search`: 语义搜索

4. **记忆系统**
   - 存储所有对话
   - 向量化语义检索
   - SQLite/PostgreSQL/Redis支持

5. **定时任务**
   - cron: 定时执行技能
   - heartbeat: 健康监控

---

## 三、环境搭建与安装

### 3.1 安装OpenClaw

**macOS/Linux**:

```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows（推荐WSL2）**:

```powershell
# 在WSL2终端中
curl -fsSL https://openclaw.ai/install.sh | bash
```

**系统要求**:
- Node.js 24.x（脚本自动安装）
- RAM ≥ 4GB
- Disk ≥ 5GB
- 网络（如使用云端模型）

### 3.2 初始配置

```bash
openclaw onboard --install-daemon
```

**配置步骤**:
1. 选择AI Provider（推荐Ollama或OpenAI）
2. 生成Gateway Token（保存好）
3. 安装为系统服务（勾选--install-daemon）
4. 验证: `openclaw status`

---

## 四、Feishu集成（知识入口）

### 4.1 安装Feishu插件

```bash
openclaw plugins install feishu
```

### 4.2 飞书开发者后台配置

1. 访问 https://open.feishu.cn/
2. 创建应用 → 获取 App ID & App Secret
3. 启用权限:
   - `im:message`（消息读写）
   - `drive:readonly`（文档读取）
   - `docx:readonly`（文档内容）
4. 生成 Encrypt Key
5. 配置事件订阅:
   - URL: `openclaw urls` 输出的 Feishu Event URL
   - Verification Token: 复制
   - 订阅事件: `im.message.receive_v1`
6. 添加机器人到文档/群组

⚠️ **注意**:
- URL必须是HTTPS且域名已ICP备案
- 必须使用 `openclaw urls` 输出的URL

### 4.3 OpenClaw配置更新

编辑 `~/.openclaw/config.json`:

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

重启: `openclaw restart`

---

## 五、记忆系统配置

记忆系统自动保存所有对话，支持语义搜索。

### 5.1 配置

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

### 5.2 使用示例

**自动保存**: 所有对话自动存入记忆

```
用户：OpenClaw的安装步骤？
助手：1. 运行安装脚本... [自动保存到记忆]
```

**语义搜索**:

```
用户：@PKM助手 搜索OpenClaw安装相关的笔记
助手：找到3条记忆：
1. 2026-03-30: 完整安装步骤...
2. 2026-04-01: Node.js版本问题...
```

---

## 六、自定义技能开发

技能是OpenClaw的扩展机制，用JavaScript编写。

### 6.1 技能结构

每个技能文件导出:

```javascript
export const name = 'skill-name';
export const description = '技能描述';

export async function execute(ctx, args) {
  // 技能逻辑
  return { result };
}

export const schema = {
  type: 'object',
  properties: { /* 参数定义 */ },
  required: []
};
```

### 6.2 技能1：自动摘要 (summarize.js)

```javascript
export const name = 'summarize';
export const description = '自动生成文档摘要';

export async function execute(ctx, args) {
  const { content, maxLength = 100 } = args;
  
  if (!content) {
    return { error: '缺少content参数' };
  }
  
  const prompt = `用${maxLength}字概括：\n${content}`;
  const summary = await ctx.agent.generate(prompt);
  
  // 保存摘要到记忆
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
    content: { type: 'string', description: '原文内容' },
    title: { type: 'string', description: '标题（可选）' },
    maxLength: { type: 'number', description: '最大字数（默认100）' }
  },
  required: ['content']
};
```

### 6.3 技能2：自动标签 (tagify.js)

```javascript
export const name = 'tagify';
export const description = '自动为内容生成标签';

export async function execute(ctx, args) {
  const { content } = args;
  
  const prompt = `为以下内容生成3-5个标签（逗号分隔）：\n\n${content}`;
  const tagsText = await ctx.agent.generate(prompt);
  
  const tags = tagsText
    .split(/[,，、\n]/)
    .map(t => t.trim())
    .filter(t => t.length > 0)
    .slice(0, 5);
    
  return { tags };
}

export const schema = {
  type: 'object',
  properties: {
    content: { type: 'string' }
  },
  required: ['content']
};
```

### 6.4 技能3：每日报告 (daily-report.js)

```javascript
export const name = 'daily-report';
export const description = '生成每日知识报告';

export async function execute(ctx) {
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  
  // 检索昨日记忆
  const memories = await ctx.memory.search('', {
    limit: 50,
    from: yesterday.toISOString()
  });
  
  const stats = `
📊 每日知识报告 (${yesterday.toLocaleDateString('zh-CN')})

📝 新增知识条目: ${memories.length} 条
⏰ 生成时间: ${new Date().toLocaleString('zh-CN')}

📋 最新条目:
${memories.slice(0, 10).map(m => 
  `• ${m.content.substring(0, 50)}...`
).join('\n')}
  `.trim();
  
  // 发送到飞书群组
  const targetChat = ctx.config.skills?.dailyReport?.targetChat;
  if (targetChat) {
    await ctx.feishu.sendMessage({
      chatId: targetChat,
      content: stats
    });
  }
  
  return { success: true, count: memories.length };
}

export const schema = {
  type: 'object',
  properties: {}
};
```

### 6.5 技能4：语义搜索 (search.js)

```javascript
export const name = 'search';
export const description = '在知识库中语义搜索';

export async function execute(ctx, args) {
  const { query, limit = 5 } = args;
  
  if (!query) {
    return { error: '缺少query参数' };
  }
  
  const results = await ctx.memory.search(query, {
    limit: parseInt(limit),
    threshold: 0.7
  });
  
  return {
    success: true,
    query,
    total: results.length,
    results: results.map((r, i) => ({
      rank: i + 1,
      content: r.content.substring(0, 200),
      type: r.type,
      similarity: r.score?.toFixed(2)
    }))
  };
}

export const schema = {
  type: 'object',
  properties: {
    query: { type: 'string' },
    limit: { type: 'number' }
  },
  required: ['query']
};
```

### 6.6 启用技能

在 `config.json` 中添加:

```json
{
  "skills": {
    "enabled": ["summarize", "tagify", "daily-report", "search"],
    "daily-report": {
      "targetChat": "your_feishu_group_chat_id"
    }
  },
  "cron": {
    "enabled": true,
    "schedule": "0 9 * * *",
    "task": "daily-report"
  }
}
```

重启: `openclaw restart`

---

## 七、生产环境部署

### 7.1 Nginx反向代理（必需）

飞书Webhook要求HTTPS，需Nginx配置:

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

**SSL证书获取**（Let's Encrypt）:

```bash
sudo certbot --nginx -d your-domain.com
# 自动续期: certbot renew
```

⚠️ **国内域名必须ICP备案，否则飞书Webhook验证失败**

### 7.2 systemd服务

创建 `/etc/systemd/system/openclaw.service`:

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

启用:

```bash
sudo systemctl daemon-reload
sudo systemctl enable openclaw
sudo systemctl start openclaw
sudo systemctl status openclaw
```

### 7.3 监控与日志

```bash
# 实时监控
openclaw logs --follow

# 错误日志
openclaw logs --level error --tail 50

# 定时检查（crontab）
*/30 * * * * openclaw status >> /var/log/openclaw/health.log
*/30 * * * * openclaw logs --level error --tail 5 >> /var/log/openclaw/errors.log
```

---

## 八、使用流程与效果

### 8.1 快速笔记

```
用户：在飞书文档写完笔记
操作：@PKM助手 发送"保存到记忆"
结果：技能自动提取关键词，存入向量数据库
后续：可通过语义搜索快速找到
```

### 8.2 知识问答

```
用户：@PKM助手 我之前说过OpenClaw怎么安装吗？
助手：检索到3条相关记忆：
  1. 2026-03-30: OpenClaw完整安装步骤...
  2. 2026-04-01: Node.js版本问题...
  3. 2026-04-02: WSL2安装问题...
  
简要回答：运行安装脚本后执行openclaw onboard...
```

### 8.3 每日报告（自动）

**每天9:00自动执行**:
1. cron触发 `daily-report` 技能
2. 检索昨日所有记忆
3. 生成统计报告
4. 发送到飞书群组

**报告示例**:

```
📊 每日知识报告 (2026-04-01)

📝 新增知识条目: 12 条
🏷️ 知识类型: summary:5, note:4, qa:3
⏰ 生成时间: 2026-04-02 09:00:15

📋 最新条目:
• summary: OpenClaw安装步骤详解...
• note: Node.js版本问题解决方案...
• qa: 如何配置Feishu webhook...

💡 提示：可以@我搜索特定主题
```

---

## 九、优化建议

### 9.1 性能优化

```json
{
  "cache": {
    "enabled": true,
    "maxSize": 1000,
    "ttl": 3600
  },
  "memory": {
    "provider": "postgres",
    "poolSize": 10
  }
}
```

### 9.2 安全加固

- 修改默认端口（8080 → 随机高端口）
- 启用API密钥验证
- 配置防火墙（仅开放443）
- 每周备份 `~/.openclaw/`

### 9.3 可扩展技能

- **Auto-tagging**: 自动分类（已完成tagify）
- **Document linking**: 文档关联
- **Knowledge graph**: 知识图谱可视化
- **Cross-platform sync**: 同步Notion/Obsidian
- **Email parser**: 邮件解析入库
- **GitHub monitor**: 监控star/issue趋势

---

## 十、总结与完整代码

### 10.1 核心收获

通过本文，你学会了：

✅ OpenClaw + Feishu搭建知识入口  
✅ 记忆系统配置与语义检索  
✅ 4个核心技能开发（摘要/标签/报告/搜索）  
✅ cron自动化与heartbeat监控  
✅ 生产部署（Nginx + systemd）  

### 10.2 完整项目结构

```
openclaw-pkm-case/
├── blog-article-zh.mdx    # 博客原文
├── blog-article-en.mdx    # 英文版
├── articles/
│   ├── zhihu-answer.md    # 知乎
│   ├── wechat-article.md  # 公众号（本文）
│   ├── csdn-article.md    # CSDN
│   ├── devto-post.md      # Dev.to
│   └── xiaohongshu-post.md # 小红书
├── images/               # 配图
├── scripts/             # 生成脚本
├── skills/              # 技能源码
│   ├── summarize.js
│   ├── tagify.js
│   ├── daily-report.js
│   └── search.js
├── config.example.json  # 配置示例
└── README.md            # 项目说明
```

### 10.3 获取完整代码

**GitHub仓库**:  
https://github.com/kunpeng-ai-research/ai-research/tree/main/openclaw-pkm-case

**博客原文**:  
https://kunpeng-ai.com/blog/openclaw-pkm-case

---

## 附录：常见问题

**Q1: OpenClaw和Notion/Obsidian有什么区别？**  
A: Notion/Obsidian是笔记工具，OpenClaw是AI自动化平台。OpenClaw可以接入Notion作为数据源，但提供AI处理和自动化能力。

**Q2: 本地Ollama和OpenAI API怎么选？**  
A: Ollama免费隐私好，适合单机；OpenAI质量更高，适合生产。可以混合使用。

**Q3: 记忆容量有限制吗？**  
A: SQLite默认无限制，但建议设置 `maxEntries` 和 `ttlDays` 自动清理。

**Q4: 可以接入其他平台吗？**  
A: 可以，OpenClaw支持Telegram、Discord、WhatsApp等20+平台。

**Q5: 技能开发复杂吗？**  
A: 只要会JavaScript，参考本文示例即可快速上手。API设计简洁。

---

**最后更新**: 2026-04-02  
**维护**: 鲲鹏AI探索局  
**许可**: CC BY-NC-SA 4.0
