#!/bin/bash
# OpenClaw PKM系统部署脚本

set -e

echo "🚀 开始部署OpenClaw PKM系统..."

# 1. 检查OpenClaw是否已安装
if ! command -v openclaw &> /dev/null; then
    echo "❌ OpenClaw未安装，请先运行: curl -fsSL https://openclaw.ai/install.sh | bash"
    exit 1
fi

# 2. 检查配置文件
CONFIG_DIR="$HOME/.openclaw"
CONFIG_FILE="$CONFIG_DIR/config.json"

if [ ! -f "$CONFIG_FILE" ]; then
    echo "📝 创建初始配置文件..."
    cp config.example.json "$CONFIG_FILE"
    echo "⚠️  请编辑 $CONFIG_FILE 填入你的配置（Feishu App ID/Secret等）"
    echo "   然后运行: openclaw restart"
else
    echo "✅ 配置文件已存在"
fi

# 3. 复制技能文件
echo "🔧 安装自定义技能..."
SKILLS_DIR="$CONFIG_DIR/skills"
mkdir -p "$SKILLS_DIR"
cp skills/*.js "$SKILLS_DIR/"

# 4. 验证配置
echo "🔍 验证配置..."
openclaw config validate || {
    echo "❌ 配置验证失败，请检查 config.json"
    exit 1
}

# 5. 重启服务
echo "🔄 重启OpenClaw服务..."
openclaw restart

# 6. 检查状态
echo "📊 检查服务状态..."
openclaw status

echo "✅ 部署完成！"
echo ""
echo "📋 后续步骤："
echo "1. 确保Nginx已配置HTTPS反向代理（生产环境必需）"
echo "2. 在飞书开发者后台配置事件订阅URL（openclaw urls 获取）"
echo "3. 测试Feishu连接: openclaw plugins test feishu"
echo "4. 查看日志: openclaw logs --follow"
echo ""
echo "💡 使用提示："
echo "- 在飞书中@机器人进行交互"
echo "- 使用技能: @机器人 执行 summarize content=\"...\""
echo "- 查看记忆: openclaw memory list"
