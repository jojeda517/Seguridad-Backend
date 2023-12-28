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
        
        
class EstudianteSchema(BaseModel):
    id: int
    cedula: str
    nombre: str
    apellido: str
    direccion: str = None
    celular: str = None
    correo: str
      

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "cedula": "1234567890",
                "nombre": "Juan",
                "apellido": "Perez",
                "direccion": "Calle 123",
                "celular": "1234567890",
                "correo": "juan@example.com"
            }
        }


class CarreraSchema(BaseModel):
    id: int
    facultad_id: int
    nombre: str
    sigla: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "facultad_id": 1,
                "nombre": "Ingeniería en Informática",
                "sigla": "Ing. Informática"
            }
        }


class RolSchema(BaseModel):
    id: int
    nombre: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "nombre": "Estudiante"
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
