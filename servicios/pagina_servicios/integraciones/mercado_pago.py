import mercadopago
import os

# Configura tu access token
sdk = mercadopago.SDK(os.getenv('TEST-6856994996810038-032215-0853099b68722319d095831fbed34bdd-257284712'))

def crear_preferencia_de_pago(pago):
    """
    Crea una preferencia de pago con Mercado Pago.

    Args:
        pago (obj): Un objeto que contiene información sobre el pago.

    Returns:
        response: Respuesta de la API de Mercado Pago.
    """
    preference_data = {
        "items": [
            {
                "title": pago.descripcion,
                "quantity": 50,
                "unit_price": pago.cantidad,
            }
        ],
        "back_urls": {
            "success": "http://tu-sitio/success",
            "failure": "http://tu-sitio/failure",
            "pending": "http://tu-sitio/pending",
        },
        "auto_return": "approved",
    }

    preference_response = sdk.preference().create(preference_data)
    preference_id = preference_response["response"]["id"]
    
    return preference_id
