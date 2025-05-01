from PyQt6.QtWidgets import QWidget, QTableWidget, QHeaderView, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import Qt
from dialogs.service_dialog import ServiceDialog
import sys
import requests
class ServicesTab(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["ID", "Название", "Стоимость", "Специальность"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.add_btn = QPushButton("Добавить услугу", clicked=self.show_add_dialog)
        
        self.delete_btn = QPushButton("Удалить", clicked=self.delete_service)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.add_btn)
        
        btn_layout.addWidget(self.delete_btn)

        layout = QVBoxLayout()
        layout.addWidget(self.table)
        layout.addLayout(btn_layout)
        self.setLayout(layout)

    def load_data(self):
        try:
            services = self.api_client.get_services()
            self.table.setRowCount(len(services))
            
            for row, service in enumerate(services):
                self.table.setItem(row, 0, QTableWidgetItem(str(service['id'])))
                self.table.setItem(row, 1, QTableWidgetItem(service['name']))
                self.table.setItem(row, 2, QTableWidgetItem(f"{service['base_cost']} ₽"))
                self.table.setItem(row, 3, QTableWidgetItem(service['specialty']))
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить услуги: {str(e)}")

    def show_add_dialog(self):
        dialog = ServiceDialog(self)
        if dialog.exec():
            try:
                self.api_client.create_service(dialog.get_data())
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка создания: {str(e)}")

    def show_edit_dialog(self):
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите услугу для редактирования")
            return
            
        service_id = self.table.item(selected, 0).data(Qt.ItemDataRole.UserRole)
        dialog = ServiceDialog(self, service_id)
        if dialog.exec():
            try:
                self.api_client.update_service(service_id, dialog.get_data())
                self.load_data()
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка обновления: {str(e)}")

    def delete_service(self):
        selected_row = self.table.currentRow()
        if selected_row >= 0:
            try:
                # Получаем ID услуги
                service_id_item = self.table.item(selected_row, 0)
                if not service_id_item:
                    raise ValueError("Не удалось получить ID услуги")
                
                service_id = service_id_item.text().strip()
                if not service_id.isdigit():
                    raise ValueError("Некорректный формат ID")
                
                # Подтверждение удаления
                confirm = QMessageBox.question(
                    self,
                    "Подтверждение",
                    "Вы уверены, что хотите удалить эту услугу?",
                    QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No
                )
                
                if confirm == QMessageBox.StandardButton.Yes:
                    self.api_client.delete_service(int(service_id))
                    self.load_data()  # Обновляем таблицу
                    QMessageBox.information(self, "Успех", "Услуга удалена")
                    
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка удаления: {str(e)}")
        else:
            QMessageBox.warning(self, "Ошибка", "Выберите услугу для удаления")