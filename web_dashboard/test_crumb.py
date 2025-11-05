import requests
from requests.auth import HTTPBasicAuth

JENKINS_URL = 'http://localhost:8081/jenkins'  # ajusta si tu Jenkins no usa /jenkins
JENKINS_USER = 'lederboy'
JENKINS_TOKEN = '11ef49313efbab8cc232e47d4549357211'  # tu token API
JOB_NAME = 'etl_retail'

auth = HTTPBasicAuth(JENKINS_USER, JENKINS_TOKEN)

print("=== TEST CRUMB Y BUILD ===")

# 1️⃣ Obtener crumb
print("[1/2] Obteniendo CSRF token (crumb)...")
crumb_data = {}

try:
    response = requests.get(f"{JENKINS_URL}/crumbIssuer/api/json", auth=auth, timeout=5)

    if response.status_code == 200:
        crumb_json = response.json()
        crumb_field = crumb_json['crumbRequestField']
        crumb_value = crumb_json['crumb']
        crumb_data = {crumb_field: crumb_value}
        print(f"✅ Crumb obtenido ({crumb_field}): {crumb_value[:30]}...")
    elif response.status_code == 404:
        print("⚠️ Jenkins no tiene CSRF habilitado.")
    else:
        print(f"⚠️ No se pudo obtener crumb (HTTP {response.status_code})")

except Exception as e:
    print(f"⚠️ Error al intentar obtener crumb: {e}")

# 2️⃣ Disparar build
print("\n[2/2] Disparando build...")

try:
    build_url = f"{JENKINS_URL}/job/{JOB_NAME}/build"
    response = requests.post(build_url, auth=auth, headers=crumb_data, timeout=10)

    print(f"Status Code: {response.status_code}")
    if response.status_code in [200, 201, 302]:
        print("🚀 BUILD INICIADO EXITOSAMENTE.")
    elif response.status_code == 403:
        print("❌ Error 403: Jenkins requiere crumb o permisos insuficientes.")
        print(f"Headers enviados: {crumb_data}")
    elif response.status_code == 401:
        print("❌ Error 401: Token o usuario inválido.")
    else:
        print(f"❌ Error HTTP {response.status_code}")
        print(f"Respuesta: {response.text[:300]}")

except Exception as e:
    print(f"❌ Error al disparar el build: {e}")
