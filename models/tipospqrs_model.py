from pydantic import BaseModel

class Tipospqrs(BaseModel):
    id_tipospqrs: int = None
    nombre_tipospqrs: str
    descripcion: str