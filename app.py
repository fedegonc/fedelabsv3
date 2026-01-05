from fastapi import FastAPI
import sys
import os

# Agregar el directorio src al path
sys.path.append(os.path.join(os.path.dirname(__file__), 'src'))

from presentation.message_controller import router as message_router

app = FastAPI(
    title="Fedelabs API",
    description="Backend profesional con arquitectura limpia",
    version="1.0.0"
)

# Incluir router de mensajes
app.include_router(message_router, tags=["messages"])

@app.get("/")
async def root():
    return {
        "message": "Fedelabs API - Backend Profesional",
        "docs": "/docs",
        "architecture": "Clean Architecture"
    }
