from sqlalchemy import Column, Integer, String, Table, ForeignKey
from config.connection import Base

metadata = Base.metadata


class Facultad(Base):
    __tablename__ = "FACULTAD"

    id = Column('ID_FAC', Integer, primary_key=True)
    nombre = Column('NOM_FAC', String(50))
    sigla = Column('SIG_FAC', String(10))
    logo = Column('LOG_FAC', String(100))


class Categoria(Base):
    __tablename__ = "CATEGORIA"

    id = Column('ID_CAT', Integer, primary_key=True)
    nombre = Column('NOM_CAT', String(255))


detalle_categoria_carrera = Table(
    'DETALLE_CAT_CAR', metadata,
    Column('ID_CAR_PER', Integer, ForeignKey('CARRERA.ID_CAR')),
    Column('ID_CAT_PER', Integer, ForeignKey('CATEGORIA.ID_CAT')),
)
