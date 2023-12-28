from fastapi import FastAPI
from routes.facultad_route import facultad_router


app = FastAPI()

app.include_router(facultad_router, tags=["facultad"], prefix="/api/v1")
