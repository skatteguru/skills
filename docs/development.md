# Development, packaging and releases

The repository ships one discoverable skill under `skills/swedish-k4-tax/`.
Repository tooling is under `scripts/`; only the skill directory goes into the ZIP.
Downloads, authentication captures and private workspaces stay outside the checkout.

## Run the checks

Use Python 3.10+ in an isolated development environment:

```sh
python3 -m venv .venv
source .venv/bin/activate
python -m pip install -r requirements-dev.txt
python -B scripts/validate_package.py
ruff check scripts skills/swedish-k4-tax/scripts tests
ruff format --check scripts skills/swedish-k4-tax/scripts tests
mypy scripts skills/swedish-k4-tax/scripts
python -B -m unittest discover -s tests -v
```

The validator checks YAML metadata and duplicate keys, one automatically discoverable
skill, publisher/version, the license, self-contained relative links, required
helpers and allowed bundle paths. Unrecognized files and symlinks fail validation;
`__pycache__` is excluded. Keep examples synthetic. These checks cannot determine
whether every sentence or financial calculation is correct; review changes and
use the [acceptance scenarios](acceptance-scenarios.md) for behavioral verification.

Development dependencies are pinned. The bundled broker downloaders themselves
still use only the Python standard library.

## Build the installable ZIP

```sh
python -B scripts/build_skill_zip.py
python -B scripts/build_skill_zip.py --check
```

Outputs in the gitignored `dist/` directory:

- `swedish-k4-tax.zip`, containing `swedish-k4-tax/SKILL.md` and all required files.
- `SHA256SUMS`, the SHA-256 checksum of that ZIP.
- `RELEASE_NOTES.md`, the changelog entry for the package version.

The builder validates first and uses sorted files, fixed timestamps/permissions and
uncompressed ZIP entries to avoid compression-library differences. `--check` verifies
that existing artifacts exactly match the current source without rewriting them.
Tests verify reproducibility, missing dependencies, changed artifacts and helpers
running from an extracted ZIP. No build or test contacts a broker or files a return.

## Release

1. Update `metadata.version` in the skill's `SKILL.md` and add a matching
   `## X.Y.Z` entry in [CHANGELOG.md](../CHANGELOG.md).
2. Run all checks and build the ZIP. Commit the reviewed release source.
3. Push an annotated `vX.Y.Z` tag pointing to that commit. The tag must match the
   skill version; published release tags should remain tied to their original source.
4. The [workflow](../.github/workflows/checks.yml) checks Python 3.10 and 3.14,
   rebuilds the tagged source and publishes the ZIP/checksum with its release notes
   only after all checks pass.
5. Check the published assets and verify the downloaded ZIP against `SHA256SUMS`.

Checks also run on pull requests, pushes to main and manual workflow runs. These
runs upload a CI artifact for inspection but do not publish a release. Read-only
permissions apply to checks; only the tag release job has write access. No production
service deployment, broker credentials or live Skatteverket submission is involved.
