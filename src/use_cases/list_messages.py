from typing import List
from repositories.message_repository import MessageRepository


class ListMessages:
    """Caso de uso: Listar todos los mensajes"""
    
    def __init__(self, repository: MessageRepository):
        self._repository = repository
    
    def execute(self) -> List:
        """Ejecuta la lógica para obtener todos los mensajes"""
        return self._repository.get_all()
