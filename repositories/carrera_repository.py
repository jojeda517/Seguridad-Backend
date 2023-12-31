from sqlalchemy.orm import Session  # La sesión de la DB
from models.models import Carrera  # El modelo ORM de nuestra DB
from schemas.schemas import CarreraSchema  # el esquema del JSON


class CarreraRepository:
    def get_carreras(db: Session, skip: int = 0, limit: int = 1000):
        return db.query(Carrera).offset(skip).limit(limit).all()

    def get_carrera(db: Session, carrera_id: int):
        return db.query(Carrera).filter(Carrera.id == carrera_id).first()

    def get_carrera_facultad(db: Session, facultad_id: int):
        return db.query(Carrera).filter(Carrera.facultad_id == facultad_id).all()

    def create_carrera(db: Session, carrera: CarreraSchema):
        db_carrera = Carrera(
            facultad_id=carrera.facultad_id,
            nombre=carrera.nombre,
            sigla=carrera.sigla
        )
        db.add(db_carrera)
        db.commit()
        db.refresh(db_carrera)
        return db_carrera

    def edit_carrera(db: Session, carrera_id: int, carrera: CarreraSchema):
        _carrera = CarreraRepository.get_carrera(db, carrera_id)
        _carrera.facultad_id = carrera.facultad_id
        _carrera.nombre = carrera.nombre
        _carrera.sigla = carrera.sigla
        db.commit()
        db.refresh(_carrera)
        return _carrera

    def delete_carrera(db: Session, carrera_id: int):
        _carrera = CarreraRepository.get_carrera(db, carrera_id)
        db.delete(_carrera)
        db.commit()
        return _carrera
