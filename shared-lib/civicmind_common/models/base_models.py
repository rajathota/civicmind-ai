"""
Base Models for CivicMind Services
==================================

Common data models used across all CivicMind microservices.
These models define the standard interfaces for civic issue processing.
"""

from typing import Dict, List, Optional, Any
from datetime import datetime
from pydantic import BaseModel, Field
from enum import Enum


class PriorityLevel(str, Enum):
    """Issue priority levels"""
    LOW = "low"
    MEDIUM = "medium"
    HIGH = "high"
    URGENT = "urgent"


class IssueStatus(str, Enum):
    """Issue processing status"""
    RECEIVED = "received"
    PROCESSING = "processing"
    ROUTED = "routed"
    COMPLETED = "completed"
    FAILED = "failed"


class CivicIssue(BaseModel):
    """Core civic issue model"""
    issue_id: Optional[str] = None
    description: str = Field(..., min_length=10, max_length=2000)
    location: str = Field(..., min_length=2, max_length=200)
    priority: PriorityLevel = PriorityLevel.MEDIUM
    category: Optional[str] = None
    subcategory: Optional[str] = None
    tags: List[str] = Field(default_factory=list)
    created_at: datetime = Field(default_factory=datetime.utcnow)
    citizen_info: Optional[Dict[str, Any]] = None


class CivicRequest(BaseModel):
    """Standard request model for all CivicMind services"""
    issue: CivicIssue
    context: Optional[Dict[str, Any]] = None
    tenant_id: Optional[str] = None
    user_id: Optional[str] = None
    trace_id: Optional[str] = None


class ServiceInfo(BaseModel):
    """Service information model"""
    service_name: str
    service_type: str
    port: int
    version: str
    health_status: str


class CivicResponse(BaseModel):
    """Standard response model for all CivicMind services"""
    issue_id: str
    status: IssueStatus
    service_info: ServiceInfo
    classification: Optional[Dict[str, Any]] = None
    recommendations: List[str] = Field(default_factory=list)
    next_steps: List[Dict[str, Any]] = Field(default_factory=list)
    contacts: List[Dict[str, Any]] = Field(default_factory=list)
    documents: List[Dict[str, Any]] = Field(default_factory=list)
    escalation_path: List[Dict[str, Any]] = Field(default_factory=list)
    cultural_considerations: Optional[Dict[str, Any]] = None
    community_first_approach: bool = True
    response_time_ms: Optional[float] = None
    confidence_score: Optional[float] = None
    metadata: Optional[Dict[str, Any]] = None
    created_at: datetime = Field(default_factory=datetime.utcnow)


class ErrorResponse(BaseModel):
    """Standard error response model"""
    error_code: str
    error_message: str
    details: Optional[Dict[str, Any]] = None
    service_info: ServiceInfo
    trace_id: Optional[str] = None
    timestamp: datetime = Field(default_factory=datetime.utcnow)


class HealthCheckResponse(BaseModel):
    """Health check response model"""
    service_name: str
    status: str  # "healthy", "degraded", "unhealthy"
    version: str
    uptime_seconds: float
    checks: Dict[str, Any] = Field(default_factory=dict)
    timestamp: datetime = Field(default_factory=datetime.utcnow)
