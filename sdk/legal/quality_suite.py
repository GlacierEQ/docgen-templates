#!/usr/bin/env python3
"""
Quality Suite - Automated Testing
"""

import unittest

class DocumentQualityTests(unittest.TestCase):
    def test_evidence_required(self):
        from evidence_aware_drafter import EvidenceRegistry, EvidenceAwareDrafter, EvidenceSource
        
        registry = EvidenceRegistry()
        registry.register(EvidenceSource(source_id="test", description="Test", exhibit_number="A"))
        drafter = EvidenceAwareDrafter(registry)
        
        # Should succeed
        result = drafter.draft_paragraph("Claim", evidence_ids=["test"])
        self.assertIn("Ex. A", result)
        
        # Should fail
        with self.assertRaises(ValueError):
            drafter.draft_paragraph("Unsupported claim", evidence_ids=[])

if __name__ == "__main__":
    unittest.main()
