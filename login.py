import sqlite3
import hashlib
from PySide2.QtCore import QSize, Qt, QCoreApplication
from PySide2.QtGui import QPixmap, QFont
from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QLabel, QLineEdit, QPushButton, QMessageBox
from staff import *
from admin import *
from assets import *
from session_manager import session_manager


class Login(QMainWindow):
    global current_username

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Login Window")
        self.resize(1200, 800)
        self.setMaximumSize(QSize(1200, 800))
        self.setStyleSheet("background-color: #002877")
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.user_interface()

    def user_interface(self):
        self.fonts()
        self.logo()
        self.input_fields()
        self.login_button()

    def fonts(self):
        self.username_password_font = QFont()
        self.username_password_font.setPointSize(12)
        self.login_font = QFont()
        self.login_font.setPointSize(12)
        self.login_font.setBold(True)

    def logo(self):
        border_logo_style = "background-color: #FFFFFF; border: 5px solid; border-radius: 75px"
        self.border_logo = QLabel(self.central_widget, objectName="border_logo")
        self.border_logo.setGeometry(360, 30, 500, 720)
        self.border_logo.setStyleSheet(border_logo_style)

        logo_style = "border-radius: 75px"
        self.logo = QLabel(self.central_widget, objectName="logo")
        self.logo.setGeometry(490, 80, 261, 571)
        self.logo.setStyleSheet(logo_style)
        self.logo.setPixmap(QPixmap("assets/slimmers_login.png"))
        self.logo.setScaledContents(True)

    def input_fields(self):
        label_style = "background-color: #FFFFFF"
        input_style = "background-color: #D9D9D9"
        self.username_label = QLabel("Username", self.central_widget, objectName="username_label")
        self.username_label.setGeometry(440, 460, 71, 16)
        self.username_label.setFont(self.username_password_font)
        self.username_label.setStyleSheet(label_style)

        self.username_input = QLineEdit(self.central_widget, objectName="username_input")
        self.username_input.setGeometry(440, 480, 341, 31)
        self.username_input.setStyleSheet(input_style)

        self.password_label = QLabel("Password", self.central_widget, objectName="password_label")
        self.password_label.setGeometry(440, 530, 71, 16)
        self.password_label.setFont(self.username_password_font)
        self.password_label.setStyleSheet(label_style)

        self.password_input = QLineEdit(self.central_widget, objectName="password_input")
        self.password_input.setGeometry(440, 550, 341, 31)
        self.password_input.setStyleSheet(input_style)
        self.password_input.setEchoMode(QLineEdit.Password)

    def login_button(self):
        button_style = "background-color: #002877; border-radius: 10px;"
        self.login_button = QPushButton("Login", self.central_widget, objectName="login_button")
        self.login_button.setGeometry(560, 600, 111, 41)
        self.login_button.setFont(self.login_font)
        self.login_button.setStyleSheet(button_style)
        self.login_button.clicked.connect(self.handle_login)

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()

        valid, role, employee_id = self.check_credentials(username, password)
        if valid:
            full_name = self.get_full_name(employee_id)
            session_manager.set_full_name(full_name)
            session_manager.set_logged_in(True)  # Set login status to true
            print(f"Logged in as: {full_name} ({current_username})")
            QMessageBox.information(None, "Login Successful", f"Welcome {full_name}")
            get_user_log("Login", username)
            set_username_global(current_username)
            self.open_main_window()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        valid, role, employee_id = self.check_credentials(username, password)
        if valid and role == "Admin":
            full_name = self.get_full_name(employee_id)
            session_manager.set_full_name(full_name)
            session_manager.set_role("Admin")
            session_manager.set_logged_in(True)  # Set login status to true
            print(f"Logged in as: {full_name} ({current_username})")
            QMessageBox.information(None, "Login Successful", f"Welcome {full_name}")
            get_user_log("Login", username)
            set_username_global(current_username)
            self.open_main_window()
        elif valid and role == "Staff":
            full_name = self.get_full_name(employee_id)
            session_manager.set_full_name(full_name)
            session_manager.set_role("Staff")
            session_manager.set_logged_in(True)  # Set login status to true
            print(f"Logged in as: {full_name} ({current_username})")
            QMessageBox.information(None, "Login Successful", f"Welcome {full_name}")
            get_user_log("Login", username)
            set_username_global(current_username)
            self.open_main_window()
        else:
            QMessageBox.warning(self, "Login Failed", "Invalid username or password.")

    def open_main_window(self):
        if session_manager.get_role() == "Admin":
            from admin import Admin  # Delayed import
            self.main_window = Admin()
        elif session_manager.get_role() == "Staff":
            from staff import Staff  # Delayed import
            self.main_window = Staff()
        self.main_window.show()
        self.close()
    def handle_logout(self):
        if not session_manager.is_logged_in():
            QMessageBox.warning(self, "Logout Failed", "No user is currently logged in.")
            return

        username = session_manager.get_full_name()
        record_log(username, "Logout")
        session_manager.set_logged_in(False)
        session_manager.set_full_name(None)
        print(f"Logged out: {username}")
        self.show_login_window()

    def show_login_window(self):
        self.login_window = Login()
        self.login_window.show()
        self.close()


    def check_credentials(self, username, password):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute('''
        SELECT employee_id, password_hash, role FROM Users WHERE username = ?
        ''', (username,))
        result = cursor.fetchone()
        connection.close()

        if result:
            employee_id, password_hash, role = result
            if self.verify_password(password, password_hash):
                print(f"Logged in as {role}")
                return True, role, employee_id
            else:
                QMessageBox.warning(None, "Login Failed", "Invalid password.")
        else:
            QMessageBox.warning(None, "Login Failed", "Invalid username.")

        return False, None, None

    def verify_password(self, password, password_hash):
        # Assuming password_hash is stored as SHA256 hash
        password_bytes = password.encode()
        hashed_password = hashlib.sha256(password_bytes).hexdigest()
        return hashed_password == password_hash

    def get_full_name(self, employee_id):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute('''
        SELECT first_name, middle_name, last_name FROM Employees WHERE employee_id = ?
        ''', (employee_id,))
        result = cursor.fetchone()
        connection.close()

        if result:
            first_name, middle_name, last_name = result
            full_name = f"{first_name} {middle_name} {last_name}".strip()
            return full_name
        return None

    def handle_logout(self):
        # Example of handling logout
        if 'current_username' in globals():
            username = current_username
            record_log(username, "Logout")
        else:
            # Handle case where no user is logged in
            QMessageBox.warning(self, "Logout Failed", "No user is currently logged in.")

        # Close current window and possibly return to the login screen
        self.close()

    def get_employee_id(self, username):
        connection = sqlite3.connect('database.db')
        cursor = connection.cursor()

        cursor.execute('''
        SELECT employee_id FROM Users WHERE username = ?
        ''', (username,))
        result = cursor.fetchone()
        connection.close()

        if result:
            return result[0]
        return None

def record_log(username, action):
        cursor.execute('''
        INSERT INTO UserLog (username, action) VALUES (?, ?)
        ''', (username, action))

        connection.commit()
        connection.close()

if __name__ == "__main__":
    app = QApplication([])
    window = Login()
    window.show()
    app.exec_()