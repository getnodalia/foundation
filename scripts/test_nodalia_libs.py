#!/usr/bin/env python3
"""Tests for nodalia_libs.py's renaming: python3 -m unittest scripts/test_nodalia_libs.py"""

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
