import requests
from django.conf import settings

def consulta_ruc(ruc, token):
    """
    Consulta la API de RUC y devuelve los datos.
    """
    url = "https://api.consultasperu.com/api/v1/query"
    headers = {"Content-Type": "application/json"}
    body = {
        "token": token,
        "type_document": "ruc",
        "document_number": ruc
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {"error": f"Error en la consulta: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}

def consulta_dni(dni, token):
    """
    Consulta la API de DNI y devuelve los datos.
    """
    url = "https://api.consultasperu.com/api/v1/query"
    headers = {"Content-Type": "application/json"}
    body = {
        "token": token,
        "type_document": "dni",
        "document_number": dni
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            return response.json().get("data", {})
        else:
            return {"error": f"Error en la consulta: {response.status_code}"}
    except Exception as e:
        return {"error": str(e)}





        
