/**
 * 自动摘要技能
 * 功能：为文档或对话内容生成简洁摘要
 */

export const name = 'summarize';
export const description = '自动生成文档摘要，支持多种内容类型';

export async function execute(ctx, args) {
  const { content, maxLength = 100 } = args;
  
  if (!content) {
    return { error: '缺少content参数' };
  }
  
  try {
    // 构建prompt
    const prompt = `请用${maxLength}字以内概括以下内容，保留关键信息：\n\n${content}`;
    
    // 调用AI模型
    const summary = await ctx.agent.generate(prompt, {
      temperature: 0.3,
      maxTokens: 200
    });
    
    // 保存到记忆
    await ctx.memory.remember({
      type: 'summary',
      content: summary,
      source: args.title || 'auto-summary',
      timestamp: new Date().toISOString()
    });
    
    return { 
      success: true, 
      summary,
      originalLength: content.length,
      summaryLength: summary.length
    };
  } catch (error) {
    ctx.logger.error('Summarize skill error:', error);
    return { error: error.message };
  }
}

export const schema = {
  type: 'object',
  properties: {
    content: { type: 'string', description: '需要摘要的内容' },
    title: { type: 'string', description: '内容标题（可选）' },
    maxLength: { type: 'number', description: '摘要最大字数（默认100）' }
  },
  required: ['content']
};
