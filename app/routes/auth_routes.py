from fastapi import APIRouter, Depends
from ..controllers.auth_controller import AuthController
from ..models.auth_model import LoginRequest, TokenResponse
from ..config.auth_deps import get_current_user

router = APIRouter(prefix="/auth", tags=["autenticación"])
controller = AuthController()


@router.post("/login", response_model=TokenResponse, summary="Iniciar sesión — obtiene JWT temporal (60 min)")
async def login(data: LoginRequest):
    """
    Credenciales demo:
    - **username**: nelson
    - **rol**: admin
    - **password**: 1234
    """
    return controller.login(data)


@router.post("/seed", summary="Seed completo: catálogos + 3 usuarios demo (solo dev)")
async def seed():
    """
    Siembra todos los datos base del sistema:
    - Roles (ADMIN, DOCENTE, ESTUDIANTE)
    - Facultad y Programa demo
    - Dependencias (5)
    - Tipos PQRS (Petición, Queja, Reclamo, Sugerencia)
    - Estados (Pendiente, En revisión, Resuelto, Rechazado)
    - Prioridades (Baja, Media, Alta)
    - Usuarios: nelson/1234 (ADMIN), maria/1234 (DOCENTE), juan/1234 (ESTUDIANTE)
    """
    return controller.seed_demo_user()


@router.get("/me", summary="Información del usuario autenticado")
async def me(current_user: dict = Depends(get_current_user)):
    return {
        "id_usuario": current_user.get("id_usuario"),
        "nombre":     current_user.get("nombre"),
        "rol":        current_user.get("rol"),
    }
