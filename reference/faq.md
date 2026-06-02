# FAQ — 常见问题

> 按学习顺序排列。每个问题配简要回答和指向详细课程的链接。

---

## 基础认知

### Q: GitHub 是什么？和 Git 是一回事吗？
**不是。** Git 是命令行工具（管理代码版本），GitHub 是网站（托管代码、协作）。你可以用 Git 不用 GitHub（比如用 GitLab / Gitee），也可以用 GitHub 的网页功能不碰 Git 命令。

### Q: 我不懂英文，能用 GitHub 吗？
**能。** 这门课的目标就是让你不看英文也能操作。配合浏览器翻译插件（推荐 Google 翻译的"翻译此页面"），看懂大概没问题。

### Q: GitHub 收费吗？
**基础功能完全免费。** 免费版可以：无限公开仓库、无限私有仓库、无限协作者、每月 2000 分钟 Actions（CI）。付费版增加 Codespaces 时长、企业功能等，个人开发者不需要。

### Q: 我不用 Git 命令行，能用 GitHub 吗？
**能，但有局限。** 你可以在网页上：看代码、提 Issue、参与讨论、Review PR。但提交代码目前只能通过 Git 命令或 GitHub Desktop。本课程只讲 GitHub 网页界面。

---

## 注册与设置

### Q: 用户名起错了能改吗？
**能。** Settings → Account → Change username。但改完之后所有旧链接（你的仓库 URL）都会失效，GitHub 会自动重定向，但别人收藏的不会。

### Q: 邮箱验证邮件没收到怎么办？
1. 检查垃圾邮件箱 2. 确认邮箱地址没写错 3. Settings → Emails → Resend verification email

### Q: 为什么用 Token 而不是密码？
**2021 年起 GitHub 不再支持密码推送代码**，这是安全措施。Token 可以精确控制权限、随时吊销、设置过期时间。生成方式：Settings → Developer settings → Personal access tokens → Generate new token (classic)。

### Q: 我该用 HTTPS 还是 SSH Clone？
- **SSH**：配一次终身免密，推荐（前提是不被公司防火墙封）
- **HTTPS**：每次 push 要输 Token，但防火墙友好

---

## 读代码

### Q: 我怎么快速了解一个陌生仓库？
按顺序看：1. 仓库名和描述 → 2. README.md → 3. Languages 占比 → 4. Star 数（判断热度） → 5. Issues（看活跃度）

### Q: Blame 是什么意思？点了会怎样？
Blame 原意是"责备"，在 Git 里是"找出每行代码是谁写的"。点进去每行左边会出现：头像、名字、提交时间、Commit SHA（点击可看那次改了什么）。

### Q: "Download ZIP" 和 "Clone" 有什么区别？
- Download ZIP：下载当前版本的快照，没有 Git 历史
- Clone：下载完整仓库（含所有历史版本），可以用 Git 命令管理

---

## Issue

### Q: Issue 和 PR 有什么区别？
- **Issue**：任务/Bug/讨论，包含文字描述和讨论
- **PR**：代码改动，包含实际代码差异和讨论
- 两者可以关联：PR 正文写 `Fixes #123`，合并后自动关闭第 123 号 Issue

### Q: 我看到一个 Bug，该提 Issue 还是直接改代码提 PR？
- 如果不确定怎么修 / 想先确认是不是 Bug → **先提 Issue**
- 如果知道怎么修且不涉及重大改动 → **直接提 PR**，PR 正文说明修了什么
- 如果不确定是不是 Bug → 去 Discussions（如果项目有）先问

### Q: Issue 被 Close 和 Delete 有什么区别？
- **Close**：关闭但不删除，被关闭的 Issue 还能搜索到、能引用、能重开。这是最常用的。
- **Delete**：彻底删除。极少用。

### Q: 为什么我的 Issue 没有自动关闭？
检查：1. PR 正文里写的是 `Fixes #N`（不是标题） 2. PR 合并到的分支是默认分支（main/master） 3. 编号是对的（注意 Issue 和 PR 编号共享）

---

## PR

### Q: Fork 和 Clone 有什么区别？
- **Fork**：在 GitHub 服务器上复制一份仓库到你名下（云端）
- **Clone**：把代码从 GitHub 下载到你电脑（本地）
- 通常是先 Fork → 再 Clone 自己的 Fork

### Q: Fork 之后，原仓库更新了，我的 Fork 会自动更新吗？
**不会。** 需要手动操作：进入你的 Fork → Fetch upstream → Fetch and merge。或者在本地用命令行同步。

### Q: Base branch 和 Compare branch 怎么设？
- **Base** = 代码要合入哪（通常是原仓库的 main）
- **Compare** = 你的代码在哪（你的 Fork 的 main 或你建的分支）
- 方向千万不要搞反（如果反了就变成你把原仓库的代码合并到你那）

### Q: 三种 Merge 方式怎么选？
- **Merge commit**：保留完整历史，大团队常用
- **Squash and merge**：把 PR 里所有 commit 压成 1 个，适合 PR 里 commit 很碎的场景
- **Rebase and merge**：历史完全线性，最干净但操作最复杂
- 不确定时，让仓库维护者决定。

### Q: PR 有冲突怎么办？
1. 先在 YouTube/B站 搜 "解决 Git merge conflict"，Git 命令行操作超出了本课范围
2. 或者用 VS Code 的合并编辑器（图形化操作，简单很多）

---

## Code Review

### Q: Approve、Comment、Request changes 有什么区别？
- **Comment**：纯评论，不表态（比如提个问题或小建议）
- **Approve**：批准合并（需要 N 个 Approve 才满足分支保护规则）
- **Request changes**：要求修改（有分支保护规则时会阻止合并）

### Q: 我提了 Review 意见，PR 作者改了代码后我收到通知了吗？
会收到。但如果作者没点 **Re-request review**，你可能不知道他改完了。建议作者改完代码后主动 Re-request。

---

## CI / Actions

### Q: CI 是什么？为什么需要 CI？
CI（持续集成）是让机器自动帮你跑测试、检查代码、部署。好处：1. 每次提 PR 自动检查 2. 避免人工遗漏 3. 配合分支保护规则强制要求测试通过。

### Q: CI 一直转圈（黄色）是怎么回事？
1. 正在运行，等一会儿 2. 在排队等资源（免费版有并发限制，等几十秒到几分钟）
3. 卡死了，点 Cancel workflow 然后 Re-run

### Q: 怎么给我的仓库加 CI 绿标（Badge）？
Actions → 选你的 Workflow → ... → Create status badge → 复制 Markdown 链接 → 粘贴到 README.md

---

## 安全

### Q: 我不小心把密码/API Key 提交到公开仓库了怎么办？
**立即行动**：1. 在对应平台吊销这个密钥（最重要！） 2. 把涉及的文件加入 .gitignore 3. 在 Git 历史中删除这个密钥（搜 "git remove sensitive data"） 4. 用新密钥替换。哪怕只公开了几秒钟也视为已泄露。

### Q: 什么设置能确保 main 分支安全？
Settings → Branches → Add rule → 输入 main → 开启：
- Require a pull request before merging
- Require approvals (至少 1 人)
- Require status checks to pass before merging
- Do not allow bypassing the above settings

---

## 其他

### Q: GitHub 能上传多大的文件？
- 网页上传：单个文件最大 25MB
- Git 推送：建议单个文件不超过 100MB，仓库总大小不超过 5GB
- 大文件用 Git LFS（Large File Storage），超出本课范围

### Q: 怎么删除一个仓库？
Settings → 拉到最下面 Danger Zone → Delete this repository → 输入仓库名确认。**会连带 Issues、PR、Wiki 全部删除，无法恢复。**

### Q: 我想学 Git 命令行去哪里？
- 推荐廖雪峰的 Git 教程（中文）
- Pro Git 中文版
- GitHub Skills 的 Introduction to GitHub（有交互式教程）
