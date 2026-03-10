from fastapi import APIRouter, Request
from controllers.pqrs_controller import PqrsController
from models.pqrs_model import Pqrs

router = APIRouter(prefix="/pqrs", tags=["pqrs"])
controller = PqrsController()

@router.post("/", summary="Crear PQRS")
async def create_pqrs(request: Request):
    data = await request.json()
    campos = ["radicado", "descripcion", "id_usuario", "id_tipospqrs", "id_estado", "id_prioridad"]
    pqrs_data = {k: data[k] for k in campos if k in data}
    pqrs = Pqrs(**pqrs_data)
    return controller.create_pqrs(pqrs)

@router.get("/", summary="Listar PQRS")
async def get_pqrs():
    return controller.get_pqrs_all()

@router.get("/{id_pqrs}", summary="Obtener PQRS")
async def get_pqrs_by_id(id_pqrs: int):
    return controller.get_pqrs(id_pqrs)

@router.put("/{id_pqrs}", summary="Actualizar PQRS")
async def update_pqrs(id_pqrs: int, request: Request):
    try:
        data = await request.json()
    except Exception:
        data = {}
    campos = ["radicado", "descripcion", "id_usuario", "id_tipospqrs", "id_estado", "id_prioridad"]
    pqrs_data = {k: data[k] for k in campos if k in data}
    pqrs = Pqrs(**pqrs_data)
    return controller.update_pqrs(id_pqrs, pqrs)

@router.delete("/{id_pqrs}", summary="Eliminar PQRS")
async def delete_pqrs(id_pqrs: int):
    return controller.delete_pqrs(id_pqrs)
