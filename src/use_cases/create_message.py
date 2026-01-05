from domain.entities.message import Message
from repositories.message_repository import MessageRepository


class CreateMessage:
    """Caso de uso: Crear un mensaje - Principio de Responsabilidad Única"""
    
    def __init__(self, repository: MessageRepository):
        self._repository = repository
    
    def execute(self, text: str) -> Message:
        """Ejecuta la lógica de crear un mensaje"""
        # Crear la entidad
        message = Message(text=text)
        
        # Validaciones de negocio
        message.validate()
        
        # Limpieza de datos
        message.sanitize()
        
        # Persistir
        return self._repository.save(message)
