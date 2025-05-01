from PyQt6.QtWidgets import QDialog, QFormLayout, QLineEdit, QDoubleSpinBox, QComboBox, QDialogButtonBox, QMessageBox

class ServiceDialog(QDialog):
    def __init__(self, parent=None, service_id=None):
        super().__init__(parent)
        self.service_id = service_id
        self.init_ui()
        
        if service_id:
            self.load_data()

    def init_ui(self):
        self.setWindowTitle("Редактирование услуги" if self.service_id else "Новая услуга")
        
        self.name_input = QLineEdit()
        self.cost_input = QDoubleSpinBox()
        self.cost_input.setMaximum(1000000)
        self.specialty_input = QComboBox()
        self.specialty_input.addItems(["Терапия", "Хирургия", "Неврология", "Кардиология"])

        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        layout = QFormLayout()
        layout.addRow("Название:", self.name_input)
        layout.addRow("Стоимость:", self.cost_input)
        layout.addRow("Специальность:", self.specialty_input)
        layout.addWidget(self.button_box)
        
        self.setLayout(layout)

    def get_data(self):
        return {
            "name": self.name_input.text(),
            "base_cost": self.cost_input.value(),
            "specialty": self.specialty_input.currentText()
        }

    def load_data(self):
        try:
            service = self.parent().api_client.get_service(self.service_id)
            self.name_input.setText(service['name'])
            self.cost_input.setValue(service['base_cost'])
            self.specialty_input.setCurrentText(service['specialty'])
        except Exception as e:
            QMessageBox.critical(self, "Ошибка", f"Не удалось загрузить данные: {str(e)}")