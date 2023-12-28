from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config.connection import SessionLocal, get_db
from sqlalchemy.orm import Session
from schemas.schemas import CategoriaSchema, ResponseSchema

from repositories.categoria_repository import CategoriaRepository

categoria_router = APIRouter()


@categoria_router.get("/categorias/{carrera_id}")
def get_categorias(carrera_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    return CategoriaRepository.get_categorias(db, carrera_id)


@categoria_router.get("/categoria/{categoria_id}")
def get_categoria(categoria_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_categoria = CategoriaRepository.get_categoria(db, categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    return db_categoria


@categoria_router.post("/categoria/{carrera_id}")
def post_categoria(carrera_id: int = Path(..., gt=0), categoria: CategoriaSchema = None, db: Session = Depends(get_db)):
    db_categoria = CategoriaRepository.post_categorias(
        db, categoria, carrera_id)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Categoria creada exitosamente",
        result=db_categoria
    )


@categoria_router.put("/categoria/{categoria_id}")
def put_categoria(categoria_id: int = Path(..., gt=0), categoria: CategoriaSchema = None, db: Session = Depends(get_db)):
    db_categoria = CategoriaRepository.get_categoria(db, categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    db_categoria = CategoriaRepository.put_categoria(
        db, categoria_id, categoria)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Categoria editada exitosamente",
        result=db_categoria
    )


@categoria_router.delete("/categoria/{categoria_id}/{carrera_id}")
def delete_categoria(categoria_id: int = Path(..., gt=0), carrera_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_categoria = CategoriaRepository.get_categoria(db, categoria_id)
    if db_categoria is None:
        raise HTTPException(status_code=404, detail="Categoria no encontrada")
    db_categoria = CategoriaRepository.delete_categoria(
        db, categoria_id, carrera_id)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Categoria eliminada exitosamente",
        result=db_categoria
    )
