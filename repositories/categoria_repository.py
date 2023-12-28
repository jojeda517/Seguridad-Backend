from sqlalchemy.orm import Session  # La sesión de la DB
from sqlalchemy import insert, delete, join, select
# El modelo ORM de nuestra DB
from models.models import Categoria, detalle_categoria_carrera
from schemas.schemas import CategoriaSchema  # el esquema del JSON


class CategoriaRepository:

    def get_categorias(db: Session, skip: int = 0, limit: int = 1000):
        return db.query(Categoria).offset(skip).limit(limit).all()

    def get_categorias(db: Session, carrera_id: int, skip: int = 0, limit: int = 1000):
        stmt = (
            select(Categoria)
            .distinct()
            .select_from(join(Categoria, detalle_categoria_carrera,
                              Categoria.id == detalle_categoria_carrera.c.ID_CAT_PER))
            .where(detalle_categoria_carrera.c.ID_CAR_PER == carrera_id)
            .offset(skip)
            .limit(limit)
        )
        results = db.execute(stmt).scalars().all()
        return results

    def get_categoria(db: Session, categoria_id: int):
        return db.query(Categoria).filter(Categoria.id == categoria_id).first()

    def post_categorias(db: Session, categoria: CategoriaSchema, id_carrera: int):
        stmt_existencia = select([Categoria.id]).where(
            Categoria.nombre == categoria.nombre)
        id_categoria_existente = db.execute(stmt_existencia).scalar()
        if id_categoria_existente is None:
            stmt_categoria = insert(Categoria).values(
                NOM_CAT=categoria.nombre,
            )
            result_categoria = db.execute(stmt_categoria)
            db.commit()
            id_categoria = result_categoria.inserted_primary_key[0]
        else:
            id_categoria = id_categoria_existente

        detalle_existente = db.query(detalle_categoria_carrera).filter(
            detalle_categoria_carrera.c.ID_CAT_PER == id_categoria,
            detalle_categoria_carrera.c.ID_CAR_PER == id_carrera
        ).first()
        if not detalle_existente:
            stmt_detalle_cat_car = insert(detalle_categoria_carrera).values(
                ID_CAT_PER=id_categoria,
                ID_CAR_PER=id_carrera
            )
            db.execute(stmt_detalle_cat_car)
            db.commit()

        categoria_creada = db.query(Categoria).filter(
            Categoria.id == id_categoria).first()

        return categoria_creada

    def put_categoria(db: Session, categoria_id: int, categoria: CategoriaSchema):
        _categoria = CategoriaRepository.get_categoria(db, categoria_id)
        _categoria.nombre = categoria.nombre
        db.commit()
        db.refresh(_categoria)
        return _categoria

    def delete_categoria(db: Session, categoria_id: int, carrera_id: int):
        _categoria = CategoriaRepository.get_categoria(db, categoria_id)
        stmt_detalle_cat_car = delete(detalle_categoria_carrera).where(
            (detalle_categoria_carrera.c.ID_CAT_PER == categoria_id) &
            (detalle_categoria_carrera.c.ID_CAR_PER == carrera_id)
        )

        db.execute(stmt_detalle_cat_car)
        db.commit()

        return _categoria
