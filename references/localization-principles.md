# 英文本地化原则

目标读者是**美国普通玩家**（不是专业从业者）。要读起来自然、像母语者写的，而不是中文直译。

## 1. 不直译

中文的句式和搭配直译过去常常生硬。判断标准：**如果美国人在日常对话里不会这么说，就改。**

| 中式直译 | 地道表达 |
|---------|---------|
| `One last, possibly abstract topic: this game has a story or not.` | `One last, and this one's a bit trickier: does this game have a story or not?` |
| `fits with the merge games you understand` | `fits in with the merge games you play` |
| `pure mechanics is enough` | `just the gameplay is enough for me` |
| `how does the feel work` | `how does it feel` |
| `Besides the phone...` | `Other than the phone...` |

**常见的中式英文信号**：

- 主语/动词缺失或错位（`so you whether or not there's a story?` —— 漏了动词）
- 名词当动词用、动词当名词用
- 把中文的"的"结构直译成 `of` 长串
- 抽象的书面词（`abstract topic`、`cognitive load`）出现在玩家题干里

## 2. 轻松友好，但不用俚语

用户定调：**口语化，但不过度口语，不俚语**。

- 可以用：`Let's talk about...`、`Have fun!`、`Don't worry about...`
- 不要用：`gonna`、`wanna`、`awesome`、`super cool`、`no-brainer`、`hit different` 等俚语或过度网络化的表达
- 专业术语只出现在内部备注里，玩家题干一律用日常词

## 3. 页面标题用 Title Case（新闻标题式）

**Question Page 的标题**（玩家在页面上看到的）用 Title Case：每个主要单词首字母大写，介词/连词/冠词小写。

| 错误 | 正确 |
|------|------|
| `About your device` | `About Your Device` |
| `About the merge games you play` | `About the Merge Games You Play` |
| `Deep dive — 3D board` | `Deep Dive — The 3D Board` |
| `Download & open the game`（任务名） | `Download & Open the Game` |

注意：这只针对**标题**。题干（Stem）、选项、正文用正常句子大小写。

## 4. 专有名词不翻译

- 游戏名保持原文：`Travel Town – Merge Adventure`、`Gossip Harbor: Merge & Story`、`Flambé: Merge and Cook`
- 平台名：`UserTesting`、`Google Play`
- 题型名：`Multiple Choice`、`Rating scale`、`NPS`、`Matrix`、`Verbal response`、`Ranking`

## 5. 一次说清一件事

题干不要堆叠。玩家不需要"阅读理解"，扫一眼就该懂。

- 一个题干聚焦一个核心问题
- 追问用破折号或分句自然带出，不要写成编号列表（除非确实有多个并列项）
- 长句拆短句

## 6. 只本地化玩家可见部分

**玩家可见**：Instruction text、Navigation task instructions、Question Page 标题、页面引导语、题干、选项、Scale Labels。

**内部参考**（保持原样，不润色）：研究落点、内部备注、研究假设、附录 RQ、主持人提醒、判定规则。

理由：内部参考是给研究团队看的，需要的是**精确**，不是地道的玩家语言。把它们也翻成口语，反而丢掉研究团队需要的术语。

## 7. 英文版必须是纯英文

英文版文档里**不能残留任何汉字和中文标点**（`，。；：、（）《》`等）。

包括：章节序号（`一、二、三` → `1. 2. 3.`）、括号里的中文说明（`(内部定稿)` → `(the Chinese-language draft)`）、页脚注释。

> 非 ASCII 的英文标点和数学符号（`·`、`—`、`｜`、`≥`、`≤`）是合法的，不用清。

## 8. 中英语义对齐

中文版和英文版是**同一份文档的两个语言版本**，结构必须一一对应：

- 题号数量一致
- 每题的题型一致
- 选项数量一致
- 量表端点一致

英文版为了本地化会调整措辞，但**语义不能跑偏**。若英文版动了语义（不只是措辞），必须回写中文版。

## 9. 语气与场景匹配

这是 Think-Out-Loud 无人主持测试，玩家要边玩边说。语言要：

- **鼓励**：让玩家放心说出真实想法（`There's no wrong way to put it.`）
- **不施压**：`no right or wrong`、`don't worry about...`
- **清楚**：`1 means definitely not, 7 means definitely yes.`

## 10. 贴住中文的原意，不贴中文的句式

第 1 节说的"不直译"针对的是**句式**，不是**语义**。这一轮返工暴露了反方向的毛病：
英文读着顺，形容词和动词却换了档——中文说"乱、不好看清"，英文写成 `a bit messy` 就把语气削掉；
中文说"合不出订单要的东西"，英文泛化成 `items`，指代就糊了。
顺口与贴意冲突时，**先贴意，再顺口**。

自检办法：把英文回译成中文，跟定稿比。少了程度、动作或对象，或者多出中文没下的判断，就是跑偏。

这一轮的实例（中文定稿 → 旧英文 → 现在用）：

| 中文 | 旧英文 | 现在用 |
|---|---|---|
| 手感怎么样（会不会拖不动、放不准、不好对齐） | how does it feel — does it drag properly, land where you want it, line up easily? | how does it feel — do they not drag properly, are they hard to place accurately, or are they hard to align? |
| 这个棋盘显得乱而且不好看清 | The board is a bit messy and hard to see clearly | The board feels cluttered and is hard to see clearly |
| 我清楚棋盘上可摆放的棋子有上限 | I'm clear that the board can only hold so many items | I am aware that there is a limit to the number of items that can be placed on the board |
| 棋子分不清 / 合成链路看不懂 | The items are hard to tell apart and the merge chain is hard to follow | Items are hard to tell apart / the merge chain is hard to understand |
| 游乐场 | carnival | amusement park |

三条纪律：

- 中文的语气与否定（"有点""不太""压根""其实可有可无"）是数据。英文别替它加权，也别替它减权。
- 中文给的是动作就别换成状态词：`把两个相同的棋子拖到一起` 不要写成 `put two matching items together`。
- 中文里的行业词（消耗性道具、战令、通行证）不照字面硬译，但也不许泛化成 `items`——先查 `glossary.md`。

改完英文版，**回译一遍再交付**。这一轮 33 题里有十来处是回译才看得出差别的。
