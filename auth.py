from PyQt6.QtWidgets import QWidget, QVBoxLayout, QLabel, QPushButton, QLineEdit, QMessageBox, QHBoxLayout
from PyQt6.QtCore import Qt
from user_data import load_users, save_user
from tasks import TaskManager

class AuthWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("PLAN-IT - Login/Signup")
        self.setGeometry(100, 100, 800, 600)
        self.initUI()

    def initUI(self):
        # Set a simple aureolin background
        self.setStyleSheet("background-color: #FDEE00;")

        # Create a layout for the login/signup form
        form_layout = QVBoxLayout()

        self.title_label = QLabel("PLAN IT", self)
        self.title_label.setStyleSheet("font-size: 50px; font-weight: bold; color: black;")
        form_layout.addWidget(self.title_label)

        self.username_input = QLineEdit(self)
        self.username_input.setPlaceholderText("Username")
        self.username_input.setStyleSheet("font-weight: bold; color: black;")
        form_layout.addWidget(self.username_input)

        self.password_input = QLineEdit(self)
        self.password_input.setPlaceholderText("Password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        self.password_input.setStyleSheet("font-weight: bold; color: black;")
        form_layout.addWidget(self.password_input)

        self.login_button = QPushButton("Login", self)
        self.login_button.setStyleSheet("font-weight: bold; color: black;")
        self.login_button.clicked.connect(self.login)
        form_layout.addWidget(self.login_button)

        self.signup_button = QPushButton("Sign Up", self)
        self.signup_button.setStyleSheet("font-weight: bold; color: black;")
        self.signup_button.clicked.connect(self.signup)
        form_layout.addWidget(self.signup_button)

        # Center the form widget
        form_container = QWidget(self)
        form_container_layout = QVBoxLayout(form_container)
        form_container_layout.addStretch()
        form_container_layout.addLayout(form_layout)
        form_container_layout.addStretch()

        main_layout = QHBoxLayout(self)
        main_layout.addStretch()
        main_layout.addWidget(form_container)
        main_layout.addStretch()

        self.setLayout(main_layout)

    def login(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        users = load_users()

        if username in users and users[username] == password:
            QMessageBox.information(self, "Success", "Login successful!")
            self.task_manager = TaskManager(username, self)
            self.task_manager.show()
            self.close()
        else:
            QMessageBox.warning(self, "Error", "Invalid username or password.")
            self.password_input.clear()

    def signup(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()

        if not username or not password:
            QMessageBox.warning(self, "Error", "Please enter both username and password.")
            return

        users = load_users()

        if username in users:
            QMessageBox.warning(self, "Error", "Username already exists.")
        else:
            save_user(username, password)
            QMessageBox.information(self, "Success", "Account created! Please log in.")
            self.username_input.clear()
            self.password_input.clear()