# 场景教程：维护自己的开源项目

> 适用人群：创建或维护开源项目的开发者
> 前置：完成全部课程
> 预计时间：15 分钟（阅读时间）

---

## 场景描述

你自己做了一个开源项目，发布在 GitHub 上。有人提 Issue、有人提 PR。你怎么高效地管理这一切？

---

## 起步：项目的基础设施

### 必须有的文件

| 文件 | 作用 |
|------|------|
| `README.md` | 项目首页说明（必须！） |
| `LICENSE` | 开源许可证（没有许可证别人不能合法使用你的代码） |
| `CONTRIBUTING.md` | 贡献指南（告诉别人怎么参与） |
| `CODE_OF_CONDUCT.md` | 行为准则 |
| `.gitignore` | 忽略不需要提交的文件 |

### 推荐的目录结构

```
你的仓库/
├── README.md
├── LICENSE
├── CONTRIBUTING.md
├── .gitignore
├── .github/
│   ├── ISSUE_TEMPLATE/
│   │   ├── bug_report.md
│   │   └── feature_request.md
│   ├── PULL_REQUEST_TEMPLATE.md
│   ├── CODEOWNERS
│   └── workflows/
│       └── ci.yml
├── src/
└── docs/
```

---

## 日常维护任务

### 任务 1：处理新 Issue

1. 打开 Issues → 看新 Issue 列表
2. 对每个新 Issue：
   - **打 Label**：`bug` / `enhancement` / `question` / `duplicate`
   - **如果不清楚**：回复问清楚 → 加 label `needs more info`
   - **如果是好上手的问题**：加 `good first issue`（引导新手）
   - **如果决定不修**：加 `wontfix` → 回复解释原因 → Close
3. 对需要修的 Issue：
   - 加 Milestone（如 `v1.2`）
   - 如果有 Assignee，指派

### 任务 2：Review PR

1. 收到新 PR → Checks 标签看 CI 是否通过
2. Files changed → 逐行审查
3. 提意见 → 选择 Comment / Approve / Request changes
4. 如果需要对方修改 → Request changes → 等对方改
5. 改完后确认 → Approve → Merge

### 任务 3：管理社区

1. **Discussions**（如果开启了）：
   - 定期看看有没有新帖子
   - 回答问题或在 Q&A 帖子中标记答案
   - 不合适的帖子转到 Issue

2. **Issue 清理**：
   - 定期（每月）看一遍老 Issue
   - 已经修了的 Close（或让 Dependabot 自动关）
   - 长时间不活跃的加 `stale` 标签

### 任务 4：发布新版本

1. 确认所有该修的都修了
2. 更新版本号（遵循语义化版本：主版本.次版本.补丁版本）
3. 打 Tag
4. 创建 Release：
   - Tag: `v1.2.0`
   - 标题: `v1.2.0`
   - Release Notes（可以用 GitHub 自动生成的）
   - 如果有编译好的产物，上传到 Assets
5. 发布

---

## 推荐的仓库配置

### 分支保护

| 设置 | 值 |
|------|----|
| Require PR before merging | ✅ |
| Require approvals | ✅ 至少 1 人 |
| Dismiss stale reviews | ✅ |
| Require status checks | ✅ |
| Require conversation resolution | ✅ |
| Do not allow bypassing | ✅ |

### Issue 模板

`.github/ISSUE_TEMPLATE/bug_report.md`：

```yaml
---
name: Bug Report
about: Create a report to help us improve
title: "[Bug] "
labels: bug
---

**Describe the bug**
<!-- A clear description -->

**To Reproduce**
Steps:
1. ...
2. ...

**Expected behavior**
<!-- What should happen -->

**Environment**
- OS: [e.g. Windows 10]
- Browser: [e.g. Chrome 120]
- Version: [e.g. v1.0.0]
```

### PR 模板

`.github/PULL_REQUEST_TEMPLATE.md`：

```markdown
## Summary
<!-- What does this PR do? -->

## Related Issue
<!-- Fixes #123 -->

## Screenshots
<!-- If applicable -->

## Checklist
- [ ] I have tested this change
- [ ] I have updated the documentation
```

---

## 应对常见情况

### 情况 1：有人提了个重复 Issue
- 回复："This is a duplicate of #456. Closing."
- 加 `duplicate` 标签 → Close

### 情况 2：有人提的 PR 代码质量很差
- 不要直接关闭（会打击贡献者热情）
- 提具体的修改意见，用 Suggested change
- 如果确实不可用，礼貌解释为什么这个方案不可行

### 情况 3：有人在 Issue 里吵架
- 先警告
- 还不消停 → Lock conversation

### 情况 4：项目被恶意 Fork 或滥用
- 如果你没有违反开源许可，一般不用管
- 如果有人用你的项目干违法的事：GitHub 举报

### 情况 5：收到安全漏洞报告
- 让报告者用 Security → Report a vulnerability（私下报告，不要公开 Issue）
- 修复后发 Security advisory
- 发布修复版本
- 感谢报告者

---

## 维护者工具速查

| 我要做什么 | 操作 |
|-----------|------|
| 批量关 Issue | Issue 列表 → 勾选 → Mark as → Closed |
| 添加协作者 | Settings → Collaborators → Add people |
| 设分支保护 | Settings → Branches → Add rule |
| 创建 Issue 模板 | 建 `.github/ISSUE_TEMPLATE/` 目录 |
| 建 CODEOWNERS | 建 `.github/CODEOWNERS` |
| 看项目流量 | Insights → Traffic |
| 看贡献者 | Insights → Contributors |
| 禁用 Issue | Settings → General → 取消 Issues |
| 归档项目 | Settings → General → Archive |
