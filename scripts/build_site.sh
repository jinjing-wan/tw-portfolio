#!/usr/bin/env bash
#
# build_site.sh — 本地构建「主站 + API 文档」合并站点
#
# 链路：
#   1) Doxygen   : api/include/*.h  -> api-docs/doxyxml (XML)
#   2) Sphinx    : api-docs/        -> api-docs/_build/html   (Breathe 渲染 API 参考)
#   3) Sphinx    : docs/            -> docs/_build/html        (主站 Sunrise 文档中心)
#   4) 合并      : api-docs/_build/html  -> docs/_build/html/api
#   结果：docs/_build/html 即「主界面 + API 子目录」同一站点、同一 alabaster 主题。
#
# 前置：
#   1) doxygen 在 PATH（mac: brew install doxygen；linux: apt install doxygen；win: winget install doxygen.doxygen）
#   2) Python 含 sphinx / myst-parser / sphinxcontrib-mermaid / breathe
#
# 用法：
#   ./scripts/build_site.sh
#   SPHINX_PYTHON=/path/to/python ./scripts/build_site.sh
#
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
API_DOCS="$ROOT/api-docs"
MAIN_DOCS="$ROOT/docs"
MAIN_OUT="$MAIN_DOCS/_build/html"

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

# --- 0. 定位 doxygen（优先环境变量 DOXYGEN_BIN，其次 PATH）---
if [[ -n "${DOXYGEN_BIN:-}" ]]; then
  :
elif command -v doxygen >/dev/null 2>&1; then
  DOXYGEN_BIN="$(command -v doxygen)"
else
  echo "ERROR: 未找到 doxygen。请先安装，或用 DOXYGEN_BIN 指定绝对路径："
  echo "       macOS : brew install doxygen"
  echo "       Linux : sudo apt-get install -y doxygen"
  echo "       Windows: winget install doxygen.doxygen   (或 choco install doxygen.install)"
  echo "       自定义: DOXYGEN_BIN=/path/to/doxygen ./scripts/build_site.sh"
  exit 1
fi

echo ">>> 使用 Python: $PY"
echo ">>> doxygen 版本: $("$DOXYGEN_BIN" --version)"

# --- 1/4 运行 Doxygen（api 私有头文件 -> api-docs/doxyxml）---
echo ">>> [1/4] 运行 Doxygen 生成 XML ..."
( cd "$API_DOCS" && "$DOXYGEN_BIN" Doxyfile )

# --- 2/4 构建 API 文档（Breathe -> api-docs/_build/html）---
echo ">>> [2/4] 构建 API 文档（Breathe）..."
( cd "$API_DOCS" && "$PY" -m sphinx -b html . _build/html )

# --- 3/4 构建主站（docs -> docs/_build/html）---
echo ">>> [3/4] 构建主站 Sunrise 文档中心..."
( cd "$MAIN_DOCS" && "$PY" -m sphinx -b html . _build/html )

# --- 4/4 合并 API 文档到主站 /api 子目录 ---
echo ">>> [4/4] 合并 API 文档 -> $MAIN_OUT/api ..."
rm -rf "$MAIN_OUT/api"
cp -r "$API_DOCS/_build/html" "$MAIN_OUT/api"
test -f "$MAIN_OUT/.nojekyll" || cp "$API_DOCS/_build/html/.nojekyll" "$MAIN_OUT/.nojekyll"

# --- 校验 ---
echo ">>> 校验产物 ..."
test -f "$MAIN_OUT/index.html"      || { echo "ERROR: 主站 index.html 缺失" >&2; exit 1; }
test -f "$MAIN_OUT/api/api_reference.html" || { echo "ERROR: API 参考页缺失" >&2; exit 1; }
echo "完成。本地预览："
echo "    主站 : file://$MAIN_OUT/index.html"
echo "    API  : file://$MAIN_OUT/api/api_reference.html"
