from PyQt6.QtWidgets import QWidget, QTableWidget, QHeaderView, QVBoxLayout, QHBoxLayout, QMessageBox
from PyQt6.QtCore import Qt, QDate
from utils.validators import validate_visit_data

class VisitsTab(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.table = QTableWidget()
        self.table.setColumnCount(6)
        self.table.setHorizontalHeaderLabels([
            "Пациент", "Врач", "Дата", "Время", 
            "Услуга", "Статус"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
        
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        self.setLayout(layout)

    def load_data(self):
        try:
            visits = self.api_client.get_visits()
            self.table.setRowCount(len(visits))
            
            for row, visit in enumerate(visits):
                self._fill_row(row, visit)
                
        except Exception as e:
            self.show_error(f"Ошибка загрузки: {str(e)}")

    def _fill_row(self, row, visit):
        # Реализация заполнения строки
        pass

    def show_error(self, message):
        QMessageBox.critical(self, "Ошибка", message)