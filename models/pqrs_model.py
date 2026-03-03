from pydantic import BaseModel

class Pqrs(BaseModel):
    id_pqrs: int = None
    radicado: str
    descripcion: str
    fecha_creacion: int
    fecha_limite: int
    id_usuario: int = None
    id_dependencia: int = None
    id_tipospqrs: int = None
    id_estado: int = None
    id_prioridad: int = None