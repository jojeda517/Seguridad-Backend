from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config.connection import get_db
from sqlalchemy.orm import Session

from repositories.estudiante_repository import EstudianteRepository
from schemas.schemas import EstudianteSchema, ResponseSchema

estudiante_router = APIRouter()


@estudiante_router.get("/estudiante")
def get_estudiante(db: Session = Depends(get_db)):
    return EstudianteRepository.get_estudiantes(db)


@estudiante_router.get("/estudiante/{estudiante_id}")
def get_estudiante(estudiante_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_estudiante = EstudianteRepository.get_estudiante(db, estudiante_id)
    if db_estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    return db_estudiante


@estudiante_router.post("/estudiante")
def create_estudiante(estudiante: EstudianteSchema, db: Session = Depends(get_db)):
    db_estudiante = EstudianteRepository.create_estudiante(db, estudiante)
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


@estudiante_router.delete("/estudiante/{estudiante_id}")
def delete_estudiante(estudiante_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_estudiante = EstudianteRepository.get_estudiante(db, estudiante_id)
    if db_estudiante is None:
        raise HTTPException(status_code=404, detail="Estudiante no encontrado")
    db_estudiante = EstudianteRepository.delete_estudiante(db, estudiante_id)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Estudiante eliminado exitosamente",
        result=db_estudiante
    )
