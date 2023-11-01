import requests
from paypalrestsdk import Invoice
import paypalrestsdk


def invoice(client_id, client_secret, merchant_email, customer_email, items, mode):

    my_api = paypalrestsdk.Api({
        "mode": mode,
        "client_id": client_id,
        "client_secret": client_secret 
    })

    resp = requests.post(
        url="https://api-m.sandbox.paypal.com/v1/oauth2/token",
        auth=(client_id, client_secret),
        data=b"grant_type=client_credentials",
        headers={
            "Accept": "application/json",
            "Accept-Language": "en_US",
        },
    )
    resp.raise_for_status()
    access_token = resp.json()['access_token']

    # creating invoice
    invoice = Invoice({
        'merchant_info': {
            "email": merchant_email,
        },
        "billing_info": [{
            "email": customer_email
        }],
        "items": items,
        "invoicer": {
            "name": {
                "given_name": "David",
                "surname": "Larusso"
            },
        }
    }, api=my_api)
    invoice.create()
    invoice_id = invoice.__getattr__('id')

    # sending invoice
    headers = {
        'Authorization': f'Bearer {access_token}',
        'Content-Type': 'application/json',
        'PayPal-Request-Id': 'b1d1f06c7246c',
    }
    data = '{ "send_to_invoicer": true }'
    response = requests.post(
        f'https://api-m.sandbox.paypal.com/v2/invoicing/invoices/{invoice_id}/send', 
        headers=headers, data=data
    )

    return response.json().get('href')
