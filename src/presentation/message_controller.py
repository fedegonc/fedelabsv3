from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
import sys
import os

# Agregar el directorio raíz al path
sys.path.append(os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__)))))

# Casos de uso (inyectados)
from use_cases.create_message import CreateMessage
from use_cases.list_messages import ListMessages
from use_cases.get_message import GetMessage

# DTOs para la API
class MessageCreate(BaseModel):
    text: str
    
    class Config:
        schema_extra = {
            "example": {
                "text": "Este es un mensaje de ejemplo"
            }
        }


class MessageResponse(BaseModel):
    id: int
    text: str
    created_at: datetime
    
    class Config:
        schema_extra = {
            "example": {
                "id": 1,
                "text": "Este es un mensaje de ejemplo",
                "created_at": "2024-01-05T18:00:00"
            }
        }


# Router
router = APIRouter()


# Inyección de dependencias (simulada para el ejemplo)
# En un proyecto real, usarías un contenedor DI
message_storage = []
next_id = 1


class InMemoryMessageRepository:
    def save(self, message):
        global next_id
        message.id = next_id
        next_id += 1
        message_storage.append(message)
        return message
    
    def get_by_id(self, message_id):
        for msg in message_storage:
            if msg.id == message_id:
                return msg
        return None
    
    def get_all(self):
        return message_storage.copy()


# Instancias de casos de uso
repo = InMemoryMessageRepository()
create_message_use_case = CreateMessage(repo)
list_messages_use_case = ListMessages(repo)
get_message_use_case = GetMessage(repo)


@router.get(
    "/messages",
    response_model=List[MessageResponse],
    summary="Obtener todos los mensajes",
    description="Retorna una lista con todos los mensajes almacenados en el sistema",
    responses={
        200: {
            "description": "Lista de mensajes obtenida exitosamente",
            "content": {
                "application/json": {
                    "example": [
                        {
                            "id": 1,
                            "text": "Primer mensaje",
                            "created_at": "2024-01-05T18:00:00"
                        }
                    ]
                }
            }
        }
    }
)
async def get_messages():
    """Endpoint para listar todos los mensajes"""
    messages = list_messages_use_case.execute()
    return [
        MessageResponse(
            id=msg.id,
            text=msg.text,
            created_at=msg.created_at
        ) for msg in messages
    ]


@router.post(
    "/messages",
    response_model=MessageResponse,
    summary="Crear un nuevo mensaje",
    description="Crea y persiste un nuevo mensaje en el sistema",
    responses={
        201: {
            "description": "Mensaje creado exitosamente",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "text": "Nuevo mensaje",
                        "created_at": "2024-01-05T18:00:00"
                    }
                }
            }
        },
        400: {
            "description": "Error de validación",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "El mensaje no puede estar vacío"
                    }
                }
            }
        }
    }
)
async def create_message(message: MessageCreate):
    """Endpoint para crear un mensaje - SIN LÓGICA DE NEGOCIO"""
    try:
        # El controller solo delega al caso de uso
        new_message = create_message_use_case.execute(message.text)
        return MessageResponse(
            id=new_message.id,
            text=new_message.text,
            created_at=new_message.created_at
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))


@router.get(
    "/messages/{message_id}",
    response_model=MessageResponse,
    summary="Obtener mensaje por ID",
    description="Retorna un mensaje específico basado en su ID único",
    responses={
        200: {
            "description": "Mensaje encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "id": 1,
                        "text": "Mensaje específico",
                        "created_at": "2024-01-05T18:00:00"
                    }
                }
            }
        },
        404: {
            "description": "Mensaje no encontrado",
            "content": {
                "application/json": {
                    "example": {
                        "detail": "Mensaje no encontrado"
                    }
                }
            }
        }
    }
)
async def get_message(message_id: int):
    """Endpoint para obtener un mensaje específico"""
    try:
        message = get_message_use_case.execute(message_id)
        if message:
            return MessageResponse(
                id=message.id,
                text=message.text,
                created_at=message.created_at
            )
        raise HTTPException(status_code=404, detail="Mensaje no encontrado")
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
