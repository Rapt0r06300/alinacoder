from __future__ import annotations

import json
import os
from pathlib import Path
from typing import Iterable

_BLOCKER_CODES = {
    "git_install": 20,
    "git_upgrade": 20,
    "git_health": 21,
    "ollama_install": 30,
    "ollama_upgrade": 30,
    "ollama_version": 31,
    "ollama_health": 32,
    "model_pull": 40,
    "model_smoke": 41,
}


def _install_dir_from_argv(argv: Iterable[str]) -> Path | None:
    args = list(argv)
    try:
        index = args.index("--install-dir")
        value = args[index + 1]
    except (ValueError, IndexError):
        return None
    return Path(value)


def translate_setup_exit_code(code: int, argv: Iterable[str]) -> int:
    """Expose the first canonical bootstrap blocker only inside GitHub Actions."""

    if code == 0 or os.environ.get("GITHUB_ACTIONS", "").strip().lower() != "true":
        return code
    install_dir = _install_dir_from_argv(argv)
    if install_dir is None:
        return code
    receipt = install_dir / "install.json"
    try:
        payload = json.loads(receipt.read_text(encoding="utf-8"))
        blockers = payload.get("bootstrap_blockers", [])
        blocker = str(blockers[0]) if blockers else ""
    except (OSError, ValueError, TypeError, json.JSONDecodeError):
        return code
    return _BLOCKER_CODES.get(blocker, code)
