"""
MongoDB Models for VERSATILE-DB
Converted from SQLAlchemy models to MongoDB collections
"""

import uuid
from datetime import datetime, timezone
from typing import Optional, List, Dict, Any
from pydantic import BaseModel, Field

class UserModel(BaseModel):
    """User model for MongoDB"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    email: str
    username: str
    discord_id: Optional[str] = None
    wallet_address: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ProfileModel(BaseModel):
    """Profile model for MongoDB"""
    user_id: str
    bio: Optional[str] = None
    region: Optional[str] = None
    roles: List[str] = []
    badges: List[str] = []
    grind_data: Optional[Dict[str, Any]] = None
    pentagon_data: Optional[Dict[str, Any]] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class GameModel(BaseModel):
    """Game model for MongoDB"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    game_name: str
    rank: Optional[str] = None
    winrate: Optional[float] = None
    top_roles: List[str] = []
    updated_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class HighlightModel(BaseModel):
    """Highlight model for MongoDB"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    title: str
    clip_url: str
    tags: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class GigModel(BaseModel):
    """Gig model for MongoDB"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    title: str
    description: str
    org_id: str
    budget: Optional[float] = None
    method: str = "upi"  # "upi" or "card"
    status: str = "open"  # "open" or "closed"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class ApplicationModel(BaseModel):
    """Application model for MongoDB"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    gig_id: str
    user_id: str
    resume_link: Optional[str] = None
    message: Optional[str] = None
    status: str = "pending"  # "pending", "accepted", "rejected"
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class EndorsementModel(BaseModel):
    """Endorsement model for MongoDB"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    endorsed_id: str
    endorsed_by: str
    rating: int = Field(..., ge=1, le=5)
    comment: Optional[str] = None
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SoulboundNFTModel(BaseModel):
    """Soulbound NFT model for MongoDB"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    user_id: str
    name: str
    reputation: str
    minted_at: str
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class TeamModel(BaseModel):
    """Team model for MongoDB"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    description: Optional[str] = None
    captain_id: str
    members: List[str] = []
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

class SponsorModel(BaseModel):
    """Sponsor model for MongoDB"""
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    name: str
    org_id: str
    verified: bool = False
    created_at: datetime = Field(default_factory=lambda: datetime.now(timezone.utc))
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat()
        }

# MongoDB Collection Names
COLLECTIONS = {
    "users": "users",
    "profiles": "profiles", 
    "games": "games",
    "highlights": "highlights",
    "gigs": "gigs",
    "applications": "applications",
    "endorsements": "endorsements",
    "soulbound_nfts": "soulbound_nfts",
    "teams": "teams",
    "sponsors": "sponsors"
} 