#!/usr/bin/env python3
"""
DOCGEN AI SDK v2.0
One-line document generation for AI assistants

Usage:
    from sdk.ai_sdk import generate, followthrough
    
    # Single line document generation
    doc = generate('motion-stay', case='1FDV-23-0001009', grounds='Due process')
    
    # Perfect follow-through
    response = followthrough('opposition.pdf', type='response')
"""

import sys
import os
sys.path.insert(0, os.path.join(os.path.dirname(__file__), '..'))

from api.docgen_engine import DocGenAI
from api.ai_interface import AIDocGenInterface
from typing import Dict, Any, Optional, List
import json

# Global instances for convenience
_engine = None
_interface = None

def _get_engine() -> DocGenAI:
    """Lazy initialization of engine"""
    global _engine
    if _engine is None:
        _engine = DocGenAI()
    return _engine

def _get_interface() -> AIDocGenInterface:
    """Lazy initialization of interface"""
    global _interface
    if _interface is None:
        _interface = AIDocGenInterface()
    return _interface

# One-line generation functions
def generate(template: str, **context) -> str:
    """
    ONE-LINE DOCUMENT GENERATION
    
    Args:
        template: Template name (e.g., 'motion-stay', 'cover-sheet')
        **context: All variables as keyword arguments
    
    Returns:
        Generated document content as string
    
    Examples:
        # Legal motion
        doc = generate('motion-stay', 
                      case='1FDV-23-0001009',
                      grounds='Constitutional violations',
                      relief='Emergency stay')
        
        # Evidence cover sheet
        doc = generate('cover-sheet',
                      exhibit='A',
                      description='Medical records')
        
        # Technical spec
        doc = generate('api-spec',
                      api_name='DOCGEN v2.0',
                      version='2.0.0')
    """
    engine = _get_engine()
    doc = engine.generate(template=f'auto/{template}', context=context)
    return doc.content

def followthrough(original: str, type: str = 'response', **context) -> str:
    """
    PERFECT FOLLOW-THROUGH GENERATION
    
    Args:
        original: Original document path or content
        type: 'response', 'reply', 'supplement', 'amended'
        **context: Additional context overrides
    
    Returns:
        Follow-through document content
    
    Examples:
        # Auto-response to opposition
        response = followthrough('opposition.pdf', type='response')
        
        # Reply brief
        reply = followthrough('response.pdf', type='reply')
        
        # Supplemental filing
        supplement = followthrough('motion.pdf', type='supplement',
                                   new_evidence='Exhibit C added')
    """
    engine = _get_engine()
    doc = engine.generate_followthrough(
        original_doc=original,
        followthrough_type=type,
        auto_context=True
    )
    return doc.content

def motion(type: str, grounds: str, relief: str, **kwargs) -> str:
    """
    LEGAL MOTION - ULTRA SIMPLIFIED
    
    Args:
        type: Motion type ('stay', 'tro', 'modify-custody')
        grounds: Legal grounds
        relief: Relief requested
        **kwargs: Additional context
    
    Returns:
        Court-ready motion content
    
    Example:
        motion_content = motion(
            type='stay',
            grounds='Default during technical difficulties',
            relief='Stay execution of decree'
        )
    """
    interface = _get_interface()
    doc = interface.create_motion(type, grounds, relief, **kwargs)
    return doc.content

def evidence_package(exhibits: List[Dict]) -> List[str]:
    """
    EVIDENCE PACKAGE - BULK GENERATION
    
    Args:
        exhibits: List of exhibit dicts with 'id', 'type', 'desc'
    
    Returns:
        List of generated cover sheets
    
    Example:
        package = evidence_package([
            {'id': 'A', 'type': 'medical', 'desc': 'C-PTSD diagnosis'},
            {'id': 'B', 'type': 'photos', 'desc': 'Arm fracture images'},
            {'id': 'C', 'type': 'audio', 'desc': 'Custody exchange recording'}
        ])
    """
    interface = _get_interface()
    docs = interface.create_evidence_package(exhibits)
    return [d.content for d in docs]

def batch(template: str, data_file: str) -> List[str]:
    """
    BATCH GENERATION FROM DATA FILE
    
    Args:
        template: Template name
        data_file: CSV or JSON file path
    
    Returns:
        List of generated documents
    
    Example:
        # Generate 100 cover sheets from CSV
        docs = batch('cover-sheet', 'exhibits.csv')
    """
    interface = _get_interface()
    docs = interface.batch_generate_from_data(template, data_file)
    return [d.content for d in docs]

def validate(content: str, template: str = None) -> Dict:
    """
    VALIDATE DOCUMENT CONTENT
    
    Args:
        content: Document content to validate
        template: Optional template name for compliance checking
    
    Returns:
        Validation results dictionary
    
    Example:
        results = validate(motion_content, template='motion-stay')
        if results['passed']:
            print('Document valid!')
    """
    engine = _get_engine()
    from api.docgen_engine import Document
    
    doc = Document(
        content=content,
        template=template or 'unknown',
        context={},
        metadata={'generated_at': ''}
    )
    
    validated = engine._validate_document(doc)
    return {
        'passed': validated.validated,
        'results': validated.validation
    }

# REST API helpers
def api_generate(template: str, context: Dict, api_url: str = 'http://localhost:8000') -> Dict:
    """
    Generate via REST API (for remote AI agents)
    
    Example:
        result = api_generate(
            template='motion-stay',
            context={'case': '1FDV-23-0001009'},
            api_url='https://docgen.yourdomain.com'
        )
    """
    import requests
    response = requests.post(
        f'{api_url}/api/v2/generate',
        json={'template': template, 'context': context}
    )
    return response.json()

# Export all convenience functions
__all__ = [
    'generate',
    'followthrough', 
    'motion',
    'evidence_package',
    'batch',
    'validate',
    'api_generate'
]

if __name__ == '__main__':
    print("🤖 DOCGEN AI SDK - Ready for AI agent integration")
    print("\nQuick test:")
    
    # Test generation
    doc = generate('test', case='1FDV-23-0001009', test='Hello from AI SDK')
    print(f"✅ SDK operational - {len(doc)} characters generated")
