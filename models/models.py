from sqlalchemy import Column, Integer, String, Table, ForeignKey, DateTime
from config.connection import Base
from datetime import datetime
import pytz

metadata = Base.metadata


class Facultad(Base):
    __tablename__ = "FACULTAD"

    id = Column('ID_FAC', Integer, primary_key=True)
    nombre = Column('NOM_FAC', String(50))
    sigla = Column('SIG_FAC', String(10))
    logo = Column('LOG_FAC', String(100))


class Estudiante(Base):
    __tablename__ = "ESTUDIANTE"

    id = Column('ID_EST', Integer, primary_key=True, autoincrement=True)
    cedula = Column('CED_EST', String(10), unique=True, nullable=False)
    nombre = Column('NOM_EST', String(255), nullable=False)
    apellido = Column('APE_EST', String(255), nullable=False)
    direccion = Column('DIR_EST', String(255))
    celular = Column('CEL_EST', String(10))
    correo = Column('COR_EST', String(255), unique=True, nullable=False)


class Carrera(Base):
    __tablename__ = "CARRERA"

    id = Column('ID_CAR', Integer, primary_key=True, autoincrement=True)
    facultad_id = Column('ID_FAC_PER', Integer)
    nombre = Column('NOM_CAR', String(255), unique=True, nullable=False)
    sigla = Column('SIG_CAR', String(255), unique=True, nullable=False)


class Rol(Base):
    __tablename__ = "ROL"

    id = Column('ID_ROL', Integer, primary_key=True, autoincrement=True)
    nombre = Column('NOM_ROL', String(255), unique=True, nullable=False)


class Categoria(Base):
    __tablename__ = "CATEGORIA"

    id = Column('ID_CAT', Integer, primary_key=True)
    nombre = Column('NOM_CAT', String(255))


class Documento(Base):
    __tablename__ = "DOCUMENTO"

    id = Column('ID_DOC', Integer, primary_key=True)
    id_categoria = Column('ID_CAT_PER', Integer,
                          ForeignKey('CATEGORIA.ID_CAT'))
    id_usuario = Column('ID_USU_PER', Integer)
    id_estudiante = Column('ID_EST_PER', Integer)
    nombre = Column('NOM_DOC', String(255))
    fecha = Column('FEC_DOC', DateTime, default=datetime.now(
        pytz.timezone('America/Guayaquil')))
    descripcion = Column('DES_DOC', String)
    url = Column('URL_DOC', String(255))


detalle_categoria_carrera = Table(
    'DETALLE_CAT_CAR', metadata,
    Column('ID_CAR_PER', Integer, ForeignKey('CARRERA.ID_CAR')),
    Column('ID_CAT_PER', Integer, ForeignKey('CATEGORIA.ID_CAT')),
)

detalle_estudiante_carrera = Table(
    'DETALLE_EST_CAR', metadata,
    Column('ID_CAR_PER', Integer, ForeignKey('CARRERA.ID_CAR')),
    Column('ID_EST_PER', Integer, ForeignKey('ESTUDIANTE.ID_EST'))
)
