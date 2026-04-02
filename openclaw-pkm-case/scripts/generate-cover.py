#!/usr/bin/env python3
"""
生成PKM案例封面图
尺寸: 1200×630 (博客标准)
"""

from PIL import Image, ImageDraw, ImageFont
import os

# 创建画布
width, height = 1200, 630
img = Image.new('RGB', (width, height), color=(225, 245, 254))  # 浅蓝色背景
draw = ImageDraw.Draw(img)

# 标题
title = "用OpenClaw构建个人知识管理系统"
subtitle = "从零到生产部署的完整实战指南"

# 尝试加载字体（需要系统有对应字体，否则用默认）
try:
    title_font = ImageFont.truetype("arial.ttf", 60)
    subtitle_font = ImageFont.truetype("arial.ttf", 36)
except:
    title_font = ImageFont.load_default()
    subtitle_font = ImageFont.load_default()

# 绘制标题
draw.text((60, 200), title, fill=(33, 150, 243), font=title_font)
draw.text((60, 280), subtitle, fill=(100, 100, 100), font=subtitle_font)

# 绘制装饰元素
draw.rectangle([60, 350, 1140, 352], fill=(33, 150, 243))

# 底部信息
info = "鲲鹏AI探索局 · OpenClaw实战案例"
draw.text((60, 380), info, fill=(150, 150, 150), font=subtitle_font)

# 保存
output_dir = os.path.dirname(os.path.abspath(__file__))
output_path = os.path.join(output_dir, "..", "images", "openclaw-pkm-cover.png")
os.makedirs(os.path.dirname(output_path), exist_ok=True)
img.save(output_path)

print(f"✅ 封面图已生成: {output_path}")
