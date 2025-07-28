"""
Agent Models for CivicMind Services
===================================

Models specific to AI agent interactions and responses.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class AgentType(str, Enum):
    """Types of civic agents"""
    PARKING = "parking"
    PERMITS = "permits"
    NOISE = "noise"
    INFRASTRUCTURE = "infrastructure"
    BUSINESS = "business"
    RELIGIOUS_EVENTS = "religious_events"
    NEIGHBOR_DISPUTE = "neighbor_dispute"
    ENVIRONMENTAL = "environmental"


class ConfidenceLevel(str, Enum):
    """Agent confidence levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    VERY_HIGH = "very_high"


class AgentClassification(BaseModel):
    """Agent classification result"""
    agent_type: AgentType
    confidence: float = Field(ge=0.0, le=1.0)
    confidence_level: ConfidenceLevel
    reasoning: Optional[str] = None
    alternative_agents: List[AgentType] = Field(default_factory=list)


class AgentAnalysis(BaseModel):
    """Detailed agent analysis"""
    summary: str
    key_factors: List[str] = Field(default_factory=list)
    risk_assessment: Optional[str] = None
    urgency_level: str
    legal_considerations: List[str] = Field(default_factory=list)
    community_impact: Optional[str] = None


class AgentAction(BaseModel):
    """Recommended agent action"""
    action_type: str
    description: str
    priority: int
    estimated_time: Optional[str] = None
    required_documents: List[str] = Field(default_factory=list)
    contacts_needed: List[str] = Field(default_factory=list)


class AgentResponse(BaseModel):
    """Complete agent analysis response"""
    agent_type: AgentType
    classification: AgentClassification
    analysis: AgentAnalysis
    recommended_actions: List[AgentAction] = Field(default_factory=list)
    community_first_options: List[str] = Field(default_factory=list)
    escalation_triggers: List[str] = Field(default_factory=list)
    cultural_guidance: Optional[Dict[str, Any]] = None
    processing_time_ms: float
    agent_version: str
    model_used: Optional[str] = None
