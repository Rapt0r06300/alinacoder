from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
from pathlib import Path


def sha256(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def post_generate(endpoint: str, model: str) -> dict:
    payload = json.dumps({
        "model": model,
        "prompt": "Reply only with OK.",
        "think": False,
        "stream": False,
        "options": {"num_predict": 16},
    }).encode("utf-8")
    request = urllib.request.Request(
        endpoint.rstrip("/") + "/api/generate",
        data=payload,
        headers={"Content-Type": "application/json", "User-Agent": "AlinaCoder-Lot19-Verifier/0.2"},
        method="POST",
    )
    with urllib.request.urlopen(request, timeout=180) as response:
        return json.loads(response.read().decode("utf-8"))


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--install-dir", type=Path, required=True)
    parser.add_argument("--artifact", type=Path, required=True)
    parser.add_argument("--commit", required=True)
    parser.add_argument("--model", default="qwen3:0.6b")
    parser.add_argument("--endpoint", default="http://127.0.0.1:11434")
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)

    installed = args.install_dir / "AlinaCoder.exe"
    metadata_path = args.install_dir / "install.json"
    state_path = args.install_dir / "bootstrap-state.json"
    receipt_path = args.install_dir / "bootstrap-receipt.json"
    required_paths = (args.artifact, installed, metadata_path, state_path, receipt_path)
    failures: list[str] = []
    for path in required_paths:
        if not path.exists():
            failures.append(f"missing:{path.name}")

    artifact_digest = sha256(args.artifact) if args.artifact.exists() else ""
    installed_digest = sha256(installed) if installed.exists() else ""
    if artifact_digest and installed_digest != artifact_digest:
        failures.append("installed_artifact_digest_mismatch")

    metadata = json.loads(metadata_path.read_text(encoding="utf-8-sig")) if metadata_path.exists() else {}
    state = json.loads(state_path.read_text(encoding="utf-8-sig")) if state_path.exists() else {}
    receipt = json.loads(receipt_path.read_text(encoding="utf-8-sig")) if receipt_path.exists() else {}
    if metadata.get("bootstrap_ready") is not True:
        failures.append("install_metadata_not_ready")
    if state.get("ready") is not True or receipt.get("ready") is not True:
        failures.append("bootstrap_state_not_ready")
    if metadata.get("selected_model") != args.model or state.get("selected_model") != args.model:
        failures.append("selected_model_mismatch")

    components = dict(state.get("components") or {})
    for component in ("git", "ollama", f"model:{args.model}"):
        entry = dict(components.get(component) or {})
        if not entry or entry.get("healthy") is not True:
            failures.append(f"unhealthy_component:{component}")
            continue
        if entry.get("origin") not in {"managed_by_alinacoder", "pre_existing"}:
            failures.append(f"invalid_ownership:{component}")
        if component in {"git", "ollama"} and entry.get("origin") == "managed_by_alinacoder":
            url = str(entry.get("source_url") or "")
            digest = str(entry.get("sha256") or "")
            if not url.startswith("https://github.com/") or "/releases/download/" not in url:
                failures.append(f"invalid_source:{component}")
            if not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
                failures.append(f"invalid_sha256:{component}")

    inference: dict = {}
    try:
        inference = post_generate(args.endpoint, args.model)
        if not str(inference.get("response") or "").strip() or inference.get("done") is not True:
            failures.append("real_inference_failed")
    except Exception as exc:  # fail closed; serialize only type, never remote payload/secrets
        failures.append(f"real_inference_exception:{type(exc).__name__}")

    report = {
        "ok": not failures,
        "bootstrap_e2e": not failures,
        "commit_sha": args.commit,
        "artifact_sha256": artifact_digest,
        "installed_artifact_sha256": installed_digest,
        "model": args.model,
        "endpoint": args.endpoint,
        "real_inference": bool(inference.get("done") is True and str(inference.get("response") or "").strip()),
        "component_origins": {name: dict(value).get("origin") for name, value in sorted(components.items())},
        "component_versions": {name: dict(value).get("version") for name, value in sorted(components.items())},
        "failures": failures,
    }
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True), encoding="utf-8")
    print(json.dumps(report, sort_keys=True))
    return 0 if report["ok"] else 2


if __name__ == "__main__":
    raise SystemExit(main())
