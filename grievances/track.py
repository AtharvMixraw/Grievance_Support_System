# track.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QListWidget
from sqlalchemy.orm import sessionmaker
from database.models import engine, Grievance

Session = sessionmaker(bind=engine)
session = Session()

class TrackGrievancesWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Track Grievances")
        layout = QVBoxLayout()

        self.grievance_list = QListWidget()
        layout.addWidget(self.grievance_list)

        self.setLayout(layout)

        self.load_grievances()

    def load_grievances(self):
        grievances = session.query(Grievance).filter_by(user_id=1).all()  # Replace with dynamic user ID

        for grievance in grievances:
            self.grievance_list.addItem(f"ID: {grievance.id}, Status: {grievance.status}, Description: {grievance.description}, Recipient: {grievance.recipient}")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TrackGrievancesWindow()
    window.show()
    sys.exit(app.exec_())
