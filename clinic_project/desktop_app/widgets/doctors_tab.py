from PyQt6.QtWidgets import (
    QWidget, QTableWidget, QHeaderView, QPushButton, 
    QVBoxLayout, QHBoxLayout, QMessageBox, QTableWidgetItem
)
from PyQt6.QtCore import Qt
from dialogs.doctor_dialog import DoctorDialog

class DoctorsTab(QWidget):
    def __init__(self, api_client):
        super().__init__()
        self.api_client = api_client
        self.init_ui()
        self.load_data()

    def init_ui(self):
        self.table = QTableWidget()
        self.table.setColumnCount(4)
        self.table.setHorizontalHeaderLabels([
            "Фамилия", "Имя", "Отчество", "Специальность"
        ])
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)

        self.add_btn = QPushButton("Добавить врача", clicked=self.show_add_dialog)
        
        self.delete_btn = QPushButton("Удалить", clicked=self.delete_doctor)

        btn_layout = QHBoxLayout()
        btn_layout.addWidget(self.add_btn)
        
        btn_layout.addWidget(self.delete_btn)

        main_layout = QVBoxLayout()
        main_layout.addLayout(btn_layout)
        main_layout.addWidget(self.table)
        
        self.setLayout(main_layout)

    def load_data(self):
        try:
            doctors = self.api_client.get_doctors()
            self.table.setRowCount(len(doctors))
            
            for row, doctor in enumerate(doctors):
                self.table.setItem(row, 0, QTableWidgetItem(doctor['last_name']))
                self.table.setItem(row, 1, QTableWidgetItem(doctor['first_name']))
                self.table.setItem(row, 2, QTableWidgetItem(doctor['middle_name']))
                self.table.setItem(row, 3, QTableWidgetItem(doctor['specialty']))
                self.table.item(row, 0).setData(Qt.ItemDataRole.UserRole, doctor['id'])
                
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить врачей: {str(e)}")

    def show_add_dialog(self):
        dialog = DoctorDialog(self)
        if dialog.exec():
            try:
                data = dialog.get_data()
                self.api_client.create_doctor(
                    data=data, 
                    photo=data['photo']
                )
                self.load_data()
                QMessageBox.information(self, "Успех", "Врач успешно добавлен")
            except Exception as e:
                QMessageBox.critical(self, "Ошибка", f"Ошибка создания: {str(e)}")

    def show_edit_dialog(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите врача для редактирования")
            return
            
        doctor_id = self.table.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)
        try:
            doctor_data = self.api_client.get_doctor(doctor_id)
            dialog = DoctorDialog(self, doctor_data)
            if dialog.exec():
                updated_data = dialog.get_data()
                self.api_client.update_doctor(
                    doctor_id=doctor_id,
                    data=updated_data,
                    photo=updated_data['photo']
                )
                self.load_data()
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка обновления: {str(e)}")

    def delete_doctor(self):
        selected_row = self.table.currentRow()
        if selected_row == -1:
            QMessageBox.warning(self, "Ошибка", "Выберите врача для удаления")
            return
            
        doctor_id = self.table.item(selected_row, 0).data(Qt.ItemDataRole.UserRole)
        try:
            self.api_client.delete_doctor(doctor_id)
            self.load_data()
            QMessageBox.information(self, "Успех", "Врач успешно удален")
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Ошибка удаления: {str(e)}")