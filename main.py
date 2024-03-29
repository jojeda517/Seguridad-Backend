from fastapi import FastAPI
from routes.facultad_route import facultad_router
from routes.categoria_route import categoria_router
from routes.estudiante_route import estudiante_router
from routes.carrera_route import carrera_router
from routes.usuario_route import usuario_router
from routes.documento_route import documento_router
from routes.carga_masiva_route import carga_masiva_router
from routes.rol_route import rol_router

from fastapi.middleware.cors import CORSMiddleware

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Permitir cualquier origen
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(facultad_router, tags=["Facultad"], prefix="/api/v1")
app.include_router(estudiante_router, tags=["Estudiante"], prefix="/api/v1")
app.include_router(carrera_router, tags=["Carrera"], prefix="/api/v1")
app.include_router(categoria_router, tags=["Categoria"], prefix="/api/v1")
app.include_router(usuario_router, tags=["Usuario"], prefix="/api/v1")
app.include_router(documento_router, tags=["Documento"], prefix="/api/v1")
app.include_router(carga_masiva_router, tags=["Carga Masiva"], prefix="/api/v1")
app.include_router(rol_router, tags=["Rol"], prefix="/api/v1")

