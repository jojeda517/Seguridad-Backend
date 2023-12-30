from typing import List, Optional, Generic, TypeVar
from pydantic import BaseModel
from pydantic.generics import GenericModel
from datetime import datetime
from fastapi import UploadFile

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


class UsuarioSchema(BaseModel):
    id: int
    rol_id: int
    facultad_id: int
    carrera_id: int
    nombre: str
    apellido: str
    correo: str
    contrasena: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "id": 1,
                "rol_id": 1,
                "facultad_id": 1,
                "carrera_id": 1,
                "nombre": "Nombre",
                "apellido": "Apellido",
                "correo": "correo@example.com",
                "contrasena": "contrasena"
            }
        }


class UsuarioLoginSechema(BaseModel):
    correo: str
    contrasena: str

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "correo": "test@gmail.com",
                "contrasena": "test"
            }
        }


class DocumentoSchema(BaseModel):
    id: int
    id_categoria: int
    id_usuario: int
    id_estudiante: int
    nombre: str
    fecha: datetime
    descripcion: str

    class Config:
        orm = {
            "example": {
                "id": 1,
                "id_categoria": 1,
                "id_usuario": 1,
                "id_estudiante": 1,
                "nombre": "doc",
                "fecha": "2021-01-24T00:00:00",
                "descripcion": "Archivo creado"
            }
        }


class ResponseSchema(BaseModel):
    code: str
    status: str
    message: str
    result: Optional[T]
