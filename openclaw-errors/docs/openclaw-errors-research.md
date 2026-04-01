# OpenClaw 常见错误与解决方案 - 研究资料

## 错误分类

### 1. 安装阶段错误

#### 1.1 安装脚本下载失败
**现象**:
```bash
curl: (60) SSL certificate problem
```
或下载速度极慢/超时

**原因**:
- 网络环境问题（国内访问GitHub慢）
- SSL证书验证失败

**解决方案**:
1. 使用国内镜像源
2. 跳过SSL验证（临时）
3. 手动下载离线包

**参考文档**: 入门指南"中国用户特别注意"章节

---

#### 1.2 Node.js版本不兼容
**现象**:
```
Error: Node.js version 18.x is not supported. Please use Node.js 24.x
```

**原因**: OpenClaw要求Node.js 24.x

**解决方案**:
```bash
# 使用nvm
nvm install 24
nvm use 24

# Windows原生用nvm-windows
nvm install 24
nvm use 24
```

---

#### 1.3 PowerShell执行策略（Windows）
**现象**:
```
File cannot be loaded because running scripts is disabled on this system.
```

**原因**: PowerShell执行策略限制

**解决方案**:
```powershell
# 临时允许（当前会话）
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass

# 永久修改（当前用户）
Set-ExecutionPolicy -Scope CurrentUser -ExecutionPolicy RemoteSigned

# 管理员权限运行
```

---

#### 1.4 WSL2安装问题（Windows）
**现象**: WSL2安装失败或无法启动

**解决方案**:
```powershell
# 启用WSL功能
dism.exe /online /enable-feature /featurename:Microsoft-Windows-Subsystem-Linux /all /norestart

# 启用虚拟机平台
dism.exe /online /enable-feature /featurename:VirtualMachinePlatform /all /norestart

# 更新WSL内核
wsl --update
```

---

### 2. 配置阶段错误

#### 2.1 API Key无效
**现象**:
```
Error: Invalid API key
```

**原因**:
- API key格式错误（OpenAI应以sk-开头）
- API key过期或未激活
- 复制时包含了空格

**解决方案**:
- 检查key格式：`sk-...`（OpenAI），`sk-ant-...`（Anthropic）
- 在官网测试key有效性
- 重新复制，确保无空格

---

#### 2.2 配置文件语法错误
**现象**:
```
Error: Invalid JSON in config file
```

**原因**: `~/.openclaw/config.json` 格式错误

**解决方案**:
```bash
# 验证配置
openclaw config validate

# 使用在线JSON校验工具
# 或重置配置
openclaw config reset
```

---

#### 2.3 Ollama连接失败
**现象**:
```
Cannot connect to Ollama at http://localhost:11434
```

**原因**:
- Ollama未运行
- 端口不对
- WSL2与Windows网络隔离

**解决方案**:
```bash
# 检查Ollama状态
systemctl status ollama  # Linux
# 或
ps aux | grep ollama     # 检查进程

# 启动Ollama
ollama serve &

# 测试连接
curl http://localhost:11434/api/tags
```

**WSL2特有**: 确保Ollama在WSL2内运行，不是Windows

---

### 3. 运行阶段错误

#### 3.1 端口8080被占用
**现象**:
```
Error: listen EADDRINUSE: :::8080
```

**原因**: 其他进程占用了8080端口

**解决方案**:
```bash
# 查找占用进程
netstat -ano | findstr :8080  # Windows
lsof -i :8080                 # Linux/macOS

# 方案1：停止占用进程
taskkill /PID <PID> /F  # Windows
kill -9 <PID>           # Linux/macOS

# 方案2：修改OpenClaw端口（推荐）
openclaw config edit
# 修改 "gateway.port": 8081
openclaw restart
```

---

#### 3.2 消息收不到
**现象**: Bot在线，但不响应消息

**排查清单**:
- [ ] `openclaw status` 确认网关运行
- [ ] 平台Bot是否在线（Telegram:@BotFather）
- [ ] 配置文件是否正确
- [ ] 防火墙是否放行端口
- [ ] 查看日志: `openclaw logs --follow`

**常见原因**:
- 事件订阅URL错误（飞书）
- Bot未安装到当前聊天
- 权限不足

---

#### 3.3 飞书Webhook验证失败
**现象**: 飞书提示"URL验证失败"

**原因**:
- 域名未备案（国内必须）
- HTTPS证书无效
- Nginx反向代理配置错误

**解决方案**:
- 确保域名已备案
- 使用Let's Encrypt免费证书
- 检查Nginx配置（SSL、proxy_pass）

---

#### 3.4 Gateway启动失败
**现象**:
```
Error: Failed to start gateway
```

**常见原因**:
- 端口被占用（见3.1）
- 配置文件语法错误（见2.2）
- 权限不足（修改~/.openclaw权限）
- 环境变量缺失

**解决方案**:
```bash
# 查看详细日志
openclaw logs --level error

# 验证配置
openclaw config validate

# 检查端口占用
netstat -ano | findstr :8080
```

---

### 4. 集成特定错误

#### 4.1 Telegram Bot未响应
**检查清单**:
- [ ] Bot Token是否正确
- [ ] Bot是否已激活（@BotFather /mybots）
- [ ] Bot是否有"隐私模式"（影响收消息）
- [ ] 是否禁用了"隐私模式"（Group Chat需要）

**解决方案**:
1. 通过 @BotFather 检查Bot状态
2. 确保Bot已加入目标群组
3. 关闭隐私模式（@BotFather → Bot Settings → Privacy Mode → Disable）

---

#### 4.2 Discord 401/403错误
**现象**: 日志显示权限错误

**原因**:
- Bot Token错误
- 未启用Message Content Intent
- 缺少频道权限

**解决方案**:
1. 重新复制Bot Token
2. 在Developer Portal启用Message Content Intent
3. 确保Bot有"Send Messages"和"Read Message History"权限

---

#### 4.3 飞书消息收不到
**排查步骤**:
1. 检查网关状态: `openclaw status`
2. 查看飞书事件订阅日志（开发者后台）
3. 查看OpenClaw日志: `openclaw logs | grep feishu`

**常见原因**:
- 事件订阅URL错误
- 机器人未安装到当前聊天
- 权限不足（检查 `im:message` 权限）

---

### 5. 性能与稳定性

#### 5.1 响应延迟高
**排查**:
```bash
# 查看日志中的延迟
openclaw logs | grep latency

# ping测试AI provider网络
ping api.openai.com
```

**优化**:
- 使用本地Ollama（无网络延迟）
- 启用缓存（config.json中配置）
- 选择更快的模型

---

#### 5.2 内存占用过高
**现象**: 内存持续增长，最终OOM

**原因**:
- 未限制缓存大小
- 长时间运行积累历史

**解决方案**:
```json
{
  "cache": {
    "enabled": true,
    "maxSize": 1000,  // 限制缓存条目
    "ttl": 3600
  }
}
```

---

### 6. 生产环境问题

#### 6.1 SSL证书过期
**现象**: 浏览器访问提示不安全

**解决方案**:
```bash
# 自动续期Let's Encrypt
certbot renew

# 或手动更新
certbot --nginx -d your-domain.com
```

---

#### 6.2 系统服务崩溃
**现象**: OpenClaw服务意外停止

**解决方案**:
```bash
# Linux systemd
sudo systemctl status openclaw
sudo journalctl -u openclaw -f

# 设置自动重启
sudo systemctl enable openclaw
```

---

## 错误数据库（待补充）

需要从以下来源收集更多真实错误：
- GitHub Issues
- Discord社区
- 用户反馈

---

## 预防措施

1. **安装前检查清单**
   - Node.js版本 >= 24
   - 系统满足最低要求
   - 网络连通性测试

2. **配置最佳实践**
   - 使用 `openclaw config validate` 验证
   - 先小规模测试再生产部署
   - 备份配置文件

3. **监控与告警**
   - 设置日志轮转
   - 监控端口和进程
   - 定期检查API额度

---

## 参考资料

- 官方文档: https://docs.openclaw.ai
- GitHub Issues: https://github.com/openclaw/openclaw/issues
- Discord社区: https://discord.gg/clawd
