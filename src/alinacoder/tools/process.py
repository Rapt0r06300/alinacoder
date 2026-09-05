from __future__ import annotations

import os
import signal
import subprocess
from typing import Sequence

from .models import ProcessReceipt


class ManagedProcessRunner:
    def run(self, argv: Sequence[str], *, timeout_seconds: float, cwd: str | None = None) -> ProcessReceipt:
        kwargs: dict[str, object] = {
            "stdout": subprocess.PIPE,
            "stderr": subprocess.PIPE,
            "text": True,
            "cwd": cwd,
        }
        if os.name == "nt":
            kwargs["creationflags"] = subprocess.CREATE_NEW_PROCESS_GROUP
        else:
            kwargs["start_new_session"] = True
        proc = subprocess.Popen(list(argv), **kwargs)
        try:
            stdout, stderr = proc.communicate(timeout=timeout_seconds)
            return ProcessReceipt(tuple(argv), proc.returncode, stdout, stderr, False)
        except subprocess.TimeoutExpired:
            if os.name == "nt":
                subprocess.run(["taskkill", "/PID", str(proc.pid), "/T", "/F"], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
            else:
                try:
                    os.killpg(proc.pid, signal.SIGKILL)
                except ProcessLookupError:
                    pass
            stdout, stderr = proc.communicate()
            return ProcessReceipt(tuple(argv), proc.returncode if proc.returncode is not None else -9, stdout, stderr, True)
