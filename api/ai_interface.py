#!/usr/bin/env python3
"""
AI Agent Interface for DocGen
Simplified interface optimized for AI assistant integration
"""

from docgen_engine import DocGenAI, legal_motion, evidence_doc, technical_doc
import json

class AIDocGenInterface:
    """
    Simplified interface for AI assistants
    Single-function calls with intelligent defaults
    """
    
    def __init__(self):
        self.engine = DocGenAI()
        self.case_defaults = {
            'case_number': '1FDV-23-0001009',
            'court': 'Family Court of the First Circuit, State of Hawaii',
            'plaintiff': 'Casey Del Carpio Barton',
            'defendant': 'Teresa Barton',
            'child': 'Kekoa'
        }
    
    def create_motion(self, motion_type: str, grounds: str, relief: str, **kwargs):
        """
        Create legal motion with minimal input
        
        Example:
            doc = ai.create_motion(
                motion_type='stay',
                grounds='Constitutional due process violations',
                relief='Emergency stay of custody order'
            )
        """
        context = {**self.case_defaults, **kwargs}
        context.update({
            'grounds': grounds,
            'relief_requested': relief,
            'date': self._today()
        })
        
        return legal_motion(motion_type, context['case_number'], **context)
    
    def create_response(self, opposing_doc: str, response_points: List[str], **kwargs):
        """
        Create response to opposition with AI-extracted context
        
        Example:
            doc = ai.create_response(
                opposing_doc='path/to/opposition.pdf',
                response_points=[
                    'Plaintiff did appear via Zoom',
                    'Technical difficulties documented',
                    'Good cause exists for relief'
                ]
            )
        """
        context = {**self.case_defaults, **kwargs}
        context['response_points'] = response_points
        context['original_document'] = opposing_doc
        
        return self.engine.generate_followthrough(
            original_doc=opposing_doc,
            followthrough_type='response',
            auto_context=True
        )
    
    def create_evidence_package(self, exhibits: List[Dict], **kwargs):
        """
        Create complete evidence package with cover sheets
        
        Example:
            package = ai.create_evidence_package([
                {'id': 'A', 'type': 'medical', 'desc': 'C-PTSD diagnosis'},
                {'id': 'B', 'type': 'photos', 'desc': 'Fractured arm images'}
            ])
        """
        docs = []
        
        for exhibit in exhibits:
            context = {**self.case_defaults, **kwargs}
            context.update(exhibit)
            
            doc = evidence_doc(
                evidence_type='cover-sheet',
                **context
            )
            docs.append(doc)
        
        return docs
    
    def create_technical_spec(self, system: str, components: List[str], **kwargs):
        """
        Create technical specification document
        
        Example:
            spec = ai.create_technical_spec(
                system='DOCGEN v2.0',
                components=['API', 'Template Engine', 'CI/CD']
            )
        """
        context = {**kwargs}
        context.update({
            'system_name': system,
            'components': components,
            'date': self._today()
        })
        
        return technical_doc(
            doc_type='specification',
            **context
        )
    
    def batch_generate_from_data(self, template: str, data_source: str):
        """
        Generate multiple documents from data source (CSV, JSON, Excel)
        
        Example:
            docs = ai.batch_generate_from_data(
                template='evidence/cover-sheet',
                data_source='exhibits.csv'
            )
        """
        # Load data from source
        contexts = self._load_data_source(data_source)
        
        # Bulk generate
        return self.engine.bulk_generate(
            template=template,
            contexts=contexts,
            parallel=True
        )
    
    def _today(self) -> str:
        """Get today's date formatted"""
        from datetime import datetime
        return datetime.now().strftime('%B %d, %Y')
    
    def _load_data_source(self, path: str) -> List[Dict]:
        """Load data from CSV, JSON, or Excel"""
        if path.endswith('.json'):
            with open(path) as f:
                return json.load(f)
        elif path.endswith('.csv'):
            import csv
            with open(path) as f:
                return list(csv.DictReader(f))
        else:
            raise ValueError(f"Unsupported data format: {path}")


# Flask API routes using AIDocGenInterface
ai_interface = AIDocGenInterface()

@app.route('/ai/motion', methods=['POST'])
def ai_motion():
    """AI-optimized motion generation"""
    data = request.json
    doc = ai_interface.create_motion(
        motion_type=data['motion_type'],
        grounds=data['grounds'],
        relief=data['relief'],
        **data.get('additional_context', {})
    )
    return jsonify(doc.to_dict())

@app.route('/ai/response', methods=['POST'])
def ai_response():
    """AI-optimized response generation"""
    data = request.json
    doc = ai_interface.create_response(
        opposing_doc=data['opposing_doc'],
        response_points=data['response_points'],
        **data.get('additional_context', {})
    )
    return jsonify(doc.to_dict())

@app.route('/ai/evidence', methods=['POST'])
def ai_evidence():
    """AI-optimized evidence package generation"""
    data = request.json
    docs = ai_interface.create_evidence_package(
        exhibits=data['exhibits'],
        **data.get('additional_context', {})
    )
    return jsonify({
        'documents': [d.to_dict() for d in docs],
        'count': len(docs)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=8000)
