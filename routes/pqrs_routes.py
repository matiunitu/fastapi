from fastapi import APIRouter, HTTPException
from controllers.pqrs_controller import *
from models.pqrs_model import Pqrs

router = APIRouter()

nuevo_pqrs = PqrsController()

@router.post("/create_pqrs")
async def create_pqrs(pqrs: Pqrs):
    rpta = nuevo_pqrs.create_pqrs(pqrs)
    return rpta

@router.get("/get_pqrs/{id_pqrs}", response_model=Pqrs)
async def get_pqrs(id_pqrs: int):
    rpta = nuevo_pqrs.get_user(id_pqrs)
    return rpta

@router.get("/get_pqrs/")
async def get_pqrs_all():
    rpta = nuevo_pqrs.get_users()
    return rpta
