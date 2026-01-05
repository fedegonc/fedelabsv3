from typing import Optional
from repositories.message_repository import MessageRepository


class GetMessage:
    """Caso de uso: Obtener un mensaje por ID"""
    
    def __init__(self, repository: MessageRepository):
        self._repository = repository
    
    def execute(self, message_id: int) -> Optional:
        """Ejecuta la lógica para obtener un mensaje específico"""
        if message_id <= 0:
            raise ValueError("ID debe ser un número positivo")
        return self._repository.get_by_id(message_id)
