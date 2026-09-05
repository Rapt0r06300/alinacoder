# AlinaCoder v0.2 — Operations

## Runtime safety
Canonical state is local/versioned; effects are mediated/idempotent; stale writers are rejected; same-lineage mirrors do not count as independent cognitive votes; self-improvement cannot modify the sealed acceptance boundary.

## Build
```powershell
python -m pip install pyinstaller==6.16.0
$env:PYTHONPATH='src'
python scripts/build_windows.py
python scripts/generate_release_metadata.py
```

## Smoke
```powershell
.\dist\AlinaCoder.exe --self-test
.\dist\AlinaCoderSetup.exe --quiet --install-dir "$env:TEMP\AlinaCoder-RC"
& "$env:TEMP\AlinaCoder-RC\AlinaCoder.exe" --self-test
.\dist\AlinaCoderSetup.exe --uninstall --quiet --install-dir "$env:TEMP\AlinaCoder-RC"
```

## Signing
RC builds are explicitly `UNSIGNED_NO_CERTIFICATE` until an owner-controlled certificate is available. Production update policy must reject unsigned/untrusted metadata.

## Supabase outage
Supabase is never canonical. Mark mirror unhealthy and continue `LOCAL_ONLY`.

## Rollback
Rollback restores the prior reviewed version and invalidates evidence bound to superseded source/artifact hashes.
