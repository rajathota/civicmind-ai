"""
Parking Agent for CivicMind Framework
====================================

Specialized agent for handling parking-related civic issues.
"""

from typing import Dict, Any
from ..agents.base_agent import BaseCivicAgent, AgentResponse
from langchain_core.messages import HumanMessage


class ParkingAgent(BaseCivicAgent):
    """
    Specialized agent for parking violations, disputes, and regulations
    """
    
    def get_system_prompt(self) -> str:
        return """
        You are a Parking Issues Specialist AI Agent for civic matters.
        
        Your expertise includes:
        - Parking violations and enforcement
        - Residential parking permits
        - Commercial loading zones
        - Disability parking requirements
        - Street cleaning schedules
        - Neighbor parking disputes
        
        Approach:
        1. First encourage friendly neighbor communication
        2. Check local parking ordinances and time restrictions
        3. Identify if it's a recurring issue or one-time occurrence
        4. Provide contact information for parking enforcement
        5. Suggest documentation methods (photos, times, license plates)
        
        Always consider community harmony before legal escalation.
        Be empathetic to both the reporter and the alleged violator.
        """
    
    def analyze_issue(self, issue_description: str, location: str,
                     context: Dict[str, Any]) -> AgentResponse:
        """Analyze parking-related issues"""
        
        analysis_prompt = f"""
        Analyze this parking issue and provide guidance:
        
        Issue: {issue_description}
        Location: {location}
        Context: {context}
        
        {self.get_common_civic_context(location)}
        
        Provide structured response:
        
        Recommendations:
        - [List 3-5 specific recommendations]
        
        Contacts:
        - [Relevant departments/contacts]
        
        Documents:
        - [Any forms or documentation needed]
        
        Next Steps:
        - [Specific actions in order of priority]
        
        Consider:
        1. Is this a safety issue or inconvenience?
        2. Are there time restrictions or permits involved?
        3. Can this be resolved through neighbor communication?
        4. What evidence should be collected?
        5. When to escalate to parking enforcement?
        """
        
        response = self.llm.invoke([
            self._create_system_message(),
            HumanMessage(content=analysis_prompt)
        ])
        
        return self._format_response(response.content)


class NoiseAgent(BaseCivicAgent):
    """
    Specialized agent for noise complaints and sound ordinances
    """
    
    def get_system_prompt(self) -> str:
        return """
        You are a Noise Complaint Specialist AI Agent for civic matters.
        
        Your expertise includes:
        - Noise ordinances and quiet hours
        - Construction noise permits
        - Pet noise issues (barking dogs)
        - Music and party complaints
        - Commercial noise violations
        - Mediation between neighbors
        
        Approach:
        1. Understand the noise type, frequency, and timing
        2. Check local noise ordinances and permitted hours
        3. Encourage diplomatic neighbor conversation first
        4. Provide guidance on documenting noise issues
        5. Suggest mediation services when appropriate
        6. Explain escalation to police or code enforcement
        
        Be sensitive to cultural differences in noise tolerance.
        Consider both immediate relief and long-term solutions.
        """
    
    def analyze_issue(self, issue_description: str, location: str,
                     context: Dict[str, Any]) -> AgentResponse:
        """Analyze noise-related issues"""
        
        analysis_prompt = f"""
        Analyze this noise complaint and provide guidance:
        
        Issue: {issue_description}
        Location: {location}
        Context: {context}
        
        {self.get_common_civic_context(location)}
        
        Provide structured response:
        
        Recommendations:
        - [List 3-5 specific recommendations]
        
        Contacts:
        - [Relevant departments/contacts for noise issues]
        
        Documents:
        - [Any forms or documentation needed]
        
        Next Steps:
        - [Specific actions prioritizing community resolution]
        
        Consider:
        1. What are the local quiet hours?
        2. Is this ongoing or occasional?
        3. Could this be resolved with neighbor conversation?
        4. How to document the noise issue?
        5. When does it warrant police involvement?
        6. Are there cultural or religious considerations?
        """
        
        response = self.llm.invoke([
            self._create_system_message(),
            HumanMessage(content=analysis_prompt)
        ])
        
        return self._format_response(response.content)
