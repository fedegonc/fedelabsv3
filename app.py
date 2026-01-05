from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "¡Hola Mundo desde FastAPI!"}

@app.get("/hola")
async def hola_mundo():
    return {"mensaje": "Hola Mundo", "framework": "FastAPI"}
