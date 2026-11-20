"""Distribution behavior tests with isolated synthetic packages and no network."""

from __future__ import annotations

import hashlib
import shutil
import subprocess
import sys
import tempfile
import unittest
import zipfile
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))

from build_skill_zip import build  # noqa: E402
from check_skill_install import verify_installation  # noqa: E402
from validate_package import SKILL_NAME, ValidationError, validate  # noqa: E402

REPO = Path(__file__).resolve().parents[1]


class PackageTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.addCleanup(self.temporary.cleanup)
        self.root = Path(self.temporary.name) / "repo"
        self.root.mkdir()
        self.skill = self.root / "skills" / SKILL_NAME
        shutil.copytree(
            REPO / "skills" / SKILL_NAME, self.skill, ignore=shutil.ignore_patterns("__pycache__")
        )
        for name in ("README.md", "AGENTS.md", "LICENSE", "CHANGELOG.md"):
            shutil.copyfile(REPO / name, self.root / name)
        shutil.copytree(REPO / "docs", self.root / "docs")
        shutil.copytree(REPO / ".github", self.root / ".github")
        self.package = validate(self.root)

    def test_build_reproducible_complete_package_and_runnable_helpers(self) -> None:
        first = build(self.root, self.root / "dist")
        second = build(self.root, self.root / "another")
        self.assertEqual(first.read_bytes(), second.read_bytes())
        checksum = (first.parent / "SHA256SUMS").read_text().split()[0]
        self.assertEqual(checksum, hashlib.sha256(first.read_bytes()).hexdigest())
        with zipfile.ZipFile(first) as archive:
            names = archive.namelist()
            self.assertEqual(names, sorted(names))
            self.assertEqual(
                archive.read(f"{SKILL_NAME}/LICENSE"), (self.root / "LICENSE").read_bytes()
            )
            self.assertFalse(any("TODO" in n or n.startswith("docs/") for n in names))
            extracted = self.root / "installed"
            archive.extractall(extracted)
        for helper in ("etrade_download.py", "etrade_orders.py"):
            result = subprocess.run(
                [sys.executable, "-B", str(extracted / SKILL_NAME / "scripts" / helper), "--help"],
                capture_output=True,
                text=True,
                check=False,
            )
            self.assertEqual(result.returncode, 0, result.stderr)
            self.assertIn("--request-file", result.stdout)

    def test_tag_mismatch_and_modified_artifacts_fail(self) -> None:
        output = self.root / "dist"
        with self.assertRaises(ValidationError):
            build(self.root, output, tag="v99.0.0")
        archive = build(self.root, output)
        build(self.root, output, check=True)
        archive.write_bytes(b"changed")
        with self.assertRaises(ValidationError):
            build(self.root, output, check=True)

    def test_missing_helper_and_unexpected_private_file_fail(self) -> None:
        helper = self.skill / "scripts/etrade_common.py"
        content = helper.read_bytes()
        helper.unlink()
        with self.assertRaises(ValidationError):
            validate(self.root)
        helper.write_bytes(content)
        (self.skill / "request.txt").write_text("synthetic capture")
        with self.assertRaises(ValidationError):
            validate(self.root)

    def test_symlinks_fail(self) -> None:
        (self.skill / "references/outside.md").symlink_to(self.root / "README.md")
        with self.assertRaises(ValidationError):
            validate(self.root)

    def test_missing_and_outside_skill_links_fail(self) -> None:
        reference = self.skill / "references/broken.md"
        for target in ("missing.md", "../../../README.md"):
            reference.write_text(f"[Reference]({target})\n")
            with self.subTest(target=target), self.assertRaises(ValidationError):
                validate(self.root)

    def test_duplicate_yaml_and_name_mismatch_fail(self) -> None:
        path = self.skill / "SKILL.md"
        original = path.read_text()
        for text in (
            original.replace(f"name: {SKILL_NAME}", "name: wrong"),
            original.replace(f"name: {SKILL_NAME}", f"name: {SKILL_NAME}\nname: duplicate"),
        ):
            path.write_text(text)
            with self.assertRaises(ValidationError):
                validate(self.root)

    def test_extra_skill_or_disabled_discovery_fail(self) -> None:
        extra = self.root / "skills/another-skill"
        extra.mkdir()
        with self.assertRaises(ValidationError):
            validate(self.root)
        extra.rmdir()
        ui = self.skill / "agents/openai.yaml"
        ui.write_text(ui.read_text() + "\npolicy:\n  allow_implicit_invocation: false\n")
        with self.assertRaises(ValidationError):
            validate(self.root)

    def test_installed_copy_runs_and_rejects_missing_or_changed_files(self) -> None:
        installed = self.root / "project/.agents/skills" / SKILL_NAME
        shutil.copytree(self.skill, installed)
        verify_installation(self.package, installed)
        for name in ("references/brokers/etrade.md", "scripts/etrade_common.py"):
            path = installed / name
            content = path.read_bytes()
            path.unlink()
            with self.subTest(missing=name), self.assertRaises(ValidationError):
                verify_installation(self.package, installed)
            path.write_bytes(content + b"\nchanged")
            with self.subTest(changed=name), self.assertRaises(ValidationError):
                verify_installation(self.package, installed)
            path.write_bytes(content)
        verify_installation(self.package, installed)

    def test_version_requires_matching_release_notes(self) -> None:
        path = self.skill / "SKILL.md"
        path.write_text(
            path.read_text().replace(f'version: "{self.package.version}"', 'version: "99.0.0"')
        )
        with self.assertRaises(ValidationError):
            validate(self.root)


if __name__ == "__main__":
    unittest.main()
