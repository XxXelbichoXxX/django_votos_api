from cryptography.fernet import Fernet, InvalidToken
import binascii
from forgetPasswordRequest.models import ForgetPasswordRequest
import logging

logger = logging.getLogger(__name__)

def load_code():
    try:
        with open("aassswascsxzas.key", "rb") as key_file:
            return key_file.read()
    except Exception as e:
        logger.error(f"Error loading key: {str(e)}")
        raise e

def check_code_exists(code):
    try:
        # Cargar la clave desde el archivo
        key = load_code()
        f = Fernet(key)

        # Obtener todos los registros y verificar si alguno coincide
        queryset = ForgetPasswordRequest.objects.all()
        for obj in queryset:
            try:
                # Desencriptar el código almacenado en la base de datos
                encrypted_code = obj.code.encode()
                decrypted_code = f.decrypt(encrypted_code).decode()

                if decrypted_code == code:
                    return True
            except (InvalidToken, binascii.Error) as e:
                # Manejo de error si el token no es válido
                logger.error(f"Error al desencriptar el código en la base de datos. Error: {str(e)}")
                continue  # Continuar con el siguiente registro

        return False
    except Exception as e:
        logger.error(f"Error inesperado: {str(e)}")
        raise
