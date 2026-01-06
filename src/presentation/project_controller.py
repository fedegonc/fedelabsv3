from datetime import datetime
from typing import List
from fastapi import APIRouter, HTTPException, status
from src.domain.entities import Project
from src.domain.enums import ProjectStatus
from src.presentation.dto import (
    ProjectResponse, 
    ProjectCreate, 
    ProjectUpdate
)

router = APIRouter(prefix="/projects", tags=["projects"])

# Simulación de base de datos en memoria
projects_db = []
next_id = 1


@router.get("/", response_model=List[ProjectResponse])
def list_projects(status: ProjectStatus = ProjectStatus.PUBLISHED):
    """Lista proyectos públicos por defecto."""
    filtered = [p for p in projects_db if p.status == status]
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
        ) for p in filtered
    ]


@router.get("/{project_id}", response_model=ProjectResponse)
def get_project(project_id: int):
    """Obtiene un proyecto específico."""
    project = next((p for p in projects_db if p.id == project_id), None)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
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


@router.post("/", response_model=ProjectResponse, status_code=status.HTTP_201_CREATED)
def create_project(project_data: ProjectCreate):
    """Crea un nuevo proyecto (siempre en draft)."""
    global next_id
    
    project = Project(
        id=next_id,
        title=project_data.title,
        description=project_data.description,
        stack=project_data.stack,
        status=ProjectStatus.DRAFT,
        repo_url=str(project_data.repo_url) if project_data.repo_url else None,
        demo_url=str(project_data.demo_url) if project_data.demo_url else None,
        created_at=datetime.now()
    )
    
    projects_db.append(project)
    next_id += 1
    
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


@router.put("/{project_id}", response_model=ProjectResponse)
def update_project(project_id: int, project_data: ProjectUpdate):
    """Actualiza un proyecto existente."""
    project = next((p for p in projects_db if p.id == project_id), None)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    if project_data.title:
        project.title = project_data.title
    if project_data.description:
        project.description = project_data.description
    if project_data.stack:
        project.stack = project_data.stack
    if project_data.repo_url:
        project.repo_url = str(project_data.repo_url)
    if project_data.demo_url:
        project.demo_url = str(project_data.demo_url)
    if project_data.status:
        project.status = project_data.status
    
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


@router.post("/{project_id}/publish", response_model=ProjectResponse)
def publish_project(project_id: int):
    """Publica un proyecto."""
    project = next((p for p in projects_db if p.id == project_id), None)
    if not project:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
    
    project.publish()
    
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


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_project(project_id: int):
    """Elimina un proyecto."""
    global projects_db
    initial_len = len(projects_db)
    projects_db = [p for p in projects_db if p.id != project_id]
    
    if len(projects_db) == initial_len:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Proyecto no encontrado"
        )
