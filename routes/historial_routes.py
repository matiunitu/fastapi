from fastapi import APIRouter, HTTPException
from controllers.historial_controller import *
from models.historial_model import Historial

router = APIRouter()

nuevo_historial = HistorialController()

@router.post("/create_historial")
async def create_historial(historial: Historial):
    rpta = nuevo_historial.create_historial(historial)
    return rpta

@router.get("/get_historial/{id_historial}", response_model=Historial)
async def get_historial(id_historial: int):
    rpta = nuevo_historial.get_user(id_historial)
    return rpta

@router.get("/get_historiales/")
async def get_historiales():
    rpta = nuevo_historial.get_users()
    return rpta