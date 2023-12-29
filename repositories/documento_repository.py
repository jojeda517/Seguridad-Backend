from sqlalchemy.orm import Session  # La sesión de la DB
from sqlalchemy import func
# El modelo ORM de nuestra DB
from models.models import Documento
from schemas.schemas import DocumentoSchema  # el esquema del JSON
from datetime import datetime
import pytz


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
