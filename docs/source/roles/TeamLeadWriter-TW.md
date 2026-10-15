---
orphan: true
---

# 第 3 章 需求详细设计（按高层级需求展开）

> 面向角色：各部门研发负责人。
> 本章对应主文档 `company_doc_init.rst` 第 3 章「需求详细设计」，自**技术写作组（Owner）**视角整理为 **3.1 研发负责人协同视图**。
> 源条目为示例数据，工时与工期为示意口径；各结论后标注来源（本地事实标 `[来源：…]`，外部行业参考标 `[外部参考：…]`），缺失处标「待确认」，不自行补全参数、版本号或指标。

:::{important}
**评估来源与精度说明**

本章引用的工时、工期与选型口径，均来自大模型 **DeepSeek-V4.1-Flash** 评估，属**模型评估**、未经工程验证，仅作决策起点。其中工时为**理论下限**，中位预期约 2 倍，请勿直接当作排期承诺。
[来源：company_doc_init.rst §2 开头 important 块、§3.1.2 note]
:::

## 3.1 研发负责人协同视图（技术写作组 Owner 视角）

:::{note}
本节从 Owner 视角，把四条高层级需求（HL-01 ~ HL-04）拆成「各团队职责 / 模块边界 / 接口契约 / 联调计划 / 性能与稳定性要求 / 风险清单 / 待确认事项」，供各部门研发负责人对照落实。
- 项目级目标 G1-G4、里程碑与干系人见 [第 1 章 · 立项报告](executive.md)；
- 选型结论、工具链与验收硬指标见 [第 2 章 · 技术方案](ManagementWriter.md)；
- 各 HL 的详细属性、优先级与目标版本见主文档 §3.2。
本节不重复上述已列内容，仅从协同视角给出 Owner 对各团队的硬性要求与约定；末尾附「Owner 设计依据（外部参考）」与「参考资源」。

行业背景：本项目落地的是 **Docs as Code（文档即代码）** 工作法——Write the Docs 社区将其核心实践归纳为五项：问题跟踪器、版本控制（Git）、纯文本标记（Markdown / reStructuredText / AsciiDoc）、代码评审、自动化测试；其关键收益之一是「可在未随特性提交文档时**阻断合并**」，把文档纳入研发的「完成定义」。
[外部参考：Write the Docs · Docs as Code]
:::

### 各团队职责

本项目以 HL 为设计粒度（不把 HL 继续拆成 LL）。下表汇总各团队在四条 HL 下的卷入关系，以及 Owner 对该团队的硬性交付要求；主责标「主」。

| 团队 | 关联 HL（主责标「主」） | Owner 对该团队的硬性要求（交付物 / 介入点） |
| --- | --- | --- |
| 技术写作组（Owner，本文视角） | 全部（主） | 搭内核与流水线、定模板与规范、编排内容、把关发布与回滚；定义各团队职责边界与接口契约 |
| 研发部 | HL-01 / HL-02（主） / HL-03 / HL-04 | 补 Doxygen 注释至可生成（全项目最大变量）；主导 HLD / API / 安装部署模板；以 PR 提交文档变更、参与三方评审 |
| 测试质量部 | HL-01 / HL-02 / HL-03 / HL-04 | 作为集成测试主管参与三方评审，校验操作步骤与接口文档一致性、验收标准可测性 |
| 产品部 | HL-01 / HL-02（主） / HL-04 | 主导需求模板内容；组织需求文档目录与盘点 |
| 运维 SRE | HL-01 / HL-02 / HL-03 / HL-04 | 提供托管 / CI 环境 / 内网镜像 / SSO；定义安装部署模板中部署与回滚部分 |
| 客户支持 | HL-02（主） / HL-04 | 主导 FAQ / 排障模板；提供对外 FAQ 素材 |
| 市场售前 | HL-02 / HL-04 | 提供对外 API 清单与 Release Notes 写法；配合对外文档脱敏迁移 |
| HR 新人培训 | HL-04（主） | 定义 3-5 天 onboarding 路径与检查点 |
| 管理层 PMO | HL-01 / HL-02 / HL-03 / HL-04 | 批平台选型与预算、批模板 / 规范、批重大发布放行或回滚、批迁移优先级 |

[来源：company_doc_init.rst §3.1.2 各 HL 受影响角色与工时表、§3.2 各角色节]

> 上表「可能工时」合计 43 人日，为**技术写作组（1 名专职文档工程师）**的示意下限，落在第 2 章 L3「40-45 人日」区间；各业务团队的投入为配合性工作量，未单列，待 PMO 与各团队确认。
> [来源：company_doc_init.rst §3.1.2 note]

### 模块边界

Owner 负责划清以下边界，避免各团队迁入后口径不一致、二次返工：

1. **目录结构边界**：统一「类型 / 模块 / 版本」三层目录树与命名规范（对应 LL-001 / LL-002 / LL-004~009），**先于迁入发布**，由目录 lint 脚本在 CI 强制校验。各团队按规范组织本领域目录，不得自定层级。
   [来源：company_doc_init.rst §3.2.1.1、§3.2.1.4]
2. **内容与格式边界**：模板的**格式与元数据**由 Owner 编排；**内容由各主责部门出**，Owner 不替业务部门写内容。职责边界写进模板说明，防止 Owner 被当成「代写内容」。
   [来源：company_doc_init.rst §3.2.2.1 风险]
3. **六类文档边界**：需求 / 设计 HLD / API 参考 / 用户与操作手册 / 安装部署 / 发布说明与 FAQ，各出一套模板，互不混用。
   [来源：company_doc_init.rst §3.2.2 场景]
4. **权限边界**：三级（公开 / 内部 / 机密）落在**托管层**，Sphinx 构建产物本身不分级；敏感文档不得直接提交公开仓库，入库前过权限检查清单。
   [来源：company_doc_init.rst §3.2.1.1 风险、§3.2.1.3]

### 接口契约

团队与流水线之间的契约（即「怎么跟文档库打交道」），由 Owner 统一制定并写进门禁：

- **变更提交契约**：文档变更以 PR 形式提交，评审记录留在 PR 上，全程可追溯；不经评审不得合入。这对应 Docs as Code 的「代码评审」实践，也是「未带文档可阻断合并」的落地方式。
  [来源：company_doc_init.rst §3.2.3 做法；外部参考：Write the Docs · Docs as Code]
- **CI 门禁契约**：`sphinx-build -W`（构建 0 告警）＋ 死链校验 ＋ 元数据必填；**不过门禁不进评审**，把格式问题拦在评审之前。业界 Docs as Code 落地普遍把「链接检查 / 拼写 / 样式 lint / 构建」放进 CI，作为质量关卡，人审只聚焦机器抓不到的准确性与叙事。
  [来源：company_doc_init.rst §3.2.3.1、§3.2.3.2；外部参考：Young Copy · Docs as Code 卡点、Ivan Walsh · Docs-as-Code]
- **三方评审契约**：领域技术主管（研发） / 集成测试主管（测试质量部） / 关联模块 Owner（技术写作组）三方评审通过后才合并发布。
  [来源：company_doc_init.rst §3.2.3 做法]
- **元数据契约**：`owner` / `version` / `status` / `评审记录` 四字段必填，进 CI 门禁，缺项即构建失败——否则「必填」形同虚设。
  [来源：company_doc_init.rst §3.2.2 做法]
- **抽取链契约**：API 符号域必须由**抽取链（Doxygen `GENERATE_XML=YES` → Breathe）**提供；pandoc 只能做「最后一公里」格式搬运，绝不承担跨语义转换，否则函数签名被降级、符号域被抹掉。Breathe 官方说明其「在 Sphinx 与 Doxygen 之间架桥、依赖 Doxygen 的 XML 输出」；Doxygen 侧须设 `GENERATE_XML = YES`（而非 HTML/LATEX）才能产出可被 Breathe 消费的 XML。
  [来源：company_doc_init.rst §3.2.3.1 风险、§3.2.4.1 风险；外部参考：Breathe 文档、Doxygen]

### 联调计划

按「四步搭建法」推进，各团队在不同阶段接入（完整节点见 [第 1 章](executive.md) §4）：

- **阶段一 · 打地基**：目录规范与命名规范先行发布，各团队按规范组织目录；此阶段未发布规范前不得批量迁入。
  [来源：company_doc_init.rst §3.2.1]
- **阶段二 · 通链路**：抽取链打通后，研发部按统一 Doxygen 注释规范补齐注释，Owner 产出首批 API 参考页；以 `objects.inv` 中 C/C++ 域符号覆盖率为联调通过判据。
  [来源：company_doc_init.rst §3.2.2.2、§3.2.3.1]
- **阶段三 · 建流水线**：PR → CI 门禁 → 三方评审 → 自动发布；研发部与测试质量部正式介入评审，门禁须能拦下死链与元数据缺失。
  [来源：company_doc_init.rst §3.2.3]
- **阶段四 · 产内容与迁移**：六类模板铺开、存量迁移入库，HR 定义 onboarding 路径。
  [来源：company_doc_init.rst §3.2.4]

**联调关键节点**：回滚演练成功一次；门禁能拦下死链与元数据缺失——二者通过即流水线 v1.0 达成。
[来源：company_doc_init.rst §2.2.1.3、§3.2.3.1]

### 性能与稳定性要求

Owner 对各团队提出以下硬性要求（完整技术侧验收指标见 [第 2 章](ManagementWriter.md) 验收标准）：

- **构建 0 告警**：`sphinx-build -W` 把告警当错误，死链 / 交叉引用失效 / 标题层级错误在合并前被拦。
  [来源：company_doc_init.rst §3.2.3 做法]
- **API 符号域硬指标（HL-03）**：解压 `objects.inv` 后，`c:` / `cpp:` 域符号数 **> 0** 且覆盖该模块 **100% 公开发布符号**；不能只看「文件是否存在」。技术依据：Sphinx 每次 HTML 构建都会生成 `objects.inv`，它正是「对象名 → 相对 URI」的映射清单；`intersphinx` 扩展正是靠解析它来跨项目链接，因此**解压后按域统计符号数**是验证 API 是否真正进入符号体系的硬手段（非空文件不等于有编程域符号）。
  [来源：company_doc_init.rst §3.2.3 note；外部参考：Sphinx · sphinx.ext.intersphinx]
- **发布可回滚**：每次发布留快照，重大发布走 Phase Gate，放行或回滚有据可查。
  [来源：company_doc_init.rst §3.2.3.1]
- **CI 环境稳定**：固定构建镜像与依赖版本，内网镜像兜底，失败可重跑。
  [来源：company_doc_init.rst §3.2.3.4 风险]
- **权限分级生效**：公开 / 内部 / 机密三级在托管层落地；目录 lint 通过。
  [来源：company_doc_init.rst §3.2.1 验收、§3.2.1.1]

### 风险清单

| 风险 / 问题 | 影响方 | Owner 视角的解法 | 关联需求 |
| --- | --- | --- | --- |
| 注释补齐是最大变量：API 自动生成依赖 Doxygen 注释规范 | 研发部 | 模板先行＋统一注释规范＋设覆盖率基线，由研发侧排期推动 | HL-02 / HL-03 |
| pandoc 位置错，函数签名降级、符号域被抹掉 | 技术写作组 / 研发部 | 语义由抽取链（Doxygen XML + Breathe）提供，pandoc 只做格式搬运 | HL-03 / HL-04 |
| 文档与实现不一致难发现 | 研发部 / 测试质量部 | 三方评审时对照构建产物与接口文档逐项核对，记录留存于 PR | HL-03 |
| CI 环境不稳定、构建偶发失败 | 运维 SRE | 固定构建镜像与依赖版本，内网镜像兜底，失败可重跑 | HL-03 |
| 敏感文档误入公开库 | 技术写作组 / 运维 SRE | 三级权限由 nginx + SSO 落地；入库前过权限检查清单，敏感文档不进公开库 | HL-01 |
| 研发迁入意愿低、进度慢 | 研发部 | 目录规范明确「单一真源」；未入库网盘副本不视为正式文档，迁入纳入里程碑考核 | HL-01 |
| 技术文档藏个人电脑，盘点清单难完整 | 研发部 | 以代码库 / 构建产物反查依赖文档，Owner 牵头逐团队核对 | HL-04 |
| 对外文档混入内部信息 | 市场售前 / 客户支持 | 对外单独模板＋发布前脱敏检查，三级权限把关 | HL-02 / HL-04 |
| 部署文档与实际环境漂移 | 运维 SRE | 步骤由运维亲自维护，变更走 PR 评审，与 HL-03 流水线联动 | HL-02 |
| 该迁的没迁 / 迁了一堆垃圾 | 技术写作组 / PMO | 盘点覆盖全部存量来源，三级判定「弃」须留理由 | HL-04 |

[来源：company_doc_init.rst §3.2 各节风险表]

### 待确认事项

1. **预算与专职人力**：是否配备专职文档岗直接决定工期（专职 L3 约 40-45 人日，兼职 2-2.5 倍），待 PMO 确认编制与预算。
   [来源：company_doc_init.rst §2.2.1.3、§3.1.2 note]
2. **权限分级策略**：公开 / 内部 / 机密三级如何界定，机密档是否本期落地（建议先落公开 / 内部两档）。
   [来源：company_doc_init.rst §3.2.1.1]
3. **检索门户是否后置、何时启动**：起步用 Sphinx 自带静态站，Next.js 门户（需前端资源）可后置，待确认时点。
   [来源：company_doc_init.rst §2.1.1]
4. **存量迁移优先级与资源**：以盘点报告留 / 改 / 弃清单与工作量估算，一次性确定优先级与投入。
   [来源：company_doc_init.rst §3.2.4.9]
5. **各 HL 目标版本起止时间**：R1 / R2 / R3 当前为示意（2026-Q4 / 2027-Q1 / 2027-Q2），待确认真实排期。
   [来源：company_doc_init.rst §3.2 各属性表]
6. **三方评审人选与授权**：「领域技术主管 / 集成测试主管 / 关联模块 Owner」具体人选与放行授权待定。
   [来源：company_doc_init.rst §3.2.3 做法]
7. **基础设施就绪度**：内网 PyPI / npm 镜像是否已就绪、SSO 分组方案待运维 SRE 确认。
   [来源：company_doc_init.rst §3.2.1.3]

### Owner 设计依据（外部参考）

本节汇总本地主文档未展开、但 Owner 据以定契约的行业依据，便于研发负责人理解「为什么这样要求」：

- **Docs as Code 五项实践**：问题跟踪器、版本控制（Git）、纯文本标记（Markdown / reStructuredText / AsciiDoc）、代码评审、自动化测试；并把「未随特性提交文档即可阻断合并」作为「文档完成定义」的一部分。
  [外部参考：Write the Docs · Docs as Code]
- **抽取链路机制**：Breathe 在 Sphinx 与 Doxygen 之间架桥、依赖 Doxygen 的 XML 输出；Doxygen 须 `GENERATE_XML = YES` 产出 XML（而非 HTML/LATEX）。本项目统一注释与抽取规范，正是为了让 API 符号进入 Sphinx 的 `c:` / `cpp:` 域、可被 `intersphinx` 跨项目引用。
  [外部参考：Breathe 文档、Doxygen、Sphinx · sphinx.ext.intersphinx]
- **写作格式选择**：本项目用 MyST（Markdown 子集）写 Sphinx 源，可通过 `:::{note}` 等原生指令写提示框、用 Markdown 相对链接做跨页引用；与第 1、2 章保持一致。
  [外部参考：MyST-Parser 文档]
- **CI 即质量门禁**：业界 Docs as Code 落地把链接检查、样式 lint、构建放进 CI，失败即阻断发布；人审聚焦准确性。本项目 `sphinx-build -W` ＋ 死链 ＋ 元数据门禁即此实践。
  [外部参考：Young Copy · Docs as Code 卡点、Ivan Walsh · Docs-as-Code]

### 参考资源

> 以下为 Owner 撰写本视图时引用的外部权威资料（非本项目内部文档，仅供研发负责人进一步查阅；链接有效性以访问时为准）。

- Write the Docs · Docs as Code（五项实践与「阻断合并」收益）：<https://www.writethedocs.org/guide/docs-as-code/>
- Breathe 官方文档（Doxygen XML → Sphinx 桥接、指令与配置）：<https://breathe.readthedocs.io/en/latest/>
- Doxygen 官网（GENERATE_XML 等配置）：<https://www.doxygen.nl/index.html>
- MyST-Parser 文档（用 Markdown 写 Sphinx、指令与提示框语法）：<https://myst-parser.readthedocs.io/en/latest/>
- Sphinx · sphinx.ext.intersphinx（objects.inv 机制与跨项目引用）：<https://www.sphinx-doc.org/en/master/ext/intersphinx.html>
- Sphinx 总文档（C/C++ 域等核心能力）：<https://www.sphinx-doc.org/en/master/>
- Young Copy · Docs as Code 为何卡住（评审 / 构建 / 发布归属）：<https://www.youngcopy.com/blog/docs-as-code-why-teams-get-stuck>
- Ivan Walsh · Docs-as-Code（CI lint/build 门禁、完成定义含文档）：<https://ivanwalsh.com/tutorial-basics/docs-as-code/>

:::{note}
所有工时与工期为**示例估算口径（理论下限）**，按 1 名专职文档工程师计，合计约 43 人日（落在 L3 区间）；实际中位预期约 2 倍，兼职岗按 2-2.5 倍估算，**请勿当作排期承诺**。完整 LL 拆分（demo）见主文档子页面 `company_doc_init_spec`。
[来源：company_doc_init.rst §3.1.2 note]
:::
