/**
 * 自动标签分类技能
 * 功能：分析内容并自动打上标签
 */

export const name = 'tagify';
export const description = '自动为内容生成标签和分类';

export async function execute(ctx, args) {
  const { content } = args;
  
  if (!content) {
    return { error: '缺少content参数' };
  }
  
  try {
    const prompt = `请为以下内容生成3-5个标签（标签应该是关键词，用逗号分隔）：\n\n${content}`;
    
    const tagsText = await ctx.agent.generate(prompt, {
      temperature: 0.5,
      maxTokens: 100
    });
    
    // 解析标签
    const tags = tagsText
      .split(/[,，、\n]/)
      .map(t => t.trim())
      .filter(t => t.length > 0 && t.length < 20);
    
    return { 
      success: true, 
      tags: tags.slice(0, 5) // 最多5个标签
    };
  } catch (error) {
    ctx.logger.error('Tagify skill error:', error);
    return { error: error.message };
  }
}

export const schema = {
  type: 'object',
  properties: {
    content: { type: 'string', description: '需要标签的内容' }
  },
  required: ['content']
};
