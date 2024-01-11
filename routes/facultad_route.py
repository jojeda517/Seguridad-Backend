from fastapi import APIRouter, HTTPException, Path, UploadFile, File, Depends
from fastapi.responses import FileResponse
from fastapi import Depends
from config.connection import get_db
from sqlalchemy.orm import Session
from schemas.schemas import FacultadSchema, ResponseSchema
from models.models import Facultad
import os

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


@facultad_router.post("/logo/{facultad_id}")
def upload_file(file: UploadFile = File(...), facultad_id: int = 0, db: Session = Depends(get_db)):
    # Directorio principal
    directorio_base = "Documents"
    os.makedirs(directorio_base, exist_ok=True)
    extension = os.path.splitext(file.filename)[1]

    datos_facultad = db.query(Facultad).filter(
        Facultad.id == facultad_id).first()

    # Construir la estructura de carpetas
    folder_structure = f"{datos_facultad.nombre}"

    # Directorio completo
    directorio_completo = os.path.join(directorio_base, folder_structure)

    # Crea la estructura de carpetas si no existen
    os.makedirs(directorio_completo, exist_ok=True)

    # Ruta donde se almacenará el documento
    file_path = os.path.join(
        directorio_completo, datos_facultad.nombre+extension)

    # Guardar el archivo en la ruta especificada
    with open(file_path, "wb") as image:
        image.write(file.file.read())

    # Actualizar la ruta del archivo en la base de datos
    db_documento = FacultadRepository.update_file(
        db=db, facultad_id=facultad_id, file=file_path)

    print(db_documento)
    return db_documento


@facultad_router.get("/logo/{facultad_id}")
async def get_logo(facultad_id: str, db: Session = Depends(get_db)):
    db_documento = FacultadRepository.get_facultad(db, facultad_id)
    directorio = db_documento.logo
    file_path = os.path.join(directorio)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return file_path
