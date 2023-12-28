from fastapi import FastAPI
from routes.facultad_route import facultad_router
from routes.categoria_route import categoria_router


app = FastAPI()

app.include_router(facultad_router, tags=["facultad"], prefix="/api/v1")
app.include_router(categoria_router, tags=["categoria"], prefix="/api/v1")
