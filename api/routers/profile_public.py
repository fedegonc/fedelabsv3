from fastapi import APIRouter, HTTPException
from src.domain.entities import Profile
from api.schemas import ProfileResponse

router = APIRouter(prefix="/profile", tags=["Profile"])


@router.get("/", response_model=ProfileResponse)
def get_profile():
    """Obtiene el perfil público."""
    profile = Profile.get_instance()
    if not profile:
        raise HTTPException(status_code=404, detail="Perfil no encontrado")
    
    return ProfileResponse(
        name=profile.name,
        role=profile.role,
        bio=profile.bio,
        links=profile.links
    )
