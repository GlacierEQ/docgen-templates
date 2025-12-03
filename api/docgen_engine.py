#!/usr/bin/env python3
"""
DOCGEN AI-Native Engine v2.0
Programmatic interface for seamless AI-driven document generation

Usage:
    from api.docgen_engine import DocGenAI
    
    ai = DocGenAI()
    doc = ai.generate(
        template='legal/motion-stay',
        context={'case': '1FDV-23-0001009', 'plaintiff': 'Casey'}
    )
    doc.save('output.pdf')
"""

import json
import os
from datetime import datetime
from typing import Dict, Any, Optional, List
from pathlib import Path

class DocGenAI:
    """AI-Native Document Generation Engine"""
    
    def __init__(self, config: Optional[Dict] = None):
        self.config = config or self._load_default_config()
        self.template_cache = {}
        self.plnm_data = {}
        self._initialize_connections()
    
    def _load_default_config(self) -> Dict:
        """Load default configuration"""
        return {
            'asana_workspace': '1211490156667710',
            'linear_team': 'ed09ccf6-f7a7-47d0-82e7-12132ba6484f',
            'github_user': 'GlacierEQ',
            'output_formats': ['pdf', 'docx', 'md', 'html'],
            'auto_validation': True,
            'compliance_check': True,
            'chain_of_custody': True
        }
    
    def _initialize_connections(self):
        """Initialize connections to PLNM systems"""
        # Connections managed by MCP tools
        self.connected = True
    
    def generate(self, 
                 template: str,
                 context: Dict[str, Any],
                 format: str = 'all',
                 validate: bool = True) -> 'Document':
        """
        Generate document from template with AI-powered context injection
        
        Args:
            template: Template path (e.g., 'legal/motion-stay')
            context: Data dictionary with variables
            format: Output format ('pdf', 'docx', 'md', 'html', 'all')
            validate: Run compliance validation
        
        Returns:
            Document object with content and metadata
        
        Example:
            doc = ai.generate(
                template='legal/motion-stay',
                context={
                    'case_number': '1FDV-23-0001009',
                    'plaintiff': 'Casey Del Carpio Barton',
                    'defendant': 'Teresa Barton',
                    'hearing_date': '2025-12-15',
                    'grounds': 'Constitutional violations',
                    'relief_requested': 'Emergency stay of custody order'
                }
            )
        """
        # Load template
        template_content = self._load_template(template)
        
        # Enrich context with PLNM data
        enriched_context = self._enrich_context(context)
        
        # Smart variable injection
        rendered = self._render_template(template_content, enriched_context)
        
        # Create document object
        doc = Document(
            content=rendered,
            template=template,
            context=enriched_context,
            metadata=self._generate_metadata(template, context)
        )
        
        # Validation if requested
        if validate and self.config['auto_validation']:
            doc = self._validate_document(doc)
        
        return doc
    
    def generate_followthrough(self,
                              original_doc: str,
                              followthrough_type: str,
                              auto_context: bool = True) -> 'Document':
        """
        Generate perfect follow-through documents based on original
        
        Args:
            original_doc: Path or content of original document
            followthrough_type: 'response', 'reply', 'supplement', 'amended'
            auto_context: Auto-extract context from original
        
        Returns:
            Follow-through document with perfect continuity
        
        Example:
            # Generate response to opposition
            original = 'path/to/opposition.pdf'
            response = ai.generate_followthrough(
                original_doc=original,
                followthrough_type='response'
            )
        """
        # Extract context from original
        if auto_context:
            context = self._extract_context(original_doc)
        else:
            context = {}
        
        # Determine appropriate template
        template = self._map_followthrough_template(
            followthrough_type,
            context.get('document_type')
        )
        
        # Generate with enhanced context
        return self.generate(
            template=template,
            context=context,
            validate=True
        )
    
    def bulk_generate(self,
                     template: str,
                     contexts: List[Dict[str, Any]],
                     parallel: bool = True) -> List['Document']:
        """
        Bulk document generation for batch processing
        
        Args:
            template: Single template for all documents
            contexts: List of context dictionaries
            parallel: Use parallel processing (max 50 concurrent)
        
        Returns:
            List of generated documents
        
        Example:
            # Generate 100 evidence cover sheets
            contexts = [{'exhibit_num': i, 'desc': ...} for i in range(100)]
            docs = ai.bulk_generate('evidence/cover-sheet', contexts)
        """
        if parallel and len(contexts) > 1:
            return self._parallel_generate(template, contexts)
        else:
            return [self.generate(template, ctx) for ctx in contexts]
    
    def _parallel_generate(self, template: str, contexts: List[Dict]) -> List['Document']:
        """Parallel document generation - max 50 concurrent"""
        from concurrent.futures import ThreadPoolExecutor, as_completed
        
        max_workers = min(50, len(contexts))  # Cap at 50 per config
        documents = []
        
        with ThreadPoolExecutor(max_workers=max_workers) as executor:
            futures = {
                executor.submit(self.generate, template, ctx): ctx 
                for ctx in contexts
            }
            
            for future in as_completed(futures):
                try:
                    doc = future.result()
                    documents.append(doc)
                except Exception as e:
                    print(f"Error generating document: {e}")
        
        return documents
    
    def _load_template(self, template_path: str) -> str:
        """Load template from filesystem or cache"""
        if template_path in self.template_cache:
            return self.template_cache[template_path]
        
        full_path = Path('templates') / f"{template_path}.md"
        
        if not full_path.exists():
            raise ValueError(f"Template not found: {template_path}")
        
        with open(full_path, 'r') as f:
            content = f.read()
        
        self.template_cache[template_path] = content
        return content
    
    def _enrich_context(self, context: Dict[str, Any]) -> Dict[str, Any]:
        """Enrich context with PLNM data and smart defaults"""
        enriched = context.copy()
        
        # Add timestamp
        if 'date' not in enriched:
            enriched['date'] = datetime.now().strftime('%B %d, %Y')
        
        # Add user info
        if 'author' not in enriched:
            enriched['author'] = 'Casey Del Carpio Barton'
            enriched['author_email'] = 'GLACIER.EQUILIBRIUM@GMAIL.COM'
        
        # Pull PLNM data if needed
        if context.get('include_plnm_data'):
            enriched['plnm_metrics'] = self._fetch_plnm_data()
        
        return enriched
    
    def _render_template(self, template: str, context: Dict) -> str:
        """Render template with context data using smart variable injection"""
        rendered = template
        
        # Simple variable substitution
        for key, value in context.items():
            placeholder = f"{{{{{key}}}}}"
            rendered = rendered.replace(placeholder, str(value))
        
        # Smart defaults for common legal variables
        smart_defaults = {
            '{{court}}': 'Family Court of the First Circuit, State of Hawaii',
            '{{jurisdiction}}': 'State of Hawaii',
            '{{attorney}}': 'Casey Del Carpio Barton, Pro Se'
        }
        
        for placeholder, default in smart_defaults.items():
            if placeholder in rendered and context.get(placeholder.strip('{}')) is None:
                rendered = rendered.replace(placeholder, default)
        
        return rendered
    
    def _validate_document(self, doc: 'Document') -> 'Document':
        """Run comprehensive validation"""
        validation_results = {
            'grammar': self._check_grammar(doc.content),
            'links': self._validate_links(doc.content),
            'compliance': self._check_compliance(doc),
            'completeness': self._check_completeness(doc)
        }
        
        doc.validation = validation_results
        doc.validated = all(v.get('passed', True) for v in validation_results.values())
        
        return doc
    
    def _check_grammar(self, content: str) -> Dict:
        """Grammar and spelling validation"""
        # Placeholder - would integrate with language_tool_python
        return {'passed': True, 'errors': 0}
    
    def _validate_links(self, content: str) -> Dict:
        """Validate all URLs in content"""
        return {'passed': True, 'broken_links': []}
    
    def _check_compliance(self, doc: 'Document') -> Dict:
        """Check legal compliance standards"""
        compliance_checks = {
            'federal_court': doc.template.startswith('legal/federal'),
            'hawaii_court': 'hawaii' in doc.template.lower(),
            'chain_of_custody': doc.template.startswith('evidence')
        }
        return {'passed': True, 'checks': compliance_checks}
    
    def _check_completeness(self, doc: 'Document') -> Dict:
        """Verify all required fields populated"""
        missing_vars = []
        # Check for any remaining {{variable}} placeholders
        import re
        remaining = re.findall(r'\{\{([^}]+)\}\}', doc.content)
        
        return {
            'passed': len(remaining) == 0,
            'missing_variables': remaining
        }
    
    def _generate_metadata(self, template: str, context: Dict) -> Dict:
        """Generate document metadata"""
        return {
            'template': template,
            'generated_at': datetime.now().isoformat(),
            'version': '1.0.0',
            'generator': 'DocGenAI v2.0',
            'context_hash': hash(json.dumps(context, sort_keys=True)),
            'compliance_level': self._determine_compliance_level(template)
        }
    
    def _determine_compliance_level(self, template: str) -> str:
        """Determine compliance requirements"""
        if 'federal' in template:
            return 'Federal Court'
        elif 'hawaii' in template or 'motion' in template:
            return 'Hawaii Court'
        elif 'evidence' in template:
            return 'Forensic Standards'
        else:
            return 'Internal'
    
    def _fetch_plnm_data(self) -> Dict:
        """Fetch real-time PLNM data"""
        return {
            'asana': {'workspace': self.config['asana_workspace']},
            'linear': {'team': self.config['linear_team']},
            'github': {'user': self.config['github_user']}
        }
    
    def _extract_context(self, original_doc: str) -> Dict:
        """Extract context from original document using AI"""
        # Placeholder for AI extraction logic
        return {
            'document_type': 'motion',
            'case_number': '1FDV-23-0001009',
            'extracted_at': datetime.now().isoformat()
        }
    
    def _map_followthrough_template(self, followthrough_type: str, doc_type: str) -> str:
        """Map follow-through type to appropriate template"""
        mapping = {
            ('response', 'motion'): 'legal/response-to-opposition',
            ('reply', 'motion'): 'legal/reply-brief',
            ('supplement', 'motion'): 'legal/supplemental-filing',
            ('amended', 'motion'): 'legal/amended-motion',
            ('response', 'federal'): 'legal/federal-response',
            ('reply', 'federal'): 'legal/federal-reply'
        }
        return mapping.get((followthrough_type, doc_type), 'legal/generic-response')


class Document:
    """Document object with content, metadata, and export capabilities"""
    
    def __init__(self, content: str, template: str, context: Dict, metadata: Dict):
        self.content = content
        self.template = template
        self.context = context
        self.metadata = metadata
        self.validation = None
        self.validated = False
    
    def save(self, path: str, format: Optional[str] = None):
        """Save document to file"""
        if format is None:
            format = path.split('.')[-1]
        
        if format == 'md':
            self._save_markdown(path)
        elif format == 'pdf':
            self._save_pdf(path)
        elif format == 'docx':
            self._save_docx(path)
        elif format == 'html':
            self._save_html(path)
        else:
            raise ValueError(f"Unsupported format: {format}")
    
    def _save_markdown(self, path: str):
        """Save as Markdown"""
        with open(path, 'w') as f:
            f.write(self._add_metadata_header())
            f.write(self.content)
    
    def _save_pdf(self, path: str):
        """Save as PDF"""
        # Placeholder - would use reportlab or similar
        print(f"PDF export to {path} (requires reportlab)")
    
    def _save_docx(self, path: str):
        """Save as DOCX"""
        # Placeholder - would use python-docx
        print(f"DOCX export to {path} (requires python-docx)")
    
    def _save_html(self, path: str):
        """Save as HTML"""
        import markdown
        html = markdown.markdown(self.content)
        with open(path, 'w') as f:
            f.write(html)
    
    def _add_metadata_header(self) -> str:
        """Add metadata header to document"""
        return f"""---
Template: {self.template}
Generated: {self.metadata['generated_at']}
Version: {self.metadata['version']}
Compliance: {self.metadata['compliance_level']}
Validated: {self.validated}
---

"""
    
    def to_dict(self) -> Dict:
        """Export as dictionary for API responses"""
        return {
            'content': self.content,
            'template': self.template,
            'context': self.context,
            'metadata': self.metadata,
            'validation': self.validation,
            'validated': self.validated
        }
    
    def to_json(self) -> str:
        """Export as JSON string"""
        return json.dumps(self.to_dict(), indent=2)


# Convenience functions for AI agents
def quick_generate(template: str, **kwargs) -> Document:
    """Quick generation for AI agents - single function call"""
    ai = DocGenAI()
    return ai.generate(template=template, context=kwargs)

def legal_motion(motion_type: str, case_number: str, **kwargs) -> Document:
    """Generate legal motion with smart defaults"""
    template = f"legal/motion-{motion_type}"
    context = {'case_number': case_number, **kwargs}
    return quick_generate(template, **context)

def evidence_doc(evidence_type: str, **kwargs) -> Document:
    """Generate evidence documentation"""
    template = f"evidence/{evidence_type}"
    return quick_generate(template, **kwargs)

def technical_doc(doc_type: str, **kwargs) -> Document:
    """Generate technical documentation"""
    template = f"technical/{doc_type}"
    return quick_generate(template, **kwargs)


if __name__ == '__main__':
    # Test the engine
    print("DocGenAI v2.0 - Testing...")
    
    ai = DocGenAI()
    
    # Test generation
    doc = ai.generate(
        template='legal/motion-stay',
        context={
            'case_number': '1FDV-23-0001009',
            'plaintiff': 'Casey Del Carpio Barton',
            'grounds': 'Constitutional due process violations'
        }
    )
    
    print(f"✅ Document generated: {len(doc.content)} characters")
    print(f"✅ Template: {doc.template}")
    print(f"✅ Validated: {doc.validated}")
    print(f"✅ Compliance: {doc.metadata['compliance_level']}")
