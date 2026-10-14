#!/usr/bin/env python3
"""把 Sphinx 构建产物的单个页面转成「自包含 HTML」。

背景：IDE 预览面板（以及任何只拿到单个 .html 文件、无法按目录结构解析
相对路径 `../_static/` 的渲染环境）会导致 Sphinx 主题样式全部丢失 —— 表现
为表格没有边框、排版塌陷。本脚本把页面引用的 CSS / JS 直接内联进 HTML，
并把 `_static/` 资源整目录复制到输出同级，使页面在「单文件」与「整目录」
两种服务方式下都能正确渲染。

用法：
  # 默认输出到 docs/_preview_html/<文件名>
  python scripts/make_standalone.py docs/_build/html/feature/xxx.html

  # 指定输出路径
  python scripts/make_standalone.py <input.html> <output.html>
"""
from __future__ import annotations

import re
import shutil
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
BUILD = ROOT / "docs" / "_build" / "html"
PREVIEW = ROOT / "docs" / "_preview_html"

# Mermaid 本地模块（相对 HTML 输出目录）；不存在时回退 CDN。
MERMAID_LOCAL = "./_static/mermaid/mermaid.esm.min.mjs"
MERMAID_CDN = "https://cdn.jsdelivr.net/npm/mermaid@11/dist/mermaid.esm.min.mjs"


def read(path: Path) -> str:
    return path.read_text(encoding="utf-8", errors="ignore")


def main() -> None:
    args = sys.argv[1:]
    if not args:
        print(__doc__, file=sys.stderr)
        sys.exit(2)

    src = Path(args[0]).resolve()
    if not src.is_file():
        print(f"输入文件不存在: {src}", file=sys.stderr)
        sys.exit(2)
    out = Path(args[1]).resolve() if len(args) > 1 else PREVIEW / src.name
    out.parent.mkdir(parents=True, exist_ok=True)

    html = read(src)
    base = src.parent  # 相对路径基准 = 产物所在目录

    def resolve(rel: str) -> Path | None:
        q = rel.split("?")[0].split("#")[0]
        if q.startswith(("http://", "https://", "//", "data:")):
            return None
        p = (base / q).resolve()
        return p if p.is_file() else None

    inlined_css, inlined_js, dropped = [], [], []

    # 1) 内联样式表（属性顺序两种都覆盖）
    def on_link(m: re.Match) -> str:
        href = m.group("href")
        p = resolve(href)
        if p is None:
            dropped.append(href)
            return f"<!-- dropped stylesheet: {href} -->"
        inlined_css.append(href.split("?")[0])
        return "<style>\n/* ==== inlined: %s ==== */\n%s\n</style>" % (href.split("?")[0], read(p))

    html = re.sub(r'<link[^>]*rel="stylesheet"[^>]*href="(?P<href>[^"]+)"[^>]*>', on_link, html)
    html = re.sub(r'<link[^>]*href="(?P<href>[^"]+)"[^>]*rel="stylesheet"[^>]*>', on_link, html)

    # 2) 内联本地脚本
    def on_script(m: re.Match) -> str:
        s = m.group("src")
        p = resolve(s)
        if p is None:
            dropped.append(s)
            return f"<!-- dropped script: {s} -->"
        inlined_js.append(s.split("?")[0])
        return "<script>\n%s\n</script>" % read(p)

    html = re.sub(r'<script[^>]*src="(?P<src>[^"]+)"[^>]*>\s*</script>', on_script, html)

    # 3) Mermaid：本地优先、CDN 兜底（动态 import，顶层 await）
    html = html.replace(
        f'import mermaid from "../_static/mermaid/mermaid.esm.min.mjs";',
        "let mermaid;"
        f"try{{mermaid=(await import(\"{MERMAID_LOCAL}\")).default;}}"
        f"catch(e){{mermaid=(await import(\"{MERMAID_CDN}\")).default;}}",
    )

    out.write_text(html, encoding="utf-8")

    # 4) 复制 _static 整目录，保证 url() 图片 / mermaid chunks 可解析
    static_src = BUILD / "_static"
    if static_src.is_dir():
        static_dst = out.parent / "_static"
        if static_dst.resolve() != static_src.resolve():
            if static_dst.exists():
                shutil.rmtree(static_dst)
            shutil.copytree(static_src, static_dst)
            print(f"已复制 _static 资源 -> {static_dst}")

    print(f"自包含页面: {out}")
    print(f"  内联样式 {len(inlined_css)}: {', '.join(inlined_css) or '(无)'}")
    print(f"  内联脚本 {len(inlined_js)}: {', '.join(inlined_js) or '(无)'}")
    if dropped:
        print(f"  跳过缺失资源 {len(dropped)}: {', '.join(dropped)}")


if __name__ == "__main__":
    main()
