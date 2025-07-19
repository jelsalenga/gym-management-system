from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
from functools import partial
from session_manager import session_manager
from inventory import Inventory
from registration import Registration
from scheduling import Scheduling
from report import Reports
from payment import Payment
from help import Help
from about import About

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1200, 800)
        MainWindow.setMaximumSize(1200, 800)

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")

        self.centralwidget_layout = QHBoxLayout(self.centralwidget)
        self.centralwidget_layout.setSpacing(0)
        self.centralwidget_layout.setContentsMargins(0, 0, 0, 0)

        self.side_frame = QFrame(self.centralwidget)
        self.side_frame.setObjectName("side_frame")
        self.side_frame.setMinimumSize(QSize(250, 800))
        self.side_frame.setStyleSheet("background-color: #002877")
        self.side_frame.setFrameShape(QFrame.StyledPanel)

        self.side_frame_layout = QVBoxLayout(self.side_frame)
        self.side_frame_layout.setSpacing(0)
        self.side_frame_layout.setContentsMargins(0, 0, 0, 0)

        self.logo_frame = QFrame(self.side_frame)
        self.logo_frame.setObjectName("logo_frame")
        self.logo_frame.setMinimumSize(QSize(150, 190))
        self.logo_frame.setMaximumSize(QSize(250, 190))
        self.logo_frame.setStyleSheet("")

        self.logo = QLabel(self.logo_frame)
        self.logo.setObjectName("logo")
        self.logo.setGeometry(QRect(50, 20, 150, 150))
        self.logo.setMinimumSize(QSize(0, 0))
        self.logo.setMaximumSize(QSize(16777215, 16777215))
        self.logo.setStyleSheet("border-radius: 75px; background-color: #FFFFFF")
        self.logo.setPixmap(QPixmap("../../Downloads/slimmerslogo-removebg-preview.png"))
        self.logo.setScaledContents(True)

        self.taskbar_frame = QFrame(self.side_frame)
        self.taskbar_frame.setObjectName("taskbar_frame")
        self.taskbar_frame.setMinimumSize(QSize(250, 550))
        self.taskbar_frame.setStyleSheet("")
        self.taskbar_frame.setFrameShape(QFrame.StyledPanel)
        self.taskbar_frame.setFrameShadow(QFrame.Raised)
        self.taskbar_frame_layout = QVBoxLayout(self.taskbar_frame)
        self.taskbar_frame_layout.setSpacing(0)
        self.taskbar_frame_layout.setObjectName("taskbar_frame_layout")
        self.taskbar_frame_layout.setContentsMargins(0, 6, 0, 0)

        self.buttons = {}
        button_names = [
            "Inventory", "Registration", "Scheduling", "Reports",
            "Payment", "Help", "About"
        ]

        FONT = QFont()
        FONT.setPointSize(16)

        # Creating the Buttons
        for name in button_names:
            button = QPushButton(self.taskbar_frame)
            button.setObjectName(f"{name.lower()}_button")
            button.setMinimumSize(QSize(250, 60))
            button.setFont(FONT)
            button.setText(name)
            self.taskbar_frame_layout.addWidget(button)
            self.buttons[name.lower()] = button

        self.logout_frame = QFrame(self.side_frame)
        self.logout_frame.setObjectName("logout_frame")
        self.logout_frame.setMinimumSize(QSize(250, 60))
        self.logout_frame.setStyleSheet("background-color: #000000")

        self.logout_frame_layout = QVBoxLayout(self.logout_frame)
        self.logout_frame_layout.setSpacing(0)
        self.logout_frame_layout.setObjectName("logout_frame_layout")
        self.logout_frame_layout.setContentsMargins(0, 0, 0, 0)

        self.logout_button = QPushButton(self.logout_frame)
        self.logout_button.setObjectName("logout_button")
        self.logout_button.setMinimumSize(QSize(250, 60))
        self.logout_button.setFont(FONT)
        self.logout_button.setStyleSheet("color: #FFFFFF")

        self.main_frame = QFrame(self.centralwidget)
        self.main_frame.setObjectName("main_frame")
        self.main_frame.setMinimumSize(QSize(950, 800))
        self.main_frame.setStyleSheet("background-color: #FFFFFF")
        self.main_frame_layout = QVBoxLayout(self.main_frame)
        self.main_frame_layout.setSpacing(0)
        self.main_frame_layout.setObjectName("main_frame_layout")
        self.main_frame_layout.setContentsMargins(0, 0, 0, 0)

        self.stacked_widget = QStackedWidget(self.main_frame)
        self.stacked_widget.setObjectName("stacked_widget")

        self.pages = {}
        page_classes = [Inventory, Registration, Scheduling, Reports, Payment, Help, About]
        for page_class in page_classes:
            page_instance = page_class()
            page_name = page_class.__name__.lower()
            page_instance.setObjectName(page_name)
            self.stacked_widget.addWidget(page_instance)
            self.pages[page_name] = page_instance

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
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "MainWindow", None))
        self.logout_button.setText(QCoreApplication.translate("MainWindow", "Logout", None))


class Staff(QMainWindow):
    def __init__(self):
        super(Staff, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # Connect the buttons to switch to the appropriate page
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
        self.ui.stacked_widget.setCurrentWidget(self.ui.pages[page_name])
        self.update_button_styles(page_name)

    def update_button_styles(self, active_page):
        for name, button in self.ui.buttons.items():
            if name == active_page:
                button.setStyleSheet("background-color: #FFFFFF; color: #000000;")
            else:
                button.setStyleSheet("background-color: transparent; color: #FFFFFF;")


if __name__ == "__main__":
    import sys
    app = QApplication(sys.argv)
    window = Staff()
    window.show()
    sys.exit(app.exec_())
