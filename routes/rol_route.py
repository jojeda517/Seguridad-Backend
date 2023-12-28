from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config.connection import get_db
from sqlalchemy.orm import Session

from repositories.rol_repository import RolRepository
from schemas.schemas import RolSchema, ResponseSchema

rol_router = APIRouter()


@rol_router.get("/rol")
def get_rol(db: Session = Depends(get_db)):
    return RolRepository.get_roles(db)


@rol_router.get("/rol/{rol_id}")
def get_rol(rol_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_rol = RolRepository.get_rol(db, rol_id)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    return db_rol


@rol_router.post("/rol")
def create_rol(rol: RolSchema, db: Session = Depends(get_db)):
    db_rol = RolRepository.create_rol(db, rol)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Rol creado exitosamente",
        result=db_rol
    )


@rol_router.put("/rol/{rol_id}")
def edit_rol(rol_id: int = Path(..., gt=0), rol: RolSchema = None, db: Session = Depends(get_db)):
    db_rol = RolRepository.get_rol(db, rol_id)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db_rol = RolRepository.edit_rol(db, rol_id, rol)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Rol editado exitosamente",
        result=db_rol
    )


@rol_router.delete("/rol/{rol_id}")
def delete_rol(rol_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_rol = RolRepository.get_rol(db, rol_id)
    if db_rol is None:
        raise HTTPException(status_code=404, detail="Rol no encontrado")
    db_rol = RolRepository.delete_rol(db, rol_id)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Rol eliminado exitosamente",
        result=db_rol
    )
