# GitHub 常见报错及解决方案

> 收录 GitHub 网页端常见的报错提示，配中文解释和解决方案。
> 最后更新：2026-06-02

---

## 网页端报错

### 404 Page not found
| 项目 | 内容 |
|------|------|
| 中文意思 | 页面不存在 |
| 常见原因 | 1. 仓库被删了 2. 仓库改成私有(Pirvate)了 3. URL 拼写错误 |
| 怎么办 | 确认仓库名和用户名拼写正确 → 问项目主人仓库还在吗 |

### 500 Internal Server Error
| 项目 | 内容 |
|------|------|
| 中文意思 | GitHub 服务器内部错误 |
| 常见原因 | GitHub 自己出问题了 |
| 怎么办 | 等几分钟刷新。可以上 https://www.githubstatus.com 看 GitHub 服务状态 |

### You have exceeded a secondary rate limit
| 项目 | 内容 |
|------|------|
| 中文意思 | 你触发了频率限制（操作太快了） |
| 常见原因 | 短时间发送太多请求 |
| 怎么办 | 等几分钟到一小时。不要用脚本刷 GitHub |

### This branch has conflicts that must be resolved
| 项目 | 内容 |
|------|------|
| 中文意思 | 这个分支有冲突，必须先解决才能合并 |
| 常见原因 | 你改的文件和目标分支上同一个文件也被人改了 |
| 怎么办 | 1. 点 Resolve conflicts 在网页上解决 2. 或在本地 `git merge main` 解决冲突后 push |

### This branch is out-of-date with the base branch
| 项目 | 内容 |
|------|------|
| 中文意思 | 你的分支落后于目标分支 |
| 常见原因 | PR 创建后，目标分支又有新提交 |
| 怎么办 | Sync Fork → 或者本地 merge main 到你的分支 → push |

### Can't automatically merge
| 项目 | 内容 |
|------|------|
| 中文意思 | 无法自动合并 |
| 常见原因 | 有冲突 |
| 怎么办 | 同冲突解决 |

### You don't have permission to push
| 项目 | 内容 |
|------|------|
| 中文意思 | 你没有推送权限 |
| 常见原因 | 1. 你在别人的仓库里不是 Collaborator 2. 用的 HTTPS 密码/Token 不对 |
| 怎么办 | 确认你是 Collaborator → 确认 Token 没过期 → 或者换 SSH |

### Repository not found (SSH)
| 项目 | 内容 |
|------|------|
| 中文意思 | 找不到仓库（SSH 方式） |
| 常见原因 | 1. SSH Key 没配 2. 仓库名拼错 3. 仓库是 Private 但你没权限 |
| 怎么办 | 确认 SSH Key 已添加 → 确认 URL 拼写 → 确认有权限 |

### Your account has been flagged
| 项目 | 内容 |
|------|------|
| 中文意思 | 你的账号被标记了 |
| 常见原因 | 可能被 GitHub 误判为垃圾账号 |
| 怎么办 | 联系 GitHub Support 申诉 |

---

## 邮件通知

### Action required: Verify your email address
| 项目 | 内容 |
|------|------|
| 中文意思 | 需要操作：验证你的邮箱 |
| 怎么办 | 点邮件里的 "Verify email address" 按钮 |

### [username] mentioned you
| 项目 | 内容 |
|------|------|
| 中文意思 | 有人在 Issue/PR 里 @ 了你 |
| 怎么办 | 正常的通知，点进去看 |

### [repo] A new pull request in [repo]
| 项目 | 内容 |
|------|------|
| 中文意思 | 有人在你 Watch 的仓库提了 PR |
| 怎么办 | 如果你不想收这类通知，去那个仓库 → Unwatch |

### [repo] Run failed: CI (main)
| 项目 | 内容 |
|------|------|
| 中文意思 | 你的 CI 运行失败了 |
| 怎么办 | 点 View workflow run 看日志 → 修代码 → Push |

### We found a potential security vulnerability
| 项目 | 内容 |
|------|------|
| 中文意思 | Dependabot 发现了安全漏洞 |
| 怎么办 | 进 Security 标签查看详情 → 更新依赖版本 |

---

## CI / Actions 报错

### Process completed with exit code 1
| 项目 | 内容 |
|------|------|
| 中文意思 | 某个 Step 执行失败（退出码 1） |
| 怎么办 | 看这个 Step 上面红色部分的报错信息 |

### npm ERR! / Module not found
| 项目 | 内容 |
|------|------|
| 中文意思 | npm 安装依赖失败 |
| 原因 | 可能是 package.json 里缺依赖 / package-lock.json 没更新 / 网络问题 |
| 怎么办 | 1. 本地先 `npm install` 确认能通过 2. 确认 package-lock.json 提交了 3. CI 里用 `npm ci` 而不是 `npm install` |

### command not found
| 项目 | 内容 |
|------|------|
| 中文意思 | 命令找不到 |
| 原因 | CI 环境里没有装对应的工具 |
| 怎么办 | Workflow 里加对应的 setup Action（如 setup-node、setup-python） |

### The job was canceled
| 项目 | 内容 |
|------|------|
| 中文意思 | CI 任务被取消了 |
| 原因 | 你手动取消 / 免费版并发限制 / 超时 |
| 怎么办 | Re-run 或者等一会儿 |

### Error: Resource not accessible by integration
| 项目 | 内容 |
|------|------|
| 中文意思 | CI 没有权限访问资源 |
| 原因 | Token 权限不够（通常是 GITHUB_TOKEN） |
| 怎么办 | 检查 Workflow 的 permissions 设置 |

---

## Quick Reference（速查）

| 报错关键词 | 可能原因 | 快速解决 |
|-----------|---------|---------|
| 404 | 仓库不存在/没权限 | 检查 URL 和权限 |
| Permission denied | 没推送权限 | 检查 Collaborator 或 Token |
| Conflict | 代码冲突 | 解决冲突 |
| Rate limit | 操作太频繁 | 等待 |
| Exit code 1 | CI 运行失败 | 看日志红色部分 |
| command not found (CI) | 缺少工具 | 加 setup Action |
| Module not found (CI) | 依赖没装 | 确认 package.json + npm ci |
