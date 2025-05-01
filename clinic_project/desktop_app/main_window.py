from PyQt6.QtWidgets import QMainWindow, QTabWidget, QMessageBox
from widgets.doctors_tab import DoctorsTab
from widgets.visits_tab import VisitsTab
from widgets.services_tab import ServicesTab
from PyQt6.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.setAttribute(Qt.WidgetAttribute.WA_DeleteOnClose, False)  # Важно!
        self.init_ui()
        self.load_data()

    

    def load_data(self):
        try:
            # Тестовый запрос для проверки работы
            services = self.api_client.get_services()
            if not services:
                raise Exception("Нет данных для отображения")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка загрузки: {str(e)}")
            self.close()

    def init_ui(self):
        self.setWindowTitle("Администрирование клиники")
        self.setMinimumSize(800, 600)
        
        tabs = QTabWidget()
        tabs.addTab(VisitsTab(self.api_client), "Записи")
        tabs.addTab(DoctorsTab(self.api_client), "Врачи")
        tabs.addTab(ServicesTab(self.api_client), "Услуги")
        
        self.setCentralWidget(tabs)

    