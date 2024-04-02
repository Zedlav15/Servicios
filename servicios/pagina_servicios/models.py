from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager
from django.contrib.auth.hashers import make_password
# Create your models here.

class SupervisorTabla(models.Model):
    cliente = models.CharField(max_length=400, null=False)
    servicio = models.CharField(max_length=700, null=False)
    comentarios_extras = models.CharField(max_length=300, default=' ')
    link = models.CharField(max_length=500, null=False)
    total = models.FloatField(null=False)
    fecha = models.DateTimeField(auto_now_add=True, null=False)
    tipo_pago = models.CharField(max_length=200, null=False)
    confirmacion_pago = models.CharField(max_length=200, null=False, default='No confirmado')
    confirmacion_servicio = models.CharField(max_length=200, null=False, default='No confirmado')

    def __str__(self):
        return self.cliente

class UsuarioServicioManager(BaseUserManager):
    def create_user(self, correo_electronico, nombre, password=None):
        """
        Crea y guarda un Usuario con el correo electrónico y contraseña dados.
        """
        if not correo_electronico:
            raise ValueError('Los usuarios deben tener un correo electrónico')
        
        usuario = self.model(
            correo_electronico=self.normalize_email(correo_electronico),
            nombre=nombre,
        )

        usuario.set_password(password)
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, correo_electronico, nombre, password):
        """
        Crea y guarda un superusuario con el correo electrónico y contraseña dados.
        """
        usuario = self.create_user(
            correo_electronico,
            nombre=nombre,
            password=password,
        )
        usuario.is_admin = True
        usuario.save(using=self._db)
        return usuario

class UsuarioServicio(AbstractBaseUser):
    nombre = models.CharField(max_length=250)
    correo_electronico = models.EmailField(max_length=255, unique=True)
    password = models.CharField(max_length=300)  # Campo renombrado a 'password'
    rol = models.IntegerField(default=2)
    creditos = models.IntegerField(default=0)

    objects = UsuarioServicioManager()

    USERNAME_FIELD = 'correo_electronico'
    REQUIRED_FIELDS = ['nombre']  # correo_electronico es el USERNAME_FIELD, por lo que solo incluimos 'nombre'

    def __str__(self):
        return self.correo_electronico

    def agregar_creditos(self, cantidad):
        self.creditos += cantidad
        self.save()

    def restar_creditos(self, cantidad):
        if self.creditos >= cantidad:
            self.creditos -= cantidad
            self.save()
            return True
        return False
    
class MetodoPago(models.Model):
    usuario = models.ForeignKey('pagina_servicios.UsuarioServicio', on_delete=models.CASCADE)
    tipo = models.CharField(max_length=50, choices=(('transferencia', 'Transferencia'), ('criptomoneda', 'Criptomoneda')))
    cantidad = models.FloatField()
    fecha = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.usuario.correo_electronico} - {self.tipo} - {self.cantidad}"
    
class CryptoPayment(models.Model):
    transaction_id = models.CharField(max_length=255, blank=True, null=True)  # Puede que no tengas el ID de transacción inmediatamente
    usd_amount = models.DecimalField(max_digits=10, decimal_places=2, default=50)
    btc_amount = models.DecimalField(max_digits=10, decimal_places=8, blank=True, null=True)  # Monto en BTC
    currency = models.CharField(max_length=4, default='BTC')
    status = models.CharField(max_length=50, default='Pending')
    created_at = models.DateTimeField(auto_now_add=True)

class PoolDeTrabajo(models.Model):
    cliente = models.CharField(max_length=400, null=False)
    servicio = models.CharField(max_length=700, null=False)
    comentarios_extras = models.CharField(max_length=300, default=' ')
    link = models.CharField(max_length=500, null=False)
    fecha = models.DateTimeField(auto_now_add=True, null=False)

    def __str__(self):
        return self.cliente