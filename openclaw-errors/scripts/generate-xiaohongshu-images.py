#!/usr/bin/env python3
"""
生成小红书配图（第二期：OpenClaw常见错误）
9张竖屏图，1080×1920
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
    
    # 加载中文字体
    font_paths = [
        "C:/Windows/Fonts/msyh.ttc",  # 微软雅黑
        "C:/Windows/Fonts/simhei.ttf",
        "C:/Windows/Fonts/arial.ttf",
    ]
    
    font_title = None
    font_content = None
    
    for path in font_paths:
        try:
            font_title = ImageFont.truetype(path, 68)
            font_content = ImageFont.truetype(path, 42)
            print(f"[OK] Using font: {path}")
            break
        except:
            continue
    
    if font_title is None:
        font_title = ImageFont.load_default()
        font_content = ImageFont.load_default()
    
    # 绘制标题
    title_bbox = draw.textbbox((0, 0), title, font=font_title)
    title_width = title_bbox[2] - title_bbox[0]
    title_x = (width - title_width) // 2
    draw.text((title_x, 180), title, font=font_title, fill=(255, 255, 255))
    
    # 绘制内容行
    y_offset = 350
    for line in content_lines:
        line_bbox = draw.textbbox((0, 0), line, font=font_content)
        line_width = line_bbox[2] - line_bbox[0]
        line_x = (width - line_width) // 2
        draw.text((line_x, y_offset), line, font=font_content, fill=(220, 220, 255))
        y_offset += 110
    
    # 底部标识
    draw.text((80, height-180), "鲲鹏AI探索局", font=font_content, fill=(180, 180, 220))
    draw.text((80, height-100), "扫码关注公众号", font=font_content, fill=(180, 180, 220))
    
    img.save(filename, 'PNG', optimize=True)
    print(f"[OK] Generated: {filename}")

# 配色方案（错误警示风格）
colors = [
    ((40, 30, 30), (80, 50, 50)),   # 深红
    ((30, 40, 30), (50, 80, 50)),   # 深绿
    ((30, 30, 40), (50, 50, 80)),   # 深蓝
    ((40, 30, 40), (80, 50, 80)),   # 紫色
    ((40, 40, 30), (80, 80, 50)),   # 棕色
]

# 9张图内容（常见错误主题）
slides = [
    ("安装错误1：下载失败", ["国内访问慢", "用淘宝npm镜像", "curl -k 跳过SSL"], colors[0]),
    ("安装错误2：Node版本", ["必须Node.js 24+", "nvm install 24", "nvm use 24"], colors[1]),
    ("安装错误3：PowerShell", ["执行策略限制", "Set-ExecutionPolicy", "RemoteSigned"], colors[2]),
    ("配置错误1：API Key", ["格式sk-开头", "无空格无换行", "官网测试curl"], colors[3]),
    ("配置错误2：JSON语法", ["运行openclaw config validate", "用jsonlint.com校验", "修复后重启"], colors[4]),
    ("运行错误1：端口占用", ["8080被占用", "netstat查找进程", "kill或改端口8081"], colors[0]),
    ("运行错误2：消息收不到", ["检查网关状态", "Bot是否在线", "查看日志logs --follow"], colors[1]),
    ("飞书集成失败", ["域名需备案", "HTTPS证书有效", "Nginx反向代理"], colors[2]),
    ("常见问题汇总", ["15+错误解决方案", "完整博客有详细指南", "持续更新中"], colors[3]),
]

output_dir = "D:/openclaw_workspace/2026-04-01-openclaw-errors/images"
os.makedirs(output_dir, exist_ok=True)

for i, (title, lines, (c1, c2)) in enumerate(slides, 1):
    filename = os.path.join(output_dir, f"xiaohongshu_{i:02d}.png")
    create_xiaohongshu_image(filename, title, lines, c1, c2)

print("\n[OK] All 9 Xiaohongshu images generated!")
