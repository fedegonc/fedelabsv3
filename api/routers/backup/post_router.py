from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, status
from src.domain.entities import Post
from src.domain.enums import PostType, PostStatus
from api.schemas import (
    PostResponse,
    PostCreate,
    PostUpdate
)

router = APIRouter(prefix="/posts", tags=["posts"])

# Simulación de base de datos en memoria
posts_db = []
next_id = 1


@router.get("/", response_model=List[PostResponse])
def list_posts(status: PostStatus = PostStatus.PUBLISHED, type: PostType = None):
    """Lista posts públicos por defecto, con filtro opcional por tipo."""
    filtered = posts_db
    
    if status:
        filtered = [p for p in filtered if p.status == status]
    
    if type:
        filtered = [p for p in filtered if p.type == type]
    
    return [
        PostResponse(
            id=p.id,
            title=p.title,
            content=p.content,
            type=p.type,
            status=p.status,
            published_at=p.published_at
        ) for p in filtered
    ]


@router.get("/{post_id}", response_model=PostResponse)
def get_post(post_id: int):
    """Obtiene un post específico."""
    post = next((p for p in posts_db if p.id == post_id), None)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post no encontrado"
        )
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        type=post.type,
        status=post.status,
        published_at=post.published_at
    )


@router.post("/", response_model=PostResponse, status_code=status.HTTP_201_CREATED)
def create_post(post_data: PostCreate):
    """Crea un nuevo post (siempre en draft)."""
    global next_id
    
    post = Post(
        id=next_id,
        title=post_data.title,
        content=post_data.content,
        type=post_data.type,
        status=PostStatus.DRAFT
    )
    
    posts_db.append(post)
    next_id += 1
    
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        type=post.type,
        status=post.status,
        published_at=post.published_at
    )


@router.put("/{post_id}", response_model=PostResponse)
def update_post(post_id: int, post_data: PostUpdate):
    """Actualiza un post existente."""
    post = next((p for p in posts_db if p.id == post_id), None)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post no encontrado"
        )
    
    if post_data.title:
        post.title = post_data.title
    if post_data.content:
        post.content = post_data.content
    if post_data.type:
        post.type = post_data.type
    if post_data.status:
        post.status = post_data.status
    
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        type=post.type,
        status=post.status,
        published_at=post.published_at
    )


@router.post("/{post_id}/publish", response_model=PostResponse)
def publish_post(post_id: int):
    """Publica un post."""
    post = next((p for p in posts_db if p.id == post_id), None)
    if not post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post no encontrado"
        )
    
    post.publish()
    
    return PostResponse(
        id=post.id,
        title=post.title,
        content=post.content,
        type=post.type,
        status=post.status,
        published_at=post.published_at
    )


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int):
    """Elimina un post."""
    global posts_db
    initial_len = len(posts_db)
    posts_db = [p for p in posts_db if p.id != post_id]
    
    if len(posts_db) == initial_len:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Post no encontrado"
        )
