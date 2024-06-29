import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget, QPushButton, QComboBox, QMessageBox
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

        self.filter_by_recipient = QComboBox(self)
        self.filter_by_recipient.addItems(["All", "HR", "Manager", "IT Support"])  # Add more roles as needed
        self.filter_by_recipient.currentIndexChanged.connect(self.load_grievances)

        self.resolve_button = QPushButton("Resolve Selected Grievance")
        self.resolve_button.clicked.connect(self.resolve_grievance)

        layout.addWidget(QLabel("Filter by Recipient"))
        layout.addWidget(self.filter_by_recipient)
        layout.addWidget(self.grievance_list)
        layout.addWidget(self.resolve_button)

        self.setLayout(layout)

        self.load_grievances()

    def load_grievances(self):
        recipient = self.filter_by_recipient.currentText()
        if recipient == "All":
            grievances = session.query(Grievance).filter_by(status="Pending").all()
        else:
            grievances = session.query(Grievance).filter_by(status="Pending", recipient=recipient).all()

        self.grievance_list.clear()
        for grievance in grievances:
            self.grievance_list.addItem(f"ID: {grievance.id}, User ID: {grievance.user_id}, Description: {grievance.description}, Recipient: {grievance.recipient}")

    def resolve_grievance(self):
        selected_item = self.grievance_list.currentItem()
        if selected_item:
            grievance_id = int(selected_item.text().split(",")[0].split(":")[1].strip())
            grievance = session.query(Grievance).filter_by(id=grievance_id).first()
            grievance.status = "Resolved"
            session.commit()

            # Show success message
            QMessageBox.information(self, "Success", "Grievance resolved successfully")

            # Prompt to quit or continue
            quit_reply = QMessageBox.question(self, 'Quit Application', 'Do you want to quit the application?',
                                              QMessageBox.Yes | QMessageBox.No, QMessageBox.No)
            if quit_reply == QMessageBox.Yes:
                sys.exit()  # Quit the application
            else:
                self.load_grievances()  # Reload grievances

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = AdminDashboard()
    window.show()
    sys.exit(app.exec_())
