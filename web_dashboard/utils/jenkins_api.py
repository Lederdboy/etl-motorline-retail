from requests.auth import HTTPBasicAuth
from config import Config
import requests

class JenkinsAPI:
    def __init__(self):
        self.base_url = Config.JENKINS_URL

        # Usa autenticación solo si hay usuario/contraseña
        if getattr(Config, "JENKINS_USER", "") and getattr(Config, "JENKINS_PASSWORD", ""):
            self.auth = HTTPBasicAuth(Config.JENKINS_USER, Config.JENKINS_PASSWORD)
        else:
            self.auth = None

    def trigger_build(self):
        """Dispara el job ETL en Jenkins"""
        try:
            url = f"{self.base_url}/job/{Config.JENKINS_JOB}/build"
            response = requests.post(url, auth=self.auth, timeout=10)

            if response.status_code in [200, 201, 302]:
                return {"status": "success", "message": "🚀 Build iniciado correctamente"}
            else:
                return {
                    "status": "error",
                    "message": f"❌ Error {response.status_code}: {response.text[:200]}"
                }
        except Exception as e:
            return {"status": "error", "message": f"⚠️ Error al conectar con Jenkins: {str(e)}"}

    def get_last_build_info(self):
        """Obtiene información del último build"""
        try:
            url = f"{self.base_url}/job/{Config.JENKINS_JOB}/lastBuild/api/json"
            response = requests.get(url, auth=self.auth, timeout=10)
            if response.status_code == 200:
                return response.json()
            return {}
        except:
            return {}

    def get_build_history(self, limit=10):
        """Obtiene el historial de builds"""
        try:
            url = f"{self.base_url}/job/{Config.JENKINS_JOB}/api/json?tree=builds[number,result,timestamp]{{0,{limit}}}"
            response = requests.get(url, auth=self.auth, timeout=10)
            if response.status_code == 200:
                return response.json()
            return {}
        except:
            return {}
