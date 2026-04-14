from fastapi import APIRouter, Request, HTTPException
from ..controllers.pqrs_controller import PqrsController
from ..models.pqrs_model import Pqrs

router = APIRouter(prefix="/pqrs", tags=["pqrs"])
controller = PqrsController()


@router.get("/")
async def get_pqrs_all():
    return controller.get_pqrs_all()


@router.get("/{id_pqrs}")
async def get_pqrs(id_pqrs: int):
    return controller.get_pqrs(id_pqrs)


@router.post("/")
async def create_pqrs(request: Request):
    data = await request.json()
    pqrs = Pqrs(**data)
    return controller.create_pqrs(pqrs)


# Keep old route for backward compat
@router.post("/create_pqrs")
async def create_pqrs_legacy(request: Request):
    data = await request.json()
    pqrs = Pqrs(**data)
    return controller.create_pqrs(pqrs)


@router.put("/{id_pqrs}")
async def update_pqrs(id_pqrs: int, request: Request):
    data = await request.json()
    pqrs = Pqrs(**data)
    return controller.update_pqrs(id_pqrs, pqrs)


# Keep old route for backward compat
@router.put("/update_pqrs/{id_pqrs}")
async def update_pqrs_legacy(id_pqrs: int, request: Request):
    data = await request.json()
    pqrs = Pqrs(**data)
    return controller.update_pqrs(id_pqrs, pqrs)


@router.patch("/{id_pqrs}/estado")
async def patch_estado_pqrs(id_pqrs: int, request: Request):
    """Cambia solo el estado de un PQRS (activo/inactivo o id_estado)."""
    data = await request.json()
    return controller.patch_estado(id_pqrs, data)


@router.delete("/{id_pqrs}")
async def delete_pqrs(id_pqrs: int):
    return controller.delete_pqrs(id_pqrs)


# Keep old route for backward compat
@router.delete("/delete_pqrs/{id_pqrs}")
async def delete_pqrs_legacy(id_pqrs: int):
    return controller.delete_pqrs(id_pqrs)