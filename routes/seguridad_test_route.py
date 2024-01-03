from fastapi import APIRouter, HTTPException, Path
from fastapi import Depends
from utils.seguridad import encriptar, desencriptar

seguridad_test = APIRouter()

# Se recibe un texto plano y se encripta
@seguridad_test.get("/encriptar/{texto}")
def encriptar_texto(texto: str = Path(..., min_length=1)):
    return encriptar(texto)


# Se recibe un texto encriptado y se desencripta
@seguridad_test.get("/desencriptar/{texto}")
def desencriptar_texto(texto: str = Path(..., min_length=1)):
    return desencriptar(texto)
