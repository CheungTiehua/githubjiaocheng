#!/usr/bin/env python3
"""GitHub 截图标注工具 — 画框、写字、画箭头，支持中文字体。"""

import argparse
import json
import sys
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

# ── 中文字体路径（按优先级查找） ──
def find_font(size: int) -> ImageFont.FreeTypeFont:
    candidates = [
        # Windows
        "C:/Windows/Fonts/msyh.ttc",        # 微软雅黑
        "C:/Windows/Fonts/msyhbd.ttc",      # 微软雅黑粗体
        "C:/Windows/Fonts/simhei.ttf",      # 黑体
        "C:/Windows/Fonts/simsun.ttc",      # 宋体
        "C:/Windows/Fonts/simkai.ttf",      # 楷体
        # macOS
        "/System/Library/Fonts/PingFang.ttc",
        "/System/Library/Fonts/STHeiti Light.ttc",
        # Linux
        "/usr/share/fonts/truetype/wqy/wqy-microhei.ttc",
        "/usr/share/fonts/truetype/droid/DroidSansFallbackFull.ttf",
    ]
    for path in candidates:
        if Path(path).exists():
            return ImageFont.truetype(path, size)
    # fallback: Pillow 默认字体（不支持中文）
    print("⚠ 警告：找不到中文字体，标注文字可能显示为方框", file=sys.stderr)
    return ImageFont.load_default()


FONT_SIZES = {"small": 18, "medium": 24, "large": 32}
COLOR_MAP = {
    "red":    (220, 40, 40),
    "green":  (40, 180, 40),
    "blue":   (40, 80, 220),
    "yellow": (220, 180, 20),
    "orange": (240, 140, 20),
    "white":  (255, 255, 255),
    "black":  (0, 0, 0),
}


def hex_to_rgb(hex_color: str) -> tuple:
    hex_color = hex_color.lstrip("#")
    return tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))


def apply_annotation(draw: ImageDraw.ImageDraw, ann: dict, font: ImageFont.FreeTypeFont) -> None:
    x, y, w, h = ann["x"], ann["y"], ann["w"], ann["h"]
    label = ann.get("label", "")
    color_str = ann.get("color", "red")
    color = hex_to_rgb(color_str) if color_str.startswith("#") else COLOR_MAP.get(color_str, COLOR_MAP["red"])
    line_width = ann.get("width", 3)
    font_size = FONT_SIZES.get(ann.get("font_size", "medium"), 24)
    arrow = ann.get("arrow", False)

    if font.size != font_size:
        font = find_font(font_size)

    # 画矩形框
    draw.rectangle([x, y, x + w, y + h], outline=color, width=line_width)

    # 写字（框的右上方）
    if label:
        bbox = draw.textbbox((0, 0), label, font=font)
        tw, th = bbox[2] - bbox[0], bbox[3] - bbox[1]
        # 标签放在框的右上方
        lx = x + w + 8
        ly = y - th - 4
        # 如果超出图片右边界，放到框下方
        img_w = draw.im.size[0] if hasattr(draw.im, "size") else 9999
        if lx + tw > img_w:
            lx = x
            ly = y + h + 4
        # 白色背景 + 文字
        pad = 3
        draw.rectangle([lx - pad, ly - pad, lx + tw + pad, ly + th + pad], fill=(255, 255, 255, 220))
        draw.text((lx, ly), label, fill=color, font=font)

    # 画箭头（从框下方指向框）
    if arrow:
        ax, ay = x + w // 2, y + h + 4
        bx, by = x + w // 2, y + h + 30
        draw.line([ax, ay, bx, by], fill=color, width=line_width)
        # 箭头尖
        draw.polygon([(bx, by), (bx - 6, by - 10), (bx + 6, by - 10)], fill=color)


def main():
    # Windows 终端 UTF-8 兼容
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

    parser = argparse.ArgumentParser(description="GitHub 截图标注工具")
    parser.add_argument("input", help="输入截图路径")
    parser.add_argument("output", help="输出标注后图片路径")
    parser.add_argument("--annotations", "-a", type=str, default="[]",
                        help='JSON 标注数组，例: \'[{"x":100,"y":200,"w":50,"h":30,"label":"按钮"}]\'')
    parser.add_argument("--file", "-f", type=str,
                        help="从 JSON 文件读取标注")
    args = parser.parse_args()

    # 读取标注
    if args.file:
        annotations = json.loads(Path(args.file).read_text(encoding="utf-8"))
    else:
        annotations = json.loads(args.annotations)

    if not annotations:
        print("错误：没有标注数据。用 --annotations 或 --file 传入。", file=sys.stderr)
        sys.exit(1)

    # 打开图片
    img = Image.open(args.input).convert("RGBA")
    draw = ImageDraw.Draw(img)
    font = find_font(FONT_SIZES["medium"])

    # 应用所有标注
    for i, ann in enumerate(annotations):
        try:
            apply_annotation(draw, ann, font)
        except Exception as e:
            print(f"⚠ 第 {i+1} 个标注出错: {e}", file=sys.stderr)

    # 保存
    Path(args.output).parent.mkdir(parents=True, exist_ok=True)
    img.save(args.output)
    print(f"✅ 已保存: {args.output} ({len(annotations)} 个标注)")


if __name__ == "__main__":
    main()
