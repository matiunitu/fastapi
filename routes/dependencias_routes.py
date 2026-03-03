from fastapi import APIRouter, HTTPException
from controllers.dependencias_controller import *
from models.dependencias_model import Dependencia

router = APIRouter()

nuevo_dependencia = DependenciasController()

@router.post("/create_dependencia")
async def create_dependencia(dependencia: Dependencia):
    rpta = nuevo_dependencia.create_dependencia(dependencia)
    return rpta

@router.get("/get_dependencia/{id_dependencia}", response_model=Dependencia)
async def get_dependencia(id_dependencia: int):
    rpta = nuevo_dependencia.get_dependencia(id_dependencia)
    return rpta

@router.get("/get_dependencias/")
async def get_dependencias():
    rpta = nuevo_dependencia.get_dependencias()
    return rpta