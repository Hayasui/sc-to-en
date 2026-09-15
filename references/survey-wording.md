# 英文问卷用语表（量表端点 · 固定选项标签）

**这份表是量表端点与固定选项标签的唯一出处。** 别处只写指向这里的一句话，不要另抄一份。
2026-09-14 出过一次事故：同一个端点在六个文件里各留了一份，其中五份写着错词
（`Very unsatisfied` 应为 `Very dissatisfied`），改一处漏五处。要改就改这里。

**中文列只为对照。** 中文标签的写法归 `adaptor`（中文定稿的源头），本表不裁决中文。

## 〇、先说清楚：没有"唯一权威的完整英文问卷用语表"

这行里不存在这样一份东西。实际是四块来源各管一段，本表按下面的优先级取用：

| 优先级 | 来源 | 管什么 |
|---|---|---|
| 1 | UserTesting 官方帮助文档 | 平台能配成什么样（量程、标签个数、题型）——见同目录 `platform-constraints.md` |
| 2 | Reichheld / Bain 的 NPS 原始定义 | NPS 的措辞与分档 |
| 3 | NN/g、SurveyMonkey、Qualtrics 这类方法论页 | 各类量表的锚点措辞、固定选项标签 |
| 4 | 项目自定 | 上面没覆盖到的（如"玩不玩"的可能性）——本表逐行标注 |

两条使用纪律：

- **厂商页也会写错。** Qualtrics 自己的 CSAT 页面写着 `Very unsatisfied`，与它别处的 `Very dissatisfied` 自相矛盾。引用时认措辞，不认页面。
- **没有现成的中英对照表可抄。** ISO 20252:2019 只定义流程术语（questionnaire、participant 这类），不含量表文字，也没有中英双语版；行业里找不到可援引的问卷术语双语表。本表的中文列是我们自己填的。

## 一、平台结构规则（硬约束）

| 项 | 规则 |
|---|---|
| Rating scale · Numeric 型 | 官方写的量程是 **-3 到 10**，所以 **1-7、1-10 都合法**，不受"必须是奇数点"约束 |
| Rating scale · Customized 型 | 标签个数上限 **7** |
| Matrix | 列的量程同为 **-3 到 10**，Customized 标签上限 **7** |
| NPS | **独立题型**，固定 **0-10**（推荐者 9-10 / 被动者 7-8 / 贬损者 0-6）；Scale Labels 可写可不写，写就低端 `0`、高端 `10` |
| 端点 | 两端都要写明；**1 是不好的一端，最大数是好的一端** |

> **关于"可选 5 / 7 / 9 / 11 点"**：那句话来自**旧平台**的帮助页，与现在的后台不是一套产品。
> 「1 永远是不好的一端」这句也只写在旧平台文档里，新平台的配置页没有重述——项目沿用。
> 引用平台规则前先分清是哪一代。

## 二、量表端点（项目在用五套）

**2026-09-15 全面改版**：区间由 1-10（Matrix 1-5）统一为 **1-7**（NPS 仍 0-10），
满意度的低端由 `Very dissatisfied` 升到 `Extremely dissatisfied`，NPS 开始写 Scale Labels。
改版的理由是统计口径：1-10 的双数点没有真正的中点，4 与 6 分居两侧；1-7 的 4 是重心，
也不会把满意度压在量表正中间。

| 量表 | 中文标签 | 英文端点（现用） | 出处 | 备注 |
|---|---|---|---|---|
| 满意度（1-7） | 1 = 非常不满意 ｜ 7 = 非常满意 | **1 = Extremely dissatisfied** ｜ **7 = Extremely satisfied** | 双极端点：Iowa DxTraining；词汇区分见 medscicommunications | 两端强度对称。1-10 时代"Very ↔ Extremely 不对称"的保留意见到此结束 |
| 继续玩的可能性（1-7） | 1 = 肯定不会玩 ｜ 7 = 肯定会玩 | **1 = Definitely won't play** ｜ **7 = Definitely will play** | **项目自定**（贴"玩不玩"的题面） | 平台样例与 SurveyMonkey 用 `Not at all likely` → `Extremely likely`；题面问的是"明天还玩不玩"，`play` 比 `likely` 贴题，保留 |
| 同意度 Matrix（1-7） | 1 = 很不同意 ｜ 7 = 很同意 | **1 = Strongly disagree** ｜ **7 = Strongly agree** | NN/g、SurveyMonkey | 与权威一致 |
| 喜好度（1-7） | 1 = 非常不喜欢 ｜ 7 = 非常喜欢 | **1 = Dislike it a lot** ｜ **7 = Like it a lot** | **项目自定** | 权威来源里**没有** "liking" 量表；最接近的是 importance 的 `Not at all important` → `Extremely important`。以后别把它当权威照抄 |
| NPS（0-10） | 0 = 不可能推荐 ｜ 10 = 特别可能会推荐 | **0 = Not likely at all** ｜ **10 = Extremely likely** | 平台样例、SurveyMonkey | 2026-09-15 起项目在 NPS 上也写标签；**低端必须写 0**，写成 1 会被 lint 拦下 |

> **有人版不写 Scale Labels。** 有人版由主持人把端点念在题干里。2026-09-15 起**只留一套念法**：
> 满意度念 `1 is extremely dissatisfied, 7 is extremely satisfied.`，可能性念
> `1 means definitely not, 7 means definitely yes.`，喜好度只念区间 `on a scale of 1 to 7`。
> 旧裁决里"Q10/Q11 念 `1 is the lowest, 10 is the highest.`、与 Q17/Q23/Q25 两套并存"的做法作废。

## 三、固定选项标签

| 中文 | 英文 | 出处 | 备注 |
|---|---|---|---|
| 其他 | **Other** | 平台（只认这个与 `None of the above`） | 英文侧只写 `Other`，不写 `Other (please specify)`。**中文侧 2026-09-15 改写成「其他（请说明）」/「其他游戏（请说明）」**，与 lint 的 `FORBIDDEN_PROMPTS`（拦「请说明」）冲突，待裁决；英文列不受影响 |
| 以上皆无 | **None of the above** | 平台 | |
| 不愿回答（未用到） | **Prefer not to answer** | NN/g；Google Surveys 作 `I prefer not to say` | 涉及敏感信息时可加 |
| 不适用 / 不知道 / 想不起来（未用到） | **Not applicable** / **I don't know** / **I don't recall** | NN/g | 备选 |

NN/g 明列的整套是 `Not applicable / None of the above / I don't know / I don't recall / Other / Prefer not to answer`。项目目前只用了前两项，其余留作备选。

## 四、口径

- Rating scale 与 Matrix 全篇 **1-7**；**NPS 是独立题型、固定 0-10**，标签低端写 `0`。不混用。
- 题型列只写中文简述，**不标区间**。
- **两份英文稿要一起改。** 2026-09-14 出现过分叉：无人版改成了 `Very dissatisfied`，有人版还留着 `Very unsatisfied`——起因就是单边改。
- **端点的唯一出处是本表。** 中英文定稿里出现端点，一律照抄，别在项目文件里另写一套。

## 五、出处

- UserTesting 帮助页：Rating scale / Matrix 配置 `help.usertesting.com/hc/en-us/articles/360000673097`；
  Matrix `360000661578`；NPS 分析页 `help.usertesting.com/hc/articles/360000662078`；
  旧平台的量表点数说明 `115003377872`。
- NPS 原始定义：Reichheld《The One Number You Need to Grow》，HBR 2003（Bain 的净推荐值）。
- 锚点措辞：NN/g `nngroup.com/articles/survey-best-practices`；
  SurveyMonkey `surveymonkey.com/mp/likert-scale`；
  双极 5 点满意度另见 Iowa DxTraining 的 `rating-scales-best-practices`（次级来源）。
- 词汇区分（satisfied / dissatisfied / unsatisfied）：`medscicommunications.com/?p=1119`。
  反例（厂商页写错）：Qualtrics UK 站 CSAT 页 `what-is-csat`。
- 固定选项标签：NN/g 同上；Google Surveys `support.google.com/surveys/answer/7380083`。
- 流程术语：ISO 20252:2019 `iso.org/standard/73671.html`（**不含量表文字，无中英对照**）。

> 其中两处链接只记到站点与页面名（Iowa DxTraining、Qualtrics CSAT），下次要用时复检一次。

## 六、待办

- **lint 校验（已定，未实现）**：把 `check_scale_labels()` 从"只查有没有"升到"查端点是否落在本表内"。
  定为 **WARN 级**——不报 ERROR，免得新增端点被逼着绕过检查；白名单从本表生成，
  表是唯一出处，改表即改检查。对应 `roadmap.md` 的第 6 项。
