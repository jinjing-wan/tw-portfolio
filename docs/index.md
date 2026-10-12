# 曦望 Sunrise · AI 推理 GPU 软件栈开发者文档中心（作品集示例）

:::{note}
本站点为 **曦望 Sunrise AI 推理 GPU 软件栈（开发者文档中心）** 的搭建示例：
由本人在 AI 协助下独立设计并搭建，结构对标 NVIDIA CUDA / 摩尔线程 MUSA 文档站；
全部内容为作品集示例，非曦望内部资料。

站点按交付成熟度分两层：
**HLD / API 参考 / 需求文档 / FAQ** —— 可评审的规范样例，架构分层、接口契约、评审流程由本文档体系产出；
**编程指南 / 库参考 / 工具链 / 性能优化 / 移植指南** —— 体系骨架，章节结构、术语与发布流程由本文档体系负责，
技术内容由曦望领域专家贡献。
:::

## 入门

```{toctree}
:maxdepth: 1

01_getting_started/getting_started
01_getting_started/installation
```

## 设计文档

```{toctree}
:maxdepth: 1

02_design_docs/hld_r1
02_design_docs/hld_r2
02_design_docs/hld_r3
02_design_docs/hld_download_file
02_design_docs/requirements
02_design_docs/hld_writing_guide
```

## 参考

```{toctree}
:maxdepth: 1

03_reference/api_reference
03_reference/libraries
03_reference/tools
```

## 开发实践

```{toctree}
:maxdepth: 1

04_development/programming_guide
04_development/performance_tuning
04_development/porting_guide
```

## 发布与支持

```{toctree}
:maxdepth: 1

05_release_support/release_notes
05_release_support/faq
```

## 文档发布流程

```{toctree}
:maxdepth: 1

06_release_pipeline/release_pipeline
```

## 功能（Feature）

```{toctree}
:maxdepth: 3

feature/company_doc_init
feature/requirements_writing_guide
```

## 变更请求（Change Request）

```{toctree}
:maxdepth: 1

changerequest/change_requests
```

## 关于本文档体系

```{toctree}
:maxdepth: 1

07_about/methodology
```

---

## 关于作者

- 4 年英文技术规范文档撰写与文档体系建设（HLD / 接口规范 / 需求文档），此前 10 年为 C++ 软件研发；
- 7 年项目管理（PMP / Scrum Master），主导跨国跨团队三方 PR 评审，把模块级新人 onboarding 压到 3-5 天；
- 熟悉 Docs-as-Code 全流程（Sphinx + GitHub + CI + 静态站双版本对比评审）；
- 本站点由本人在 AI 协助下独立设计并搭建（Sphinx + MyST 构建、GitHub Actions 自动发布），
  结构对照曦望 AI 推理 GPU 软件栈的开发者文档场景设计。
