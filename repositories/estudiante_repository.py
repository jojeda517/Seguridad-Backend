from sqlalchemy.orm import Session  # La sesión de la DB
from sqlalchemy import insert, select, join, delete, distinct
# El modelo ORM de nuestra DB
from models.models import Estudiante, detalle_estudiante_carrera
from schemas.schemas import EstudianteSchema  # el esquema del JSON


class EstudianteRepository:
    def get_estudiantes(db: Session, carrera_id: int, skip: int = 0, limit: int = 1000):
        stmt = (
            select(Estudiante)
            .distinct()
            .select_from(join(Estudiante, detalle_estudiante_carrera,
                              Estudiante.id == detalle_estudiante_carrera.c.ID_EST_PER))
            .where(detalle_estudiante_carrera.c.ID_CAR_PER == carrera_id)
            .offset(skip)
            .limit(limit)
        )
        results = db.execute(stmt).scalars().all()

        return results

    def get_all_estudiantes(db: Session, skip: int = 0, limit: int = 1000):
        return db.query(Estudiante).offset(skip).limit(limit).all()

    def get_estudiante(db: Session, estudiante_id: int):
        return db.query(Estudiante).filter(Estudiante.id == estudiante_id).first()

    def get_estudiante_by_cedula(db: Session, cedula: str):
        return db.query(Estudiante).filter(Estudiante.cedula == cedula).first()

    def create_estudiante(db: Session, estudiante: EstudianteSchema, id_carrera: int):
        stmt_existencia = select([Estudiante.id]).where(
            Estudiante.cedula == estudiante.cedula)
        id_estudiante_existente = db.execute(stmt_existencia).scalar()

        if id_estudiante_existente is None:
            stmt_estudiante = insert(Estudiante).values(
                CED_EST=estudiante.cedula,
                NOM_EST=estudiante.nombre,
                APE_EST=estudiante.apellido,
                DIR_EST=estudiante.direccion,
                CEL_EST=estudiante.celular,
                COR_EST=estudiante.correo
            )

            result_estudiante = db.execute(stmt_estudiante)
            db.commit()
            id_estudiante = result_estudiante.inserted_primary_key[0]
        else:
            id_estudiante = id_estudiante_existente

        detalle_existente = db.query(detalle_estudiante_carrera).filter(
            detalle_estudiante_carrera.c.ID_EST_PER == id_estudiante,
            detalle_estudiante_carrera.c.ID_CAR_PER == id_carrera
        ).first()
        if not detalle_existente:
            stmt_detalle_est_car = insert(detalle_estudiante_carrera).values(
                ID_EST_PER=id_estudiante,
                ID_CAR_PER=id_carrera
            )
            db.execute(stmt_detalle_est_car)
            db.commit()

        estudiante_creado = db.query(Estudiante).filter(
            Estudiante.id == id_estudiante).first()

        return estudiante_creado

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

    def delete_estudiante(db: Session, estudiante_id: int, carrera_id: int):
        _estudiante = EstudianteRepository.get_estudiante(db, estudiante_id)
        stmt_detalle_cat_car = delete(detalle_estudiante_carrera).where(
            (detalle_estudiante_carrera.c.ID_EST_PER == estudiante_id) &
            (detalle_estudiante_carrera.c.ID_CAR_PER == carrera_id)
        )
        db.execute(stmt_detalle_cat_car)
        db.commit()
        return _estudiante
