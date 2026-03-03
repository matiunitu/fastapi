from fastapi import APIRouter, HTTPException
from controllers.tipospqrs_controller import *
from models.tipospqrs_model import Tipospqrs
from controllers.tipospqrs_controller import TipospqrsController

router = APIRouter()
nuevo_tipospqrs = TipospqrsController()

@router.post("/create_tipospqrs")
async def create_tipospqrs(tipospqrs: Tipospqrs):
    rpta = nuevo_tipospqrs.create_tipospqrs(tipospqrs)
    return rpta

@router.get("/get_tipospqrs/{id_tipospqrs}", response_model=Tipospqrs)
async def get_tipospqrs(id_tipospqrs: int):
    rpta = nuevo_tipospqrs.get_tipospqrs(id_tipospqrs)
    return rpta

@router.get("/get_tipospqrs/")
async def get_tipospqrs_all():
    rpta = nuevo_tipospqrs.get_tipospqrs()
    return rpta