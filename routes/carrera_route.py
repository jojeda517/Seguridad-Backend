from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config.connection import get_db
from sqlalchemy.orm import Session

from repositories.carrera_repository import CarreraRepository
from schemas.schemas import CarreraSchema, ResponseSchema

carrera_router = APIRouter()


@carrera_router.get("/carrera")
def get_carrera(db: Session = Depends(get_db)):
    return CarreraRepository.get_carreras(db)


@carrera_router.get("/carrera/{carrera_id}")
def get_carrera(carrera_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_carrera = CarreraRepository.get_carrera(db, carrera_id)
    if db_carrera is None:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    return db_carrera


@carrera_router.get("/carrera/facultad/{facultad_id}")
def get_carrera_facultad(facultad_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_carrera = CarreraRepository.get_carrera_facultad(db, facultad_id)
    if db_carrera is None:
        raise HTTPException(status_code=404, detail="Carreras no encontrada")
    return db_carrera


@carrera_router.post("/carrera")
def create_carrera(carrera: CarreraSchema, db: Session = Depends(get_db)):
    db_carrera = CarreraRepository.create_carrera(db, carrera)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Carrera creada exitosamente",
        result=db_carrera
    )


@carrera_router.put("/carrera/{carrera_id}")
def edit_carrera(carrera_id: int = Path(..., gt=0), carrera: CarreraSchema = None, db: Session = Depends(get_db)):
    db_carrera = CarreraRepository.get_carrera(db, carrera_id)
    if db_carrera is None:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    db_carrera = CarreraRepository.edit_carrera(db, carrera_id, carrera)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Carrera editada exitosamente",
        result=db_carrera
    )


@carrera_router.delete("/carrera/{carrera_id}")
def delete_carrera(carrera_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_carrera = CarreraRepository.get_carrera(db, carrera_id)
    if db_carrera is None:
        raise HTTPException(status_code=404, detail="Carrera no encontrada")
    db_carrera = CarreraRepository.delete_carrera(db, carrera_id)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Carrera eliminada exitosamente",
        result=db_carrera
    )
