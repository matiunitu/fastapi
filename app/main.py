from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

# Importar rutas
from routes.usuarios_routes import router as usuarios_router
from routes.roles_routes import router as roles_router
from routes.dependencias_routes import router as dependencias_router
from routes.historial_routes import router as historial_router
from routes.facultades_routes import router as facultades_router
from routes.programas_routes import router as programas_router
from routes.tipospqrs_routes import router as tipospqrs_router
from routes.estados_routes import router as estados_router
from routes.prioridades_routes import router as prioridades_router
from routes.pqrs_routes import router as pqrs_router
from routes.respuestas_routes import router as respuestas_router
from routes.historial_estados_routes import router as historial_estados_router

# Crear app FastAPI
app = FastAPI(
    title="API de Gestión de Usuarios Universitarios",
    description="API para gestionar usuarios, roles, dependencias e historial con PostgreSQL",
    version="1.0.0",
)

# Middleware CORS para permitir que cualquier frontend pueda consumir la API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],          # Permite todos los orígenes
    allow_credentials=True,
    allow_methods=["*"],          # Permite todos los métodos HTTP
    allow_headers=["*"],          # Permite todos los headers
)

# Incluir todas las rutas
app.include_router(usuarios_router)
app.include_router(roles_router)
app.include_router(dependencias_router)
app.include_router(facultades_router)
app.include_router(programas_router)
app.include_router(tipospqrs_router)
app.include_router(estados_router)
app.include_router(prioridades_router)
app.include_router(pqrs_router)
app.include_router(respuestas_router)
app.include_router(historial_router)
app.include_router(historial_estados_router)

# Ruta raíz de prueba
@app.get("/", summary="Saludo base")
async def root():
    return {"message": "API de Gestión de Usuarios Universitarios activa"}