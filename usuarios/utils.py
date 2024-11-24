import requests

def consulta_api(document_number, token, type_document):
    """
    Consulta genérica a la API para obtener información de RUC o DNI.
    """
    url = "https://api.consultasperu.com/api/v1/query"
    headers = {"Content-Type": "application/json"}
    body = {
        "token": token,
        "type_document": type_document,
        "document_number": document_number
    }

    try:
        response = requests.post(url, headers=headers, json=body)
        if response.status_code == 200:
            data = response.json().get("data", {})
            if data:
                return data
            return {"error": f"No se encontraron datos para el {type_document} {document_number}."}
        else:
            return {"error": f"Error en la consulta: {response.status_code}"}
    except Exception as e:
        return {"error": f"Error al conectarse a la API: {str(e)}"}

def consulta_ruc(ruc, token):
    """
    Consulta específica para RUC.
    """
    return consulta_api(ruc, token, "ruc")

def consulta_dni(dni, token):
    """
    Consulta específica para DNI.
    """
    return consulta_api(dni, token, "dni")