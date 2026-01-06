from fastapi import APIRouter, HTTPException, status
from src.domain.entities import Profile
from api.schemas import ProfileResponse, ProfileUpdate

router = APIRouter(prefix="/profile", tags=["profile"])

# Perfil singleton en memoria
profile_instance: Profile = None


@router.get("/", response_model=ProfileResponse)
def get_profile():
    """Obtiene el perfil."""
    profile = Profile.get_instance()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado. Crea uno primero."
        )
    
    return ProfileResponse(
        name=profile.name,
        role=profile.role,
        bio=profile.bio,
        links=profile.links
    )


@router.post("/", response_model=ProfileResponse, status_code=status.HTTP_201_CREATED)
def create_profile(name: str, role: str, bio: str, links: dict = None):
    """Crea el perfil (solo se puede crear una vez)."""
    if Profile.get_instance():
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El perfil ya existe. Usa PUT para actualizarlo."
        )
    
    global profile_instance
    profile_instance = Profile.create(
        name=name,
        role=role,
        bio=bio,
        links=links or {}
    )
    
    return ProfileResponse(
        name=profile_instance.name,
        role=profile_instance.role,
        bio=profile_instance.bio,
        links=profile_instance.links
    )


@router.put("/", response_model=ProfileResponse)
def update_profile(profile_data: ProfileUpdate):
    """Actualiza el perfil."""
    profile = Profile.get_instance()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado. Crea uno primero."
        )
    
    profile.update(
        name=profile_data.name,
        role=profile_data.role,
        bio=profile_data.bio,
        links=profile_data.links
    )
    
    return ProfileResponse(
        name=profile.name,
        role=profile.role,
        bio=profile.bio,
        links=profile.links
    )


@router.post("/links", response_model=ProfileResponse)
def add_link(platform: str, url: str):
    """Agrega un nuevo enlace al perfil."""
    profile = Profile.get_instance()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado. Crea uno primero."
        )
    
    profile.add_link(platform, url)
    
    return ProfileResponse(
        name=profile.name,
        role=profile.role,
        bio=profile.bio,
        links=profile.links
    )


@router.delete("/links/{platform}", response_model=ProfileResponse)
def remove_link(platform: str):
    """Elimina un enlace del perfil."""
    profile = Profile.get_instance()
    if not profile:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Perfil no encontrado. Crea uno primero."
        )
    
    profile.remove_link(platform)
    
    return ProfileResponse(
        name=profile.name,
        role=profile.role,
        bio=profile.bio,
        links=profile.links
    )
