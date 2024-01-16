from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config.connection import get_db
from sqlalchemy.orm import Session

from repositories.estudiante_repository import EstudianteRepository
from schemas.schemas import EstudianteSchema, ResponseSchema


estudiante_router = APIRouter()


@estudiante_router.get("/estudiantes")
def get_estudiantes(skip: int = 0, limit: int = 1000, db: Session = Depends(get_db)):
    return EstudianteRepository.get_all_estudiantes(db, skip, limit)


@estudiante_router.get("/estudiantes/{carrera_id}")
def get_estudiante(carrera_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    return EstudianteRepository.get_estudiantes(db, carrera_id)


@estudiante_router.get("/estudiante/{estudiante_id}")
def get_estudiante(estudiante_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_estudiante = EstudianteRepository.get_estudiante(db, estudiante_id)
    if db_estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return db_estudiante


@estudiante_router.post("/estudiante/{carrera_id}")
def create_estudiante(carrera_id: int = Path(..., gt=0), estudiante: EstudianteSchema = None, db: Session = Depends(get_db)):
    db_estudiante = EstudianteRepository.create_estudiante(
        db, estudiante, carrera_id)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Estudiante creado exitosamente",
        result=db_estudiante
    )


@estudiante_router.put("/estudiante/{estudiante_id}")
def edit_estudiante(estudiante_id: int = Path(..., gt=0), estudiante: EstudianteSchema = None, db: Session = Depends(get_db)):
    db_estudiante = EstudianteRepository.get_estudiante(db, estudiante_id)
    if db_estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")

    db_estudiante = EstudianteRepository.edit_estudiante(
        db, estudiante_id, estudiante)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Estudiante editado exitosamente",
        result=db_estudiante
    )


@estudiante_router.delete("/estudiante/{estudiante_id}/{carrera_id}")
def delete_estudiante(estudiante_id: int = Path(..., gt=0), carrera_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_estudiante = EstudianteRepository.get_estudiante(db, estudiante_id)
    if db_estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    db_estudiante = EstudianteRepository.delete_estudiante(
        db, estudiante_id, carrera_id)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Estudiante eliminado exitosamente",
        result=db_estudiante
    )
