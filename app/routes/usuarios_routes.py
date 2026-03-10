from fastapi import APIRouter, Request
from controllers.usuarios_controller import UsuariosController
from models.usuario_model import Usuario

router = APIRouter(prefix="/usuarios", tags=["usuarios"])
controller = UsuariosController()


@router.post("/", summary="Crear usuario")
async def create_usuario(request: Request):
    data = await request.json()
    campos = ["nombre", "documento", "correo", "telefono", "id_rol", "id_programa"]
    usuario_data = {k: data[k] for k in campos if k in data}
    usuario = Usuario(**usuario_data)
    return controller.create_usuario(usuario)


@router.get("/", summary="Listar usuarios")
async def get_usuarios():
    return controller.get_usuarios()


@router.get("/{id_usuario}", summary="Obtener usuario por ID")
async def get_usuario(id_usuario: int):
    return controller.get_usuario(id_usuario)


@router.put("/{id_usuario}", summary="Actualizar usuario")
async def update_usuario(id_usuario: int, request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    campos = ["nombre", "documento", "correo", "telefono", "id_rol", "id_programa", "activo"]
    usuario_data = {k: data[k] for k in campos if k in data}
    usuario = Usuario(**usuario_data)
    return controller.update_usuario(id_usuario, usuario)


@router.delete("/{id_usuario}", summary="Eliminar usuario")
async def delete_usuario(id_usuario: int):
    return controller.delete_usuario(id_usuario)
