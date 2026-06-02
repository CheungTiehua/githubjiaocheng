# 课程总纲

---

## 模块 01：注册与基础设置（1 节，约 25 分钟）

### 1.1 从零开始

| 步骤 | 内容 |
|------|------|
| 打开 github.com | 首页介绍（导航栏、搜索框、Sign up / Sign in） |
| 注册 | 用户名规则、邮箱、密码、验证码 |
| 选择计划 | Free vs Team vs Enterprise，选 Free |
| 验证邮箱 | 查收邮件、点链接激活 |
| 首次登录 | Dashboard 长什么样 |

### 1.2 个人设置 (Settings)

| 设置页 | 讲什么 |
|--------|--------|
| Public profile | 头像、Name、Bio、URL、Company、Location |
| Account | 改密码、改邮箱、Delete account |
| Appearance | 主题切换（Dark mode）、emoji 风格 |
| Notifications | 通知方式、Subscribe 是什么 |
| SSH and GPG keys | 为什么需要 SSH Key、怎么生成、怎么添加 |
| Developer settings | Personal Access Token（是什么、什么时候用） |
| 右上角菜单 | 每个菜单项干什么 |

---

## 模块 02：读代码（2 节，约 50 分钟）

### 2.1 仓库主页

| 区域 | 内容 |
|------|------|
| 顶部导航栏 | 搜索框、通知铃铛、+ 号菜单、头像菜单 |
| 仓库头部 | 仓库名、Public/Private 标签、Star/Fork/Watch 按钮 |
| 标签栏 | Code / Issues / Pull requests / Actions / Projects / Wiki / Security / Insights / Settings |
| 文件列表 | 目录树、文件图标、Last commit 信息 |
| 右侧面板 | About、Releases、Packages、Languages、Contributors |

### 2.2 看代码

| 功能 | 内容 |
|------|------|
| 点进文件 | 代码高亮、行号、Raw / Blame / History 按钮 |
| Blame | 每行谁写的、什么时候写的、点进 commit |
| History / Commits | 提交历史、commit message、SHA、diff |
| 切换分支/标签 | Branch 下拉、Tag 是什么 |
| Releases | 下载源码包、Release notes |
| 搜索 | 仓库内搜索、GitHub 全站搜索、搜索语法 |

---

## 模块 03：Issue（2 节，约 50 分钟）

### 3.1 创建和管理 Issue

| 功能 | 内容 |
|------|------|
| Issue 列表 | 过滤器、Label、Milestone、Assignee |
| 创建 Issue | Title、正文、Markdown 编辑器、Preview |
| 正文功能 | 粘贴图片、代码块、Checklist 交互、@提及、#引用 |
| Label | 默认标签、自定义标签、颜色 |
| Milestone | 是什么、怎么创建、怎么关联 |
| Assignee | 指派给谁 |

### 3.2 Issue 高级功能

| 功能 | 内容 |
|------|------|
| Issue Template | 怎么创建模板、怎么用 |
| Pin Issue | 置顶 |
| Lock / Transfer | 锁定讨论、转移仓库 |
| 关联 PR | Close / Fix / Resolve 关键词自动关闭 |

---

## 模块 04：Pull Request 全流程（3 节，约 80 分钟）

### 4.1 Fork 和 Clone 概念

| 概念 | 内容 |
|------|------|
| Fork | Fork 是什么、Fork 按钮在哪、Fork 后仓库在哪 |
| Upstream vs Origin | 上游仓库和 Fork 仓库的区别 |
| Clone | Clone 按钮、HTTPS vs SSH、GitHub Desktop |

### 4.2 创建 PR

| 步骤 | 内容 |
|------|------|
| 推送代码后 | 黄色提示条、Compare & pull request |
| PR 创建页面 | Base/Branch 选择、Title、正文、Reviewers/Assignees/Labels |
| Draft PR | 草稿 PR 是什么、什么时候用 |
| PR 模板 | Pull request template |

### 4.3 PR 生命周期

| 阶段 | 内容 |
|------|------|
| Conversation 标签 | 讨论、Review 评论、CI 状态 |
| Commits 标签 | 所有 commit 列表 |
| Checks 标签 | CI 跑的结果 |
| Files changed 标签 | 所有改动文件、Diff 视图 |
| Merge | 三种合并方式（Merge commit / Squash / Rebase） |
| Close PR | 关闭但不合并 |

---

## 模块 05：Code Review（1 节，约 25 分钟）

### 5.1 Review 界面

| 功能 | 内容 |
|------|------|
| Files changed | 逐文件查看改动、展开/折叠 |
| Review 评论 | 单行评论、多行评论、Suggested change |
| Review 提交 | Comment / Approve / Request changes 三个按钮 |
| Re-request review | 修改后重新请求 Review |
| Dismiss review | 驳回过时的 Review |

---

## 模块 06：Actions / CI（2 节，约 50 分钟）

### 6.1 理解 CI

| 概念 | 内容 |
|------|------|
| CI 是什么 | 自动化测试、自动部署、自动检查 |
| Workflow 文件 | .github/workflows/ 目录、YAML 语法简介 |
| Actions 市场 | 搜索和引用现成的 Action |

### 6.2 Actions 界面

| 页面 | 内容 |
|------|------|
| Actions 标签 | Workflow 列表、运行历史 |
| 单次运行 | Job 列表、Step 展开、日志查看 |
| Badge | 状态徽章、怎么加到 README |

---

## 模块 07：项目管理（2 节，约 40 分钟）

### 7.1 Projects

| 功能 | 内容 |
|------|------|
| 创建 Project | Board / Table / Roadmap 三种视图 |
| 卡片/行 | 添加 Issue/PR、自定义字段 |
| 自动化 | 状态自动流转 |

### 7.2 其他协作工具

| 功能 | 内容 |
|------|------|
| Wiki | 创建页面、Markdown 编辑、侧边栏 |
| Discussions | 论坛式讨论、分类、置顶 |
| Releases | 打 Tag、写 Release notes、上传附件 |
| Packages | 包托管（npm/Docker 等）简介 |

---

## 模块 08：安全与权限（1 节，约 25 分钟）

### 8.1 仓库安全

| 功能 | 内容 |
|------|------|
| Branch protection | 分支保护规则、必须 Review、必须 CI 通过 |
| CODEOWNERS | 文件责任人、自动添加 Reviewer |
| Security 标签 | Dependabot、安全公告、Secret scanning |

---

## 附录

### A. 每个模块需要准备的截图

每个模块需要预先截取 GitHub 对应页面截图，放在 `assets/` 目录下，按模块编号命名：

```
assets/
├── 01-register/
│   ├── 01-homepage.png
│   ├── 02-signup-form.png
│   ├── 03-verify-email.png
│   └── ...
├── 02-read-code/
└── ...
```

### B. 需要录制的操作视频

- Fork → Clone → PR → Merge 完整流程（模块 04 核心）
- Code Review 完整交互（模块 05）
- Actions 日志查看（模块 06）
