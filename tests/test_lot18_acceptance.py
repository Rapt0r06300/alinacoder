import hashlib,unittest
from alinacoder.release.acceptance import AcceptanceEvidence,AcceptanceGate,ReleaseBundle,TraceabilityMatrix
class Lot18AcceptanceTests(unittest.TestCase):
 def test_traceability_requires_all_mandatory_domains(self):
  m=TraceabilityMatrix(required_domains={'conversation','goal','security','verification'});m.cover('conversation','src/a.py','tests/a.py');m.cover('goal','src/b.py','tests/b.py');m.cover('security','src/c.py','tests/c.py');self.assertFalse(m.complete());m.cover('verification','src/d.py','tests/d.py');self.assertTrue(m.complete())
 def test_runtime_ready_requires_fresh_pass_for_every_gate(self):
  h=hashlib.sha256(b'exe').hexdigest();g=AcceptanceGate(required={'spec','tests','package','install','security'},commit_sha='abc',artifact_sha256=h)
  for n in g.required:g.add(AcceptanceEvidence(n,'PASS','abc',h,True))
  self.assertTrue(g.runtime_v0_2_ready())
 def test_stale_or_wrong_commit_evidence_is_rejected(self):
  g=AcceptanceGate(required={'tests'},commit_sha='new',artifact_sha256='hash');g.add(AcceptanceEvidence('tests','PASS','old','hash',True));self.assertFalse(g.runtime_v0_2_ready())
 def test_release_bundle_requires_exe_setup_manifest_sbom_and_docs(self):
  self.assertTrue(ReleaseBundle({'AlinaCoder.exe','AlinaCoderSetup.exe','release-manifest.json','sbom.spdx.json','USER_GUIDE.md','OPERATIONS.md'}).complete());self.assertFalse(ReleaseBundle({'AlinaCoder.exe'}).complete())
if __name__=='__main__':unittest.main()
