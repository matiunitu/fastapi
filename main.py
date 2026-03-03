from fastapi import FastAPI
from routes.roles_routes import router as role_router
from routes.programas_routes import router as programa_router
from routes.dependencias_routes import router as dependencias_router
from routes.tipospqrs_routes import router as tipospqrs_router
from routes.estados_routes import router as estados_router
from routes.Prioridades_routes import router as Prioridades_router
from routes.pqrs_routes import router as pqrs_router
from routes.respuestas_routes import router as respuestas_router
from routes.historial_routes import router as historial_router
from routes.usuarios_routes import router as usuarios_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

origins = [
    "https://ep-square-flower-aiq3n3y4-pooler.c-4.us-east-1.aws.neon.tech",
    "http://localhost"
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(role_router)
app.include_router(programa_router)
app.include_router(dependencias_router)
app.include_router(tipospqrs_router)
app.include_router(estados_router)
app.include_router(Prioridades_router)
app.include_router(pqrs_router)
app.include_router(respuestas_router)
app.include_router(historial_router)
app.include_router(usuarios_router)

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)