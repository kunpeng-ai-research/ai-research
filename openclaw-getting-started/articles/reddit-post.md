Title: I built OpenClaw - a self-hosted AI gateway that works with 20+ chat apps. Here's my 5-minute setup guide.

Body:

**TL;DR**: OpenClaw lets you run your own AI assistant that connects to WhatsApp, Telegram, Discord, iMessage, and more. No cloud lock-in, full data control. I've been using it for 3 months and it's been rock solid.

---

## What is OpenClaw?

OpenClaw is a self-hosted gateway that bridges any chat app to any AI model.

```
[WhatsApp]  [Telegram]  [Discord]
       \       |       /
        \      |      /
     [OpenClaw Gateway]
           |
    [OpenAI / Claude / Ollama]
```

It's like having ChatGPT in your pocket, but:
- ✅ Your data never leaves your machine
- ✅ Works on any chat app you already use
- ✅ Switch AI providers anytime
- ✅ No monthly subscription (just API costs or local models)

---

## Why I chose OpenClaw over ChatGPT/Claude

I was tired of:
- Paying $20/month for ChatGPT Plus
- Not being able to use it on my phone without the official app
- Worrying about my chat history being stored on OpenAI's servers
- Being locked into one provider

OpenClaw solved all of that. I run it on a $5/mo VPS, use my own OpenAI API key ($5-10/month in usage), and chat with it from Telegram, Discord, and iMessage.

---

## Quick Start (5 minutes)

### 1. Install

**macOS/Linux**:
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows (WSL2 recommended)**:
```bash
curl -fsSL https://openclaw.ai/install.sh | bash
```

**Windows PowerShell**:
```powershell
iwr -useb https://openclaw.ai/install.ps1 | iex
```

### 2. Run onboarding

```bash
openclaw onboard --install-daemon
```

You'll be prompted for:
- AI provider (OpenAI, Anthropic, Ollama, etc.)
- API key (or local model config)
- Gateway token (auto-generated)

### 3. Connect a chat platform (Telegram example)

1. Message @BotFather on Telegram
2. `/newbot` → follow prompts
3. Copy the bot token
4. Edit `~/.openclaw/config.json`:

```json5
{
  "plugins": {
    "telegram": {
      "botToken": "YOUR_BOT_TOKEN"
    }
  }
}
```

5. Restart: `openclaw restart`
6. Open your bot in Telegram and say hello!

---

## Supported Platforms (20+)

**First-class support**:
- Telegram (Bot API)
- Discord (Bot API)
- Slack (Bolt)
- Feishu (WebSocket)
- iMessage (via BlueBubbles)
- WhatsApp (via BlueBubbles)

**Community plugins**:
- LINE
- Matrix
- Signal
- IRC
- Microsoft Teams
- Nextcloud Talk
- Nostr
- And more...

Full list: https://docs.openclaw.ai/channels/index

---

## Advanced Features I Use Daily

### 1. Different personalities per platform

```json5
{
  "channels": {
    "telegram": {
      "agent": {
        "systemPrompt": "Be concise, mobile-friendly."
      }
    },
    "discord": {
      "agent": {
        "systemPrompt": "Be casual, use emoji."
      }
    }
  }
}
```

### 2. Local models with Ollama

I run `ollama serve` on the same machine and use `llama3.2:3b` for simple queries (no API cost), fall back to GPT-4 for complex stuff.

```json5
{
  "models": {
    "default": {
      "provider": "openai",
      "model": "gpt-4o"
    },
    "fallback": {
      "provider": "ollama",
      "model": "llama3.2:3b",
      "baseUrl": "http://localhost:11434"
    }
  }
}
```

### 3. Cron jobs for automation

```bash
# Daily 9 AM summary
openclaw cron create --schedule "0 9 * * *" \
  --message "Summarize yesterday's GitHub notifications" \
  --to +1234567890
```

---

## Performance & Cost

My setup: VPS (2 vCPU, 4GB RAM, $5/mo) + OpenAI API.

- **OpenAI**: ~$10-15/month for my usage (light chat + occasional coding)
- **VPS**: $5/month (could run on home server too)
- **Total**: ~$15-20/month vs ChatGPT Plus $20/month, but with WAY more flexibility.

Latency: ~500ms-2s depending on model and network.

---

## What Could Be Better?

- **Docs are a bit sparse** — I had to dig through GitHub issues for some configs
- **Windows native support** is still WSL2 recommended (not pure Windows)
- **No official mobile app** (but you can use any chat app so this is minor)
- **Initial setup requires some technical comfort** (not for complete beginners)

But the community on Discord is super helpful!

---

## Questions for r/LocalLLaMA

1. Anyone else using OpenClaw in production? What's your setup?
2. Best practices for running multiple AI providers and routing based on query type?
3. Has anyone integrated OpenClaw with Home Assistant or other IoT systems?
4. How do you handle auth for family members? Multiple chat IDs?

---

## Resources

- **GitHub**: https://github.com/openclaw/openclaw
- **Docs**: https://docs.openclaw.ai
- **Install script**: https://openclaw.ai/install.sh
- **Discord**: https://discord.gg/clawd (very active)

---

**Flair**: Discussion

---

Edit: Fixed formatting, added more details about cost breakdown.
