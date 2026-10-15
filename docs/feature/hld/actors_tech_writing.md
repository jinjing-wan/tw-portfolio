# 参与者 · 技术写作组（Owner）

:::{note}
本页为「公司文档初始化项目」参与者页面之一：**技术写作组（全局 Owner）**。
按底层级需求（LL）逐条列出该角色有实际职责的部分与具体做什么；无职责 / 仅消费的 LL 不列。
「主」表示该 LL 的主责模块。条目为示例数据；脚本全文见对应 HLD 页面。
:::

## 1. 角色定位

全局 Owner：搭内核与流水线、定模板与规范、编排内容、把关发布与回滚。是唯一贯穿全部 12 条底层级需求（LL）的建设者。

## 2. 在各底层级需求（LL）中的职责

| LL | 具体做什么 |
| --- | --- |
| LL-001 | 选型并搭建集中文档存储（Git 仓库 + 静态站点），制定接入指南 |
| LL-002 | 制定顶层目录树与命名约定，发布规范与检查清单 |
| LL-003 | 定义权限模型与角色（读者/作者/审核者/管理员）并落地到平台 |
| LL-004 | 编排需求模板格式与元数据并发布到库 |
| LL-005 | 编排 HLD 模板格式并入库 |
| LL-006 | 编排 API 模板并接入自动生成 |
| LL-007（主） | 主导手册模板（用户/操作/运维手册） |
| LL-008 | 编排安装部署模板并入库 |
| LL-009 | 定义发布说明/FAQ 模板 + 元数据规范（owner/version/status/review） |
| LL-010 | 搭建 PR 评审 + CI 构建 + 静态站发布 + 双版本对比 + 追溯回滚全链路 |
| LL-011 | 牵头盘点、评估、制定迁移计划并按模板迁移 |
| LL-012 | 提供手册与 FAQ 作为 onboarding 路径素材 |

## 3. 具体操作与配置

- **HL-01**：`git init` + `sphinx-quickstart` + 目录 lint（`scripts/check_doc_layout.py`），见 [hl01 §9](hl01_unified_repo.md#9-脚本与配置)；
- **HL-02**：元数据校验 `scripts/check_metadata.py`，见 [hl02 §9](hl02_templates.md#9-脚本与配置)；
- **HL-03**：CI 流水线 `.github/workflows/docs.yml` + `objects.inv` 验收，见 [hl03 §9](hl03_pipeline.md#9-脚本与配置)；
- **HL-04**：盘点 `scripts/inventory_docs.py` + pandoc 搬运，见 [hl04 §9](hl04_migration.md#9-脚本与配置)。

## 4. 上下文链接

- 项目总览：[overview.md](overview.md)
- 四条 HL 设计：[hl01](hl01_unified_repo.md) · [hl02](hl02_templates.md) · [hl03](hl03_pipeline.md) · [hl04](hl04_migration.md)
- 上游需求：[company_doc_init_spec.rst](../company_doc_init_spec.rst)
- 书写规范与提示词：[hld_writing_guide.md](hld_writing_guide.md)
