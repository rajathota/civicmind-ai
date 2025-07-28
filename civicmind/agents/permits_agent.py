"""
Permits Agent for CivicMind Framework
====================================

Specialized agent for handling permit-related civic issues.
"""

from typing import Dict, Any
from ..agents.base_agent import BaseCivicAgent, AgentResponse
from langchain_core.messages import HumanMessage


class PermitsAgent(BaseCivicAgent):
    """
    Specialized agent for permits, licenses, and regulatory compliance
    """
    
    def get_system_prompt(self) -> str:
        return """
        You are a Permits and Licensing Specialist AI Agent for civic matters.
        
        Your expertise includes:
        - Building and construction permits
        - Home business licenses
        - Event permits for gatherings
        - Tree removal permits
        - Fence and structure permits
        - Religious and cultural event permits
        
        Approach:
        1. Identify the specific type of permit needed
        2. Explain the application process clearly
        3. List required documents and fees
        4. Provide timeline expectations
        5. Suggest alternatives if permits are not required
        6. Connect with appropriate city departments
        
        Be thorough in explaining requirements to avoid delays.
        Consider cost-effective alternatives when appropriate.
        """
    
    def analyze_issue(self, issue_description: str, location: str,
                     context: Dict[str, Any]) -> AgentResponse:
        """Analyze permit-related issues"""
        
        analysis_prompt = f"""
        Analyze this permit inquiry and provide guidance:
        
        Issue: {issue_description}
        Location: {location}
        Context: {context}
        
        {self.get_common_civic_context(location)}
        
        Provide structured response:
        
        Recommendations:
        - [List specific permit requirements and alternatives]
        
        Contacts:
        - [Relevant city departments and offices]
        
        Documents:
        - [Required forms, plans, and supporting documents]
        
        Next Steps:
        - [Step-by-step application process]
        
        Consider:
        1. What type of permit is actually needed?
        2. Are there size/scope thresholds that apply?
        3. What are the fees and timeline?
        4. Are there alternatives that don't require permits?
        5. What happens if you proceed without a permit?
        6. Are there cultural or religious considerations for events?
        """
        
        response = self.llm.invoke([
            self._create_system_message(),
            HumanMessage(content=analysis_prompt)
        ])
        
        return self._format_response(response.content)
