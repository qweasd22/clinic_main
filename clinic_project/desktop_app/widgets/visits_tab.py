from PyQt6.QtWidgets import QWidget, QTableWidget, QHeaderView, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import Qt
import requests

class VisitsTab(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Дата",   
            "Пациент", "Врач", "Услуга"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.refresh_btn = QPushButton("Обновить", clicked=self.load_data)
        

        
        
        layout = QVBoxLayout()
        layout.addWidget(self.table)
        
        layout.addWidget(self.refresh_btn)
        self.setLayout(layout)



    def load_data(self):
        try:
            visits = self.api_client.get_visits()
            self.table.setRowCount(len(visits))

            for row, visit in enumerate(visits):
                patient_id = visit.get("patient")
                
                # Логирование для отладки
                self.api_client.logger.debug(f"Обработка визита {row}: patient_id={patient_id}")
                
                patient_name = (
                    self.api_client.get_patient_name(patient_id) 
                    if patient_id 
                    else "Нет данных"
                )
                
                # Проверка индекса столбца "Пациент"
                self.table.setItem(row, 1, QTableWidgetItem(patient_name))  # Индекс 1 для столбца "Пациент"
                
                doctor_name = self.api_client.get_doctor_name(visit["doctor"])
                service_name = self.api_client.get_service_name(visit["service"])

                self.table.setItem(row, 0, QTableWidgetItem(visit["date"]))
                self.table.setItem(row, 1, QTableWidgetItem(patient_name))
                self.table.setItem(row, 2, QTableWidgetItem(doctor_name))
                self.table.setItem(row, 3, QTableWidgetItem(service_name))

        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить визиты: {str(e)}")
