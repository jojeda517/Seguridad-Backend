from fastapi import FastAPI
from routes.facultad_route import facultad_router
from routes.estudiante_route import estudiante_router
from routes.carrera_route import carrera_router


app = FastAPI()

app.include_router(facultad_router, tags=["Facultad"], prefix="/api/v1")
app.include_router(estudiante_router, tags=["Estudiante"], prefix="/api/v1")
app.include_router(carrera_router, tags=["Carrera"], prefix="/api/v1")
