from django.contrib.auth.backends import BaseBackend
from django.contrib.auth.hashers import check_password
from .models import UsuarioServicio
    
class EmailAuthBackend(BaseBackend):
    def authenticate(self, request, correo_electronico=None, password=None):
        try:
            usuario = UsuarioServicio.objects.get(correo_electronico=correo_electronico)
            pwd_valid = check_password(password, usuario.password)
            if pwd_valid:
                return usuario
            return None
        except UsuarioServicio.DoesNotExist:
            return None

    def get_user(self, user_id):
        try:
            return UsuarioServicio.objects.get(pk=user_id)
        except UsuarioServicio.DoesNotExist:
            return None
