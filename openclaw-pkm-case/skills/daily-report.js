/**
 * 每日知识报告技能
 * 功能：自动生成每日知识总结并发送通知
 */

export const name = 'daily-report';
export const description = '生成并发送每日知识报告';

export async function execute(ctx) {
  try {
    // 1. 获取昨天的所有记忆（根据时间范围）
    const yesterday = new Date();
    yesterday.setDate(yesterday.getDate() - 1);
    const startDate = yesterday.toISOString();
    
    const memories = await ctx.memory.search('', {
      limit: 50,
      from: startDate
    });
    
    if (memories.length === 0) {
      return { success: true, message: '昨日无新知识' };
    }
    
    // 2. 按类型分组
    const summaries = memories.map(mem => {
      return `• ${mem.type}: ${mem.content.substring(0, 100)}...`;
    });
    
    // 3. 生成统计报告
    const stats = `
📊 每日知识报告 (${yesterday.toLocaleDateString('zh-CN')})

📝 新增知识条目: ${memories.length} 条
🏷️ 知识类型分布: ${getTypeDistribution(memories)}
⏰ 生成时间: ${new Date().toLocaleString('zh-CN')}

📋 最新条目:
${summaries.slice(0, 10).join('\n')}

${memories.length > 10 ? `... 还有 ${memories.length - 10} 条未显示` : ''}

💡 建议：可以@我搜索特定主题，如"OpenClaw安装"
    `.trim();
    
    // 4. 发送到配置的群组（如果有）
    const targetChat = ctx.config.cron?.reportTargetChat;
    if (targetChat) {
      await ctx.feishu.sendMessage({
        chatId: targetChat,
        content: stats
      });
    }
    
    return { 
      success: true, 
      stats: {
        total: memories.length,
        date: yesterday.toISOString().split('T')[0]
      }
    };
  } catch (error) {
    ctx.logger.error('Daily report error:', error);
    return { error: error.message };
  }
}

function getTypeDistribution(memories) {
  const counts = {};
  memories.forEach(m => {
    counts[m.type] = (counts[m.type] || 0) + 1;
  });
  return Object.entries(counts)
    .map(([type, count]) => `${type}:${count}`)
    .join(', ');
}

export const schema = {
  type: 'object',
  properties: {}
};
