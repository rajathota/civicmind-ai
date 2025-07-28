"""
Core Civic Orchestrator
=======================

The main orchestrator that routes civic issues to appropriate agents using LangGraph.
This is the heart of the CivicMind framework.
"""

from typing import Dict, List, Optional, Any
import asyncio
from datetime import datetime
from dataclasses import dataclass
from enum import Enum

from langchain_openai import ChatOpenAI
from langchain_core.messages import HumanMessage, SystemMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolExecutor
from pydantic import BaseModel

class IssueType(Enum):
    PARKING = "parking"
    NOISE = "noise"
    PERMITS = "permits"
    INFRASTRUCTURE = "infrastructure"
    BUSINESS = "home_business"
    RELIGIOUS_EVENTS = "religious_events"
    NEIGHBOR_DISPUTE = "neighbor_dispute"
    ENVIRONMENTAL = "environmental"
    UNKNOWN = "unknown"

class Priority(Enum):
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"

@dataclass
class CivicIssue:
    """Represents a civic issue raised by a citizen"""
    id: str
    description: str
    location: Optional[str] = None
    issue_type: IssueType = IssueType.UNKNOWN
    priority: Priority = Priority.MEDIUM
    citizen_info: Dict[str, Any] = None
    timestamp: datetime = None
    context: Dict[str, Any] = None

class CivicState(BaseModel):
    """State object that flows through the agent graph"""
    issue: CivicIssue
    analysis: Dict[str, Any] = {}
    recommendations: List[str] = []
    contacts: List[Dict[str, str]] = []
    documents: List[str] = []
    next_steps: List[str] = []
    resolution_path: str = "community_first"  # community_first or legal_direct
    
class CivicOrchestrator:
    """
    Main orchestrator for routing civic issues through appropriate agents
    """
    
    def __init__(self, 
                 openai_api_key: str,
                 model_name: str = "gpt-4o",
                 langsmith_api_key: Optional[str] = None):
        self.llm = ChatOpenAI(
            api_key=openai_api_key,
            model=model_name,
            temperature=0.1
        )
        
        self.langsmith_api_key = langsmith_api_key
        self.agents = {}
        self.graph = None
        self._build_agent_graph()
    
    def _build_agent_graph(self):
        """Build the LangGraph workflow for agent orchestration"""
        
        workflow = StateGraph(CivicState)
        
        # Add nodes
        workflow.add_node("classify_issue", self._classify_issue)
        workflow.add_node("analyze_context", self._analyze_context)
        workflow.add_node("route_to_agent", self._route_to_agent)
        workflow.add_node("generate_recommendations", self._generate_recommendations)
        workflow.add_node("prepare_documents", self._prepare_documents)
        workflow.add_node("community_resolution", self._community_resolution)
        workflow.add_node("legal_escalation", self._legal_escalation)
        
        # Add edges
        workflow.set_entry_point("classify_issue")
        workflow.add_edge("classify_issue", "analyze_context")
        workflow.add_edge("analyze_context", "route_to_agent")
        workflow.add_edge("route_to_agent", "generate_recommendations")
        
        # Conditional routing based on resolution path
        workflow.add_conditional_edges(
            "generate_recommendations",
            self._should_try_community_first,
            {
                "community": "community_resolution",
                "legal": "legal_escalation",
                "documents": "prepare_documents"
            }
        )
        
        workflow.add_edge("community_resolution", END)
        workflow.add_edge("legal_escalation", END)
        workflow.add_edge("prepare_documents", END)
        
        self.graph = workflow.compile()
    
    async def process_issue(self, issue: CivicIssue) -> CivicState:
        """
        Process a civic issue through the agent pipeline
        """
        initial_state = CivicState(issue=issue)
        
        # Run through the graph
        result = await self.graph.ainvoke(initial_state)
        return result
    
    def _classify_issue(self, state: CivicState) -> CivicState:
        """Classify the type of civic issue"""
        
        classification_prompt = f"""
        Analyze this civic issue and classify it:
        
        Issue: {state.issue.description}
        Location: {state.issue.location}
        
        Classify into one of these types:
        - parking: Parking violations, disputes, permits
        - noise: Noise complaints, sound ordinances
        - permits: Building, event, business permits
        - infrastructure: Roads, utilities, public works
        - home_business: Running business from home
        - religious_events: Cultural/religious event planning
        - neighbor_dispute: Interpersonal neighbor conflicts
        - environmental: Pollution, waste, environmental issues
        - unknown: Cannot classify
        
        Also determine priority: low, medium, high, urgent
        
        Return in format: TYPE|PRIORITY|REASONING
        """
        
        response = self.llm.invoke([SystemMessage(content=classification_prompt)])
        
        try:
            parts = response.content.strip().split('|')
            issue_type = IssueType(parts[0].strip().lower())
            priority = Priority(parts[1].strip().lower())
            reasoning = parts[2] if len(parts) > 2 else ""
            
            state.issue.issue_type = issue_type
            state.issue.priority = priority
            state.analysis["classification_reasoning"] = reasoning
            
        except (ValueError, IndexError):
            state.issue.issue_type = IssueType.UNKNOWN
            state.issue.priority = Priority.MEDIUM
        
        return state
    
    def _analyze_context(self, state: CivicState) -> CivicState:
        """Analyze the context and gather additional information"""
        
        context_prompt = f"""
        Analyze this civic issue for context and requirements:
        
        Issue: {state.issue.description}
        Type: {state.issue.issue_type.value}
        Location: {state.issue.location}
        
        Determine:
        1. What local laws or ordinances might apply?
        2. Which government departments would handle this?
        3. What information is missing that we need to collect?
        4. Are there community-level solutions to try first?
        5. What cultural or social sensitivities should we consider?
        
        Provide analysis in JSON format.
        """
        
        response = self.llm.invoke([SystemMessage(content=context_prompt)])
        
        # Parse response and add to state
        state.analysis["context_analysis"] = response.content
        
        return state
    
    def _route_to_agent(self, state: CivicState) -> CivicState:
        """Route to the appropriate specialized agent"""
        
        # This would route to specific agents based on issue type
        agent_name = f"{state.issue.issue_type.value}_agent"
        state.analysis["assigned_agent"] = agent_name
        
        return state
    
    def _generate_recommendations(self, state: CivicState) -> CivicState:
        """Generate recommendations for resolving the issue"""
        
        recommendations_prompt = f"""
        Generate specific, actionable recommendations for this civic issue:
        
        Issue: {state.issue.description}
        Type: {state.issue.issue_type.value}
        Analysis: {state.analysis.get('context_analysis', 'None')}
        
        Provide:
        1. Immediate actions the citizen can take
        2. Community-level solutions to try first
        3. Government contacts and departments
        4. Required documents or forms
        5. Timeline and expectations
        
        Format as numbered list of actionable steps.
        """
        
        response = self.llm.invoke([SystemMessage(content=recommendations_prompt)])
        
        # Parse recommendations
        recommendations = [
            line.strip() for line in response.content.split('\n') 
            if line.strip() and not line.strip().startswith('#')
        ]
        
        state.recommendations = recommendations
        
        return state
    
    def _should_try_community_first(self, state: CivicState) -> str:
        """Determine if community resolution should be tried first"""
        
        # Community-first issues
        community_first_types = [
            IssueType.NEIGHBOR_DISPUTE,
            IssueType.NOISE,
            IssueType.PARKING
        ]
        
        if state.issue.issue_type in community_first_types:
            return "community"
        elif state.issue.issue_type == IssueType.PERMITS:
            return "documents"
        else:
            return "legal"
    
    def _community_resolution(self, state: CivicState) -> CivicState:
        """Handle community-level resolution approaches"""
        
        community_steps = [
            "Try friendly conversation with neighbor",
            "Consult community mediator or HOA",
            "Post in neighborhood app for advice",
            "Attend community meeting if available"
        ]
        
        state.next_steps.extend(community_steps)
        state.resolution_path = "community_first"
        
        return state
    
    def _legal_escalation(self, state: CivicState) -> CivicState:
        """Handle legal/government escalation"""
        
        legal_steps = [
            "Contact appropriate city department",
            "File formal complaint if needed",
            "Follow up within specified timeframe",
            "Consider legal consultation if unresolved"
        ]
        
        state.next_steps.extend(legal_steps)
        state.resolution_path = "legal_direct"
        
        return state
    
    def _prepare_documents(self, state: CivicState) -> CivicState:
        """Prepare necessary documents and forms"""
        
        # This would generate actual documents based on the issue type
        state.documents = [
            "Completed application form",
            "Supporting documentation checklist",
            "Contact information for follow-up"
        ]
        
        return state

# Example usage
if __name__ == "__main__":
    import os
    
    # Initialize orchestrator
    orchestrator = CivicOrchestrator(
        openai_api_key=os.getenv("OPENAI_API_KEY")
    )
    
    # Create a sample issue
    sample_issue = CivicIssue(
        id="issue_001",
        description="My neighbor's dog barks loudly every night from 11 PM to 2 AM. It's affecting my sleep and my family's well-being.",
        location="Folsom, CA",
        timestamp=datetime.now()
    )
    
    # Process the issue
    async def test_orchestrator():
        result = await orchestrator.process_issue(sample_issue)
        print(f"Issue Type: {result.issue.issue_type}")
        print(f"Priority: {result.issue.priority}")
        print(f"Recommendations: {result.recommendations}")
        print(f"Next Steps: {result.next_steps}")
    
    # Run the test
    asyncio.run(test_orchestrator())
