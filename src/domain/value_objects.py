from dataclasses import dataclass
from typing import Optional
import re


@dataclass(frozen=True)
class URL:
    """Value object para URLs validadas."""
    value: str
    
    def __post_init__(self):
        if not self.value:
            object.__setattr__(self, 'value', '')
            return
        
        # Validación básica de URL
        url_pattern = re.compile(
            r'^https?:\/\/'  # http:// o https://
            r'(?:(?:[A-Z0-9](?:[A-Z0-9-]{0,61}[A-Z0-9])?\.)+[A-Z]{2,6}\.?|'  # dominio
            r'localhost|'  # localhost
            r'\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3})'  # IP
            r'(?::\d+)?'  # puerto opcional
            r'(?:/?|[/?]\S+)$', re.IGNORECASE)
        
        if not url_pattern.match(self.value):
            raise ValueError(f"URL inválida: {self.value}")
    
    def __str__(self) -> str:
        return self.value
    
    @classmethod
    def create(cls, url: Optional[str]) -> Optional['URL']:
        """Crea una URL o devuelve None si está vacía."""
        if not url:
            return None
        return cls(url)


@dataclass(frozen=True)
class Stack:
    """Value object para el stack tecnológico."""
    technologies: list[str]
    
    def __post_init__(self):
        if not self.technologies:
            raise ValueError("El stack no puede estar vacío")
        
        # Normalizar y validar
        normalized = []
        for tech in self.technologies:
            if not tech or not tech.strip():
                continue
            normalized.append(tech.strip().lower())
        
        if not normalized:
            raise ValueError("Debe haber al menos una tecnología válida")
        
        object.__setattr__(self, 'technologies', normalized)
    
    def __str__(self) -> str:
        return ", ".join(self.technologies)
    
    def contains(self, technology: str) -> bool:
        """Verifica si una tecnología está en el stack."""
        return technology.lower() in self.technologies
