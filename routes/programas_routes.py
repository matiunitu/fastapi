from fastapi import APIRouter, HTTPException
from controllers.programas_controller import *
from models.programas_model import Programas

router = APIRouter()

nuevo_programa = ProgramasController()

@router.post("/create_programa")
async def create_programa(programa: Programas):
    rpta = nuevo_programa.create_programas(programa)
    return rpta

@router.get("/get_programa/{id_programa}", response_model=Programas)
async def get_programa(id_programa: int):
    rpta = nuevo_programa.get_programas(id_programa)
    return rpta

@router.get("/get_programas/")
async def get_programas():
    rpta = nuevo_programa.get_programass()
    return rpta