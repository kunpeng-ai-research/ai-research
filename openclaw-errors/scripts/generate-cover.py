#!/usr/bin/env python3
"""
生成博客封面图（第二期：OpenClaw常见错误）
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

# 绘制装饰图形（错误警告风格）
# 左上角感叹号
draw.ellipse([50, 50, 150, 150], fill=(255, 69, 0, 100))
# 右下角齿轮/工具
draw.ellipse([width-150, height-150, width-50, height-50], fill=(255, 69, 0, 100))

# 标题文字
title = "OpenClaw 常见错误与解决方案"
subtitle = "15+常见问题 | 完整排错指南 | 从安装到生产"

# 使用中文字体
font_paths = [
    "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
    "C:/Windows/Fonts/simhei.ttf",  # 黑体
    "C:/Windows/Fonts/arial.ttf",   # 回退
]

font_title = None
font_subtitle = None

for path in font_paths:
    try:
        font_title = ImageFont.truetype(path, 72)
        font_subtitle = ImageFont.truetype(path, 36)
        print(f"[OK] Using font: {path}")
        break
    except:
        continue

if font_title is None:
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
draw.text((50, height-50), "鲲鹏AI探索局 · OpenClaw故障排查指南", font=font_subtitle, fill=(180, 180, 220))

# 保存
output_dir = "D:/openclaw_workspace/2026-04-01-openclaw-errors"
os.makedirs(output_dir, exist_ok=True)
output_path = os.path.join(output_dir, "openclaw-errors-cover.png")
img.save(output_path, 'PNG', optimize=True)

print(f"[OK] 封面图已生成: {output_path}")
print(f"   尺寸: {width}x{height}")
