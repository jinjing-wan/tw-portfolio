# Configuration file for the Sunrise API Reference (示例).
# Doxygen(XML) -> Breathe -> Sphinx 的独立子工程，不依赖主站 docs/。

project = "Sunrise API Reference (示例)"
copyright = "2026, 在 AI 协助下独立设计并搭建"
author = "在 AI 协助下独立设计并搭建"

extensions = [
    "myst_parser",   # 用 Markdown 写说明页
    "breathe",       # 桥接 Doxygen XML
]

source_suffix = {
    ".md": "markdown",
    ".rst": "restructuredtext",
}

master_doc = "index"

# --- Breathe：读取 Doxygen 生成的 XML（路径相对本 conf.py 所在目录）---
breathe_projects = {"sunrise_api": "doxyxml"}
breathe_default_project = "sunrise_api"

# --- MyST 基础扩展 ---
myst_enable_extensions = ["colon_fence", "deflist", "fieldlist", "substitution"]

html_theme = "alabaster"
exclude_patterns = ["_build", "doxyxml"]

# 左侧导航栏：alabaster 默认只有 navigation.html（全站树），补 localtoc.html
# 让长页面（如 Runtime 层）左侧也有「本页目录」，可页内跳转。
html_sidebars = {
    "**": [
        "about.html",
        "searchfield.html",
        "localtoc.html",
        "navigation.html",
        "relations.html",
    ]
}

# 部署到 GitHub Pages 时带上 .nojekyll，避免下划线前缀路径被当作私有文件
html_extra_path = [".nojekyll"]
