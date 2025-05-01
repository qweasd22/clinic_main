from PyQt6.QtWidgets import QWidget, QLineEdit, QPushButton, QVBoxLayout, QMessageBox
import requests

class AuthWindow(QWidget):
    def __init__(self, on_success=None):  # Сделайте on_success необязательным
        super().__init__()
        self.on_success = on_success  # Сохраняем callback
        self.init_ui()
        self.setFixedSize(300, 150)

    def init_ui(self):
        self.setWindowTitle("Авторизация")
        
        self.username_input = QLineEdit(placeholderText="Логин")
        self.password_input = QLineEdit(
            placeholderText="Пароль", 
            echoMode=QLineEdit.EchoMode.Password
        )
        
        self.login_btn = QPushButton("Войти")
        self.login_btn.clicked.connect(self.authenticate)

        layout = QVBoxLayout()
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_btn)
        self.setLayout(layout)
        
        

    def set_on_success(self, callback):  # Добавьте метод для установки callback
        self.on_success = callback


    def authenticate(self):
        try:
            response = requests.post(
                "http://localhost:18800/api-token-auth/",
                data={
                    "username": self.username_input.text(),
                    "password": self.password_input.text()
                }
            )
            
            if response.status_code == 200 and self.on_success:
                self.on_success(response.json()['token'])
            else:
                QMessageBox.critical(self, "Ошибка", "Неверные учетные данные")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Сервер недоступен: {str(e)}")