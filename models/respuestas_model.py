from pydantic import BaseModel

class Respuestas(BaseModel):
    id_respuesta: int = None
    mensaje: str
    fecha_respuesta: int
    id_pqrs: int = None
    id_usuario: int = None