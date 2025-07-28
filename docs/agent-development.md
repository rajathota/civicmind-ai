# 🤖 Agent Development Guide

Complete guide for developing AI agents in CivicMind AI's microservices platform, including MCP server creation, agent specialization, and integration patterns.

## 🎯 Overview

CivicMind AI agents are intelligent, domain-specific AI assistants that provide natural language interfaces to civic services through the Model Context Protocol (MCP). Each agent specializes in a specific civic domain while integrating seamlessly with the broader microservices ecosystem.

### 🏗️ Agent Architecture

```
┌─────────────────┐    ┌─────────────────┐    ┌─────────────────┐
│   Citizen       │    │   AI Agent      │    │ Civic Service   │
│   Query         │ ──►│   (MCP Server)  │ ──►│   (REST API)    │
└─────────────────┘    └─────────────────┘    └─────────────────┘
                                │
                       ┌─────────────────┐
                       │ Shared Library  │
                       │ (civicmind_     │
                       │  common)        │
                       └─────────────────┘
```

### 🚀 Key Components

- **🧠 AI Agent Core**: Natural language processing and decision making
- **🔌 MCP Server**: Standardized protocol interface for AI assistants
- **🛠️ Tool Integration**: Direct access to civic service APIs
- **📊 Resource Management**: Domain-specific data and knowledge bases
- **🔒 Security Layer**: Authentication, authorization, and data protection

---

## 🛠️ Creating a New Agent

### Step 1: Set Up Agent Structure

```bash
# Create new agent directory
mkdir -p civicmind/agents/your_domain_agent
cd civicmind/agents/your_domain_agent

# Create core files
touch __init__.py
touch agent.py
touch mcp_server.py
touch tools.py
touch resources.py
```

### Step 2: Define the Agent Class

```python
# civicmind/agents/your_domain_agent/agent.py
from typing import Dict, List, Any, Optional
from civicmind_common.base import BaseAgent, AgentResponse
from civicmind_common.tools import BaseTool
from civicmind_common.auth import require_auth
import asyncio

class YourDomainAgent(BaseAgent):
    """
    AI agent for handling [Your Domain] civic services.
    
    Specializes in:
    - Domain-specific issue analysis
    - Service recommendations  
    - Process guidance
    - Resource coordination
    """
    
    def __init__(self, api_client, tools: Optional[List[BaseTool]] = None):
        super().__init__(
            domain="your_domain",
            api_client=api_client,
            tools=tools or []
        )
        self.service_url = f"http://your-domain-service:800X"
    
    def get_system_prompt(self) -> str:
        """Define agent's specialized knowledge and behavior"""
        return """
        You are a specialized AI assistant for [Your Domain] civic services.
        
        **Your Expertise:**
        - [Domain-specific regulations and processes]
        - [Common citizen questions and solutions]
        - [Integration with other city services]
        
        **Your Approach:**
        - Always prioritize citizen needs and community benefit
        - Provide clear, actionable guidance
        - Connect citizens with appropriate resources
        - Escalate complex issues to human specialists
        
        **Communication Style:**
        - Professional yet approachable
        - Use clear, jargon-free language
        - Provide step-by-step instructions
        - Include relevant deadlines and costs
        """
    
    async def analyze_issue(self, query: str, context: Dict[str, Any]) -> AgentResponse:
        """
        Analyze citizen issues and provide intelligent responses
        
        Args:
            query: Citizen's question or description
            context: Additional context (location, user info, etc.)
            
        Returns:
            AgentResponse with analysis and recommendations
        """
        try:
            # Step 1: Classify the issue type
            issue_type = await self._classify_issue(query, context)
            
            # Step 2: Gather relevant resources
            resources = await self._gather_resources(issue_type, context)
            
            # Step 3: Execute appropriate tools
            tool_results = await self._execute_tools(issue_type, query, context)
            
            # Step 4: Generate comprehensive response
            response = await self._generate_response(
                query, issue_type, resources, tool_results
            )
            
            return AgentResponse(
                success=True,
                response=response,
                issue_type=issue_type,
                confidence=0.95,
                next_steps=self._generate_next_steps(issue_type, tool_results),
                estimated_resolution_time=self._estimate_resolution_time(issue_type),
                required_documents=self._get_required_documents(issue_type),
                related_services=self._get_related_services(issue_type)
            )
            
        except Exception as e:
            return AgentResponse(
                success=False,
                error=f"Analysis failed: {str(e)}",
                fallback_response="I apologize, but I'm having trouble analyzing your request. Please contact our office directly for assistance."
            )
    
    async def _classify_issue(self, query: str, context: Dict[str, Any]) -> str:
        """Classify the type of civic issue"""
        classification_prompt = f"""
        Classify this civic issue into one of these categories:
        - application_new
        - status_check
        - requirement_inquiry
        - complaint_filing
        - payment_processing
        - general_information
        
        Query: {query}
        Context: {context.get('location', 'Not specified')}
        
        Return only the category name.
        """
        
        result = await self.llm.agenerate([classification_prompt])
        return result.generations[0][0].text.strip().lower()
    
    async def _gather_resources(self, issue_type: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Gather relevant domain resources"""
        resources = {}
        
        # Get regulations and ordinances
        if hasattr(self, 'regulations_tool'):
            resources['regulations'] = await self.regulations_tool.get_relevant_rules(issue_type)
        
        # Get location-specific information
        if context.get('location'):
            resources['location_info'] = await self._get_location_info(context['location'])
        
        # Get fee schedules
        resources['fees'] = await self._get_fee_information(issue_type)
        
        return resources
    
    async def _execute_tools(self, issue_type: str, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute appropriate tools based on issue type"""
        results = {}
        
        for tool in self.tools:
            if tool.is_applicable(issue_type, query, context):
                try:
                    tool_result = await tool.execute(query, context)
                    results[tool.name] = tool_result
                except Exception as e:
                    results[tool.name] = {"error": str(e)}
        
        return results
    
    async def _generate_response(self, query: str, issue_type: str, 
                               resources: Dict[str, Any], 
                               tool_results: Dict[str, Any]) -> str:
        """Generate comprehensive response using LLM"""
        
        response_prompt = f"""
        Based on the analysis, provide a helpful response to this citizen query:
        
        **Query:** {query}
        **Issue Type:** {issue_type}
        **Available Resources:** {resources}
        **Tool Results:** {tool_results}
        
        Provide a comprehensive, helpful response that:
        1. Directly addresses the citizen's question
        2. Provides specific next steps
        3. Includes relevant costs and timelines
        4. References applicable regulations
        5. Offers alternative solutions if appropriate
        
        Be conversational but professional.
        """
        
        result = await self.llm.agenerate([response_prompt])
        return result.generations[0][0].text
    
    def _generate_next_steps(self, issue_type: str, tool_results: Dict[str, Any]) -> List[str]:
        """Generate specific next steps for the citizen"""
        steps = []
        
        if issue_type == "application_new":
            steps.extend([
                "Review required documents list",
                "Prepare application materials",
                "Submit application online or in-person",
                "Pay applicable fees"
            ])
        elif issue_type == "status_check":
            steps.extend([
                "Note your application/case number",
                "Check online portal for updates",
                "Contact office if no updates in expected timeframe"
            ])
        
        # Add tool-specific steps
        for tool_name, result in tool_results.items():
            if result.get("next_steps"):
                steps.extend(result["next_steps"])
        
        return steps
    
    def _estimate_resolution_time(self, issue_type: str) -> str:
        """Estimate resolution timeframe"""
        timeframes = {
            "application_new": "2-4 weeks",
            "status_check": "Immediate",
            "requirement_inquiry": "Immediate",
            "complaint_filing": "1-2 weeks",
            "payment_processing": "2-3 business days",
            "general_information": "Immediate"
        }
        return timeframes.get(issue_type, "1-2 weeks")
```

### Step 3: Create MCP Server Interface

```python
# civicmind/agents/your_domain_agent/mcp_server.py
import asyncio
import json
from typing import Dict, List, Any, Optional
from mcp import McpServer, Resource, Tool
from mcp.types import TextContent, ImageContent
from .agent import YourDomainAgent
from .tools import YourDomainTools
from .resources import YourDomainResources

class YourDomainMCPServer:
    """
    MCP server implementation for Your Domain civic services.
    
    Provides standardized interface for AI assistants to interact
    with domain-specific tools and resources.
    """
    
    def __init__(self, agent: YourDomainAgent):
        self.agent = agent
        self.server = McpServer("your-domain-civic-agent")
        self.tools = YourDomainTools(agent.api_client)
        self.resources = YourDomainResources(agent.api_client)
        
        # Register MCP handlers
        self._register_resources()
        self._register_tools()
        self._register_prompts()
    
    def _register_resources(self):
        """Register domain-specific resources"""
        
        @self.server.list_resources()
        async def list_resources() -> List[Resource]:
            """List available domain resources"""
            return [
                Resource(
                    uri="your-domain://regulations",
                    name="Domain Regulations",
                    description="Complete regulations and ordinances for your domain",
                    mimeType="application/json"
                ),
                Resource(
                    uri="your-domain://processes", 
                    name="Service Processes",
                    description="Step-by-step guides for common processes",
                    mimeType="application/json"
                ),
                Resource(
                    uri="your-domain://fees",
                    name="Fee Schedule",
                    description="Current fees and payment information",
                    mimeType="application/json"
                ),
                Resource(
                    uri="your-domain://contacts",
                    name="Department Contacts",
                    description="Contact information for specialists",
                    mimeType="application/json"
                )
            ]
        
        @self.server.read_resource()
        async def read_resource(uri: str) -> str:
            """Read specific resource content"""
            try:
                resource_type = uri.split("://")[1]
                
                if resource_type == "regulations":
                    data = await self.resources.get_regulations()
                elif resource_type == "processes":
                    data = await self.resources.get_processes()
                elif resource_type == "fees":
                    data = await self.resources.get_fees()
                elif resource_type == "contacts":
                    data = await self.resources.get_contacts()
                else:
                    raise ValueError(f"Unknown resource: {resource_type}")
                
                return json.dumps(data, indent=2)
                
            except Exception as e:
                return json.dumps({"error": str(e)})
    
    def _register_tools(self):
        """Register domain-specific tools"""
        
        @self.server.list_tools()
        async def list_tools() -> List[Tool]:
            """List available domain tools"""
            return [
                Tool(
                    name="analyze_issue",
                    description="Analyze a citizen's issue and provide recommendations",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "query": {
                                "type": "string",
                                "description": "Citizen's question or issue description"
                            },
                            "location": {
                                "type": "string", 
                                "description": "Location context (address, district, etc.)"
                            },
                            "priority": {
                                "type": "string",
                                "enum": ["low", "medium", "high", "urgent"],
                                "description": "Issue priority level"
                            }
                        },
                        "required": ["query"]
                    }
                ),
                Tool(
                    name="check_requirements",
                    description="Get requirements for a specific process or application",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "process_type": {
                                "type": "string",
                                "description": "Type of process or application"
                            },
                            "location": {
                                "type": "string",
                                "description": "Property or business location"
                            }
                        },
                        "required": ["process_type"]
                    }
                ),
                Tool(
                    name="submit_application",
                    description="Submit a new application or request",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "application_type": {
                                "type": "string",
                                "description": "Type of application"
                            },
                            "applicant_info": {
                                "type": "object",
                                "description": "Applicant contact information"
                            },
                            "details": {
                                "type": "object",
                                "description": "Application-specific details"
                            }
                        },
                        "required": ["application_type", "applicant_info"]
                    }
                ),
                Tool(
                    name="check_status",
                    description="Check status of existing application or case",
                    inputSchema={
                        "type": "object",
                        "properties": {
                            "reference_number": {
                                "type": "string",
                                "description": "Application or case reference number"
                            },
                            "applicant_info": {
                                "type": "object",
                                "description": "Applicant identification for verification"
                            }
                        },
                        "required": ["reference_number"]
                    }
                )
            ]
        
        @self.server.call_tool()
        async def call_tool(name: str, arguments: Dict[str, Any]) -> List[TextContent]:
            """Execute specific tool"""
            try:
                if name == "analyze_issue":
                    response = await self.agent.analyze_issue(
                        query=arguments["query"],
                        context={
                            "location": arguments.get("location"),
                            "priority": arguments.get("priority", "medium")
                        }
                    )
                    
                    if response.success:
                        content = self._format_analysis_response(response)
                    else:
                        content = f"❌ **Analysis Failed**\n\n{response.error}\n\n{response.fallback_response}"
                
                elif name == "check_requirements":
                    result = await self.tools.check_requirements(
                        process_type=arguments["process_type"],
                        location=arguments.get("location")
                    )
                    content = self._format_requirements_response(result)
                
                elif name == "submit_application":
                    result = await self.tools.submit_application(
                        application_type=arguments["application_type"],
                        applicant_info=arguments["applicant_info"],
                        details=arguments["details"]
                    )
                    content = self._format_submission_response(result)
                
                elif name == "check_status":
                    result = await self.tools.check_status(
                        reference_number=arguments["reference_number"],
                        applicant_info=arguments.get("applicant_info", {})
                    )
                    content = self._format_status_response(result)
                
                else:
                    content = f"❌ Unknown tool: {name}"
                
                return [TextContent(type="text", text=content)]
                
            except Exception as e:
                error_content = f"❌ **Tool Error**\n\nTool '{name}' failed: {str(e)}\n\nPlease try again or contact support if the issue persists."
                return [TextContent(type="text", text=error_content)]
    
    def _register_prompts(self):
        """Register domain-specific prompts"""
        
        @self.server.list_prompts()
        async def list_prompts():
            return [
                {
                    "name": "citizen_assistance",
                    "description": "Help citizens with domain-specific questions"
                },
                {
                    "name": "process_guidance", 
                    "description": "Provide step-by-step process guidance"
                }
            ]
    
    def _format_analysis_response(self, response: Any) -> str:
        """Format agent analysis response for MCP"""
        formatted = f"""
🔍 **Issue Analysis**

**Issue Type:** {response.issue_type.replace('_', ' ').title()}
**Confidence:** {int(response.confidence * 100)}%

{response.response}

📋 **Next Steps:**
"""
        for i, step in enumerate(response.next_steps, 1):
            formatted += f"{i}. {step}\n"
        
        if response.estimated_resolution_time:
            formatted += f"\n⏱️ **Estimated Time:** {response.estimated_resolution_time}"
        
        if response.required_documents:
            formatted += f"\n📄 **Required Documents:**\n"
            for doc in response.required_documents:
                formatted += f"• {doc}\n"
        
        if response.related_services:
            formatted += f"\n🔗 **Related Services:**\n"
            for service in response.related_services:
                formatted += f"• {service}\n"
        
        return formatted
    
    def _format_requirements_response(self, result: Dict[str, Any]) -> str:
        """Format requirements response"""
        formatted = f"""
📋 **Requirements for {result.get('process_type', 'Process').title()}**

"""
        if result.get('description'):
            formatted += f"{result['description']}\n\n"
        
        if result.get('documents'):
            formatted += "**Required Documents:**\n"
            for doc in result['documents']:
                formatted += f"• {doc}\n"
            formatted += "\n"
        
        if result.get('fees'):
            formatted += f"**Fees:** ${result['fees']}\n\n"
        
        if result.get('timeline'):
            formatted += f"**Processing Time:** {result['timeline']}\n\n"
        
        if result.get('steps'):
            formatted += "**Process Steps:**\n"
            for i, step in enumerate(result['steps'], 1):
                formatted += f"{i}. {step}\n"
        
        return formatted
    
    def _format_submission_response(self, result: Dict[str, Any]) -> str:
        """Format application submission response"""
        if result.get('success'):
            return f"""
✅ **Application Submitted Successfully**

**Reference Number:** {result.get('reference_number')}
**Status:** {result.get('status', 'Submitted')}
**Estimated Processing Time:** {result.get('processing_time', 'Unknown')}

📧 **Confirmation sent to:** {result.get('contact_email')}

**Next Steps:**
• Save your reference number for tracking
• Check status online or by phone
• Respond promptly to any requests for additional information
"""
        else:
            return f"""
❌ **Application Submission Failed**

**Error:** {result.get('error', 'Unknown error occurred')}

**What to do next:**
• Review the error message above
• Correct any issues and try again
• Contact our office if you need assistance

**Contact Information:**
• Phone: {result.get('contact_phone', '(555) 123-4567')}
• Email: {result.get('contact_email', 'help@city.ai')}
"""
    
    def _format_status_response(self, result: Dict[str, Any]) -> str:
        """Format status check response"""
        if result.get('found'):
            status_emoji = {
                'submitted': '📝',
                'under_review': '🔍', 
                'approved': '✅',
                'rejected': '❌',
                'pending': '⏳'
            }.get(result.get('status', '').lower(), '📋')
            
            formatted = f"""
{status_emoji} **Application Status**

**Reference Number:** {result.get('reference_number')}
**Status:** {result.get('status', 'Unknown').title()}
**Last Updated:** {result.get('last_updated', 'Unknown')}

"""
            if result.get('progress'):
                formatted += f"**Progress:** {result['progress']}% complete\n\n"
            
            if result.get('current_step'):
                formatted += f"**Current Step:** {result['current_step']}\n\n"
            
            if result.get('next_actions'):
                formatted += "**Next Actions Required:**\n"
                for action in result['next_actions']:
                    formatted += f"• {action}\n"
                formatted += "\n"
            
            if result.get('comments'):
                formatted += f"**Comments:** {result['comments']}\n\n"
            
            if result.get('estimated_completion'):
                formatted += f"**Estimated Completion:** {result['estimated_completion']}\n"
            
            return formatted
        
        else:
            return f"""
❌ **Application Not Found**

We couldn't find an application with reference number: {result.get('reference_number')}

**Possible reasons:**
• Reference number was entered incorrectly
• Application is too old and archived
• Application was submitted to a different department

**What to do:**
• Double-check the reference number
• Contact our office for assistance
• Try searching with different information

**Contact Information:**
• Phone: (555) 123-4567
• Email: help@city.ai
"""
    
    async def run(self, host: str = "0.0.0.0", port: int = 9300):
        """Start the MCP server"""
        await self.server.run(host=host, port=port)

# Server startup
async def main():
    # Initialize dependencies
    from civicmind_common.api_client import CivicAPIClient
    from civicmind_common.llm import get_llm
    
    api_client = CivicAPIClient(base_url="http://api-gateway:8300")
    llm = get_llm()
    
    # Create agent and server
    agent = YourDomainAgent(api_client=api_client)
    mcp_server = YourDomainMCPServer(agent)
    
    # Start server
    print("🚀 Starting Your Domain MCP Server...")
    await mcp_server.run(port=9300)

if __name__ == "__main__":
    asyncio.run(main())
```

### Step 4: Implement Domain Tools

```python
# civicmind/agents/your_domain_agent/tools.py
from typing import Dict, List, Any, Optional
from civicmind_common.tools import BaseTool
from civicmind_common.api_client import CivicAPIClient

class YourDomainTools:
    """Collection of tools for your domain civic services"""
    
    def __init__(self, api_client: CivicAPIClient):
        self.api_client = api_client
        self.service_url = "http://your-domain-service:800X"
    
    async def check_requirements(self, process_type: str, location: Optional[str] = None) -> Dict[str, Any]:
        """Get requirements for a specific process"""
        try:
            response = await self.api_client.post(
                f"{self.service_url}/api/v1/requirements",
                json={
                    "process_type": process_type,
                    "location": location
                }
            )
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def submit_application(self, application_type: str, 
                               applicant_info: Dict[str, Any],
                               details: Dict[str, Any]) -> Dict[str, Any]:
        """Submit a new application"""
        try:
            response = await self.api_client.post(
                f"{self.service_url}/api/v1/applications",
                json={
                    "application_type": application_type,
                    "applicant_info": applicant_info,
                    "details": details
                }
            )
            return response.json()
        except Exception as e:
            return {"success": False, "error": str(e)}
    
    async def check_status(self, reference_number: str, 
                          applicant_info: Dict[str, Any]) -> Dict[str, Any]:
        """Check application status"""
        try:
            response = await self.api_client.get(
                f"{self.service_url}/api/v1/applications/{reference_number}/status",
                params=applicant_info
            )
            return response.json()
        except Exception as e:
            return {"found": False, "error": str(e)}

# Additional specialized tools
class RequirementsAnalysisTool(BaseTool):
    """Tool for analyzing and explaining requirements"""
    
    name = "requirements_analysis"
    description = "Analyze requirements for complex processes"
    
    def __init__(self, api_client: CivicAPIClient):
        self.api_client = api_client
    
    def is_applicable(self, issue_type: str, query: str, context: Dict[str, Any]) -> bool:
        """Check if this tool should be used"""
        keywords = ["requirements", "needed", "documents", "application"]
        return any(keyword in query.lower() for keyword in keywords)
    
    async def execute(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Execute requirements analysis"""
        # Implementation specific to your domain
        pass

class FeeCalculatorTool(BaseTool):
    """Tool for calculating fees and costs"""
    
    name = "fee_calculator"
    description = "Calculate applicable fees for services"
    
    async def execute(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """Calculate fees based on application details"""
        # Implementation specific to your domain
        pass
```

### Step 5: Define Domain Resources

```python
# civicmind/agents/your_domain_agent/resources.py
from typing import Dict, List, Any
from civicmind_common.api_client import CivicAPIClient

class YourDomainResources:
    """Manage domain-specific resources and data"""
    
    def __init__(self, api_client: CivicAPIClient):
        self.api_client = api_client
        self.service_url = "http://your-domain-service:800X"
    
    async def get_regulations(self) -> Dict[str, Any]:
        """Get current regulations and ordinances"""
        try:
            response = await self.api_client.get(f"{self.service_url}/api/v1/regulations")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def get_processes(self) -> Dict[str, Any]:
        """Get process guides and workflows"""
        try:
            response = await self.api_client.get(f"{self.service_url}/api/v1/processes")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def get_fees(self) -> Dict[str, Any]:
        """Get current fee schedule"""
        try:
            response = await self.api_client.get(f"{self.service_url}/api/v1/fees")
            return response.json()
        except Exception as e:
            return {"error": str(e)}
    
    async def get_contacts(self) -> Dict[str, Any]:
        """Get department contact information"""
        return {
            "general_info": {
                "phone": "(555) 123-4567",
                "email": "your-domain@city.ai",
                "hours": "Monday-Friday 8:00 AM - 5:00 PM"
            },
            "specialists": [
                {
                    "name": "Jane Smith",
                    "role": "Senior Specialist",
                    "phone": "(555) 123-4568",
                    "email": "jane.smith@city.ai",
                    "specialties": ["Complex applications", "Appeals"]
                }
            ],
            "emergency": {
                "phone": "(555) 911",
                "description": "For urgent issues outside business hours"
            }
        }
```

---

## 🧪 Testing Your Agent

### Unit Testing

```python
# tests/test_your_domain_agent.py
import pytest
import asyncio
from unittest.mock import AsyncMock, MagicMock
from civicmind.agents.your_domain_agent.agent import YourDomainAgent

class TestYourDomainAgent:
    
    @pytest.fixture
    def mock_api_client(self):
        client = MagicMock()
        client.post = AsyncMock()
        client.get = AsyncMock()
        return client
    
    @pytest.fixture
    def agent(self, mock_api_client):
        return YourDomainAgent(api_client=mock_api_client)
    
    @pytest.mark.asyncio
    async def test_analyze_issue_success(self, agent):
        """Test successful issue analysis"""
        query = "I need information about application requirements"
        context = {"location": "Downtown District"}
        
        response = await agent.analyze_issue(query, context)
        
        assert response.success is True
        assert response.issue_type is not None
        assert response.response is not None
        assert len(response.next_steps) > 0
    
    @pytest.mark.asyncio
    async def test_classify_issue(self, agent):
        """Test issue classification"""
        query = "How do I apply for a new permit?"
        context = {}
        
        issue_type = await agent._classify_issue(query, context)
        
        assert issue_type in ['application_new', 'requirement_inquiry']
    
    @pytest.mark.asyncio
    async def test_error_handling(self, agent):
        """Test error handling"""
        # Mock API client to raise exception
        agent.api_client.get.side_effect = Exception("API Error")
        
        response = await agent.analyze_issue("test query", {})
        
        assert response.success is False
        assert response.error is not None
        assert response.fallback_response is not None

# Integration testing
@pytest.mark.integration
class TestYourDomainIntegration:
    
    @pytest.mark.asyncio
    async def test_end_to_end_workflow(self):
        """Test complete workflow from query to response"""
        # This would test against a running instance
        pass
    
    @pytest.mark.asyncio 
    async def test_mcp_server_integration(self):
        """Test MCP server functionality"""
        # Test MCP protocol compliance
        pass
```

### Load Testing

```python
# tests/load_test_your_domain.py
import asyncio
import time
import statistics
from civicmind.agents.your_domain_agent.mcp_server import YourDomainMCPServer

async def load_test_agent(concurrent_requests=50, total_requests=1000):
    """Load test the agent with concurrent requests"""
    
    async def make_request():
        # Simulate client request
        start_time = time.time()
        try:
            # Make actual request to agent
            result = await agent.analyze_issue("test query", {})
            return {"success": True, "time": time.time() - start_time}
        except Exception as e:
            return {"success": False, "error": str(e), "time": time.time() - start_time}
    
    # Run load test
    tasks = [make_request() for _ in range(total_requests)]
    results = await asyncio.gather(*tasks)
    
    # Analyze results
    successful = [r for r in results if r["success"]]
    failed = [r for r in results if not r["success"]]
    response_times = [r["time"] for r in successful]
    
    print(f"Load Test Results:")
    print(f"  Total Requests: {total_requests}")
    print(f"  Successful: {len(successful)} ({len(successful)/total_requests*100:.1f}%)")
    print(f"  Failed: {len(failed)} ({len(failed)/total_requests*100:.1f}%)")
    print(f"  Average Response Time: {statistics.mean(response_times):.3f}s")
    print(f"  95th Percentile: {statistics.quantiles(response_times, n=20)[18]:.3f}s")

if __name__ == "__main__":
    asyncio.run(load_test_agent())
```

---

## 🚀 Advanced Agent Techniques

### Multi-Agent Coordination

```python
# civicmind/agents/coordination/multi_agent_orchestrator.py
from typing import Dict, List, Any
from civicmind.agents.base_agent import BaseAgent

class MultiAgentOrchestrator:
    """Coordinate multiple agents for complex cross-domain issues"""
    
    def __init__(self, agents: Dict[str, BaseAgent]):
        self.agents = agents
    
    async def orchestrate_complex_issue(self, query: str, context: Dict[str, Any]) -> Dict[str, Any]:
        """
        Handle issues that require multiple domain expertise
        
        Example: Opening a restaurant requires permits, parking, safety, zoning
        """
        
        # Step 1: Identify required domains
        required_domains = await self._identify_domains(query, context)
        
        # Step 2: Parallel analysis by relevant agents
        analyses = await asyncio.gather(*[
            self.agents[domain].analyze_issue(query, context)
            for domain in required_domains
        ])
        
        # Step 3: Synthesize responses
        orchestrated_response = await self._synthesize_responses(
            query, required_domains, analyses
        )
        
        return orchestrated_response
    
    async def _identify_domains(self, query: str, context: Dict[str, Any]) -> List[str]:
        """Identify which domains need to be involved"""
        # Use classification model or keywords to determine domains
        domain_keywords = {
            "permits": ["permit", "license", "application", "building"],
            "parking": ["parking", "vehicle", "citation"],
            "safety": ["safety", "emergency", "fire", "police"],
            "zoning": ["zoning", "land use", "development"]
        }
        
        identified = []
        query_lower = query.lower()
        
        for domain, keywords in domain_keywords.items():
            if any(keyword in query_lower for keyword in keywords):
                identified.append(domain)
        
        return identified if identified else ["general"]
    
    async def _synthesize_responses(self, query: str, domains: List[str], 
                                  analyses: List[Any]) -> Dict[str, Any]:
        """Combine multiple agent responses into coherent guidance"""
        
        # Combine all next steps
        all_steps = []
        for analysis in analyses:
            if analysis.success:
                all_steps.extend(analysis.next_steps)
        
        # Identify dependencies between steps
        prioritized_steps = self._prioritize_steps(all_steps, domains)
        
        # Generate coordinated timeline
        timeline = self._generate_timeline(analyses, domains)
        
        return {
            "coordinated_response": self._format_coordinated_response(analyses),
            "prioritized_steps": prioritized_steps,
            "timeline": timeline,
            "total_estimated_cost": sum(a.estimated_cost for a in analyses if hasattr(a, 'estimated_cost')),
            "coordination_complexity": "high" if len(domains) > 2 else "medium"
        }
```

### Agent Learning and Improvement

```python
# civicmind/agents/learning/feedback_system.py
class AgentFeedbackSystem:
    """System for collecting feedback and improving agent responses"""
    
    def __init__(self, agent: BaseAgent):
        self.agent = agent
        self.feedback_db = self._connect_feedback_db()
    
    async def collect_feedback(self, query: str, response: Any, 
                             user_feedback: Dict[str, Any]):
        """Collect user feedback on agent responses"""
        feedback_record = {
            "query": query,
            "response": response.dict(),
            "user_rating": user_feedback.get("rating"),
            "user_comments": user_feedback.get("comments"),
            "resolution_success": user_feedback.get("resolved"),
            "timestamp": time.time()
        }
        
        await self.feedback_db.insert(feedback_record)
        
        # Trigger improvement analysis if rating is low
        if user_feedback.get("rating", 5) < 3:
            await self._analyze_poor_response(feedback_record)
    
    async def _analyze_poor_response(self, feedback: Dict[str, Any]):
        """Analyze poorly rated responses for improvement opportunities"""
        
        # Identify patterns in poor responses
        similar_queries = await self.feedback_db.find_similar_queries(
            feedback["query"], min_similarity=0.7
        )
        
        poor_responses = [q for q in similar_queries if q["user_rating"] < 3]
        
        if len(poor_responses) >= 5:  # Pattern detected
            improvement_suggestion = await self._generate_improvement_suggestion(
                poor_responses
            )
            
            # Log for human review
            await self._log_improvement_opportunity(improvement_suggestion)
    
    async def get_performance_metrics(self) -> Dict[str, Any]:
        """Get agent performance analytics"""
        recent_feedback = await self.feedback_db.get_recent_feedback(days=30)
        
        return {
            "total_interactions": len(recent_feedback),
            "average_rating": statistics.mean([f["user_rating"] for f in recent_feedback]),
            "resolution_rate": len([f for f in recent_feedback if f["resolution_success"]]) / len(recent_feedback),
            "top_issues": self._identify_top_issues(recent_feedback),
            "improvement_areas": self._identify_improvement_areas(recent_feedback)
        }
```

### Custom LLM Integration

```python
# civicmind/agents/llm/custom_llm.py
from langchain.llms.base import LLM
from typing import Optional, List, Dict, Any

class CivicMindLLM(LLM):
    """Custom LLM wrapper optimized for civic domain"""
    
    def __init__(self, model_name: str = "gpt-4", **kwargs):
        super().__init__(**kwargs)
        self.model_name = model_name
        self.civic_context = self._load_civic_context()
    
    def _load_civic_context(self) -> str:
        """Load civic-specific context and knowledge"""
        return """
        You are an AI assistant specialized in civic services and government processes.
        
        Key Principles:
        - Prioritize citizen welfare and community benefit
        - Provide accurate, actionable information
        - Maintain professional yet approachable tone
        - Respect privacy and confidentiality
        - Escalate complex legal matters to human experts
        
        Domain Knowledge:
        - Municipal codes and regulations
        - Government processes and procedures
        - Community resources and services
        - Accessibility requirements
        - Cultural sensitivity guidelines
        """
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None) -> str:
        """Execute LLM call with civic context"""
        enhanced_prompt = f"{self.civic_context}\n\nCitizen Query: {prompt}"
        
        # Add any domain-specific prompt engineering
        enhanced_prompt = self._add_civic_instructions(enhanced_prompt)
        
        # Call underlying LLM
        return self._call_base_llm(enhanced_prompt, stop)
    
    def _add_civic_instructions(self, prompt: str) -> str:
        """Add civic-specific instructions to prompt"""
        instructions = """
        
        Response Guidelines:
        1. Start with empathy and acknowledgment
        2. Provide clear, step-by-step guidance
        3. Include relevant costs and timelines
        4. Mention required documents
        5. Offer alternative solutions when appropriate
        6. Include contact information for follow-up
        7. Use inclusive, accessible language
        
        Format your response to be helpful and actionable.
        """
        
        return prompt + instructions
    
    @property
    def _llm_type(self) -> str:
        return "civic_mind_llm"
```

---

## 🌍 Cultural Sensitivity and Accessibility

### Multilingual Support

```python
# civicmind/agents/i18n/multilingual_agent.py
from typing import Dict, Any, Optional
from civicmind.agents.base_agent import BaseAgent
import translators as ts

class MultilingualAgent(BaseAgent):
    """Agent wrapper with multilingual support"""
    
    def __init__(self, base_agent: BaseAgent, supported_languages: List[str] = None):
        self.base_agent = base_agent
        self.supported_languages = supported_languages or ['en', 'es', 'zh', 'fr', 'ar']
        self.default_language = 'en'
    
    async def analyze_issue(self, query: str, context: Dict[str, Any]) -> Any:
        """Analyze issue with automatic language detection and translation"""
        
        # Detect language
        detected_language = self._detect_language(query)
        
        # Translate to English if needed
        if detected_language != 'en':
            translated_query = await self._translate_text(query, detected_language, 'en')
            translated_context = await self._translate_context(context, detected_language, 'en')
        else:
            translated_query = query
            translated_context = context
        
        # Get response from base agent
        response = await self.base_agent.analyze_issue(translated_query, translated_context)
        
        # Translate response back if needed
        if detected_language != 'en' and response.success:
            response.response = await self._translate_text(
                response.response, 'en', detected_language
            )
            response.next_steps = await self._translate_list(
                response.next_steps, 'en', detected_language
            )
        
        return response
    
    def _detect_language(self, text: str) -> str:
        """Detect the language of input text"""
        # Implementation using language detection library
        from langdetect import detect
        try:
            detected = detect(text)
            return detected if detected in self.supported_languages else 'en'
        except:
            return 'en'
    
    async def _translate_text(self, text: str, from_lang: str, to_lang: str) -> str:
        """Translate text between languages"""
        if from_lang == to_lang:
            return text
        
        try:
            return ts.translate_text(text, from_language=from_lang, to_language=to_lang)
        except Exception as e:
            # Log translation error and return original text
            print(f"Translation error: {e}")
            return text
```

### Accessibility Features

```python
# civicmind/agents/accessibility/accessible_agent.py
class AccessibleAgent(BaseAgent):
    """Agent wrapper with accessibility enhancements"""
    
    def __init__(self, base_agent: BaseAgent):
        self.base_agent = base_agent
    
    async def analyze_issue(self, query: str, context: Dict[str, Any]) -> Any:
        """Enhance response with accessibility features"""
        
        response = await self.base_agent.analyze_issue(query, context)
        
        if response.success:
            # Add accessibility enhancements
            response.response = self._enhance_for_accessibility(response.response)
            response.audio_description = await self._generate_audio_description(response)
            response.simplified_language = await self._simplify_language(response.response)
            response.large_print_formatting = self._format_for_large_print(response.response)
        
        return response
    
    def _enhance_for_accessibility(self, text: str) -> str:
        """Enhance text for accessibility"""
        
        # Add clear structure
        enhanced = "🔍 **SUMMARY**\n"
        enhanced += self._extract_summary(text) + "\n\n"
        
        # Add clear sections
        enhanced += "📋 **DETAILED INFORMATION**\n"
        enhanced += text + "\n\n"
        
        # Add navigation aids
        enhanced += "🎯 **QUICK ACTIONS**\n"
        enhanced += "• Call main number for immediate help: (555) 123-4567\n"
        enhanced += "• Text HELP to 12345 for text-based assistance\n"
        enhanced += "• Visit office at [Address] for in-person help\n"
        
        return enhanced
    
    async def _generate_audio_description(self, response: Any) -> str:
        """Generate audio-optimized description"""
        
        audio_text = f"""
        This is a response from the {self.base_agent.domain} department.
        
        Issue type: {response.issue_type.replace('_', ' ')}
        
        Main response: {response.response}
        
        You have {len(response.next_steps)} action items to complete.
        
        For detailed steps, please ask for the step-by-step guide.
        """
        
        return audio_text
    
    async def _simplify_language(self, text: str) -> str:
        """Simplify language for easier comprehension"""
        
        # Use plain language principles
        simplification_prompt = f"""
        Rewrite this text using simple, clear language:
        - Use common words instead of jargon
        - Use shorter sentences
        - Use active voice
        - Explain any necessary technical terms
        - Maintain all important information
        
        Original text: {text}
        """
        
        simplified = await self.llm.agenerate([simplification_prompt])
        return simplified.generations[0][0].text
```

---

## 📚 Advanced Integration Patterns

### External API Integration

```python
# civicmind/agents/integrations/external_apis.py
class ExternalAPIIntegration:
    """Integration with external government and civic APIs"""
    
    def __init__(self, api_keys: Dict[str, str]):
        self.api_keys = api_keys
        self.clients = self._initialize_clients()
    
    def _initialize_clients(self):
        """Initialize external API clients"""
        return {
            "usps": USPSClient(self.api_keys.get("usps")),
            "census": CensusClient(self.api_keys.get("census")),
            "weather": WeatherClient(self.api_keys.get("weather")),
            "transit": TransitClient(self.api_keys.get("transit"))
        }
    
    async def validate_address(self, address: str) -> Dict[str, Any]:
        """Validate address using USPS API"""
        return await self.clients["usps"].validate_address(address)
    
    async def get_demographic_data(self, location: str) -> Dict[str, Any]:
        """Get demographic data for better service targeting"""
        return await self.clients["census"].get_demographics(location)
    
    async def check_weather_impact(self, service_type: str, date: str) -> Dict[str, Any]:
        """Check if weather might impact service delivery"""
        weather = await self.clients["weather"].get_forecast(date)
        
        weather_impacts = {
            "outdoor_inspection": weather.get("precipitation", 0) > 0.1,
            "construction": weather.get("wind_speed", 0) > 25,
            "public_event": weather.get("temperature", 70) < 32
        }
        
        return {
            "weather": weather,
            "impact": weather_impacts.get(service_type, False),
            "recommendation": self._get_weather_recommendation(service_type, weather)
        }

# Usage in agent
class WeatherAwareAgent(BaseAgent):
    """Agent that considers weather in recommendations"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.external_apis = ExternalAPIIntegration(api_keys={
            "weather": os.getenv("WEATHER_API_KEY")
        })
    
    async def analyze_issue(self, query: str, context: Dict[str, Any]) -> Any:
        """Enhance analysis with weather considerations"""
        
        base_response = await super().analyze_issue(query, context)
        
        # Check for weather-sensitive services
        if self._is_weather_sensitive(base_response.issue_type):
            weather_impact = await self.external_apis.check_weather_impact(
                base_response.issue_type,
                context.get("scheduled_date", "today")
            )
            
            if weather_impact["impact"]:
                base_response.weather_warning = weather_impact["recommendation"]
                base_response.response += f"\n\n⚠️ Weather Advisory: {weather_impact['recommendation']}"
        
        return base_response
```

### Real-Time Data Integration

```python
# civicmind/agents/realtime/live_data_agent.py
import asyncio
import websockets
from typing import Dict, Any

class LiveDataAgent(BaseAgent):
    """Agent with real-time data integration"""
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.live_data_feeds = {}
        self.data_cache = {}
    
    async def start_data_feeds(self):
        """Start real-time data feeds"""
        feeds = [
            self._start_traffic_feed(),
            self._start_emergency_feed(),
            self._start_service_status_feed()
        ]
        await asyncio.gather(*feeds)
    
    async def _start_traffic_feed(self):
        """Monitor traffic conditions"""
        async with websockets.connect("ws://traffic-api/live") as websocket:
            async for message in websocket:
                traffic_data = json.loads(message)
                self.data_cache["traffic"] = traffic_data
                await self._process_traffic_update(traffic_data)
    
    async def analyze_issue(self, query: str, context: Dict[str, Any]) -> Any:
        """Enhance analysis with real-time data"""
        
        base_response = await super().analyze_issue(query, context)
        
        # Add real-time context
        if context.get("location"):
            real_time_context = await self._get_real_time_context(context["location"])
            
            if real_time_context.get("traffic_delays"):
                base_response.response += f"\n\n🚦 Traffic Alert: Current delays in your area may affect service timing."
            
            if real_time_context.get("service_outages"):
                outages = real_time_context["service_outages"]
                base_response.response += f"\n\n⚠️ Service Alert: {outages} affecting your area."
        
        return base_response
    
    async def _get_real_time_context(self, location: str) -> Dict[str, Any]:
        """Get current real-time context for location"""
        context = {}
        
        # Traffic conditions
        if "traffic" in self.data_cache:
            context["traffic_delays"] = self._check_traffic_delays(location)
        
        # Service outages
        if "service_status" in self.data_cache:
            context["service_outages"] = self._check_service_outages(location)
        
        # Emergency situations
        if "emergency" in self.data_cache:
            context["emergency_alerts"] = self._check_emergency_alerts(location)
        
        return context
```

---

This comprehensive agent development guide provides everything needed to create sophisticated AI agents within CivicMind AI's microservices platform. The modular design enables rapid development while maintaining consistency and quality across all civic domains.
