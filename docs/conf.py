# Configuration file for the Sphinx documentation builder.
# 曦望 Sunrise AI 推理 GPU 软件栈文档中心（作品集示例）——Docs-as-Code 全流程

project = "曦望 Sunrise AI 推理 GPU 软件栈文档中心（作品集示例）"
author = "Wan Jinjing"
copyright = "2026, Wan Jinjing"

# -- 构建配置 -------------------------------------------------
# myst_parser    : 让 Sphinx 直接吃 Markdown（.md）源文件
# sphinxcontrib.mermaid : Markdown 里的 ```mermaid 围栏渲染为 UML 图
extensions = ["myst_parser", "sphinxcontrib.mermaid"]

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
exclude_patterns = ["_build", "Thumbs.db", ".DS_Store"]

# -- HTML 输出配置 --------------------------------------------
html_theme = "alabaster"
html_static_path = ["_static"]
html_extra_path = ["../.nojekyll"]  # 部署 GitHub Pages 时自动带 .nojekyll

# 部署到 GitHub Pages 时改成你的实际地址，例如：
# html_baseurl = "https://yourname.github.io/tw-portfolio/"
html_baseurl = ""

# 语言
language = "zh_CN"
