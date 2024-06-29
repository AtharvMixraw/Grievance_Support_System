import sys
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QAction, QMessageBox,
    QLabel, QVBoxLayout, QWidget, QPushButton
)
from PyQt5.QtGui import QPixmap, QPalette, QColor
from PyQt5.QtCore import Qt

# Assuming you have these imports for your specific windows
from auth.login import LoginWindow
from auth.register import RegisterWindow
from grievances.submit import SubmitGrievanceWindow
from grievances.track import TrackGrievancesWindow
from admin.dashboard import AdminDashboard
from chatbot import ChatbotWindow  # Import the ChatbotWindow class

class MainApp(QMainWindow):
    def __init__(self):
        super().__init__()
        self.is_logged_in = False
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Organizational Grievance Support System")
        self.setGeometry(100, 100, 1440, 900)  # Set the window size to match the MacBook Air 2017 screen

        # Create central widget and layout
        central_widget = QWidget()
        layout = QVBoxLayout()

        # Project name
        project_name = QLabel("Grievance Management System")
        project_name.setStyleSheet("font-size: 50px; font-weight: bold; color: #7776B3;")
        project_name.setAlignment(Qt.AlignCenter)

        # Set background image
        background_image = QPixmap("background_image.jpg")  # Replace with your background image path
        background_label = QLabel(self)
        background_label.setPixmap(background_image)
        background_label.setGeometry(0, 0, 1440, 900)  # Set the size to match window size

        # Heading for AI Chatbot
        chatbot_heading = QLabel("Facing problem using our platform? Try this bot!")
        chatbot_heading.setStyleSheet("font-size: 25px; font-weight: bold; color: #9B86BD;")
        chatbot_heading.setAlignment(Qt.AlignCenter)

        # Instructions on what questions to ask
        chatbot_instructions = QLabel(
            "You can ask the bot questions like:\n"
            "- How do I login?\n"
            "- How do I register?\n"
            "- How do I submit a grievance?\n"
            "- How do I track my grievances?\n"
            "- How do I use the admin dashboard?\n"
            "\n"
            "NOTE: ASK THE QUESTIONS GIVEN IN ABOVE FORMAT ONLY !!"
        )
        chatbot_instructions.setStyleSheet("font-size: 20px; color: #2F4F4F;")
        chatbot_instructions.setAlignment(Qt.AlignCenter)

        # Chatbot button
        chatbot_button = QPushButton("AI Chatbot", self)
        chatbot_button.setStyleSheet("font-size: 16px; background-color: #4682B4; color: #FFFFFF;")
        chatbot_button.clicked.connect(self.show_chatbot)

        # Add widgets to layout
        layout.addWidget(project_name)
        layout.addWidget(chatbot_heading)
        layout.addWidget(chatbot_instructions)
        layout.addWidget(chatbot_button)
        central_widget.setLayout(layout)
        self.setCentralWidget(central_widget)

        menubar = self.menuBar()
        auth_menu = menubar.addMenu("Auth")
        grievances_menu = menubar.addMenu("Grievances")
        admin_menu = menubar.addMenu("Admin")
        help_menu = menubar.addMenu("Help")  # Add Help menu for chatbot

        login_action = QAction("Login", self)
        login_action.triggered.connect(self.show_login)
        register_action = QAction("Register", self)
        register_action.triggered.connect(self.show_register)
        submit_grievance_action = QAction("Submit Grievance", self)
        submit_grievance_action.triggered.connect(self.show_submit_grievance)
        track_grievance_action = QAction("Track Grievances", self)
        track_grievance_action.triggered.connect(self.show_track_grievances)
        admin_dashboard_action = QAction("Admin Dashboard", self)
        admin_dashboard_action.triggered.connect(self.show_admin_dashboard)
        chatbot_action = QAction("AI Chatbot", self)  # Chatbot menu action
        chatbot_action.triggered.connect(self.show_chatbot)

        auth_menu.addAction(login_action)
        auth_menu.addAction(register_action)
        grievances_menu.addAction(submit_grievance_action)
        grievances_menu.addAction(track_grievance_action)
        admin_menu.addAction(admin_dashboard_action)
        help_menu.addAction(chatbot_action)  # Add chatbot action to Help menu

    def show_login(self):
        self.login_window = LoginWindow(self)  # Pass the main app to login window
        self.login_window.show()

    def show_register(self):
        self.register_window = RegisterWindow(self)  # Pass the main app to register window
        self.register_window.show()

    def show_submit_grievance(self):
        if self.is_logged_in:
            self.submit_grievance_window = SubmitGrievanceWindow()
            self.submit_grievance_window.show()
        else:
            QMessageBox.warning(self, "Warning", "You need to log in to submit a grievance.")

    def show_track_grievances(self):
        self.track_grievances_window = TrackGrievancesWindow()
        self.track_grievances_window.show()

    def show_admin_dashboard(self):
        self.admin_dashboard_window = AdminDashboard()
        self.admin_dashboard_window.show()

    def show_chatbot(self):
        self.chatbot_window = ChatbotWindow()
        self.chatbot_window.show()

    def login(self):
        self.is_logged_in = True

    def logout(self):
        self.is_logged_in = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    main_app = MainApp()
    main_app.show()
    sys.exit(app.exec_())