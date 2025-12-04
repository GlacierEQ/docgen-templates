#!/usr/bin/env python3
"""
Jurisdiction Registry - Multi-Court Support
"""

from typing import Dict, List, Optional
from dataclasses import dataclass, field
from enum import Enum

class CourtLevel(Enum):
    STATE_FAMILY = "state_family"
    FEDERAL_DISTRICT = "federal_district"
    FEDERAL_CIRCUIT = "federal_circuit"

@dataclass
class FormattingRules:
    font_family: str = "Times New Roman"
    font_size: int = 12
    line_spacing: float = 2.0
    margin_top: float = 1.0
    margin_bottom: float = 1.0
    margin_left: float = 1.0
    margin_right: float = 1.0

@dataclass
class CourtProfile:
    court_id: str
    court_name: str
    court_level: CourtLevel
    jurisdiction: str
    formatting: FormattingRules
    special_rules: Dict[str, any] = field(default_factory=dict)

class JurisdictionRegistry:
    def __init__(self):
        self.profiles: Dict[str, CourtProfile] = {}
        self._load_default_profiles()
        
    def _load_default_profiles(self):
        # Hawaii Family Court
        self.register_profile(CourtProfile(
            court_id="hi_family",
            court_name="Hawaii Family Court",
            court_level=CourtLevel.STATE_FAMILY,
            jurisdiction="Hawaii",
            formatting=FormattingRules(),
            special_rules={"verification_required": True}
        ))
        
        # Northern District of California
        self.register_profile(CourtProfile(
            court_id="cand",
            court_name="US District Court, Northern District of California",
            court_level=CourtLevel.FEDERAL_DISTRICT,
            jurisdiction="California (ND)",
            formatting=FormattingRules(),
            special_rules={"ecf_filing": True}
        ))
        
        # Ninth Circuit
        self.register_profile(CourtProfile(
            court_id="ca9",
            court_name="US Court of Appeals, Ninth Circuit",
            court_level=CourtLevel.FEDERAL_CIRCUIT,
            jurisdiction="Ninth Circuit",
            formatting=FormattingRules(font_family="Century Schoolbook", font_size=14),
            special_rules={"word_limit": 14000}
        ))
        
    def register_profile(self, profile: CourtProfile) -> None:
        self.profiles[profile.court_id] = profile
        
    def get_profile(self, court_id: str) -> Optional[CourtProfile]:
        return self.profiles.get(court_id)
