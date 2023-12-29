from fastapi import APIRouter, HTTPException, Path, UploadFile, File, Body
from fastapi import Depends
from config.connection import SessionLocal, get_db
from sqlalchemy.orm import Session
from sqlalchemy import select
from schemas.schemas import DocumentoSchema, ResponseSchema
from repositories.documento_repository import DocumentoRepository
from models.models import Documento, Estudiante, Carrera, Facultad, Categoria
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

""" @documento_router.post("/archivo/{documento_id}")
def upload_file(file:UploadFile=File(...), documento_id:int=0, db:Session=Depends(get_db)):
    #Directorio  principal
    directorio="Documents"
    os.makedirs(directorio, exist_ok=True)
    extension=os.path.splitext(file.filename)[1]
    # Crea la ruta donde se almacenarán los documentos
    file_path = os.path.join(directorio, file.filename)
    with open(file_path, "wb") as image:
        image.write(file.file.read())
    file_path = f"facultad/carrera/estudiante/categoria{file.filename}"
    db_documento=DocumentoRepository.update_file(db=db, documento_id=documento_id, file=file_path)
    print(db_documento)
    return db_documento

@documento_router.post("/archivo2/{documento_id}")
def upload_file2(file: UploadFile = File(...), documento_id: int = 0, db: Session = Depends(get_db)):
    # Directorio principal
    directorio = "Documents"
    os.makedirs(directorio, exist_ok=True)
    extension = os.path.splitext(file.filename)[1]

    datos_documento=db.query(Documento).filter(Documento.id==documento_id).first()
    datos_usuario=db.query(Usuario).filter(Usuario.id==datos_documento.id).first()
    datos_facultad=db.query(Facultad).filter(Facultad.id==datos_usuario.id_facultad).first()
    datos_carrera=db.query(Carrera).filter(Carrera.id==datos_usuario.id_carrra).first()
    datos_estudiante=db.query(Estudiante).filter(Estudiante.id==datos_documento.id_estudiante).first()
    datos_categoria=db.query(Categoria).filter(Categoria.id==datos_documento.id_categoria).first()
    
    # Crea la ruta donde se almacenarán los documentos
    file_path = os.path.join(directorio, file.filename)
    with open(file_path, "wb") as image:
        image.write(file.file.read())

    # Construir la estructura de carpetas
    folder_structure = f"{datos_facultad['NOM_FAC']}/{datos_carrera['NOM_CAR']}/{datos_estudiante['NOM_EST']}_{datos_estudiante['APE_EST']}/{datos_categoria['ID_CAT']}"

    # Actualizar la ruta del archivo en la base de datos
    file_path = os.path.join(folder_structure, file.filename)
    db_documento = DocumentoRepository.update_file(db=db, documento_id=documento_id, file=file_path)

    print(db_documento)
    return db_documento """