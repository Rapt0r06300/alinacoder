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
WINDOWS_MANIFEST = ROOT / "packaging" / "alinacoder-windows.manifest"
WIN10_11_GUID = "{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def _embedded_windows_contract(path: Path) -> bool:
    payload = path.read_bytes()
    return WIN10_11_GUID.encode("ascii") in payload and b"asInvoker" in payload


def main() -> int:
    app = DIST / "AlinaCoder.exe"
    setup = DIST / "AlinaCoderSetup.exe"
    if not app.exists():
        raise SystemExit("missing dist/AlinaCoder.exe")
    if not setup.exists():
        raise SystemExit("missing dist/AlinaCoderSetup.exe")
    if not PREREQUISITES.exists():
        raise SystemExit("missing packaging/prerequisites-v0.2.json")
    if not WINDOWS_MANIFEST.exists():
        raise SystemExit("missing packaging/alinacoder-windows.manifest")

    commit = os.environ.get("GITHUB_SHA", "LOCAL-UNVERIFIED")
    prerequisite_policy = json.loads(PREREQUISITES.read_text(encoding="utf-8"))
    if prerequisite_policy.get("minimum_windows_major") != 10:
        raise SystemExit("v0.2 release policy must target Windows major version 10")

    source_windows_manifest = WINDOWS_MANIFEST.read_text(encoding="utf-8")
    if WIN10_11_GUID not in source_windows_manifest or "asInvoker" not in source_windows_manifest:
        raise SystemExit("Windows 10/11 compatibility manifest is incomplete")
    app_manifest_embedded = _embedded_windows_contract(app)
    setup_manifest_embedded = _embedded_windows_contract(setup)
    if not app_manifest_embedded or not setup_manifest_embedded:
        raise SystemExit("packaged executables are missing the Windows 10/11 compatibility manifest")

    manifest = ReleaseManifest.from_bytes("0.2.0", commit, app.name, app.read_bytes()).as_dict()
    manifest["channel"] = "v0.2-rc"
    manifest["signature"] = "UNSIGNED_NO_CERTIFICATE"
    manifest["windows_compatibility"] = {
        "minimum_windows_major": 10,
        "supported_os_guid": WIN10_11_GUID,
        "windows_10": True,
        "windows_11": True,
        "app_manifest_embedded": app_manifest_embedded,
        "setup_manifest_embedded": setup_manifest_embedded,
        "source_manifest_sha256": sha256(WINDOWS_MANIFEST),
        "setup_sha256": sha256(setup),
    }
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
    sbom["windowsCompatibility"] = manifest["windows_compatibility"]
    (DIST / "sbom.spdx.json").write_text(json.dumps(sbom, indent=2, sort_keys=True), encoding="utf-8")

    shutil.copy2(PREREQUISITES, DIST / "prerequisites-v0.2.json")
    for name in ["USER_GUIDE.md", "OPERATIONS.md"]:
        shutil.copy2(ROOT / "docs" / name, DIST / name)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
