from PyQt6.QtWidgets import (
    QDialog, QFormLayout, QLineEdit, QComboBox, QPushButton, 
    QFileDialog, QLabel, QDialogButtonBox, QSpinBox
)
from PyQt6.QtCore import Qt
from pathlib import Path

class DoctorDialog(QDialog):
    def __init__(self, parent=None, doctor_data=None):
        super().__init__(parent)
        self.doctor_data = doctor_data
        self.photo_path = None
        self.init_ui()
        
        if doctor_data:
            self.load_existing_data()

    def init_ui(self):
        self.setWindowTitle("Редактирование врача" if self.doctor_data else "Новый врач")
        self.setMinimumWidth(400)

        # Элементы формы
        self.last_name_input = QLineEdit()
        self.first_name_input = QLineEdit()
        self.middle_name_input = QLineEdit()
        self.specialty_input = QLineEdit()
        
        # Категории с числовыми кодами
        self.category_input = QComboBox()
        self.category_input.addItem("Высшая", 3)
        self.category_input.addItem("Первая", 2)
        self.category_input.addItem("Вторая", 1)
        
        self.photo_label = QLabel("Фото не выбрано")
        self.photo_btn = QPushButton("Выбрать фото...")
        self.photo_btn.clicked.connect(self.select_photo)
        self.experience_input = QSpinBox()
        self.experience_input.setRange(0, 100)

        # Кнопки
        buttons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel
        self.button_box = QDialogButtonBox(buttons)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        # Layout
        layout = QFormLayout()
        layout.addRow("Фамилия:", self.last_name_input)
        layout.addRow("Имя:", self.first_name_input)
        layout.addRow("Отчество:", self.middle_name_input)
        layout.addRow("Специальность:", self.specialty_input)
        layout.addRow("Категория:", self.category_input)
        layout.addRow("Фото:", self.photo_label)
        layout.addRow("Опыт работы:", self.experience_input)
        layout.addRow(self.photo_btn)
        layout.addWidget(self.button_box)

        self.setLayout(layout)

    def select_photo(self):
        path, _ = QFileDialog.getOpenFileName(
            self,
            "Выберите фото",
            str(Path.home()),
            "Images (*.png *.jpg *.jpeg)"
        )
        if path:
            self.photo_path = path
            self.photo_label.setText(Path(path).name)

    def get_data(self):
        data = {
            "last_name": self.last_name_input.text(),
            "first_name": self.first_name_input.text(),
            "middle_name": self.middle_name_input.text(),
            "specialty": self.specialty_input.text(),
            "category": self.category_input.currentData(),
            "photo": self.photo_path if self.photo_path else None,
            "experience": self.experience_input.value(),
        }
        
        if self.doctor_data and 'id' in self.doctor_data:
            data['id'] = self.doctor_data['id']
            
        return data

    def load_existing_data(self):
        self.last_name_input.setText(self.doctor_data.get('last_name', ''))
        self.first_name_input.setText(self.doctor_data.get('first_name', ''))
        self.middle_name_input.setText(self.doctor_data.get('middle_name', ''))
        self.specialty_input.setText(self.doctor_data.get('specialty', ''))
        
        # Установка категории по значению
        category_value = self.doctor_data.get('category', 1)
        index = self.category_input.findData(category_value)
        if index >= 0:
            self.category_input.setCurrentIndex(index)
            
        self.experience_input.setValue(self.doctor_data.get('experience', 0))