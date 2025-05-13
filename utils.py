import requests, base64, os, time
from datetime import datetime
from dotenv import load_dotenv
from token_cache import load_token, save_token

load_dotenv()

def get_access_token():
    cached_token = load_token()
    if cached_token:
        return cached_token
    
    consumer_key = os.getenv("CONSUMER_KEY")
    consumer_secret = os.getenv("CONSUMER_SECRET")
    api_url = "https://sandbox.safaricom.co.ke/oauth/v1/generate?grant_type=client_credentials"
    response = requests.get(api_url, auth=(consumer_key, consumer_secret))

    access_token = response.json().get('access_token')

    expiry = time.time() + 3500 
    save_token(access_token, expiry)

    return response.json().get('access_token')

def lipa_na_mpesa_online(phone_number, amount):
    access_token = get_access_token()
    shortcode = os.getenv("BUSINESS_SHORTCODE")
    passkey = os.getenv("PASSKEY")

    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    password = base64.b64encode(f"{shortcode}{passkey}{timestamp}".encode()).decode()

    api_url = "https://sandbox.safaricom.co.ke/mpesa/stkpush/v1/processrequest"
    headers = {"Authorization": f"Bearer {access_token}"}
    payload = {
        "BusinessShortCode": int(shortcode),
        "Password": password,
        "Timestamp": timestamp,
        "TransactionType": "CustomerPayBillOnline",
        "Amount": int(amount),
        "PartyA": int(phone_number),
        "PartyB": int(shortcode),
        "PhoneNumber": int(phone_number),
        "CallBackURL": os.getenv("CALLBACK_URL"),
        "AccountReference": "Testing",
        "TransactionDesc": "Payment testing"
    }

    response = requests.post(api_url, json=payload, headers=headers)
    return response.json()
