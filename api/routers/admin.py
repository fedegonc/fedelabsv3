from fastapi import APIRouter, HTTPException, status, Depends
from typing import Dict, Any
from src.domain.entities import Project, Post, Profile
from src.domain.enums import ProjectStatus, PostStatus
from api.schemas import ProfileUpdate

router = APIRouter(prefix="/admin", tags=["Admin"])

# Simulación de base de datos en memoria
projects_db = []
posts_db = []

# TODO: Implementar autenticación real
async def verify_admin():
    """Verifica si el usuario es admin (placeholder)."""
    # En producción, implementar JWT o similar
    return True


@router.post("/projects/{project_id}/publish", status_code=status.HTTP_204_NO_CONTENT)
async def publish_project(project_id: int, admin: bool = Depends(verify_admin)):
    """Publica un proyecto (solo admin)."""
    for project in projects_db:
        if project.id == project_id:
            project.status = ProjectStatus.PUBLISHED
            return
    raise HTTPException(status_code=404, detail="Proyecto no encontrado")


@router.post("/posts/{post_id}/publish", status_code=status.HTTP_204_NO_CONTENT)
async def publish_post(post_id: int, admin: bool = Depends(verify_admin)):
    """Publica un post (solo admin)."""
    for post in posts_db:
        if post.id == post_id:
            post.status = PostStatus.PUBLISHED
            return
    raise HTTPException(status_code=404, detail="Post no encontrado")


@router.put("/profile", response_model=Dict[str, Any])
async def update_profile(profile_data: ProfileUpdate, admin: bool = Depends(verify_admin)):
    """Actualiza el perfil (solo admin)."""
    profile = Profile.get_instance()
    if not profile:
        profile = Profile()
    
    if profile_data.name:
        profile.name = profile_data.name
    if profile_data.role:
        profile.role = profile_data.role
    if profile_data.bio:
        profile.bio = profile_data.bio
    if profile_data.links:
        profile.links = profile_data.links
    
    return {"message": "Perfil actualizado correctamente"}
