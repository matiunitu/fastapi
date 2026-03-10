from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class Usuario(BaseModel):
    id_usuario: Optional[int] = None
    nombre: str
    documento: str
    correo: str
    telefono: str
    id_rol: int
    id_programa: int
    activo: bool = True
    created_at: Optional[datetime] = None

    class Config:
        from_attributes = True

