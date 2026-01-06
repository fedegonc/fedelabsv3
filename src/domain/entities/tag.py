from dataclasses import dataclass
from typing import Optional


@dataclass
class Tag:
    """Ordena, no decora."""
    id: Optional[int]
    name: str
    
    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("El nombre del tag no puede estar vacío")
        self.name = self.name.lower().strip()
        if len(self.name) > 20:
            raise ValueError("El tag debe tener máximo 20 caracteres")
        if ' ' in self.name:
            raise ValueError("Los tags no pueden contener espacios")
    
    @classmethod
    def create(cls, name: str) -> 'Tag':
        """Crea un nuevo tag validado."""
        return cls(id=None, name=name)
    
    def __str__(self) -> str:
        return self.name
