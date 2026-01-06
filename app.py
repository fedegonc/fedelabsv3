from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

# Importar routers públicos y admin
from api.routers.projects_public import router as projects_router
from api.routers.posts_public import router as posts_router
from api.routers.profile_public import router as profile_router
from api.routers.admin import router as admin_router
from api.schemas import HealthResponse

app = FastAPI(
    title="Fedelabs API",
    description="Backend profesional con arquitectura limpia",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc",
    openapi_url="/openapi.json"
)

# Configurar CORS para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers públicos
app.include_router(projects_router)
app.include_router(posts_router)
app.include_router(profile_router)

# Incluir router admin (endpoints privados)
app.include_router(admin_router)


@app.get("/", response_model=dict)
def root():
    """Endpoint raíz con información de la API."""
    return {
        "message": "Fedelabs API",
        "description": "Backend profesional con arquitectura limpia",
        "endpoints": {
            "public": {
                "projects": "/projects",
                "posts": "/posts",
                "profile": "/profile",
                "health": "/health"
            },
            "admin": {
                "publish_project": "/admin/projects/{id}/publish",
                "publish_post": "/admin/posts/{id}/publish",
                "update_profile": "/admin/profile"
            },
            "docs": "/docs"
        }
    }


@app.get("/health", response_model=HealthResponse)
def health_check():
    """Health check simple."""
    return HealthResponse(
        status="healthy",
        timestamp=datetime.now(),
        version="1.0.0"
    )


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
