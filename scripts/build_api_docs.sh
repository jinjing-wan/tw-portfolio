#!/usr/bin/env bash
#
# build_api_docs.sh — 本地构建 Sunrise API 文档
# 链路：Doxygen(头文件 -> XML) -> Breathe -> Sphinx(HTML)
#
# 前置：
#   1) doxygen 已安装并在 PATH（mac/linux: brew/apt install doxygen；windows: winget/choco）
#   2) Python 含 sphinx / myst-parser / breathe（见 api-docs/requirements.txt）
#
# 用法：
#   ./scripts/build_api_docs.sh
#   SPHINX_PYTHON=/path/to/python ./scripts/build_api_docs.sh
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
API_DOCS="$ROOT/api-docs"

# --- 选择 Python（优先级：环境变量 > managed venv > 系统 python）---
if [[ -n "${SPHINX_PYTHON:-}" ]]; then
  PY="$SPHINX_PYTHON"
elif [[ -x "C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe" ]]; then
  PY="C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
elif command -v python >/dev/null 2>&1; then
  PY="$(command -v python)"
else
  echo "ERROR: 未找到 Python，请设置 SPHINX_PYTHON 指向含 sphinx/breathe 的解释器。" >&2
  exit 1
fi

# --- 0. 校验 doxygen 可用 ---
if ! command -v doxygen >/dev/null 2>&1; then
  echo "ERROR: 未找到 doxygen。请先安装："
  echo "       macOS : brew install doxygen"
  echo "       Linux : sudo apt-get install -y doxygen"
  echo "       Windows: winget install doxygen.doxygen   (或 choco install doxygen.install)"
  exit 1
fi

echo ">>> 使用 Python: $PY"
echo ">>> doxygen 版本: $(doxygen --version)"

# --- 1/3 运行 Doxygen（生成 XML 到 api-docs/doxyxml）---
echo ">>> [1/3] 运行 Doxygen 生成 XML ..."
( cd "$API_DOCS" && doxygen Doxyfile )

# --- 2/3 运行 Sphinx（生成 HTML 到 api-docs/_build/html）---
echo ">>> [2/3] 运行 Sphinx 生成 HTML ..."
( cd "$API_DOCS" && "$PY" -m sphinx -b html . _build/html )

# --- 3/3 校验产物 ---
echo ">>> [3/3] 校验产物 ..."
test -f "$API_DOCS/_build/html/index.html" || { echo "ERROR: 未生成 index.html" >&2; exit 1; }
echo "完成。本地预览："
echo "    file://$API_DOCS/_build/html/index.html"
