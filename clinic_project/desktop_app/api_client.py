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
            self.logger = logging.getLogger(self.__class__.__name__)
            # Проверка соединения
            test_response = self._handle_request("get", "services")
            if not test_response:
                raise Exception("Не удалось подключиться к API")
                
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Инициализация API не удалась: {str(e)}")
            sys.exit(1)

    def _handle_request(self, method, endpoint, **kwargs):
        url = f"{self.base_url}/api/admin/{endpoint}/"
        try:
            response = getattr(self.session, method)(url, **kwargs)
            response.raise_for_status()
            return response.json()  # Гарантированно возвращает dict/list
        except RequestException as e:
            self.logger.error(f"API Error: {str(e)}")
            raise

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

    def delete_service(self, service_id):
        self.logger.info(f"Удаление услуги ID: {service_id}")
        response = self.session.delete(f"{self.base_url}/api/admin/services/{service_id}/")
        response.raise_for_status()
    def get_visits(self, params=None):
        response = self.session.get(f"{self.base_url}/api/admin/visits/", params=params)
        response.raise_for_status()
        return response.json()

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

    def get_patients(self):
        """Загружает список пациентов с проверкой формата ответа."""
        try:
            response = self._handle_request("get", "patients")
            if isinstance(response, list):
                return response
            else:
                self.logger.error("API вернул некорректный формат данных для пациентов.")
                return []
        except Exception as e:
            self.logger.error(f"Ошибка при загрузке пациентов: {str(e)}")
            return []

    def get_patient_name(self, patient_id):
        """Возвращает ФИО пациента, комбинируя данные из patient и user."""
        try:
            if not patient_id:
                return "Нет данных"
            
            # 1. Получаем данные пациента
            patient_data = self._handle_request("get", f"patients/{patient_id}")
            if not isinstance(patient_data, dict):
                return "Неизвестно"
            
            # 2. Извлекаем user_id и отчество
            user_id = patient_data.get("user")
            middle_name = patient_data.get("middle_name", "")
            
            # 3. Получаем данные пользователя
            user_data = self._handle_request("get", f"users/{user_id}")
            if not isinstance(user_data, dict):
                return "Неизвестно"
            
            # 4. Извлекаем имя и фамилию
            first_name = user_data.get("first_name", "")
            last_name = user_data.get("last_name", "")
            
            # 5. Формируем ФИО
            return f"{last_name} {first_name} {middle_name}".strip()
            
        except Exception as e:
            self.logger.error(f"Ошибка: {str(e)}")
            return "Ошибка"

    def get_doctor_name(self, doctor_id):
        """Возвращает ФИО врача с обработкой ошибок."""
        try:
            doctors = self.get_doctors()
            for doctor in doctors:
                if doctor.get('id') == doctor_id:
                    last_name = doctor.get('last_name', '')
                    first_name = doctor.get('first_name', '')
                    return f"{last_name} {first_name}".strip()
            return "Неизвестно"
        except Exception as e:
            self.logger.error(f"Ошибка получения имени врача: {str(e)}")
            return "Ошибка"

    def get_service_name(self, service_id):
        """Возвращает название услуги с обработкой ошибок."""
        try:
            services = self.get_services()
            for service in services:
                if service.get('id') == service_id:
                    return service.get('name', 'Неизвестно')
            return "Неизвестно"
        except Exception as e:
            self.logger.error(f"Ошибка получения названия услуги: {str(e)}")
            return "Ошибка"