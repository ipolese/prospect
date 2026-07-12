import hashlib
import importlib.util
import json
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


dashboard = load("dashboard_server", ROOT / "skills/dashboard-leads/references/dashboard-server.py")
publisher = load("secure_publisher", ROOT / "scripts/publicador-seguro.py")
preview = load("preview_server", ROOT / "scripts/servidor-sites.py")


class DashboardValidationTests(unittest.TestCase):
    def test_rejects_script_slug(self):
        with self.assertRaises(ValueError):
            dashboard.safe_slug("x');alert(1)//")

    def test_rejects_javascript_url(self):
        with self.assertRaises(ValueError):
            dashboard.safe_url("javascript:alert(1)")

    def test_rejects_unknown_fields(self):
        with self.assertRaises(ValueError):
            dashboard.validate_lead({"slug": "lead-ok", "admin": True})

    def test_rejects_invalid_status(self):
        with self.assertRaises(ValueError):
            dashboard.validate_lead({"slug": "lead-ok", "status": "root"})

    def test_escapes_stored_xss_for_legacy_template(self):
        class Row(dict):
            pass
        result = dashboard.public_lead(Row(slug="lead-ok", nome='<img src=x onerror="alert(1)">'))
        self.assertNotIn("<img", result["nome"])
        self.assertIn("&lt;img", result["nome"])

    def test_normalizes_contacts_for_duplicate_detection(self):
        self.assertEqual(dashboard.normalized_contact("https://www.Example.com/"), "examplecom")

    def test_rejects_non_http_url(self):
        with self.assertRaises(ValueError):
            dashboard.safe_url("file:///tmp/site.html")


class PreviewTests(unittest.TestCase):
    def test_blocks_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                preview.resolve_public_path(Path(tmp), "/../../prospector-config.json")

    def test_blocks_encoded_traversal(self):
        with tempfile.TemporaryDirectory() as tmp:
            with self.assertRaises(ValueError):
                preview.resolve_public_path(Path(tmp), "/%2e%2e/prospector.db")


class ManifestTests(unittest.TestCase):
    def make_workspace(self):
        tmp = tempfile.TemporaryDirectory()
        root = Path(tmp.name)
        page = root / "sites/cliente/cliente.html"
        page.parent.mkdir(parents=True)
        page.write_text("<h1>ok</h1>", encoding="utf-8")
        return tmp, root, page

    def write_manifest(self, root, page, origin=None, destination="public_html/clientes/cliente/index.html", digest=None):
        manifest = root / "manifest.json"
        manifest.write_text(json.dumps({
            "version": 1,
            "jobId": "job-12345678",
            "arquivos": [{
                "origem": origin or str(page.relative_to(root)),
                "destino": destination,
                "sha256": digest or hashlib.sha256(page.read_bytes()).hexdigest(),
            }],
        }), encoding="utf-8")
        return manifest

    def test_accepts_valid_site_file(self):
        tmp, root, page = self.make_workspace()
        try:
            _, files = publisher.validate_manifest(self.write_manifest(root, page), root)
            self.assertEqual(1, len(files))
        finally:
            tmp.cleanup()

    def test_rejects_file_outside_sites(self):
        tmp, root, page = self.make_workspace()
        try:
            secret = root / "prospector-config.json"
            secret.write_text("secret", encoding="utf-8")
            manifest = self.write_manifest(root, page, origin="prospector-config.json", digest=hashlib.sha256(secret.read_bytes()).hexdigest())
            with self.assertRaises(ValueError):
                publisher.validate_manifest(manifest, root)
        finally:
            tmp.cleanup()

    def test_rejects_remote_traversal(self):
        tmp, root, page = self.make_workspace()
        try:
            with self.assertRaises(ValueError):
                publisher.validate_manifest(self.write_manifest(root, page, destination="../../stolen.html"), root)
        finally:
            tmp.cleanup()

    def test_rejects_hash_mismatch(self):
        tmp, root, page = self.make_workspace()
        try:
            with self.assertRaises(ValueError):
                publisher.validate_manifest(self.write_manifest(root, page, digest="0" * 64), root)
        finally:
            tmp.cleanup()

    def test_rejects_batch_injection(self):
        tmp, root, page = self.make_workspace()
        try:
            with self.assertRaises(ValueError):
                publisher.validate_manifest(self.write_manifest(root, page, destination='public_html/x.html\nput "secret" "x"'), root)
        finally:
            tmp.cleanup()


if __name__ == "__main__":
    unittest.main()
