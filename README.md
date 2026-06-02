# GitHub 中文手把手教程

> 不讲 Git 命令行，不讲编程。只讲一件事——**GitHub 网页上每一个按钮都是干什么的**。

## 这是什么

一本给**英文吃力**的中国工程师看的 GitHub 教程。15 节课，从注册账号到 PR 合并、CI 配置、安全管理，**鼠标指到哪讲到哪**。

## 快速开始

打开 `site/index.html` 即可浏览完整网站。

或在线访问：[cheungtiehua.github.io/wangzhan](https://cheungtiehua.github.io/wangzhan)（需启用 GitHub Pages）

## 课程结构

| 课 | 内容 |
|----|------|
| 01 | 注册与基础设置 |
| 02 | 读代码（上）— 仓库主页全解 |
| 03 | 读代码（下）— 文件与历史 |
| 04 | Issue（上）— 创建与管理 |
| 05 | Issue（下）— 高级功能 |
| 06 | PR（一）— Fork 与 Clone |
| 07 | PR（二）— 创建 Pull Request |
| 08 | PR（三）— 生命周期与合并 |
| 09 | Code Review |
| 10 | Actions/CI（上）— 概念与配置 |
| 11 | Actions/CI（下）— 阅读运行日志 |
| 12 | 项目管理（上）— Projects |
| 13 | 项目管理（下）— Wiki/Discussions/Releases/Packages |
| 14 | 安全与权限 |
| 15 | 附录：速查手册 |

## 参考文档

- 170+ 英文术语中英对照
- 40+ 常见问题 FAQ
- 3 个场景实战（首次贡献 / 团队协作 / 项目维护）
- 常见报错 + 快捷键 + 推荐设置

## 重新构建

改完 Markdown 后重新生成网站：

```bash
pip install markdown jinja2 pygments
python build_site.py
```

## 截图标注

```bash
# 全自动截图 + 标注
python screenshot_course.py --all --annotate

# 只截某一课
python screenshot_course.py --lesson 02 --annotate
```

## 许可

MIT
