# submit.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox, QComboBox
from sqlalchemy.orm import sessionmaker
from database.models import engine, Grievance

Session = sessionmaker(bind=engine)
session = Session()

class SubmitGrievanceWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Submit Grievance")
        layout = QVBoxLayout()

        self.description_input = QLineEdit(self)
        self.description_input.setPlaceholderText("Description")

        self.recipient_input = QComboBox(self)
        self.recipient_input.addItems(["HR", "Manager", "IT Support"])  # Add more roles as needed

        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit_grievance)

        layout.addWidget(QLabel("Submit Grievance"))
        layout.addWidget(self.description_input)
        layout.addWidget(QLabel("Recipient"))
        layout.addWidget(self.recipient_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_grievance(self):
        description = self.description_input.text()
        recipient = self.recipient_input.currentText()
        new_grievance = Grievance(user_id=1, description=description, status="Pending", recipient=recipient)  # Replace with dynamic user ID
        session.add(new_grievance)
        session.commit()
        QMessageBox.information(self, "Success", "Grievance submitted successfully")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SubmitGrievanceWindow()
    window.show()
    sys.exit(app.exec_())
