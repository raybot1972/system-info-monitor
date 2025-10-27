import requests

def get_public_ip():
    try:
        return requests.get("https://api.ipify.org").text
    except Exception:
        return "Unavailable"

