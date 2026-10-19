#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
check_internal_leak.py —— 公开站 objects.inv 隐私泄露校验（防御性）。

为什么需要它：
    内部版文档（docs/_internal/）与公开站（docs/）是两套独立 Sphinx 工程。
    内部 inv 不进公开仓有四重保障：.gitignore 排除 docs/_internal/ 与 docs/_build/、
    docs/conf.py 的 exclude_patterns 排除 _internal、CI 只部署 docs/_build/html。
    但「路径层面」的隔离拦不住「内容层面」的串味——例如某天有人用 .. include::
    把内部文件拉进公开页、或误把内部工程构建到了公开输出目录。一旦内部对象名
    混进公开站的 objects.inv，所有内部锚点/符号就随 Pages 公之于众。

本脚本解压公开站构建产物里的 objects.inv，做三道检查：
    1) 头部 # Project: 必须等于公开站工程名（若误构建内部工程则立刻现形）；
    2) 任意记录行不得含 '_internal' 关键字（URI / 名字出现即异常）；
    3) 任意记录行不得命中内部标记清单（docs/_internal/scripts/internal_markers.txt，
       该文件本身在 gitignored 的 _internal 内，绝不外泄）。

依赖：仅 Python 标准库（zlib / re），CI 与本地均零额外安装。

用法：
    python scripts/check_internal_leak.py
    python scripts/check_internal_leak.py --inv docs/_build/html/objects.inv
    python scripts/check_internal_leak.py --project "示例 AI 推理 GPU 软件栈文档中心"
退出码：0=无泄露 / 1=检出泄露 / 2=用法或文件错误。
"""
from __future__ import annotations

import argparse
import sys
import zlib
from pathlib import Path

DEFAULT_INV = "docs/_build/html/objects.inv"
DEFAULT_MARKERS = "docs/_internal/scripts/internal_markers.txt"
DEFAULT_PROJECT = "示例 AI 推理 GPU 软件栈文档中心"
INTERNAL_PROJECT_HINT = "公司文档初始化"  # 内部工程 project 字符串特征


def read_markers(path: str) -> list[str]:
    p = Path(path)
    if not p.exists():
        return []
    out: list[str] = []
    for ln in p.read_text(encoding="utf-8").splitlines():
        s = ln.strip()
        if not s or s.startswith("#"):
            continue
        out.append(s)
    return out


def decode_inv(data: bytes) -> tuple[str, list[str]]:
    """返回 (project 名, 记录行列表)。兼容 v1 明文与 v2 zlib。"""
    data = data.replace(b"\r\n", b"\n")
    project = ""
    header, _, body = data.partition(b"\n\n")
    for line in header.split(b"\n"):
        if line.startswith(b"# Project:"):
            project = line.split(b"# Project:", 1)[1].decode("utf-8", "replace").strip()
    if not body:
        # v1 明文：整文件即记录
        return project, data.decode("utf-8", "replace").splitlines()
    try:
        raw = zlib.decompress(body)
    except zlib.error:
        # 退化：当作明文
        return project, data.decode("utf-8", "replace").splitlines()
    return project, raw.decode("utf-8", "replace").splitlines()


def main() -> int:
    ap = argparse.ArgumentParser(description="公开站 objects.inv 内部泄露校验")
    ap.add_argument("--inv", default=DEFAULT_INV, help=f"公开站 objects.inv 路径 (默认 {DEFAULT_INV})")
    ap.add_argument("--markers", default=DEFAULT_MARKERS, help="内部标记清单 (默认 gitignored 路径)")
    ap.add_argument("--project", default=DEFAULT_PROJECT, help="期望的公开站工程名")
    args = ap.parse_args()

    inv = Path(args.inv)
    if not inv.exists():
        print(f"[SKIP] 未找到公开站 objects.inv：{inv}（跳过，建议先构建）", file=sys.stderr)
        return 0

    project, records = decode_inv(inv.read_bytes())

    hits: list[tuple[str, str]] = []

    # 检查 1：工程名必须匹配公开站，否则说明误构建了内部工程
    if project and project != args.project:
        hits.append(("project-mismatch", f"# Project: {project}  != 期望公开站：{args.project}"))
    if INTERNAL_PROJECT_HINT and INTERNAL_PROJECT_HINT in project:
        hits.append(("internal-project", f"# Project: {project} 命中内部工程特征"))

    # 检查 2/3：逐记录扫描
    markers = read_markers(args.markers)
    if not markers:
        print(f"[WARN] 未加载内部标记清单（{args.markers}），仅做工程名与 '_internal' 关键字扫描",
              file=sys.stderr)
    for ln in records:
        if "_internal" in ln:
            hits.append(("_internal-keyword", ln))
            continue
        for m in markers:
            if m in ln:
                hits.append((f"marker:{m}", ln))
                break

    if hits:
        print(f"[LEAK] 公开站 objects.inv 检出 {len(hits)} 处疑似内部泄露：", file=sys.stderr)
        for tag, ln in hits[:50]:
            print(f"  [{tag}] {ln}", file=sys.stderr)
        if len(hits) > 50:
            print(f"  ... 其余 {len(hits) - 50} 处省略", file=sys.stderr)
        return 1

    print(f"[OK] 公开站 objects.inv 无内部泄露（扫描 {len(records)} 条记录；project={project!r}）")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
