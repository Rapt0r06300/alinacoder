from __future__ import annotations

import hashlib
import json
import os
import shutil
from pathlib import Path

from alinacoder.product.core import ReleaseManifest, SBOMBuilder

ROOT = Path(__file__).resolve().parents[1]
DIST = ROOT / "dist"
PREREQUISITES = ROOT / "packaging" / "prerequisites-v0.2.json"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> int:
    app = DIST / "AlinaCoder.exe"
    if not app.exists():
        raise SystemExit("missing dist/AlinaCoder.exe")
    if not PREREQUISITES.exists():
        raise SystemExit("missing packaging/prerequisites-v0.2.json")

    commit = os.environ.get("GITHUB_SHA", "LOCAL-UNVERIFIED")
    prerequisite_policy = json.loads(PREREQUISITES.read_text(encoding="utf-8"))
    manifest = ReleaseManifest.from_bytes("0.2.0", commit, app.name, app.read_bytes()).as_dict()
    manifest["channel"] = "v0.2-rc"
    manifest["signature"] = "UNSIGNED_NO_CERTIFICATE"
    manifest["prerequisite_policy"] = {
        "file": "prerequisites-v0.2.json",
        "sha256": sha256(PREREQUISITES),
        "delivery": "download-at-install-time",
        "ollama": {
            "minimum_version": prerequisite_policy["ollama"]["minimum_version"],
            "repository": prerequisite_policy["ollama"]["allowed_repository"],
        },
        "git": {
            "minimum_version": prerequisite_policy["git"]["minimum_version"],
            "repository": prerequisite_policy["git"]["allowed_repository"],
        },
        "models": [item["model"] for item in prerequisite_policy["model_profiles"]],
    }
    (DIST / "release-manifest.json").write_text(json.dumps(manifest, indent=2, sort_keys=True), encoding="utf-8")

    packages = [
        "python-stdlib",
        "pyinstaller==6.16.0",
        f"ollama>={prerequisite_policy['ollama']['minimum_version']}",
        f"git>={prerequisite_policy['git']['minimum_version']}",
    ] + [f"model:{item['model']}" for item in prerequisite_policy["model_profiles"]]
    sbom = SBOMBuilder().build(packages)
    sbom["documentNamespace"] = f"https://github.com/Rapt0r06300/alinacoder/{commit}"
    sbom["externalPrerequisites"] = {
        "policy": "prerequisites-v0.2.json",
        "policySha256": sha256(PREREQUISITES),
        "ollama": prerequisite_policy["ollama"],
        "git": prerequisite_policy["git"],
        "modelProfiles": prerequisite_policy["model_profiles"],
    }
    (DIST / "sbom.spdx.json").write_text(json.dumps(sbom, indent=2, sort_keys=True), encoding="utf-8")

    shutil.copy2(PREREQUISITES, DIST / "prerequisites-v0.2.json")
    for name in ["USER_GUIDE.md", "OPERATIONS.md"]:
        shutil.copy2(ROOT / "docs" / name, DIST / name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
