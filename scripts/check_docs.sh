#!/usr/bin/env bash
#
# check_docs.sh — Sphinx 严格构建校验
#
# 等价指令（本项目验收口径，源自 .workbuddy/rules/docs-rules.md 第 7 条
#            + 项目 MEMORY.md 验收标准 sphinx -b html -W --keep-going 0 warning）：
#
#     sphinx-build -W --keep-going -b html docs docs/_build/html
#
# 要求：0 warning 才算通过（规则 7：构建失败只修语法，不改写事实）。
#
# 用法：
#   ./scripts/check_docs.sh
#   SPHINX_PYTHON=/path/to/python ./scripts/check_docs.sh   # 指定解释器
#   SPHINX_OUT=/tmp/out ./scripts/check_docs.sh             # 指定产物目录
#
set -uo pipefail

# --- 0. 定位项目根目录（脚本所在目录的上一级）---
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"
cd "$PROJECT_ROOT" || { echo "ERROR: 无法进入项目根目录 $PROJECT_ROOT" >&2; exit 1; }

# --- 1. 选择带 Sphinx 的 Python（优先级：环境变量 > managed 默认 > .venv > 系统）---
if [[ -n "${SPHINX_PYTHON:-}" ]]; then
  PY="$SPHINX_PYTHON"
elif [[ -x "C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe" ]]; then
  PY="C:/Users/Administrator/.workbuddy/binaries/python/envs/default/Scripts/python.exe"
elif [[ -x "$PROJECT_ROOT/.venv/Scripts/python.exe" ]]; then
  PY="$PROJECT_ROOT/.venv/Scripts/python.exe"
else
  PY="$(command -v python3 || command -v python || true)"
fi

if [[ -z "$PY" ]]; then
  echo "ERROR: 未找到 Python，请设置 SPHINX_PYTHON 环境变量指向含 Sphinx 的解释器。" >&2
  exit 1
fi

# --- 2. 校验 Sphinx 可用 ---
if ! "$PY" -c "import sphinx" >/dev/null 2>&1; then
  echo "ERROR: $PY 未安装 Sphinx。" >&2
  echo "       本项目验收使用 managed 环境（Sphinx 9.1.0）。" >&2
  echo "       或设置 SPHINX_PYTHON 指向已安装 sphinx 的解释器。" >&2
  exit 1
fi

# --- 3. 产物目录 ---
OUT_DIR="${SPHINX_OUT:-$PROJECT_ROOT/docs/_build/html}"

# --- 4. 严格构建（-W: 告警即错误；--keep-going: 报全量告警）---
echo ">>> 使用 Python: $PY"
echo ">>> sphinx-build -W --keep-going -b html docs $OUT_DIR"
"$PY" -m sphinx -W --keep-going -b html docs "$OUT_DIR"
RC=$?

if [[ $RC -eq 0 ]]; then
  echo "[PASS] 构建通过：0 warning（满足 docs-rules.md 第 7 条）。"
  echo "       产物目录: $OUT_DIR"
else
  echo "[FAIL] 构建失败（exit=$RC）。按规则 7：仅修复语法，不得改写事实。" >&2
fi
exit $RC
