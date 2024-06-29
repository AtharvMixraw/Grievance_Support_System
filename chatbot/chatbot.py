# chatbot.py
import sys
from PyQt5.QtWidgets import QApplication, QDialog, QVBoxLayout, QLabel, QLineEdit, QTextEdit, QPushButton

class ChatbotWindow(QDialog):
    def __init__(self):
        super().__init__()
        self.init_ui()

    def init_ui(self):
        self.setWindowTitle("AI Chatbot")
        self.setGeometry(100, 100, 400, 300)
        
        layout = QVBoxLayout()
        
        self.chat_area = QTextEdit(self)
        self.chat_area.setReadOnly(True)
        
        self.user_input = QLineEdit(self)
        self.user_input.setPlaceholderText("Ask me how to use the system...")
        
        self.send_button = QPushButton("Send", self)
        self.send_button.clicked.connect(self.respond_to_query)
        
        layout.addWidget(QLabel("AI Chatbot"))
        layout.addWidget(self.chat_area)
        layout.addWidget(self.user_input)
        layout.addWidget(self.send_button)
        
        self.setLayout(layout)
    
    def respond_to_query(self):
        user_query = self.user_input.text().lower()
        self.chat_area.append(f"You: {user_query}")
        response = self.get_response(user_query)
        self.chat_area.append(f"Bot: {response}")
        self.user_input.clear()
    
    def get_response(self, query):
        responses = {
            "how do i login?": "To log in, go to the 'Auth' menu and select 'Login'. Enter your username and password, then click 'Login'.",
            "how do i register?": "To register, go to the 'Auth' menu and select 'Register'. Fill in the required details and click 'Register'.",
            "how do i submit a grievance?": "To submit a grievance, log in first, then go to the 'Grievances' menu and select 'Submit Grievance'. Fill in the form and submit.",
            "how do i track my grievances?": "To track your grievances, go to the 'Grievances' menu and select 'Track Grievances'. You can view the status of your submissions there.",
            "how do i use the admin dashboard?": "To use the admin dashboard, log in as an admin and go to the 'Admin' menu and select 'Admin Dashboard'. Here you can manage grievances."
        }
        return responses.get(query, "I'm sorry, I can only help with questions on how to use the system.")

if __name__ == '__main__':
    app = QApplication(sys.argv)
    chatbot = ChatbotWindow()
    chatbot.show()
    sys.exit(app.exec_())
