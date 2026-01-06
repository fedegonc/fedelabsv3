from dataclasses import dataclass
from typing import Dict, Optional, List


@dataclass
class Profile:
    """No sos multiusuario. Sos vos."""
    name: str
    role: str
    bio: str
    links: Dict[str, str]
    
    _instance: Optional['Profile'] = None
    
    def __post_init__(self):
        if not self.name or not self.name.strip():
            raise ValueError("El nombre no puede estar vacío")
        if not self.role or not self.role.strip():
            raise ValueError("El rol no puede estar vacío")
        if not self.bio or not self.bio.strip():
            raise ValueError("La bio no puede estar vacía")
    
    @classmethod
    def get_instance(cls) -> Optional['Profile']:
        """Obtiene la única instancia del perfil."""
        return cls._instance
    
    @classmethod
    def create(cls, name: str, role: str, bio: str, links: Optional[Dict[str, str]] = None) -> 'Profile':
        """Crea o actualiza el perfil único."""
        if cls._instance is not None:
            raise ValueError("Ya existe un perfil. Usa update() para modificarlo.")
        
        cls._instance = cls(
            name=name,
            role=role,
            bio=bio,
            links=links or {}
        )
        return cls._instance
    
    def update(self, name: Optional[str] = None, role: Optional[str] = None, 
               bio: Optional[str] = None, links: Optional[Dict[str, str]] = None) -> None:
        """Actualiza los datos del perfil."""
        if name:
            self.name = name
        if role:
            self.role = role
        if bio:
            self.bio = bio
        if links is not None:
            self.links = links
    
    def add_link(self, platform: str, url: str) -> None:
        """Agrega un nuevo enlace."""
        self.links[platform] = url
    
    def remove_link(self, platform: str) -> None:
        """Elimina un enlace."""
        self.links.pop(platform, None)
    
    def get_links(self) -> List[tuple]:
        """Devuelve los enlaces como lista de tuplas."""
        return list(self.links.items())
