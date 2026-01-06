from datetime import datetime
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from src.presentation.project_controller import router as projects_router
from src.presentation.post_controller import router as posts_router
from src.presentation.profile_controller import router as profile_router
from src.presentation.dto import HealthResponse

app = FastAPI(
    title="Portfolio Técnico API",
    description="Un portfolio vivo con criterio técnico - sin humo, sin red social, sin CMS gigante",
    version="1.0.0",
    docs_url="/docs",
    redoc_url="/redoc"
)

# Configurar CORS para desarrollo
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://localhost:8080"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Incluir routers
app.include_router(projects_router)
app.include_router(posts_router)
app.include_router(profile_router)


@app.get("/", response_model=dict)
def root():
    """Endpoint raíz con información del portfolio."""
    return {
        "message": "Portfolio Técnico Vivo",
        "description": "Exposición de trabajo y pensamiento técnico",
        "endpoints": {
            "projects": "/projects",
            "posts": "/posts",
            "profile": "/profile",
            "docs": "/docs",
            "health": "/health"
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
