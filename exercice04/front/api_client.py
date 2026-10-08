import os
import requests

API_URL = os.getenv("API_URL", "http://127.0.0.1:8000")

def login_api(username, password):
    try:
        return requests.post(f"{API_URL}/auth/login", json={"username": username, "password": password})
    except Exception as e:
        return None

def get_frequentations_api(page=1, page_size=5):
    try:
        return requests.get(f"{API_URL}/frequentations", params={"page": page, "page_size": page_size})
    except Exception as e:
        return None

def get_bilan_api(token):
    headers = {"Authorization": f"Bearer {token}"} if token else {}
    try:
        return requests.get(f"{API_URL}/analytics/bilan", headers=headers)
    except Exception as e:
        return None