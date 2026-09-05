from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from alinacoder.release.acceptance import ReleaseBundle, sha256_file


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
    bundle = ReleaseBundle({item.name for item in args.dist.iterdir()})
    policy_binding = manifest.get("prerequisite_policy", {})
    policy_sha = hashlib.sha256(policy_path.read_bytes()).hexdigest()
    policy_ok = (
        policy_binding.get("file") == "prerequisites-v0.2.json"
        and policy_binding.get("sha256") == policy_sha
        and policy_binding.get("delivery") == "download-at-install-time"
    )
    ok = (
        bundle.complete()
        and app.exists()
        and manifest.get("commit_sha") == args.commit
        and manifest.get("sha256") == sha256_file(app)
        and policy_ok
    )
    print(json.dumps({
        "ok": ok,
        "bundle_complete": bundle.complete(),
        "commit": manifest.get("commit_sha"),
        "artifact_sha256": sha256_file(app) if app.exists() else None,
        "prerequisite_policy_sha256": policy_sha,
        "prerequisite_policy_bound": policy_ok,
    }, sort_keys=True))
    return 0 if ok else 2


if __name__ == "__main__":
    raise SystemExit(main())
