from fastapi import APIRouter, HTTPException
from controllers.estados_controller import *
from models.estados_model import Estados

router = APIRouter()

nuevo_estado = EstadosController()

@router.post("/create_estado")
async def create_estados(estado: Estados):
    rpta = nuevo_estado.create_estado(estado)
    return rpta

@router.get("/get_estado/{id_estado}", response_model=Estados)
async def get_estado(id_estado: int):
    rpta = nuevo_estado.get_user(id_estado)
    return rpta

@router.get("/get_estados/")
async def get_estados():
    rpta = nuevo_estado.get_users()
    return rpta