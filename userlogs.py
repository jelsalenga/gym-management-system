from PySide2.QtCore import *
from PySide2.QtGui import *
from PySide2.QtWidgets import *
import sys
from assets import *
class UserLogs(QMainWindow):  # Inherit from QWidget
    def __init__(self, parent=None):
        super(UserLogs, self).__init__(parent)
        self.setObjectName("Form")
        self.resize(950, 800)
        self.setStyleSheet("background-color: #FFFFFF")
        self.open_user_logs_page()

    def open_user_logs_page(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.verticalLayout = QVBoxLayout(self.central_widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.central_widget)
        self.stackedWidget.setObjectName("stackedWidget")

        
        self.open_user_logs_main_page()
        self.verticalLayout.addWidget(self.stackedWidget)
        self.stackedWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(self)

    def open_user_logs_main_page(self):
        self.user_log_page = QWidget()
        self.user_log_page.setObjectName("user_log_page")
        self.stackedWidget.addWidget(self.user_log_page)


        self.user_logs_text_label = createLabel(
            parent=self.user_log_page,
            name="schedule_appointment_text",
            geometry=QRect(400, 60, 400, 40),
            text="User Logs",
            font=font4,
            style="font: bold"
        )

        self.user_log_table = QTableWidget(self.user_log_page)
        self.user_log_table.setGeometry(QRect(40, 120, 890, 650))
        self.user_log_table.setColumnCount(4)
        self.user_log_table.setHorizontalHeaderLabels(
            ["Log ID","Username", "Action", "Time Stamp"])
        self.user_log_table.horizontalHeader().setStretchLastSection(True)
        self.user_log_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)


        self.refresh_button = createButton(
            parent=self.user_log_page,
            name="add_appointment",
            geometry=QRect(820, 50, 100, 50),
            text="Refresh",
            font=font3,
            style="background-color: #28a745; color: #FFFFFF"
        )
        self.refresh_button.clicked.connect(self.load_logs)
        self.load_logs()

    
    def load_logs(self):
        self.user_log_table.setRowCount(0)  # Clear existing rows

        cursor.execute('''
            SELECT * FROM UserLog ORDER BY log_id DESC
            ''')


        for row_number, row_data in enumerate(cursor.fetchall()):
            self.user_log_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))  # Convert data to string for QTableWidgetItem
                self.user_log_table.setItem(row_number, column_number, item)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = UserLogs()
    window.show()
    sys.exit(app.exec_())
