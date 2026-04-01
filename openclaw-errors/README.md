# OpenClaw 错误处理与调试 - 配套资源

本文档记录了 OpenClaw 错误处理与调试相关的内容的配套资源。

## 📁 项目结构

```
openclaw-errors/
├── articles/          # 各平台文章版本
│   ├── zhihu-answer-v2.md     # 知乎精简版
│   ├── wechat-article-v2.md   # 公众号版
│   ├── csdn-article-v2.md     # CSDN技术版
│   ├── devto-article.md       # Dev.to英文版
│   ├── reddit-post.md         # Reddit帖子
│   └── xiaohongshu-post.md    # 小红书图文
├── images/           # 配图资源
│   ├── openclaw-getting-started-cover.png  # 博客封面图 1200×630
│   ├── openclaw-errors-cover.png           # 本主题封面
│   ├── openclaw-errors-cover-en.png       # 英文封面
│   ├── xiaohongshu_01.png ~ xiaohongshu_09.png  # 9张竖屏图
│   └── (其他配图)
├── scripts/          # 生成脚本
│   ├── generate-cover.py
│   ├── generate-cover-en.py
│   └── generate-xiaohongshu-images.py
├── docs/             # 研究文档
│   └── openclaw-errors-research.md
└── README.md         # 本文件

```

## 📖 文章说明

### 平台文章（已就绪）
- **zhihu-answer-v2.md**: 知乎精简版（950字问答格式）
- **wechat-article-v2.md**: 公众号版（2000字+配图说明）
- **csdn-article-v2.md**: CSDN技术版（4000字，技术关键词前置）
- **devto-article.md**: Dev.to英文技术社区版
- **reddit-post.md**: Reddit讨论帖（r/LocalLLaMA）
- **xiaohongshu-post.md**: 小红书合规图文

**注意**: 博客原文（blog-article-zh.mdx / blog-article-en.mdx）位于 `../openclaw-getting-started/` 目录，不应在此重复。

## 🖼️ 图片资源

### 已就绪
- 博客封面图：1200×630 PNG
- 本主题封面：中文版 + 英文版
- 小红书9张竖屏图：1080×1920 PNG

## 🔧 脚本工具

- **generate-cover.py**: 生成中文封面图
- **generate-cover-en.py**: 生成英文封面图
- **generate-xiaohongshu-images.py**: 生成小红书9张竖屏图

## 📋 发布检查清单

- [x] 博客中文/英文已发布（在 openclaw-getting-started/）
- [x] 各平台文章草稿完成
- [x] 所有配图准备就绪
- [x] 生成脚本整理完成
- [x] 推送到 kunpeng-ai-research/ai-research 仓库
- [ ] 知乎发布
- [ ] 公众号发布
- [ ] CSDN发布
- [ ] Dev.to发布
- [ ] Reddit发布
- [ ] 小红书发布

## 📊 相关信息

- **博客中文**: https://kunpeng-ai.com/blog/openclaw-getting-started
- **博客英文**: https://kunpeng-ai.com/en/blog/en-openclaw-getting-started
- **GitHub仓库**: https://github.com/kunpeng-ai-research/ai-research
- **发布日期**: 2026-04-01
- **主题**: OpenClaw 错误处理与调试

## ⚠️ 注意事项

1. **严禁私密文件上传**: 推送前必须检查 git status，确保无敏感信息
2. **结构化组织**: 文件必须按 categories 分类存放
3. **分工明确**: 博客原文只在 `openclaw-getting-started/`，本目录只放配套资源
4. **lang 字段规范**: 平台文章使用 `zh` 或 `en`，不能使用 `zh-CN` 等

---

**创建时间**: 2026-04-01 18:41
**创建人**: 小鲲 (AI助手)
**状态**: 资源就绪，待平台发布