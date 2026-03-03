from fastapi import APIRouter, HTTPException
from controllers.roles_controller import *
from models.roles_model import Roles

router = APIRouter()

nuevo_role = RolesController()

@router.post("/create_role")
async def create_role(role: Roles):
    rpta = nuevo_role.create_roles(role)
    return rpta

@router.get("/get_role/{id_rol}", response_model=Roles)
async def get_role(id_rol: int):
    rpta = nuevo_role.get_user(id_rol)
    return rpta

@router.get("/get_roles/")
async def get_roles():
    rpta = nuevo_role.get_users()
    return rpta