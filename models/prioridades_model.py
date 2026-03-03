from pydantic import BaseModel

class Prioridades(BaseModel):
    id_prioridad: int = None
    nombre_prioridad: str
    nivel: int