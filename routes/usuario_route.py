from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from config.connection import get_db
from sqlalchemy.orm import Session

from repositories.usuario_repository import UsuarioRepository
from schemas.schemas import UsuarioSchema, ResponseSchema, UsuarioLoginSechema

usuario_router = APIRouter()


@usuario_router.get("/usuario")
def get_usuario(db: Session = Depends(get_db)):
    return UsuarioRepository.get_usuarios(db)


@usuario_router.get("/usuario/{usuario_id}")
def get_usuario(usuario_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_usuario = UsuarioRepository.get_usuario(db, usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario


@usuario_router.post("/usuario/login")
def login(usuario: UsuarioLoginSechema, db: Session = Depends(get_db)):
    db_usuario = UsuarioRepository.login(db, usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario


@usuario_router.post("/usuario/login/microsoft")
def login_microsoft(usuario: UsuarioLoginSechema, db: Session = Depends(get_db)):
    db_usuario = UsuarioRepository.login_microsoft(db, usuario)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    return db_usuario


@usuario_router.post("/usuario")
def create_usuario(usuario: UsuarioSchema, db: Session = Depends(get_db)):
    db_usuario = UsuarioRepository.create_usuario(db, usuario)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Usuario creado exitosamente",
        result=db_usuario
    )


@usuario_router.put("/usuario/{usuario_id}")
def edit_usuario(usuario_id: int = Path(..., gt=0), usuario: UsuarioSchema = None, db: Session = Depends(get_db)):
    db_usuario = UsuarioRepository.get_usuario(db, usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_usuario = UsuarioRepository.edit_usuario(db, usuario_id, usuario)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Usuario editado exitosamente",
        result=db_usuario
    )


@usuario_router.delete("/usuario/{usuario_id}")
def delete_usuario(usuario_id: int = Path(..., gt=0), db: Session = Depends(get_db)):
    db_usuario = UsuarioRepository.get_usuario(db, usuario_id)
    if db_usuario is None:
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
    db_usuario = UsuarioRepository.delete_usuario(db, usuario_id)
    return ResponseSchema(
        code="OK",
        status="success",
        message="Usuario eliminado exitosamente",
        result=db_usuario
    )
