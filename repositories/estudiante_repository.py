from sqlalchemy.orm import Session  # La sesión de la DB
from models.models import Estudiante  # El modelo ORM de nuestra DB
from schemas.schemas import EstudianteSchema  # el esquema del JSON


class EstudianteRepository:
    def get_estudiantes(db: Session, skip: int = 0, limit: int = 1000):
        return db.query(Estudiante).offset(skip).limit(limit).all()

    def get_estudiante(db: Session, estudiante_id: int):
        return db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()

    def get_estudiante_by_cedula(db: Session, cedula: str):
        return db.query(Estudiante).filter(Estudiante.cedula == cedula).first()

    def create_estudiante(db: Session, estudiante: EstudianteSchema):
        db_estudiante = Estudiante(
            cedula=estudiante.cedula,
            nombre=estudiante.nombre,
            apellido=estudiante.apellido,
            direccion=estudiante.direccion,
            celular=estudiante.celular,
            correo=estudiante.correo
        )
        db.add(db_estudiante)
        db.commit()
        db.refresh(db_estudiante)
        return db_estudiante

    def edit_estudiante(db: Session, estudiante_id: int, estudiante: EstudianteSchema):
        _estudiante = EstudianteRepository.get_estudiante(db, estudiante_id)
        _estudiante.cedula = estudiante.cedula
        _estudiante.nombre = estudiante.nombre
        _estudiante.apellido = estudiante.apellido
        _estudiante.direccion = estudiante.direccion
        _estudiante.celular = estudiante.celular
        _estudiante.correo = estudiante.correo
        db.commit()
        db.refresh(_estudiante)
        return _estudiante

    def delete_estudiante(db: Session, estudiante_id: int):
        _estudiante = EstudianteRepository.get_estudiante(db, estudiante_id)
        db.delete(_estudiante)
        db.commit()
        return _estudiante
