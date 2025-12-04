# Legal Document Templates

Legal Doc Gundam integrated templates with zero-hallucination enforcement.

## Available Templates

### Hawaii Family Court
- `hi_family_motion.tex` - Standard motion template
- Court profile: `hi_family`
- Features: Evidence enforcement, verification support

### Federal District Court (CAND)
- Court profile: `cand`
- Features: ECF compliance, page limits, TOA required

### Ninth Circuit
- Court profile: `ca9`
- Features: Word count limits, appellate formatting

## Usage

```python
from sdk.legal.evidence_aware_drafter import EvidenceRegistry, EvidenceAwareDrafter, EvidenceSource
from sdk.legal.jurisdiction_registry import JurisdictionRegistry

# Initialize evidence
registry = EvidenceRegistry()
registry.register(EvidenceSource(
    source_id="exhibit_a",
    description="Email from Respondent",
    exhibit_number="A",
    page_numbers=[1, 2]
))

# Draft with evidence
drafter = EvidenceAwareDrafter(registry)
para = drafter.draft_paragraph(
    "On January 1, 2024, Respondent sent an email.",
    evidence_ids=["exhibit_a"]
)
# Output: "On January 1, 2024, Respondent sent an email. (Ex. A, pp. 1-2)"

# Validate court compliance
jurisdictions = JurisdictionRegistry()
profile = jurisdictions.get_profile("hi_family")
```

## Court Profiles

- **hi_family**: Hawaii Family Court
- **cand**: Northern District of California
- **ca9**: Ninth Circuit Court of Appeals
