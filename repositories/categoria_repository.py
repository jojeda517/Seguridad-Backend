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
        stmt_categoria = insert(Categoria).values(
            NOM_CAT=categoria.nombre
        )

        result_categoria = db.execute(stmt_categoria)
        db.commit()

        id_categoria = result_categoria.inserted_primary_key[0]
        stmt_detalle_cat_car = insert(detalle_categoria_carrera).values(
            ID_CAT_PER=id_categoria,
            ID_CAR_PER=id_carrera
        )

        db.execute(stmt_detalle_cat_car)
        db.commit()

        return result_categoria

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
        db.delete(_categoria)
        db.commit()

        return _categoria
