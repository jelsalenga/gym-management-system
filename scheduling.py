from PySide2.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QStackedWidget, QCalendarWidget, QTableWidget, QHeaderView, QTableWidgetItem, QPushButton, QComboBox, QLabel, QLineEdit, QTimeEdit
from PySide2.QtCore import QRect, QMetaObject, QDate
from assets import *  # Assuming assets contains the font and style definitions
import sys
import random
class Scheduling(QMainWindow):
    def __init__(self, parent=None):
        super(Scheduling, self).__init__(parent)
        self.setObjectName("Form")
        self.resize(950, 800)
        self.setStyleSheet("background-color: #FFFFFF")
        self.open_scheduling_page()

    def open_scheduling_page(self):
        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)
        self.verticalLayout = QVBoxLayout(self.central_widget)
        self.verticalLayout.setSpacing(0)
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.stackedWidget = QStackedWidget(self.central_widget)
        self.stackedWidget.setObjectName("stackedWidget")

        
        self.open_main_page()
        self.open_add_appointment_page()

        self.verticalLayout.addWidget(self.stackedWidget)
        self.stackedWidget.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(self)

    
    def show_main_appointment_page(self):
        self.stackedWidget.setCurrentIndex(0)

    def show_add_appointment_page(self):
        clear_inputs(self.schedule_page)
        self.stackedWidget.setCurrentIndex(1)

    def open_main_page(self):
        self.main_page = QWidget()
        self.main_page.setObjectName("main_page")
        self.stackedWidget.addWidget(self.main_page)

        self.calendar_widget = QCalendarWidget(self.main_page)
        self.calendar_widget.setGeometry(QRect(0, 0, 951, 411))
        self.calendar_widget.setVerticalHeaderFormat(QCalendarWidget.NoVerticalHeader)
        self.calendar_widget.setStyleSheet(
            """
            QCalendarWidget QWidget {
                background-color: #FFFFFF;
                alternate-background-color: #E0E0E0;
            }
            QCalendarWidget QAbstractItemView:enabled {
                background-color: #FFFFFF;
                color: #000000;
                selection-background-color: #0000FF;
                selection-color: #FFFFFF;
            }
            QCalendarWidget QAbstractItemView:disabled {
                color: #CCCCCC;
            }
            QCalendarWidget QWidget#qt_calendar_navigationbar {
                background-color: #0000FF;
                color: #FFFFFF;
            }
            QCalendarWidget QToolButton {
                background-color: #0000FF;
                color: #FFFFFF;
                border: none;
                margin: 5px;
                padding: 5px;
            }
            QCalendarWidget QToolButton::hover {
                background-color: #0000CC;
            }
            QCalendarWidget QAbstractItemView:enabled {
                selection-background-color: #0000FF;
                selection-color: #FFFFFF;
            }
            """
        )
        self.calendar_widget.clicked.connect(self.show_appointments)

        self.appointments_table = QTableWidget(self.main_page)
        self.appointments_table.setGeometry(QRect(0, 410, 950, 310))
        self.appointments_table.setColumnCount(7)
        self.appointments_table.setHorizontalHeaderLabels(
            ["Schedule ID","Member Name", "Employee Name", "Start Time", "End Time", "Name", "Status"])
        self.appointments_table.horizontalHeader().setStretchLastSection(True)
        self.appointments_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)

        self.add_appointment_button = createButton(
            parent=self.main_page,
            name="add_appointment",
            geometry=QRect(700, 740, 240, 50),
            text="Schedule",
            font=font3,
            style="background-color: #28a745; color: #FFFFFF"
        )

        self.cancel_appointment_button = createButton(
            parent=self.main_page,
            name="cancel_appointment",
            geometry=QRect(520, 740, 170, 50),
            text="Cancel",
            font=font3,
            style="background-color: #882400; color: #FFFFFF"
        )

        self.cancel_appointment_button.clicked.connect(self.cancel_appointment)
        self.add_appointment_button.clicked.connect(self.show_add_appointment_page)
    def show_appointments(self, date):
        self.appointments_table.setRowCount(0)
        date_str = date.toString("yyyy-MM-dd")
        cursor.execute('''
                SELECT  s.schedule_id,
                        m.first_name || ' ' || m.last_name AS member_name, 
                        e.first_name || ' ' || e.last_name AS employee_name, 
                        s.appointment_start_time, 
                        s.appointment_end_time, 
                        s.appointment_name, 
                        s.status 
                    FROM Schedule s
                    JOIN Members m ON s.member_id = m.member_id
                    JOIN Employees e ON s.employee_id = e.employee_id
                    WHERE s.appointment_date = ? AND s.status != "Cancelled"
        ''', (date_str,))
        for row in cursor.fetchall():
            row_position = self.appointments_table.rowCount()
            self.appointments_table.insertRow(row_position)
            for column, data in enumerate(row):
                self.appointments_table.setItem(row_position, column, QTableWidgetItem(str(data)))

    def open_add_appointment_page(self):
        self.schedule_page = QWidget()
        self.schedule_page.setObjectName("schedule_page")
        self.stackedWidget.addWidget(self.schedule_page)

        self.schedule_text_label = createLabel(
            parent=self.schedule_page,
            name="schedule_appointment_text",
            geometry=QRect(290, 60, 400, 40),
            text="Schedule Appointment",
            font=font4,
            style="font: bold"
        )

        self.member_name_label = createLabel(
            parent=self.schedule_page,
            name="member_name",
            geometry=QRect(50, 140, 190, 40),
            text="Member Name:",
            font=font1,
            style=""
        )

        self.member_id_label = createLabel(
            parent=self.schedule_page,
            name="member_id",
            geometry=QRect(50, 200, 190, 40),
            text="Member ID",
            font=font1,
            style=""
        )

        self.membership_type_label = createLabel(
            parent=self.schedule_page,
            name="membership_type",
            geometry=QRect(380, 200, 210, 40),
            text="Membership Type",
            font=font1,
            style=""
        )

        self.employee_name_label = createLabel(
            parent=self.schedule_page,
            name="employee_name",
            geometry=QRect(50, 330, 190, 40),
            text="Employee Name",
            font=font1,
            style=""
        )

        self.employee_id_label = createLabel(
            parent=self.schedule_page,
            name="employee_id",
            geometry=QRect(50, 390, 190, 40),
            text="Employee ID",
            font=font1,
            style=""
        )

        self.employee_position_label = createLabel(
            parent=self.schedule_page,
            name="employee_position",
            geometry=QRect(390, 390, 130, 40),
            text="Position",
            font=font1,
            style=""
        )

        self.appointment_type_label = createLabel(
            parent=self.schedule_page,
            name="appointment_type",
            geometry=QRect(50, 510, 220, 40),
            text="Appointment Type",
            font=font1,
            style=""
        )

        self.appointment_name_label = createLabel(
            parent=self.schedule_page,
            name="appointment_name",
            geometry=QRect(300, 510, 230, 40),
            text="Appointment Name",
            font=font1,
            style=""
        )

        self.date_label = createLabel(
            parent=self.schedule_page,
            name="appointment_name",
            geometry=QRect(560, 510, 230, 40),
            text="Date",
            font=font1,
            style=""
        )

        self.start_time_label = createLabel(
            parent = self.schedule_page,
            name = "start_time",
            geometry = QRect(50, 620, 130, 40),
            text = "Start Time",
            font = font1,
            style = ""
        )

        self.end_time_label = createLabel(
            parent = self.schedule_page,
            name = "end_time",
            geometry = QRect(310, 620, 130, 40),
            text = "End Time",
            font = font1,
            style = ""
        )


        self.member_id_output = createLabel(
            parent=self.schedule_page,
            name="output",
            geometry=QRect(50, 250, 330, 40),
            text="",
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )   

        self.membership_type_output = createLabel(
            parent=self.schedule_page,
            name="output",
            geometry=QRect(390, 250, 260, 40),
            text="",
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        self.employee_id_output = createLabel(
            parent=self.schedule_page,
            name="output",
            geometry=QRect(50, 440, 330, 40),
            text="",
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        self.position_output = createLabel(
            parent=self.schedule_page,
            name="output",
            geometry=QRect(390, 440, 330, 40),
            text="",
            font=font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )
        
        self.image_output = createLabel(
            parent = self.schedule_page,
            name = "output",
            geometry = QRect(680, 140, 250, 250),
            text = "",
            font = font2,
            style = "background-color: #F9F7FF; border: 1px solid black"
        )

        self.member_name_input = createLineInput(
            parent = self.schedule_page,
            name = "member_input",
            geometry = QRect(250, 140, 410, 40),
            font = font2,
            style = "background-color: #F9F7FF; border: 1px solid black"
        )


        self.employee_name_input = createLineInput(
            parent = self.schedule_page,
            name = "employee_input",
            geometry = QRect(250, 330, 410, 40),
            font = font2,
            style = "background-color: #F9F7FF; border: 1px solid black"
        )

        self.member_name_input.setPlaceholderText("Search Member Name")
        self.member_name_input.textChanged.connect(self.update_member_search_results)

        self.employee_name_input.setPlaceholderText("Search Employee Name")
        self.employee_name_input.textChanged.connect(self.update_employee_search_results)
        
        self.member_search_results = QListWidget(self.schedule_page)
        self.member_search_results.hide()  # Hide initially
        self.member_search_results.setGeometry(250, 180, 410, 150)
        self.member_search_results.setFont(font2)

        self.member_search_results.itemClicked.connect(self.handle_member_item_selection)

        self.employee_search_results = QListWidget(self.schedule_page)
        self.employee_search_results.hide()  # Hide initially
        self.employee_search_results.setGeometry(250, 370, 410, 150)
        self.employee_search_results.setFont(font2)

        self.employee_search_results.itemClicked.connect(self.handle_employee_item_selection)


        self.date = createDate(
            parent = self.schedule_page,
            name = "date",
            geometry = QRect(560, 550, 200, 40),
            font = font2,
            style= "background-color: #F9F7FF; border: 1px solid black",
        )
        self.appointment_type_combo_box = QComboBox(self.schedule_page)
        self.appointment_type_combo_box.setGeometry(QRect(50, 560, 230, 40))
        self.appointment_type_combo_box.setStyleSheet("background-color: #F9F7FF; border: 1px solid black")
        self.appointment_type_combo_box.setFont(font2)

        self.appointment_name_combo_box = QComboBox(self.schedule_page)
        self.appointment_name_combo_box.setGeometry(QRect(300, 560, 230, 40))
        self.appointment_name_combo_box.setStyleSheet("background-color: #F9F7FF; border: 1px solid black")
        self.appointment_name_combo_box.setFont(font2)
        # Example data to fill appointment_type_combo_box
        self.appointment_type_combo_box.addItems(["Body Treatments", "Fitness Programs", "Face & Skin Programs"])

        # Connect signal to slot
        self.appointment_type_combo_box.currentIndexChanged.connect(self.update_appointments)


        self.start_time = createTime(
            parent = self.schedule_page,
            name = "start_time",
            geometry = QRect(50, 670, 200, 40),
            font = font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        self.end_time = createTime(
            parent = self.schedule_page,
            name = "end_time",
            geometry = QRect(310, 670, 200, 40),
            font = font2,
            style="background-color: #F9F7FF; border: 1px solid black"
        )

        # BACK BUTTON
        self.member_back_button = createButton(
            parent = self.schedule_page,
            name = "back_button",
            geometry = QRect(40, 50, 70, 50),
            text = "Back",
            font = font3,
            style = "background-color: #004F9A"
        )

        # CLEAR BUTTON
        self.schedule_clear_button = createButton(
            parent = self.schedule_page,
            name = "clear_button",
            geometry = QRect(510, 730, 170, 50),
            text = "Clear",
            font = font3,
            style = "background-color: #882400"
        )

        # REGISTER BUTTON
        self.schedule_register_button = createButton(
            parent = self.schedule_page,
            name = "register_button",
            geometry = QRect(690, 730, 250, 50),
            text = "Register",
            font = font3,
            style = "background-color: #006646"
        )

        self.schedule_clear_button.clicked.connect(lambda: clear_inputs(self.schedule_page))
        self.schedule_register_button.clicked.connect(self.add_appointment)
        self.member_back_button.clicked.connect(self.show_main_appointment_page)

    def update_appointments(self):
        selected_type = self.appointment_type_combo_box.currentText()
        print(f"Selected appointment type: {selected_type}")  # Debug print

        self.appointment_name_combo_box.clear()

        if selected_type == "Body Treatments":
            self.appointment_name_combo_box.addItems([
                "Aromatherapy", "Biolift", "Body Former", "Bodytight FX",
                "Cellu-O", "Cellulite Cure Massage", "Chili Masque", "Coreshape",
                "emPULSE 360", "Endoslim", "G5", "Hot Masque", "Hot Stone Massage",
                "Le Shape", "Liposure", "Maximus", "Megaslim", "Pro Trim",
                "Quick Slim", "Reflexology", "Swedish Massage", "Thermasque",
                "Thermoslim", "Ultra Cellulite Treatment", "Ultraflex", "Ultraform",
                "Venus Freeze", "Vitastin"
            ])
        elif selected_type == "Fitness Programs":
            self.appointment_name_combo_box.addItems(["Aerobics Class", "Biometric Intensive Inch Loss Program",
                "Biometrics Intensive Weight Loss Program", "Corefit", "Cykl Squad",
                "Passive Slimming Program", "Personal Training", "Power Stretching",
                "Powerbox", "Squad Core"])
        elif selected_type == "Face & Skin Programs":
            self.appointment_name_combo_box.addItems(["Aquafacial", "Back Cleansing Regimen", "Black Swan", "Body Scrub",
                "Botox", "Caviar Collagen Masque", "Cosmelan", "Cosmetic Filler",
                "Diamond Ultrapeel", "Electrocautery", "Exohair", "Exosomes",
                "Facial Skin System", "Fibrolift", "Glutathione", "Glycolic Acid Peel",
                "Goldfit", "iGlow", "Intralesional Injection", "IPL - Hair Removal",
                "IPL - Skin Rejuvenation", "iRejuve", "iReplenish", "iSlim",
                "Keloid Treatment", "Laser Acne Treatment", "Laser Hair Removal",
                "Laser White", "Liftera", "Madonna Facial", "Masque De Visage",
                "Meladerm", "Meso- Rejuvenation", "Mesolift", "Mesowhite", "Milk Bath",
                "Nasolift", "Neckfirme", "Nutracell-Face", "Oxygeneo", "PINS Therapy",
                "Profhilo", "PRP", "Pure White Collagen Masque", "Reboost", "Sclerotherapy",
                "Skin Whitening System", "Skinfirme", "TCA", "Thread Lift", "Tornado Lift",
                "Ultimate Body Whitening", "Ultralift", "V-Contour", "Vitaderm", "Volite"])


    def add_appointment(self):
        if not self.member_name_input or not self.employee_name_input:
            QMessageBox.warning(None, "Selection Error", "Please select both a member and an employee.")
            return

        member_id = self.member_id_output.text()
        employee_id = self.employee_id_output.text()
        appointment_type = self.appointment_type_combo_box.currentText()
        appointment_name = self.appointment_name_combo_box.currentText()
        appointment_date = self.date.date().toString("yyyy-MM-dd")
        appointment_start_time = self.start_time.time().toString("HH:mm")
        appointment_end_time = self.end_time.time().toString("HH:mm")

        if not self.check_for_conflicts(appointment_date, appointment_start_time, appointment_end_time):
            schedule_id = "09" + str(random.randint(100000, 999999))

            cursor.execute('''
                INSERT INTO Schedule (schedule_id, member_id, employee_id, appointment_type, appointment_name, appointment_date, appointment_start_time, appointment_end_time, status)
                VALUES (?, ?, ?, ?, ?, ?, ?, ?, 'ongoing')
            ''', (schedule_id, member_id, employee_id, appointment_type, appointment_name, appointment_date, appointment_start_time, appointment_end_time))
            connection.commit()

            QMessageBox.information(None, "Yippie", "Schedule booked.")
            self.load_appointments()
            self.update_calendar()
            clear_inputs(self.schedule_page)

        else:
            QMessageBox.warning(None, "Conflict", "The selected time slot is already booked.")
    

    def check_for_conflicts(self, date, start_time, end_time):
        if validate_time(start_time, end_time):
            cursor.execute('''
                SELECT * FROM schedule
                WHERE appointment_date = ? 
                AND (
                    (
                        appointment_start_time < ? AND appointment_end_time > ?
                    )
                    OR
                    (
                        appointment_start_time < ? AND appointment_end_time > ?
                    )
                    OR
                    (
                        appointment_start_time >= ? AND appointment_end_time <= ?
                    )
                )
                AND status != "Cancelled";

            ''', (date, end_time, start_time, end_time, start_time, start_time, end_time))
            
            return False, cursor.fetchone() is not None
        return True
    def load_appointments(self):
        self.appointments_table.setRowCount(0)  # Clear existing rows

        cursor.execute('''
            SELECT s.schedule_id,
                    m.first_name || ' ' || m.last_name AS member_name, 
                   e.first_name || ' ' || e.last_name AS employee_name, 
                   s.appointment_start_time, 
                   s.appointment_end_time, 
                   s.appointment_name, 
                   s.status 
            FROM Schedule s
            JOIN Members m ON s.member_id = m.member_id
            JOIN Employees e ON s.employee_id = e.employee_id
            WHERE s.status != "Cancelled"
        ''')

        for row_number, row_data in enumerate(cursor.fetchall()):
            self.appointments_table.insertRow(row_number)
            for column_number, data in enumerate(row_data):
                item = QTableWidgetItem(str(data))  # Convert data to string for QTableWidgetItem
                self.appointments_table.setItem(row_number, column_number, item)

    def update_calendar(self):
        cursor.execute('SELECT appointment_date FROM Schedule')
        dates = set(row[0] for row in cursor.fetchall())
        fmt = QTextCharFormat()
        fmt.setBackground(QColor("lightblue"))
        self.calendar_widget.setDateTextFormat(QDate(), QTextCharFormat())  # Clear previous highlights
        for date in dates:
            qdate = QDate.fromString(date, "yyyy-MM-dd")
            self.calendar_widget.setDateTextFormat(qdate, fmt)

    def update_member_search_results(self):
        search_text = self.member_name_input.text()
        self.member_search_results.clear()

        if search_text:
            # Fetch members from database based on search text
            query = "SELECT first_name, last_name FROM Members WHERE first_name || ' ' || last_name LIKE ?"
            cursor.execute(query, ('%' + search_text + '%',))
            results = cursor.fetchall()
            # Add results to list widget
            for first_name, last_name in results:
                full_name = f"{first_name} {last_name}"
                self.member_search_results.addItem(full_name)
            self.member_search_results.show()  # Show list widget when there are results
        else:
            self.member_search_results.hide()  # Hide list widget if search text is empty


    def update_employee_search_results(self):
        search_text = self.employee_name_input.text()
        self.employee_search_results.clear()

        if search_text:
            # Fetch members from database based on search text
            query = "SELECT first_name, last_name FROM Employees WHERE first_name || ' ' || last_name LIKE ?"
            cursor.execute(query, ('%' + search_text + '%',))
            results = cursor.fetchall()
            # Add results to list widget
            for first_name, last_name in results:
                full_name = f"{first_name} {last_name}"
                self.employee_search_results.addItem(full_name)
            self.employee_search_results.show()  # Show list widget when there are results
        else:
            self.employee_search_results.hide()  # Hide list widget if search text is empty

    
    def handle_member_item_selection(self, item):
        selected_name = item.text()
        # Handle item selection (e.g., perform an action with the selected name)
        self.member_name_input.setText(selected_name)
        self.search_member(selected_name)

        self.member_search_results.hide()  # Hide list widget after selection

    def handle_employee_item_selection(self, item):
        selected_name = item.text()
        # Handle item selection (e.g., perform an action with the selected name)
        self.employee_name_input.setText(selected_name)
        self.search_employee(selected_name)

        self.employee_search_results.hide()  # Hide list widget after selection


    def search_member(self, member_input):
        # Split the full name into first name and last name
        name_parts = member_input.rsplit(' ', 1)
        
        if len(name_parts) < 2:
            print("Please enter both first name and last name.")
            return
        
        first_name = name_parts[0].strip()
        last_name = name_parts[1].strip()

        # Debug: Print the first and last name
        print(f"Searching for: first_name = '{first_name}', last_name = '{last_name}'")

        # Execute the SQL query with placeholders for the first name and last name
        cursor.execute('''
            SELECT member_id, membership_type, photo
            FROM Members
            WHERE first_name = ? AND last_name = ?
        ''', (first_name, last_name))

        # Fetch the results
        results = cursor.fetchone()

        # Check if the results are found
        if results:
            membership_id, membership_type, photo = results
            pixmap = QPixmap()
            if photo:
                pixmap.loadFromData(photo, 'PNG')  # 'PNG' is the format of the image. Change if necessary.
                self.image_output.setPixmap(pixmap)
                self.image_output.show()
            else:
                print("No photo found.")

        else:
            print("No matching member found.")

        self.member_id_output.setText(str(membership_id))
        self.membership_type_output.setText(membership_type)

    def search_employee(self, member_input):
        # Split the full name into first name and last name
        name_parts = member_input.rsplit(' ', 1)
        
        if len(name_parts) < 2:
            print("Please enter both first name and last name.")
            return
        
        first_name = name_parts[0].strip()
        last_name = name_parts[1].strip()

        # Debug: Print the first and last name
        print(f"Searching for: first_name = '{first_name}', last_name = '{last_name}'")

        # Execute the SQL query with placeholders for the first name and last name
        cursor.execute('''
            SELECT employee_id, position
            FROM Employees
            WHERE first_name = ? AND last_name = ?
        ''', (first_name, last_name))

        # Fetch the results
        results = cursor.fetchone()

        # Check if the results are found
        if results:
            employee_id, position = results

        else:
            print("No matching member found.")

        self.employee_id_output.setText(str(employee_id))
        self.position_output.setText(position)


    def cancel_appointment(self):
        selected_row = self.appointments_table.currentRow()
        if selected_row < 0:
            QMessageBox.warning(None, "No Selection", "Please select an appointment to cancel.")
            return

        appointment_id = self.appointments_table.item(selected_row, 0).text()

        cursor.execute('''
            UPDATE Schedule
            SET status = 'Cancelled'
            WHERE schedule_id = ?
        ''', (appointment_id,))
        connection.commit()
            
        QMessageBox.information(None, "Success", "Appointment canceled successfully.")
        self.load_appointments()
if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = Scheduling()
    window.show()
    sys.exit(app.exec_())
