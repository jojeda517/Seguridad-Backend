from sqlalchemy.orm import Session  # La sesión de la DB
from models.models import Facultad  # El modelo ORM de nuestra DB
from schemas.schemas import FacultadSchema  # el esquema del JSON


class FacultadRepository:

    def get_facultades(db: Session, skip: int = 0, limit: int = 1000):
        return db.query(Facultad).offset(skip).limit(limit).all()

    def get_facultad(db: Session, facultad_id: int):
        return db.query(Facultad).filter(Facultad.id == facultad_id).first()

    def create_facultad(db: Session, facultad: FacultadSchema):
        db_facultad = Facultad(
            nombre=facultad.nombre,
            sigla=facultad.sigla,
            logo=facultad.logo
        )
        db.add(db_facultad)
        db.commit()
        db.refresh(db_facultad)
        return db_facultad

    def edit_facultad(db: Session, facultad_id: int, facultad: FacultadSchema):
        _facultad = FacultadRepository.get_facultad(db, facultad_id)
        _facultad.nombre = facultad.nombre
        _facultad.sigla = facultad.sigla
        _facultad.logo = facultad.logo
        db.commit()
        db.refresh(_facultad)
        return _facultad

    def delete_facultad(db: Session, facultad_id: int):
        _facultad = FacultadRepository.get_facultad(db, facultad_id)
        db.delete(_facultad)
        db.commit()
        return _facultad

    def update_file(db: Session, facultad_id: int, file: str):
        db.query(Facultad).filter(Facultad.id ==
                                  facultad_id).update({"logo": file})
        db.commit()
        return db.query(Facultad).filter(Facultad.id == facultad_id).first()
