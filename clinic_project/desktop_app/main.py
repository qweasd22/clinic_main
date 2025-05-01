import sys
from PyQt6.QtWidgets import QApplication, QMessageBox
from auth_window import AuthWindow
from main_window import MainWindow
from api_client import ApiClient
from utils.logger import configure_logging

class AppManager:
    def __init__(self):
        configure_logging()
        self.app = QApplication(sys.argv)
        self.main_window = None  # Сохраняем ссылку на главное окно

    def run(self):
        auth_window = AuthWindow()
        auth_window.on_success = self.on_auth_success
        auth_window.show()
        sys.exit(self.app.exec())

    def on_auth_success(self, token):
        try:
            api_client = ApiClient("http://localhost:18800", token)
            self.main_window = MainWindow(api_client)  # Сохраняем в атрибут класса
            self.main_window.show()
        except Exception as e:
            QMessageBox.critical(None, "Ошибка", f"Не удалось запустить приложение: {str(e)}")
            sys.exit(1)

if __name__ == "__main__":
    manager = AppManager()
    manager.run()