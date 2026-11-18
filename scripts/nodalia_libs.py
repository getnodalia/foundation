#!/usr/bin/env python3
"""Give the shared libraries Nodalia's names.

The libraries Nodalia's apps build against began upstream as craft-libs, craft-i18n and
craft-fonts. Their mirrors stay untouched on `vendor/<repo>/*`; this script turns any commit of a
mirror into the same tree under Nodalia's names, and records it on `nodalia/<library>`:

    nodalia_libs.py rename libs DIR        rename a checkout in place
    nodalia_libs.py generate libs SHA      commit the renamed tree of SHA on nodalia/libs
    nodalia_libs.py lookup libs SHA        print the nodalia/libs commit made from SHA

Every generated commit's parent is the previous generated commit, so the branch is a list of
renamed snapshots. Its message ends with `Upstream-Commit: <sha>`, the mirror commit it was made
from, whose history, authors and attributions stay on the mirror; the trailer is how `lookup` and
the apps' weekly sync find it. Upstream's `.github/workflows` are left out: they are not this
branch's CI, and the workflow's token may not push workflow files.

What is renamed, and what is not, is listed in RULES below. Licence texts, NOTICE (which gets a
paragraph saying where the code comes from), ATTRIBUTION and third-party code under `vendor/` keep
their words, because the licences and the credits require them; so do links.
"""

from __future__ import annotations

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = "https://github.com/getnodalia/foundation"

# Product names inside crate or directory names: each library crate named after an upstream app
# takes the name of the Nodalia app that inherited it. File signatures inside the formats are
# string literals and are never touched, so documents saved before keep opening.
PRODUCT_WORDS = {
    "anicraft": "anima",
    "deckcraft": "lamina",
    "designcraft": "pliego",
    "figcraft": "trama",
    "gridcraft": "celdas",
    "pcraft": "lienzo",
    "scraft": "sound",
    "stencilcraft": "stencil",
    "tcraft": "texture-archive",
    "vectorcraft": "pluma",
}

# Upstream apps named in prose, messages and generators: each is the Nodalia app that inherited it.
# "<App> contributors", "<App> maintainers" and "<App> Team" are credits and keep the name; so do the
# lower-case words, which are file signatures, extensions and folder names.
PRODUCT_NAMES = {
    "AniCraft": "Ánima", "CADCraft": "Forja", "CadCraft": "Forja", "DeckCraft": "Lámina",
    "DesignCraft": "Pliego", "EffectCraft": "Pulso", "FigCraft": "Trama", "FilmCraft": "Toma",
    "GridCraft": "Celdas", "LightCraft": "Luz", "PdfCraft": "Papel", "PhotoCraft": "Lienzo",
    "SolidCraft": "Torno", "VectorCraft": "Pluma", "WordCraft": "Letra",
}
CREDIT = r"(?!\s+(?:contributors|maintainers|authors|Team)\b)"

# Repositories that are mirrored in foundation: a git dependency on one of them moves here and
# keeps its rev, since the mirrors keep every upstream SHA.
MIRRORED = ["craft-libs", "craft-i18n", "craft-fonts", "egui", "winit", "winprint.rs",
            "indd-utils", "filmcraft", "vectorcraft", "craft-media"]

# Words that are not crate names but name the libraries themselves.
EXTRA_NAMES = {
    "craft-libs": "nodalia-libs",
    "craft-i18n": "nodalia-i18n",
    "craft-fonts": "nodalia-fonts",
}

SKIP_FILES = {"NOTICE", "ATTRIBUTION.md", "CHANGELOG.md", "LICENSE-MIT", "LICENSE-APACHE",
              "LICENSE", "Cargo.lock"}
SKIP_DIRS = {".git", "vendor", "licenses", "target", "node_modules"}
TEXT_SUFFIXES = {".rs", ".toml", ".md", ".txt", ".yml", ".yaml", ".json", ".sh", ".py", ".ps1",
                 ".tsv", ".ftl", ".html", ".css", ".js", ".in", ".cfg", ".nix", ".rev", ""}

LIBRARIES = {
    "libs": {"mirror": "vendor/craft-libs/main", "branch": "nodalia/libs",
             "upstream": "storytold/craft-libs"},
    "i18n": {"mirror": "vendor/craft-i18n/main", "branch": "nodalia/i18n",
             "upstream": "storytold/craft-i18n",
             # Catalogs named after upstream apps are the Nodalia apps' catalogs.
             "file_renames": {"photocraft.tsv": "lienzo.tsv", "pdfcraft.tsv": "papel.tsv",
                              "vectorcraft.tsv": "pluma.tsv", "wordcraft.tsv": "letra.tsv",
                              "deckcraft.tsv": "lamina.tsv", "filmcraft.tsv": "toma.tsv",
                              "cadcraft.tsv": "forja.tsv", "texturecraft.tsv": "texture.tsv",
                              "craft-launcher.tsv": "launcher.tsv"}},
    "fonts": {"mirror": "vendor/craft-fonts/main", "branch": "nodalia/fonts",
              "upstream": "storytold/craft-fonts"},
    # Windows printing: alampy's winprint.rs with upstream's GDI helper crate.
    "winprint": {"mirror": "vendor/winprint.rs/main", "branch": "nodalia/winprint",
                 "upstream": "storytold/winprint.rs"},
    # Toma's media crates (codecs, containers, frames, time), which Pulso uses. Toma's own rename
    # rules make them, so they carry the same names as in Toma's repository.
    "toma": {"mirror": "vendor/filmcraft/main", "branch": "nodalia/toma",
             "upstream": "storytold/filmcraft", "rules": "getnodalia/toma",
             "packages": ("filmcraft-", "toma-")},
}

# A git dependency on one of these repositories is a dependency on another generated library:
# it moves to that library's commit made from the same upstream rev.
GENERATED_REPOS = {"winprint.rs": "winprint", "craft-libs": "libs"}

# Packages of the other generated libraries, which a tree names without defining them.
SIBLING_CRATES = {"craft-winprint-gdi": "nodalia-winprint-gdi"}

# Links, and upstream issues or repositories named without one (storytold/craft-libs#7230), keep
# their words: they name someone else's pages.
URL = re.compile(r"https?://[^\s)\]\"'<>`]+|(?<![\w/.-])storytold/[\w.-]+")


def bounded(word: str) -> str:
    """A regex for `word` standing alone: not part of a longer name."""
    return r"(?<![A-Za-z0-9_-])" + re.escape(word) + r"(?![A-Za-z0-9])"


def new_crate_suffix(suffix: str) -> str:
    for old, new in sorted(PRODUCT_WORDS.items(), key=lambda kv: -len(kv[0])):
        suffix = re.sub(r"(?<![a-z])" + old + r"(?![a-z])", new, suffix)
    return suffix


def crate_names(root: Path) -> dict[str, str]:
    """Every `craft-*` package in the tree, mapped to its Nodalia name."""
    names: dict[str, str] = {}
    for manifest in root.rglob("Cargo.toml"):
        if any(part in SKIP_DIRS for part in manifest.relative_to(root).parts):
            continue
        match = re.search(r'^name\s*=\s*"(craft-[A-Za-z0-9-]+)"', manifest.read_text(errors="replace"),
                          re.M)
        if match:
            names[match.group(1)] = "nodalia-" + new_crate_suffix(match.group(1)[len("craft-"):])
    for old, new in {**EXTRA_NAMES, **SIBLING_CRATES}.items():
        names.setdefault(old, new)
    return names


def dependency_names(root: Path) -> dict[str, str]:
    """Every `craft-*` package the tree's manifests depend on, mapped to its Nodalia name: what
    a tree outside the libraries names without defining."""
    names: dict[str, str] = {}
    for manifest in root.rglob("Cargo.toml"):
        if any(part in SKIP_DIRS for part in manifest.relative_to(root).parts):
            continue
        for old in re.findall(r'^\s*(craft-[A-Za-z0-9-]*[A-Za-z0-9])\s*=', manifest.read_text(errors="replace"), re.M):
            names[old] = "nodalia-" + new_crate_suffix(old[len("craft-"):])
    for old, new in {**EXTRA_NAMES, **SIBLING_CRATES}.items():
        names.setdefault(old, new)
    return names


def directory_renames(root: Path) -> dict[str, str]:
    """Directories named after an upstream product, mapped to their new names."""
    renames = {}
    for path in root.rglob("*"):
        rel = path.relative_to(root)
        if path.is_dir() and not any(p in SKIP_DIRS for p in rel.parts):
            new = new_crate_suffix(path.name)
            if new.startswith("craft-"):
                new = "nodalia-" + new[len("craft-"):]
            if new != path.name:
                renames[path.name] = new
    return renames


class Renamer:
    def __init__(self, root: Path, file_renames: dict[str, str], rev_map=None,
                 names: dict[str, str] | None = None, sha_map: dict[str, str] | None = None,
                 skip: set[str] | None = None, products: bool = True,
                 env_names: set[str] | None = None):
        self.root = root
        self.products = products
        self.rev_map = rev_map
        self.sha_map = sha_map or {}
        self.skip = skip or set()
        if names is None:
            names = crate_names(root)
            self.dirs = directory_renames(root)
        else:
            self.dirs = {}
        self.file_renames = file_renames
        pairs: list[tuple[str, str]] = []
        for old, new in names.items():
            pairs.append((old, new))
            pairs.append((old.replace("-", "_"), new.replace("-", "_")))
        pairs.sort(key=lambda kv: -len(kv[0]))
        self.table = dict(pairs)
        self.name_re = re.compile(
            r"(?<![A-Za-z0-9_-])(" + "|".join(re.escape(k) for k, _ in pairs) + r")(?![A-Za-z0-9])")
        # Path components: `crates/pcraft-format/...`, `"../pcraft-format"`.
        all_dirs = {**self.dirs, **file_renames}
        self.dir_re = (re.compile(r"(?<=[/\"'`(\s])(" + "|".join(
            re.escape(k) for k in sorted(all_dirs, key=len, reverse=True)) + r")(?=[/\"'`)\s]|$)",
            re.M) if all_dirs else None)
        self.all_dirs = all_dirs
        self.product_re = re.compile(r"(?<![A-Za-z0-9_])(" + "|".join(PRODUCT_NAMES) +
                                     r")(?![A-Za-z0-9_])" + CREDIT)
        if env_names is None:
            self.env_re = re.compile(r"(?<![A-Za-z0-9_])CRAFT_(?=[A-Z0-9])")
        else:
            # Only the libraries' own variables: an app's own CRAFT_* names (installer
            # properties a previous install saved) keep working.
            self.env_re = re.compile(r"(?<![A-Za-z0-9_])CRAFT_(?=(?:" + "|".join(
                re.escape(n[len("CRAFT_"):]) for n in sorted(env_names, key=len, reverse=True)) +
                r")(?![A-Za-z0-9_]))") if env_names else re.compile(r"(?!x)x")
        mirrored = "|".join(re.escape(r) for r in MIRRORED)
        self.git_re = re.compile(r"https://github\.com/storytold/(" + mirrored + r")(?:\.git)?\b")
        generated = "|".join(re.escape(r) for r in GENERATED_REPOS)
        self.dep_re = re.compile(r'(git\s*=\s*"https://github\.com/(?:storytold|getnodalia)/(?:' + generated +
                                 r')(?:\.git)?"\s*,\s*rev\s*=\s*")([0-9a-f]{7,40})(")')
        self.repo_re = re.compile(r"https://github\.com/storytold/craft-(?:libs|i18n|fonts)\b(?![/#])")

    def text(self, s: str, manifest: bool) -> str:
        if manifest:
            if self.rev_map:
                s = self.dep_re.sub(self.move_rev, s)
            s = self.git_re.sub(REPO, s)
        s = self.repo_re.sub(REPO, s)
        # The libraries' old home named as a repository (not an issue or pull request there).
        s = re.sub(r"(?<![\w/.-])storytold/craft-(libs|i18n|fonts)(?![\w#-])", r"getnodalia/foundation (nodalia/\1)", s)
        # The mirrors' branch names, in links and prose, become the generated branches.
        s = re.sub(r"vendor/craft-(libs|i18n|fonts)/main\b", r"nodalia/\1", s)
        s = re.sub(r"vendor/winprint\.rs/main\b", "nodalia/winprint", s)
        # Links keep their words: they point at someone else's pages.
        kept: list[str] = []

        def keep(m: re.Match) -> str:
            kept.append(m.group(0))
            return f"\x00{len(kept) - 1}\x00"

        s = URL.sub(keep, s)
        if self.sha_map:
            s = re.sub(r"\b[0-9a-f]{40}\b", lambda m: self.sha_map.get(m.group(0), m.group(0)), s)
        s = self.name_re.sub(lambda m: self.table[m.group(1)], s)
        s = self.env_re.sub("NODALIA_", s)
        if self.products:
            s = self.product_re.sub(lambda m: PRODUCT_NAMES[m.group(1)], s)
        if self.dir_re:
            s = self.dir_re.sub(lambda m: self.all_dirs[m.group(1)], s)
        return re.sub("\x00(\\d+)\x00", lambda m: kept[int(m.group(1))], s)

    def move_rev(self, m: re.Match) -> str:
        repo = re.search(r"/(?:storytold|getnodalia)/([^\"]+?)(?:\.git)?\"", m.group(1))
        name = repo.group(1) if repo else ""
        new = self.rev_map(GENERATED_REPOS.get(name, ""), m.group(2)) if name in GENERATED_REPOS else None
        return m.group(1) + (new or m.group(2)) + m.group(3)

    def run(self) -> None:
        for path in sorted(self.root.rglob("*"), key=lambda p: -len(p.parts)):
            rel = path.relative_to(self.root)
            if any(p in SKIP_DIRS for p in rel.parts) or not path.is_file():
                continue
            if rel.as_posix() in self.skip or any(rel.as_posix().startswith(p + "/") for p in self.skip):
                continue
            if path.name in SKIP_FILES or path.suffix not in TEXT_SUFFIXES and path.name != "Makefile":
                continue
            try:
                before = path.read_text()
            except UnicodeDecodeError:
                continue
            after = self.text(before, path.name == "Cargo.toml")
            if after != before:
                path.write_text(after)
        # Rename files, then directories, deepest first.
        for path in sorted(self.root.rglob("*"), key=lambda p: -len(p.parts)):
            rel = path.relative_to(self.root)
            if any(p in SKIP_DIRS for p in rel.parts[:-1]) or rel.parts[0] in SKIP_DIRS:
                continue
            if path.is_dir():
                new = self.dirs.get(path.name)
            else:
                new = self.file_renames.get(path.name)
            if new:
                path.rename(path.with_name(new))


def notice(root: Path, library: str, upstream_sha: str) -> None:
    spec = LIBRARIES[library]
    text = (f"\nNodalia\n\nThis tree is nodalia-{library}, made from {spec['upstream']} at "
            f"{upstream_sha} by renaming it\n(scripts/nodalia_libs.py in {REPO}). Its code "
            "and assets keep the licences, copyright\nnotices and credits above and in "
            "ATTRIBUTION.md, unchanged.\n")
    path = root / "NOTICE"
    path.write_text((path.read_text() if path.exists() else "") + text)


def git(*args: str, cwd: Path | None = None, env: dict | None = None) -> str:
    return subprocess.run(["git", *args], cwd=cwd, env=env, check=True, text=True,
                          capture_output=True).stdout.strip()


def lookup(library: str, upstream_sha: str, repo: Path) -> str | None:
    branch = LIBRARIES[library]["branch"]
    try:
        log = git("log", "--first-parent", "--format=%H %(trailers:key=Upstream-Commit,valueonly)",
                  f"origin/{branch}", cwd=repo)
    except subprocess.CalledProcessError:
        return None
    try:
        full = git("rev-parse", "--verify", f"{upstream_sha}^{{commit}}", cwd=repo)
    except subprocess.CalledProcessError:
        return None
    for line in log.splitlines():
        parts = line.split()
        if len(parts) == 2 and parts[1] == full:
            return parts[0]
    return None


class MissingCommit(Exception):
    """An upstream commit that the mirrors in this repository do not hold (yet)."""


def app_rules(slug: str, repo: Path) -> tuple[Path, Path]:
    """An app's rebrand.py and its rules (without the formatter step), cloned once per repo."""
    home = Path(git("rev-parse", "--absolute-git-dir", cwd=repo)) / "nodalia-rules" / slug.replace("/", "-")
    if not (home / "scripts" / "rebrand.py").exists():
        git("clone", "--quiet", "--depth", "1", f"https://github.com/{slug}", str(home))
    config = home / "rebrand-no-after.toml"
    rules = (home / ".github" / "rebrand.toml").read_text()
    # A library is not formatted: its users never check its style, and a formatter would need cargo.
    config.write_text(re.sub(r"^after\s*=.*$", "", rules, flags=re.M))
    return home / "scripts" / "rebrand.py", config


def generate(library: str, upstream_sha: str, repo: Path) -> str:
    """Commit the renamed tree of upstream_sha on top of the branch; return the new commit."""
    found = lookup(library, upstream_sha, repo)
    if found:
        return found
    spec = LIBRARIES[library]
    try:
        full = git("rev-parse", "--verify", f"{upstream_sha}^{{commit}}", cwd=repo)
    except subprocess.CalledProcessError:
        raise MissingCommit(f"{spec['upstream']}@{upstream_sha} is not mirrored here") from None
    with tempfile.TemporaryDirectory() as tmp:
        work = Path(tmp) / "tree"
        git("worktree", "add", "--detach", str(work), full, cwd=repo)
        try:
            names = None
            if "rules" in spec:
                script, config = app_rules(spec["rules"], repo)
                subprocess.run([sys.executable, str(script), "apply", "--root", str(work),
                                "--config", str(config)], check=True, stdout=subprocess.DEVNULL)
                # The app's rules renamed its own packages; the libraries' are left to rename.
                names = dependency_names(work)
            Renamer(work, spec.get("file_renames", {}),
                    lambda lib, rev: generate(lib, rev, repo), names=names).run()
            notice(work, library, full)
            # Upstream's CI is not this branch's: it would run on every push, and a workflow
            # token may not write workflow files.
            shutil.rmtree(work / ".github" / "workflows", ignore_errors=True)
            git("add", "-A", cwd=work)
            tree = git("write-tree", cwd=work)
        finally:
            git("worktree", "remove", "--force", str(work), cwd=repo)
    # One parent: the previous generated commit. The upstream commit is named by the trailer and
    # its history stays on the mirror; as a parent it would bring upstream's workflow files into
    # the push, which the workflow's token may not do.
    parents: list[str] = []
    try:
        parents = ["-p", git("rev-parse", f"origin/{spec['branch']}", cwd=repo)]
    except subprocess.CalledProcessError:
        pass
    date = git("show", "-s", "--format=%cI", full, cwd=repo)
    env = {**os.environ, "GIT_AUTHOR_NAME": "Nodalia", "GIT_AUTHOR_EMAIL": "noreply@getnodalia.com",
           "GIT_COMMITTER_NAME": "Nodalia", "GIT_COMMITTER_EMAIL": "noreply@getnodalia.com",
           "GIT_AUTHOR_DATE": date, "GIT_COMMITTER_DATE": date}
    message = (f"nodalia-{library} from {spec['upstream']}@{full[:12]}\n\n"
               f"Upstream-Commit: {full}\n")
    commit = git("commit-tree", tree, *parents, "-m", message, cwd=repo, env=env)
    git("update-ref", f"refs/remotes/origin/{spec['branch']}", commit, cwd=repo)
    return commit


def generated_upstreams(library: str, repo: Path) -> set[str]:
    branch = LIBRARIES[library]["branch"]
    try:
        log = git("log", "--first-parent", "--format=%(trailers:key=Upstream-Commit,valueonly)",
                  f"origin/{branch}", cwd=repo)
    except subprocess.CalledProcessError:
        return set()
    return {line.strip() for line in log.splitlines() if line.strip()}


# How many main-line commits one run fills in; past this it generates only the tip.
MAX_BACKFILL = 100


def update(library: str, repo: Path) -> list[str]:
    """Generate what is missing: every first-parent commit of the mirror's main branch newer
    than the newest one already generated (or only its tip, the first time), and the tip of every
    other branch of the mirror, where apps pin commits that main does not hold."""
    spec = LIBRARIES[library]
    mirror = spec["mirror"]
    done = generated_upstreams(library, repo)
    todo: list[str] = []
    main_line = git("rev-list", "--first-parent", f"origin/{mirror}", cwd=repo).splitlines()
    for sha in main_line:  # newest first
        if sha in done:
            break
        todo.append(sha)
    if len(todo) > MAX_BACKFILL or not done.intersection(main_line):
        # Nothing recent generated: start at the tip.
        todo = todo[:1]
    todo.reverse()
    prefix = mirror.rsplit("/", 1)[0]
    for tip in git("for-each-ref", "--format=%(objectname)", f"refs/remotes/origin/{prefix}/",
                   cwd=repo).splitlines():
        if tip not in done and tip not in todo:
            todo.append(tip)
    made = []
    for sha in todo:
        try:
            made.append(f"{sha} {generate(library, sha, repo)}")
        except MissingCommit as e:
            made.append(f"{sha} skipped: {e}")
    return made


# Files of an app that keep their words: credits, history, and the rename rules themselves.
APP_SKIP = {"vendor", "licenses", "docs/release-notes", "docs/upstream.md", "docs/upstream-readme.md",
            ".github/rebrand.toml", "scripts/rebrand.py", "contributors", "NODALIA_MIGRATION.md"}


def mirror_packages(repo: Path) -> dict[str, str]:
    """Every craft-* package defined at the tips of the mirrored libraries, with its Nodalia name."""
    names: dict[str, str] = {}
    for library in ("libs", "winprint"):
        tip = f"origin/{LIBRARIES[library]['mirror']}"
        for path in git("ls-tree", "-r", "--name-only", tip, cwd=repo).splitlines():
            if path.endswith("Cargo.toml") and not path.startswith("vendor/"):
                text = git("show", f"{tip}:{path}", cwd=repo)
                m = re.search(r'^name\s*=\s*"(craft-[A-Za-z0-9-]+)"', text, re.M)
                if m:
                    names[m.group(1)] = "nodalia-" + new_crate_suffix(m.group(1)[len("craft-"):])
    names.update({**EXTRA_NAMES, **SIBLING_CRATES})
    return names


def library_variables(repo: Path) -> set[str]:
    """The CRAFT_* variables the libraries read or set, at the tips of their mirrors."""
    tips = [f"origin/{LIBRARIES[lib]['mirror']}" for lib in ("libs", "i18n", "fonts")]
    try:
        out = git("grep", "-ohE", r"CRAFT_[A-Z0-9_]*[A-Z0-9]", *tips, cwd=repo)
    except subprocess.CalledProcessError:
        out = ""
    names = {line.split(":", 1)[-1] for line in out.splitlines()}
    return {n for n in names if n.startswith("CRAFT_")} | {
        "CRAFT_FONTS_DIR", "CRAFT_FONTS_REQUIRED", "CRAFT_I18N_DIR", "CRAFT_I18N_REQUIRED"}


def renamed_packages(app: Path) -> dict[str, str]:
    """Packages of the libraries renamed by an app's rules (filmcraft-media -> toma-media) that
    the app's manifests name. Old pins hold packages the mirror's tip has dropped, so the names
    come from the app rather than from the mirror."""
    prefixes = [spec["packages"] for spec in LIBRARIES.values() if "packages" in spec]
    names: dict[str, str] = {}
    for manifest in app.rglob("Cargo.toml"):
        if any(part in SKIP_DIRS for part in manifest.relative_to(app).parts):
            continue
        text = manifest.read_text(errors="replace")
        for old, new in prefixes:
            for name in re.findall(r"(?<![A-Za-z0-9_-])" + re.escape(old) + r"[A-Za-z0-9-]*[A-Za-z0-9]", text):
                names[name] = new + name[len(old):]
    return names


def library_of(sha: str, repo: Path) -> str | None:
    """The generated library whose mirror holds commit sha, if any."""
    try:
        git("cat-file", "-e", f"{sha}^{{commit}}", cwd=repo)
    except subprocess.CalledProcessError:
        return None
    refs = git("for-each-ref", "--contains", sha, "--format=%(refname:short)",
               "refs/remotes/origin/vendor/", cwd=repo).splitlines()
    for library, spec in LIBRARIES.items():
        mirror = spec["mirror"].rsplit("/", 1)[0]  # vendor/<repo>
        if any(r.startswith(f"origin/{mirror}/") for r in refs):
            return library
    return None


def migrate_app(app: Path, repo: Path, allow_generate: bool) -> int:
    """Rename an app's uses of the libraries and move its pins to the Nodalia commits.

    The same pass serves the first migration and every weekly upstream sync afterwards: whatever
    upstream names (craft-ui at an upstream rev, CRAFT_FONTS_DIR, pdfcraft.tsv) comes out under
    Nodalia's names at the matching Nodalia commit.
    """
    names = mirror_packages(repo)
    names.update(dependency_names(app))
    names.update(renamed_packages(app))
    shas: set[str] = set()
    for path in app.rglob("*"):
        rel = path.relative_to(app)
        if path.is_file() and rel.parts[0] not in SKIP_DIRS and (
                path.name in ("Cargo.toml", "Cargo.lock") or path.suffix in (".yml", ".yaml", ".rev")):
            shas.update(re.findall(r"\b[0-9a-f]{40}\b", path.read_text(errors="replace")))
    sha_map: dict[str, str] = {}
    missing = []
    for sha in sorted(shas):
        library = library_of(sha, repo)
        if library is None:
            continue
        new = lookup(library, sha, repo)
        if new is None and allow_generate:
            try:
                new = generate(library, sha, repo)
            except MissingCommit:
                new = None
        if new:
            sha_map[sha] = new
        else:
            missing.append(f"{library} {sha}")
    if missing:
        print("No Nodalia commit yet for:\n  " + "\n  ".join(missing) +
              "\nRun the Nodalia libraries workflow in getnodalia/foundation with these, then retry.",
              file=sys.stderr)
        return 1
    file_renames = dict(LIBRARIES["i18n"]["file_renames"])
    Renamer(app, file_renames, names=names, sha_map=sha_map, skip=APP_SKIP,
            products=False, env_names=library_variables(repo)).run()
    old_rev = app / "craft-i18n.rev"
    if old_rev.exists():
        old_rev.rename(app / "nodalia-i18n.rev")
    for sha, new in sorted(sha_map.items()):
        print(f"{sha} -> {new}")
    return 0


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__,
                                     formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = parser.add_subparsers(dest="cmd", required=True)
    p = sub.add_parser("update", help="generate what the mirrors added since the last run")
    p.add_argument("library", nargs="*", help="libraries to update (default: all)")
    p.add_argument("--repo", type=Path, default=Path.cwd())
    p = sub.add_parser("app", help="move an app's checkout to the Nodalia libraries")
    p.add_argument("dir", type=Path)
    p.add_argument("--repo", type=Path, required=True, help="a foundation clone with vendor/* "
                   "and nodalia/* fetched as origin/*")
    p.add_argument("--generate", action="store_true",
                   help="generate missing Nodalia commits instead of failing")
    p = sub.add_parser("rename")
    p.add_argument("library", choices=LIBRARIES)
    p.add_argument("dir", type=Path)
    for name in ("generate", "lookup"):
        p = sub.add_parser(name)
        p.add_argument("library", choices=LIBRARIES)
        p.add_argument("sha", nargs="+")
        p.add_argument("--repo", type=Path, default=Path.cwd())
    args = parser.parse_args()
    if args.cmd == "update":
        unknown = set(args.library) - set(LIBRARIES)
        if unknown:
            parser.error(f"unknown libraries: {', '.join(sorted(unknown))}")
        for library in args.library or ["winprint", "libs", "i18n", "fonts", "toma"]:
            for line in update(library, args.repo):
                print(f"{library} {line}")
        return 0
    if args.cmd == "app":
        return migrate_app(args.dir, args.repo, args.generate)
    if args.cmd == "rename":
        Renamer(args.dir, LIBRARIES[args.library].get("file_renames", {})).run()
        return 0
    status = 0
    for sha in args.sha:
        try:
            result = (generate if args.cmd == "generate" else lookup)(args.library, sha, args.repo)
        except MissingCommit as e:
            print(f"{sha}: {e}", file=sys.stderr)
            result = None
        if result is None:
            print(f"{sha} -", file=sys.stderr)
            status = 1
        else:
            print(f"{sha} {result}")
    return status


if __name__ == "__main__":
    sys.exit(main())
