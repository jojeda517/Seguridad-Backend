import secrets
import base64


clave = secrets.token_hex(32)
clave_base64 = base64.urlsafe_b64encode(bytes.fromhex(clave)).decode('utf-8')
print (clave)
print(clave_base64)

