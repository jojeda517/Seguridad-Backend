from sqlalchemy.orm import Session  # La sesión de la DB
from models.models import Usuario  # El modelo ORM de nuestra DB
from schemas.schemas import UsuarioSchema  # el esquema del JSON


class UsuarioRepository:
    def get_usuarios(db: Session, skip: int = 0, limit: int = 1000):
        return db.query(Usuario).offset(skip).limit(limit).all()

    def get_usuario(db: Session, usuario_id: int):
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def login(db: Session, usuario: UsuarioSchema):
        return db.query(Usuario).filter(Usuario.correo == usuario.correo, Usuario.contrasena == usuario.contrasena).first()

    def create_usuario(db: Session, usuario: UsuarioSchema):
        db_usuario = Usuario(
            rol_id=usuario.rol_id,
            facultad_id=usuario.facultad_id,
            carrera_id=usuario.carrera_id,
            nombre=usuario.nombre,
            apellido=usuario.apellido,
            correo=usuario.correo,
            contrasena=usuario.contrasena
        )
        db.add(db_usuario)
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    def edit_usuario(db: Session, usuario_id: int, usuario: UsuarioSchema):
        db_usuario = UsuarioRepository.get_usuario(db, usuario_id)
        db_usuario.rol_id = usuario.rol_id
        db_usuario.facultad_id = usuario.facultad_id
        db_usuario.carrera_id = usuario.carrera_id
        db_usuario.nombre = usuario.nombre
        db_usuario.apellido = usuario.apellido
        db_usuario.correo = usuario.correo
        db_usuario.contrasena = usuario.contrasena
        db.commit()
        db.refresh(db_usuario)
        return db_usuario

    def delete_usuario(db: Session, usuario_id: int):
        db_usuario = UsuarioRepository.get_usuario(db, usuario_id)
        db.delete(db_usuario)
        db.commit()
        return db_usuario
