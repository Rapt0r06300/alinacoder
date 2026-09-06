from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from alinacoder.release.acceptance import ReleaseBundle, sha256_file

WIN10_11_GUID = "{8e0f7a12-bfb3-4fe8-b9a5-48fd50a15a9a}"


def main(argv=None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--dist", type=Path, default=Path("dist"))
    parser.add_argument("--commit", required=True)
    args = parser.parse_args(argv)

    manifest_path = args.dist / "release-manifest.json"
    policy_path = args.dist / "prerequisites-v0.2.json"
    if not manifest_path.exists() or not policy_path.exists():
        print(json.dumps({"ok": False, "reason": "missing_manifest_or_prerequisite_policy"}, sort_keys=True))
        return 2
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    app = args.dist / "AlinaCoder.exe"
    setup = args.dist / "AlinaCoderSetup.exe"
    bundle = ReleaseBundle({item.name for item in args.dist.iterdir()})
    policy_binding = manifest.get("prerequisite_policy", {})
    policy_sha = hashlib.sha256(policy_path.read_bytes()).hexdigest()
    policy_ok = (
        policy_binding.get("file") == "prerequisites-v0.2.json"
        and policy_binding.get("sha256") == policy_sha
        and policy_binding.get("delivery") == "download-at-install-time"
    )
    windows = manifest.get("windows_compatibility", {})
    windows_ok = (
        windows.get("minimum_windows_major") == 10
        and windows.get("supported_os_guid") == WIN10_11_GUID
        and windows.get("windows_10") is True
        and windows.get("windows_11") is True
        and windows.get("app_manifest_embedded") is True
        and windows.get("setup_manifest_embedded") is True
        and setup.exists()
        and windows.get("setup_sha256") == sha256_file(setup)
    )
    ok = (
        bundle.complete()
        and app.exists()
        and manifest.get("commit_sha") == args.commit
        and manifest.get("sha256") == sha256_file(app)
        and policy_ok
        and windows_ok
    )
    print(json.dumps({
        "ok": ok,
        "bundle_complete": bundle.complete(),
        "commit": manifest.get("commit_sha"),
        "artifact_sha256": sha256_file(app) if app.exists() else None,
        "prerequisite_policy_sha256": policy_sha,
        "prerequisite_policy_bound": policy_ok,
        "windows_10_11_compatible": windows_ok,
        "supported_os_guid": windows.get("supported_os_guid"),
        "minimum_windows_major": windows.get("minimum_windows_major"),
    }, sort_keys=True))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
