"""CLI: `uv run make-figures <article-number-or-slug>` runs that article's make_figures.py."""

import runpy
import sys
from pathlib import Path

ARTICLES = Path(__file__).resolve().parents[2] / "articles" / "robot-arm"


def main() -> None:
    if len(sys.argv) != 2:
        sys.exit("usage: make-figures <NN or slug>")
    key = sys.argv[1]
    matches = sorted(p for p in ARTICLES.iterdir() if p.is_dir() and p.name.startswith(key))
    if len(matches) != 1:
        sys.exit(f"no unique article for {key!r}: {[p.name for p in matches]}")
    runpy.run_path(str(matches[0] / "make_figures.py"), run_name="__main__")
