from fastapi import APIRouter, HTTPException, Path, UploadFile, File
from fastapi import Depends
from sqlalchemy.orm import sessionmaker
from config.connection import engine

import pandas as pd

from models.models import Estudiante

carga_masiva_router = APIRouter()

# Carrera es 9

Session = sessionmaker(bind=engine)
session = Session()


@carga_masiva_router.post("/cargar-estudiantes/{carrera_id}")
async def cargar_estudiantes(file: UploadFile = File(...), carrera_id: int = Path(...)):
    contents = await file.read()
    df = pd.read_excel(contents)
    df.rename(columns={
        'cedula': 'cedula',
        'nombres': 'nombre',
        'apellidos': 'apellido',
        'direccion': 'direccion',
        'celular': 'celular',
        'correo': 'correo'
    }, inplace=True)

    # Crear una lista para almacenar los IDs generados
    generated_ids = []

    try:
        # Iniciar sesión con SQLAlchemy
        Session = sessionmaker(bind=engine)
        session = Session()

        # Iterar sobre cada fila del DataFrame e insertar en la base de datos
        for index, row in df.iterrows():
            estudiante = Estudiante(**row.to_dict())
            session.add(estudiante)
            session.flush()  # Forzar la generación del ID antes de hacer commit
            generated_ids.append(estudiante.id)

        # Insertar el id del estudiante y el id de la carrera en la tabla de detalle
        for id_estudiante in generated_ids:
            session.execute(
                "INSERT INTO DETALLE_EST_CAR (ID_EST_PER, ID_CAR_PER) VALUES (:id_estudiante, :id_carrera)",
                {"id_estudiante": id_estudiante, "id_carrera": carrera_id}
            )

        # Confirmar los cambios en la base de datos
        session.commit()

        # Cerrar la sesión
        session.close()

        return {"filename": file.filename, "generated_ids": generated_ids}

    except Exception as e:
        # Manejar cualquier error y retornar un HTTPException
        raise HTTPException(status_code=500, detail=str(e))
