# auth/register.py
import sys
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QLabel, QLineEdit, QPushButton, QMessageBox
from sqlalchemy.orm import sessionmaker
from database.models import engine, User
import bcrypt

Session = sessionmaker(bind=engine)

class RegisterWindow(QWidget):
    def __init__(self, main_app):
        super().__init__()
        self.main_app = main_app  # Reference to MainApp instance
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("Register")
        layout = QVBoxLayout()

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.Password)
        self.register_button = QPushButton("Register", self)
        self.register_button.clicked.connect(self.register)

        layout.addWidget(QLabel("Register"))
        layout.addWidget(self.username_input)
        layout.addWidget(self.password_input)
        layout.addWidget(self.register_button)

        self.setLayout(layout)

    def register(self):
        session = Session()
        try:
            username = self.username_input.text()
            password = self.password_input.text()
            hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())

            if session.query(User).filter_by(username=username).first():
                QMessageBox.warning(self, "Error", "Username already exists")
            else:
                new_user = User(username=username, password=hashed_password, role="user")
                session.add(new_user)
                session.commit()
                QMessageBox.information(self, "Success", "Registration successful")
                self.main_app.login()  # Log the user in after successful registration
                self.close()  # Close the registration window
        except Exception as e:
            session.rollback()
            QMessageBox.critical(self, "Error", f"An error occurred: {e}")
        finally:
            session.close()

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = RegisterWindow()
    window.show()
    sys.exit(app.exec_())
