# 高层级设计（项目级 / Epic 级）书写规范与提示词

> 本文沉淀「**项目级 / Epic 级 HLD**」的书写方法——即**一条高层级需求（HL）**如何写成一页
> 可评审、可落地、可验收的设计页，以及**每个参与者**如何单独成页。
> 可作为可复用提示词直接喂给 AI，生成或重写同类页面。
> 样例见本目录：`overview.md`（总览）、`hl01~hl04_*.md`（四条 HL）、`actors_*.md`（九个参与者）。

---

## 1. 目的与适用边界

**目的**：把一条高层级需求（Epic）从「做什么」下沉到「怎么做」——给出模块交互、每个角色的
输入输出、调用的接口与工具（附 reference 链接）、涉及脚本配置时的操作步骤与脚本全文，
使设计可评审、可落地、可验收。

**适用**：项目级 / Epic 级 HLD——一条 HL 一页，多角色协作、多工具、含脚本配置的场景。
**不适用**：单功能 / 单条接口的设计（那是**功能级 HLD**，见 `02_design_docs/hld_writing_guide.md`）。

**与功能级 HLD 的关系**：项目级 HLD 定「谁在什么条件下做什么、用什么工具、产出什么」；
功能级 HLD 定「单功能内的参数、时序、异常与告警」。功能级是项目级的**下钻一层**。

---

## 2. 语言约定（重要）

| 项 | 约定 |
| --- | --- |
| 正文 | **默认中文**（读者是多部门干系人：研发/测试/产品/运维/售前/支持/PMO/HR，非纯工程师） |
| 术语/命令/脚本/文件名 | 保持**英文原文**（`git init`、`sphinx-build`、`check_metadata.py`、`Feature ref`），不翻译 |
| reference 链接 | 指向工具的**英文官方文档**（sphinx-doc.org、pandoc.org 等） |
| 图内文本 | PlantUML 用中文 + `Microsoft YaHei` 字体（`skinparam defaultFontName "Microsoft YaHei"`） |

> 对比：功能级 HLD 正文英文（读者是 SW/RAN 工程师）；项目级 HLD 正文中文（读者是多部门）。
> 两者语言不同，但「不写元描述、公共声明不写进页面、只写可验证事实」的红线一致。

---

## 3. 目录与文件组织

```
docs/feature/hld/
├── overview.md               # 总体架构图 + 导航（一张组件图）
├── hl01~hl04_*.md            # 每条高层级需求一页 HLD
├── actors_*.md               # 每个参与者（角色）一页
├── hld_writing_guide.md      # 本规范（可复用提示词）
└── uml/*.puml                # PlantUML 源码（唯一真相源）
```

渲染：`python scripts/render_uml.py` 把 `uml/*.puml` 渲染到 `docs/_static/uml/*.svg`，
页面用 `![alt](../../_static/uml/<name>.svg)` 引用（hld 目录深两层，前缀是 `../../_static/`）。

---

## 4. HLD 页面骨架（每条 HL 一页，顺序固定）

| # | 区块 | 作用 | 必填 |
| --- | --- | --- | --- |
| 1 | 标题（HL 名称） | 一页一条高层级需求 | 必填 |
| 2 | Requirement Summary 表 | 含 **Feature ref** | 必填 |
| 3 | Purpose | 做什么（一句话） | 必填 |
| 4 | Scope | 包含 / 不包含 | 必填 |
| 5 | Precondition | 前置条件 | 必填 |
| 6 | 参与者与职责 | 只列**有职责**的角色 | 必填 |
| 7 | 交互设计（PlantUML 时序图） | 正常流 + 异常流 | 必填 |
| 8 | 角色输入输出 | 每个角色的输入 / 输出 | 必填 |
| 9 | 调用的接口与工具 | **含 reference 链接** | 必填 |
| 10 | 脚本与配置 | 操作步骤 + 脚本全文 | 有脚本则必填 |
| 11 | PostCondition / 验收 | 可验收的终态 | 必填 |
| 12 | Note | 风险 / 坑 | 必填 |
| 13 | Related | 上下文链接 | 必填 |

---

## 5. Requirement Summary 表（含 Feature ref）

**固定字段**，用两列表（`Field | Value`）：

| Field | 填写 |
| --- | --- |
| Requirement ID | HL-xx |
| **Feature ref** | 该 HL 对应的 Feature / Sub-feature 编号（来自需求库，如 `Feature-A / B / C / D / E / F` 或 `HL-03-A~F`） |
| Priority | P0 / P1 / P2 |
| Target Release | R1（2026-Q4）等 |
| Testable | 可测试 / 部分可测试 + 可验证依据 |
| 对应底层级需求 | LL-xxx 列表 |

**硬规则**：`Feature ref` 必须来自需求库的「对应 Feature/Sub-feature」字段，不能凭空写；
它把 HLD 与需求拆分（HL ↔ LL ↔ Feature）串起来，缺了不可追溯。

---

## 6. 参与者页面（每个角色一页）

**核心规则：只列有职责的 LL，无职责 / 仅消费 / 按角色使用的一律不写。**

| 区块 | 写法 |
| --- | --- |
| 角色定位 | 一句话 |
| 职责表 | 两列表 `LL | 具体做什么`，**只列该角色有实际职责的 LL**；主责标「主」 |
| 具体操作与配置 | 有则写命令/配置要点；无则指向对应 HLD 页 |
| 上下文链接 | 相关 HLD 页 + 总览 |

- 无职责的 LL 不写、不占位；若要说明「为什么没列」，最多一行备注（如「LL-003 为按角色使用，不列」）。
- 职责描述**必须标注 LL 编号**，保证「这个角色在哪个 LL 里具体做什么」可定位、可对照 spec。

---

## 7. PlantUML 约定

- **总体图用组件图**（component / package）：角色层 → HL 组件层 → 工具链层，三层关系。
- **每条 HL 用时序图**：参与者至少覆盖该 HL 有职责的角色；`autonumber` 编号；异常分支用 `alt/else` 显式画出。
- 图内文本中文，加 `skinparam defaultFontName "Microsoft YaHei"` 避免方框。
- 渲染：`.puml` 源码入库、SVG 预渲染入库，站点构建不依赖 JVM（见 §3）。

---

## 8. 可复用提示词（直接喂给 AI）

````text
你是写高层级设计（HLD）的文档工程师。按「项目级 / Epic 级 HLD」规范，为下面的高层级需求写一页设计文档（Markdown）。

【语言要求】
- 正文默认中文（读者是多部门干系人：研发/测试/产品/运维/售前/支持/PMO/HR）。
- 工具名/命令/脚本/文件名/参数名保持英文原文（git init、sphinx-build、check_metadata.py、Feature ref），不翻译。
- reference 链接指向英文官方文档。

【不要写进页面的内容】
- 不写「本图展示了一次…」「下面这张图说明…」等元描述；要求转化为图上的分支、表里的行、正文的设计结论。
- 不写「这是样例/作品集/演示」「编号是占位」等元说明；公共声明不进页面。
- 只写该需求的可验证技术内容。

【需求信息】
- 需求编号：HL-xx
- Feature ref：<该 HL 对应的 Feature/Sub-feature 编号，来自需求库，没有则标注缺失并待补>
- Priority / Target Release / Testable：<给出并附可验证依据>
- 对应底层级需求：LL-xxx 列表
- Owner：<邮箱>
- 参与者与职责：<逐角色给出「在哪些 LL 里具体做什么」，只列有职责的，无职责/消费不列，主责标「主」>
- 脚本/配置：<若有，给出操作步骤 + 脚本全文>
- 接口与工具：<列出，并给官方文档 reference 链接>

【强制结构，顺序不可变】
1. 一级标题 = 需求名（HL 名称）
2. Requirement Summary 表（Field|Value），字段固定：Requirement ID / Feature ref / Priority /
   Target Release / Testable / 对应底层级需求
3. Purpose → 一句话
4. Scope → 包含 / 不包含
5. Precondition → 前置条件
6. 参与者与职责 → 表格（角色 | 在本 HLD 中的角色 | 做什么），只列有职责角色
7. 交互设计 → 嵌入 PlantUML 时序图（参与者覆盖有职责角色；alt/else 画异常分支）
8. 角色输入输出 → 表格（角色 | 输入 | 输出）
9. 调用的接口与工具 → 表格（接口/工具 | 用途 | reference 链接）
10. 脚本与配置 → 操作步骤 + 脚本全文（若有）
11. PostCondition / 验收 → 可验收终态
12. Note → 表格（风险/坑 | 说明与处理）
13. Related → 上下文链接（Markdown 相对链接）

【图与文件约定】
- UML 用 PlantUML：源码放 <模块目录>/uml/<name>.puml，渲染为 docs/_static/uml/<name>.svg，
  页面用 ![alt](../../_static/uml/<name>.svg) 引用；图内文本中文 + defaultFontName "Microsoft YaHei"。
- 跨页引用用 Markdown 相对链接（[overview.md](overview.md)），站点与 GitHub 两边都成立。
````

---

## 9. 与功能级 HLD 的关系（对照）

| 维度 | 项目级 HLD（本规范） | 功能级 HLD（02_design_docs/hld_writing_guide.md） |
| --- | --- | --- |
| 粒度 | 一条高层级需求（HL） | 单功能 / 单接口 |
| 读者 | 多部门干系人 | SW / RAN 工程师 |
| 正文语言 | 中文 | 英文 |
| 表头 | 含 Feature ref | 含 Feature / LLR |
| 图 | 组件图（总体）+ 时序图（交互） | 类图（参数）+ 时序图（调用） |
| 核心产出 | 谁在什么条件做什么、用什么工具、产出什么 | 单功能的参数、时序、异常、告警 |

两者通过 **Feature ref / LL 编号** 挂钩：项目级 HL 拆出 LL，功能级 HLD 挂某个 LL 或 Feature。
