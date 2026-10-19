# 示例 · AI 推理 GPU 软件栈开发者文档中心（作品集示例）

> 定位：Docs-as-Code 技术文档体系设计示例（从 0 搭建的 AI 推理 GPU 软件栈开发者文档中心）。
> 作者：在 AI 协助下独立设计并搭建
> 构建方式：Sphinx + Markdown（MyST）+ reStructuredText（Docs-as-Code 全流程，详见 `methodology.rst`）

---

## 这是什么

一个从 0 搭建的**技术文档体系示例**，覆盖三块内容：

1. **Docs-as-Code 全流程**：Sphinx + GitHub + CI，文档与代码同版本管理、走 PR 评审；
2. **面向工程师的规范文档**：HLD（Release 级分层架构 + 功能级单页）、接口规范、需求文档、变更请求；
3. **模块级 onboarding 材料**：把「知识留在个人经验里、新人看不懂」整理为可检索、可评审的文档资产。

---

## 目录结构

```
tw-portfolio/
├── README.md              # 本文件
├── requirements.txt       # 构建依赖（sphinx + myst-parser + mermaid + jdk4py + breathe）
├── scripts/
│   ├── render_uml.py      # 一键渲染 PlantUML（.puml → SVG），jar 首次运行自动获取
│   ├── build_api_docs.sh  # 仅构建「API 文档」独立子工程（api-docs/）
│   └── build_site.sh      # 构建「主站 + API 文档」合并站点（推荐）
├── tools/plantuml/        # PlantUML 引擎（~30MB，不入版本库，脚本自动下载）
├── api/                   # 【私有】C/C++ 示例库源码（头文件 + .cpp，含 Doxygen 注释）；不入库
├── api-docs/              # Doxygen + Breathe + Sphinx 的独立 API 文档子工程
│   ├── Doxyfile           # 仅出 XML（GENERATE_XML=YES）
│   ├── conf.py            # 挂载 breathe
│   └── doxyxml/           # Doxygen 产物（接口文档，可 force-add 发布；不入库默认）
├── docs/
│   ├── conf.py            # Sphinx 配置（MyST 支持 .md；mermaid 本地引擎；breathe 桥接 API）
│   ├── index.md           # 站点首页 / 分组导航
│   ├── _static/mermaid/   # 本地 Mermaid 渲染引擎（离线渲染，不依赖 CDN）
│   ├── _static/uml/       # PlantUML 预渲染产物（SVG，页面直接引用）
│   ├── 01_getting_started/   # 快速开始 / 安装指南
│   ├── 02_design_docs/       # 设计文档
│   │   ├── hld_r1.md / hld_r2.md / hld_r3.md  # Release 级 HLD（分版本演进）
│   │   ├── hld_download_file.md  # 功能级 HLD：Download File to RU（downloadFile API · 含 UML 图）
│   │   ├── hld_writing_guide.md  # 功能级 HLD 书写规范与可复用提示词
│   │   ├── requirements.md       # 需求文档（PRD/MRD 样例）
│   │   └── uml/*.puml            # 上述 HLD 图示的 PlantUML 源码（唯一真相源）
│   ├── 03_reference/         # API 参考 / 库参考 / 工具链（骨架）
│   ├── 04_development/       # 编程指南 / 性能优化 / 移植指南（骨架）
│   ├── 05_release_support/   # 发布说明 / FAQ
│   ├── 06_release_pipeline/  # 文档发布流水线
│   ├── 07_about/             # 文档体系方法论（Docs-as-Code + 三方评审）
│   ├── changerequest/        # 变更请求（Change Request）
│   └── feature/              # 特性规格样例 + 需求文档书写规范（提示词）
└── .nojekyll              # 部署 GitHub Pages 用
```

> **源文件为什么用 `.md`**：Markdown 源文件在 github.com 上可直接阅读
> （表格、代码块、Mermaid 围栏都会原生渲染），评审与浏览阶段都能零门槛查看；
> 站点构建侧由 MyST 负责把它转成正式 HTML。
> 转换按模块**增量推进**：目前设计文档组（`02_design_docs/`）已全部 `.md` 化，其余页面保持 `.rst` 混跑。

---

## 首页导航（对标 CUDA / CUDA-like 文档站结构）
- 入门：快速开始、安装指南
- 设计文档：**HLD（Release 级 3 个版本 + 功能级单页）**、需求文档
- 参考：API 参考、库参考、工具链
- 开发实践：编程指南、性能优化、移植指南
- 发布与支持：发布说明、FAQ
- 关于本文档体系：methodology

> 技术内容板块（编程指南 / 库 / 工具 / 性能 / 移植）为体系骨架：章节结构、术语、评审与发布流程
> 由本文档体系负责，具体技术内容由领域专家贡献。

## 本地构建（3 步）

```bash
# 1. 进虚拟环境（用 WorkBuddy 托管的 python）
"C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/activate"
# 或 Windows:
# C:\Users\Administrator\.workbuddy\binaries\python\envs\default\Scripts\activate.bat

# 2. 装依赖（仅需一次）
pip install -r requirements.txt

# 3. 渲染 HLD 的 UML 图（只在改动过 *.puml 时需要）
python scripts/render_uml.py

# 4. 构建 HTML
cd tw-portfolio
sphinx-build -b html docs docs/_build/html
```

构建产物在 `docs/_build/html/`，浏览器打开 `index.html` 即可本地预览。

> **UML 渲染说明**：`scripts/render_uml.py` 需要 JVM，按 `JAVA_HOME` → `jdk4py`（PyPI 自带 JRE，
> 见 `requirements.txt`）→ `PATH` 顺序查找；`plantuml.jar` 首次运行时自动从 Maven 中央仓库获取。
> 渲染产物（`docs/_static/uml/*.svg`）已入库，因此**拉取仓库后直接构建即可，不需要 Java 环境**。

---

## 部署到 GitHub Pages

站点：**https://jinjing-wan.github.io/tw-portfolio/**

采用 **Docs-as-Code 标准流水线**：向 `main` 推送即自动构建并发布，不需要本地手动构建、也不需要手动维护产物分支。

- 工作流：`.github/workflows/docs.yml`
  （`actions/checkout` → `setup-python` → `pip install -r requirements.txt` → `sphinx-build` → `upload-pages-artifact` → `deploy-pages`）
- 仓库 **Settings → Pages → Source 选 `GitHub Actions`**（只需设一次）
- 之后每次推送，站点在 1–2 分钟内自动更新；也可在 Actions 页用 `workflow_dispatch` 手动触发

```bash
git add .
git commit -m "docs: ..."
git push origin main      # 推完即发布
```

> **历史方案已废弃并清理**：早期是把 `docs/_build/html/` 手工推到 `gh-pages` 分支、Pages 指向该分支。
> 那份快照**不会随 `main` 自动更新**（`docs/_build/` 本身也在 `.gitignore` 里），
> 极易造成「明明推送了、页面却纹丝不动」的错觉，故改为 Actions 自动构建。
> `gh-pages` 分支（远端与本地）已于 2026-10-12 删除，`main` 现为唯一分支。
> `.nojekyll` 仍由 `conf.py` 的 `html_extra_path` 打包进产物——Actions 发布时 GitHub 不做 Jekyll 处理，
> 该项实际已非必需，保留仅为兼容将来可能切回分支发布的场景。

---

## API 文档（私有 C/C++ 源码 → Doxygen + Breathe → Sphinx）

本站点是 **Docs-as-Code 在 API 文档场景的实战落地**：Doxygen 从 C/C++ 头文件抽取 XML，
Breathe 桥接进 Sphinx 自动渲染类 / 函数 / 分组，**零手写重复**。
约束：**源码私有、不进公开仓库**；但**接口契约（签名+注释）随仓库发布**——公开站左侧导航的
「API 参考」节点直接渲染真实接口，不含任何 `.cpp` 实现。

### 目录角色

| 目录 | 是否入库 | 说明 |
| --- | --- | --- |
| `api/` | ❌ 不入库（`.gitignore`） | C/C++ 示例库，含两套对比示例：① `include/gx/*.h` 类式 API（`gx::Device` + `memory` 分组）；② `include/gx/device.h` C 风格 API（不透明句柄 `gxDevice_t`/枚举 `gxError_t`/返回状态码的自由函数，**仿主流 GPU 厂商 CUDA-like 风格**，29 个函数分 device/memory/stream/event 四组）。全部含完整 Doxygen 注释，纯英文。**换成你的真实私有库头文件即可，流程一字不改。** |
| `api-docs/` | ✅ 配置入库 | Doxygen + Breathe + Sphinx 的独立子工程（Doxyfile / conf.py / 说明页），用于本地预览与生成接口产物。 |
| `api-docs/doxyxml/` | ✅ 入库（接口产物） | Doxygen 产物，**仅含接口签名 + 注释、不含 `.cpp` 实现**。`git add -f` 提交后，主站与 CI 都能渲染真实接口。 |
| `docs/03_reference/api.md` | ✅ 入库 | 主站内「API 参考」节点（toctree 内、共享左侧导航）——**直接用 Breathe 渲染真实接口**（gx C 风格为主 + gx 类式对照）。 |

### 本地预览（推荐一条命令）

```bash
# 本机先装 Doxygen：
#   macOS : brew install doxygen
#   Linux : sudo apt-get install -y doxygen
#   Windows: winget install doxygen.doxygen   （或 choco install doxygen.install）
#   自定义路径：DOXYGEN_BIN=/path/to/doxygen ./scripts/build_site.sh

./scripts/build_site.sh
# 链路：doxygen(api/*.h) → api-docs/doxyxml(XML)
#     → 主站 Sphinx + Breathe 渲染 API 节点 → 同时合并 /api 子目录
```

打开 `docs/_build/html/index.html`：点击左侧**「参考 → API 参考」**，即可看到完整的
主流 GPU 厂商风格 `gx` C 接口（Device / Memory / Stream / Event 四组共 29 函数）与 `gx`
类式对照示例——全部由 Breathe 自动生成，与主站同 alabaster 主题、共享左侧导航。

> 主站 `docs/conf.py` 已加载 Breathe，并把 `api-docs/doxyxml` 配置为项目；
> 该 XML 仅含接口契约、不含 `.cpp`，作为接口产物随仓库提交，故公开站与本地渲染完全一致。

### 发布到公开站（接口契约公开，实现源码仍私有）

**默认即可**：`api-docs/doxyxml` 已随仓库提交，向 `main` 推送后 GitHub Actions 自动构建，
公开站左侧「API 参考」节点即显示真实接口——**只有签名与注释，没有 `.cpp` 实现**，符合"代码不公开"。

如需额外提供独立的 `/api` 子目录（同源同主题完整站），本地构建后 force-add 预构建 HTML：

```bash
./scripts/build_site.sh            # 生成 docs/_build/html/api 下的完整 API 站
git add -f api-docs/_build/html    # 仅释出渲染结果，不含源码
git commit -m "docs: 发布 API 文档（独立 /api 子目录）"
git push origin main               # docs.yml 检测到该目录即并入 /api
```

> **隐私口径**：上面两条都只释出**接口契约（XML 或 HTML）**，`api/` 下的 `.cpp`
> 实现源码始终留在本地、不进公开仓。若你日后把 `api/` 换成**真实私有库**，同样只提交 /
> 发布接口产物即可，实现代码不会泄漏。
>
> 若既不 force-add `doxyxml` 也不 force-add HTML，公开站仍正常发布，只是 API 节点/子目录不显示真实内容（降级占位），主站其余页面不受影响。


