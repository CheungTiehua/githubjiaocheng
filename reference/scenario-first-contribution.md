# 场景教程：第一次给开源项目贡献代码

> 适用人群：想给开源项目提 PR 但不知道完整流程的人
> 前置：完成第六、七、八课（PR 全流程）
> 预计时间：30 分钟

---

## 场景描述

你发现 ant-design 的 Select 组件有一个小 Bug：多选模式下 placeholder 不显示。
你花 5 分钟找到了问题并在本地修好了。现在你想把这个修复贡献给 ant-design。

---

## 完整流程（7 步）

### 第 1 步：Fork（2 min）

1. 打开 https://github.com/ant-design/ant-design
2. 点右上角 **Fork** 按钮
3. 弹出窗口 → Owner 选你自己 → 保持 "Copy the main branch only" 勾选
4. 点 **Create fork**
5. 等几秒 → 自动跳转到 `github.com/你的用户名/ant-design`

> 现在你有了一份自己的 ant-design 代码副本。

### 第 2 步：Clone 到本地（2 min）

1. 在你的 Fork 页面 → 点绿色 **Code** 按钮
2. 如果配了 SSH Key：选 SSH 标签，复制 URL
3. 如果没配：选 HTTPS 标签，复制 URL
4. 打开终端：
   ```bash
   cd ~/projects      # 到你放代码的目录
   git clone git@github.com:你的用户名/ant-design.git
   cd ant-design
   ```

> 现在代码在你电脑上了。

### 第 3 步：创建分支并修改代码（3 min）

1. 创建新分支（不要在 main 上直接改）：
   ```bash
   git checkout -b fix/select-placeholder-multiple
   ```
2. 用你的 IDE 打开代码，找到 Bug 位置，修改
3. 保存 → 提交：
   ```bash
   git add .
   git commit -m "fix(Select): placeholder not showing in multiple mode"
   ```
4. 推送到你的 Fork：
   ```bash
   git push origin fix/select-placeholder-multiple
   ```

> Commit message 格式：`类型(范围): 描述`，如 `fix(Select): xxx`、`feat(Button): xxx`

### 第 4 步：创建 PR（5 min）

1. Push 后回到 GitHub → 你的 Fork 页面
2. 顶部会出现**黄色提示条**："fix/select-placeholder-multiple had recent pushes"
3. 点击 **Compare & pull request**
4. 进入 PR 创建页面：

**检查 Base 和 Compare：**
- Base repository: `ant-design/ant-design` ← 原仓库
- Base branch: `master` ← 原仓库的主分支
- Head repository: `你的用户名/ant-design` ← 你的 Fork
- Compare branch: `fix/select-placeholder-multiple` ← 你改代码的分支

**填写 PR 标题和正文：**

标题：
```
fix(Select): placeholder not showing in multiple mode (select)
```

正文：
```markdown
## 发生了什么
当 Select 的 mode 设为 multiple 时，placeholder 不显示。

## 原因
`renderPlaceholder` 方法中，当 value 是数组且长度为 0 时，走了错误的分支。

## 修复方案
在 `renderPlaceholder` 增加对空数组的检查。

## 截图
| Before | After |
|--------|-------|
| (拖入修复前的截图) | (拖入修复后的截图) |

## 关联 Issue
Fixes #12345
```

5. 右侧可选的设置：
   - Reviewers：不填（维护者会自己分派）
   - Labels：不填（维护者会加）
6. 点绿色 **Create pull request**

> 🎉 你的第一个开源贡献 PR 创建成功！

### 第 5 步：等待 Review（时长不定）

PR 创建后：
1. CI 会自动跑测试（你可以在 Checks 标签看结果）
2. 维护者会收到通知
3. 可能需要等几小时到几天（维护者都是志愿者，耐心等待）
4. 不要催（除非过了一周完全没动静，可以礼貌地问一下）

### 第 6 步：回应 Review（10 min）

如果维护者提了修改意见：
1. 认真看每条评论
2. 在本地的同一个分支上修改代码
3. Commit → Push（PR 会自动更新，不需要重新创建）
4. 在 PR 页面的 Reviewers 列表里点 🔄 **Re-request review**

如果有人提了 **Suggested change**：
1. 看 Suggested change 是否合理
2. 如果合理，点 **Commit suggestion** 一键接受
3. 如果不合理，回复解释原因

### 第 7 步：合并！

当 CI 通过 + 获得 Approve：
- 维护者会点击 Merge
- 你的代码正式进入 ant-design！
- Issue #12345 自动关闭

**后续：**
- 可以（但不必须）删除你的分支
- 你的 Fork 会落后于原仓库，记得 Sync Fork

---

## 行为准则（非常重要）

- ✅ 一个 PR 只做一件事（不要混入多个不相关改动）
- ✅ 阅读项目的 CONTRIBUTING.md（如果有）了解贡献规则
- ✅ PR 正文写清楚"为什么"和"怎么修"
- ❌ 不要 PR 超大改动（1000+ 行还没解释）
- ❌ 不要催 Review（开源维护者都是无偿工作）
- ❌ 不要改代码风格（格式化交给 Linter）
- ❌ 不要在 PR 里对喷

---

## 流程图

```
发现Bug → 检查是否已有Issue
                ↓
          [没有] 提 Issue 说明Bug（可选但推荐）
                ↓
          Fork 原仓库
                ↓
          Clone 到本地
                ↓
          创建新分支
                ↓
          改代码 → commit → push
                ↓
          打开 GitHub → Compare & PR
                ↓
          写清楚标题和正文 → 提交
                ↓
          等 CI 通过 + 等 Review
                ↓
        [有修改意见] 改代码 → push → Re-request
                ↓
          CI 通过 + 有人 Approve
                ↓
          维护者 Merge → 🎉完成！
```
