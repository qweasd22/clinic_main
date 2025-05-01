import requests
import logging
from requests.exceptions import RequestException
from PyQt6.QtWidgets import QMessageBox
import sys
class ApiClient:
    def __init__(self, base_url, token):
        try:
            self.base_url = base_url
            self.session = requests.Session()
            self.session.headers.update({"Authorization": f"Token {token}"})
            
            # Проверка соединения
            test_response = self._handle_request("get", "services")
            if not test_response:
                raise Exception("Не удалось подключиться к API")
                
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Инициализация API не удалась: {str(e)}")
            sys.exit(1)

    def _handle_request(self, method, endpoint, **kwargs):
        try:
            url = f"{self.base_url}/api/admin/{endpoint}/"
            response = getattr(self.session, method)(url, **kwargs)
            response.raise_for_status()
            return response.json()
        except RequestException as e:
            self.logger.error(f"API Error: {str(e)}")
            raise Exception(f"API Request Failed: {str(e)}")

    def get_doctors(self):
        response = self.session.get(f"{self.base_url}/api/admin/doctors/")
        response.raise_for_status()
        return response.json()

    def create_doctor(self, data, photo=None):
        files = {'photo': open(photo, 'rb')} if photo else None
        response = self.session.post(
            f"{self.base_url}/api/admin/doctors/",
            data=data,
            files=files
        )
        response.raise_for_status()
        return response.json()

    def update_doctor(self, doctor_id, data, photo=None):
        files = {'photo': open(photo, 'rb')} if photo else None
        response = self.session.put(
            f"{self.base_url}/api/admin/doctors/{doctor_id}/",
            data=data,
            files=files
        )
        response.raise_for_status()
        return response.json()

    def delete_doctor(self, doctor_id):
        response = self.session.delete(
            f"{self.base_url}/api/admin/doctors/{doctor_id}/"
        )
        response.raise_for_status()

    def get_visits(self, params=None):
        return self._handle_request("get", "visits", params=params)

    def get_services(self):
        return self._handle_request("get", "services")

    def create_visit(self, data):
        return self._handle_request("post", "visits", json=data)
    def get_service(self, service_id):
        return self._handle_request("get", f"services/{service_id}")

    def create_service(self, data):
        return self._handle_request("post", "services", json=data)

    def update_service(self, service_id, data):
        return self._handle_request("put", f"services/{service_id}", json=data)

    def delete_service(self, service_id):
        return self._handle_request("delete", f"services/{service_id}")