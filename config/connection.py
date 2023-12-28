from dotenv import load_dotenv
import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

load_dotenv()

# Variables de coneccion tomadas del .env
host = os.getenv("AWS_HOST")
user = os.getenv("AWS_USER")
password = os.getenv("AWS_PASSWORD")
database = os.getenv("AWS_DATABASE")
port = os.getenv("AWS_PORT")

# Crecion de la coneccion
engine = create_engine(
    f"mysql+pymysql://{user}:{password}@{host}:{port}/{database}")

# Luego creamos los parametros para las sessiones que se creen de dicho motor
SessionLocal = sessionmaker(autocommit=False,
                            autoflush=False,
                            bind=engine)

# Creamos el mapeador ORM
Base = declarative_base()

# Creamos la función para el uso de session de la DB


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
