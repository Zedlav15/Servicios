from binance.client import Client
from django.conf import settings
import requests

def get_binance_client():
    """Crea y devuelve un cliente de Binance configurado."""
    return Client(settings.BINANCE_API_KEY, settings.BINANCE_SECRET_KEY)

def convert_usd_to_btc(usd_amount):
    """
    Convierte una cantidad especificada en USD a BTC utilizando la tasa de cambio actual.
    """
    url = "https://api.coindesk.com/v1/bpi/currentprice/BTC.json"
    
    try:
        response = requests.get(url)
        response.raise_for_status()  # Esto lanzará una excepción para respuestas de error HTTP
        data = response.json()
        btc_price = data['bpi']['USD']['rate_float']
        btc_amount = float(usd_amount) / btc_price  # Asegúrate de manejar usd_amount como float
        return round(btc_amount, 8)  # Redondear a 8 decimales para BTC
    except requests.RequestException as e:
        # Maneja errores de red (problemas de conexión, etc.)
        print(f"Error de red al acceder a CoinDesk: {e}")
    except ValueError as e:
        # Maneja errores de JSON (decodificación fallida, etc.)
        print(f"Error al decodificar la respuesta de CoinDesk: {e}")
    except KeyError as e:
        # Maneja errores si la estructura esperada de datos JSON no se encuentra
        print(f"Error al extraer el precio de BTC de la respuesta: {e}")

    return 0  # Retorna 0 como valor predeterminado en caso de error
