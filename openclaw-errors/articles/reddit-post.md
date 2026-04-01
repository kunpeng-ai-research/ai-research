# OpenClaw: 15+ Common Errors Solved - A Troubleshooting Guide for Self-Hosted AI Gateway

Hey r/selfhosted and r/LocalLLaMA,

I've been running OpenClaw (self-hosted AI gateway for 20+ chat apps) for months and hit many errors along the way. Instead of figuring it out each time, I compiled a **complete troubleshooting guide** covering 15+ common issues.

Sharing it here in case it helps others.

---

## Why This Guide?

OpenClaw is powerful but has a steep learning curve due to:
- Multiple OS support (Win/Linux/macOS, WSL2/Docker)
- Various AI providers (OpenAI, Anthropic, Ollama, etc.)
- Complex config (gateway, models, plugins, channels)

This guide categorizes errors by **phase**: Installation → Configuration → Runtime → Integration → Production.

---

## Key Errors Covered

### Installation
1. Script download fails (especially in China)
2. Node.js version incompatibility (must be 24+)
3. PowerShell execution policy (Windows)
4. WSL2 setup issues
5. Installer hangs/timeouts

### Configuration
6. Invalid API key
7. JSON syntax errors in config
8. Ollama connection fails

### Runtime
9. Port 8080 already in use
10. Messages not arriving
11. Feishu webhook verification fails (ICP/HTTPS)
12. Telegram bot privacy mode blocks group messages
13. Gateway fails to start

### Platform-Specific
14. Discord 401/403 (token/intents/permissions)
15. WhatsApp QR code issues
16. Multi-platform user conflicts

### Production
17. High latency
18. Memory leaks
19. SSL certificate expiry
20. Service crash recovery

---

## Most Common Pitfalls

Based on community feedback, here are the **top 3** that trip people up:

### 1. Node.js Version
**Error**: `Node.js version 18.x is not supported`

**Fix**: Use nvm:
```bash
nvm install 24
nvm use 24
```

### 2. Config Validation
**Error**: `Invalid JSON in config file`

**Fix**: Run this before anything:
```bash
openclaw config validate
```

### 3. Feishu Integration
**Requires**:
- ICP-filed domain
- Valid HTTPS certificate
- Correct Nginx reverse proxy config

---

## Full Guide

I've written a detailed blog post (with code snippets, config examples, step-by-step fixes):

👉 **https://kunpeng-ai.com/blog/openclaw-errors?utm_source=reddit**

It includes:
- 15+ errors with symptoms, causes, solutions
- Complete config examples
- Production deployment checklist
- Monitoring & alerting setup
- Official resources list

---

## Discussion

**Have you used OpenClaw?**
- What errors did you encounter?
- Any tips not in the guide?
- Production deployment experience?

Let's share knowledge and help each other run OpenClaw smoothly! 🚀

---

*Note: This is a cross-post from my blog. Feedback welcome!*
