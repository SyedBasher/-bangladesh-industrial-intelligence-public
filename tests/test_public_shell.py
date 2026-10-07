"""Small, dependency-free safety and contract tests for the *public* shell only."""
import re
import subprocess
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
PREVIEW = ROOT / "index.html"
ALLOWED_TRACKED_FILES = {
    ".gitignore",
    ".github/workflows/public-ci.yml",
    "README.md",
    "index.html",
    "docs/DATA_POLICY.md",
    "docs/METHODOLOGY_OVERVIEW.md",
    "tests/test_public_shell.py",
}
PUBLIC_TEXT_FILES = (
    ROOT / "README.md",
    ROOT / "index.html",
    ROOT / "docs/DATA_POLICY.md",
    ROOT / "docs/METHODOLOGY_OVERVIEW.md",
    ROOT / ".github/workflows/public-ci.yml",
)


class PublicShellTests(unittest.TestCase):
    def test_expected_tracked_manifest_only(self):
        result = subprocess.run(
            ["git", "ls-files"],
            cwd=ROOT, capture_output=True, text=True, check=True
        )
        tracked = set(result.stdout.splitlines())
        self.assertEqual(tracked, ALLOWED_TRACKED_FILES)

    def test_preview_is_static_synthetic_and_independent(self):
        html = PREVIEW.read_text(encoding="utf-8")
        self.assertTrue(html.lstrip().lower().startswith("<!doctype html>"))
        self.assertIn("DEMO-001", html)
        self.assertIn("synthetic", html.lower())
        self.assertIn("not Bangladesh estimates", html)
        for pattern in (
            r"https?://", r"fetch\s*\(", r"XMLHttpRequest", r"WebSocket\s*\(",
            r"<iframe\b", r"<script\s+[^>]*src\s*=",
        ):
            with self.subTest(pattern=pattern):
                self.assertNotRegex(html, pattern)

    def test_no_credentials_or_private_paths_in_public_text(self):
        patterns = (
            r"gh[pousr]_[A-Za-z0-9]{20,}",
            r"github_pat_[A-Za-z0-9_]{20,}",
            r"sk-[A-Za-z0-9]{24,}",
            r"-----BEGIN (?:RSA |EC |OPENSSH )?PRIVATE KEY-----",
            r"(?i)C:\\\\Users\\\\",
        )
        for path in PUBLIC_TEXT_FILES:
            content = path.read_text(encoding="utf-8")
            for pattern in patterns:
                with self.subTest(file=path.name, pattern=pattern):
                    self.assertIsNone(re.search(pattern, content))

    def test_workflow_is_public_only(self):
        yml = (ROOT / ".github/workflows/public-ci.yml").read_text(encoding="utf-8")
        self.assertIn("permissions:\n  contents: read", yml)
        self.assertNotIn("${{ secrets.", yml)
        self.assertIn("uses: actions/checkout@v4", yml)
        self.assertIn("persist-credentials: false", yml)
        self.assertNotIn("secrets:", yml)
        self.assertNotRegex(yml, r"(?i)BEI_READ_TOKEN|CLOUDFLARE_API_TOKEN|repository:\s*SyedBasher/")

if __name__ == "__main__":
    unittest.main()
