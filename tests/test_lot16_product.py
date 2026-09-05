import hashlib,unittest
from pathlib import Path
from alinacoder.product.core import ReleaseManifest,SBOMBuilder,UpdateVerifier,build_install_plan
class Lot16ProductTests(unittest.TestCase):
 def test_update_rejects_downgrade_and_hash_mismatch(self):
  v=UpdateVerifier(current_version='0.2.0',require_signature=False);self.assertFalse(v.accepts({'version':'0.1.9','sha256':'x'},artifact=b'x'));self.assertFalse(v.accepts({'version':'0.2.1','sha256':'bad'},artifact=b'x'));self.assertTrue(v.accepts({'version':'0.2.1','sha256':hashlib.sha256(b'x').hexdigest()},artifact=b'x'))
 def test_production_update_requires_trusted_signature(self):
  v=UpdateVerifier(current_version='0.2.0',require_signature=True);h=hashlib.sha256(b'x').hexdigest();self.assertFalse(v.accepts({'version':'0.2.1','sha256':h,'signature':'UNTRUSTED'},artifact=b'x'));self.assertTrue(v.accepts({'version':'0.2.1','sha256':h,'signature':'TRUSTED'},artifact=b'x'))
 def test_release_manifest_binds_artifact_to_commit(self):
  m=ReleaseManifest.from_bytes('0.2.0','abc123','AlinaCoder.exe',b'binary');self.assertEqual(m.commit_sha,'abc123');self.assertTrue(m.verify(b'binary'));self.assertFalse(m.verify(b'tampered'))
 def test_install_plan_is_per_user_and_explicit_about_data_retention(self):
  p=build_install_plan(version='0.2.0',install_dir=Path('C:/Users/test/AppData/Local/AlinaCoder'),preserve_user_data=True);self.assertTrue(p.preserve_user_data);self.assertIn('AlinaCoder.exe',str(p.executable))
 def test_sbom_lists_runtime_and_build_components(self):
  s=SBOMBuilder().build(['python-stdlib','pyinstaller==6.16.0']);self.assertEqual(s['spdxVersion'],'SPDX-2.3');self.assertEqual(len(s['packages']),2)
if __name__=='__main__':unittest.main()
