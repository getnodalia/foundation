#!/usr/bin/env python3
"""Fail when a workflow uses a remote action or reusable workflow not pinned to a full commit SHA.

Usage: check_pins.py DIR [DIR...]

Local references (`./...`) and Docker images pinned by digest are allowed. Every other `uses:`
must end in `@<40 hex chars>`, ideally followed by `# vX.Y.Z` so a reader knows which release it is.
"""
import pathlib
import re
import sys

USES = re.compile(r"^\s*(?:-\s*)?uses:\s*['\"]?([^'\"\s#]+)")
SHA = re.compile(r"@[0-9a-f]{40}$")


def main(dirs: list[str]) -> int:
    bad = []
    for d in dirs:
        root = pathlib.Path(d)
        if not root.is_dir():
            continue
        for path in sorted(list(root.rglob("*.yml")) + list(root.rglob("*.yaml"))):
            for n, line in enumerate(path.read_text(encoding="utf-8").splitlines(), 1):
                m = USES.match(line)
                if not m:
                    continue
                ref = m.group(1)
                if ref.startswith("./") or ref.startswith("docker://") and "@sha256:" in ref:
                    continue
                if not SHA.search(ref):
                    bad.append(f"{path}:{n}: {ref}")
    for b in bad:
        print(f"::error::not pinned to a commit SHA: {b}")
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:] or [".github/workflows"]))
