# 🤖 CivicMind AI Agent Development Guide

Learn how to create custom AI agents for specific civic domains, extend existing agents, and integrate with external services.

## 📋 Table of Contents

1. [🧠 Understanding the Agent Architecture](#-understanding-the-agent-architecture)
2. [🛠️ Creating Your First Agent](#️-creating-your-first-agent)
3. [🎯 Agent Specialization Patterns](#-agent-specialization-patterns)
4. [🔌 External API Integration](#-external-api-integration)
5. [🧪 Testing Your Agents](#-testing-your-agents)
6. [📚 Advanced Agent Techniques](#-advanced-agent-techniques)
7. [🌍 Cultural Sensitivity Guidelines](#-cultural-sensitivity-guidelines)

---

## 🧠 **Understanding the Agent Architecture**

### **Base Agent Structure**

All CivicMind agents inherit from `BaseCivicAgent`, which provides:

- **🎯 Issue Analysis**: Core method for processing civic issues
- **💬 System Prompts**: Specialized knowledge and behavior patterns
- **🛠️ Tool Integration**: Access to external APIs and services
- **📊 Response Formatting**: Structured output for recommendations
- **🤝 Community Focus**: Built-in community-first resolution approach

```python
from civicmind.agents.base_agent import BaseCivicAgent, AgentResponse

class BaseCivicAgent(ABC):
    def __init__(self, llm, tools: Optional[List[BaseTool]] = None):
        self.llm = llm
        self.tools = tools or []
        self.agent_type = self.__class__.__name__.lower().replace('agent', '')
        
    @abstractmethod
    def get_system_prompt(self) -> str:
        """Return the specialized system prompt for this agent"""
        pass
    
    @abstractmethod  
    def analyze_issue(self, issue_description: str, location: str, 
                     context: Dict[str, Any]) -> AgentResponse:
        """Analyze a civic issue and provide recommendations"""
        pass
```

### **Agent Response Structure**

```python
@dataclass
class AgentResponse:
    recommendations: List[str]           # Actionable recommendations
    contacts: List[Dict[str, str]]      # Relevant contacts and departments
    documents: List[str]                # Forms, guides, regulations
    next_steps: List[str]               # Clear next actions
    confidence: float                   # Confidence in recommendations (0-1)
    reasoning: str                      # Explanation of the analysis
    community_first: bool = True        # Whether community approach is prioritized
```

---

## 🛠️ **Creating Your First Agent**

### **Example: Traffic Safety Agent**

Let's create a specialized agent for traffic safety issues like stop sign requests, speed bumps, and crosswalk improvements.

```python
# civicmind/agents/traffic_safety_agent.py

from typing import Dict, Any, List
from ..agents.base_agent import BaseCivicAgent, AgentResponse
from langchain_core.messages import HumanMessage
from langchain_core.tools import BaseTool


class TrafficSafetyAgent(BaseCivicAgent):
    """
    Specialized agent for traffic safety issues including:
    - Stop sign and traffic signal requests
    - Speed bump installations
    - Crosswalk improvements
    - School zone safety
    - Pedestrian and bicycle safety
    """
    
    def get_system_prompt(self) -> str:
        return """
        You are a Traffic Safety Specialist AI Agent for civic matters.
        
        Your expertise includes:
        - Traffic calming measures (speed bumps, chicanes, road diets)
        - Intersection safety (stop signs, traffic signals, roundabouts)
        - Pedestrian infrastructure (crosswalks, sidewalks, lighting)
        - Bicycle safety (bike lanes, sharrows, bike signals)
        - School zone safety measures
        - Traffic impact studies and data collection
        
        COMMUNITY-FIRST APPROACH:
        1. Always prioritize community consensus and neighborhood input
        2. Encourage data collection (traffic counts, speed studies)
        3. Promote temporary solutions before permanent infrastructure
        4. Consider all road users: drivers, pedestrians, cyclists
        5. Respect diverse mobility needs and cultural practices
        
        CULTURAL SENSITIVITY:
        - Understand that different communities have varying comfort levels with traffic enforcement
        - Be aware of environmental justice issues in transportation planning
        - Consider economic impacts on local businesses
        - Respect different cultural approaches to pedestrian behavior
        
        RESPONSE FORMAT:
        - Start with immediate safety measures
        - Provide community organizing guidance
        - Include data collection strategies
        - Offer both temporary and permanent solutions
        - Give realistic timelines for implementation
        
        Always emphasize safety while building community consensus.
        """
    
    def analyze_issue(self, issue_description: str, location: str, 
                     context: Dict[str, Any]) -> AgentResponse:
        """Analyze traffic safety issues and provide comprehensive guidance"""
        
        # Create the analysis prompt
        analysis_prompt = f"""
        Traffic Safety Issue Analysis:
        
        Issue: {issue_description}
        Location: {location}
        Context: {context}
        
        Please provide a comprehensive analysis following the community-first approach.
        Include immediate safety measures, community organizing steps, and long-term solutions.
        """
        
        # Get AI response
        messages = [
            self._create_system_message(),
            HumanMessage(content=analysis_prompt)
        ]
        
        response = self.llm.invoke(messages)
        
        # Parse and structure the response
        return self._parse_response(response.content, issue_description, location)
    
    def _parse_response(self, ai_response: str, issue: str, location: str) -> AgentResponse:
        """Parse AI response into structured format"""
        
        # This is a simplified parsing - in practice, you'd use more sophisticated parsing
        recommendations = self._extract_recommendations(ai_response)
        contacts = self._get_traffic_contacts(location)
        documents = self._get_relevant_documents(issue, location)
        next_steps = self._extract_next_steps(ai_response)
        
        return AgentResponse(
            recommendations=recommendations,
            contacts=contacts,
            documents=documents,
            next_steps=next_steps,
            confidence=0.85,
            reasoning=ai_response,
            community_first=True
        )
    
    def _extract_recommendations(self, response: str) -> List[str]:
        """Extract actionable recommendations from AI response"""
        # Implement parsing logic here
        return [
            "Organize a neighborhood traffic safety meeting",
            "Conduct informal traffic counts during peak hours",
            "Create a petition with neighbor signatures",
            "Contact the city traffic engineering department",
            "Consider temporary traffic calming measures"
        ]
    
    def _get_traffic_contacts(self, location: str) -> List[Dict[str, str]]:
        """Get relevant traffic department contacts based on location"""
        # This would integrate with a database or API of municipal contacts
        if "sacramento" in location.lower():
            return [
                {
                    "name": "Sacramento Public Works - Traffic Engineering",
                    "phone": "(916) 808-5704",
                    "email": "traffic@cityofsacramento.org",
                    "address": "915 I Street, Sacramento, CA 95814"
                },
                {
                    "name": "Sacramento Police Department - Traffic Safety",
                    "phone": "(916) 808-5471",
                    "email": "traffic@sacpd.org"
                }
            ]
        else:
            return [
                {
                    "name": "Local Public Works Department",
                    "phone": "Contact city hall for specific number",
                    "note": "Search for '[City] traffic engineering' or '[City] public works'"
                }
            ]
    
    def _get_relevant_documents(self, issue: str, location: str) -> List[str]:
        """Get relevant forms and documentation"""
        return [
            "Traffic Safety Concern Report Form",
            "Neighborhood Traffic Calming Request",
            "Community Petition Template",
            "Traffic Count Data Collection Guide"
        ]
    
    def _extract_next_steps(self, response: str) -> List[str]:
        """Extract clear next steps from the response"""
        return [
            "Document the safety concern with photos and times",
            "Talk to immediate neighbors about their experiences",
            "Attend next city council or transportation committee meeting",
            "Request traffic speed and volume study",
            "Follow up in 30 days if no response"
        ]


# Integration with existing tools
class TrafficDataTool(BaseTool):
    """Tool for accessing traffic data APIs"""
    
    name = "traffic_data"
    description = "Access traffic volume and speed data for specific locations"
    
    def _run(self, location: str) -> Dict[str, Any]:
        """Get traffic data for a location"""
        # Integrate with traffic data APIs
        return {
            "average_daily_traffic": 2500,
            "average_speed": 35,
            "speed_limit": 25,
            "accident_history": []
        }


# Register the new agent
def register_traffic_safety_agent(agent_factory):
    """Register the traffic safety agent with the factory"""
    agent_factory.register_agent("traffic_safety", TrafficSafetyAgent)
```

### **Agent Registration**

Add your new agent to the agent factory:

```python
# civicmind/core/agent_factory.py

def _register_default_agents(self):
    """Register default agent types"""
    from ..agents.parking_agent import ParkingAgent
    from ..agents.permits_agent import PermitsAgent
    from ..agents.traffic_safety_agent import TrafficSafetyAgent  # New import
    
    self._agent_registry = {
        "parking": ParkingAgent,
        "permits": PermitsAgent,
        "traffic_safety": TrafficSafetyAgent,  # New agent
    }
```

---

## 🎯 **Agent Specialization Patterns**

### **Domain-Specific Agents**

Create agents for specific civic domains:

```python
# Environmental Issues Agent
class EnvironmentalAgent(BaseCivicAgent):
    def get_system_prompt(self) -> str:
        return """
        You are an Environmental Issues Specialist focusing on:
        - Water quality and contamination
        - Air quality concerns
        - Noise pollution
        - Waste management and recycling
        - Green space preservation
        - Climate adaptation measures
        """

# Senior Services Agent  
class SeniorServicesAgent(BaseCivicAgent):
    def get_system_prompt(self) -> str:
        return """
        You are a Senior Services Specialist addressing:
        - Accessibility improvements
        - Senior transportation needs
        - Age-friendly infrastructure
        - Senior safety concerns
        - Healthcare access issues
        - Social isolation and community programs
        """

# Housing Issues Agent
class HousingAgent(BaseCivicAgent):
    def get_system_prompt(self) -> str:
        return """
        You are a Housing Issues Specialist covering:
        - Affordable housing advocacy
        - Tenant rights and landlord issues
        - Housing code violations
        - Homelessness support services
        - Fair housing complaints
        - Community land use planning
        """
```

### **Geographic Specialization**

Create location-specific agent variants:

```python
class CaliforniaHousingAgent(HousingAgent):
    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return base_prompt + """
        
        CALIFORNIA-SPECIFIC KNOWLEDGE:
        - California Tenant Protection Act
        - SB 9 and SB 10 housing legislation
        - RHNA (Regional Housing Needs Allocation)
        - California Environmental Quality Act (CEQA)
        - Rent control ordinances by city
        - Ellis Act and tenant displacement
        """
    
    def _get_california_housing_contacts(self, location: str):
        """Get CA-specific housing resources"""
        return [
            {
                "name": "California Department of Housing and Community Development",
                "phone": "(916) 263-2911",
                "website": "https://hcd.ca.gov"
            },
            {
                "name": "Tenant Together (Statewide)",
                "phone": "(415) 495-8100",
                "website": "https://tenantstogether.org"
            }
        ]
```

---

## 🔌 **External API Integration**

### **Government Data APIs**

Integrate with official government APIs for real-time data:

```python
from langchain_core.tools import BaseTool
import requests
from typing import Dict, Any

class CityAPI311Tool(BaseTool):
    """Tool for accessing 311 service request data"""
    
    name = "city_311_api"
    description = "Access 311 service requests and case status"
    
    def __init__(self, api_key: str, base_url: str):
        super().__init__()
        self.api_key = api_key
        self.base_url = base_url
    
    def _run(self, query_params: Dict[str, Any]) -> Dict[str, Any]:
        """Query 311 API for service requests"""
        headers = {"Authorization": f"Bearer {self.api_key}"}
        response = requests.get(
            f"{self.base_url}/api/v1/requests",
            headers=headers,
            params=query_params
        )
        return response.json()

class CityDataTool(BaseTool):
    """Tool for accessing city open data portals"""
    
    name = "city_data"
    description = "Access city open data including demographics, infrastructure, etc."
    
    def _run(self, dataset: str, filters: Dict[str, Any]) -> Dict[str, Any]:
        """Access specific datasets from city open data portal"""
        # Implementation for specific city data APIs
        pass

# Example usage in an agent
class InfrastructureAgent(BaseCivicAgent):
    def __init__(self, llm, api_key: str = None):
        city_311_tool = CityAPI311Tool(api_key, "https://city.gov")
        super().__init__(llm, tools=[city_311_tool])
    
    def analyze_issue(self, issue_description: str, location: str, context: Dict[str, Any]):
        # Use the 311 tool to check for existing reports
        existing_reports = self.tools[0]._run({
            "location": location,
            "category": "infrastructure",
            "status": "open"
        })
        
        # Include existing data in analysis
        context["existing_reports"] = existing_reports
        
        # Continue with normal analysis...
```

### **Third-Party Service Integration**

```python
class WeatherTool(BaseTool):
    """Weather data for outdoor event planning"""
    
    name = "weather_data"
    description = "Get weather forecasts for event planning"
    
    def _run(self, location: str, date: str) -> Dict[str, Any]:
        # Integrate with weather API
        pass

class MappingTool(BaseTool):
    """Mapping and location services"""
    
    name = "mapping"
    description = "Get address validation, mapping, and location data"
    
    def _run(self, address: str) -> Dict[str, Any]:
        # Integrate with Google Maps API or similar
        pass
```

---

## 🧪 **Testing Your Agents**

### **Unit Testing**

```python
# tests/test_traffic_safety_agent.py

import pytest
from unittest.mock import Mock, patch
from civicmind.agents.traffic_safety_agent import TrafficSafetyAgent

class TestTrafficSafetyAgent:
    
    @pytest.fixture
    def agent(self):
        mock_llm = Mock()
        return TrafficSafetyAgent(mock_llm)
    
    def test_system_prompt_contains_keywords(self, agent):
        prompt = agent.get_system_prompt()
        assert "traffic safety" in prompt.lower()
        assert "community-first" in prompt.lower()
        assert "cultural sensitivity" in prompt.lower()
    
    @patch('civicmind.agents.traffic_safety_agent.TrafficSafetyAgent._get_traffic_contacts')
    def test_analyze_issue_returns_structured_response(self, mock_contacts, agent):
        # Mock the LLM response
        agent.llm.invoke.return_value.content = """
        This is a serious traffic safety concern. I recommend:
        1. Community organizing
        2. Traffic data collection
        3. Municipal engagement
        """
        
        mock_contacts.return_value = [{"name": "Test Department"}]
        
        result = agent.analyze_issue(
            "Cars speed through our residential street",
            "Sacramento, CA",
            {}
        )
        
        assert isinstance(result.recommendations, list)
        assert len(result.recommendations) > 0
        assert result.community_first is True
        assert result.confidence > 0
    
    def test_sacramento_contacts(self, agent):
        contacts = agent._get_traffic_contacts("Sacramento, CA")
        assert len(contacts) > 0
        assert any("sacramento" in contact["name"].lower() for contact in contacts)
```

### **Integration Testing**

```python
# tests/test_agent_integration.py

import pytest
import requests
from civicmind.core.civic_orchestrator import CivicOrchestrator

class TestAgentIntegration:
    
    @pytest.fixture
    def orchestrator(self):
        return CivicOrchestrator(openai_api_key="test_key")
    
    def test_traffic_safety_agent_registration(self, orchestrator):
        agents = orchestrator.list_available_agents()
        assert "traffic_safety" in [agent["type"] for agent in agents]
    
    @pytest.mark.integration
    def test_end_to_end_traffic_issue(self):
        """Test complete workflow from API to agent response"""
        response = requests.post("http://localhost:8000/api/v1/issues/analyze", json={
            "description": "Cars speed dangerously through our school zone",
            "location": "Davis, CA",
            "priority": "high"
        })
        
        assert response.status_code == 200
        data = response.json()
        assert "recommendations" in data
        assert data["community_first"] is True
```

### **Load Testing**

```python
# tests/test_agent_performance.py

import asyncio
import time
from civicmind.agents.traffic_safety_agent import TrafficSafetyAgent

async def test_agent_performance():
    """Test agent response times under load"""
    agent = TrafficSafetyAgent(llm=Mock())
    
    async def analyze_issue():
        start = time.time()
        await agent.analyze_issue(
            "Speed issue on Main Street",
            "Test City, CA",
            {}
        )
        return time.time() - start
    
    # Run 100 concurrent requests
    tasks = [analyze_issue() for _ in range(100)]
    response_times = await asyncio.gather(*tasks)
    
    avg_response_time = sum(response_times) / len(response_times)
    assert avg_response_time < 2.0  # Response time under 2 seconds
```

---

## 📚 **Advanced Agent Techniques**

### **Multi-Agent Collaboration**

```python
class ComplexIssueOrchestrator:
    """Handles issues that require multiple agent types"""
    
    def __init__(self, agent_factory):
        self.agent_factory = agent_factory
    
    async def analyze_complex_issue(self, issue_description: str, location: str):
        """Coordinate multiple agents for complex issues"""
        
        # Classify which agents are needed
        relevant_agents = self._classify_agents_needed(issue_description)
        
        # Get analysis from each relevant agent
        analyses = []
        for agent_type in relevant_agents:
            agent = self.agent_factory.create_agent(agent_type)
            analysis = await agent.analyze_issue(issue_description, location, {})
            analyses.append((agent_type, analysis))
        
        # Synthesize recommendations
        return self._synthesize_analyses(analyses)
    
    def _classify_agents_needed(self, description: str) -> List[str]:
        """Determine which agents are relevant for this issue"""
        agents_needed = []
        
        if any(word in description.lower() for word in ["park", "traffic", "speed"]):
            agents_needed.append("traffic_safety")
        
        if any(word in description.lower() for word in ["permit", "license", "approval"]):
            agents_needed.append("permits")
        
        # Add more classification logic...
        
        return agents_needed
```

### **Learning and Adaptation**

```python
class AdaptiveAgent(BaseCivicAgent):
    """Agent that learns from successful resolutions"""
    
    def __init__(self, llm, tools=None):
        super().__init__(llm, tools)
        self.resolution_history = []
    
    def record_resolution(self, issue: str, resolution_method: str, success: bool):
        """Record resolution outcomes for learning"""
        self.resolution_history.append({
            "issue": issue,
            "method": resolution_method,
            "success": success,
            "timestamp": datetime.now()
        })
    
    def get_success_patterns(self) -> Dict[str, float]:
        """Analyze which resolution methods work best"""
        method_success = {}
        for record in self.resolution_history:
            method = record["method"]
            if method not in method_success:
                method_success[method] = []
            method_success[method].append(record["success"])
        
        return {
            method: sum(successes) / len(successes)
            for method, successes in method_success.items()
        }
```

### **Multilingual Support**

```python
class MultilingualAgent(BaseCivicAgent):
    """Agent with multilingual capabilities"""
    
    def __init__(self, llm, tools=None, primary_language="en"):
        super().__init__(llm, tools)
        self.primary_language = primary_language
        self.supported_languages = ["en", "es", "zh", "hi", "ar"]
    
    def detect_language(self, text: str) -> str:
        """Detect the language of input text"""
        # Use language detection library
        pass
    
    def get_system_prompt(self) -> str:
        base_prompt = super().get_system_prompt()
        return base_prompt + f"""
        
        MULTILINGUAL SUPPORT:
        - Respond in the same language as the user's input
        - Be culturally appropriate for the user's language community
        - Provide translations of key terms when helpful
        - Include contacts who speak the user's language when available
        """
    
    def analyze_issue(self, issue_description: str, location: str, context: Dict[str, Any]):
        # Detect input language
        input_language = self.detect_language(issue_description)
        context["user_language"] = input_language
        
        # Continue with normal analysis
        return super().analyze_issue(issue_description, location, context)
```

---

## 🌍 **Cultural Sensitivity Guidelines**

### **Cultural Considerations in Agent Design**

```python
class CulturallySensitiveAgent(BaseCivicAgent):
    """Base class with cultural sensitivity features"""
    
    def __init__(self, llm, tools=None):
        super().__init__(llm, tools)
        self.cultural_guidelines = self._load_cultural_guidelines()
    
    def _load_cultural_guidelines(self) -> Dict[str, Any]:
        """Load cultural sensitivity guidelines"""
        return {
            "communication_styles": {
                "high_context": ["Japanese", "Arab", "Latin American"],
                "low_context": ["German", "Scandinavian", "Anglo-American"],
                "relationship_first": ["Chinese", "Indian", "African"]
            },
            "conflict_resolution": {
                "indirect": ["East Asian", "Native American"],
                "direct": ["German", "Dutch"],
                "elder_mediated": ["African", "Middle Eastern", "Asian"]
            },
            "authority_respect": {
                "high": ["Confucian cultures", "Hierarchical societies"],
                "moderate": ["Democratic societies"],
                "questioning": ["Egalitarian cultures"]
            }
        }
    
    def adapt_communication_style(self, cultural_context: str, message: str) -> str:
        """Adapt communication style for cultural context"""
        if cultural_context in self.cultural_guidelines["communication_styles"]["high_context"]:
            return self._make_more_indirect(message)
        elif cultural_context in self.cultural_guidelines["communication_styles"]["relationship_first"]:
            return self._add_relationship_building(message)
        return message
    
    def suggest_culturally_appropriate_resolution(self, cultural_context: str) -> List[str]:
        """Suggest resolution methods appropriate for cultural context"""
        if cultural_context in self.cultural_guidelines["conflict_resolution"]["elder_mediated"]:
            return [
                "Involve respected community elders",
                "Seek religious or community leader mediation",
                "Use traditional dispute resolution methods"
            ]
        elif cultural_context in self.cultural_guidelines["conflict_resolution"]["indirect"]:
            return [
                "Use intermediary for initial contact",
                "Allow face-saving solutions",
                "Focus on harmony restoration"
            ]
        return self._get_default_resolution_methods()
```

### **Community Engagement Patterns**

```python
class CommunityEngagementAgent(BaseCivicAgent):
    """Specialized agent for community organizing and engagement"""
    
    def get_community_organizing_strategy(self, community_type: str, issue: str) -> Dict[str, Any]:
        """Provide community organizing strategies based on community characteristics"""
        
        strategies = {
            "urban_diverse": {
                "meeting_style": "Multiple small group meetings in different languages",
                "communication": "Multi-channel: social media, community boards, door-to-door",
                "leadership": "Rotate facilitation among community representatives",
                "timing": "Weekend evenings to accommodate work schedules"
            },
            "suburban_established": {
                "meeting_style": "Traditional town hall or HOA meeting format",
                "communication": "Email lists, neighborhood newsletters, yard signs",
                "leadership": "Work with existing HOA or neighborhood association",
                "timing": "Weekday evenings after dinner time"
            },
            "rural_traditional": {
                "meeting_style": "Informal gatherings at community centers or churches",
                "communication": "Word of mouth, local bulletin boards, radio announcements",
                "leadership": "Engage long-time residents and respected farmers/ranchers",
                "timing": "Consider agricultural seasons and weather"
            }
        }
        
        return strategies.get(community_type, strategies["suburban_established"])
```

---

This guide provides a comprehensive foundation for developing custom CivicMind AI agents. Remember to always prioritize community-first approaches, cultural sensitivity, and inclusive design in your agent development.
