from dataclasses import dataclass
from datetime import datetime
from typing import Optional
from src.domain.enums import PostType, PostStatus


@dataclass
class Post:
    """Tu pensamiento técnico, no tu ego."""
    id: Optional[int]
    title: str
    content: str
    type: PostType
    status: PostStatus
    published_at: Optional[datetime] = None
    
    def __post_init__(self):
        if not self.title or not self.title.strip():
            raise ValueError("El título no puede estar vacío")
        if not self.content or not self.content.strip():
            raise ValueError("Un post dice algo o no existe")
        if self.type not in PostType:
            raise ValueError("Tipo de post inválido")
        if self.status not in PostStatus:
            raise ValueError("Estado de post inválido")
    
    def publish(self) -> None:
        """Publica el post y registra la fecha."""
        if self.status == PostStatus.DRAFT:
            self.status = PostStatus.PUBLISHED
            self.published_at = datetime.now()
    
    def archive(self) -> None:
        """Archiva el post."""
        self.status = PostStatus.ARCHIVED
    
    def is_published(self) -> bool:
        return self.status == PostStatus.PUBLISHED
    
    def is_draft(self) -> bool:
        return self.status == PostStatus.DRAFT
    
    def has_meaningful_content(self) -> bool:
        """Verifica que el post aporte valor."""
        return len(self.content.strip()) > 50  # Mínimo de caracteres para considerar significativo
