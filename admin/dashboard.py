# admin/dashboard.py
import sys
from tkinter import messagebox
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton
from sqlalchemy.orm import sessionmaker
from database.models import engine, Grievance

Session = sessionmaker(bind=engine)
session = Session()

class AdminDashboard(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Admin Dashboard")
        layout = QVBoxLayout()

        self.grievance_list = QListWidget()
        self.resolve_button = QPushButton("Resolve Selected Grievance")
        self.resolve_button.clicked.connect(self.resolve_grievance)

        layout.addWidget(self.grievance_list)
        layout.addWidget(self.resolve_button)

        self.setLayout(layout)

        self.load_grievances()

    def load_grievances(self):
        grievances = session.query(Grievance).filter_by(status="Pending").all()

        for grievance in grievances:
            self.grievance_list.addItem(f"ID: {grievance.id}, User ID: {grievance.user_id}, Description: {grievance.description}")

    def resolve_grievance(self):
        selected_item = self.grievance_list.currentItem()
        if selected_item:
            grievance_id = int(selected_item.text().split(",")[0].split(":")[1].strip())
            grievance = session.query(Grievance).filter_by(id=grievance_id).first()
            grievance.status = "Resolved"
            session.commit()
            messagebox.information(self, "Success", "Grievance resolved successfully")
            self.load_grievances()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AdminDashboard()
    window.show()
    sys.exit(app.exec_())
