# 用OpenClaw构建个人知识管理系统：完整实战案例

## 问题背景

作为一个知识工作者，我每天需要处理大量信息：
- 飞书文档中的会议记录
- 技术文章的阅读笔记
- 项目进展和待办事项

如何让这些碎片化的知识自动整理、快速检索、定期回顾？经过摸索，我用OpenClaw搭建了一套完整的个人知识管理系统。

本文是一个完整的实战案例，包含架构设计、核心代码、部署运维全流程。

---

## 一、为什么选择OpenClaw？

OpenClaw是自托管AI网关，核心优势：

| 对比维度 | OpenClaw | ChatGPT/Claude |
|---------|----------|---------------|
| 数据控制 | ✅ 自己掌控 | ❌ 云端服务 |
| 平台接入 | ✅ 20+聊天平台 | ❌ 仅官方App |
| 模型选择 | ✅ 多Provider切换 | ❌ 单一平台 |
| 可定制性 | ✅ 技能+自动化 | ❌ 有限 |
| 部署方式 | ✅ 自托管 | ❌ 官方托管 |

如果你需要：
- 数据完全自主
- 多平台统一入口
- 可扩展的自动化
- 自定义AI工作流

OpenClaw是目前最好的选择之一。

---

## 二、系统架构

```
用户输入（飞书/Telegram）
    ↓
OpenClaw Gateway（消息路由）
    ↓
    ├→ AI模型处理（OpenAI/Ollama）
    ├→ 技能处理（摘要/标签/报告）
    └→ 记忆系统（向量存储+检索）
    ↓
回复用户 + 自动保存到知识库
```

**核心组件**：
1. **Feishu集成**：作为主要知识输入（文档+聊天）
2. **记忆系统**：自动保存所有对话，支持语义搜索
3. **技能模块**：
   - `summarize`：自动摘要
   - `tagify`：自动标签
   - `daily-report`：每日报告
   - `search`：语义检索
4. **cron任务**：每天9点生成昨日知识报告
5. **heartbeat监控**：每30分钟健康检查

---

## 三、核心功能实现

### 3.1 环境准备

```bash
# 安装OpenClaw
curl -fsSL https://openclaw.ai/install.sh | bash

# 初始配置
openclaw onboard --install-daemon

# 建议选择Ollama（免费本地）或OpenAI API
```

### 3.2 连接飞书

```bash
# 安装Feishu插件
openclaw plugins install feishu
```

配置 `~/.openclaw/config.json`：

```json
{
  "plugins": {
    "feishu": {
      "appId": "your_app_id",
      "appSecret": "your_app_secret",
      "encryptKey": "your_encrypt_key"
    }
  }
}
```

**飞书开发者后台配置**：
1. 启用权限：`im:message`、`drive:readonly`、`docx:readonly`
2. 事件订阅URL：运行 `openclaw urls` 获取 Feishu Event URL
3. 配置机器人可访问的文档和群组

### 3.3 记忆系统

```json
{
  "memory": {
    "enabled": true,
    "provider": "sqlite",
    "maxEntries": 10000,
    "ttlDays": 30
  }
}
```

所有对话自动保存，支持语义搜索：

```
用户：@PKM助手 搜索OpenClaw安装相关的笔记
助手：找到3条相关记忆：
1. 2026-03-30: OpenClaw安装步骤...
2. 2026-04-01: Node.js版本问题...
```

### 3.4 自定义技能

**技能文件结构**：

```
skills/
├── summarize.js    # 自动摘要
├── tagify.js       # 自动标签
├── daily-report.js # 每日报告
└── search.js       # 语义搜索
```

**示例：summarize技能**

```javascript
export const name = 'summarize';
export async function execute(ctx, args) {
  const { content } = args;
  const summary = await ctx.agent.generate(`用100字概括：\n${content}`);
  await ctx.memory.remember({
    type: 'summary',
    content: summary
  });
  return { summary };
}
```

**启用技能**：

```json
{
  "skills": {
    "enabled": ["summarize", "tagify", "daily-report", "search"]
  }
}
```

### 3.5 cron定时任务

```json
{
  "cron": {
    "enabled": true,
    "schedule": "0 9 * * *",  // 每天9点
    "task": "daily-report"
  }
}
```

**daily-report技能**：

```javascript
export async function execute(ctx) {
  // 获取昨天的所有记忆
  const memories = await ctx.memory.search('', { from: yesterday });
  
  // 生成报告
  const report = `📊 昨日知识报告\n新增: ${memories.length}条\n最新: ${memories[0]?.content}`;
  
  // 发送到飞书群组
  await ctx.feishu.sendMessage({
    chatId: "your_group_id",
    content: report
  });
  
  return { success: true };
}
```

---

## 四、完整配置示例

```json
{
  "gateway": {
    "port": 8080,
    "publicUrl": "https://your-domain.com"
  },
  "agent": {
    "name": "PKM助手",
    "systemPrompt": "你是个人知识管理助手，帮助用户管理、检索和总结知识。",
    "avatar": "https://example.com/pkm-avatar.png"
  },
  "models": {
    "default": {
      "provider": "ollama",
      "model": "qwen2.5:7b",
      "baseURL": "http://localhost:11434"
    }
  },
  "plugins": {
    "feishu": {
      "appId": "xxx",
      "appSecret": "xxx",
      "encryptKey": "xxx"
    }
  },
  "memory": {
    "enabled": true,
    "provider": "sqlite",
    "maxEntries": 10000,
    "ttlDays": 30
  },
  "skills": {
    "enabled": ["summarize", "tagify", "daily-report", "search"]
  },
  "cron": {
    "enabled": true,
    "schedule": "0 9 * * *",
    "task": "daily-report"
  }
}
```

---

## 五、生产环境部署

### 5.1 Nginx反向代理（必需）

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

**注意**：飞书要求HTTPS域名必须ICP备案！

### 5.2 systemd服务

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

启用：

```bash
sudo systemctl daemon-reload
sudo systemctl enable openclaw
sudo systemctl start openclaw
sudo systemctl status openclaw
```

### 5.3 监控与日志

```bash
# 实时监控
openclaw logs --follow

# cron定时检查
*/30 * * * * openclaw status >> /var/log/openclaw/health.log
*/30 * * * * openclaw logs --level error --tail 5 >> /var/log/openclaw/errors.log
```

---

## 六、实际使用场景

### 场景1：快速笔记

在飞书文档中写完笔记后，@机器人：

```
@PKM助手 保存这篇笔记到记忆
```

技能自动提取关键词，存入向量数据库。

### 场景2：知识问答

```
@PKM助手 我之前说过OpenClaw怎么安装吗？
```

OpenClaw检索记忆，找到相关对话并给出答案。

### 场景3：每日报告

每天9点，机器人自动推送昨日知识总结到飞书群组，包含：
- 新增文档数量
- 重要关键词
- 未读笔记提醒

---

## 七、优化建议

### 7.1 性能优化

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

### 7.2 安全加固

- 修改默认端口（8080 → 随机端口）
- 启用API密钥验证
- 配置防火墙（仅开放443和自定义端口）
- 每周备份 `~/.openclaw/` 目录

### 7.3 可扩展技能

继续开发：
- **Auto-tagging**：基于内容自动打标签（已完成tagify）
- **Document linking**：发现文档间的关联关系
- **Knowledge graph**：构建知识网络可视化
- **Cross-platform sync**：Notion、Obsidian等同步

---

## 八、总结

通过这个实战案例，你学会了：

- ✅ 用OpenClaw + Feishu构建知识入口
- ✅ 配置记忆系统实现语义检索
- ✅ 开发自定义技能（摘要、标签、报告）
- ✅ 设置cron自动化
- ✅ 生产环境部署与监控

这套系统可以根据你的需求无限扩展，真正成为**属于你自己的AI知识管理平台**。

**完整代码已开源**，包括所有技能源码、配置文件、部署脚本。欢迎Star和提Issue。

---

## 配套资源

- **完整代码**: https://github.com/kunpeng-ai-research/ai-research/tree/main/openclaw-pkm-case
- **博客原文**: https://kunpeng-ai.com/blog/openclaw-pkm-case
- **OpenClaw文档**: https://docs.openclaw.ai
- **技术交流**: 欢迎在评论区提问

---

**最后更新**: 2026-04-02  
**维护**: 鲲鹏AI探索局
