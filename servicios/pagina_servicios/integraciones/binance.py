from binance.client import Client
import os

client = Client(api_key=os.getenv('BINANCE_API_KEY'), api_secret=os.getenv('BINANCE_API_SECRET'))

def generar_direccion_btc():
    # Obtén detalles para el depósito en BTC
    btc_details = client.get_deposit_address(coin='BTC')
    return btc_details['address'], btc_details['tag']

def monitorear_direccion_btc(direccion):
    # Aquí tendrías que implementar lógica para monitorear la dirección
    # Esto podría implicar revisar periódicamente las transacciones entrantes.
    pass
