#!/usr/bin/env python3
"""Tests for nodalia_libs.py's renaming: python3 -m unittest scripts/test_nodalia_libs.py"""

import os
import subprocess
import sys
import tempfile
import unittest
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
import nodalia_libs as nl  # noqa: E402


def renamer(root: Path, **kw) -> nl.Renamer:
    names = {"craft-ui": "nodalia-ui", "craft-pcraft-format": "nodalia-lienzo-format",
             "craft-media": "nodalia-media", "craft-media-testkit": "nodalia-media-testkit",
             **nl.EXTRA_NAMES, **nl.SIBLING_CRATES}
    return nl.Renamer(root, kw.pop("file_renames", {}), names=names, **kw)


class TextTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.r = renamer(Path(self.tmp.name))

    def tearDown(self):
        self.tmp.cleanup()

    def test_crate_names_and_paths(self):
        self.assertEqual(self.r.text("use craft_ui::Theme;", False), "use nodalia_ui::Theme;")
        self.assertEqual(self.r.text('craft-ui = { workspace = true }', True),
                         'nodalia-ui = { workspace = true }')
        self.assertEqual(self.r.text("craft_media_testkit::x()", False), "nodalia_media_testkit::x()")
        self.assertEqual(self.r.text("craft_pcraft_format", False), "nodalia_lienzo_format")

    def test_a_minus_sign_is_not_part_of_a_name(self):
        # `-craft_ui::X` negates a constant; only a kebab name `foo-craft-ui` is left alone.
        self.assertEqual(self.r.text("clamp(-craft_ui::MAX, craft_ui::MAX)", False),
                         "clamp(-nodalia_ui::MAX, nodalia_ui::MAX)")
        self.assertEqual(self.r.text("my-craft-ui", False), "my-craft-ui")

    def test_longer_names_are_left_alone(self):
        # Not a crate: a file name that merely starts like one.
        self.assertEqual(self.r.text('"craft-coated-fogra39.icc"', False), '"craft-coated-fogra39.icc"')
        self.assertEqual(self.r.text("craftsman", False), "craftsman")

    def test_signatures_stay(self):
        # The lower-case product word is a file signature or extension, never renamed.
        src = '{"format":"pcraft"} .pcraft vectorcraft'
        self.assertEqual(self.r.text(src, False), src)

    def test_environment(self):
        self.assertEqual(self.r.text('env::var("CRAFT_FONTS_DIR")', False),
                         'env::var("NODALIA_FONTS_DIR")')
        self.assertEqual(self.r.text("MYCRAFT_X", False), "MYCRAFT_X")

    def test_an_apps_own_variables_stay(self):
        r = renamer(Path(self.tmp.name), env_names={"CRAFT_FONTS_DIR"})
        self.assertEqual(r.text("CRAFT_FONTS_DIR CRAFT_USER_DIR CRAFT_FONTS_DIRS", False),
                         "NODALIA_FONTS_DIR CRAFT_USER_DIR CRAFT_FONTS_DIRS")

    def test_names_defined_by_vendored_code_stay(self):
        root = Path(self.tmp.name)
        (root / "vendor" / "krilla").mkdir(parents=True)
        (root / "vendor" / "krilla" / "lib.rs").write_text("pub const CRAFT_OPTIONAL_CONTENT: bool = true;")
        r = renamer(root)
        self.assertEqual(r.text("CRAFT_OPTIONAL_CONTENT CRAFT_FONTS_DIR", False),
                         "CRAFT_OPTIONAL_CONTENT NODALIA_FONTS_DIR")

    def test_links_keep_their_words(self):
        src = "see https://github.com/storytold/craft-libs/pull/29 and craft-libs"
        self.assertEqual(self.r.text(src, False),
                         "see https://github.com/storytold/craft-libs/pull/29 and nodalia-libs")

    def test_git_dependencies_move_here(self):
        src = 'winprint = { git = "https://github.com/storytold/winprint.rs", rev = "abc1234" }'
        self.assertEqual(self.r.text(src, True),
                         'winprint = { git = "https://github.com/getnodalia/foundation", rev = "abc1234" }')

    def test_generated_dependency_revs_move(self):
        r = renamer(Path(self.tmp.name), rev_map=lambda lib, rev: "f" * 40 if lib == "winprint" else None)
        src = 'craft-winprint-gdi = { git = "https://github.com/storytold/winprint.rs", rev = "64e7afd" }'
        self.assertEqual(r.text(src, True),
                         f'nodalia-winprint-gdi = {{ git = "https://github.com/getnodalia/foundation", rev = "{"f" * 40}" }}')

    def test_products_but_not_credits(self):
        self.assertEqual(self.r.text("written by PhotoCraft", False), "written by Lienzo")
        self.assertEqual(self.r.text("PhotoCraft contributors", False), "PhotoCraft contributors")
        r = renamer(Path(self.tmp.name), products=False)
        self.assertEqual(r.text("written by PhotoCraft", False), "written by PhotoCraft")

    def test_branches_and_repositories(self):
        self.assertEqual(self.r.text("vendor/craft-fonts/main", False), "nodalia/fonts")
        self.assertEqual(self.r.text("a storytold/craft-fonts checkout", False),
                         "a getnodalia/foundation (nodalia/fonts) checkout")
        self.assertEqual(self.r.text("storytold/craft-libs#7230", False), "storytold/craft-libs#7230")

    def test_shas_map(self):
        old, new = "a" * 40, "b" * 40
        r = renamer(Path(self.tmp.name), sha_map={old: new})
        self.assertEqual(r.text(f"rev = \"{old}\"", True), f"rev = \"{new}\"")

    def test_catalog_names(self):
        r = renamer(Path(self.tmp.name), file_renames=nl.LIBRARIES["i18n"]["file_renames"])
        self.assertEqual(r.text('const APP: &str = "pdfcraft.tsv";', False),
                         'const APP: &str = "papel.tsv";')


class GeneratorTests(unittest.TestCase):
    def test_commits_of_an_older_generator_are_made_again(self):
        sha = "a" * 40
        self.assertIsNone(nl.current(["c" * 40, sha]))
        self.assertIsNone(nl.current(["c" * 40, sha, str(nl.GENERATOR - 1)]))
        self.assertEqual(nl.current(["c" * 40, sha, str(nl.GENERATOR)]), sha)


HEAD = "# Spanish (es) interface catalog for lienzo.\n# Columns...\n"


def catalog(*rows: tuple[str, str]) -> str:
    return HEAD + "\n" + "".join(f"\t{src}\t{tr}\n" for src, tr in rows)


class MergeRowsTests(unittest.TestCase):
    def test_what_the_branch_added_survives_an_older_upstream(self):
        base = catalog(("Open", "Abrir"), ("Save", "Guardar"))
        ours = catalog(("Open", "Abrir"), ("Open Recent", "Abrir reciente"), ("Save", "Guardar"))
        theirs = catalog(("Open", "Abrir"), ("Save", "Guardar archivo"))
        merged = nl.merge_rows(base, ours, theirs)
        self.assertEqual(merged, catalog(("Open", "Abrir"), ("Open Recent", "Abrir reciente"),
                                         ("Save", "Guardar archivo")))

    def test_a_row_both_changed_keeps_the_branchs(self):
        base = catalog(("Save", "Guardar"))
        ours = catalog(("Save", "Guardar como"))
        theirs = catalog(("Save", "Salvar"))
        self.assertEqual(nl.merge_rows(base, ours, theirs), ours)

    def test_a_row_upstream_dropped_stays(self):
        # The apps still show it; upstream's own app moved on.
        base = catalog(("Open", "Abrir"), ("Save", "Guardar"))
        self.assertEqual(nl.merge_rows(base, base, catalog(("Open", "Abrir"))), base)
        ours = catalog(("Open", "Abrir"), ("Save", "Guardar archivo"))
        self.assertEqual(nl.merge_rows(base, ours, catalog(("Open", "Abrir"))), ours)

    def test_a_file_that_is_not_a_catalog_is_left_to_the_line_merge(self):
        self.assertIsNone(nl.merge_rows("a\tb\n", "a\tb\n", "a\tb\n"))


class MergeLocalTests(unittest.TestCase):
    def run_git(self, *args, **kw):
        return subprocess.run(["git", *args], cwd=self.repo, check=True, text=True,
                              capture_output=True, env=self.env, **kw).stdout.strip()

    def commit(self, files: dict[str, str], *parents: str) -> str:
        for name, text in files.items():
            path = self.repo / name
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text)
        self.run_git("add", "-A")
        tree = self.run_git("write-tree")
        args = [a for p in parents for a in ("-p", p)]
        return self.run_git("commit-tree", tree, *args, "-m", "c")

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.repo = Path(self.tmp.name)
        self.env = {**os.environ, "GIT_AUTHOR_NAME": "t", "GIT_AUTHOR_EMAIL": "t@t",
                    "GIT_COMMITTER_NAME": "t", "GIT_COMMITTER_EMAIL": "t@t"}
        self.run_git("init", "-q")

    def tearDown(self):
        self.tmp.cleanup()

    def test_rows_added_on_the_branch_survive_the_next_upstream_commit(self):
        f = "locales/es/lienzo.tsv"
        pure1 = self.commit({f: catalog(("Open", "Abrir"), ("Save", "Guardar")), "NOTICE": "a\nb\n"})
        # Someone adds a row on the branch next to the one upstream is about to change.
        tip = self.commit({f: catalog(("Open", "Abrir"), ("Open Recent", "Abrir reciente"),
                                      ("Save", "Guardar")), "NOTICE": "a\nb\nours\n"}, pure1)
        pure2 = self.commit({f: catalog(("Open", "Abrir"), ("Save", "Guardar archivo"),
                                        ("Zoom", "Ampliar")), "NOTICE": "a\nb\nupstream\n"}, pure1)
        merged = nl.merge_local(pure1, tip, pure2, self.repo)
        self.assertEqual(self.run_git("show", f"{merged}:{f}") + "\n",
                         catalog(("Open", "Abrir"), ("Open Recent", "Abrir reciente"),
                                 ("Save", "Guardar archivo"), ("Zoom", "Ampliar")))
        # A conflicting line of another file takes the branch's side.
        self.assertIn("ours", self.run_git("show", f"{merged}:NOTICE"))
        self.assertNotIn("<<<<", self.run_git("show", f"{merged}:NOTICE"))

    def test_rows_upstream_dropped_are_not_dropped_by_a_clean_merge_either(self):
        f = "locales/es/letra.tsv"
        rows = [("A", "a"), ("B", "b"), ("C", "c")]
        pure1 = self.commit({f: catalog(*rows)})
        tip = self.commit({f: catalog(*rows, ("Z", "z"))}, pure1)
        pure2 = self.commit({f: catalog(("A", "a"))}, pure1)
        merged = nl.merge_local(pure1, tip, pure2, self.repo)
        self.assertEqual(self.run_git("show", f"{merged}:{f}") + "\n", catalog(*rows, ("Z", "z")))

    def test_the_base_is_the_commit_generated_from_the_fork_point(self):
        commit = self._commit_msg
        u1 = commit("u1", "u1")
        u2 = commit("u2", "u2", u1)
        u3 = commit("u3", "u3", u2)
        side = commit("side", "side", u1)
        trailer = lambda sha: f"gen\n\nUpstream-Commit: {sha}\nGenerator: {nl.GENERATOR}\n"
        g1 = self._commit_msg("g1", trailer(u1))
        edit = self._commit_msg("edit", "edit", g1)
        pure2 = self._commit_msg("g2", trailer(u2), g1)
        tip = self._commit_msg("merged", trailer(u2), edit, pure2)
        nl.LIBRARIES["t"] = {"branch": "t", "mirror": "m", "upstream": "u"}
        try:
            self.assertEqual(nl.pure_base("t", u3, tip, self.repo), pure2)
            self.assertEqual(nl.pure_base("t", side, tip, self.repo), g1)
            # A branch holding only the first generated commit and an edit.
            self.assertEqual(nl.pure_base("t", u3, edit, self.repo), g1)
            # Nothing generated yet.
            self.assertIsNone(nl.pure_base("t", u3, u3, self.repo))
        finally:
            del nl.LIBRARIES["t"]

    def _commit_msg(self, name, message, *parents):
        (self.repo / name).write_text(name)
        self.run_git("add", "-A")
        args = [a for p in parents for a in ("-p", p)]
        return self.run_git("commit-tree", self.run_git("write-tree"), *args, "-m", message)


class TreeTests(unittest.TestCase):
    def test_directories_and_files_are_renamed(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "crates/pcraft-format/src").mkdir(parents=True)
            (root / "crates/pcraft-format/Cargo.toml").write_text('[package]\nname = "craft-pcraft-format"\n')
            (root / "crates/pcraft-format/src/lib.rs").write_text("//! craft_pcraft_format\n")
            (root / "Cargo.toml").write_text(
                '[workspace.dependencies]\ncraft-pcraft-format = { path = "crates/pcraft-format" }\n')
            (root / "NOTICE").write_text("craft-libs\nCopyright ArtCraft Team\n")
            nl.Renamer(root, {}).run()
            self.assertTrue((root / "crates/lienzo-format/src/lib.rs").exists())
            self.assertIn('nodalia-lienzo-format = { path = "crates/lienzo-format" }',
                          (root / "Cargo.toml").read_text())
            self.assertIn('name = "nodalia-lienzo-format"',
                          (root / "crates/lienzo-format/Cargo.toml").read_text())
            # The licence notice keeps its words.
            self.assertEqual((root / "NOTICE").read_text(), "craft-libs\nCopyright ArtCraft Team\n")

    def test_names_a_tree_depends_on(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "Cargo.toml").write_text(
                '[workspace.dependencies]\ncraft-ui = { git = "x", rev = "y" }\n'
                'filmcraft-media = { git = "x", rev = "y" }\n'
                '# filmcraft-codecs = { path = "../filmcraft/crates/codecs" }\n')
            self.assertEqual(nl.dependency_names(root)["craft-ui"], "nodalia-ui")
            self.assertEqual(nl.renamed_packages(root),
                             {"filmcraft-media": "toma-media", "filmcraft-codecs": "toma-codecs"})


if __name__ == "__main__":
    unittest.main()
