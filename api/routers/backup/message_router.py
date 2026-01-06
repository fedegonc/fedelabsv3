from fastapi import APIRouter, HTTPException
from typing import List
from datetime import datetime
from api.schemas import MessageCreate, MessageResponse

router = APIRouter()

# Almacenamiento en memoria (temporal)
message_storage = []
next_id = 1


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
    return message_storage


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
    """Endpoint para crear un mensaje"""
    global next_id
    
    if not message.text or not message.text.strip():
        raise HTTPException(status_code=400, detail="El mensaje no puede estar vacío")
    
    new_message = MessageResponse(
        id=next_id,
        text=message.text,
        created_at=datetime.now()
    )
    
    message_storage.append(new_message)
    next_id += 1
    
    return new_message


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
    for message in message_storage:
        if message.id == message_id:
            return message
    
    raise HTTPException(status_code=404, detail="Mensaje no encontrado")
