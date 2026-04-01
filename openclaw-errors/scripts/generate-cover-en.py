#!/usr/bin/env python3
"""
生成博客封面图（第二期：OpenClaw常见错误）- 英文版
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
    r = int(30 + (80 - 30) * y / height)
    g = int(30 + (40 - 30) * y / height)
    b = int(40 + (120 - 40) * y / height)
    draw.line([(0, y), (width, y)], fill=(r, g, b))

# 绘制装饰图形
draw.ellipse([50, 50, 150, 150], fill=(255, 69, 0, 100))
draw.ellipse([width-150, height-150, width-50, height-50], fill=(255, 69, 0, 100))

# 标题文字
title = "OpenClaw Common Errors & Solutions"
subtitle = "15+ Issues Covered | Complete Troubleshooting Guide"

# 使用英文字体
try:
    font_title = ImageFont.truetype("arial.ttf", 60)
    font_subtitle = ImageFont.truetype("arial.ttf", 30)
except:
    font_title = ImageFont.load_default()
    font_subtitle = ImageFont.load_default()

# 绘制标题阴影
text_bbox = draw.textbbox((0, 0), title, font=font_title)
text_width = text_bbox[2] - text_bbox[0]
text_x = (width - text_width) // 2
text_y = height // 2 - 60

draw.text((text_x+3, text_y+3), title, font=font_title, fill=(0, 0, 0, 150))
draw.text((text_x, text_y), title, font=font_title, fill=(255, 255, 255))

# 副标题
sub_bbox = draw.textbbox((0, 0), subtitle, font=font_subtitle)
sub_width = sub_bbox[2] - sub_bbox[0]
sub_x = (width - sub_width) // 2
draw.text((sub_x, text_y + 90), subtitle, font=font_subtitle, fill=(255, 200, 100))

# 底部标识
draw.text((50, height-50), "Kunpeng AI Research · OpenClaw Troubleshooting", font=font_subtitle, fill=(180, 180, 220))

# 保存
output_dir = "D:/openclaw_workspace/2026-04-01-openclaw-errors"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "openclaw-errors-cover-en.png")
img.save(output_path, 'PNG', optimize=True)

print(f"[OK] English cover generated: {output_path}")
print(f"    Size: {width}x{height}")
