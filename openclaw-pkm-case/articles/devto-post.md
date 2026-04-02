# Building a Personal Knowledge Management System with OpenClaw: Complete Tutorial

## Summary

A complete guide to building an AI-powered PKM system using OpenClaw self-hosted AI gateway. Covers architecture design, Feishu integration, custom skill development, cron automation, production deployment with Nginx + systemd. Includes 4 core skills source code, full config examples, and monitoring setup.

**Tags**: openclaw, pkm, knowledgemanagement, tutorial, aiassistant, selfhosted

---

## Why OpenClaw for PKM?

Traditional PKM tools (Notion, Obsidian) lack AI automation. OpenClaw fills the gap:

- ✅ Multi-platform access (Feishu, Telegram, Discord)
- ✅ Built-in AI capabilities (OpenAI, Anthropic, Ollama)
- ✅ Custom skills for automation
- ✅ Self-hosted data control
- ✅ Semantic search out of the box

---

## Architecture

```
User Input (Feishu/Telegram)
    ↓
OpenClaw Gateway
    ↓
├── AI Model (response generation)
├── Skills (automation)
└── Memory (storage + retrieval)
    ↓
Reply + Auto-save + Scheduled Reports
```

---

## Installation

```bash
# macOS/Linux
curl -fsSL https://openclaw.ai/install.sh | bash

# Windows (WSL2)
curl -fsSL https://openclaw.ai/install.sh | bash

# Initial setup
openclaw onboard --install-daemon
```

---

## Feishu Integration

```bash
openclaw plugins install feishu
```

**Feishu Developer Console**:
1. Create app → get App ID & Secret
2. Enable scopes: `im:message`, `drive:readonly`, `docx:readonly`
3. Configure Event URL: `openclaw urls` (must be HTTPS with ICP备案)
4. Add bot to docs/groups

**Config** (`~/.openclaw/config.json`):

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

---

## Memory System

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

**Usage**:
- Auto-saves all conversations
- Semantic search: `@PKM Assistant search for OpenClaw installation`

---

## Custom Skills

### 1. Summarize

```javascript
// skills/summarize.js
export const name = 'summarize';
export async function execute(ctx, args) {
  const { content, maxLength = 100 } = args;
  const summary = await ctx.agent.generate(
    `Summarize in ${maxLength} words:\n${content}`
  );
  await ctx.memory.remember({
    type: 'summary',
    content: summary
  });
  return { summary };
}
```

### 2. Tagify (Auto-tagging)

```javascript
export const name = 'tagify';
export async function execute(ctx, args) {
  const { content } = args;
  const tagsText = await ctx.agent.generate(
    `Generate 3-5 tags (comma-separated):\n${content}`
  );
  const tags = tagsText.split(/[,，、\n]/)
    .map(t => t.trim())
    .filter(t => t)
    .slice(0, 5);
  return { tags };
}
```

### 3. Daily Report

```javascript
export const name = 'daily-report';
export async function execute(ctx) {
  const yesterday = new Date();
  yesterday.setDate(yesterday.getDate() - 1);
  
  const memories = await ctx.memory.search('', {
    from: yesterday.toISOString(),
    limit: 50
  });
  
  const report = `📊 Daily Report (${yesterday.toLocaleDateString()})
📝 New entries: ${memories.length}
Latest: ${memories.slice(0, 3).map(m => 
  `• ${m.content.substring(0, 50)}...`
).join('\n')}`;
  
  await ctx.feishu.sendMessage({
    chatId: ctx.config.skills?.dailyReport?.targetChat,
    content: report
  });
  
  return { success: true, count: memories.length };
}
```

### 4. Semantic Search

```javascript
export const name = 'search';
export async function execute(ctx, args) {
  const { query, limit = 5 } = args;
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
```

### Enable Skills

```json
{
  "skills": {
    "enabled": ["summarize", "tagify", "daily-report", "search"],
    "daily-report": {
      "targetChat": "your_feishu_group_id"
    }
  },
  "cron": {
    "enabled": true,
    "schedule": "0 9 * * *",
    "task": "daily-report"
  }
}
```

---

## Production Deployment

### Nginx Reverse Proxy

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

**SSL**: `sudo certbot --nginx -d your-domain.com`

⚠️ **Chinese domain must have ICP备案** or Feishu webhook verification fails.

### systemd Service

`/etc/systemd/system/openclaw.service`:

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

```bash
sudo systemctl daemon-reload
sudo systemctl enable openclaw
sudo systemctl start openclaw
sudo systemctl status openclaw
```

---

## Real-World Usage

### Quick Note-taking

```
1. Write notes in Feishu doc
2. @PKM Assistant "save to memory"
3. Auto-extract keywords, store in vector DB
4. Search later via semantic queries
```

### Knowledge Q&A

```
User: @PKM Assistant how to install OpenClaw?
Assistant: Found 3 related memories:
  1. 2026-03-30: Full installation steps...
  2. 2026-04-01: Node.js version issues...
  3. 2026-04-02: WSL2 setup...
```

### Daily Report (Auto)

Every 9:00 AM:
1. cron triggers `daily-report`
2. Fetches yesterday's memories
3. Generates stats
4. Sends to Feishu group

---

## Optimization

```json
{
  "cache": { "enabled": true, "maxSize": 1000, "ttl": 3600 },
  "memory": { "provider": "postgres", "poolSize": 10 }
}
```

Security:
- Change default port
- Enable API key auth
- Configure firewall (443 only)
- Weekly backup `~/.openclaw/`

---

## Complete Source Code

**GitHub**: https://github.com/kunpeng-ai-research/ai-research/tree/main/openclaw-pkm-case

Includes:
- All skill source code
- Full config examples
- Deployment scripts
- Platform-specific articles

---

**Happy PKM building!** 🐋
