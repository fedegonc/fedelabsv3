from dataclasses import dataclass
from datetime import datetime
from typing import Optional


@dataclass
class Message:
    """Entidad de Mensaje - Corazón del dominio"""
    text: str
    id: Optional[int] = None
    created_at: Optional[datetime] = None
    
    def __post_init__(self):
        if self.created_at is None:
            self.created_at = datetime.now()
    
    def validate(self):
        """Validación de negocio"""
        if not self.text or len(self.text.strip()) == 0:
            raise ValueError("El mensaje no puede estar vacío")
        if len(self.text) > 255:
            raise ValueError("El mensaje no puede exceder 255 caracteres")
    
    def sanitize(self):
        """Limpieza de datos"""
        self.text = self.text.strip()
