from dataclasses import dataclass
from datetime import datetime
from typing import Optional, List
from src.domain.enums import ProjectStatus


@dataclass
class Project:
    """Una pieza de evidencia técnica, no un post."""
    id: Optional[int]
    title: str
    description: str
    stack: List[str]
    status: ProjectStatus
    repo_url: Optional[str] = None
    demo_url: Optional[str] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise ValueError("El título no puede estar vacío")
        if not self.description or not self.description.strip():
            raise ValueError("La descripción no puede estar vacía")
        if not self.stack:
            raise ValueError("El stack tecnológico no puede estar vacío")
    
    def publish(self) -> None:
        """Publica el proyecto si está en draft."""
        if self.status == ProjectStatus.DRAFT:
            self.status = ProjectStatus.PUBLISHED
    
    def archive(self) -> None:
        """Archiva el proyecto."""
        self.status = ProjectStatus.ARCHIVED
    
    def is_published(self) -> bool:
        return self.status == ProjectStatus.PUBLISHED
    
    def is_draft(self) -> bool:
        return self.status == ProjectStatus.DRAFT
