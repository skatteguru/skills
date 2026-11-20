"""Validate the single installable skill and its repository documentation."""

from __future__ import annotations

import argparse
import ast
import re
from dataclasses import dataclass
from pathlib import Path
from typing import Any
from urllib.parse import unquote, urlsplit

import yaml
from yaml.nodes import MappingNode, ScalarNode

ROOT = Path(__file__).resolve().parents[1]
SKILL_NAME = "swedish-k4-tax"
MCP_URL = "https://rust.skatteguru.se/mcp"
EXAMPLES = {
    "examples/canonical-stock-trades.csv",
    "examples/canonical-fractional-stock-trades.csv",
    "examples/canonical-crypto-trades.csv",
}
REQUIRED = {
    "SKILL.md",
    "LICENSE",
    "agents/openai.yaml",
    "scripts/etrade_common.py",
    "scripts/etrade_download.py",
    "scripts/etrade_orders.py",
    *EXAMPLES,
}


class ValidationError(Exception):
    """The package is unsuitable for distribution."""


class UniqueLoader(yaml.SafeLoader):
    def construct_mapping(self, node: MappingNode, deep: bool = False) -> dict[Any, Any]:
        keys = []
        for key, _ in node.value:
            if not isinstance(key, ScalarNode) or key.tag != "tag:yaml.org,2002:str":
                raise ValidationError("YAML keys must be strings.")
            keys.append(key.value)
        if len(set(keys)) != len(keys):
            raise ValidationError("YAML keys must be unique.")
        return super().construct_mapping(node, deep=deep)


def mapping(text: str, label: str) -> dict[str, Any]:
    try:
        value = yaml.load(text, Loader=UniqueLoader)
    except yaml.YAMLError:
        raise ValidationError(f"Invalid YAML in {label}.") from None
    if not isinstance(value, dict) or any(not isinstance(key, str) for key in value):
        raise ValidationError(f"Expected a YAML mapping in {label}.")
    return value


@dataclass(frozen=True)
class Package:
    root: Path
    skill: Path
    version: str
    files: tuple[Path, ...]
    notes: str


def collect_files(skill: Path) -> tuple[Path, ...]:
    files = []
    for path in sorted(skill.rglob("*")):
        if path.is_symlink():
            raise ValidationError("Symlinks are not allowed in the skill bundle.")
        relative = path.relative_to(skill)
        if "__pycache__" in relative.parts:
            continue
        if path.is_dir():
            continue
        name = relative.as_posix()
        allowed = (
            name in REQUIRED
            or (relative.parts[0] == "references" and path.suffix == ".md")
            or (relative.parts[0] == "scripts" and path.suffix == ".py")
        )
        if not allowed:
            raise ValidationError(
                f"Unexpected skill file: {name}. Keep user data outside the skill."
            )
        if path.suffix == ".py":
            try:
                ast.parse(path.read_text(encoding="utf-8"), feature_version=(3, 10))
            except (SyntaxError, UnicodeError):
                raise ValidationError(f"Not valid Python 3.10 source: {name}.") from None
        files.append(path)
    missing = REQUIRED - {p.relative_to(skill).as_posix() for p in files}
    if missing:
        raise ValidationError("Missing package files: " + ", ".join(sorted(missing)))
    return tuple(files)


def check_links(path: Path, root: Path, skill: Path) -> None:
    text = path.read_text(encoding="utf-8")
    for target in re.findall(r"!?\[[^\]]*\]\(([^)]+)\)", text):
        target = target.strip().removeprefix("<").removesuffix(">")
        parsed = urlsplit(target)
        if parsed.scheme or target.startswith("#"):
            continue
        destination = (path.parent / unquote(parsed.path)).resolve()
        boundary = skill if path.is_relative_to(skill) else root
        if not destination.is_relative_to(boundary) or not destination.exists():
            raise ValidationError(f"Broken or out-of-package link in {path.relative_to(root)}.")
    for url in re.findall(r"https://[^\s`\)\"<>]+/mcp\b", text):
        if url != MCP_URL:
            raise ValidationError("Public instructions must use the production MCP endpoint.")


def release_notes(root: Path, version: str) -> str:
    changelog = root / "CHANGELOG.md"
    if not changelog.is_file():
        raise ValidationError("Missing CHANGELOG.md.")
    match = re.search(
        rf"^## {re.escape(version)}\s*\n(.*?)(?=^## |\Z)",
        changelog.read_text(encoding="utf-8"),
        re.MULTILINE | re.DOTALL,
    )
    if not match or not match[1].strip():
        raise ValidationError("The skill version needs a nonempty changelog entry.")
    return match[1].strip() + "\n"


def validate(root: Path) -> Package:
    root = root.resolve()
    skills = root / "skills"
    if not skills.is_dir():
        raise ValidationError("Missing skills directory.")
    entries = list(skills.iterdir())
    if len(entries) != 1 or entries[0].name != SKILL_NAME or entries[0].is_symlink():
        raise ValidationError("Ship exactly one discoverable skill: " + SKILL_NAME)
    skill = entries[0]
    files = collect_files(skill)
    match = re.match(
        r"\A---\r?\n(.*?)\r?\n---(?:\r?\n|$)",
        (skill / "SKILL.md").read_text(encoding="utf-8"),
        re.DOTALL,
    )
    if not match:
        raise ValidationError("SKILL.md needs YAML frontmatter.")
    data = mapping(match[1], "SKILL.md")
    if data.get("name") != SKILL_NAME:
        raise ValidationError("Skill name must match its directory.")
    if not isinstance(data.get("description"), str) or not data["description"].strip():
        raise ValidationError("Skill description must be a nonempty string.")
    metadata = data.get("metadata")
    if not isinstance(metadata, dict) or metadata.get("publisher") != "Skatteguru":
        raise ValidationError("Skill publisher must be Skatteguru.")
    version = metadata.get("version")
    if not isinstance(version, str) or not re.fullmatch(r"\d+\.\d+\.\d+", version):
        raise ValidationError("Use a quoted major.minor.patch skill version.")
    ui = mapping((skill / "agents/openai.yaml").read_text(encoding="utf-8"), "openai.yaml")
    interface = ui.get("interface")
    if (
        not isinstance(interface, dict)
        or interface.get("display_name") != "Swedish investment tax (K4)"
    ):
        raise ValidationError("Missing or incorrect display name.")
    short = interface.get("short_description")
    if not isinstance(short, str) or not 25 <= len(short) <= 64:
        raise ValidationError("UI short description must contain 25 to 64 characters.")
    prompt = interface.get("default_prompt")
    if not isinstance(prompt, str) or f"${SKILL_NAME}" not in prompt:
        raise ValidationError("Default prompt must reference the skill identifier.")
    policy = ui.get("policy", {})
    if not isinstance(policy, dict) or policy.get("allow_implicit_invocation", True) is not True:
        raise ValidationError("Keep automatic skill discovery enabled.")
    if data.get("disable-model-invocation", False) or ui.get("dependencies"):
        raise ValidationError("Keep the skill discoverable and usable without MCP.")
    if (skill / "LICENSE").read_bytes() != (root / "LICENSE").read_bytes():
        raise ValidationError("The bundle and repository licenses must match.")
    documents = [root / "README.md", root / "AGENTS.md", root / "CHANGELOG.md"]
    documents += sorted((root / "docs").rglob("*.md"))
    documents += [p for p in files if p.suffix == ".md"]
    for path in documents:
        if not path.is_file() or path.is_symlink():
            raise ValidationError("Missing or symlinked documentation.")
        check_links(path, root, skill)
    return Package(root, skill, version, files, release_notes(root, version))


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    args = parser.parse_args()
    try:
        package = validate(args.root)
    except (ValidationError, OSError, UnicodeError) as error:
        parser.exit(1, f"Validation failed: {error}\n")
    print(f"Valid: {SKILL_NAME} {package.version}, {len(package.files)} bundle files.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
