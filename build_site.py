#!/usr/bin/env python3
"""GitHub 中文教程 — 静态网站构建脚本。
用法: python build_site.py
输出: site/ 目录（index.html + 15 课 HTML + CSS + 截图 + 参考文档）
"""

import re, sys, io, shutil
from pathlib import Path
from markdown import markdown
from jinja2 import Environment, FileSystemLoader

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")

ROOT = Path(__file__).parent
LESSONS = ROOT / "lessons"
ASSETS = ROOT / "assets"
REFERENCE = ROOT / "reference"
TEMPLATE = ROOT / "template"
SITE = ROOT / "docs"

# ── 课程元信息 ──
LESSON_META = [
    {"num": 1,  "short_title": "注册与基础设置",       "duration": "25min", "p0_count": "19"},
    {"num": 2,  "short_title": "读代码（上）— 仓库主页",  "duration": "25min", "p0_count": "21"},
    {"num": 3,  "short_title": "读代码（下）— 文件与历史",  "duration": "25min", "p0_count": "17"},
    {"num": 4,  "short_title": "Issue（上）— 创建与管理",  "duration": "25min", "p0_count": "18"},
    {"num": 5,  "short_title": "Issue（下）— 高级功能",    "duration": "25min", "p0_count": "12"},
    {"num": 6,  "short_title": "PR：Fork 与 Clone",       "duration": "30min", "p0_count": "16"},
    {"num": 7,  "short_title": "PR：创建 Pull Request",   "duration": "25min", "p0_count": "14"},
    {"num": 8,  "short_title": "PR：生命周期与合并",        "duration": "30min", "p0_count": "18"},
    {"num": 9,  "short_title": "Code Review",             "duration": "25min", "p0_count": "14"},
    {"num": 10, "short_title": "Actions/CI（上）— 概念",   "duration": "25min", "p0_count": "15"},
    {"num": 11, "short_title": "Actions/CI（下）— 日志",   "duration": "25min", "p0_count": "13"},
    {"num": 12, "short_title": "项目管理（上）— Projects",  "duration": "20min", "p0_count": "11"},
    {"num": 13, "short_title": "项目管理（下）— Wiki等",    "duration": "20min", "p0_count": "12"},
    {"num": 14, "short_title": "安全与权限",               "duration": "25min", "p0_count": "14"},
    {"num": 15, "short_title": "附录：速查手册",            "duration": "20min", "p0_count": "170+"},
]

# ── Markdown 预处理：自动匹配截图 ──
def inject_screenshots(md_text: str, lesson_num: int) -> str:
    """为每课的 **画面**：和 **操作演示**：标记后插入对应截图。"""
    lesson_str = f"{lesson_num:02d}"
    lesson_asset_dir = ASSETS / lesson_str
    if not lesson_asset_dir.exists():
        return md_text

    all_imgs = sorted(lesson_asset_dir.glob("*.png"))
    annotated = {p.stem.replace("-annotated", ""): p for p in all_imgs if "-annotated" in p.stem}
    regular = {p.stem: p for p in all_imgs if "-annotated" not in p.stem}
    candidates = list(annotated.values()) + [p for s, p in regular.items() if s not in annotated]

    img_idx = 0
    def insert_img(match):
        nonlocal img_idx
        if img_idx < len(candidates):
            img_path = candidates[img_idx]
            rel_path = f"assets/{lesson_str}/{img_path.name}"
            img_idx += 1
            return match.group(0) + f'\n\n![{img_path.stem}]({rel_path})\n'
        return match.group(0)

    md_text = re.sub(r'^\*\*(?:画面|操作演示)\*\*：.*$', insert_img, md_text, flags=re.MULTILINE)
    return md_text


def convert_markdown(md_text: str, lesson_num: int) -> str:
    """Markdown → HTML，附加课程特定处理。"""
    md_text = inject_screenshots(md_text, lesson_num)

    # 自定义扩展：术语表加 CSS class
    md_text = md_text.replace("## 本课术语速查", "## 本课术语速查\n{.glossary-table}")

    html = markdown(md_text, extensions=["tables", "fenced_code", "codehilite", "nl2br", "attr_list"])
    return html


def build_lesson(env, meta: dict, prev_meta=None, next_meta=None):
    """构建一课的 HTML。"""
    num = meta["num"]
    md_path = LESSONS / f"{num:02d}-{meta['short_title'].split('—')[0].strip().replace(' ','-')}.md"
    # 如果上面的路径不存在，尝试 glob 匹配
    if not md_path.exists():
        candidates = list(LESSONS.glob(f"{num:02d}-*.md"))
        if candidates:
            md_path = candidates[0]
        else:
            print(f"  ✗ 找不到第 {num} 课文件")
            return

    md_text = md_path.read_text(encoding="utf-8")
    content = convert_markdown(md_text, num)

    # 提取标题
    title_match = re.search(r'<h1>(.+?)</h1>', content)
    title = title_match.group(1) if title_match else f"第 {num:02d} 课"

    template = env.get_template("lesson.html")
    html = template.render(
        title=title,
        content=content,
        current=num,
        lessons=LESSON_META,
        meta=f"第{num:02d}课 · {meta['duration']} · {meta['p0_count']} 词条",
        prev_num=prev_meta["num"] if prev_meta else 0,
        prev_title=prev_meta["short_title"] if prev_meta else "",
        next_num=next_meta["num"] if next_meta else 0,
        next_title=next_meta["short_title"] if next_meta else "",
    )

    out_path = SITE / f"lesson-{num:02d}.html"
    out_path.write_text(html, encoding="utf-8")
    print(f"  ✓ lesson-{num:02d}.html")


def build_reference_page(env, md_name: str, html_name: str, title: str):
    """构建参考文档页。"""
    md_path = REFERENCE / md_name
    if not md_path.exists():
        print(f"  ✗ 参考文档不存在: {md_name}")
        return

    md_text = md_path.read_text(encoding="utf-8")
    html_body = markdown(md_text, extensions=["tables", "fenced_code", "codehilite", "attr_list"])

    template = env.get_template("lesson.html")
    html = template.render(
        title=title,
        content=html_body,
        current=-1,
        lessons=LESSON_META,
        meta="参考文档",
        prev_num=0, prev_title="",
        next_num=0, next_title="",
    )

    out_path = SITE / html_name
    out_path.write_text(html, encoding="utf-8")
    print(f"  ✓ {html_name}")


def build_index(env):
    """构建首页。"""
    template = env.get_template("index.html")
    html = template.render(lessons=LESSON_META)
    (SITE / "index.html").write_text(html, encoding="utf-8")
    print("  ✓ index.html")


def main():
    # 清空输出目录
    if SITE.exists():
        shutil.rmtree(SITE)
    SITE.mkdir()

    # 复制 CSS / JS
    shutil.copy(TEMPLATE / "style.css", SITE / "style.css")
    shutil.copy(TEMPLATE / "chatbox.css", SITE / "chatbox.css")
    shutil.copy(TEMPLATE / "chatbox.js", SITE / "chatbox.js")
    print("  ✓ style.css + chatbox")

    # 复制截图目录
    if ASSETS.exists():
        dest = SITE / "assets"
        shutil.copytree(ASSETS, dest)
        print("  ✓ assets/ (截图)")

    # Jinja2 环境
    env = Environment(loader=FileSystemLoader(str(TEMPLATE)))

    # 构建首页
    print("\n[构建首页]")
    build_index(env)

    # 构建所有课程
    print("\n[构建课程]")
    for i, meta in enumerate(LESSON_META):
        prev_meta = LESSON_META[i - 1] if i > 0 else None
        next_meta = LESSON_META[i + 1] if i < len(LESSON_META) - 1 else None
        build_lesson(env, meta, prev_meta, next_meta)

    # 构建参考文档
    print("\n[构建参考文档]")
    ref_pages = [
        ("glossary.md", "glossary.html", "术语中英对照表"),
        ("faq.md", "faq.html", "常见问题 FAQ"),
        ("scenario-first-contribution.md", "scenario-first-contribution.html", "场景: 第一次贡献代码"),
        ("scenario-team-workflow.md", "scenario-team-workflow.html", "场景: 团队协作日常"),
        ("scenario-maintainer.md", "scenario-maintainer.html", "场景: 维护开源项目"),
        ("common-errors.md", "common-errors.html", "常见报错及解决"),
        ("keyboard-shortcuts.md", "keyboard-shortcuts.html", "快捷键大全"),
        ("recommended-settings.md", "recommended-settings.html", "推荐设置清单"),
    ]
    for md_name, html_name, title in ref_pages:
        build_reference_page(env, md_name, html_name, title)

    print(f"\n✅ 网站构建完成: {SITE}")
    print(f"   打开 {SITE / 'index.html'} 即可浏览")


if __name__ == "__main__":
    main()
