from pydantic import BaseModel

class Programas(BaseModel):
    id_programa: int = None
    nombre_programa: str
    descripcion: str