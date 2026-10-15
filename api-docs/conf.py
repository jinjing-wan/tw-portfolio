# Configuration file for the Sunrise API Reference (示例).
# Doxygen(XML) -> Breathe -> Sphinx 的独立子工程，不依赖主站 docs/。

project = "Sunrise API Reference (示例)"
copyright = "2026, Wan Jinjing"
author = "Wan Jinjing"

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

# 部署到 GitHub Pages 时带上 .nojekyll，避免下划线前缀路径被当作私有文件
html_extra_path = [".nojekyll"]
