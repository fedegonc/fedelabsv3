from typing import List
from fastapi import APIRouter, HTTPException
from src.domain.entities import Project
from src.domain.enums import ProjectStatus
from api.schemas import ProjectResponse

router = APIRouter(prefix="/projects", tags=["Projects"])

# Simulación de base de datos en memoria
projects_db = []


@router.get("/", response_model=List[ProjectResponse])
def list_projects(status: ProjectStatus = ProjectStatus.PUBLISHED):
    """Lista todos los proyectos públicos."""
    filtered_projects = [p for p in projects_db if p.status == status]
    return [
        ProjectResponse(
            id=p.id,
            title=p.title,
            description=p.description,
            stack=p.stack,
            status=p.status,
            repo_url=p.repo_url,
            demo_url=p.demo_url,
            created_at=p.created_at
        ) for p in filtered_projects
    ]


@router.get("/{slug}", response_model=ProjectResponse)
def get_project_by_slug(slug: str):
    """Obtiene un proyecto por su slug."""
    for project in projects_db:
        if project.slug == slug and project.status == ProjectStatus.PUBLISHED:
            return ProjectResponse(
                id=project.id,
                title=project.title,
                description=project.description,
                stack=project.stack,
                status=project.status,
                repo_url=project.repo_url,
                demo_url=project.demo_url,
                created_at=project.created_at
            )
    raise HTTPException(status_code=404, detail="Proyecto no encontrado")
