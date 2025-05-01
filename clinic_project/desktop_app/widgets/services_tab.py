from PyQt6.QtWidgets import QWidget, QTableWidget, QHeaderView, QPushButton, QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem
from PyQt6.QtCore import Qt
from dialogs.service_dialog import ServiceDialog

class ServicesTab(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.table = QTableWidget()
        self.table.setColumnCount(3)
        self.table.setHorizontalHeaderLabels(["Название", "Стоимость", "Специальность"])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.add_btn = QPushButton("Добавить услугу", clicked=self.show_add_dialog)
        self.edit_btn = QPushButton("Редактировать", clicked=self.show_edit_dialog)
        self.delete_btn = QPushButton("Удалить", clicked=self.delete_service)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.add_btn)
        btn_layout.addWidget(self.edit_btn)
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
                self.table.setItem(row, 0, QTableWidgetItem(service['name']))
                self.table.setItem(row, 1, QTableWidgetItem(f"{service['base_cost']} ₽"))
                self.table.setItem(row, 2, QTableWidgetItem(service['specialty']))
                
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
        selected = self.table.currentRow()
        if selected == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите услугу для удаления")
            return
            
        service_id = self.table.item(selected, 0).data(Qt.ItemDataRole.UserRole)
        try:
            self.api_client.delete_service(service_id)
            self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка удаления: {str(e)}")