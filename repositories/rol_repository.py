from sqlalchemy.orm import Session  # La sesión de la DB
from models.models import Rol  # El modelo ORM de nuestra DB
from schemas.schemas import RolSchema  # el esquema del JSON


class RolRepository:
    def get_roles(db: Session, skip: int = 0, limit: int = 1000):
        return db.query(Rol).offset(skip).limit(limit).all()

    def get_rol(db: Session, rol_id: int):
        return db.query(Rol).filter(Rol.id == rol_id).first()

    def create_rol(db: Session, rol: RolSchema):
        db_rol = Rol(
            nombre=rol.nombre
        )
        db.add(db_rol)
        db.commit()
        db.refresh(db_rol)
        return db_rol

    def edit_rol(db: Session, rol_id: int, rol: RolSchema):
        _rol = RolRepository.get_rol(db, rol_id)
        _rol.nombre = rol.nombre
        db.commit()
        db.refresh(_rol)
        return _rol

    def delete_rol(db: Session, rol_id: int):
        _rol = RolRepository.get_rol(db, rol_id)
        db.delete(_rol)
        db.commit()
        return _rol
