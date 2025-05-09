import asyncio
import uvicorn
import os
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import aiohttp

from src.api.routes import document_routes
from src.api.middlewares.error_handler import ErrorHandler
from src.infrastructure.database.mongodb_client import MongoDBClient

# Crear aplicación FastAPI
app = FastAPI(title="Olivia API", description="API para asistente legal Olivia")

# Configurar CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Para desarrollo
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Configurar manejador de errores
ErrorHandler(app)

# Registrar rutas
app.include_router(document_routes.router)

@app.get("/", tags=["Root"])
async def read_root():
    return {"message": "Bienvenido a Olivia API - Asistente Legal"}

@app.get("/health", tags=["Health"])
async def health_check():
    return {"status": "ok"}

@app.on_event("startup")
async def startup():
    # Inicializar conexión a MongoDB
    await MongoDBClient.connect()

@app.on_event("shutdown")
async def shutdown():
    # Cerrar conexión a MongoDB
    await MongoDBClient.disconnect()
@app.get("/models")
async def list_ollama_models():
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get("http://localhost:11434/api/tags") as response:
                if response.status == 200:
                    data = await response.json()
                    return data
                return {"error": f"Ollama responded with status {response.status}"}
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=int(os.getenv("PORT", "8000")),
        reload=True
    )