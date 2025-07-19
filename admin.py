from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from functools import partial
from inventory import *
from registration import *
from scheduling import *
from report import *
from payment import *
from help import *
from about import *
from maintenance import *
from userlogs import *
from session_manager import *
class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setMaximumSize(1200, 800)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget_layout = QHBoxLayout(self.centralwidget)
        self.centralwidget_layout.setSpacing(0)
        self.centralwidget_layout.setContentsMargins(0, 0, 0, 0)

        self.side_frame = QFrame(self.centralwidget)
        self.side_frame.setMinimumSize(250, 800)
        self.side_frame.setStyleSheet("background-color: #002877")
        self.side_frame.setFrameShape(QFrame.StyledPanel)

        self.side_frame_layout = QVBoxLayout(self.side_frame)
        self.side_frame_layout.setSpacing(0)
        self.side_frame_layout.setContentsMargins(0, 0, 0, 0)

        self.logo_frame = QFrame(self.side_frame)
        self.logo_frame.setMinimumSize(150, 190)
        self.logo_frame.setMaximumSize(250, 190)

        self.logo = QLabel(self.logo_frame)
        self.logo.setGeometry(50, 20, 150, 150)
        self.logo.setStyleSheet("border-radius: 10px; background-color: #FFFFFF")
        self.logo.setPixmap(QPixmap("assets\slimmerslogo.jpg"))
        self.logo.setScaledContents(True)

        self.taskbar_frame = QFrame(self.side_frame)
        self.taskbar_frame.setMinimumSize(250, 550)
        self.taskbar_frame_layout = QVBoxLayout(self.taskbar_frame)
        self.taskbar_frame_layout.setSpacing(0)
        self.taskbar_frame_layout.setContentsMargins(0, 6, 0, 0)

        self.buttons = {}
        button_names = [
            "Inventory", "Registration", "Scheduling", "Reports", "Payment",
            "User Logs", "Maintenance", "Help", "About"
        ]

        FONT = QFont()
        FONT.setPointSize(16)

        for name in button_names:
            button = QPushButton(self.taskbar_frame)
            button.setObjectName(f"{name.lower()}_button")
            button.setMinimumSize(250, 60)
            button.setFont(FONT)
            button.setText(name)
            self.taskbar_frame_layout.addWidget(button)
            self.buttons[name.lower()] = button

        self.logout_frame = QFrame(self.side_frame)
        self.logout_frame.setMinimumSize(250, 60)

        self.logout_frame_layout = QVBoxLayout(self.logout_frame)
        self.logout_frame_layout.setSpacing(0)
        self.logout_frame_layout.setContentsMargins(0, 0, 0, 0)

        self.logout_button = QPushButton(self.logout_frame)
        self.logout_button.setMinimumSize(250, 60)
        self.logout_button.setFont(FONT)
        self.logout_button.setStyleSheet("background-color: #000000; color: #FFFFFF")

        self.main_frame = QFrame(self.centralwidget)
        self.main_frame.setMinimumSize(950, 800)
        self.main_frame.setStyleSheet("background-color: #FFFFFF")

        self.main_frame_layout = QVBoxLayout(self.main_frame)
        self.main_frame_layout.setSpacing(0)
        self.main_frame_layout.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget = QStackedWidget(self.main_frame)

        self.pages = {}

        # Create instances for each page and add them to stacked widget and pages dictionary
        self.inventory_page = Inventory()
        self.stacked_widget.addWidget(self.inventory_page)
        self.pages["inventory"] = self.inventory_page

        self.registration_page = Registration()
        self.stacked_widget.addWidget(self.registration_page)
        self.pages["registration"] = self.registration_page

        self.scheduling_page = Scheduling()
        self.stacked_widget.addWidget(self.scheduling_page)
        self.pages["scheduling"] = self.scheduling_page

        self.reports_page = Reports()
        self.stacked_widget.addWidget(self.reports_page)
        self.pages["reports"] = self.reports_page

        self.payment_page = Payment()
        self.stacked_widget.addWidget(self.payment_page)
        self.pages["payment"] = self.payment_page

        self.user_logs_page = UserLogs()
        self.stacked_widget.addWidget(self.user_logs_page)
        self.pages["user logs"] = self.user_logs_page  # Use "user logs" as the key


        self.maintenance_page = Maintenance()
        self.stacked_widget.addWidget(self.maintenance_page)
        self.pages["maintenance"] = self.maintenance_page

        self.help_page = Help()
        self.stacked_widget.addWidget(self.help_page)
        self.pages["help"] = self.help_page

        self.about_page = About()
        self.stacked_widget.addWidget(self.about_page)
        self.pages["about"] = self.about_page


        self.side_frame_layout.addWidget(self.logo_frame)
        self.side_frame_layout.addWidget(self.taskbar_frame)
        self.side_frame_layout.addWidget(self.logout_frame)
        self.logout_frame_layout.addWidget(self.logout_button)
        self.centralwidget_layout.addWidget(self.side_frame)
        self.main_frame_layout.addWidget(self.stacked_widget)
        self.centralwidget_layout.addWidget(self.main_frame)

        MainWindow.setCentralWidget(self.centralwidget)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle("Admin")
        self.logout_button.setText("Logout")

class Admin(QMainWindow):
    def __init__(self):
        super(Admin, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)
        
        for name, button in self.ui.buttons.items():
            button.clicked.connect(partial(self.switch_page, name))

        self.ui.logout_button.clicked.connect(self.handle_logout)

        self.update_button_styles("inventory")
        self.full_name = session_manager.get_full_name()
        
    def handle_logout(self):
        if session_manager.is_logged_in():
            session_manager.set_logged_in(False)
            session_manager.set_full_name(None)
            print(f"Logged out: {self.full_name}")
            self.show_login_window()
        else:
            QMessageBox.warning(self, "Logout Failed", "No user is currently logged in.")

    def show_login_window(self):
        from login import Login  # Import here to avoid circular import
        self.login_window = Login()
        self.login_window.show()
        self.close()

    def switch_page(self, page_name):
        if page_name in self.ui.pages:
            self.ui.stacked_widget.setCurrentWidget(self.ui.pages[page_name])
            self.update_button_styles(page_name)
        else:
            print(f"Page {page_name} not found.")

    def update_button_styles(self, active_page):
        for name, button in self.ui.buttons.items():
            if name == active_page:
                button.setStyleSheet("background-color: #FFFFFF; color: #000000;")
            else:
                button.setStyleSheet("background-color: transparent; color: #FFFFFF;")

if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Admin()
    window.show()
    sys.exit(app.exec_())