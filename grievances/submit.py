# grievances/submit.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
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
        self.submit_button = QPushButton("Submit", self)
        self.submit_button.clicked.connect(self.submit_grievance)

        layout.addWidget(QLabel("Submit Grievance"))
        layout.addWidget(self.description_input)
        layout.addWidget(self.submit_button)

        self.setLayout(layout)

    def submit_grievance(self):
        description = self.description_input.text()
        new_grievance = Grievance(user_id=1, description=description, status="Pending")  # Replace with dynamic user ID
        session.add(new_grievance)
        session.commit()
        QMessageBox.information(self, "Success", "Grievance submitted successfully")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = SubmitGrievanceWindow()
    window.show()
    sys.exit(app.exec_())
