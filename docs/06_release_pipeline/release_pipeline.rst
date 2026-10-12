文档发布流水线（版本锁定 vs 常青滚动）
=======================================================

本文给出 Docs-as-Code 体系下的文档发版策略：在 Docs-as-Code 体系里， **不是所有文档都该跟着代码逐个 release 发** 。
把文档按"是否强绑定该版本代码行为"分流到两条流水线，能避免两类典型事故——
"文档写着 v2、代码还是 v1"（版本错配），以及"常青内容被无谓地重复打版"（维护浪费）。

.. note::
   本页用 **纯 reStructuredText 原生写法（ASCII 流程图 + list-table）** 呈现，
   在仅依赖 ``sphinx>=7.0``（``extensions = []``、无 Graphviz 二进制）的环境下零依赖即可构建。
   文末附等价的 Graphviz 图形源码，加入对应扩展后可替换 ASCII 版本。

1. 判定原则（一条规则分天下）
-----------------------------------------------

.. code-block:: text

   这份文档的内容，是不是由该版本代码 / 工具链直接生成，或强绑定该版本的运行时行为？

   ├─ 是  → 必须跟随代码，单个 release 发（错一版就误导用户）
   └─ 否  → 可以常青（evergreen）滚动，跨多个 release 混在一份里，
             用版本徽标 / 选择器隔离差异

2. 两条流水线（图）
-----------------------------------------------

.. code-block:: text

   代码 Release Tag（触发）
           │
           ├──────────────────────────────┐
           ▼                              ▼
   A. 版本锁定流水线                B. 常青滚动流水线
      （单 release 发）               （多 release 混发）
      │                              │
      ├─ 发布说明 / Release Notes    ├─ 安装 / Quick Start
      ├─ API 参考（代码生成）         ├─ 编程指南（+版本化附录）
      ├─ 库文档 muBLAS 等            └─ Musify 移植指南
      ├─ 工具 / Tools
      ├─ mcc 编译器
      └─ 性能 / 性能优化
           │                              │
           ▼                              ▼
      打包：该 release 文档包        增量更新：单份常青文档
      （含全量 API Ref / 库 /        + 适用版本徽标 / 选择器
       工具 / 编译器 / 性能）
           │                              │
           └──────────────┬───────────────┘
                          ▼
               文档站点发布（版本下拉 ·
               单版页面由对应代码生成）

3. 文档分类明细
-----------------------------------------------

.. list-table:: 各文档发版策略与判定理由
   :header-rows: 1
   :widths: 30 20 50

   * - 文档
     - 发版策略
     - 判定理由
   * - 发布说明 / Release Notes
     - 单 release ⛔
     - 本质就是该版本变更清单，无法合并到别的版本
   * - API 参考
     - 单 release ⛔
     - 由代码抽取生成，函数签名 / 枚举 / 行为须与该版二进制逐字一致
   * - 库文档（muBLAS 等）
     - 单 release ⛔
     - 库 API 表面、精度、kernel 行为随版本演进，下游按版编译链接
   * - 工具 / Tools
     - 单 release ⛔
     - CLI 参数、输出格式、退出码随版本变化
   * - mcc 编译器
     - 单 release ⛔
     - 编译选项、intrinsic、诊断信息、ABI 逐版变化
   * - 性能 / 性能优化
     - 单 release ⛔
     - benchmark 数字、新优化特性、调优开关都是逐版实测结果，合并会失真
   * - 安装 / Quick Start
     - 可混发 ✅
     - 装驱动、设环境变量、跑 deviceQuery 等步骤跨小版本基本不变
   * - 编程指南
     - 可混发（带版本附录）🔶
     - 编程模型 / 内存层次 / 执行模型稳定；新增特性章节作为版本化附录挂载，不写死进正文
   * - Musify 移植指南
     - 可混发 ✅
     - 是"CUDA → 自有架构"的移植方法论，概念跨版本通用

4. 实操要点
-----------------------------------------------

- **拆两条 CI 流水线** ：A 类（Release Notes / API / 库 / 工具 / 编译器 / 性能）随代码 tag 自动抽取打包；B 类（安装 / 编程指南 / 移植指南）走独立常青流水线，增量更新。
- **常青文档也必须带版本锚点** ：即便混发，版本相关语句要标范围（如"自 MUSA 2.4 起支持"），某版本改了依赖就在该页加版本提示框，而不是另开新文档。
- **API 参考的"混发"是假象** ：多数文档站把 API 参考做成带版本下拉的同一站点，但 **底层每个版本页面仍由该版代码单独生成** ——打包粒度上，单 release 文档包必须含该版全量 API Ref，不能用上一版凑数。
- **发布门禁对齐 Phase Gate** ：北向接口契约变更，文档须与代码同版本发布，避免版本错配（详见 ``methodology`` §5）。

5. 升级为图形化图表（可选）
-----------------------------------------------

本页为保持"零依赖可构建"刻意使用 ASCII + list-table。若在 ``conf.py`` 加入
``sphinx.ext.graphviz``（需系统安装 Graphviz 的 ``dot`` 二进制）或 ``sphinxcontrib.mermaid``，
可将 §2 的 ASCII 流程图替换为下方等价源码：

.. code-block:: dot

   digraph release_pipeline {
       rankdir=TB;
       node [shape=box, style=rounded];

       trigger [label="代码 Release Tag（触发）", shape=ellipse];

       subgraph clusterA {
           label="A. 版本锁定流水线（单 release 发）";
           color=blue;
           rn  [label="发布说明 / Release Notes"];
           api [label="API 参考（代码生成）"];
           lib [label="库文档 muBLAS 等"];
           tool [label="工具 / Tools"];
           cc  [label="mcc 编译器"];
           perf [label="性能 / 性能优化"];
       }

       subgraph clusterB {
           label="B. 常青滚动流水线（多 release 混发）";
           color=green;
           inst [label="安装 / Quick Start"];
           pg   [label="编程指南（+版本化附录）"];
           port [label="Musify 移植指南"];
       }

       apkg [label="打包：该 release 文档包（全量 API Ref/库/工具/编译器/性能）"];
       bpkg [label="增量更新：单份常青文档 + 版本徽标"];
       pub  [label="文档站点发布（版本下拉）", shape=ellipse];

       trigger -> rn; trigger -> inst;
       rn -> api -> lib -> tool -> cc -> perf -> apkg;
       inst -> pg -> port -> bpkg;
       apkg -> pub; bpkg -> pub;
   }

.. tip::
   纯 rST 版本（本页当前形态）零依赖即可构建；
   图形化版本需先加入对应 Sphinx 扩展与二进制，否则会破坏"零依赖可构建"的前提。
