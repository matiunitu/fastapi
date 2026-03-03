from pydantic import BaseModel

class Historial(BaseModel):
    id_historial: int = None
    fecha_cambio: int
    id_pqrs: int = None
    id_estado_anterior: int = None
    id_estado_nuevo: int = None
    cambiado_por: str