from fastapi import APIRouter
from controllers.dependencias_controller import DependenciasController
from models.dependencias_model import Dependencias

router = APIRouter()
nuevo_dependencia = DependenciasController()

@router.post("/create_dependencia")
async def create_dependencia(dependencia: Dependencias):
    return nuevo_dependencia.create_dependencia(dependencia)

@router.get("/get_dependencia/{id_dependencia}")
async def get_dependencia(id_dependencia: int):
    return nuevo_dependencia.get_dependencia(id_dependencia)

@router.get("/get_dependencias/")
async def get_dependencias():
    return nuevo_dependencia.get_dependencias()