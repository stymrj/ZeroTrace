"""Unit tests for ZeroTrace modules."""
import unittest
from zerotrace.modules.email_intel import scan_email
from zerotrace.modules.domain_intel import scan_domain

class TestZeroTraceModules(unittest.TestCase):
    def test_email_validation_valid(self):
        res = scan_email("admin@github.com")
        self.assertEqual(res.get("Syntax Valid"), "Yes")
        self.assertEqual(res.get("Domain"), "github.com")

    def test_email_validation_invalid(self):
        res = scan_email("not-an-email")
        self.assertIn("error", res)

    def test_domain_recon_structure(self):
        res = scan_domain("github.com")
        self.assertIn("Domain", res)
        self.assertEqual(res["Domain"], "github.com")

if __name__ == '__main__':
    unittest.main()
