# OpenClaw Common Errors and Solutions: 15+ Issues Covered

Hey fellow developers!

I've been using OpenClaw for a while now and encountered my fair share of errors. Instead of solving each problem from scratch, I compiled a **comprehensive troubleshooting guide** covering 15+ common issues from installation to production.

---

## Table of Contents

1. [Installation Errors (5 Issues)](#installation)
2. [Configuration Errors (3 Issues)](#configuration)
3. [Runtime Errors (5 Issues)](#runtime)
4. [Platform-Specific Issues (4 Issues)](#platform)
5. [Performance & Production (5 Tips)](#performance)
6. [Best Practices](#best-practices)
7. [Getting Help](#help)

---

## <a name="installation"></a>1. Installation Errors

### 1.1 Installer Download Fails

**Symptoms**: `curl: (60) SSL certificate problem` or timeout.

**Solutions**:

**Use Chinese mirrors**:
```bash
npm config set registry https://registry.npmmirror.com/
curl -k https://openclaw.ai/install.sh | bash
```

**Windows manual**:
```powershell
iwr -useb https://openclaw.ai/install.ps1 -OutFile install.ps1
.\install.ps1
```

---

### 1.2 Node.js Version Incompatibility

**Error**: `Node.js version 18.x is not supported. Please use Node.js 24.x`

**Fix**:
```bash
# nvm
nvm install 24
nvm use 24

# Windows: use nvm-windows
```

---

### 1.3 PowerShell Execution Policy (Windows)

**Error**: `File cannot be loaded because running scripts is disabled`

**Fix**:
```powershell
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned
```

---

### 1.4 WSL2 Installation Issues

**Enable features (Admin PowerShell)**:
```powershell
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart
wsl --update
wsl --set-default-version 2
```

---

### 1.5 Installer Hangs

**Diagnosis**:
```bash
openclaw logs --follow
```

**Common causes**: Invalid API key, proxy issues, firewall.

**Fix**: Retry or check network settings.

---

## <a name="configuration"></a>2. Configuration Errors

### 2.1 Invalid API Key

**Error**: `Error: Invalid API key`

**Checklist**:
- OpenAI key starts with `sk-`
- No extra spaces
- Test: `curl https://api.openai.com/v1/models -H "Authorization: Bearer YOUR_KEY"`

---

### 2.2 JSON Syntax Error

**Error**: `Error: Invalid JSON in config file at line XX`

**Fix**:
```bash
openclaw config validate  # validates
openclaw config reset     # reset if needed
```

Or use https://jsonlint.com/

---

### 2.3 Ollama Connection Fails

**Error**: `Cannot connect to Ollama at http://localhost:11434`

**Fix**:
```bash
# Check if Ollama is running
ps aux | grep ollama

# Start it
ollama serve &

# Test
curl http://localhost:11434/api/tags
```

**WSL2 note**: If Ollama is on Windows host, WSL2 can't access localhost. Install Ollama inside WSL2 instead.

---

## <a name="runtime"></a>3. Runtime Errors

### 3.1 Port 8080 Already in Use

**Error**: `Error: listen EADDRINUSE: :::8080`

**Fix**:

Find and kill process:
```bash
# Windows
netstat -ano | findstr :8080
taskkill /PID <PID> /F

# Linux/macOS
lsof -i :8080
kill -9 <PID>
```

Or change OpenClaw port:
```bash
openclaw config edit  # change "gateway.port" to 8081
openclaw restart
```

---

### 3.2 Messages Not Arriving

**Checklist**:

✅ `openclaw status`  
✅ Bot online (@BotFather etc.)  
✅ `openclaw config validate`  
✅ Firewall allows port  
✅ `openclaw logs --follow`

---

### 3.3 Feishu Webhook Verification Fails

**Causes**:
- Domain not ICP-filed (required in China)
- Invalid/expired HTTPS certificate
- Nginx misconfiguration

**Fix**:

1. Ensure domain is ICP-filed
2. Use valid SSL (Let's Encrypt)
3. Check Nginx config:
   ```nginx
   location / {
       proxy_pass http://127.0.0.1:8080;
       proxy_http_version 1.1;
       proxy_set_header Upgrade $http_upgrade;
       proxy_set_header Connection "upgrade";
       proxy_set_header Host $host;
   }
   ```
4. Get correct URL: `openclaw urls`

---

### 3.4 Telegram Bot Privacy Mode

**Issue**: Bot doesn't receive group messages.

**Fix**:
1. @BotFather → `/mybots`
2. Select bot → Bot Settings → Group Privacy
3. Turn off
4. Re-invite bot to group

---

### 3.5 Gateway Fails to Start

**Diagnosis**:
```bash
openclaw logs --level error --tail 50
openclaw config validate
netstat -ano | findstr :8080
```

Common fixes:
- Port in use → change port (see 3.1)
- Config error → reset config
- Permission denied → run as admin

---

## <a name="platform"></a>4. Platform-Specific Issues

### 4.1 Feishu: URL Format

**Correct**: `https://your-domain.com/api/plugins/feishu/events`

Get it from: `openclaw urls`

Must be HTTPS, no query params.

---

### 4.2 Discord: 401/403 Errors

**Causes**: Wrong token, Message Content Intent disabled, insufficient permissions.

**Fix**:
1. Re-copy Bot Token from Developer Portal
2. Enable **Message Content Intent** (required!)
3. Ensure bot has Send Messages + Read Message History permissions

---

### 4.3 WhatsApp: QR Code Issues

**Check**:
```bash
openclaw status
curl http://localhost:8080/api/plugins/whatsapp/qr
```

**Cloud server**: Open port 8080 or configure Nginx reverse proxy.

---

### 4.4 Multi-Platform Message Conflicts

**Enable user mapping** to distinguish users across platforms:
```json
{
  "plugins": {
    "common": {
      "userMapping": true
    }
  }
}
```

---

## <a name="performance"></a>5. Performance & Production

### 5.1 High Latency

**Optimizations**:
- Use local Ollama (< 1s latency)
- Enable caching (TTL 3600)
- Choose faster models (gpt-4o-mini, claude-3-haiku)

---

### 5.2 High Memory Usage

**Limit cache**:
```json
{
  "cache": {
    "enabled": true,
    "maxSize": 1000,
    "ttl": 3600
  }
}
```

---

### 5.3 SSL Certificate Expired

**Renew**:
```bash
certbot renew
systemctl reload nginx
```

Set up cron for auto-renewal.

---

### 5.4 Service Crashes

**systemd auto-restart** (`/etc/systemd/system/openclaw.service`):
```ini
[Unit]
Description=OpenClaw Gateway
After=network.target

[Service]
Type=simple
User=yourname
WorkingDirectory=/home/yourname/.openclaw
ExecStart=/usr/local/bin/openclaw gateway
Restart=always
RestartSec=10

[Install]
WantedBy=multi-user.target
```

---

## <a name="best-practices"></a>6. Best Practices

### Pre-Installation
- ✅ Node.js >= 24
- ✅ Port 8080 free
- ✅ Network connectivity

### Configuration
- ✅ `openclaw config validate` after each change
- ✅ Test locally before production
- ✅ Version control `~/.openclaw/`

### Monitoring
```bash
openclaw logs --level error --follow
# cron: */30 * * * * openclaw logs --level error --tail 10 > /var/log/openclaw/errors.log
```

---

## <a name="help"></a>7. Getting Help

**Official resources**:
- Docs: https://docs.openclaw.ai
- GitHub Issues: https://github.com/openclaw/openclaw/issues
- Discord: https://discord.gg/clawd (fastest)

**When asking for help, include**:
```bash
openclaw --version
openclaw config validate
openclaw logs --level error --tail 50
OS info
Reproduction steps
```

---

## Conclusion

Most OpenClaw errors are environment-related (Node.js version, network, permissions) or config mistakes.

**Key takeaways**:
1. Check Node.js 24+ before install
2. Always `openclaw config validate`
3. Feishu needs ICP domain + HTTPS
4. Local Ollama avoids network issues
5. Backup config with git

Stuck? Search docs and community first — 90% of issues are already solved.

---

**Full blog post** (latest updates):
https://kunpeng-ai.com/blog/openclaw-errors

Comments, questions, or your own OpenClaw troubleshooting tips? Share them below!

---

*Published on Kunpeng AI Research. Last updated: 2026-04-01*
