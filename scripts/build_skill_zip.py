"""Build a reproducible installable ZIP, checksum and version-specific release notes."""

from __future__ import annotations

import argparse
import hashlib
import io
import zipfile
from pathlib import Path

from validate_package import ROOT, SKILL_NAME, Package, ValidationError, validate


def archive_bytes(package: Package) -> bytes:
    output = io.BytesIO()
    # Stored entries avoid zlib-version differences; this small text bundle stays compact.
    with zipfile.ZipFile(output, "w", compression=zipfile.ZIP_STORED) as archive:
        for path in package.files:
            name = f"{SKILL_NAME}/{path.relative_to(package.skill).as_posix()}"
            entry = zipfile.ZipInfo(name, date_time=(1980, 1, 1, 0, 0, 0))
            entry.create_system = 3
            entry.external_attr = 0o100644 << 16
            archive.writestr(entry, path.read_bytes())
    content = output.getvalue()
    with zipfile.ZipFile(io.BytesIO(content)) as archive:
        if archive.testzip() is not None:
            raise ValidationError("Built ZIP failed its integrity check.")
        if len(archive.namelist()) != len(package.files):
            raise ValidationError("Built ZIP is missing source files.")
    return content


def build(root: Path, output_dir: Path, *, tag: str | None = None, check: bool = False) -> Path:
    package = validate(root)
    if tag is not None and tag != f"v{package.version}":
        raise ValidationError("Release tag must match the skill version.")
    if output_dir.resolve().is_relative_to(package.skill):
        raise ValidationError("Build outside the installed skill directory.")
    content = archive_bytes(package)
    filename = f"{SKILL_NAME}.zip"
    checksum = f"{hashlib.sha256(content).hexdigest()}  {filename}\n".encode()
    artifacts = {
        filename: content,
        "SHA256SUMS": checksum,
        "RELEASE_NOTES.md": package.notes.encode("utf-8"),
    }
    if check:
        for name, expected in artifacts.items():
            path = output_dir / name
            if path.is_symlink() or not path.is_file() or path.read_bytes() != expected:
                raise ValidationError(f"Missing or stale build artifact: {name}.")
    else:
        output_dir.mkdir(parents=True, exist_ok=True)
        for name, expected in artifacts.items():
            path = output_dir / name
            if path.is_symlink():
                raise ValidationError("Refusing to overwrite a symlink build artifact.")
            path.write_bytes(expected)
    return output_dir / filename


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--output-dir", type=Path)
    parser.add_argument("--tag", help="Require a release tag matching the skill version.")
    parser.add_argument(
        "--check", action="store_true", help="Check existing artifacts without writing."
    )
    args = parser.parse_args()
    try:
        path = build(
            args.root, args.output_dir or args.root / "dist", tag=args.tag, check=args.check
        )
    except (ValidationError, OSError, UnicodeError) as error:
        parser.exit(1, f"Build failed: {error}\n")
    print(f"{'Checked' if args.check else 'Built'}: {path}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
