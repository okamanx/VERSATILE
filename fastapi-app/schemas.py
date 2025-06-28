from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import datetime

class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str
    user_type: str  # "player" or "org"
    bio: Optional[str] = None
    location: Optional[str] = None
    socials: Optional[dict] = None  # like {"twitter": "...", "twitch": "..."}
    games: Optional[list[str]] = None

class UserOut(BaseModel):
    id: str
    username: str
    email: EmailStr
    user_type: str
    bio: Optional[str] = None
    location: Optional[str] = None
    socials: Optional[dict] = None
    games: Optional[list[str]] = None

class UserUpdate(BaseModel):
    username: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    socials: Optional[dict] = None
    games: Optional[list[str]] = None

class UserLogin(BaseModel):
    email: EmailStr
    password: str

class GigCreate(BaseModel):
    title: str
    description: str
    location: str
    game: Optional[str] = None
    budget: Optional[str] = None
    skills_required: Optional[List[str]] = []
    tags: Optional[List[str]] = []
    deadline: Optional[datetime] = None
    status: Optional[str] = "open"

class GigOut(GigCreate):
    id: str
    org_id: str
    created_at: datetime
    applicant_count: Optional[int] = 0

class GigUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    location: Optional[str] = None
    game: Optional[str] = None
    budget: Optional[str] = None
    skills_required: Optional[List[str]] = None
    tags: Optional[List[str]] = None
    deadline: Optional[str] = None
    status: Optional[str] = None

class ApplicationCreate(BaseModel):
    gig_id: str
    player_id: str
    status: Optional[str] = "Pending"


class EndorsementCreate(BaseModel):
    endorsed_id: str
    rating: int = Field(..., ge=1, le=5, description="Rating must be between 1 and 5")
    comment: Optional[str] = None
