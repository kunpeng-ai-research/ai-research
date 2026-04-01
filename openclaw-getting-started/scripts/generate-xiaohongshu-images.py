#!/usr/bin/env python3
"""
生成小红书配图（9张竖屏图，1080×1920）
每张图展示文章的一个关键部分
"""
from PIL import Image, ImageDraw, ImageFont
import os

def create_xiaohongshu_image(filename, title, content_lines, bg_color1, bg_color2):
    """创建单张小紅书配图"""
    width, height = 1080, 1920
    img = Image.new('RGB', (width, height), color=bg_color1)
    draw = ImageDraw.Draw(img)
    
    # 渐变背景
    for y in range(height):
        r = int(bg_color1[0] + (bg_color2[0] - bg_color1[0]) * y / height)
        g = int(bg_color1[1] + (bg_color2[1] - bg_color1[1]) * y / height)
        b = int(bg_color1[2] + (bg_color2[2] - bg_color1[2]) * y / height)
        draw.line([(0, y), (width, y)], fill=(r, g, b))
    
    # 标题
    try:
        font_title = ImageFont.truetype("arial.ttf", 72)
        font_content = ImageFont.truetype("arial.ttf", 48)
    except:
        font_title = ImageFont.load_default()
        font_content = ImageFont.load_default()
    
    # 绘制标题
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 200), title, font=font_title, fill=(255, 255, 255))
    
    # 绘制内容行
    y_offset = 400
    for line in content_lines:
        line_bbox = draw.textbbox((0, 0), line, font=font_content)
        line_width = line_bbox[2] - line_bbox[0]
        line_x = (width - line_width) // 2
        draw.text((line_x, y_offset), line, font=font_content, fill=(220, 220, 255))
        y_offset += 120
    
    # 底部标识
    draw.text((100, height-150), "鲲鹏AI探索局", font=font_content, fill=(180, 180, 220))
    draw.text((100, height-80), "扫码关注公众号", font=font_content, fill=(180, 180, 220))
    
    img.save(filename, 'PNG', optimize=True)
    print("[OK] Generated: {}".format(filename))

# 配色方案
colors = [
    ((30, 40, 80), (60, 80, 140)),   # 深蓝
    ((40, 60, 100), (80, 120, 180)), # 蓝色
    ((60, 30, 80), (120, 60, 140)),  # 紫色
    ((30, 60, 60), (60, 120, 120)),  # 青色
    ((60, 40, 30), (120, 80, 60)),   # 棕色
]

# 9张图的内容
slides = [
    ("OpenClaw是什么？", ["自托管AI网关", "20+聊天平台支持", "数据完全自控"], colors[0]),
    ("为什么选择OpenClaw？", ["隐私保护", "成本更低", "模型自由"], colors[1]),
    ("5分钟快速安装", ["curl安装脚本", "macOS/Linux/Windows", "自动配置"], colors[2]),
    ("配置AI Provider", ["OpenAI / Anthropic", "Google / Ollama", "随时切换"], colors[3]),
    ("连接Telegram", ["@BotFather", "创建Bot", "获取Token"], colors[4]),
    ("连接Discord", ["Developer Portal", "添加Bot", "邀请到服务器"], colors[0]),
    ("连接飞书", ["创建应用", "配置Webhook", "安装插件"], colors[1]),
    ("自定义助手", ["改名+头像", "System Prompt", "多平台差异化"], colors[2]),
    ("总结与进阶", ["自动化Cron", "自定义技能", "生产部署"], colors[3]),
]

output_dir = "D:/openclaw_workspace/2026-03-30-openclaw-getting-started"
os.makedirs(output_dir, exist_ok=True)

for i, (title, lines, (c1, c2)) in enumerate(slides, 1):
    filename = os.path.join(output_dir, "xiaohongshu_{:02d}.png".format(i))
    create_xiaohongshu_image(filename, title, lines, c1, c2)

print("\n[OK] All 9 images generated!")
