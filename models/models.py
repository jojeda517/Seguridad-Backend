from sqlalchemy import Column, Integer, String
from config.connection import Base


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

