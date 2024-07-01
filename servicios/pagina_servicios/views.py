from django.shortcuts import render, redirect
from django.db import IntegrityError
from django.contrib.auth import authenticate, login
from .models import UsuarioServicio,MetodoPago, SupervisorTabla, PoolDeTrabajo
from .forms import LoginForm,RegistroForm, ComentariosForm, ReaccionesForm, CompartidasForm, ReproduccionesForm, SeguidoresForm, LikesForm, VotosForm, RtForm, enVivoForm
from django.contrib.auth.hashers import make_password
from django.contrib import messages
from django.views import View
from django.http import JsonResponse, HttpResponse
from django.contrib.auth import logout
import requests
import mercadopago
from django.conf import settings
from django.urls import reverse
from .models import CryptoPayment
import hmac
import hashlib
from django.http import JsonResponse, HttpResponseBadRequest,HttpResponseServerError
from django.views.decorators.csrf import csrf_exempt
from .utils import get_binance_client, convert_usd_to_btc
import time
import json
# Create your views here.
from binance.client import Client
import logging
from binance.exceptions import BinanceAPIException
from decimal import Decimal, getcontext, ROUND_HALF_UP

def calcular_costo(request):
    numero = request.POST.get('numero', 0)
    id_enlace = request.session.get('servicio_id', '')

    # Define tus porcentajes aquí, como en el PHP original
    percentages = {
        "reacciones_Facebook": 0.10,
        "comentarios_Facebook": 1,
        "reproducciones_Facebook": 0.03,
        "envivo_Facebook": 0.08,
        "compartidas_Facebook": 0.08,
        "seguidores_Facebook": 0.15,
        "votos_Twitter": 0.03,
        "retwitt_Twitter": 0.04,
        "likes_Twitter": 0.04,
        "comentarios_Twitter": 2,
        "seguidores_Twitter": 0.04,
        "comentarios_Instagram": 5,
        "likes_Instagram": 0.04,
        "seguidores_Instagram": 0.04,
        "seguidores_Tiktok": 0.03,
        "reproducciones_Tiktok": 0.03,
        # Agrega los demás servicios
    }

    if id_enlace in percentages:
        service_value = Decimal(percentages[id_enlace]).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        total_price = (Decimal(numero) * service_value).quantize(Decimal('0.01'), rounding=ROUND_HALF_UP)
        
        # Convertir a cadena con dos dígitos decimales para la precisión
        service_value_str = "{:.2f}".format(service_value)
        total_price_str = "{:.2f}".format(total_price)
        
        request.session['servicioPrice'] = service_value_str
        request.session['precioTotal'] = total_price_str
        
        return JsonResponse({"total": total_price_str})
    else:
        return JsonResponse({"error": "Operación no válida o servicio no encontrado."}, status=400)

def validateOperation(request):
    try:
        usuario_servicio = UsuarioServicio.objects.get(correo_electronico=request.user.correo_electronico)  # Usar .email si es un usuario estándar de Django
        creditos = usuario_servicio.creditos
    except UsuarioServicio.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado'}, status=404)
    
    precioTotal = request.session.get('precioTotal')
    if precioTotal is None:
        return JsonResponse({'error': 'Precio total no definido en la sesión'}, status=400)

    data = {
        'creditos': creditos,
        'precioTotal': precioTotal
    }
    
    return JsonResponse(data)

def agregar_transaccion(request):
    usuario = request.user
    servicio = request.session.get('servicio_id')
    total = request.session.get('precioTotal')
    realTotal = float(total)
    dataType = "Transferencia"
    confirmacion = "Confirmado"
    comentsNum = request.session.get('secondOpt')
    comentsUnit = request.session.get('numberValue')
    link = request.session.get('link')

    if comentsNum is not None:
        comentario = f"{comentsNum} / {comentsUnit} unidades"
    else:
        comentario = f"{comentsUnit} unidades"

    # Insertar en SupervisorTabla
    nueva_transaccion = SupervisorTabla.objects.create(
        cliente=usuario.nombre,
        servicio=servicio,
        comentarios_extras=comentario,
        link=link,
        total=realTotal,
        tipo_pago=dataType,
        confirmacion_pago=confirmacion
    )

    nuevo_servicio = PoolDeTrabajo.objects.create(
        cliente=usuario.nombre,
        servicio=servicio,
        comentarios_extras=comentario,
        link=link,
    )

    # Actualizar créditos en UsuarioServicio
    usuario_servicio, created = UsuarioServicio.objects.get_or_create(correo_electronico=request.user.correo_electronico)
    usuario_servicio.creditos -= realTotal  # Asumiendo que `total` ya está convertido adecuadamente
    usuario_servicio.save()

    url_redireccion = reverse('perfil') + '#pedidosContainer'
    request.session['secondOpt'] = None
    return JsonResponse({'redirect_url': url_redireccion})
    
def creditos_usuario(request):
    # Asumiendo que tienes un modelo UsuarioServicio que guarda la relación de usuario y créditos
    try:
        usuario_servicio = UsuarioServicio.objects.get(correo_electronico=request.user.correo_electronico)
        creditos = usuario_servicio.creditos
        response = {'creditos': creditos}
        return JsonResponse(response)
    except UsuarioServicio.DoesNotExist:
        return JsonResponse({'error': 'Usuario no encontrado.'}, status=404)

def backend_cliente(request):
    usuario = request.user  # Esto asume que el nombre de usuario es el que se usa para identificar al cliente

    # Realizar la consulta a la base de datos usando Django ORM
    datos = SupervisorTabla.objects.filter(cliente=usuario.nombre).values(
    'servicio', 'fecha', 'total', 'confirmacion_pago', 'confirmacion_servicio'
    )

    # Convertir los datos a formato JSON
    return JsonResponse(list(datos), safe=False)  # `safe=False` es necesario para serializar una lista


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo_electronico = form.cleaned_data.get('correo_electronico')
            password = form.cleaned_data.get('password')
            # Update 'email' to 'correo_electronico' to match your custom backend
            usuario = authenticate(request, correo_electronico=correo_electronico, password=password)
            if usuario is not None:
                login(request, usuario)
                # Assuming 'rol' is stored directly in 'usuario' (the User model) and not in a related model
                # If 'rol' is a field in the User model itself:
                if usuario.rol == 1:  # Admin
                    return redirect('admin_dashboard')
                elif usuario.rol == 2:  # Usuario normal
                    return redirect('user_dashboard')
                # If the `rol` field is not directly on the `usuario`, but you're sure every user will have a corresponding `UsuarioServicio`:
                else:
                    try:
                        usuario_servicio = UsuarioServicio.objects.get(correo_electronico=correo_electronico)
                        if usuario_servicio.rol == 1:  # Admin
                            return redirect('admin_dashboard')
                        elif usuario_servicio.rol == 2:  # Usuario normal
                            return redirect('user_dashboard')
                    except UsuarioServicio.DoesNotExist:
                        pass  # Consider redirecting to a default page or showing an error if the role can't be determined
            else:
                # It's a good practice to pass 'invalid_credentials': True to differentiate between form errors and invalid login
                return render(request, 'login.html', {'form': form, 'error': 'Credenciales inválidas.'})
    else:
        form = LoginForm()
    return render(request, 'login.html', {'form': form})

def payInfo(request):
    data = {
        'numeroTotal': request.session['numberValue'],
        'servicio': request.session['servicio_id'],
        'precioTotal': request.session['precioTotal'],
        'precioUnitario': request.session['servicioPrice']
    }
    return JsonResponse(data)

def user_data(request):
    data = {
        'nombre': request.user.nombre,
        'correo': request.user.correo_electronico
    }
    return JsonResponse(data)

def check_logged_in(request):
    if request.user.is_authenticated:
        # Aquí podría ir lógica adicional basada en el rol del usuario
        return JsonResponse({'loggedIn': True})
    else:
        return JsonResponse({'loggedIn': False})
    
def registro_usuario(request):
    if request.method == 'POST':
        form = RegistroForm(request.POST)
        if form.is_valid():
            try:
                # Intenta crear un nuevo usuario y guardarlo
                nuevo_usuario = UsuarioServicio(
                    nombre=form.cleaned_data['nombre'],
                    correo_electronico=form.cleaned_data['correo_electronico'],
                    password=make_password(form.cleaned_data['password']),
                    rol=2,  # Rol establecido automáticamente a 2
                    creditos = 0,
                )
                nuevo_usuario.save()
                # Redirigir al login después de registrar
                return redirect('login_view')
            except IntegrityError:
                # Si hay un error de integridad (correo electrónico duplicado), informar al usuario
                messages.error(request, "Este correo electrónico ya está en uso. Por favor elija otro.")
                # Vuelve a cargar la página de registro con el formulario y el mensaje de error
                return render(request, 'registro.html', {'form': form})
    else:
        form = RegistroForm()
    return render(request, 'registro.html', {'form': form})

def redireccion_rol(request, usuario_id):
    try:
        usuario = UsuarioServicio.objects.get(id=usuario_id)
        if usuario.rol == 1:  # Admin
            return redirect('admin_dashboard')
    except UsuarioServicio.DoesNotExist:
        return redirect('login_view')
    return render(request, 'index.html')
    
def user_dashboard(request):
    # Aquí puedes añadir lógica para verificar si el usuario está autenticado y es un usuario normal
    return render(request, 'index.html')

def admin_dashboard(request):
    # Aquí puedes añadir lógica para verificar si el usuario está autenticado y es un administrador
    return render(request, 'supervisor.html')

def reacciones(request):
    return render(request, 'Reacciones.html')

def comentarios(request):
    return render(request, 'Comentarios.html')

def reproducciones(request):
    return render(request, 'Reproducciones.html')

def envivo(request):
    return render(request, 'Envivo.html')

def compartidas(request):
    return render(request, 'compartidas.html')

def seguidores(request):
    return render(request, 'Seguidores.html')

def votos(request):
    return render(request, 'votos.html')

def rt(request):
    return render(request, 'rt.html')

def likes(request):
    return render(request, 'likes.html')

def perfil(request):
    return render(request, 'perfil.html')

def carrito(request):
    return render(request, 'carrito.html')

def logout_view(request):
    logout(request)
    return redirect('user_dashboard')

def comentarios(request):
    id_servicio = request.GET.get('id')
    if id_servicio:
        request.session['servicio_id'] = id_servicio

    if request.method == 'POST':
        form = ComentariosForm(request.POST)
        if form.is_valid():
            comentarios = form.cleaned_data['comentariosInput']
            link = form.cleaned_data['linkInput']

            request.session['numberValue'] = comentarios
            request.session['link'] = link

            return redirect('carrito')
        else:
            # Si el formulario no es válido, renderizar de nuevo con errores
            return render(request, 'Comentarios.html', {'form': form})
    else:
        form = ComentariosForm()
        return render(request, 'Comentarios.html', {'form': form})

def reacciones(request):
    id_servicio = request.GET.get('id')
    if id_servicio:
        request.session['servicio_id'] = id_servicio

    if request.method == 'POST':
        form = ReaccionesForm(request.POST)
        if form.is_valid():
            reaccionOpcion = form.cleaned_data['selectOptVal']
            reacciones = form.cleaned_data['reaccionInput']
            link = form.cleaned_data['linkInput']

            request.session['secondOpt'] = reaccionOpcion
            request.session['numberValue'] = reacciones
            request.session['link'] = link

            return redirect('carrito')
        else:
            # Si el formulario no es válido, renderizar de nuevo con errores
            return render(request, 'Reacciones.html', {'form': form})
    else:
        form = ReaccionesForm()
        return render(request, 'Reacciones.html', {'form': form})

def compartidas(request):
    id_servicio = request.GET.get('id')
    if id_servicio:
        request.session['servicio_id'] = id_servicio

    if request.method == 'POST':
        form = CompartidasForm(request.POST)
        if form.is_valid():
            compartidas = form.cleaned_data['compartidasInput']
            link = form.cleaned_data['linkInput']

            request.session['numberValue'] = compartidas
            request.session['link'] = link

            return redirect('carrito')
        else:
            # Si el formulario no es válido, renderizar de nuevo con errores
            return render(request, 'compartidas.html', {'form': form})
    else:
        form = CompartidasForm()
        return render(request, 'compartidas.html', {'form': form})

def reproducciones(request):
    id_servicio = request.GET.get('id')
    if id_servicio:
        request.session['servicio_id'] = id_servicio

    if request.method == 'POST':
        form = ReproduccionesForm(request.POST)
        if form.is_valid():
            reproducciones = form.cleaned_data['reproInput']
            link = form.cleaned_data['linkInput']

            request.session['numberValue'] = reproducciones
            request.session['link'] = link

            return redirect('carrito')
        else:
            # Si el formulario no es válido, renderizar de nuevo con errores
            return render(request, 'Reproducciones.html', {'form': form})
    else:
        form = ReproduccionesForm()
        return render(request, 'Reproducciones.html', {'form': form})
    
def seguidores(request):
    id_servicio = request.GET.get('id')
    if id_servicio:
        request.session['servicio_id'] = id_servicio

    if request.method == 'POST':
        form = SeguidoresForm(request.POST)
        if form.is_valid():
            seguidores = form.cleaned_data['segInput']
            link = form.cleaned_data['linkInput']

            request.session['numberValue'] = seguidores
            request.session['link'] = link

            return redirect('carrito')
        else:
            # Si el formulario no es válido, renderizar de nuevo con errores
            return render(request, 'Seguidores.html', {'form': form})
    else:
        form = SeguidoresForm()
        return render(request, 'Seguidores.html', {'form': form})
    
def likes(request):
    id_servicio = request.GET.get('id')
    if id_servicio:
        request.session['servicio_id'] = id_servicio
    
    if request.method == 'POST':
        form = LikesForm(request.POST)
        if form.is_valid():
            likes = form.cleaned_data['likesInput']
            link = form.cleaned_data['linkInput']

            request.session['numberValue'] = likes
            request.session['link'] = link

            return redirect('carrito')
        else:
            # Si el formulario no es válido, renderizar de nuevo con errores
            return render(request, 'likes.html', {'form': form})
    else:
        form = LikesForm()
        return render(request, 'likes.html', {'form': form})

def votos(request):
    id_servicio = request.GET.get('id')
    if id_servicio:
        request.session['servicio_id'] = id_servicio

    if request.method == 'POST':
        form = VotosForm(request.POST)
        if form.is_valid():
            votoOpcion = form.cleaned_data['formatV']
            votos = form.cleaned_data['votosInput']
            link = form.cleaned_data['linkInput']

            request.session['secondOpt'] = votoOpcion
            request.session['numberValue'] = votos
            request.session['link'] = link

            return redirect('carrito')
        else:
            # Si el formulario no es válido, renderizar de nuevo con errores
            return render(request, 'votos.html', {'form': form})
    else:
        form = VotosForm()
        return render(request, 'votos.html', {'form': form})
    
def rt(request):
    id_servicio = request.GET.get('id')
    if id_servicio:
        request.session['servicio_id'] = id_servicio

    if request.method == 'POST':
        form = RtForm(request.POST)
        if form.is_valid():
            rt = form.cleaned_data['rtInput']
            link = form.cleaned_data['linkInput']

            request.session['numberValue'] = rt
            request.session['link'] = link

            return redirect('carrito')
        else:
            # Si el formulario no es válido, renderizar de nuevo con errores
            return render(request, 'rt.html', {'form': form})
    else:
        form = RtForm()
        return render(request, 'rt.html', {'form': form})

def enVivo(request):
    id_servicio = request.GET.get('id')
    if id_servicio:
        request.session['servicio_id'] = id_servicio

    if request.method == 'POST':
        form = enVivoForm(request.POST)
        if form.is_valid():
            tiempoOpcion = form.cleaned_data['formatT']
            espectadores = form.cleaned_data['especInput']
            link = form.cleaned_data['linkInput']

            request.session['secondOpt'] = tiempoOpcion
            request.session['numberValue'] = espectadores
            request.session['link'] = link

            return redirect('carrito')
        else:
            # Si el formulario no es válido, renderizar de nuevo con errores
            return render(request, 'Envivo.html', {'form': form})
    else:
        form = enVivoForm()
        return render(request, 'Envivo.html', {'form': form})
    
def crear_pago(request):
    sdk = mercadopago.SDK(settings.MERCADOPAGO_ACCESS_TOKEN)

    preference_data = {
        "items": [
            {
                "title": "Creditos",
                "quantity": 1,
                "unit_price": 50.0,
                "currency_id": "USD",
            }
        ],
        "back_urls": {
            "success": "http://127.0.0.1:8000/es/",
            "failure": "http://www.tu-sitio/failure",
            "pending": "http://127.0.0.1:8000/es/"
        },
        "auto_return": "approved",
        "payment_methods": {
        "excluded_payment_types": [
            {"id": "credit_card"},
            {"id": "debit_card"}
        ],
        "installments": 1
    },
    }

    preference_response = sdk.preference().create(preference_data)
    preference_id = preference_response["response"]["id"]

    return JsonResponse({"preference_id": preference_id})
    
logging.basicConfig(level=logging.INFO)

# Configura tus claves API aquí
api_key = 'INGRESE SU API_KEY'
api_secret = 'INGRESE SU API_SECRET'
client = Client(api_key, api_secret)

def obtener_tiempo_servidor_binance():
    try:
        url = "https://api.binance.com/api/v3/time"
        response = requests.get(url)
        response.raise_for_status()  # Esto lanzará un error si el código de estado no es 200.
        data = response.json()
        return data['serverTime']
    except requests.RequestException as e:
        raise Exception("Error al obtener el tiempo del servidor de Binance: {}".format(e))

# Asegúrate de que el cliente de Binance ajuste su timestamp basado en el tiempo del servidor de Binance
def ajustar_cliente_con_tiempo_servidor():
    server_time = obtener_tiempo_servidor_binance()
    diferencia_tiempo = server_time - int(time.time() * 1000)
    client.timestamp_offset = diferencia_tiempo

def get_btc_deposit_address():
    ajustar_cliente_con_tiempo_servidor()
    address = client.get_deposit_address(coin='BTC')
    return address['address']

# Función modificada para utilizar el tiempo del servidor de Binance
getcontext().prec = 10  # Ajusta la precisión según tus necesidades

def get_btc_amount(usd_amount):
    price = client.get_symbol_ticker(symbol="BTCUSDT")
    btc_price = Decimal(price['price'])  # Convertir el precio de BTC a Decimal
    btc_amount = usd_amount / btc_price  # Ahora es una operación Decimal / Decimal
    return btc_amount


def create_payment(request):
    context = {}
    if request.method == "POST":
        usd_amount = request.POST.get("usd_amount", 50)
        usd_amount = Decimal(usd_amount)
        if usd_amount < 50:
            context['error'] = 'El monto en USD debe ser al menos 50.'
        else:
            btc_amount = get_btc_amount(usd_amount)
            btc_address = get_btc_deposit_address()
            
            payment = CryptoPayment.objects.create(
                usd_amount=usd_amount, 
                btc_amount=btc_amount,
                currency='BTC',
                status='Pending',
            )
            
            context['message'] = 'Please send the payment'
            context['btc_amount'] = str(btc_amount)
            context['btc_address'] = btc_address
            # Aquí podrías incluir un id de transacción o cualquier otro dato relevante
    return render(request, "create_payment.html", context)

def verify_payment(transaction_id):
    try:
        transaction = client.get_transaction(transaction_id)
        # Asumiendo que la función get_transaction devuelve un diccionario con la información de la transacción
        if transaction and transaction['status'] == 'CONFIRMED':
            logging.info(f"Transacción {transaction_id} confirmada.")
            return True
        else:
            logging.warning(f"Transacción {transaction_id} no confirmada o no encontrada.")
            return False
    except BinanceAPIException as e:
        # Manejo específico de errores de la API de Binance
        logging.error(f"Error de la API de Binance: {e.status_code} - {e.message}")
    except Exception as e:
        # Manejo genérico de errores
        logging.error(f"Error al verificar la transacción {transaction_id}: {str(e)}")
    return False

def obtener_datos(request):
    datos = list(SupervisorTabla.objects.values())
    return JsonResponse(datos, safe=False)

def obtener_pool(request):
    datos = list(PoolDeTrabajo.objects.values())
    return JsonResponse(datos, safe=False)

def actualizar_registro(request):
    data = json.loads(request.body)
    try:
        registro = SupervisorTabla.objects.get(id=data['id'])
        setattr(registro, data['columna'], data['valor'])
        registro.save()
        return JsonResponse({'success': True, 'message': 'Actualización exitosa.'})
    except SupervisorTabla.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Registro no encontrado.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def actualizar_pool(request):
    data = json.loads(request.body)
    try:
        # Obtenemos el registro por ID y lo eliminamos
        registro = PoolDeTrabajo.objects.get(id=data['id'])
        registro.delete()
        return JsonResponse({'success': True, 'message': 'Registro eliminado exitosamente.'})
    except PoolDeTrabajo.DoesNotExist:
        return JsonResponse({'success': False, 'message': 'Registro no encontrado.'})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})
