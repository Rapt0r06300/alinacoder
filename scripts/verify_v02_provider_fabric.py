from __future__ import annotations

import argparse
import hashlib
import json
from pathlib import Path

from alinacoder.intelligence_mesh import CapabilityRequirement
from alinacoder.intelligence_mesh.runtime import build_default_inference_fabric


class EmptyVault:
    def get(self, provider_id: str) -> str | None:
        return None


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open('rb') as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b''):
            digest.update(chunk)
    return digest.hexdigest()


def verify(*, artifact: Path, commit: str, model: str) -> dict[str, object]:
    failures: list[str] = []
    artifact = artifact.resolve()
    if not artifact.is_file():
        failures.append('artifact_missing')
        digest = ''
    else:
        digest = sha256_file(artifact)

    provider_ids: tuple[str, ...] = ()
    provider_id = ''
    model_id = ''
    response_text = ''
    real_inference = False

    try:
        fabric = build_default_inference_fabric(EmptyVault(), mode='hybrid')
        provider_ids = fabric.provider_ids()
        if provider_ids != ('ollama_local',):
            failures.append('unexpected_runtime_provider_set')
        if 'github_models' in provider_ids:
            failures.append('github_models_not_tombstoned')

        response = fabric.complete(
            [
                {
                    'role': 'user',
                    'content': 'Reply with one short sentence confirming AlinaCoder provider fabric is operational.',
                }
            ],
            CapabilityRequirement({'reasoning': 0.1, 'code': 0.1}),
            mode='hybrid',
        )
        provider_id = str(response.provider_id)
        model_id = str(response.model_id)
        response_text = str(response.text).strip()
        real_inference = bool(response_text and provider_id == 'ollama_local' and model_id == model)
        if provider_id != 'ollama_local':
            failures.append('local_fallback_not_used')
        if model_id != model:
            failures.append('unexpected_local_model')
        if not response_text:
            failures.append('empty_inference')
    except Exception as exc:
        failures.append(f'inference_error:{type(exc).__name__}:{exc}')

    ok = bool(
        artifact.is_file()
        and len(digest) == 64
        and bool(commit)
        and real_inference
        and not failures
    )
    return {
        'ok': ok,
        'provider_fabric_e2e': ok,
        'real_inference': real_inference,
        'commit_sha': commit,
        'artifact_sha256': digest,
        'provider_ids': list(provider_ids),
        'provider_id': provider_id,
        'model_id': model_id,
        'response_nonempty': bool(response_text),
        'failures': failures,
    }


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('--artifact', type=Path, required=True)
    parser.add_argument('--commit', required=True)
    parser.add_argument('--model', required=True)
    parser.add_argument('--out', type=Path, required=True)
    args = parser.parse_args()

    report = verify(artifact=args.artifact, commit=str(args.commit), model=str(args.model))
    args.out.parent.mkdir(parents=True, exist_ok=True)
    args.out.write_text(json.dumps(report, indent=2, sort_keys=True), encoding='utf-8')
    print(json.dumps(report, sort_keys=True))
    return 0 if report['ok'] else 2


if __name__ == '__main__':
    raise SystemExit(main())
