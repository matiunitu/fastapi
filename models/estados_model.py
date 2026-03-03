from pydantic import BaseModel

class Estados(BaseModel):
    id_estado: int = None
    nombre_estado: str