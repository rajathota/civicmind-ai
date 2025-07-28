"""
Agent Factory for CivicMind Framework
====================================

Factory class for creating and managing specialized civic agents.
"""

from typing import Dict, Type, Optional
from abc import ABC, abstractmethod

from langchain_openai import ChatOpenAI
from langchain_core.tools import BaseTool


class AgentFactory:
    """
    Factory for creating specialized civic agents
    """
    
    def __init__(self, openai_api_key: str, model_name: str = "gpt-4o"):
        self.openai_api_key = openai_api_key
        self.model_name = model_name
        self.llm = ChatOpenAI(
            api_key=openai_api_key,
            model=model_name,
            temperature=0.1
        )
        self._agent_registry = {}
        self._register_default_agents()
    
    def _register_default_agents(self):
        """Register default agent types"""
        from ..agents.parking_agent import ParkingAgent
        from ..agents.noise_agent import NoiseAgent
        from ..agents.permits_agent import PermitsAgent
        from ..agents.infrastructure_agent import InfrastructureAgent
        from ..agents.business_agent import BusinessAgent
        from ..agents.religious_events_agent import ReligiousEventsAgent
        from ..agents.neighbor_dispute_agent import NeighborDisputeAgent
        from ..agents.environmental_agent import EnvironmentalAgent
        
        self._agent_registry = {
            "parking": ParkingAgent,
            "noise": NoiseAgent,
            "permits": PermitsAgent,
            "infrastructure": InfrastructureAgent,
            "home_business": BusinessAgent,
            "religious_events": ReligiousEventsAgent,
            "neighbor_dispute": NeighborDisputeAgent,
            "environmental": EnvironmentalAgent
        }
    
    def create_agent(self, agent_type: str, **kwargs):
        """Create an agent of the specified type"""
        if agent_type not in self._agent_registry:
            raise ValueError(f"Unknown agent type: {agent_type}")
        
        agent_class = self._agent_registry[agent_type]
        return agent_class(llm=self.llm, **kwargs)
    
    def register_agent(self, agent_type: str, agent_class: Type):
        """Register a new agent type"""
        self._agent_registry[agent_type] = agent_class
    
    def list_agents(self) -> Dict[str, Type]:
        """List all registered agent types"""
        return self._agent_registry.copy()
