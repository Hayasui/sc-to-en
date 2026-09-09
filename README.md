# sc-to-en · 用研文档中文定稿 → 英文本地化 → UserTesting 配置

把游戏/产品用研的简体中文 Markdown 文档（访谈大纲、玩家甄别问卷、测试脚本），
本地化成**可以直接逐条复制到 UserTesting 平台**的英文版。

不是直译——是让美国普通玩家读起来自然，同时满足平台的所有字段限制。

## 这个 skill 解决什么问题

用研文档通常有两套读者：**玩家**（读题干和选项）和**研究团队**（读研究落点与内部备注）。
中文稿写完后，需要一份英文版配置到 UserTesting 上。直接翻译会踩两类坑：

- **平台限制**：字段字符上限、自填选项只能叫 `Other` / `None of the above`、
  无法按前一题答案动态生成选项、量表题必须填 Scale Labels
- **语言不地道**：中式英文、"核心玩家 vs 破圈大众"这类术语、生硬的祈使句

本 skill 把这两类问题固化成流程、检查清单和自动校验脚本。

## 目录结构

```
SKILL.md                      主流程（场景判断 → 本地化 → 校验 → 汇报）
references/
  platform-constraints.md     UserTesting 平台限制与坑（含条件逻辑的真实能力）
  localization-principles.md  英文本地化标准（不直译、无俚语、面向普通玩家）
  doc-structure.md            文档结构规范（玩家可见/内部参考分离、有人/无人版命名）
  glossary.md                 术语对照表（跨文档、跨会话保持一致）
  checklist.md                交付前逐项检查清单
  roadmap.md                  升级路线图与已知未解决项
scripts/
  lint_usertesting.py         自动校验（中英对齐、题号、隐形字符、平台限制）
  test_lint.py                lint 的回归测试（26 个用例，正例+反例成对）
```

## 用法

### 校验文档

```bash
# 只检查英文版
python scripts/lint_usertesting.py <英文版.md>

# 同时比对中文版（推荐）
python scripts/lint_usertesting.py <英文版.md> --sc <中文版.md>
```

检查项：

| 类别 | 内容 |
|------|------|
| 平台 | Instruction/Navigation 超 1000 字符、禁止的自填提示、量表题缺 Scale Labels |
| 本地化 | 残留汉字 / 中文标点 / 中文标点序号 / **隐形字符** |
| 结构 | 题号连续性与重复、**题号交叉引用是否指向存在的题**、Task/Page 或环节结构完整性 |
| 对齐 | 中英题号数、每题选项数、量表端点是否一致（需 `--sc`） |

### 改完脚本跑自测

```bash
python scripts/test_lint.py
```

## 三条设计原则

**版本链条**：中文 md 是源头（内容设计在此定稿）→ 英文 md 是本地化产物（面向玩家，措辞可自由）
→ xlsx 是下游留档渲染。英文版可单边调整措辞，**一旦动了语义必须回写中文版**。

**玩家可见 vs 内部参考严格分离**：只本地化玩家可见部分（题干、选项、量表标签、
页面引导语）；研究落点、内部备注、研究假设保持原样，不参与润色。

**平台限制优先于语言美感**：一句话再漂亮，违反平台字段限制也得改。先满足平台，再谈地道。

## 使用前提

- Python 3.8+
- 无第三方依赖（lint 与测试均只用标准库）
- 面向 UserTesting 的 Unmoderated Think-out-Loud Test 与 Moderated Interview

## 许可

内部研究工具，按需自取。
