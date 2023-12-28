from sqlalchemy import Column, Integer, String
from config.connection import Base

class Facultad(Base):
    __tablename__ = "FACULTAD"
    
    id = Column('ID_FAC', Integer, primary_key=True)
    nombre = Column('NOM_FAC', String(50))
    sigla = Column('SIG_FAC', String(10))
    logo = Column('LOG_FAC', String(100))
