"""Input-preservation checks, independent of the TeX engine."""
import importlib.util
import tempfile
import unittest
from pathlib import Path

SOURCE = Path(__file__).resolve().parents[1]

class StagingTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        spec = importlib.util.spec_from_file_location('avia_build_test', SOURCE/'scripts/build.py')
        self.build = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(self.build)
        self.build.ROOT = Path(self.temp.name)
        self.build.BUILD = self.build.ROOT/'.build'
        (self.build.ROOT/'main.tex').write_text('Manuscrito de prueba', encoding='utf-8')
        (self.build.ROOT/'assets').mkdir()

    def test_manuscript_assets_preserved(self):
        asset = self.build.ROOT/'assets/tall.pdf'
        self.build.shape_pdf(asset, 33, 17)
        original = asset.read_bytes()
        # Staging copies bytes; actual image decoding belongs to the PDF build.
        upper = self.build.ROOT/'assets/IMAGEN.PNG'
        upper.write_bytes(b'input-preservation-sentinel')
        manifest = self.build.prepare(False, 10)
        self.assertEqual(manifest['cases'][0]['min_pages'], 1)
        stage = self.build.BUILD/'cases/demo/assets'
        self.assertEqual((stage/'tall.pdf').read_bytes(), original)
        self.assertEqual((stage/'IMAGEN.PNG').read_bytes(), upper.read_bytes())
        self.assertIn('assets/IMAGEN.PNG', manifest['source_hashes'])
        self.assertFalse((stage/'wide.pdf').exists())
        self.assertFalse((stage/'square.pdf').exists())

    def test_stale_pdf_and_aux_are_not_reused(self):
        (self.build.ROOT/'main.pdf').write_bytes(b'old-pdf')
        (self.build.ROOT/'main.aux').write_text('old-aux')
        self.build.prepare(False, 10)
        stage = self.build.BUILD/'cases/demo'
        self.assertFalse((stage/'main.pdf').exists())
        self.assertFalse((stage/'main.aux').exists())
        approved = self.build.BUILD/'approved'
        approved.mkdir()
        (approved/'main.pdf').write_bytes(b'old-approved-pdf')
        self.build.prepare(False, 10)
        self.assertFalse(approved.exists())

if __name__=='__main__':
    unittest.main()
