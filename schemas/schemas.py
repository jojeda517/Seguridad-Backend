from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

# creamos un tipo de variable "cualquiera"
T = TypeVar("T")


class FacultadSchema(BaseModel):
    id: int
    nombre: str
    sigla: str
    logo: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Facultad de Ingenieria",
                "sigla": "FI",
                "logo": "ruta/al/logo.png"
            }
        }


class CategoriaSchema(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Nivelacion"
            }
        }


class ResponseSchema(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T]
