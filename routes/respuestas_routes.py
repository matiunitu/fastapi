from fastapi import APIRouter, HTTPException
from controllers.respuestas_controller import *
from models.respuestas_model import Respuestas

router = APIRouter()

nuevo_respuesta = RespuestasController()

@router.post("/create_respuesta")
async def create_respuesta(respuesta: Respuestas):
    rpta = nuevo_respuesta.create_respuestas(respuesta)
    return rpta

@router.get("/get_respuesta/{id_respuesta}", response_model=Respuestas)
async def get_respuesta(id_respuesta: int):
    rpta = nuevo_respuesta.get_user(id_respuesta)
    return rpta

@router.get("/get_respuestas/")
async def get_users():
    rpta = nuevo_respuesta.get_respuestas()
    return rpta