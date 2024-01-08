from cryptography.fernet import Fernet
from dotenv import load_dotenv
import os

load_dotenv()

clave = os.getenv("AES_KEY")
cipher_suite = Fernet(clave)

def encriptar(texto):
    texto = texto.encode('utf-8')
    texto_encriptado = cipher_suite.encrypt(texto)
    return texto_encriptado


def desencriptar(texto):
    texto_desencriptado = cipher_suite.decrypt(texto)
    return texto_desencriptado.decode('utf-8')
