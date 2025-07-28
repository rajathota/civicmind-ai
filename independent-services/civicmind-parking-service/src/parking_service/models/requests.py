"""
Parking Service Data Models
===========================

Service-specific request and response models.
"""

from typing import Optional, List, Dict, Any
from datetime import datetime
from pydantic import BaseModel, Field


class ParkingAnalysisRequest(BaseModel):
    """Request model for parking issue analysis"""
    
    description: str = Field(..., description="Description of the parking issue")
    location: Optional[str] = Field(None, description="Location of the issue")
    priority: Optional[str] = Field("medium", description="Issue priority")
    citizen_info: Optional[Dict[str, Any]] = Field(None, description="Citizen information")
    context: Optional[Dict[str, Any]] = Field(None, description="Additional context")


class ParkingClassification(BaseModel):
    """Parking issue classification"""
    
    type: str = Field(..., description="Main issue type")
    subtype: Optional[str] = Field(None, description="Issue subtype")
    confidence: float = Field(..., description="Classification confidence")
    tags: List[str] = Field(default_factory=list, description="Issue tags")


class ParkingRecommendation(BaseModel):
    """Parking issue recommendation"""
    
    step: int = Field(..., description="Step number")
    action: str = Field(..., description="Recommended action")
    description: str = Field(..., description="Action description")
    script: Optional[str] = Field(None, description="Communication script")
    timeline: Optional[str] = Field(None, description="Expected timeline")


class ParkingContact(BaseModel):
    """Contact information for parking issues"""
    
    name: str = Field(..., description="Contact name")
    phone: Optional[str] = Field(None, description="Phone number")
    email: Optional[str] = Field(None, description="Email address")
    hours: Optional[str] = Field(None, description="Operating hours")
    department: Optional[str] = Field(None, description="Department")


class ParkingAnalysisResponse(BaseModel):
    """Response model for parking issue analysis"""
    
    issue_id: str = Field(..., description="Unique issue identifier")
    classification: ParkingClassification = Field(..., description="Issue classification")
    community_first_approach: bool = Field(..., description="Community resolution priority")
    recommendations: List[str] = Field(..., description="High-level recommendations")
    step_by_step_resolution: List[ParkingRecommendation] = Field(..., description="Detailed steps")
    escalation_path: List[Dict[str, Any]] = Field(..., description="Escalation options")
    contacts: List[ParkingContact] = Field(..., description="Relevant contacts")
    documents: List[Dict[str, Any]] = Field(..., description="Relevant documents")
    cultural_considerations: Optional[Dict[str, Any]] = Field(None, description="Cultural guidance")
    estimated_resolution_time: Optional[str] = Field(None, description="Expected resolution time")
    follow_up_required: bool = Field(False, description="Whether follow-up is needed")
    created_at: datetime = Field(default_factory=datetime.now, description="Response timestamp")


class ServiceHealthResponse(BaseModel):
    """Health check response model"""
    
    service: str = Field(..., description="Service name")
    status: str = Field(..., description="Health status")
    version: str = Field(..., description="Service version")
    uptime_seconds: float = Field(..., description="Service uptime")
    checks: Dict[str, Any] = Field(default_factory=dict, description="Health checks")
    timestamp: datetime = Field(default_factory=datetime.now, description="Check timestamp")
