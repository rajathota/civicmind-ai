"""
CivicMind AI Agent Framework
===========================

A comprehensive framework for building AI agents that solve civic problems.
This package provides the core components for creating intelligent civic assistants.
"""

__version__ = "0.1.0"
__author__ = "Raja Kishore Thota"
__email__ = "your-email@domain.com"

from .core.agent_factory import AgentFactory
from .core.civic_orchestrator import CivicOrchestrator
from .agents.base_agent import BaseCivicAgent

__all__ = [
    "AgentFactory",
    "CivicOrchestrator", 
    "BaseCivicAgent"
]
