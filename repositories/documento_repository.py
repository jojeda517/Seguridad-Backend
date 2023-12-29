from sqlalchemy.orm import Session  # La sesión de la DB
from sqlalchemy import func
# El modelo ORM de nuestra DB
from models.models import Documento
from schemas.schemas import DocumentoSchema  # el esquema del JSON
from datetime import datetime
import pytz
import os


class DocumentoRepository:
    def get_documentos(db: Session, estudiante_id: int, categoria_id: int):
        return db.query(Documento).filter(Documento.id_estudiante == estudiante_id, Documento.id_categoria == categoria_id).all()

    def get_documento(db: Session, documento_id: int):
        return db.query(Documento).filter(Documento.id == documento_id).first()

    def post_documento(db: Session, documento: DocumentoSchema, usuario_id: int, categoria_id: int, estudiante_id: int):

        db_documento = Documento(
            id_categoria=categoria_id,
            id_usuario=usuario_id,
            id_estudiante=estudiante_id,
            nombre=documento.nombre,
            fecha=documento.fecha,
            descripcion=documento.descripcion
        )

        db.add(db_documento)
        db.commit()
        db.refresh(db_documento)

        return db_documento

    def put_documento(db: Session, documento_id: int, usuario_id: int, documento: DocumentoSchema):
        _documento = DocumentoRepository.get_documento(db, documento_id)
        _documento.id_usuario = usuario_id
        _documento.nombre = documento.nombre
        _documento.fecha = datetime.now(pytz.timezone('America/Guayaquil'))
        _documento.descripcion = documento.descripcion
        db.commit()
        db.refresh(_documento)
        url = (db.query(Documento).filter(
            Documento.id == documento_id).first()).url
        # Verificar si hay un parámetro de carpeta en la URL
        if url:
            # Obtener la carpeta de la URL y la extensión del archivo existente
            folder_path, old_file_name = os.path.split(url)
            _, old_file_extension = os.path.splitext(old_file_name)

            # Construir la nueva ruta del archivo con la misma extensión
            new_file_path = os.path.join(
                folder_path, f"{documento.nombre}{old_file_extension}")

            # Renombrar el archivo en el servidor
            os.rename(url, new_file_path)

            # Actualizar la ruta del archivo en la base de datos
            _documento.url = new_file_path
            db.commit()
            db.refresh(_documento)

        return _documento

    def delete_documento(db: Session, documento_id: int):
        _documento = DocumentoRepository.get_documento(db, documento_id)
        db.delete(_documento)
        db.commit()
        return _documento

    def update_file(db: Session, documento_id: int, file: str):
        db.query(Documento).filter(Documento.id ==
                                   documento_id).update({"url": file})
        db.commit()
        return db.query(Documento).filter(Documento.id == documento_id).first()
