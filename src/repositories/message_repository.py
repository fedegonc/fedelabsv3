from abc import ABC, abstractmethod
from typing import List, Optional
from src.domain.entities.message import Message


class MessageRepository(ABC):
    """Contrato del repositorio - Principio de Inversión de Dependencias"""
    
    @abstractmethod
    def save(self, message: Message) -> Message:
        """Guardar un mensaje"""
        pass
    
    @abstractmethod
    def get_by_id(self, message_id: int) -> Optional[Message]:
        """Obtener mensaje por ID"""
        pass
    
    @abstractmethod
    def get_all(self) -> List[Message]:
        """Obtener todos los mensajes"""
        pass
