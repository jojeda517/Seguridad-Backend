from fastapi import APIRouter, HTTPException, Path, UploadFile, File, Depends
from fastapi.responses import FileResponse
from config.connection import get_db
from sqlalchemy.orm import Session
from schemas.schemas import DocumentoSchema, ResponseSchema
from repositories.documento_repository import DocumentoRepository
from models.models import Documento, Estudiante, Carrera, Facultad, Categoria, Usuario
import os

documento_router = APIRouter()


@documento_router.get("/documento/{estudiante_id}/{categoria_id}")
def get_documentos(estudiante_id: int = Path(..., gt=0), categoria_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_documento = DocumentoRepository.get_documentos(
        db, estudiante_id, categoria_id)
    if db_documento is None:
        raise HTTPException(
            status_code=404, detail="El estudiante no tiene Documentos")
    return db_documento


@documento_router.get("/documento/{documento_id}")
def get_documento(documento_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_documento = DocumentoRepository.get_documento(db, documento_id)
    if db_documento is None:
        raise HTTPException(
            status_code=404, detail="ENo se encontro el documento")
    return db_documento


@documento_router.post("/documento/{usuario_id}/{categoria_id}/{estudiante_id}")
def create_documento(usuario_id: int = Path(..., gt=0), categoria_id: int = Path(..., gt=0), estudiante_id: int = Path(..., gt=0), documento: DocumentoSchema = None, db: Session = Depends(get_db)):

    db_documento = DocumentoRepository.post_documento(
        db, documento, usuario_id, categoria_id, estudiante_id)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Documento creado exitosamente",
        result=db_documento
    )


@documento_router.put("/documento/{documento_id}/{usuario_id}")
def edit_documento(documento_id: int = Path(..., gt=0), usuario_id: int = Path(..., gt=0), documento: DocumentoSchema = None, db: Session = Depends(get_db)):
    db_documento = DocumentoRepository.get_documento(db, documento_id)
    if db_documento is None:
        raise HTTPException(status_code=404, detail="Documento no encontrada")
    db_documento = DocumentoRepository.put_documento(
        db, documento_id, usuario_id, documento)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Documento editada exitosamente",
        result=db_documento
    )


@documento_router.delete("/documento/{documento_id}")
def delete_documento(documento_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_documento = DocumentoRepository.get_documento(db, documento_id)
    if db_documento is None:
        raise HTTPException(status_code=404, detail="Documento no encontrada")
    db_documento = DocumentoRepository.delete_documento(db, documento_id)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Documento eliminada exitosamente",
        result=db_documento
    )


@documento_router.post("/archivo/{documento_id}")
def upload_file(file: UploadFile = File(...), documento_id: int = 0, db: Session = Depends(get_db)):
    # Directorio principal
    directorio_base = "Documents"
    os.makedirs(directorio_base, exist_ok=True)
    extension = os.path.splitext(file.filename)[1]

    datos_documento = db.query(Documento).filter(
        Documento.id == documento_id).first()
    datos_usuario = db.query(Usuario).filter(
        Usuario.id == datos_documento.id_usuario).first()
    datos_facultad = db.query(Facultad).filter(
        Facultad.id == datos_usuario.facultad_id).first()
    datos_carrera = db.query(Carrera).filter(
        Carrera.id == datos_usuario.carrera_id).first()
    datos_estudiante = db.query(Estudiante).filter(
        Estudiante.id == datos_documento.id_estudiante).first()
    datos_categoria = db.query(Categoria).filter(
        Categoria.id == datos_documento.id_categoria).first()

    # Construir la estructura de carpetas
    folder_structure = f"{datos_facultad.nombre}/{datos_carrera.nombre}/{datos_estudiante.nombre}_{datos_estudiante.apellido}/{datos_categoria.nombre}"

    # Directorio completo
    directorio_completo = os.path.join(directorio_base, folder_structure)

    # Crea la estructura de carpetas si no existen
    os.makedirs(directorio_completo, exist_ok=True)

    # Ruta donde se almacenará el documento
    file_path = os.path.join(
        directorio_completo, datos_documento.nombre+extension)

    # Guardar el archivo en la ruta especificada
    with open(file_path, "wb") as image:
        image.write(file.file.read())

    # Actualizar la ruta del archivo en la base de datos
    db_documento = DocumentoRepository.update_file(
        db=db, documento_id=documento_id, file=file_path)

    print(db_documento)
    return db_documento


@documento_router.get("/archivo/{document_id}")
async def get_document(document_id: str, db: Session = Depends(get_db)):
    db_documento = DocumentoRepository.get_documento(db, document_id)
    directorio = db_documento.url
    file_path = os.path.join(directorio)
    if os.path.exists(file_path):
        return FileResponse(file_path)
    else:
        return file_path
