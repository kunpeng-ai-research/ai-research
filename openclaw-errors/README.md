<<<<<<< HEAD
# OpenClaw 入门指南 - 配套资源

本文档记录了 OpenClaw 完整入门指南的配套资源。

## 📁 项目结构

```
openclaw-errors/
├── articles/          # 各平台文章版本
│   ├── blog-article-zh.mdx    # 博客中文原文（MDX格式）
│   ├── blog-article-en.mdx    # 博客英文原文（MDX格式）
│   ├── zhihu-answer-v2.md     # 知乎精简版（待补充）
│   ├── wechat-article-v2.md   # 公众号版（待补充）
│   ├── csdn-article-v2.md     # CSDN技术版（待补充）
│   ├── devto-article.md       # Dev.to英文版（待补充）
│   ├── reddit-post.md         # Reddit帖子（待补充）
│   └── xiaohongshu-post.md    # 小红书图文（待补充）
├── images/           # 配图资源
│   ├── openclaw-getting-started-cover.png  # 博客封面图 1200×630
│   └── (其他配图待补充)
├── scripts/          # 生成脚本（待补充）
│   ├── generate-cover.py
│   └── generate-xiaohongshu-images.py
└── README.md         # 本文件

```

## 📖 文章说明

### 博客原文（已就绪）
- **blog-article-zh.mdx**: 中文完整版，约5000字，包含代码示例和配置说明
- **blog-article-en.mdx**: 英文完整版，约7000字，面向国际读者

### 待发布平台文章（需补充）
以下平台文章尚未完成，需要补充：
- 知乎（950字精简问答格式）
- 公众号（2000字+配图说明）
- CSDN（4000字技术深度版）
- Dev.to（英文技术社区）
- Reddit（r/LocalLLaMA讨论帖）
- 小红书（9张竖屏图文）

## 🖼️ 图片资源

### 已就绪
- 博客封面图：1200×630 PNG格式

### 待补充
- 公众号封面图（900×383）
- 小红书9张竖屏图（1080×1920）
- 技术架构图、性能对比表等

## 🔧 脚本工具

需要整理以下生成脚本（从历史项目中提取）：
- 封面图生成脚本
- 小红书图片生成脚本
- TTS配音生成脚本
- 视频合成脚本

## 📋 发布检查清单

- [x] 博客中文/英文已发布
- [ ] 知乎文章草稿完成
- [ ] 公众号文章草稿完成
- [ ] CSDN文章草稿完成
- [ ] Dev.to文章草稿完成
- [ ] Reddit帖子草稿完成
- [ ] 小红书图文草稿完成
- [ ] 所有配图准备就绪
- [ ] 生成脚本整理完成
- [ ] 推送到 kunpeng-ai-research/ai-research 仓库

## 📊 博客信息

- **博客中文**: https://kunpeng-ai.com/blog/openclaw-getting-started
- **博客英文**: https://kunpeng-ai.com/en/blog/en-openclaw-getting-started
- **GitHub仓库**: https://github.com/kunpeng-ai-research/ai-research
- **发布日期**: 2026-04-01
- **文章主题**: OpenClaw 完整入门指南

## ⚠️ 注意事项

1. **严禁私密文件上传**: 推送前必须检查 git status，确保无敏感信息
2. **结构化组织**: 文件必须按 categories 分类存放
3. **分工明确**: 博客主站只放MDX原文，配套资源放本仓库
4. **lang 字段规范**: 只能是 `zh` 或 `en`，不能使用 `zh-CN` 等

---

**创建时间**: 2026-04-01 18:41
**创建人**: 小鲲 (AI助手)
**状态**: 部分就绪，待补充内容
=======
# AI Research - 博客配套资源仓库

本仓库是 **鲲鹏AI探索局** 的博客配套资源总览，采用**子项目**形式组织，每篇博客对应一个子目录。

---

## 📚 子项目列表

### OpenClaw 入门指南
- **目录**: `openclaw-getting-started/`
- **博客**: https://kunpeng-ai.com/blog/openclaw-getting-started
- **内容**:
  - 完整安装配置教程（5分钟上手）
  - 支持 Telegram、Discord、飞书、WhatsApp 等 20+ 平台
  - 本地模型接入（Ollama）
  - 自动化与技能开发
- **配套资源**:
  - 各平台发布版本（知乎/公众号/CSDN/Reddit/小红书）
  - 封面图与配图
  - 图片生成脚本

---

## 🗂️ 子项目结构

每个子项目都包含以下结构：

```
项目名/
├── blog-article-zh.mdx      # 博客原文（中文）
├── blog-article-en.mdx      # 博客原文（英文）
├── articles/                # 各平台文章版本
│   ├── zhihu-answer-v2.md  # 知乎精简版
│   ├── wechat-article-v2.md # 公众号版
│   ├── csdn-article-v2.md  # CSDN版
│   ├── reddit-post.md      # Reddit帖子
│   └── xiaohongshu-post.md # 小红书图文
├── images/                  # 所有配图
│   ├── 封面图（1200×630）
│   └── 小红书竖屏图（1080×1920）
├── scripts/                 # 生成脚本
│   ├── generate-cover.py
│   └── generate-xiaohongshu-images.py
└── README.md                # 项目说明（可选）
```

---

## 🤝 贡献与反馈

本仓库内容采用 **CC BY-NC-SA 4.0** 协议，欢迎分享和引用。

- 发现错误？欢迎提 [Issue](https://github.com/kunpeng-ai-research/ai-research/issues)
- 有建议？欢迎提 [Pull Request](https://github.com/kunpeng-ai-research/ai-research/pulls)

---

## 🔗 相关链接

- **主站博客**: https://kunpeng-ai.com
- **GitHub 组织**: https://github.com/kunpeng-ai-research
- **OpenClaw 官方**: https://openclaw.ai

---

**最后更新**: 2026-03-31
**维护者**: 鲲鹏AI探索局
>>>>>>> 8fc664b5e1347d6ab43349cea85814bd29962fcb
