#!/usr/bin/env python3
"""
生成博客封面图
尺寸: 1200×630
"""
from PIL import Image, ImageDraw, ImageFont
import os

# 创建画布
width, height = 1200, 630
img = Image.new('RGB', (width, height), color=(30, 30, 40))
draw = ImageDraw.Draw(img)

# 绘制渐变背景
for y in range(height):
    r = int(30 + (60 - 30) * y / height)
    g = int(30 + (80 - 30) * y / height)
    b = int(40 + (120 - 40) * y / height)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# 绘制装饰图形（模拟OpenClaw lobster风格）
draw.ellipse([50, 50, 200, 200], fill=(255, 69, 0, 128))
draw.ellipse([width-200, height-200, width-50, height-50], fill=(255, 69, 0, 128))

# 标题文字
title = "OpenClaw Getting Started"
subtitle = "5分钟搭建你的个人AI助手"

# 使用默认字体
try:
    font_large = ImageFont.truetype("arial.ttf", 72)
    font_small = ImageFont.truetype("arial.ttf", 36)
except:
    font_large = ImageFont.load_default()
    font_small = ImageFont.load_default()

# 计算文字位置
text_bbox = draw.textbbox((0, 0), title, font=font_large)
text_width = text_bbox[2] - text_bbox[0]
text_x = (width - text_width) // 2
text_y = height // 2 - 50

# 绘制文字阴影
draw.text((text_x+2, text_y+2), title, font=font_large, fill=(0, 0, 0, 128))
draw.text((text_x, text_y), title, font=font_large, fill=(255, 255, 255))

# 副标题
sub_bbox = draw.textbbox((0, 0), subtitle, font=font_small)
sub_width = sub_bbox[2] - sub_bbox[0]
sub_x = (width - sub_width) // 2
draw.text((sub_x, text_y + 100), subtitle, font=font_small, fill=(200, 200, 255))

# 底部标识
draw.text((50, height-50), "鲲鹏AI探索局 · OpenClaw入门指南", font=font_small, fill=(150, 150, 200))

# 保存
output_dir = "D:/openclaw_workspace/2026-03-30-openclaw-getting-started"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "openclaw-getting-started-cover.png")
img.save(output_path, 'PNG', optimize=True)

print("[OK] 封面图已生成: {}".format(output_path))
print("   尺寸: {}x{}".format(width, height))
