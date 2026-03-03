from pydantic import BaseModel

class Usuarios(BaseModel):
    id_usuario: int = None
    nombre: str
    documento: str
    correo: str
    telefono: int
    id_rol: int = None
    id_programa: int = None
    activo: str
    created_at: str