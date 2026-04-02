# 个人知识管理系统实战

> 用OpenClaw构建属于你的AI驱动知识库

## 项目说明

这是《用OpenClaw构建个人知识管理系统：从零到生产部署》一文的配套资源仓库。

- **博客原文**: [https://kunpeng-ai.com/blog/openclaw-pkm-case](https://kunpeng-ai.com/blog/openclaw-pkm-case)
- **文章类型**: 实战案例
- **难度**: 中高级
- **预计阅读**: 15分钟

## 目录结构

```
openclaw-pkm-case/
├── blog-article-zh.mdx    # 博客原文（中文，Nextra MDX格式）
├── blog-article-en.mdx    # 博客原文（英文，Nextra MDX格式）
├── articles/              # 各平台适配版本
│   ├── zhihu-answer.md    # 知乎回答精简版
│   ├── wechat-article.md  # 微信公众号版
│   ├── csdn-article.md    # CSDN博客版
│   ├── devto-post.md      # Dev.to英文版
│   └── xiaohongshu-post.md # 小红书图文版
├── images/                # 配图资源
│   ├── cover.png         # 封面图 (1200×630)
│   ├── architecture.png  # 架构图
│   └── screenshots/      # 实际运行截图
├── scripts/              # 辅助脚本
│   ├── generate-cover.py # 封面图生成脚本
│   └── deploy.sh         # 部署脚本
└── README.md             # 本文件
```

## 快速开始

### 1. 阅读博客原文

中文版：`blog-article-zh.mdx`  
英文版：`blog-article-en.mdx`

### 2. 部署你自己的PKM系统

参考文章中的完整配置示例，或直接使用本仓库的配置：

```bash
# 克隆配置
cp -r config/ ~/.openclaw/
# 修改关键配置（appId、API keys等）
openclaw config edit
# 启动服务
openclaw gateway
```

### 3. 运行技能

所有技能代码在 `skills/` 目录：

```bash
# 启用技能
openclaw config edit  # 在skills.enabled中添加技能名
openclaw restart
```

## 核心技能

| 技能名 | 功能 | 文件 |
|--------|------|------|
| summarize | 自动摘要 | `skills/summarize.js` |
| tagify | 自动标签分类 | `skills/tagify.js` |
| daily-report | 每日知识报告 | `skills/daily-report.js` |
| search | 语义检索 | `skills/search.js` |

## 系统要求

- Node.js 24+
- 内存 ≥ 4GB
- 磁盘 ≥ 10GB（用于记忆存储）
- Feishu开发者账号（用于文档集成）
- 可选：Ollama本地模型或OpenAI API

## 问题反馈

- 博客评论区：在博客原文底部留言
- GitHub Issues：[提交问题](https://github.com/kunpeng-ai-research/ai-research/issues)
- 官方文档：[https://docs.openclaw.ai](https://docs.openclaw.ai)

## 许可

本仓库内容采用 CC BY-NC-SA 4.0 协议。

---

**最后更新**: 2026-04-02  
**维护者**: 鲲鹏AI探索局
