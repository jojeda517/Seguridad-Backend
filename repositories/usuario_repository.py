from sqlalchemy.orm import Session  # La sesión de la DB
from models.models import Usuario  # El modelo ORM de nuestra DB
from schemas.schemas import UsuarioSchema, UsuarioLoginSechema  # el esquema del JSON


class UsuarioRepository:
    def get_usuarios(db: Session, skip: int = 0, limit: int = 1000):
        return db.query(Usuario).offset(skip).limit(limit).all()

    def get_usuario(db: Session, usuario_id: int):
        return db.query(Usuario).filter(Usuario.id == usuario_id).first()

    def get_usuario_por_rol(db: Session, rol_id: int):
        return db.query(Usuario).filter(Usuario.rol_id == rol_id).all()

    def login(db: Session, usuario: UsuarioLoginSechema):
        return db.query(Usuario).filter(Usuario.correo == usuario.correo).first()

    def login_microsoft(db: Session, usuario: UsuarioLoginSechema):
        _usuario = db.query(Usuario).filter(
            Usuario.correo == usuario.correo).first()
        if _usuario is None:
            return None
        else:
            return _usuario.rol_id

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
