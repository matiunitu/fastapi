from fastapi import APIRouter
from controllers.usuarios_controller import UsuariosController
from models.usuarios_model import Usuarios

router = APIRouter()

nuevo_usuario = UsuariosController()

@router.post("/create_usuario")
async def create_usuario(usuario: Usuarios):
    return nuevo_usuario.create_usuarios(usuario)


@router.get("/get_usuario/{id_usuario}", response_model=Usuarios)
async def get_usuario(id_usuario: int):
    return nuevo_usuario.get_user(id_usuario)


@router.get("/get_usuarios/")
async def get_usuarios():
    return nuevo_usuario.get_users()