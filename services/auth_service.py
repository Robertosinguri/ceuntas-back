from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from firebase_admin import auth
import logging

# Esto habilita el botón "Authorize" en la documentación de FastAPI (SwaggerUI)
security = HTTPBearer()

def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    """
    Verifica el ID Token de Firebase enviado en el header Authorization como Bearer.
    Si el token es válido, retorna los datos del usuario.
    """
    token = credentials.credentials
    try:
        # Verificamos el token con Firebase Admin SDK
        decoded_token = auth.verify_id_token(token)
        return decoded_token # {uid, email, name, etc.}
    except Exception as e:
        logging.error(f"Error al verificar el token de Firebase: {e}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token inválido o expirado",
            headers={"WWW-Authenticate": "Bearer"},
        )
