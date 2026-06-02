# 推荐设置清单

> 从零到专业。按"个人 → 仓库 → 组织"三个层级列出所有推荐配置。

---

## 一、个人账号设置

| 设置项 | 路径 | 推荐 | 为什么 |
|--------|------|------|--------|
| 头像 | 点右上角头像 → Your profile → 点头像编辑 | 上传一张照片 | 让你的 GitHub 看起来像活人 |
| Name | Settings → Public profile | 填你的名字 | 别人能知道你是谁 |
| Bio | Settings → Public profile | 一句话介绍 | 让人知道你的技术方向 |
| Location | Settings → Public profile | 城市, 国家 | 比如 "Beijing, China" |
| 主题 | Settings → Appearance | Dark mode | 保护眼睛 |
| SSH Key | Settings → SSH and GPG keys | 添加至少一个 | 免密推送代码 |
| Token | Settings → Developer settings → PAT | 生成一个，过期一年 | 用 Token 代替密码 |
| 2FA | Settings → Password and authentication | **开启！必须！** | 防止账号被盗 |
| 备份邮箱 | Settings → Emails | 添加一个备用的 | 主邮箱被封时还能恢复 |

---

## 二、单仓库设置（所有仓库都推荐配置）

### 2.1 基础设置（Settings → General）

| 设置项 | 推荐 | 原因 |
|--------|------|------|
| Default branch | `main` | 不用 `master`（有历史负担的命名） |
| Features: Issues | ✅ 开启 | 默认开启 |
| Features: Wiki | ✅ 按需 | 需要文档就开 |
| Features: Discussions | ✅ 开启 | 方便社区交流 |
| Merge button: Squash and merge | ✅ 开启 | 保持历史干净 |
| Merge button: Rebase and merge | ⬜ 按需 | 追求线性历史 |
| Automatically delete head branches | ✅ 开启 | PR 合并后自动清理分支 |

### 2.2 分支保护（Settings → Branches → Add rule）

| 规则 | 推荐值 |
|------|--------|
| Branch name pattern | `main` |
| Require a pull request before merging | ✅ |
| Require approvals | ✅ 至少 1 人 |
| Dismiss stale reviews when new commits are pushed | ✅ |
| Require status checks to pass before merging | ✅（如果有 CI） |
| Require conversation resolution before merging | ✅ |
| Do not allow bypassing the above settings | ✅ |
| Allow force pushes | ❌ |
| Allow deletions | ❌ |

### 2.3 模板文件

| 文件 | 优先级 | 作用 |
|------|--------|------|
| `.github/ISSUE_TEMPLATE/bug_report.md` | 高 | Bug 报告用模板 |
| `.github/ISSUE_TEMPLATE/feature_request.md` | 中 | 功能请求模板 |
| `.github/PULL_REQUEST_TEMPLATE.md` | 高 | PR 模板 |
| `.github/CODEOWNERS` | 中 | 代码责任人 |
| `CONTRIBUTING.md` | 中 | 贡献指南 |

---

## 三、CI 配置（.github/workflows/ci.yml）

### 最小 CI（任何语言都适用）

```yaml
name: CI
on: [push, pull_request]
jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v4
      - # 你的语言 setup
      - run: <你的测试命令>
```

### 推荐扩展到

```yaml
name: CI
on:
  push:
    branches: [main]
  pull_request:
    branches: [main]
jobs:
  lint:     # 代码风格检查
    ...
  test:     # 单元测试
    ...
  build:    # 编译检查（如果适用）
    ...
```

---

## 四、组织（Organization）设置

> 如果有多个仓库和成员，建议创建 Organization

| 设置项 | 推荐 |
|--------|------|
| 成员权限：Base permissions | Read（最小权限） |
| Repository: Default branch name | `main` |
| 团队管理 | 按功能建 Team（前端、后端、DevOps） |
| 分支保护 | 对所有仓库的 main 要求 PR + Review |

---

## 五、安全清单（定期检查）

| 检查项 | 频率 |
|--------|------|
| Dependabot 警报 | 每周看一次 |
| Secret scanning 警报 | 实时（有就立刻处理） |
| 协作者权限 | 每月检查（离职的人移除） |
| Token 过期日期 | 每月检查（快过期的重新生成） |
| 2FA 状态 | 一次（开着就行） |
| Security log | 每月扫一眼 |

---

## 六、浏览器插件推荐

| 插件 | 作用 | 适用浏览器 |
|------|------|-----------|
| Google 翻译 | 右键 → "翻译此页面" | Chrome |
| Octotree | 侧边栏文件树（方便浏览代码） | Chrome / Firefox |
| Refined GitHub | 增强 GitHub 界面功能 | Chrome / Firefox |

---

## 七、一言概之

```
个人：头像 + SSH Key + 2FA + Token
仓库：README + 分支保护 + CI + PR 模板
组织：最小权限 + Team 管理
安全：Dependabot + Secret scanning + 权限审计
```
