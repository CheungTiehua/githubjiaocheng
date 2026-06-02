# 场景教程：团队协作日常

> 适用人群：在团队中用 GitHub 协作的人
> 前置：完成第四、六、七、八、九课
> 预计时间：20 分钟（阅读时间）

---

## 场景描述

你和 5 个同事一起开发一个项目。仓库是你们公司的私有仓库。每个人的日常工作是：领 Issue → 创建分支 → 改代码 → 提 PR → 同事 Review → 合并。

---

## 完整流程（6 步，每天循环）

### 第 1 步：领取任务

1. 打开项目仓库 → Issues 标签
2. 看 Assignee 是空的 Issue（没人领的）
3. 点进去 → 右侧 Assignees → 选自己
4. 开始干活

> 有些团队用 Projects 做看板，流程一样：把卡片从 Todo 拖到 In Progress。

### 第 2 步：创建分支

```bash
git checkout main
git pull origin main            # 确保是最新的
git checkout -b feat/my-feature # 建新分支
```

**分支命名建议：**
- `feat/` + 功能描述：`feat/dark-mode`
- `fix/` + Bug 描述：`fix/login-redirect`
- `chore/` + 杂项：`chore/update-deps`

### 第 3 步：改代码 + 提交

```bash
# 改代码...
git add .
git commit -m "feat: add dark mode toggle to header"
git push origin feat/my-feature
```

**Commit message 格式（团队约定）：**
```
类型: 简短描述

详细的解释（如果需要）
```

常见类型：`feat`（新功能）、`fix`（修 Bug）、`docs`（文档）、`refactor`（重构）、`test`（测试）、`chore`（杂项）

### 第 4 步：创建 PR

1. Push 后 GitHub 自动弹出黄色提示条
2. 点 **Compare & pull request**
3. 确认 Base = `main`，Compare = 你的分支
4. 填写 PR：
   ```markdown
   ## 做了什么
   在导航栏右上角添加了深色模式切换按钮

   ## 截图
   | 浅色 | 深色 |
   |------|------|
   | (截图) | (截图) |

   ## 怎么测试
   1. 点击导航栏右侧的月亮/太阳图标
   2. 页面应在浅色和深色之间切换
   3. 刷新后应保持选择
   ```
5. 右侧 Reviewers → 选要 Review 的同事
6. Labels → 加 `feat`
7. 点 **Create pull request**

### 第 5 步：Code Review + 迭代

1. 等待同事 Review
2. 如果 CI 失败 → 点 Checks 看日志 → 修代码 → Push
3. 如果同事提了修改意见：
   - 逐条回复或修改
   - 改完 push → Re-request review
4. 如果同事给了 Approve（且 CI 通过）→ 准备合并

### 第 6 步：合并 + 清理

1. 确认 CI 通过了（绿勾 ✅）
2. 确认有足够的 Approve（按团队规则）
3. 点 **Squash and merge**（推荐，保持历史干净）
4. 合并后 GitHub 提示是否删除分支 → 点 Delete branch
5. 本地切回 main 并拉取最新：
   ```bash
   git checkout main
   git pull origin main
   git branch -d feat/my-feature  # 删除本地分支
   ```

---

## 日常习惯清单

### 每天开始工作前
- `git checkout main && git pull origin main`

### 创建 PR 时
- 确认 PR 只包含相关改动（没有混入无关文件）
- 确认 CI 通过后再找同事 Review
- 确认 PR 正文写清楚了"做了什么"和"怎么测试"

### Review 别人代码时
- 对事不对人
- 区分"必须改"和"建议改"
- 具体问题用 Suggested change 功能

### 合并后
- 删除分支（保持仓库整洁）
- 如果关联了 Issue，确认 Issue 已自动关闭

---

## 团队配置建议

| 配置 | 路径 | 推荐 |
|------|------|------|
| 分支保护 | Settings → Branches → main | PR + 至少 1 Approve + CI 通过 |
| PR 模板 | `.github/PULL_REQUEST_TEMPLATE.md` | 要求写 Summary + Screenshots |
| CODEOWNERS | `.github/CODEOWNERS` | 核心目录指定 Owner |
| Issue 模板 | `.github/ISSUE_TEMPLATE/` | Bug Report + Feature Request |

---

## 团队用语对照（中英）

| 日常工作用语 | GitHub 对应操作 |
|-------------|----------------|
| "我领了这个任务" | Issue → Assignees → 选自己 |
| "代码写好了，帮我看看" | 创建 PR → Reviewers → 选同事 |
| "这里改一下" | Review → 行评论 → Request changes |
| "没问题，合并吧" | Review → Approve |
| "合并吧" | Merge pull request |
| "删掉这个分支" | PR 合并后点 Delete branch |
