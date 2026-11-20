"""Install the checkout with the pinned skills CLI and verify the installed skill."""

from __future__ import annotations

import argparse
import os
import subprocess
import sys
import tempfile
from pathlib import Path

from validate_package import ROOT, SKILL_NAME, Package, ValidationError, check_links, validate

INSTALLER = "skills@1.9.0"


def verify_installation(package: Package, installed: Path) -> None:
    if installed.is_symlink() or not installed.is_dir():
        raise ValidationError("Installer did not create a project-local skill copy.")
    installed = installed.resolve()
    if {p.name for p in installed.parent.iterdir()} != {SKILL_NAME}:
        raise ValidationError("Expected exactly one installed skill.")
    expected = {p.relative_to(package.skill).as_posix(): p for p in package.files}
    actual = {}
    for path in installed.rglob("*"):
        if path.is_symlink():
            raise ValidationError("Installed skill must be copied, not linked to the source.")
        if path.is_file():
            actual[path.relative_to(installed).as_posix()] = path
    if set(actual) != set(expected):
        raise ValidationError("Installed file inventory does not match the complete skill.")
    for name, source in expected.items():
        if actual[name].read_bytes() != source.read_bytes():
            raise ValidationError(f"Installed file differs from source: {name}.")
        if actual[name].suffix == ".md":
            check_links(actual[name], installed.parent.parent.parent, installed)
    for helper in ("etrade_download.py", "etrade_orders.py"):
        result = subprocess.run(
            [sys.executable, "-B", str(installed / "scripts" / helper), "--help"],
            cwd=installed,
            stdin=subprocess.DEVNULL,
            capture_output=True,
            text=True,
            check=False,
            timeout=30,
        )
        if result.returncode != 0 or "--request-file" not in result.stdout:
            raise ValidationError(f"Installed downloader entry point failed: {helper}.")


def check_install(root: Path) -> int:
    package = validate(root)
    with tempfile.TemporaryDirectory(prefix="swedish-k4-install-") as temporary:
        project = Path(temporary).resolve()
        subprocess.run(["git", "init", "--quiet", str(project)], check=True, timeout=30)
        env = os.environ.copy()
        env.update({"DISABLE_TELEMETRY": "1", "DO_NOT_TRACK": "1", "CI": "true"})
        env.setdefault("npm_config_cache", str(project / ".npm-cache"))
        # A local source tests this exact checkout, including PR changes, not default-branch HEAD.
        subprocess.run(
            [
                "npx",
                "--yes",
                INSTALLER,
                "add",
                str(package.root),
                "--skill",
                SKILL_NAME,
                "--agent",
                "codex",
                "--yes",
                "--copy",
            ],
            cwd=project,
            env=env,
            stdin=subprocess.DEVNULL,
            check=True,
            timeout=180,
        )
        verify_installation(package, project / ".agents" / "skills" / SKILL_NAME)
    return len(package.files)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        count = check_install(args.root)
    except (ValidationError, OSError, subprocess.SubprocessError) as error:
        parser.exit(1, f"Installation check failed: {error}\n")
    print(f"Verified {INSTALLER}: {count} installed files and both downloader entry points.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
