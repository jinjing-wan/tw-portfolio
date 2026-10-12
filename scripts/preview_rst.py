#!/usr/bin/env python3
"""
将仓库中的 reStructuredText (.rst) 转换为 HTML 以便本地预览。

用法：
  # 转换指定文件并输出到默认位置
  python scripts/preview_rst.py docs/feature/company_doc_init_spec.rst

  # 转换指定输入并指定输出文件
  python scripts/preview_rst.py <input.rst> <output.html>

  # 无参数：批量转换 docs/ 下所有 .rst 到 docs/_preview_html/
  python scripts/preview_rst.py

依赖：需要安装 docutils：pip install docutils
"""
from __future__ import annotations
import os
import sys
from pathlib import Path

def convert(input_path: str, output_path: str) -> None:
	try:
		# import here to provide friendly error if missing
		from docutils.core import publish_file
	except Exception as e:
		print("错误：缺少 docutils。请运行: pip install docutils", file=sys.stderr)
		raise

	os.makedirs(os.path.dirname(output_path), exist_ok=True)
	publish_file(source_path=input_path, destination_path=output_path, writer_name="html5")


def main() -> None:
	if len(sys.argv) == 1:
		src_root = Path("docs")
		out_root = Path("docs/_preview_html")
		count = 0
		for p in src_root.rglob("*.rst"):
			rel = p.relative_to(src_root)
			out = out_root / rel.with_suffix('.html')
			convert(str(p), str(out))
			count += 1
		print(f"转换完成：{count} 个 .rst -> {out_root}")
		return

	input_path = Path(sys.argv[1])
	if not input_path.exists():
		print(f"输入文件不存在: {input_path}", file=sys.stderr)
		sys.exit(2)

	if len(sys.argv) >= 3:
		output_path = Path(sys.argv[2])
	else:
		output_path = Path("docs/_preview_html") / input_path.relative_to('docs').with_suffix('.html')

	convert(str(input_path), str(output_path))
	print(f"转换完成: {input_path} -> {output_path}")


if __name__ == '__main__':
	main()
