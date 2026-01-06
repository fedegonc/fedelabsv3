from datetime import datetime
from typing import List, Optional, Dict
from pydantic import BaseModel, Field, HttpUrl
from src.domain.enums import ProjectStatus, PostType, PostStatus


class ProjectResponse(BaseModel):
    id: Optional[int]
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    stack: List[str] = Field(..., min_items=1)
    status: ProjectStatus
    repo_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None
    created_at: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class ProjectCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    description: str = Field(..., min_length=1, max_length=1000)
    stack: List[str] = Field(..., min_items=1)
    repo_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None


class ProjectUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    description: Optional[str] = Field(None, min_length=1, max_length=1000)
    stack: Optional[List[str]] = Field(None, min_items=1)
    repo_url: Optional[HttpUrl] = None
    demo_url: Optional[HttpUrl] = None
    status: Optional[ProjectStatus] = None


class PostResponse(BaseModel):
    id: Optional[int]
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=50)
    type: PostType
    status: PostStatus
    published_at: Optional[datetime] = None
    
    class Config:
        json_encoders = {
            datetime: lambda v: v.isoformat() if v else None
        }


class PostCreate(BaseModel):
    title: str = Field(..., min_length=1, max_length=200)
    content: str = Field(..., min_length=50)
    type: PostType


class PostUpdate(BaseModel):
    title: Optional[str] = Field(None, min_length=1, max_length=200)
    content: Optional[str] = Field(None, min_length=50)
    type: Optional[PostType] = None
    status: Optional[PostStatus] = None


class TagResponse(BaseModel):
    id: Optional[int]
    name: str = Field(..., min_length=1, max_length=20, regex=r'^[a-zA-Z0-9_-]+$')


class TagCreate(BaseModel):
    name: str = Field(..., min_length=1, max_length=20, regex=r'^[a-zA-Z0-9_-]+$')


class ProfileResponse(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    role: str = Field(..., min_length=1, max_length=100)
    bio: str = Field(..., min_length=1, max_length=500)
    links: Dict[str, str] = Field(default_factory=dict)


class ProfileUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    role: Optional[str] = Field(None, min_length=1, max_length=100)
    bio: Optional[str] = Field(None, min_length=1, max_length=500)
    links: Optional[Dict[str, str]] = None


class HealthResponse(BaseModel):
    status: str
    timestamp: datetime
    version: str = "1.0.0"
