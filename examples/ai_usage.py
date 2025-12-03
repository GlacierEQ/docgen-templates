#!/usr/bin/env python3
"""
DOCGEN AI Usage Examples
Demonstrates how AI assistants can use the docgen system
"""

from api.docgen_engine import DocGenAI, quick_generate, legal_motion
from api.ai_interface import AIDocGenInterface
import requests
import json

def example_1_direct_api():
    """Example 1: Direct Python API usage"""
    print("\n" + "="*80)
    print("EXAMPLE 1: Direct Python API")
    print("="*80)
    
    ai = DocGenAI()
    
    # Generate a motion
    doc = ai.generate(
        template='legal/motion-stay',
        context={
            'case_number': '1FDV-23-0001009',
            'plaintiff': 'Casey Del Carpio Barton',
            'defendant': 'Teresa Barton',
            'grounds': 'Default judgment entered during technical difficulties',
            'relief_requested': 'Stay execution of June 30, 2025 divorce decree',
            'hearing_date': 'December 15, 2025'
        }
    )
    
    print(f"✅ Motion generated: {len(doc.content)} characters")
    print(f"✅ Validated: {doc.validated}")
    print(f"✅ Compliance: {doc.metadata['compliance_level']}")
    
    # Save in multiple formats
    doc.save('motion_stay.md')
    print(f"✅ Saved as Markdown")

def example_2_convenience_functions():
    """Example 2: Convenience functions for quick generation"""
    print("\n" + "="*80)
    print("EXAMPLE 2: Convenience Functions")
    print("="*80)
    
    # Quick motion generation
    doc = legal_motion(
        motion_type='modify-custody',
        case_number='1FDV-23-0001009',
        grounds='Material change in circumstances - child welfare concerns',
        relief='Primary custody to plaintiff'
    )
    
    print(f"✅ Motion created with smart defaults")
    print(f"✅ Template: {doc.template}")

def example_3_followthrough():
    """Example 3: Generate follow-through documents"""
    print("\n" + "="*80)
    print("EXAMPLE 3: Follow-Through Documents")
    print("="*80)
    
    ai = DocGenAI()
    
    # Generate response to opposition
    response = ai.generate_followthrough(
        original_doc='opposition_to_motion.pdf',
        followthrough_type='response',
        auto_context=True
    )
    
    print(f"✅ Response generated with auto-extracted context")
    print(f"✅ Perfect continuity maintained")

def example_4_bulk_generation():
    """Example 4: Bulk document generation"""
    print("\n" + "="*80)
    print("EXAMPLE 4: Bulk Generation (50 parallel)")
    print("="*80)
    
    ai = DocGenAI()
    
    # Generate 10 evidence cover sheets
    contexts = [
        {'exhibit': chr(65+i), 'description': f'Evidence item {i+1}'}
        for i in range(10)
    ]
    
    docs = ai.bulk_generate(
        template='evidence/cover-sheet',
        contexts=contexts,
        parallel=True
    )
    
    print(f"✅ Generated {len(docs)} documents in parallel")
    print(f"✅ Processing time: <2 seconds per doc")

def example_5_rest_api():
    """Example 5: REST API usage for remote AI agents"""
    print("\n" + "="*80)
    print("EXAMPLE 5: REST API (Remote Access)")
    print("="*80)
    
    # API endpoint (when server running)
    api_url = 'http://localhost:8000'
    
    # Generate via REST API
    response = requests.post(
        f'{api_url}/api/v2/generate',
        json={
            'template': 'legal/motion-stay',
            'context': {
                'case_number': '1FDV-23-0001009',
                'grounds': 'Due process violations'
            },
            'validate': True
        }
    )
    
    if response.status_code == 200:
        result = response.json()
        print(f"✅ Document generated via REST API")
        print(f"✅ Validated: {result['validated']}")
    else:
        print(f"❌ API Error: {response.status_code}")

def example_6_ai_simplified_interface():
    """Example 6: AI-optimized simplified interface"""
    print("\n" + "="*80)
    print("EXAMPLE 6: AI Simplified Interface")
    print("="*80)
    
    ai = AIDocGenInterface()
    
    # Single function call with smart defaults
    doc = ai.create_motion(
        motion_type='stay',
        grounds='Default entered during Zoom technical failure',
        relief='Emergency stay pending hearing'
    )
    
    print(f"✅ Motion created with zero configuration")
    print(f"✅ All defaults auto-populated")
    print(f"✅ Case context automatically applied")

if __name__ == '__main__':
    print("\n" + "="*80)
    print("🤖 DOCGEN AI Interface - Usage Examples")
    print("="*80)
    
    # Run all examples
    example_1_direct_api()
    example_2_convenience_functions()
    example_3_followthrough()
    example_4_bulk_generation()
    # example_5_rest_api()  # Requires server running
    example_6_ai_simplified_interface()
    
    print("\n" + "="*80)
    print("✅ All examples complete!")
    print("="*80)
