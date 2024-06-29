# auth/login.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from sqlalchemy.orm import sessionmaker
from database.models import engine, User
import bcrypt
from auth.google_login import GoogleLogin

Session = sessionmaker(bind=engine)
session = Session()

class LoginWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app  # Reference to MainApp instance
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Login")
        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.login_button = QPushButton("Login", self)
        self.login_button.clicked.connect(self.login)

        self.google_login_button = QPushButton("Login with Google", self)
        self.google_login_button.clicked.connect(self.google_login)

        layout.addWidget(QLabel("Login"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.login_button)
        layout.addWidget(self.google_login_button)

        self.setLayout(layout)

    def login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        user = session.query(User).filter_by(username=username).first()

        if user and bcrypt.checkpw(password.encode('utf-8'), user.password):
            QMessageBox.information(self, "Success", "Login successful")
            self.main_app.login()  # Update the login state in MainApp
            self.close()  # Close the login window
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password")

    def google_login(self):
        client_id = "1064475791928-cggetobfvf6ps5eo0igp68jce7gqqhi9.apps.googleusercontent.com"
        client_secret = "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"
        google_login = GoogleLogin(client_id, client_secret)
        user_info = google_login.login()

        if user_info:
            QMessageBox.information(self, "Success", f"Welcome {user_info['name']}")
            self.main_app.login()  # Update the login state in MainApp
            self.close()  # Close the login window

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = LoginWindow()
    window.show()
    sys.exit(app.exec_())
