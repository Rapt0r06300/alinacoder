from __future__ import annotations

import unittest

from alinacoder.desktop.experience import FirstRunOnboarding, VoiceInputAdapter, WindowsSpeechRecognizer
from alinacoder.product.provenance import ProvenanceEvidence, ReleaseAdmissionPolicy


class Lot14DesktopProductCompletionTests(unittest.TestCase):
    def test_first_run_onboarding_requires_project_and_inference_configuration(self) -> None:
        onboarding = FirstRunOnboarding()
        self.assertFalse(onboarding.complete)
        onboarding.configure_project(r"C:\repo")
        onboarding.configure_inference(provider_mode="local-only", local_runtime="ollama")
        onboarding.enable_input_mode("text")
        onboarding.enable_input_mode("voice")
        onboarding.finish()
        self.assertTrue(onboarding.complete)
        restored = FirstRunOnboarding.from_dict(onboarding.to_dict())
        self.assertEqual(restored.project_path, r"C:\repo")
        self.assertEqual(restored.provider_mode, "local-only")
        self.assertIn("voice", restored.input_modes)

    def test_onboarding_fails_closed_if_no_inference_route_is_configured(self) -> None:
        onboarding = FirstRunOnboarding()
        onboarding.configure_project(r"C:\repo")
        with self.assertRaises(ValueError):
            onboarding.finish()

    def test_voice_adapter_is_stateful_and_injectable_without_microphone(self) -> None:
        adapter = VoiceInputAdapter(lambda: "corrige ce bug puis lance les tests")
        self.assertEqual(adapter.state, "IDLE")
        transcript = adapter.capture_once()
        self.assertEqual(transcript, "corrige ce bug puis lance les tests")
        self.assertEqual(adapter.state, "IDLE")
        self.assertEqual(adapter.last_transcript, transcript)

    def test_windows_speech_recognizer_builds_local_powershell_command(self) -> None:
        command = WindowsSpeechRecognizer().powershell_script()
        self.assertIn("System.Speech", command)
        self.assertIn("SetInputToDefaultAudioDevice", command)
        self.assertNotIn("http://", command.lower())
        self.assertNotIn("https://", command.lower())


class Lot16ReleaseProvenanceCompletionTests(unittest.TestCase):
    def test_rc_requires_verified_commit_bound_provenance_and_sbom(self) -> None:
        evidence = ProvenanceEvidence(
            commit_sha="abc123",
            artifact_sha256="f" * 64,
            provenance_verified=True,
            sbom_verified=True,
            signer_identity="github-actions://Rapt0r06300/alinacoder/.github/workflows/ci.yml",
            authenticode_verified=False,
        )
        policy = ReleaseAdmissionPolicy(channel="rc")
        self.assertTrue(policy.admit(evidence, expected_commit="abc123", expected_artifact_sha256="f" * 64))
        self.assertFalse(policy.admit(evidence, expected_commit="different", expected_artifact_sha256="f" * 64))

    def test_production_channel_requires_authenticode_in_addition_to_provenance(self) -> None:
        evidence = ProvenanceEvidence(
            commit_sha="abc123",
            artifact_sha256="f" * 64,
            provenance_verified=True,
            sbom_verified=True,
            signer_identity="github-actions://Rapt0r06300/alinacoder/.github/workflows/ci.yml",
            authenticode_verified=False,
        )
        self.assertFalse(
            ReleaseAdmissionPolicy(channel="production").admit(
                evidence,
                expected_commit="abc123",
                expected_artifact_sha256="f" * 64,
            )
        )


if __name__ == "__main__":
    unittest.main()
