#!/usr/bin/env python3
"""GitHub 课程全自动截图+标注工具。
用法: python screenshot_course.py --lesson 02 --annotate
      python screenshot_course.py --all --annotate"""

import argparse, json, sys, io, time, subprocess
from pathlib import Path
from playwright.sync_api import sync_playwright

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
COURSE_ROOT = Path(__file__).parent
ASSETS = COURSE_ROOT / "assets"

# ── GitHub 常用元素选择器 ──
S = {
    "star_btn": 'button[aria-label*="Star"]',
    "fork_btn": 'button[aria-label*="Fork"]',
    "code_btn": 'button:has-text("Code")',
    "repo_name": 'strong.mr-2 a, h1 strong a',
    "public_badge": '.Label--secondary',
    "tab_code": 'a[href*="/fastapi"]',
    "tab_issues": 'a#issues-tab',
    "tab_pr": 'a#pull-requests-tab',
    "tab_actions": 'a#actions-tab',
    "tab_wiki": 'a#wiki-tab',
    "tab_security": 'a#security-tab',
    "tab_settings": 'a[href*="/settings"]',
    "tab_projects": 'a#projects-tab',
    "branch_menu": '#branch-picker-repos-header-ref-selector',
    "file_list": '[role="grid"]',
    "raw_btn": 'a:has-text("Raw")',
    "blame_btn": 'a:has-text("Blame")',
    "history_btn": 'a:has-text("History")',
    "readme_area": 'article.markdown-body',
    "about_section": 'h2:has-text("About")',
    "languages_bar": '.progress-bar',
    "new_issue_btn": 'a:has-text("New issue")',
    "issue_labels": 'a[href*="/labels"]',
    "issue_milestones": 'a[href*="/milestones"]',
    "comments_section": '#discussion_bucket',
    "right_sidebar": '.BorderGrid',
}

REPO = "https://github.com/tiangolo/fastapi"

# ── 全课程页面配置（每页配标注）──
AD = "https://github.com/ant-design/ant-design"
PAGES = {
    "01": [
        {"n": "01-homepage",     "u": "https://github.com",
         "a": [{"s": 'a[href="/signup"]', "l": "Sign up 注册", "c": "red"},
               {"s": 'a[href="/login"]',  "l": "Sign in 登录", "c": "green"},
               {"s": 'input[type="email"],input[name="user[email]"]', "l": "输入邮箱即可注册", "c": "yellow", "opt": True}]},
        {"n": "02-signup",       "u": "https://github.com/signup",
         "a": [{"s": 'input#email,input[name="user[email]"]', "l": "Email 邮箱", "c": "red", "opt": True},
               {"s": 'input#password,input[name="user[password]"]', "l": "Password 密码", "c": "green", "opt": True},
               {"s": 'input#login,input[name="user[login]"]', "l": "Username 用户名", "c": "blue", "opt": True}]},
    ],
    "02": [
        {"n": "01-repo-home",   "u": REPO,
         "a": [{"s": "repo_name",    "l": "仓库名 owner/repo", "c": "red"},
               {"s": "star_btn",     "l": "Star 收藏", "c": "yellow"},
               {"s": "fork_btn",     "l": "Fork 复刻", "c": "orange"},
               {"s": "tab_issues",   "l": "Issues 议题", "c": "blue"},
               {"s": "tab_pr",       "l": "Pull requests", "c": "blue"}]},
        {"n": "02-code-dropdown","u": REPO,
         "ac": [{"click": "button:has-text('Code')"}, {"w": 800}],
         "a": [{"s": "text=Download ZIP", "l": "Download ZIP 下载源码", "c": "red"}]},
        {"n": "03-file-list",   "u": REPO,
         "a": [{"s": "branch_menu", "l": "分支选择", "c": "red"},
               {"s": "file_list",   "l": "文件列表", "c": "yellow"},
               {"s": "readme_area", "l": "README 说明文档", "c": "green", "opt": True}]},
        {"n": "04-right-panel", "u": REPO,
         "ac": [{"scroll_to": ".BorderGrid"}],
         "a": [{"s": "about_section",  "l": "About 项目简介", "c": "red"},
               {"s": "languages_bar",  "l": "编程语言占比", "c": "green"}]},
        {"n": "05-readme",      "u": REPO,
         "ac": [{"scroll_to": "article.markdown-body"}],
         "a": [{"s": "readme_area",   "l": "README 项目文档", "c": "red"}]},
    ],
    "03": [
        {"n": "01-file-view",   "u": f"{REPO}/blob/main/pyproject.toml",
         "a": [{"s": "raw_btn",     "l": "Raw 原始代码", "c": "red"},
               {"s": "blame_btn",   "l": "Blame 逐行追溯", "c": "green"},
               {"s": "history_btn", "l": "History 历史记录", "c": "blue"}]},
        {"n": "02-blame-view",  "u": f"{REPO}/blame/main/pyproject.toml", "ac": [{"w": 1000}],
         "a": [{"s": "div.BorderGrid", "l": "左边: 作者/时间/CommitSHA", "c": "red"}]},
        {"n": "03-commits-list","u": f"{REPO}/commits/main",
         "a": [{"s": "ol,div.TimelineItem", "l": "提交历史列表", "c": "red"}]},
        {"n": "04-releases",    "u": f"{REPO}/releases",
         "a": [{"s": "a[href*='/releases/tag']", "l": "版本号 (如 v1.0)", "c": "red"}]},
    ],
    "04": [
        {"n": "01-issues-list", "u": f"{REPO}/issues",
         "a": [{"s": "new_issue_btn", "l": "New issue 新建议题", "c": "red"},
               {"s": "issue_labels",  "l": "Labels 标签管理", "c": "green"},
               {"s": "issue_milestones","l": "Milestones 里程碑", "c": "blue"}]},
        {"n": "02-issue-detail","u": f"{REPO}/issues/1",
         "a": [{"s": "right_sidebar","l": "Assignees/Labels/Milestone", "c": "red"},
               {"s": "comments_section","l": "评论区", "c": "green"}]},
    ],
    "05": [
        {"n": "01-template-choose","u": f"{AD}/issues/new/choose",
         "a": [{"s": "text=Bug Report", "l": "Bug 报告模板", "c": "red"},
               {"s": "text=Feature Request", "l": "功能请求模板", "c": "green"}]},
        {"n": "02-labels-page",  "u": f"{AD}/labels",
         "a": [{"s": "a[href*='labels/bug']", "l": "bug 标签(红色)", "c": "red", "opt": True},
               {"s": "a:has-text('New label')", "l": "创建新标签", "c": "green"}]},
        {"n": "03-milestones",   "u": f"{AD}/milestones",
         "a": [{"s": "a:has-text('New milestone')", "l": "新建里程碑", "c": "red"}]},
    ],
    "06": [
        {"n": "01-fork-btn",    "u": REPO,
         "a": [{"s": "fork_btn", "l": "Fork 复刻按钮", "c": "red"},
               {"s": "star_btn", "l": "Star 收藏 (Fork左边)", "c": "yellow"}]},
        {"n": "02-code-ssh",    "u": REPO,
         "ac": [{"click": "button:has-text('Code')"}, {"w": 800}],
         "a": [{"s": "text=HTTPS", "l": "HTTPS 地址", "c": "red"},
               {"s": "text=SSH",   "l": "SSH 地址 (免密)", "c": "green"}]},
    ],
    "07": [
        {"n": "01-compare",     "u": f"{REPO}/compare",
         "a": [{"s": "summary:has-text('main'),#branch-picker-repos-header-ref-selector", "l": "Base 目标分支", "c": "red", "opt": True},
               {"s": ".flex-auto h3, #compare-page h1", "l": "Compare 对比页面", "c": "green"}]},
    ],
    "08": [
        {"n": "01-pr-page",     "u": f"{REPO}/pull/1",
         "a": [{"s": "tab_pr",      "l": "Conversation 讨论", "c": "blue"},
               {"s": "#files_tab_counter", "l": "Files changed 文件改动", "c": "green", "opt": True}]},
        {"n": "02-pr-files",    "u": f"{REPO}/pull/1/files",
         "a": [{"s": ".file-info a, [data-file-list]", "l": "改动的文件列表", "c": "red", "opt": True}]},
        {"n": "03-pr-commits",  "u": f"{REPO}/pull/1/commits",
         "a": [{"s": "ol,div.TimelineItem", "l": "PR中的提交列表", "c": "red"}]},
    ],
    "09": [
        {"n": "01-review-files","u": f"{REPO}/pull/1/files",
         "a": [{"s": "button:has-text('Review changes')", "l": "Review changes 提交审查", "c": "red"},
               {"s": "button:has-text('Viewed')", "l": "Viewed 标记已看", "c": "green", "opt": True}]},
    ],
    "10": [
        {"n": "01-actions-list","u": f"{REPO}/actions",
         "a": [{"s": "a[href*='/actions/workflows']", "l": "Workflow 工作流列表", "c": "red"}]},
        {"n": "02-marketplace", "u": "https://github.com/marketplace?type=actions",
         "a": [{"s": "input[aria-label*='Search']", "l": "搜索 Actions", "c": "red"}]},
    ],
    "11": [
        {"n": "01-actions-run", "u": f"{REPO}/actions",
         "a": [{"s": ".Box-row,div[data-hovercard-type='workflow_run']", "l": "运行历史记录", "c": "red"}]},
    ],
    "12": [
        {"n": "01-projects",    "u": f"{REPO}/projects",
         "a": [{"s": "a:has-text('New project')", "l": "新建项目看板", "c": "red"}]},
    ],
    "13": [
        {"n": "01-releases",    "u": f"{REPO}/releases",
         "a": [{"s": "a:has-text('Create a new release')", "l": "创建新 Release", "c": "red"},
               {"s": ".release-title,h2", "l": "已发布版本列表", "c": "green"}]},
        {"n": "02-wiki",        "u": f"{REPO}/wiki",
         "a": [{"s": "a:has-text('Create the first page'),text=New Page", "l": "新建 Wiki 页面", "c": "red", "opt": True},
               {"s": "text=Pages", "l": "侧边栏: 页面列表", "c": "green", "opt": True}]},
    ],
    "14": [
        {"n": "01-settings-branches","u": f"{REPO}/settings/branches",
         "a": [{"s": "text=Add branch protection rule", "l": "添加分支保护规则", "c": "red"},
               {"s": "text=Branch protection rules", "l": "已有保护规则列表", "c": "green"}]},
        {"n": "02-security",    "u": f"{REPO}/security",
         "a": [{"s": "text=Dependabot", "l": "Dependabot 依赖警报", "c": "red"},
               {"s": "text=Secret scanning", "l": "Secret scanning 密钥扫描", "c": "green"}]},
    ],
}


def run_annotate(inp: Path, out: Path, anns: list):
    if not anns: return
    r = subprocess.run(["python", str(COURSE_ROOT/"annotate.py"), str(inp), str(out),
         "--annotations", json.dumps(anns, ensure_ascii=False)],
         capture_output=True, text=True, encoding="utf-8", errors="replace")
    if r.returncode == 0:
        print(f" +{len(anns)}标注", end="")


def capture_lesson(lesson: str, do_annotate: bool = False):
    d = ASSETS / lesson; d.mkdir(parents=True, exist_ok=True)
    items = PAGES.get(lesson, [])
    if not items: print(f"  第{lesson}课无配置"); return

    with sync_playwright() as p:
        b = p.chromium.launch(headless=True)
        ctx = b.new_context(viewport={"width":1440,"height":900}, device_scale_factor=1)
        pg = ctx.new_page()

        for i, it in enumerate(items):
            name = it["n"]
            try:
                print(f"  [{i+1}/{len(items)}] {name} ", end="", flush=True)
                pg.goto(it["u"], wait_until="domcontentloaded", timeout=45000)
                time.sleep(0.3)

                for ac in it.get("ac", []):
                    if "click" in ac:
                        try: pg.click(ac["click"], timeout=3000); time.sleep(0.3); pg.keyboard.press("Escape"); time.sleep(0.2)
                        except Exception:
                            if not ac.get("opt"): raise
                    elif "hover" in ac: pg.hover(ac["hover"])
                    elif "scroll_to" in ac: pg.evaluate(f"document.querySelector('{ac['scroll_to']}')?.scrollIntoView({{block:'start'}})")
                    elif "scroll" in ac: pg.evaluate(f"window.scrollBy(0,{ac['scroll']})")
                    elif "w" in ac: time.sleep(ac["w"]/1000)

                time.sleep(0.5)
                raw = d / f"{name}.png"
                pg.screenshot(path=str(raw), full_page=False)
                print("OK", end="", flush=True)

                if do_annotate and it.get("a"):
                    anns = []
                    for ann in it["a"]:
                        sel = S.get(ann["s"], ann["s"])
                        try:
                            box = pg.locator(sel).first.bounding_box()
                            if box and box["width"] > 0 and box["height"] > 0:
                                anns.append({"x":int(box["x"]),"y":int(box["y"]),"w":int(box["width"]),"h":int(box["height"]),
                                             "label":ann["l"],"color":ann.get("c","red")})
                        except: pass
                    if anns:
                        run_annotate(raw, d/f"{name}-annotated.png", anns)
                print()
            except Exception as e: print(f"FAIL: {e}")
        b.close()
    print(f"  第{lesson}课完成 -> {d}\n")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--lesson","-l"); ap.add_argument("--all",action="store_true"); ap.add_argument("--annotate","-a",action="store_true")
    a = ap.parse_args()
    lessons = sorted(PAGES.keys()) if a.all else ([a.lesson] if a.lesson else [])
    if not lessons: print("用法: --lesson 02 --annotate  或 --all --annotate"); return
    for ln in lessons:
        print(f"\n=== 第 {ln} 课 ===")
        capture_lesson(ln, a.annotate)

if __name__ == "__main__": main()
