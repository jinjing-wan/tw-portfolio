# Configuration file for the Sphinx documentation builder.
# 曦望 Sunrise AI 推理 GPU 软件栈文档中心 —— Docs-as-Code 全流程

project = "曦望 Sunrise AI 推理 GPU 软件栈文档中心"
author = "在 AI 协助下独立设计并搭建"
copyright = "2026, 在 AI 协助下独立设计并搭建"

# -- 构建配置 -------------------------------------------------
# myst_parser          : 让 Sphinx 直接吃 Markdown（.md）源文件
# sphinxcontrib.mermaid: Markdown 里的 ```mermaid 围栏渲染为 UML 图
# sphinx.ext.intersphinx: 跨项目符号引用 —— 主站按名字引用「API 参考工程」
#                        (api-docs/) 里定义的 C/C++ 符号，链接由 objects.inv
#                        自动解析（Docusaurus 无此内置机制）。
# 说明：API 参考已独立为 api-docs/ 子工程（Doxygen + Breathe 渲染），
# 主站不再内置 Breathe，改由 intersphinx 跨项目引用其符号。
extensions = ["myst_parser", "sphinxcontrib.mermaid", "sphinx.ext.intersphinx"]

# --- Intersphinx：跨项目符号引用 ---
# 主站文档里写 `:cpp:func:`mtxMalloc`` 这类领域引用时，Sphinx 去 api-docs/
# 工程构建出的 objects.inv 查符号位置，自动生成可点击链接（跨项目、改名跟随）。
# 元组第二项填「本地 inventory 路径」（构建时解析用），第一项填「线上 URL
# 前缀」（生成的链接前缀，api-docs 部署在主站 /api 子路径）。
intersphinx_mapping = {
    "sunrise_api": ("api/", "../api-docs/_build/html/objects.inv"),
}

# 源文件后缀：新文档一律用 .md（可在 GitHub 上直接阅读并渲染 Mermaid）；
# 保留 .rst 以兼容历史页面，两者可混写、互相引用。
source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

# -- Markdown（MyST）配置 -------------------------------------
myst_enable_extensions = [
    "colon_fence",      # ::: 围栏，写 note / warning 等 directive
    "deflist",          # 定义列表
    "fieldlist",        # 字段列表，接口文档常用
    "attrs_block",      # 段落级属性
    "attrs_inline",     # 行内属性
    "substitution",     # 变量替换
    "tasklist",         # 复选框
]
myst_heading_anchors = 3   # 为 h1~h3 生成锚点，便于跨页引用
# 让 ```mermaid 围栏按 directive 解析：Sphinx 出图，
# 同时该围栏在 github.com 上也会被原生渲染为图（两边通吃）。
myst_fence_as_directive = ["mermaid"]

# Pygments 没有 plantuml 词法器，注册一个纯文本兜底，
# 让 ```plantuml 代码块保持语义标签的同时不产生构建告警。
from pygments.lexers.special import TextLexer  # noqa: E402
from sphinx.highlighting import lexers  # noqa: E402

lexers.setdefault("plantuml", TextLexer())

# -- UML 图（Mermaid，离线可用）--------------------------------
# 使用随仓库打包的本地 mermaid ESM（docs/_static/mermaid/），
# 构建产物自带渲染引擎，无需联网即可渲染 UML 时序图 / 类图。
mermaid_use_local = "mermaid/mermaid.esm.min.mjs"
mermaid_light_theme = "default"
# 说明：HLD 页面的正式图示采用 PlantUML 预渲染 SVG
# （源文件 docs/**/uml/*.puml，渲染脚本 scripts/render_uml.py）。

templates_path = ["_templates"]
# _internal：内部完整版文档目录（含公司内部信息，仅内网构建，绝不随公开仓库发布）
exclude_patterns = ["_build", "_internal", "Thumbs.db", ".DS_Store"]

# -- HTML 输出配置 --------------------------------------------
html_theme = "alabaster"
html_static_path = ["_static"]
html_extra_path = ["../.nojekyll"]  # 部署 GitHub Pages 时自动带 .nojekyll

# 左侧导航栏组成：
#   about.html      站点简介（项目/版权）
#   searchfield.html 搜索框
#   localtoc.html   本页目录（当前页各级标题，长页如 API 参考可页内跳转）
#   navigation.html 全站文档树（默认已含；保证「点进任意页左侧都有导航」）
#   relations.html  上一页/下一页
# 说明：alabaster 默认侧栏只有 navigation.html（全站树），不含 localtoc.html，
# 导致 API 参考这类长页面左侧缺少页内目录；此处显式补齐。
html_sidebars = {
    "**": [
        "about.html",
        "searchfield.html",
        "localtoc.html",
        "navigation.html",
        "relations.html",
    ]
}

# 部署到 GitHub Pages 时填实际站点地址，例如：
# html_baseurl = "https://yourname.github.io/tw-portfolio/"
html_baseurl = ""

# 语言
language = "zh_CN"
