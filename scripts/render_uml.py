#!/usr/bin/env python3
"""Render PlantUML sources (``*.puml``) into images for the documentation site.

Why pre-render instead of using a Sphinx extension
--------------------------------------------------
The rendered images are committed alongside the pages, so:

* the site build needs no JVM at all — ``sphinx-build`` alone is enough;
* the same images are visible when the Markdown sources are read directly
  on github.com (GitHub does not render PlantUML by itself);
* the ``.puml`` sources stay in the repository as the single source of truth.

Environment
-----------
A JVM is required **only when you run this script**. It is resolved in order:

1. ``$JAVA_HOME``
2. ``jdk4py`` (``pip install jdk4py`` — ships a JRE, no system install needed)
3. ``java`` on ``PATH``

``tools/plantuml/plantuml.jar`` is fetched from Maven Central on first run.

Usage
-----
::

    python scripts/render_uml.py                 # render every *.puml
    python scripts/render_uml.py --check         # report stale images only
    python scripts/render_uml.py --format png    # PNG instead of SVG
    python scripts/render_uml.py path/to/x.puml  # render selected files
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SOURCE_DIRS = [ROOT / "docs"]
OUT_DIR = ROOT / "docs" / "_static" / "uml"

PLANTUML_VERSION = "1.2026.8"
PLANTUML_JAR = ROOT / "tools" / "plantuml" / f"plantuml-{PLANTUML_VERSION}.jar"
PLANTUML_URL = (
    "https://repo1.maven.org/maven2/net/sourceforge/plantuml/plantuml/"
    f"{PLANTUML_VERSION}/plantuml-{PLANTUML_VERSION}.jar"
)


def find_java() -> str | None:
    """Locate a Java executable, preferring the PyPI-provided JRE."""
    import os

    candidates: list[Path] = []
    if os.environ.get("JAVA_HOME"):
        candidates.append(Path(os.environ["JAVA_HOME"]))
    try:
        import jdk4py  # type: ignore

        candidates.append(Path(jdk4py.JAVA_HOME))
    except Exception:
        pass

    for home in candidates:
        exe = home / "bin" / ("java.exe" if sys.platform == "win32" else "java")
        if exe.exists():
            return str(exe)

    return shutil.which("java")


def ensure_jar(check_only: bool) -> Path | None:
    if PLANTUML_JAR.exists():
        return PLANTUML_JAR
    if check_only:
        print(f"[uml] missing engine: {PLANTUML_JAR.relative_to(ROOT)}")
        return None

    PLANTUML_JAR.parent.mkdir(parents=True, exist_ok=True)
    print(f"[uml] downloading plantuml {PLANTUML_VERSION} ...")
    tmp = PLANTUML_JAR.with_suffix(".jar.part")
    urllib.request.urlretrieve(PLANTUML_URL, tmp)
    tmp.replace(PLANTUML_JAR)
    print(f"[uml] saved {PLANTUML_JAR.relative_to(ROOT)} "
          f"({PLANTUML_JAR.stat().st_size / 1e6:.1f} MB)")
    return PLANTUML_JAR


def collect_sources(selected: list[str]) -> list[Path]:
    if selected:
        return [Path(p).resolve() for p in selected]
    found: list[Path] = []
    for base in SOURCE_DIRS:
        found.extend(sorted(base.rglob("*.puml")))
    return found


def render(java: str, jar: Path, source: Path, fmt: str) -> bool:
    OUT_DIR.mkdir(parents=True, exist_ok=True)
    cmd = [
        java,
        "-jar", str(jar),
        "-charset", "UTF-8",
        f"-t{fmt}",
        "-o", str(OUT_DIR),
        str(source),
    ]
    proc = subprocess.run(cmd, capture_output=True, text=True)
    output = (proc.stdout + proc.stderr).strip()
    target = OUT_DIR / f"{source.stem}.{fmt}"

    if proc.returncode != 0 or not target.exists() or output:
        detail = output or f"exit code {proc.returncode}"
        print(f"[uml] FAIL {source.relative_to(ROOT)}: {detail}")
        return False

    print(f"[uml] ok   {source.relative_to(ROOT)} -> "
          f"{target.relative_to(ROOT)} ({target.stat().st_size / 1024:.1f} KB)")
    return True


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("files", nargs="*", help="specific .puml files to render")
    parser.add_argument("--format", default="svg", choices=["svg", "png"],
                        help="output image format (default: svg)")
    parser.add_argument("--check", action="store_true",
                        help="report out-of-date images without rendering")
    args = parser.parse_args()

    sources = collect_sources(args.files)
    if not sources:
        print("[uml] no *.puml found")
        return 0

    if args.check:
        stale = [
            s for s in sources
            if not (OUT_DIR / f"{s.stem}.{args.format}").exists()
            or (OUT_DIR / f"{s.stem}.{args.format}").stat().st_mtime < s.stat().st_mtime
        ]
        for s in stale:
            print(f"[uml] STALE {s.relative_to(ROOT)}")
        print(f"[uml] {len(sources) - len(stale)}/{len(sources)} up to date")
        return 1 if stale else 0

    java = find_java()
    if not java:
        print("[uml] no JVM found. Install one of: JAVA_HOME / jdk4py / java on PATH")
        return 2
    jar = ensure_jar(check_only=False)
    if not jar:
        return 2

    ok = sum(render(java, jar, s, args.format) for s in sources)
    print(f"[uml] rendered {ok}/{len(sources)} -> {OUT_DIR.relative_to(ROOT)}")
    return 0 if ok == len(sources) else 1


if __name__ == "__main__":
    raise SystemExit(main())
