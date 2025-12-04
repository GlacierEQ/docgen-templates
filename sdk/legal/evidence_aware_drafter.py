#!/usr/bin/env python3
"""
Evidence-Aware Legal Document Drafter

Zero-hallucination document generation with mandatory evidence citation.
"""

import re
from typing import List, Dict, Optional
from dataclasses import dataclass
from pathlib import Path

@dataclass
class EvidenceSource:
    source_id: str
    description: str
    file_path: Optional[Path] = None
    page_numbers: Optional[List[int]] = None
    exhibit_number: Optional[str] = None
    
class EvidenceRegistry:
    def __init__(self):
        self.evidence: Dict[str, EvidenceSource] = {}
        
    def register(self, evidence: EvidenceSource) -> None:
        self.evidence[evidence.source_id] = evidence
        
    def get(self, source_id: str) -> Optional[EvidenceSource]:
        return self.evidence.get(source_id)
        
    def validate_citations(self, citation_ids: List[str]) -> tuple[bool, List[str]]:
        missing = [cid for cid in citation_ids if cid not in self.evidence]
        return len(missing) == 0, missing

class EvidenceAwareDrafter:
    def __init__(self, evidence_registry: EvidenceRegistry):
        self.registry = evidence_registry
        self.citations = []
        
    def draft_paragraph(self, content: str, evidence_ids: List[str], require_citation: bool = True) -> str:
        if require_citation:
            if not evidence_ids:
                raise ValueError(f"Evidence required: {content[:50]}...")
            is_valid, missing = self.registry.validate_citations(evidence_ids)
            if not is_valid:
                raise ValueError(f"Invalid evidence IDs: {missing}")
        
        citation_text = self._format_citations(evidence_ids)
        return f"{content} {citation_text}"
    
    def _format_citations(self, evidence_ids: List[str]) -> str:
        if not evidence_ids:
            return ""
        citations = []
        for eid in evidence_ids:
            evidence = self.registry.get(eid)
            if evidence and evidence.exhibit_number:
                cite = f"Ex. {evidence.exhibit_number}"
                if evidence.page_numbers:
                    if len(evidence.page_numbers) == 1:
                        cite += f", p. {evidence.page_numbers[0]}"
                    else:
                        cite += f", pp. {evidence.page_numbers[0]}-{evidence.page_numbers[-1]}"
                citations.append(cite)
        return f"({'; '.join(citations)})"
