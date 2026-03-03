from pydantic import BaseModel

class Dependencias(BaseModel):
    id_dependencia: int
    nombre_dependencia: str
    descripcion: str