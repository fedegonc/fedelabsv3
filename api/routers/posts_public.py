from typing import List
from fastapi import APIRouter, HTTPException
from src.domain.entities import Post
from src.domain.enums import PostStatus
from api.schemas import PostResponse

router = APIRouter(prefix="/posts", tags=["Posts"])

# Simulación de base de datos en memoria
posts_db = []


@router.get("/", response_model=List[PostResponse])
def list_posts(status: PostStatus = PostStatus.PUBLISHED):
    """Lista todos los posts públicos."""
    filtered_posts = [p for p in posts_db if p.status == status]
    return [
        PostResponse(
            id=p.id,
            title=p.title,
            content=p.content,
            type=p.type,
            status=p.status,
            published_at=p.published_at
        ) for p in filtered_posts
    ]


@router.get("/{slug}", response_model=PostResponse)
def get_post_by_slug(slug: str):
    """Obtiene un post por su slug."""
    for post in posts_db:
        if post.slug == slug and post.status == PostStatus.PUBLISHED:
            return PostResponse(
                id=post.id,
                title=post.title,
                content=post.content,
                type=post.type,
                status=post.status,
                published_at=post.published_at
            )
    raise HTTPException(status_code=404, detail="Post no encontrado")
