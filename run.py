import uvicorn
import os

if __name__ == "__main__":
    # Configuración automática
    host = os.getenv("HOST", "127.0.0.1")
    port = int(os.getenv("PORT", 8000))
    reload = os.getenv("RELOAD", "true").lower() == "true"
    
    print(f"Iniciando Fedelabs API en http://{host}:{port}")
    print(f"Documentacion: http://{host}:{port}/docs")
    
    uvicorn.run(
        "app:app",
        host=host,
        port=port,
        reload=reload
    )
