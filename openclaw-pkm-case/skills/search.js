/**
 * 语义搜索技能
 * 功能：在记忆中搜索相关内容
 */

export const name = 'search';
export const description = '在知识库中语义搜索相关内容';

export async function execute(ctx, args) {
  const { query, limit = 5 } = args;
  
  if (!query) {
    return { error: '缺少query参数' };
  }
  
  try {
    // 使用记忆系统的语义搜索
    const results = await ctx.memory.search(query, {
      limit: parseInt(limit),
      threshold: 0.7 // 相似度阈值
    });
    
    if (results.length === 0) {
      return { 
        success: true, 
        message: `未找到与"${query}"相关的内容`,
        results: []
      };
    }
    
    // 格式化结果
    const formatted = results.map((r, index) => ({
      rank: index + 1,
      content: r.content.substring(0, 200) + (r.content.length > 200 ? '...' : ''),
      type: r.type,
      source: r.source || 'unknown',
      similarity: r.score?.toFixed(2) || 'N/A'
    }));
    
    return { 
      success: true, 
      query,
      total: results.length,
      results: formatted
    };
  } catch (error) {
    ctx.logger.error('Search skill error:', error);
    return { error: error.message };
  }
}

export const schema = {
  type: 'object',
  properties: {
    query: { type: 'string', description: '搜索查询' },
    limit: { type: 'number', description: '最大返回结果数（默认5）' }
  },
  required: ['query']
};
