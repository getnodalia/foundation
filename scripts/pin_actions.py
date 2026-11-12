#!/usr/bin/env python3
"""Pin every `uses: owner/repo[/path]@<tag>` in the given workflow files to the tag's commit SHA.

Usage: pin_actions.py FILE [FILE...]

The tag is resolved with `git ls-remote` (annotated tags are dereferenced), and the comment names
the most specific version tag that points at the same commit, so `@v4` becomes
`@<sha> # v4.2.2`. References already pinned to a SHA, local actions and Docker images are left
alone. Behaviour does not change: the workflow runs exactly the commit the tag named today.
"""
import re
import subprocess
import sys

USES = re.compile(r"^(?P<pre>\s*(?:-\s*)?uses:\s*)(?P<repo>[A-Za-z0-9_.-]+/[A-Za-z0-9_.-]+)(?P<path>/[^@\s]*)?@(?P<ref>[^\s#]+)(?P<post>.*)$")
SHA = re.compile(r"^[0-9a-f]{40}$")
_cache: dict[str, dict[str, str]] = {}


def tags(repo: str) -> dict[str, str]:
    """Map tag name -> commit SHA (dereferenced)."""
    if repo not in _cache:
        out = subprocess.run(["git", "ls-remote", "--tags", f"https://github.com/{repo}"],
                             check=True, capture_output=True, text=True).stdout
        result: dict[str, str] = {}
        for line in out.splitlines():
            sha, ref = line.split("\t")
            name = ref.removeprefix("refs/tags/")
            if name.endswith("^{}"):
                result[name[:-3]] = sha  # the dereferenced commit wins over the tag object
            else:
                result.setdefault(name, sha)
        _cache[repo] = result
    return _cache[repo]


def version_key(name: str):
    return [int(p) if p.isdigit() else p for p in re.split(r"[.]", name.lstrip("v"))]


def pin_line(line: str) -> str:
    m = USES.match(line)
    if not m or SHA.match(m["ref"]):
        return line
    repo, ref = m["repo"], m["ref"]
    t = tags(repo)
    if ref not in t:
        print(f"warning: {repo}@{ref} is not a tag; left as is", file=sys.stderr)
        return line
    sha = t[ref]
    same = [n for n, s in t.items() if s == sha and re.match(r"^v?\d+(\.\d+)*$", n)]
    label = max(same, key=lambda n: (len(n.split(".")), version_key(n))) if same else ref
    return f"{m['pre']}{repo}{m['path'] or ''}@{sha} # {label}\n"


def main(files: list[str]) -> int:
    for f in files:
        with open(f, encoding="utf-8") as fh:
            lines = fh.readlines()
        new = [pin_line(l) for l in lines]
        if new != lines:
            with open(f, "w", encoding="utf-8") as fh:
                fh.writelines(new)
            print(f"pinned {f}")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
