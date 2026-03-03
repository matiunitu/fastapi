from pydantic import BaseModel

class Roles(BaseModel):
    id_rol: int = None
    nombre_rol: str
    descripcion: str