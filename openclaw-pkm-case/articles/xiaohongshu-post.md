# OpenClaw实战：用AI打造你的个人知识管理系统 🚀

作为一个知识工作者，每天要处理大量信息，如何自动化管理？今天分享我用OpenClaw搭建PKM系统的完整方案！

---

## 🌟 为什么选OpenClaw？

✅ 自托管数据自主  
✅ 20+平台接入（飞书/Telegram/Discord）  
✅ AI自动处理（摘要/标签/搜索）  
✅ 自定义技能无限扩展  
✅ 免费（用Ollama本地模型）

---

## 📐 系统架构

```
用户输入（飞书/Telegram）
    ↓
OpenClaw网关（消息路由）
    ↓
    ├→ AI模型（OpenAI/Ollama）
    ├→ 技能处理（摘要/标签/报告）
    └→ 记忆系统（向量存储）
    ↓
回复 + 自动保存 + 每日报告
```

---

## 🔧 核心功能实现

### 1️⃣ 连接飞书

```bash
openclaw plugins install feishu
```

配置App ID/Secret，事件订阅URL用 `openclaw urls` 获取

⚠️ 域名必须HTTPS且ICP备案！

### 2️⃣ 记忆系统

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

所有对话自动保存，支持语义搜索！

### 3️⃣ 4个核心技能

**summarize** - 自动摘要  
**tagify** - 自动标签  
**daily-report** - 每日报告  
**search** - 语义搜索

技能代码已开源，直接复制就能用 👇

### 4️⃣ 定时任务

```json
{
  "cron": {
    "enabled": true,
    "schedule": "0 9 * * *",
    "task": "daily-report"
  }
}
```

每天9点自动生成昨日知识总结，发送到飞书群组！

---

## 🚀 生产部署

### Nginx反向代理（必需）

```nginx
server {
    listen 443 ssl http2;
    server_name your-domain.com;
    
    ssl_certificate /etc/letsencrypt/live/your-domain.com/fullchain.pem;
    ssl_certificate_key /etc/letsencrypt/live/your-domain.com/privkey.pem;
    
    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
    }
}
```

### systemd服务

```ini
[Unit]
Description=OpenClaw AI Gateway
After=network.target

[Service]
Type=simple
User=yourname
ExecStart=/usr/local/bin/openclaw gateway
Restart=always

[Install]
WantedBy=multi-user.target
```

---

## 💡 使用场景

### 场景1：快速笔记

飞书文档写完 → @机器人"保存" → 自动存入知识库

### 场景2：知识问答

"我之前说过OpenClaw安装吗？" → AI检索记忆并回答

### 场景3：每日报告（自动）

每天9点 → 推送昨日知识总结到群组

---

## 📦 完整代码已开源

包含：
- ✅ 4个技能源码（summarize/tagify/daily-report/search）
- ✅ 完整配置文件
- ✅ Nginx + systemd部署脚本
- ✅ 各平台适配版本（知乎/公众号/CSDN/Dev.to）

**GitHub**:  
https://github.com/kunpeng-ai-research/ai-research/tree/main/openclaw-pkm-case

**博客原文**:  
https://kunpeng-ai.com/blog/openclaw-pkm-case

---

## 🎯 下一步

1. 按本文配置OpenClaw环境
2. 复制技能代码到 `~/.openclaw/skills/`
3. 更新config.json启用技能
4. 配置Nginx + HTTPS
5. 开始使用！

有任何问题欢迎评论区交流～ 👇

---

#OpenClaw #知识管理 #PKM #AI助手 #自托管 #实战教程 #技术分享

---

**最后更新**: 2026-04-02  
**维护**: 鲲鹏AI探索局
