from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config.connection import SessionLocal, get_db
from sqlalchemy.orm import Session
from schemas.schemas import FacultadSchema, ResponseSchema

from repositories.facultad_repository import FacultadRepository

facultad_router = APIRouter()


@facultad_router.get("/facultad")
def get_facultad(db: Session = Depends(get_db)):
    return FacultadRepository.get_facultades(db)


@facultad_router.get("/facultad/{facultad_id}")
def get_facultad(facultad_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_facultad = FacultadRepository.get_facultad(db, facultad_id)
    if db_facultad is None:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    return db_facultad


@facultad_router.post("/facultad")
def create_facultad(facultad: FacultadSchema, db: Session = Depends(get_db)):
    db_facultad = FacultadRepository.create_facultad(db, facultad)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Facultad creada exitosamente",
        result=db_facultad
    )


@facultad_router.put("/facultad/{facultad_id}")
def edit_facultad(facultad_id: int = Path(..., gt=0), facultad: FacultadSchema = None, db: Session = Depends(get_db)):
    db_facultad = FacultadRepository.get_facultad(db, facultad_id)
    if db_facultad is None:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    db_facultad = FacultadRepository.edit_facultad(db, facultad_id, facultad)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Facultad editada exitosamente",
        result=db_facultad
    )


@facultad_router.delete("/facultad/{facultad_id}")
def delete_facultad(facultad_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_facultad = FacultadRepository.get_facultad(db, facultad_id)
    if db_facultad is None:
        raise HTTPException(status_code=404, detail="Facultad no encontrada")
    db_facultad = FacultadRepository.delete_facultad(db, facultad_id)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Facultad eliminada exitosamente",
        result=db_facultad
    )
