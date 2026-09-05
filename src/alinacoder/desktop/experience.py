from __future__ import annotations

from dataclasses import dataclass, field
import os
import subprocess
from typing import Callable


_ALLOWED_PROVIDER_MODES = frozenset({"local-only", "free-cloud", "hybrid"})
_ALLOWED_INPUT_MODES = frozenset({"text", "voice"})


@dataclass
class FirstRunOnboarding:
    """Persistable, fail-closed first-run configuration for the desktop product."""

    project_path: str = ""
    provider_mode: str = ""
    local_runtime: str = ""
    input_modes: set[str] = field(default_factory=set)
    complete: bool = False

    def configure_project(self, project_path: str) -> None:
        value = str(project_path).strip()
        if not value:
            raise ValueError("project path is required")
        self.project_path = value
        self.complete = False

    def configure_inference(self, *, provider_mode: str, local_runtime: str = "") -> None:
        mode = provider_mode.strip().lower()
        if mode not in _ALLOWED_PROVIDER_MODES:
            raise ValueError("provider mode must be local-only, free-cloud, or hybrid")
        runtime = local_runtime.strip().lower()
        if mode in {"local-only", "hybrid"} and not runtime:
            raise ValueError("local runtime is required for local-only/hybrid mode")
        self.provider_mode = mode
        self.local_runtime = runtime
        self.complete = False

    def enable_input_mode(self, mode: str) -> None:
        normalized = mode.strip().lower()
        if normalized not in _ALLOWED_INPUT_MODES:
            raise ValueError("unsupported input mode")
        self.input_modes.add(normalized)
        self.complete = False

    def finish(self) -> None:
        if not self.project_path:
            raise ValueError("first-run onboarding requires a project")
        if self.provider_mode not in _ALLOWED_PROVIDER_MODES:
            raise ValueError("first-run onboarding requires an inference route")
        if self.provider_mode in {"local-only", "hybrid"} and not self.local_runtime:
            raise ValueError("first-run onboarding requires a local runtime")
        if "text" not in self.input_modes:
            raise ValueError("text input must remain available")
        self.complete = True

    def to_dict(self) -> dict:
        return {
            "project_path": self.project_path,
            "provider_mode": self.provider_mode,
            "local_runtime": self.local_runtime,
            "input_modes": sorted(self.input_modes),
            "complete": self.complete,
        }

    @classmethod
    def from_dict(cls, value: dict | None) -> "FirstRunOnboarding":
        value = dict(value or {})
        return cls(
            project_path=str(value.get("project_path", "")),
            provider_mode=str(value.get("provider_mode", "")),
            local_runtime=str(value.get("local_runtime", "")),
            input_modes={str(item) for item in value.get("input_modes", []) if str(item) in _ALLOWED_INPUT_MODES},
            complete=bool(value.get("complete", False)),
        )


class WindowsSpeechRecognizer:
    """One-shot offline/local Windows speech adapter using the OS System.Speech stack."""

    def powershell_script(self) -> str:
        return r"""
$ErrorActionPreference = 'Stop'
Add-Type -AssemblyName System.Speech
$recognizer = New-Object System.Speech.Recognition.SpeechRecognitionEngine
$recognizer.LoadGrammar((New-Object System.Speech.Recognition.DictationGrammar))
$recognizer.SetInputToDefaultAudioDevice()
$result = $recognizer.Recognize([TimeSpan]::FromSeconds(8))
if ($null -eq $result) { exit 3 }
[Console]::OutputEncoding = [System.Text.UTF8Encoding]::new()
$result.Text
""".strip()

    def recognize_once(self, timeout_seconds: float = 12.0) -> str:
        if os.name != "nt":
            raise RuntimeError("Windows voice input is only available on Windows")
        completed = subprocess.run(
            ["powershell.exe", "-NoProfile", "-NonInteractive", "-Command", self.powershell_script()],
            capture_output=True,
            text=True,
            timeout=max(1.0, timeout_seconds),
            check=False,
        )
        if completed.returncode != 0:
            detail = completed.stderr.strip() or "no speech recognized"
            raise RuntimeError(f"voice recognition failed: {detail}")
        transcript = completed.stdout.strip()
        if not transcript:
            raise RuntimeError("voice recognition returned an empty transcript")
        return transcript


class VoiceInputAdapter:
    """Stateful capture boundary with an injectable recognizer for deterministic testing."""

    def __init__(self, recognizer: Callable[[], str] | None = None) -> None:
        self._recognizer = recognizer or WindowsSpeechRecognizer().recognize_once
        self.state = "IDLE"
        self.last_transcript = ""
        self.last_error = ""

    def capture_once(self) -> str:
        if self.state != "IDLE":
            raise RuntimeError("voice capture is already active")
        self.state = "CAPTURING"
        self.last_error = ""
        try:
            transcript = str(self._recognizer()).strip()
            if not transcript:
                raise RuntimeError("voice recognizer returned empty text")
            self.last_transcript = transcript
            return transcript
        except Exception as exc:
            self.last_error = str(exc)
            raise
        finally:
            self.state = "IDLE"
