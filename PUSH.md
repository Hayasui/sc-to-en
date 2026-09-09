# 推送到 GitHub

仓库已就绪（3 个提交，分支 `main`），只差远端地址与凭据。

## 方式一：在能访问 GitHub 的机器上推

```bash
# 1. 在 GitHub 上新建空仓库（不要勾选 README / .gitignore / license）
#    建议仓库名：sc-to-en

# 2. 关联远端并推送
cd ~/.workbuddy/skills/sc-to-en
git remote add origin git@github.com:<你的用户名>/sc-to-en.git
git push -u origin main
```

## 方式二：从本机传输（无 GitHub 凭据时）

本目录已生成 `sc-to-en.bundle`（放在项目目录 `C:/Agent/用研工作/3D二合/`），
是一个自包含的 git 仓库快照，拷到任何机器都能还原：

```bash
# 在目标机器上
git clone sc-to-en.bundle sc-to-en
cd sc-to-en
git remote set-url origin git@github.com:<你的用户名>/sc-to-en.git
git push -u origin main
```

## 方式三：本机直接推（需要凭据）

```bash
cd ~/.workbuddy/skills/sc-to-en
git remote add origin https://github.com/<用户名>/sc-to-en.git
# 推送时输入用户名 + Personal Access Token（不是账号密码）
git push -u origin main
```

## 提交历史

| 提交 | 内容 |
|------|------|
| `b6f0b44` | 添加 README：项目说明、用法、检查项清单 |
| `ddcb8c5` | roadmap: 记录版本控制现状与远端同步待办 |
| `c995ac9` | lint 补隐形字符/交叉引用/环节检查，加回归测试，纳入版本控制 |
