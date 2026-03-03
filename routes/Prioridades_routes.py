from fastapi import APIRouter, HTTPException
from controllers.prioridades_controller import *
from models.prioridades_model import Prioridades

router = APIRouter()

nuevo_prioridad = PrioridadesController()

@router.post("/create_prioridad")
async def create_prioridad(prioridad: Prioridades):
    rpta = nuevo_prioridad.create_prioridades(prioridad)
    return rpta

@router.get("/get_prioridad/{id_prioridad}", response_model=Prioridades)
async def get_prioridad(id_prioridad: int):
    rpta = nuevo_prioridad.get_user(id_prioridad)
    return rpta

@router.get("/get_prioridades/")
async def get_prioridades():
    rpta = nuevo_prioridad.get_users()
    return rpta