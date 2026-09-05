# AlinaCoder v0.2 — Operations

## Runtime safety
Canonical state is local/versioned; effects are mediated/idempotent; stale writers are rejected; same-lineage mirrors do not count as independent cognitive votes; self-improvement cannot modify the sealed acceptance boundary.

## Zero-touch prerequisite bootstrap
`AlinaCoderSetup.exe` owns the orchestration, while `packaging/prerequisites-v0.2.json` is the versioned policy. The manifest allow-lists official Ollama and Git for Windows release APIs, minimum versions, the local Ollama endpoint and hardware-fit model profiles.

Bootstrap order is: inventory → deterministic plan → verified prerequisite download/install → Ollama health → model pull → real inference → atomic receipts. Remote Windows installers are accepted only from allow-listed HTTPS GitHub release assets with GitHub-published SHA-256 and valid Authenticode signatures.

Machine-local evidence is stored beside the installed application:
- `install.json`: product operation and readiness summary;
- `bootstrap-state.json`: canonical ownership/version/provenance state;
- `bootstrap-receipt.json`: actions, blockers, model and resulting state;
- `.bootstrap-cache/`: verified prerequisite installers used by the lifecycle.

Ownership is safety-critical. `pre_existing` means the dependency belonged to the user before AlinaCoder touched it and normal uninstall/purge must preserve it. `managed_by_alinacoder` may be removed only by an explicit managed-prerequisite purge. An upgrade of a pre-existing dependency does not transfer ownership to AlinaCoder.

## Build
```powershell
python -m pip install pyinstaller==6.16.0
$env:PYTHONPATH='src'
python scripts/build_windows.py
python scripts/generate_release_metadata.py
```

The release bundle must contain `prerequisites-v0.2.json`; release manifest and SPDX SBOM describe Git/Ollama/model dependencies as runtime-downloaded external prerequisites. Final readiness is invalid unless LOT 19 bootstrap evidence is bound to the exact commit and `AlinaCoder.exe` digest.

## Smoke
```powershell
.\dist\AlinaCoder.exe --self-test
.\dist\AlinaCoderSetup.exe --quiet --install-dir "$env:TEMP\AlinaCoder-RC" --model qwen3:0.6b
python scripts/verify_lot19_bootstrap.py --install-dir "$env:TEMP\AlinaCoder-RC" --artifact .\dist\AlinaCoder.exe --commit $env:GITHUB_SHA --model qwen3:0.6b --out .\dist\lot19-bootstrap-evidence.json
& "$env:TEMP\AlinaCoder-RC\AlinaCoder.exe" --self-test
.\dist\AlinaCoderSetup.exe --uninstall --quiet --install-dir "$env:TEMP\AlinaCoder-RC"
```

## Repair, upgrade, rollback and offline recovery
```powershell
.\dist\AlinaCoderSetup.exe --repair --quiet --install-dir "$env:TEMP\AlinaCoder-RC" --model qwen3:0.6b
.\dist\AlinaCoderSetup.exe --upgrade --quiet --install-dir "$env:TEMP\AlinaCoder-RC" --model qwen3:0.6b
.\dist\AlinaCoderSetup.exe --rollback --quiet --install-dir "$env:TEMP\AlinaCoder-RC"
.\dist\AlinaCoderSetup.exe --offline --quiet --install-dir "$env:TEMP\AlinaCoder-RC" --model qwen3:0.6b
```
Rollback is fail-closed: only a `managed_by_alinacoder` component with an exact recorded prior official release URL and SHA-256 may be restored. A user-owned/pre-existing Git or Ollama installation is never an automatic rollback target. Network/dependency interruption leaves a non-ready receipt and a later setup run resumes from observed state rather than claiming success.

## Signing and provenance
RC application builds are explicitly `UNSIGNED_NO_CERTIFICATE` until an owner-controlled application-signing certificate is available. GitHub Actions produces cryptographic build/SBOM attestations for the RC artifact. Production update policy must reject unsigned/untrusted application metadata. This is separate from the Authenticode verification applied to downloaded third-party Windows prerequisite installers.

## Supabase outage
Supabase is never canonical. Mark mirror unhealthy and continue `LOCAL_ONLY`.

## Product rollback
Product-version rollback restores the prior reviewed AlinaCoder version and invalidates evidence bound to superseded source/artifact hashes. Prerequisite rollback follows the stricter ownership/provenance contract above.
