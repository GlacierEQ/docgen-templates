#!/usr/bin/env python3
"""
Multi-Model Router - AI Selection
"""

from enum import Enum
from typing import Dict, List

class ModelType(Enum):
    GPT4 = "gpt-4"
    CLAUDE_OPUS = "claude-3-opus"
    CLAUDE_SONNET = "claude-3-sonnet"

class TaskType(Enum):
    LEGAL_RESEARCH = "legal_research"
    DOCUMENT_GEN = "document_generation"
    LEGAL_ANALYSIS = "legal_analysis"

class ModelRouter:
    def __init__(self):
        self.fallbacks = {
            TaskType.LEGAL_RESEARCH: [ModelType.CLAUDE_OPUS, ModelType.GPT4],
            TaskType.DOCUMENT_GEN: [ModelType.CLAUDE_OPUS, ModelType.GPT4],
            TaskType.LEGAL_ANALYSIS: [ModelType.GPT4, ModelType.CLAUDE_OPUS]
        }
    
    def select_model(self, task_type: str) -> ModelType:
        try:
            task = TaskType(task_type)
            return self.fallbacks.get(task, [ModelType.GPT4])[0]
        except:
            return ModelType.GPT4
